"""Conferencia estrutural dos modelos .plecs gerados, sem executar o PLECS.

Verifica chaves balanceadas, texto ASCII, nomes unicos, parametros existentes na
biblioteca do PLECS 5.0 (desenvolvimento/blocos_biblioteca.json), extremidades de
fios e sinais, faixa de terminais por tipo, terminais eletricos ligados uma unica
vez, entradas de sinal com uma unica origem, variaveis dos parametros definidas
nos comandos de inicializacao e variaveis de ModelVars existentes no modelo.
Tambem compila o codigo do C-Script com gcc (se houver) sobre macros simuladas e
confere, pela resposta em frequencia, que a realizacao em espaco de estados do
compensador reproduz Cv(s) da planilha. Nada disso substitui carregar o modelo
no PLECS: e uma barreira contra erros de digitacao antes da execucao.
Uso: python "simulação PLECS/conferir_modelos.py"
"""
from pathlib import Path
import re, json, shutil, subprocess, tempfile, sys

SIM = Path(__file__).resolve().parent
ROOT = SIM.parent
BIB = json.loads((ROOT / 'desenvolvimento/blocos_biblioteca.json').read_text(encoding='utf-8'))
MOD = json.loads((SIM / 'modelos.json').read_text(encoding='utf-8'))
ENS = json.loads((SIM / 'ensaios.json').read_text(encoding='utf-8'))
ELETRICO = {'Resistor': 2, 'Inductor': 2, 'Capacitor': 2, 'Diode': 2, 'DCVoltageSource': 2, 'ACVoltageSource': 2,
            'Voltmeter': 2, 'Ammeter': 2, 'Switch': 2, 'MosfetWithDiode': 2, 'Ground': 1}
SAIDA_SINAL = {'Voltmeter': [3], 'Ammeter': [3], 'TriangleGenerator': [1], 'Constant': [1], 'Comparator': [3]}
ENTRADA_SINAL = {'Switch': [3], 'MosfetWithDiode': [3], 'Comparator': [1, 2], 'Output': [1]}
FUNCOES = {'sqrt', 'pi', 'inf', 'exp', 'sin', 'cos', 'double'}


def blocos(texto, tipo):
    for m in re.finditer(r'\b' + tipo + r'\s*\{', texto):
        i, nivel, aspas, esc = m.end(), 1, False, False
        while nivel and i < len(texto):
            c = texto[i]
            if aspas:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == '"':
                    aspas = False
            elif c == '"':
                aspas = True
            elif c == '{':
                nivel += 1
            elif c == '}':
                nivel -= 1
            i += 1
        yield texto[m.start():i]


def desescapa(s):
    return json.loads('"' + s + '"')


def conferir(nome):
    erros = []
    caminho = SIM / f'{nome}.plecs'
    bruto = caminho.read_bytes()
    texto = bruto.decode('ascii')
    assert texto.count('{') == texto.count('}')
    init = desescapa(re.search(r'InitializationCommands\s+"((?:[^"\\]|\\.)*)"', texto)[1])
    definidas = set(re.findall(r'(?m)(?:^|;)\s*([A-Za-z_]\w*)\s*=', init))
    comps = {}
    for b in blocos(texto, 'Component'):
        m = re.match(r'Component\s*\{\s*Type\s+(\S+)\s+Name\s+"([^"]*)"', b)
        tipo, cn = m[1], m[2]
        if cn in comps:
            erros.append(f'nome duplicado {cn}')
        params = {k: desescapa(v) for k, v in re.findall(r'Variable\s+"([^"]+)"\s+Value\s+"((?:[^"\\]|\\.)*)"', b)}
        comps[cn] = (tipo, params)
        if tipo not in BIB:
            erros.append(f'tipo sem exemplo na biblioteca: {tipo}')
        else:
            for k in params:
                if k not in BIB[tipo]['parametros']:
                    erros.append(f'{cn}: parametro {k} nao existe em {tipo}')
        if tipo != 'CScript':
            for k, v in params.items():
                for ident in re.findall(r'[A-Za-z_]\w*', v):
                    if ident not in definidas and ident not in FUNCOES and not (k in ('Windings', 'n', 'Polarity')):
                        erros.append(f'{cn}.{k}: variavel {ident} nao definida')
        else:
            for ident in re.findall(r'[A-Za-z_]\w*', params['Parameters']):
                if ident not in definidas and ident not in FUNCOES:
                    erros.append(f'{cn}.Parameters: variavel {ident} nao definida')
    usados, destinos = {}, {}
    for b in blocos(texto, 'Connection'):
        tipo_con = re.search(r'Type\s+(Wire|Signal)', b)[1]
        pinos = re.findall(r'(Src|Dst)Component\s+"([^"]*)"\s+(?:Src|Dst)Terminal\s+(\d+)', b)
        for papel, cn, t in pinos:
            t = int(t)
            if cn not in comps:
                erros.append(f'conexao para componente inexistente {cn}')
                continue
            tipo = comps[cn][0]
            if tipo_con == 'Wire':
                if tipo == 'Transformer':
                    nw = sum(int(x) for x in comps[cn][1]['Windings'].strip('[]').split())
                    ok = 1 <= t <= 2 * nw
                else:
                    ok = 1 <= t <= ELETRICO.get(tipo, 0)
                if not ok:
                    erros.append(f'{cn}: terminal eletrico {t} invalido para {tipo}')
                if (cn, t) in usados:
                    erros.append(f'{cn}:{t} ligado em dois fios')
                usados[(cn, t)] = True
            else:
                if papel == 'Dst':
                    destinos[(cn, t)] = destinos.get((cn, t), 0) + 1
    for cn, (tipo, params) in comps.items():
        if tipo == 'Transformer':
            nw = sum(int(x) for x in params['Windings'].strip('[]').split())
            n_el = 2 * nw
        else:
            n_el = ELETRICO.get(tipo, 0)
        for t in range(1, n_el + 1):
            if (cn, t) not in usados:
                erros.append(f'{cn}: terminal eletrico {t} desligado')
        entradas = ENTRADA_SINAL.get(tipo, [])
        if tipo == 'CScript':
            entradas = list(range(1, int(params['NumInputs']) + 1))
        for t in entradas:
            if destinos.get((cn, t), 0) != 1:
                erros.append(f'{cn}: entrada de sinal {t} com {destinos.get((cn, t), 0)} origens')
    idx_top = sorted(int(i) for i in re.findall(r'Terminal\s*\{\s*Type Output Index "(\d+)"', texto))
    idx_out = sorted(int(p['Index']) for t, p in comps.values() if t == 'Output')
    if idx_top != idx_out or idx_out != list(range(1, len(idx_out) + 1)):
        erros.append('terminais de saida inconsistentes')
    if len(MOD['modelos'][nome]['colunas']) != len(idx_out) + 1:
        erros.append('modelos.json nao corresponde aos terminais de saida')
    for en, e in ENS.items():
        if e['modelo'] == nome:
            for k in e['ModelVars']:
                if k not in definidas:
                    erros.append(f'{en}: ModelVar {k} nao definida nos comandos de inicializacao')
    return erros, comps


def compilar_cscript(params):
    gcc = shutil.which('gcc')
    if not gcc:
        return 'gcc ausente; compilacao nao verificada'
    mock = r'''#include <math.h>
static double _p[16]={1}; static double _x[3],_dx[3],_y[8],_z[6],_u[1]; static double CurrentTime;
#define ParamRealData(i,j) (_p[i])
#define ContState(i) (_x[i])
#define ContDeriv(i) (_dx[i])
#define OutputSignal(i,j) (_y[i])
#define ZCSignal(i) (_z[i])
#define InputSignal(i,j) (_u[i])
'''
    fonte = (mock + params['Declarations'] + '\nvoid start(void){\n' + params['StartFcn'] + '\n}\nvoid out(void){\n' +
             params['OutputFcn'] + '\n}\nvoid der(void){\n' + params['DerivativeFcn'] + '\n}\nint main(void){start();out();der();return 0;}\n')
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / 'cs.c'
        c.write_text(fonte)
        r = subprocess.run([gcc, '-std=c99', '-Wall', '-Wextra', '-Werror', '-o', str(Path(d) / 'a.out'), str(c), '-lm'],
                           capture_output=True, text=True)
        return 'compilado sem avisos (gcc -std=c99 -Wall -Wextra -Werror)' if r.returncode == 0 else 'ERRO: ' + r.stderr


def realizacao_confere():
    import numpy as np
    P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
    c = P['simulacao']['comp']
    Kc, wz1, wz2, wp1, wp2 = (c[k] for k in ('Kc', 'wz1', 'wz2', 'wp1', 'wp2'))
    # x0' = Kc e ; x1' = wp1 (x0 - x1) ; x2' = wp2 (Y2 - x2), Y2 = x0 + a1 x1 ; u = Y2 + a2 x2
    a1, a2 = wz1 / wp1 - 1, wz2 / wp2 - 1
    A = np.array([[0, 0, 0], [wp1, -wp1, 0], [wp2, wp2 * a1, -wp2]])
    B = np.array([[Kc], [0], [0]])
    C = np.array([[1.0, a1, a2]])
    f = np.logspace(0, 5.5, 400)
    h = np.array([(C @ np.linalg.solve(2j * np.pi * fi * np.eye(3) - A, B))[0, 0] for fi in f])
    s = 2j * np.pi * f
    ref = Kc * (s + wz1) * (s + wz2) / (s * (s + wp1) * (s + wp2))
    return float(np.max(np.abs(h / ref - 1)))


if __name__ == '__main__':
    relatorio, total = {}, 0
    for nome in MOD['modelos']:
        erros, comps = conferir(nome)
        total += len(erros)
        relatorio[nome] = dict(componentes=len(comps), erros=erros)
        print(nome, 'OK' if not erros else erros)
        cs = [p for t, p in comps.values() if t == 'CScript']
        if cs:
            relatorio[nome]['cscript'] = compilar_cscript(cs[0])
            print('  C-Script:', relatorio[nome]['cscript'])
    try:
        err = realizacao_confere()
        relatorio['realizacao_compensador_erro_relativo_max'] = err
        print('Realizacao do compensador: erro relativo maximo %.2e frente a Cv(s)' % err)
    except ImportError:
        relatorio['realizacao_compensador_erro_relativo_max'] = 'numpy ausente'
    (SIM / 'conferencia_modelos.json').write_text(json.dumps(relatorio, indent=1, ensure_ascii=False), encoding='utf-8')
    sys.exit(1 if total else 0)
