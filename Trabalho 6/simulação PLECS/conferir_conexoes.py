"""Confere que a mudanca de layout nao alterou nenhum componente nem nenhuma ligacao.

Compara cada modelo .plecs desta pasta com a copia guardada em layout_anterior/ (gerada
antes da reorganizacao). De cada arquivo extrai:

  - o conjunto de componentes, cada um como (tipo, nome, parametros ordenados). Position,
    Direction, Flipped e LabelPosition ficam de fora de proposito, porque sao desenho;
  - o conjunto de nos eletricos e o de nos de sinal, cada no como o conjunto de pares
    (componente, terminal) que ele liga. Nos espalhados por mais de uma conexao sao unidos
    pelas componentes conexas do grafo de pinos, de modo que a comparacao nao depende de
    como as conexoes foram quebradas em Branch;
  - os terminais Output de nivel superior e o indice de cada bloco Output.

Qualquer diferenca e listada e o programa termina com codigo 1. O resultado vai para
conferencia_conexoes.json.
Uso: python "simulação PLECS/conferir_conexoes.py"
"""
from pathlib import Path
import json, re, sys

SIM = Path(__file__).resolve().parent
ANTES = SIM / 'layout_anterior'
MOD = json.loads((SIM / 'modelos.json').read_text(encoding='utf-8'))


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


def unir(grupos):
    """Componentes conexas: cada grupo e um conjunto de pinos que uma conexao liga."""
    pai = {}

    def raiz(a):
        while pai[a] != a:
            pai[a] = pai[pai[a]]
            a = pai[a]
        return a

    for g in grupos:
        for p in g:
            pai.setdefault(p, p)
        base = raiz(next(iter(g)))
        for p in g:
            pai[raiz(p)] = base
    nos = {}
    for p in pai:
        nos.setdefault(raiz(p), set()).add(p)
    return {frozenset(v) for v in nos.values()}


def ler(caminho):
    texto = caminho.read_bytes().decode('ascii')
    comps, saidas = set(), {}
    for b in blocos(texto, 'Component'):
        m = re.match(r'Component\s*\{\s*Type\s+(\S+)\s+Name\s+"([^"]*)"', b)
        tipo, nome = m[1], m[2]
        params = tuple(sorted((k, desescapa(v)) for k, v in
                              re.findall(r'Variable\s+"([^"]+)"\s+Value\s+"((?:[^"\\]|\\.)*)"', b)))
        comps.add((tipo, nome, params))
        if tipo == 'Output':
            saidas[nome] = dict(params)['Index']
    fios, sinais = [], []
    for b in blocos(texto, 'Connection'):
        kind = re.search(r'Type\s+(Wire|Signal)', b)[1]
        pinos = {(c, int(t)) for _, c, t in
                 re.findall(r'(Src|Dst)Component\s+"([^"]*)"\s+(?:Src|Dst)Terminal\s+(\d+)', b)}
        (fios if kind == 'Wire' else sinais).append(pinos)
    topo = sorted(int(i) for i in re.findall(r'Terminal\s*\{\s*Type Output Index "(\d+)"', texto))
    return dict(componentes=comps, nos_eletricos=unir(fios), nos_de_sinal=unir(sinais),
                saidas=saidas, terminais_de_topo=topo)


def descrever(no):
    return sorted(f'{c}:{t}' for c, t in no)


def comparar(nome):
    novo, velho = ler(SIM / f'{nome}.plecs'), ler(ANTES / f'{nome}.plecs')
    dif = {}
    for chave in ('componentes', 'nos_eletricos', 'nos_de_sinal'):
        so_antes = velho[chave] - novo[chave]
        so_agora = novo[chave] - velho[chave]
        if so_antes or so_agora:
            if chave == 'componentes':
                dif[chave] = dict(so_no_anterior=sorted(f'{t} {n}' for t, n, _ in so_antes),
                                  so_no_novo=sorted(f'{t} {n}' for t, n, _ in so_agora))
            else:
                dif[chave] = dict(so_no_anterior=[descrever(x) for x in so_antes],
                                  so_no_novo=[descrever(x) for x in so_agora])
    if velho['saidas'] != novo['saidas']:
        dif['saidas'] = dict(anterior=velho['saidas'], novo=novo['saidas'])
    if velho['terminais_de_topo'] != novo['terminais_de_topo']:
        dif['terminais_de_topo'] = dict(anterior=velho['terminais_de_topo'], novo=novo['terminais_de_topo'])
    return dif, dict(componentes=len(novo['componentes']), nos_eletricos=len(novo['nos_eletricos']),
                     nos_de_sinal=len(novo['nos_de_sinal']), saidas=len(novo['saidas']))


def pontos(txt):
    m = re.search(r'Points\s+\[([^\]]*)\]', txt)
    if not m:
        return []
    return [tuple(int(float(v)) for v in par.split(',')) for par in m[1].split(';')]


def cabeca(txt):
    """Trecho de um Connection ou Branch antes do primeiro Branch filho."""
    i, prof = 0, 0
    while i < len(txt):
        if txt.startswith('Branch {', i) and prof == 0:
            return txt[:i], i
        if txt[i] == '{':
            prof += 1
        elif txt[i] == '}':
            prof -= 1
        i += 1
    return txt, len(txt)


def filhos(txt):
    """Blocos Branch do nivel imediato."""
    saida, i = [], 0
    while i < len(txt):
        if txt.startswith('Branch {', i):
            j, prof = i + 8, 1
            while prof and j < len(txt):
                if txt[j] == '{':
                    prof += 1
                elif txt[j] == '}':
                    prof -= 1
                j += 1
            saida.append(txt[i + 8:j - 1])
            i = j
        else:
            i += 1
    return saida


def polilinhas(corpo, origem, terminal_de):
    """Todas as polilinhas de uma conexao, do terminal de origem a cada destino."""
    def desce(txt, base):
        cab, _ = cabeca(txt)
        caminho = base + pontos(cab)
        d = re.search(r'DstComponent\s+"([^"]*)"\s+DstTerminal\s+(\d+)', cab)
        if d:
            yield caminho + [terminal_de(d[1], int(d[2]))], (d[1], int(d[2]))
        for f in filhos(txt):
            yield from desce(f, caminho)
    yield from desce(corpo, [origem])


def cruza(a, b, caixa):
    """O segmento a-b entra na caixa (xa, ya, xb, yb)?"""
    xa, ya, xb, yb = caixa
    if a[0] == b[0]:
        return xa < a[0] < xb and min(a[1], b[1]) < yb and max(a[1], b[1]) > ya
    return ya < a[1] < yb and min(a[0], b[0]) < xb and max(a[0], b[0]) > xa


def geometria(nome):
    """Confere, no modelo novo, que todo segmento e ortogonal e nao passa sobre bloco.

    Reconstroi a posicao de cada terminal com a mesma tabela usada para gerar (TERMINAIS
    de gerar_modelos.py), de modo que o trecho entre o ultimo Points e o terminal tambem
    entra na conta."""
    sys.path.insert(0, str(SIM))
    import gerar_modelos as gm
    texto = (SIM / f'{nome}.plecs').read_bytes().decode('ascii')
    mod = gm.Modelo(nome, '')
    for b in blocos(texto, 'Component'):
        m = re.match(r'Component \{ Type (\S+) Name "([^"]*)" Show on Position \[(-?\d+), (-?\d+)\] '
                     r'Direction (\S+) Flipped (\S+)', b)
        params = {k: desescapa(v) for k, v in
                  re.findall(r'Variable "([^"]+)" Value "((?:[^"\\]|\\.)*)"', b)}
        mod.add(m[1], m[2], int(m[3]), int(m[4]), params, m[5], m[6])
    caixas = {n: mod.caixa(n) for n in mod.pos}
    diagonais, sobre = [], []
    for b in blocos(texto, 'Connection'):
        corpo = b[b.index('{') + 1:b.rindex('}')]
        src = re.search(r'SrcComponent\s+"([^"]*)"\s+SrcTerminal\s+(\d+)', corpo)
        origem = mod.terminal(src[1], int(src[2]))[0]
        envolvidos = {src[1]} | {c for c, _ in re.findall(r'DstComponent\s+"([^"]*)"\s+DstTerminal\s+(\d+)', corpo)}
        for seq, dst in polilinhas(corpo, origem, lambda c, t: mod.terminal(c, t)[0]):
            for p, r in zip(seq, seq[1:]):
                if p[0] != r[0] and p[1] != r[1]:
                    diagonais.append([src[1], dst[0], list(p), list(r)])
                for n, cx in caixas.items():
                    if n not in envolvidos and cruza(p, r, cx):
                        sobre.append([src[1], dst[0], n, list(p), list(r)])
    return diagonais, sobre


if __name__ == '__main__':
    if not ANTES.is_dir():
        sys.exit(f'falta a pasta de referencia {ANTES}')
    relatorio, total = {}, 0
    for nome in MOD['modelos']:
        dif, tamanhos = comparar(nome)
        diagonais, sobre = geometria(nome)
        total += len(dif) + len(diagonais) + len(sobre)
        relatorio[nome] = dict(tamanhos, diferencas=dif, segmentos_em_diagonal=diagonais,
                               segmentos_sobre_bloco=sobre)
        print(nome, 'IGUAL' if not dif else 'DIFERENTE', tamanhos,
              f'diagonais: {len(diagonais)}, sobre bloco: {len(sobre)}')
        for chave, v in dif.items():
            print('  ', chave, json.dumps(v, ensure_ascii=False)[:400])
        for x in sobre[:6]:
            print('    sobre bloco:', x)
    (SIM / 'conferencia_conexoes.json').write_text(
        json.dumps(dict(referencia=str(ANTES.name), modelos=relatorio), indent=1, ensure_ascii=False), encoding='utf-8')
    print('conferencia_conexoes.json gravado;', 'sem diferencas' if not total else f'{total} problemas')
    sys.exit(1 if total else 0)
