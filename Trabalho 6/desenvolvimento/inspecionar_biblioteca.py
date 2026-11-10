"""Extrai da instalacao do PLECS 5.0 a sintaxe e a geometria dos blocos usados nos modelos.

Duas coisas vao para blocos_biblioteca.json:

1. um exemplo literal de cada tipo de bloco, com a lista de parametros aceitos, tirado dos
   demos e de components.plecs. Serve de referencia de sintaxe para gerar_modelos.py e de
   base para a conferencia de parametros de conferir_modelos.py;

2. a posicao de cada terminal no referencial do bloco (Direction right, Flipped off), medida
   nos arquivos que o proprio PLECS gravou. Num .plecs cada Connection e uma polilinha
       [terminal de origem] + Points... + [terminal de destino]
   com todos os segmentos ortogonais. Os Points estao no arquivo e os dois extremos nao, de
   modo que cada extremo impoe, contra o ponto vizinho p,
       posicao.x + deslocamento.x == p.x   ou   posicao.y + deslocamento.y == p.y
   Levando cada medida ao referencial do bloco (Direction gira, Flipped espelha ao longo do
   eixo do bloco e troca as duas pontas), as quatro direcoes somam evidencia sobre o mesmo
   deslocamento, e o candidato que satisfaz todas as restricoes e o verdadeiro. O lado de
   cada terminal sai de uma votacao a parte: num esquema limpo o fio nao atravessa o corpo
   do bloco, logo o ponto vizinho esta do mesmo lado que o terminal.

   Transformer e CScript mudam de tamanho com os parametros (Windings, NumInputs e
   NumOutputs), entao a medida e feita por valor de parametro e o resultado aparece como
   regra em gerar_modelos.py (term_transformador e term_cscript).

Uso: python desenvolvimento/inspecionar_biblioteca.py [caminho_da_instalacao]
"""
from pathlib import Path
import re, json, sys, collections

PADRAO = Path(r'C:\Users\josem\OneDrive - L2M Power Electronics\Documentos\Plexim\PLECS 5.0 (64 bit)')
INSTALL = Path(sys.argv[1]) if len(sys.argv) > 1 else PADRAO
TIPOS = ['ACVoltageSource', 'DCVoltageSource', 'Switch', 'Ammeter', 'Voltmeter', 'Resistor', 'Inductor', 'Capacitor',
         'Diode', 'MosfetWithDiode', 'Transformer', 'Ground', 'TriangleGenerator', 'Comparator', 'Constant', 'CScript', 'Output']
GRADE = [(dx, dy) for dx in range(-80, 81, 5) for dy in range(-80, 81, 5)]
GIRO = dict(right=lambda x, y: (x, y), down=lambda x, y: (-y, x),
            left=lambda x, y: (-x, -y), up=lambda x, y: (y, -x))
VOLTA = dict(right=lambda x, y: (x, y), down=lambda x, y: (y, -x),
             left=lambda x, y: (-x, -y), up=lambda x, y: (-y, x))


def blocos(texto, palavra='Component'):
    for m in re.finditer(r'(?<![A-Za-z])' + palavra + r'\s*\{', texto):
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
        yield m.start(), i, texto[m.end():i - 1]


def nivel_imediato(corpo, palavra):
    fora = []
    for a, b, c in blocos(corpo, palavra):
        if not any(x < a and b <= y for x, y, _ in fora):
            fora.append((a, b, c))
    return fora


def campo(corpo, chave, aspas=True):
    p = rf'(?m)^\s*{chave}\s+"([^"]*)"' if aspas else rf'(?m)^\s*{chave}\s+(\S+)'
    m = re.search(p, corpo)
    return m[1] if m else None


def pontos(texto):
    m = re.search(r'(?m)^\s*Points\s+\[([^\]]*)\]', texto)
    if not m:
        return []
    saida = []
    for par in m[1].split(';'):
        v = par.split(',')
        if len(v) == 2:
            saida.append((int(float(v[0])), int(float(v[1]))))
    return saida


def aplicar(d, flip, o):
    x, y = o
    if flip == 'on':
        x = -x
    return GIRO[d](x, y)


def desaplicar(d, flip, v):
    x, y = VOLTA[d](*v)
    return (-x, y) if flip == 'on' else (x, y)


def forma(tipo, corpo):
    c = corpo.replace('\n', ' ')
    if tipo == 'Transformer':
        w = re.search(r'Variable\s+"Windings"\s*Value\s+"([^"]*)"', c)
        return w[1].strip() if w else '?'
    if tipo == 'CScript':
        ni = re.search(r'Variable\s+"NumInputs"\s*Value\s+"([^"]*)"', c)
        no = re.search(r'Variable\s+"NumOutputs"\s*Value\s+"([^"]*)"', c)
        return f"{ni[1] if ni else '?'}/{no[1] if no else '?'}"
    return ''


def ler_esquema(corpo, restricoes, votos, por_forma):
    comps = {}
    for a, b, c in nivel_imediato(corpo, 'Component'):
        tipo, nome = campo(c, 'Type', False), campo(c, 'Name')
        pos = re.search(r'(?m)^\s*Position\s+\[\s*([-\d.]+),\s*([-\d.]+)\s*\]', c)
        if tipo and nome is not None and pos:
            comps[nome] = (tipo, (int(float(pos[1])), int(float(pos[2]))),
                           campo(c, 'Direction', False) or 'right',
                           campo(c, 'Flipped', False) or 'off', forma(tipo, c))
        for _, _, sub in nivel_imediato(c, 'Schematic'):
            ler_esquema(sub, restricoes, votos, por_forma)
    for a, b, c in nivel_imediato(corpo, 'Connection'):
        src, st = campo(c, 'SrcComponent'), campo(c, 'SrcTerminal', False)
        if src is None or st is None or src not in comps:
            continue
        ramos = nivel_imediato(c, 'Branch')
        cab = c if not ramos else c[:min(x for x, _, _ in ramos)]
        raiz, folhas = pontos(cab), []

        def desce(txt, cam):
            cam = cam + pontos(txt)
            d, dt = campo(txt, 'DstComponent'), campo(txt, 'DstTerminal', False)
            if d is not None and dt is not None:
                folhas.append((d, dt, cam))
            for _, _, s in nivel_imediato(txt, 'Branch'):
                desce(s, cam)
        if ramos:
            for _, _, r in ramos:
                desce(r, raiz)
        else:
            d, dt = campo(c, 'DstComponent'), campo(c, 'DstTerminal', False)
            if d is not None and dt is not None:
                folhas.append((d, dt, raiz))
        ts, ps, ds, fs, hs = comps[src]
        for d, dt, cam in folhas:
            if d not in comps or not cam:
                continue
            if any(p[0] != r[0] and p[1] != r[1] for p, r in zip(cam, cam[1:])):
                continue                      # polilinha ja em diagonal: nao serve de medida
            td, pd, dd, fd, hd = comps[d]
            for tipo, term, dirc, flip, pos, pt, h in ((ts, int(st), ds, fs, ps, cam[0], hs),
                                                       (td, int(dt), dd, fd, pd, cam[-1], hd)):
                restricoes[(tipo, term)].append((dirc, flip, pos, pt))
                por_forma[(tipo, h, term)].append((dirc, flip, pos, pt))
                vx, _ = desaplicar(dirc, flip, (pt[0] - pos[0], pt[1] - pos[1]))
                if vx:
                    votos[(tipo, term)][1 if vx > 0 else -1] += 1


def ajustar(lista):
    bons, melhor = [], -1
    for ob in GRADE:
        n = 0
        for d, f, pos, pt in lista:
            o = aplicar(d, f, ob)
            if pos[0] + o[0] == pt[0] or pos[1] + o[1] == pt[1]:
                n += 1
        if n > melhor:
            bons, melhor = [ob], n
        elif n == melhor:
            bons.append(ob)
    return bons, melhor


def arquivos():
    saida = sorted((INSTALL / 'demos').rglob('*.plecs'))
    for extra in ('examples', 'tsps', 'wbstoolbox', 'toolbox'):
        if (INSTALL / extra).is_dir():
            saida += sorted((INSTALL / extra).rglob('*.plecs'))
    for nome in ('components.plecs', 'deprecated.plecs', 'spicelib.plecs'):
        if (INSTALL / nome).is_file():
            saida.append(INSTALL / nome)
    return saida


if __name__ == '__main__':
    if not INSTALL.is_dir():
        sys.exit(f'instalacao do PLECS nao encontrada em {INSTALL}')
    achados = {}
    for p in [*sorted((INSTALL / 'demos').rglob('*.plecs')), INSTALL / 'components.plecs']:
        for _, _, b in blocos(p.read_text(encoding='utf-8', errors='replace')):
            pass
    for p in [*sorted((INSTALL / 'demos').rglob('*.plecs')), INSTALL / 'components.plecs']:
        texto = p.read_text(encoding='utf-8', errors='replace')
        for inicio, fim, _ in blocos(texto):
            b = texto[inicio:fim]
            m = re.match(r'Component\s*\{\s*Type\s+(\S+)', b)
            if m and m[1] in TIPOS and m[1] not in achados and len(b) < 30000:
                achados[m[1]] = dict(fonte=str(p.relative_to(INSTALL)).replace('\\', '/'),
                                     parametros=re.findall(r'Variable\s+"([^"]+)"', b), bloco=b)
        if len(achados) == len(TIPOS):
            break

    restricoes = collections.defaultdict(list)
    votos = collections.defaultdict(collections.Counter)
    por_forma = collections.defaultdict(list)
    lidos = arquivos()
    for p in lidos:
        t = p.read_text(encoding='utf-8', errors='replace').replace('\r\n', '\n')
        for _, _, corpo in nivel_imediato(t, 'Schematic'):
            ler_esquema(corpo, restricoes, votos, por_forma)

    geometria = {}
    for (tipo, term), lista in sorted(restricoes.items()):
        if tipo not in TIPOS or tipo in ('Transformer', 'CScript'):
            continue
        cand, ok = ajustar(lista)
        c = votos[(tipo, term)]
        lado = 1 if c[1] >= c[-1] else -1
        geometria.setdefault(tipo, {})[f't{term}'] = dict(
            deslocamento=list(cand[0]) if len(cand) == 1 else None,
            candidatos=[list(x) for x in cand[:4]], restricoes=len(lista), satisfeitas=ok,
            lado_do_eixo='+x' if lado > 0 else '-x',
            votos_do_lado=dict(mais=c[1], menos=c[-1]))
    por_param = {}
    for (tipo, h, term), lista in sorted(por_forma.items()):
        if tipo not in ('Transformer', 'CScript') or len(lista) < 4:
            continue
        cand, ok = ajustar(lista)
        por_param.setdefault(tipo, {}).setdefault(h, {})[f't{term}'] = dict(
            candidatos=[list(x) for x in cand[:4]], restricoes=len(lista), satisfeitas=ok)

    saida = Path(__file__).parent / 'blocos_biblioteca.json'
    saida.write_text(json.dumps(dict(
        instalacao=str(INSTALL), arquivos_lidos=len(lidos),
        metodo=('Deslocamento de cada terminal no referencial do bloco (Direction right, Flipped off), '
                'medido pela ortogonalidade das polilinhas dos arquivos .plecs da instalacao. '
                'Transformer e CScript aparecem por valor de Windings e de NumInputs/NumOutputs, '
                'porque mudam de tamanho com esses parametros.'),
        blocos=achados, geometria_dos_terminais=geometria,
        geometria_por_parametro=por_param), indent=1, ensure_ascii=False), encoding='utf-8')
    for t in TIPOS:
        g = geometria.get(t, {})
        resumo = ' '.join(f"{k}={v['deslocamento']}" for k, v in g.items()) if g else 'por parametro'
        print(f"{t:18s} {achados.get(t, {}).get('fonte', 'NAO ENCONTRADO'):60s} {resumo}")
    print(len(lidos), 'arquivos lidos;', saida.name, 'gravado')
