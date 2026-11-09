"""Executa os ensaios do Trabalho 6 SOMENTE no PLECS, via XML-RPC (porta 1080).

Usa apenas a biblioteca padrao do Python (xmlrpc.client, json, gzip, csv, hashlib),
para rodar em qualquer Python do Windows sem instalar pacotes.
Pre-requisitos: PLECS Standalone aberto, com File > PLECS Preferences > General >
RPC interface habilitada na porta 1080, e os modelos gerados por
"simulação PLECS/gerar_modelos.py" (a matriz de ensaios esta em ensaios.json).

Uso (na pasta Trabalho 6):
  python "resultados PLECS/executar_ensaios.py" --teste            carrega cada modelo e simula 2 ms
  python "resultados PLECS/executar_ensaios.py" --ensaio nb_176_nl  um ensaio (pode repetir --ensaio)
  python "resultados PLECS/executar_ensaios.py" --grupo regulacao   um grupo inteiro
  python "resultados PLECS/executar_ensaios.py" --todos             matriz completa
Opcoes: --forcar repete ensaios ja executados; --paralelo N agrupa ensaios de regulacao
em lotes de N simulacoes paralelas do PLECS (padrao 11; use 1 para sequencial);
--url muda o endereco do servidor RPC.
Cada simulacao recebe SolverOpts.Timeout (segundos de relogio, definido por ensaio em
ensaios.json): se o PLECS nao terminar nesse prazo, o ensaio e registrado como falha e a
execucao segue para o proximo. Ctrl+C interrompe e marca o ensaio em curso como interrompido.

Para cada ensaio sao gravados <nome>.csv, <nome>_rpc.json.gz (retorno nativo) e
<nome>_execucao.json (data, versao, hash do modelo, ModelVars, solver, duracao,
amostras, colunas, hash do CSV e status). Falhas sao registradas com a mensagem
do PLECS e nenhum resultado ficticio e criado.
"""
from pathlib import Path
import argparse, csv, datetime, gzip, hashlib, json, socket, sys, time, xmlrpc.client

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
SIM = ROOT / 'simulação PLECS'
ENS = json.loads((SIM / 'ensaios.json').read_text(encoding='utf-8'))
MOD = json.loads((SIM / 'modelos.json').read_text(encoding='utf-8'))
socket.setdefaulttimeout(max(e.get('Timeout', 600) for e in ENS.values()) + 600)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def agora():
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def tempos(faixas):
    """Uniao ordenada das grades [inicio, fim, passo], sem duplicatas numericas."""
    ts = set()
    for a, b, p in faixas:
        n = int(round((b - a) / p))
        for k in range(n + 1):
            ts.add(round(a + k * p, 10))
    return sorted(ts)


def opcoes(e, teste=False):
    sol = MOD['solver']
    stop = 0.002 if teste else e['TimeSpan']
    mv = dict(e['ModelVars'], Tstop=stop)
    so = dict(TimeSpan=stop, Solver=sol['Solver'], MaxStep=float(e.get('MaxStep', sol['MaxStep'])),
              RelTol=float(e.get('RelTol', sol['RelTol'])), AbsTol=float(sol['AbsTol']))
    if teste:
        so['OutputTimes'] = tempos([[0.0, stop, 1e-5]])
    else:
        so['OutputTimes'] = tempos(e['grade'])
    so['OutputTimesOption'] = 'specified'
    so['Timeout'] = float(min(e.get('Timeout', 600), 120) if teste else e.get('Timeout', 600))
    return dict(ModelVars=mv, SolverOpts=so)


def resumo_opcoes(op):
    so = {k: v for k, v in op['SolverOpts'].items() if k != 'OutputTimes'}
    so['OutputTimes_n'] = len(op['SolverOpts']['OutputTimes'])
    return dict(ModelVars=op['ModelVars'], SolverOpts=so)


def assinatura(e):
    """Hash das opcoes que afetam o resultado (o Timeout fica de fora)."""
    r = resumo_opcoes(opcoes(e))
    r['SolverOpts'].pop('Timeout', None)
    return hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()


class Servidor:
    def __init__(self, url):
        self.p = xmlrpc.client.ServerProxy(url, allow_none=True)
        self.carregados = {}

    def carregar(self, modelo):
        caminho = SIM / f'{modelo}.plecs'
        h = sha(caminho)
        if self.carregados.get(modelo) != h:
            try:
                self.p.plecs.close(modelo)
            except Exception:
                pass
            self.p.plecs.load(str(caminho.resolve()).replace('\\', '/'))
            self.carregados[modelo] = h
        return h

    def simular(self, modelo, op):
        return self.p.plecs.simulate(modelo, op)


def gravar_resultado(nome, e, dados, rec):
    with gzip.open(OUT / f'{nome}_rpc.json.gz', 'wt', encoding='utf-8') as f:
        json.dump(dados, f, separators=(',', ':'))
    t = dados['Time']
    v = dados['Values']
    if v and not isinstance(v[0], list):
        v = [v]
    if len(v) == len(t) and (not v or len(v[0]) != len(t)):
        v = [list(c) for c in zip(*v)]          # chega como tempo x sinais: transpoe
    colunas = MOD['modelos'][e['modelo']]['colunas']
    if len(v) != len(colunas) - 1:
        raise RuntimeError(f'{len(v)} sinais retornados, {len(colunas) - 1} esperados')
    for linha in v:
        if len(linha) != len(t):
            raise RuntimeError('sinais com comprimentos diferentes')
        for x in linha:
            if x != x or x in (float('inf'), float('-inf')):
                raise RuntimeError('valor nao finito no retorno do PLECS')
    arq = OUT / f'{nome}.csv'
    with open(arq, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(colunas)
        for k in range(len(t)):
            w.writerow([f'{t[k]:.10g}'] + [f'{s[k]:.10g}' for s in v])
    rec.update(status='executado', amostras=len(t), colunas=colunas, sha256_csv=sha(arq),
               tempo_inicial_s=float(t[0]), tempo_final_s=float(t[-1]), fim=agora())


def registro(nome, e, h, op, versao):
    return dict(ensaio=nome, descricao=e['descricao'], grupo=e['grupo'], modelo=e['modelo'], sha256_modelo=h,
                inicio=agora(), PLECS=versao, opcoes=resumo_opcoes(op), assinatura_opcoes=assinatura(e),
                grade_saida=e['grade'], janelas=e['janelas'], status='iniciado')


def executar(srv, nomes, versao, paralelo=11):
    falhas = []
    # agrupa ensaios de regulacao do mesmo modelo para simulacao paralela
    lotes, atual = [], []
    for n in nomes:
        if paralelo > 1 and ENS[n]['grupo'].startswith('regulacao'):
            atual.append(n)
            if len(atual) == paralelo:
                lotes.append(atual)
                atual = []
        else:
            lotes.append([n])
    if atual:
        lotes.append(atual)
    for lote in lotes:
        modelo = ENS[lote[0]]['modelo']
        try:
            h = srv.carregar(modelo)
        except Exception as ex:
            for n in lote:
                falhas.append(n)
                rec = dict(ensaio=n, modelo=modelo, status='falhou', erro='load: ' + repr(ex), inicio=agora(), PLECS=versao)
                (OUT / f'{n}_execucao.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
                print(n, 'FALHOU ao carregar', repr(ex), flush=True)
            continue
        ops = [opcoes(ENS[n]) for n in lote]
        recs = [registro(n, ENS[n], h, op, versao) for n, op in zip(lote, ops)]
        for n, rec in zip(lote, recs):
            (OUT / f'{n}_execucao.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
        print(f"{datetime.datetime.now():%H:%M:%S} iniciando {', '.join(lote)} (limite {ops[0]['SolverOpts']['Timeout']:.0f} s)", flush=True)
        t0 = time.monotonic()
        try:
            res = srv.simular(modelo, ops if len(lote) > 1 else ops[0])
            if len(lote) == 1:
                res = [res]
            elif not isinstance(res, list) or len(res) != len(lote):
                raise RuntimeError('retorno inesperado da simulacao paralela')
        except Exception as ex:
            if len(lote) > 1:
                print('lote paralelo falhou (' + str(ex)[:200] + '); repetindo em sequencia', flush=True)
                res = []
                for op in ops:
                    try:
                        res.append(srv.simular(modelo, op))
                    except Exception as ex2:
                        res.append(repr(ex2))
            else:
                res = [repr(ex)]
        except KeyboardInterrupt:
            for n, rec in zip(lote, recs):
                rec.update(status='interrompido', erro='interrompido pelo usuario (Ctrl+C)', fim=agora(),
                           duracao_real_s=round(time.monotonic() - t0, 3))
                (OUT / f'{n}_execucao.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
            print('interrompido; o ensaio em curso foi marcado como interrompido. Pare a simulacao no PLECS se ela continuar.', flush=True)
            raise SystemExit(130)
        dur = time.monotonic() - t0
        for n, rec, r in zip(lote, recs, res):
            rec['duracao_real_s'] = round(dur, 3)
            if len(lote) > 1:
                rec['lote_paralelo'] = lote
            try:
                if not isinstance(r, dict):
                    raise RuntimeError(str(r))
                gravar_resultado(n, ENS[n], r, rec)
                print(f"{n}: executado, {rec['amostras']} amostras, {dur:.1f} s", flush=True)
            except Exception as ex:
                rec.update(status='falhou', erro=str(ex)[:4000], fim=agora())
                falhas.append(n)
                print(n, 'FALHOU', str(ex)[:500], flush=True)
            (OUT / f'{n}_execucao.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
    return falhas


def teste(srv, versao):
    """Carrega cada modelo e simula 2 ms com o primeiro ensaio do modelo; grava em testes/."""
    pasta = OUT / 'testes'
    pasta.mkdir(exist_ok=True)
    falhas = []
    for modelo in MOD['modelos']:
        nome = next(n for n, e in ENS.items() if e['modelo'] == modelo)
        rec = dict(modelo=modelo, ensaio_base=nome, inicio=agora(), PLECS=versao)
        try:
            rec['sha256_modelo'] = srv.carregar(modelo)
            t0 = time.monotonic()
            d = srv.simular(modelo, opcoes(ENS[nome], teste=True))
            rec.update(status='carregou e simulou 2 ms', duracao_real_s=round(time.monotonic() - t0, 3),
                       amostras=len(d['Time']), sinais=len(d['Values']) if d['Values'] and isinstance(d['Values'][0], list) else 1)
            print(modelo, 'OK:', rec['status'], flush=True)
        except Exception as ex:
            rec.update(status='falhou', erro=str(ex)[:4000])
            falhas.append(modelo)
            print(modelo, 'FALHOU:', str(ex)[:800], flush=True)
        (pasta / f'teste_{modelo}.json').write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8')
    return falhas


def ja_executado(nome):
    log = OUT / f'{nome}_execucao.json'
    if not log.exists():
        return False
    r = json.loads(log.read_text(encoding='utf-8'))
    e = ENS[nome]
    csvp = OUT / f'{nome}.csv'
    return (r.get('status') == 'executado' and r.get('sha256_modelo') == sha(SIM / f"{e['modelo']}.plecs")
            and r.get('assinatura_opcoes') == assinatura(e) and csvp.exists() and r.get('sha256_csv') == sha(csvp))


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--teste', action='store_true')
    a.add_argument('--ensaio', action='append', choices=sorted(ENS), default=[])
    a.add_argument('--grupo', action='append', default=[])
    a.add_argument('--todos', action='store_true')
    a.add_argument('--forcar', action='store_true')
    a.add_argument('--paralelo', type=int, default=11)
    a.add_argument('--url', default='http://localhost:1080')
    a.add_argument('--versao', default='PLECS Standalone 5.0 (64 bit), formato 5.0; 5.0.6 segundo o registro do Trabalho 4')
    args = a.parse_args()
    srv = Servidor(args.url)
    try:
        srv.p.system.listMethods()
    except Exception as ex:
        print('PLECS nao respondeu em', args.url, '->', repr(ex))
        print('Abra o PLECS e habilite File > PLECS Preferences > General > RPC interface (porta 1080).')
        sys.exit(2)
    if args.teste:
        f = teste(srv, args.versao)
        sys.exit(1 if f else 0)
    nomes = list(ENS) if args.todos else [n for n in ENS if n in args.ensaio or ENS[n]['grupo'] in args.grupo]
    if not nomes:
        a.error('indique --teste, --ensaio, --grupo ou --todos')
    pendentes = []
    for n in nomes:
        if not args.forcar and ja_executado(n):
            print(n, 'ja executado com este modelo e estas opcoes; preservado', flush=True)
        else:
            pendentes.append(n)
    falhas = executar(srv, pendentes, args.versao, max(1, args.paralelo))
    resumo = dict(data=agora(), solicitados=nomes, executados_agora=[n for n in pendentes if n not in falhas], falhas=falhas)
    (OUT / 'resumo_ultima_execucao.json').write_text(json.dumps(resumo, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'{len(pendentes) - len(falhas)} executados, {len(falhas)} falhas, {len(nomes) - len(pendentes)} preservados.')
    sys.exit(1 if falhas else 0)
