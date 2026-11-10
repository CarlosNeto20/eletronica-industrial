"""Monta o artigo IEEE A4 a partir do template OOXML Strict, sem alterar estilos.

Le o texto de conteudo.py (que tira todos os numeros de parametros.json e metricas.json),
substitui apenas o corpo de word/document.xml, acrescenta as figuras em word/media e
registra as relacoes e o tipo PNG. styles.xml, numbering.xml, theme e as demais partes
do template sao copiados byte a byte. Equacoes sao OMML nativas (editaveis no Word).
Uso: python artigo/fonte/gerar_artigo.py
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
import re, struct, json, hashlib, sys
from lxml import etree as E

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conteudo as C

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'artigo'
QA = OUT / 'qa'
QA.mkdir(exist_ok=True)
TPL = ROOT / 'documentos de referência' / 'template-a4.docx'
SHA_TPL = '9d0153f7121508f585eff77c6fc112234a9d289c0390bf54a5296d15d01b04d3'
NS = {'w': 'http://purl.oclc.org/ooxml/wordprocessingml/main',
      'm': 'http://purl.oclc.org/ooxml/officeDocument/math',
      'r': 'http://purl.oclc.org/ooxml/officeDocument/relationships',
      'wp': 'http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing',
      'a': 'http://purl.oclc.org/ooxml/drawingml/main',
      'pic': 'http://purl.oclc.org/ooxml/drawingml/picture'}
LARGURA_PT = 234.0
# largura util da pagina (A4 menos as margens do corpo), para as figuras que ocupam as duas
# colunas, como o modelo IEEE faz com os esquemas de circuito
LARGURA_TOTAL = 500.0


def no(tag, attrs=None, text=None):
    pre, key = tag.split(':')
    o = E.Element('{' + NS[pre] + '}' + key)
    for k, v in (attrs or {}).items():
        if ':' in k:
            a, b = k.split(':')
            k = '{' + NS[a] + '}' + b
        o.set(k, str(v))
    if text is not None:
        o.text = text
    return o


def add(pai, tag, attrs=None, text=None):
    o = no(tag, attrs, text)
    pai.append(o)
    return o


def serial(x):
    return E.tostring(x, encoding='UTF-8', xml_declaration=True, standalone=True)


def run(txt, size=None, bold=False, italic=False, sub=False, sup=False):
    r = no('w:r')
    pr = add(r, 'w:rPr')
    if bold:
        add(pr, 'w:b')
    if italic:
        add(pr, 'w:i')
    add(pr, 'w:color', {'w:val': '000000'})
    if size:
        add(pr, 'w:sz', {'w:val': round(2 * size)})
    if sub or sup:
        add(pr, 'w:vertAlign', {'w:val': 'subscript' if sub else 'superscript'})
    add(pr, 'w:lang', {'w:val': 'pt-BR'})
    t = add(r, 'w:t', text=txt)
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r


def runs_marcados(texto, size=None):
    """Texto com marcacao leve: _{x} subscrito, ^{x} sobrescrito, *x* italico."""
    out = []
    for parte in re.split(r'(_\{[^}]*\}|\^\{[^}]*\}|\*[^*]+\*)', texto):
        if not parte:
            continue
        if parte.startswith('_{'):
            out.append(run(parte[2:-1], size, sub=True))
        elif parte.startswith('^{'):
            out.append(run(parte[2:-1], size, sup=True))
        elif parte.startswith('*') and parte.endswith('*') and len(parte) > 2:
            out.append(run(parte[1:-1], size, italic=True))
        else:
            out.append(run(parte, size))
    return out


def para(text='', style='BodyText', align=None, keep=False, size=None, after=None, first=None, before=None,
         linha=None, regra=None, keeplines=False):
    """Paragrafo com pPr na ordem do esquema OOXML (pStyle, keepNext, keepLines, widowControl,
    numPr, spacing, ind, jc). linha/regra permitem espacamento 'atLeast' para figuras e equacoes."""
    p = no('w:p')
    pr = add(p, 'w:pPr')
    add(pr, 'w:pStyle', {'w:val': style})
    if keep:
        add(pr, 'w:keepNext')
    if keeplines:
        add(pr, 'w:keepLines')
    add(pr, 'w:widowControl')
    num = add(pr, 'w:numPr')
    add(num, 'w:numId', {'w:val': 0})
    if after is not None or before is not None or linha is not None:
        sp = add(pr, 'w:spacing')
        if before is not None:
            sp.set('{' + NS['w'] + '}before', f'{before}pt')
        if after is not None:
            sp.set('{' + NS['w'] + '}after', f'{after}pt')
        if linha is not None:
            sp.set('{' + NS['w'] + '}line', f'{linha}pt')
            sp.set('{' + NS['w'] + '}lineRule', regra or 'atLeast')
    if first is not None:
        add(pr, 'w:ind', {'w:firstLine': f'{first}pt', 'w:start': '0pt', 'w:end': '0pt'})
    if align:
        add(pr, 'w:jc', {'w:val': align})
    if text:
        p.extend(runs_marcados(text, size))
    return p


# --- equacoes OMML: \frac{a}{b}, \sqrt{x}, x_{i}, x^{2}, {grupos} -----------------
def mathparse(s):
    i = 0

    def mr(t):
        r = no('m:r')
        pr = add(r, 'w:rPr')
        add(pr, 'w:rFonts', {'w:ascii': 'Cambria Math', 'w:hAnsi': 'Cambria Math'})
        add(pr, 'w:sz', {'w:val': 19})
        add(r, 'm:t', text=t)
        return r

    def grupo():
        nonlocal i
        if i < len(s) and s[i] == '{':
            i += 1
            v = seq('}')
            i += 1
            return v
        if i < len(s):
            c = s[i]
            i += 1
            return [mr(c)]
        return []

    def seq(fim=None):
        nonlocal i
        out = []
        while i < len(s) and s[i] != fim:
            if s.startswith('\\frac', i):
                i += 5
                nu, de = grupo(), grupo()
                f = no('m:f')
                n = add(f, 'm:num')
                n.extend(nu)
                d = add(f, 'm:den')
                d.extend(de)
                out.append(f)
            elif s.startswith('\\sqrt', i):
                i += 5
                arg = grupo()
                rad = no('m:rad')
                rp = add(rad, 'm:radPr')
                add(rp, 'm:degHide', {'m:val': 'on'})
                add(rad, 'm:deg')
                e = add(rad, 'm:e')
                e.extend(arg)
                out.append(rad)
            elif s[i] == '^' and out and E.QName(out[-1]).localname == 'sSub':
                i += 1
                g = grupo()
                base = out.pop()
                t = no('m:sSubSup')
                e = add(t, 'm:e')
                e.extend(list(base.find('m:e', NS)))
                q = add(t, 'm:sub')
                q.extend(list(base.find('m:sub', NS)))
                q = add(t, 'm:sup')
                q.extend(g)
                out.append(t)
            elif s[i] in '_^':
                op = s[i]
                i += 1
                g = grupo()
                base = out.pop()
                t = no('m:sSub' if op == '_' else 'm:sSup')
                e = add(t, 'm:e')
                e.append(base)
                q = add(t, 'm:sub' if op == '_' else 'm:sup')
                q.extend(g)
                out.append(t)
            elif s[i] == '{':
                out.extend(grupo())
            else:
                out.append(mr(s[i]))
                i += 1
        return out
    return seq()


def equacao(text, n):
    p = para('', style='equation', align='center', first=0, before=3, after=5, linha=12, keeplines=True)
    mp = add(p, 'm:oMathPara')
    mpp = add(mp, 'm:oMathParaPr')
    add(mpp, 'm:jc', {'m:val': 'center'})
    om = add(mp, 'm:oMath')
    om.extend(mathparse(text))
    rr = add(om, 'm:r')
    add(rr, 'm:t', text=f' ({n})')
    return p


with ZipFile(TPL) as z:
    pkg = {n: z.read(n) for n in z.namelist()}
doc = E.fromstring(pkg['word/document.xml'])
body = doc.find('w:body', NS)
secs = body.findall('.//w:sectPr', NS)
sec_titulo = deepcopy(secs[0])
sec_corpo = deepcopy(next(s for s in secs if s.find('w:cols', NS) is not None and s.find('w:cols', NS).get('{' + NS['w'] + '}num') == '2'))
for sec in (sec_titulo, sec_corpo):
    for el in list(sec):
        if E.QName(el).localname in ('headerReference', 'footerReference', 'titlePg'):
            sec.remove(el)
    for k in list(sec.attrib):
        del sec.attrib[k]
for el in list(body):
    body.remove(el)

body.append(para(C.TITULO, 'papertitle', align='center', keep=True, first=0))
for a in C.AUTORES:
    body.append(para(a, 'Author', align='center', keep=True, first=0, after=1, before=0))
for linha in C.AFILIACAO[:-1]:
    body.append(para(linha, 'Author', align='center', keep=True, first=0, size=9, after=1, before=0))
ult = para(C.AFILIACAO[-1], 'Author', align='center', first=0, size=9, after=12, before=0)
ult[0].append(sec_titulo)
body.append(ult)
r = para('', 'Abstract', first=0, after=6)
r.append(run('Resumo', bold=True, italic=True))
r.extend(runs_marcados('. ' + C.RESUMO))
body.append(r)
k = para('', 'Keywords', first=0, after=6)
k.append(run('Palavras-chave', bold=True, italic=True))
k.extend(runs_marcados('. ' + C.PALAVRAS))
body.append(k)

rels = E.fromstring(pkg['word/_rels/document.xml.rels'])
rns = E.QName(rels).namespace
ct = E.fromstring(pkg['[Content_Types].xml'])
ctns = E.QName(ct).namespace
if not any(e.get('Extension') == 'png' for e in ct):
    E.SubElement(ct, '{' + ctns + '}Default', Extension='png', ContentType='image/png')


def figura(caminho, nf, largura=LARGURA_PT):
    blob = Path(caminho).read_bytes()
    pw, ph = struct.unpack('>II', blob[16:24])
    cx = round(largura * 12700)
    cy = round(cx * ph / pw)
    rid = f'rIdArtigo{nf}'
    alvo = f'media/artigo_fig_{nf}.png'
    pkg['word/' + alvo] = blob
    E.SubElement(rels, '{' + rns + '}Relationship', Id=rid, Type=NS['r'] + '/image', Target=alvo)
    p = para('', align='center', keep=True, first=0, after=0, before=2, linha=12)
    r = add(p, 'w:r')
    dr = add(r, 'w:drawing')
    inl = add(dr, 'wp:inline', {'distT': 0, 'distB': 0, 'distL': 0, 'distR': 0})
    add(inl, 'wp:extent', {'cx': cx, 'cy': cy})
    nome = Path(caminho).stem
    add(inl, 'wp:docPr', {'id': 1000 + nf, 'name': nome, 'descr': nome.replace('_', ' ')})
    g = add(inl, 'a:graphic')
    gd = add(g, 'a:graphicData', {'uri': NS['pic']})
    pic = add(gd, 'pic:pic')
    nv = add(pic, 'pic:nvPicPr')
    add(nv, 'pic:cNvPr', {'id': 1000 + nf, 'name': nome})
    add(nv, 'pic:cNvPicPr')
    bf = add(pic, 'pic:blipFill')
    add(bf, 'a:blip', {'r:embed': rid})
    st = add(bf, 'a:stretch')
    add(st, 'a:fillRect')
    sp = add(pic, 'pic:spPr')
    xf = add(sp, 'a:xfrm')
    add(xf, 'a:off', {'x': 0, 'y': 0})
    add(xf, 'a:ext', {'cx': cx, 'cy': cy})
    pg = add(sp, 'a:prstGeom', {'prst': 'rect'})
    add(pg, 'a:avLst')
    return p


def tabela(linhas, larguras):
    ws = [round(w * LARGURA_PT * 20) for w in larguras]
    t = no('w:tbl')
    pr = add(t, 'w:tblPr')
    add(pr, 'w:tblW', {'w:w': sum(ws), 'w:type': 'dxa'})
    add(pr, 'w:jc', {'w:val': 'center'})
    bd = add(pr, 'w:tblBorders')
    for borda in ('top', 'bottom', 'insideH'):
        add(bd, 'w:' + borda, {'w:val': 'single', 'w:sz': 4, 'w:color': '888888'})
    add(pr, 'w:tblLayout', {'w:type': 'fixed'})
    mar = add(pr, 'w:tblCellMar')
    for borda, val in (('top', 25), ('bottom', 25), ('start', 45), ('end', 45)):
        add(mar, 'w:' + borda, {'w:w': val, 'w:type': 'dxa'})
    gr = add(t, 'w:tblGrid')
    for w in ws:
        add(gr, 'w:gridCol', {'w:w': w})
    for ri, lin in enumerate(linhas):
        tr = add(t, 'w:tr')
        trpr = add(tr, 'w:trPr')
        add(trpr, 'w:cantSplit')
        if ri == 0:
            add(trpr, 'w:tblHeader')
        for ci, txt in enumerate(lin):
            tc = add(tr, 'w:tc')
            tcpr = add(tc, 'w:tcPr')
            add(tcpr, 'w:tcW', {'w:w': ws[ci], 'w:type': 'dxa'})
            if ri == 0:
                add(tcpr, 'w:shd', {'w:val': 'clear', 'w:color': 'auto', 'w:fill': 'EEEEEE'})
            add(tcpr, 'w:vAlign', {'w:val': 'center'})
            pa = para(txt, 'tablecopy', align='start' if ci == 0 else 'center', size=7.5, first=0,
                      keep=ri < len(linhas) - 1, after=0, before=0, linha=9.5)
            tc.append(pa)
    return t


def tem_sec(p):
    pr = p.find('w:pPr', NS)
    return pr is not None and pr.find('w:sectPr', NS) is not None


def secao(p, num_colunas):
    """Faz a secao terminar neste paragrafo, com o numero de colunas pedido.

    E assim que o Word muda de uma para duas colunas no meio da pagina: o sectPr guardado
    no pPr de um paragrafo descreve a secao que acaba nele. Uma figura larga fica, portanto,
    entre um paragrafo que fecha a secao de duas colunas e a sua legenda, que fecha a secao
    de uma coluna."""
    sec = deepcopy(sec_corpo)
    cols = sec.find('w:cols', NS)
    cols.set('{' + NS['w'] + '}num', str(num_colunas))
    sec.insert(0, no('w:type', {'w:val': 'continuous'}))
    pr = p.find('w:pPr', NS)
    if pr is None:
        pr = E.Element('{' + NS['w'] + '}pPr')
        p.insert(0, pr)
    pr.append(sec)


nfig = neq = ntab = 0
ROMANOS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
for bloco in C.blocos():
    tipo = bloco[0]
    if tipo == 'h':
        body.append(para(bloco[1], 'Heading1', keep=True, first=0))
    elif tipo == 'sub':
        body.append(para(bloco[1], 'Heading2', keep=True, first=0))
    elif tipo == 'p':
        body.append(para(bloco[1]))
    elif tipo == 'eq':
        neq += 1
        body.append(equacao(bloco[1], neq))
    elif tipo == 'fig':
        nfig += 1
        body.append(figura(bloco[1], nfig))
        body.append(para(f'Fig. {nfig}. ' + bloco[2], 'figurecaption', first=0, after=6))
    elif tipo == 'figw':
        nfig += 1
        if len(body) and E.QName(body[-1]).localname == 'p' and not tem_sec(body[-1]):
            secao(body[-1], 2)
        body.append(figura(bloco[1], nfig, largura=LARGURA_TOTAL))
        legenda = para(f'Fig. {nfig}. ' + bloco[2], 'figurecaption', first=0, after=6)
        secao(legenda, 1)
        body.append(legenda)
    elif tipo == 'tab':
        ntab += 1
        body.append(para(f'TABELA {ROMANOS[ntab - 1]}', 'tablehead', align='center', keep=True, first=0, after=0))
        body.append(para(bloco[1], 'tablehead', align='center', keep=True, first=0, after=2))
        body.append(tabela(bloco[2], bloco[3]))
        body.append(para('', after=2))
body.append(para('Referências', 'Heading1', keep=True, first=0))
for i, ref in enumerate(C.REFERENCIAS, 1):
    ref = re.sub(r'https?://\S+', lambda m: m[0].replace('/', '/​').replace('_', '_​').replace('-', '-​'), ref)
    body.append(para(f'[{i}] ' + ref, 'references', first=0, size=8, after=3))
body[-1][0].append(sec_corpo)
sec_final = deepcopy(sec_corpo)
sec_final.find('w:cols', NS).set('{' + NS['w'] + '}num', '1')
body.append(sec_final)

pkg['word/document.xml'] = serial(doc)
pkg['word/_rels/document.xml.rels'] = serial(rels)
pkg['[Content_Types].xml'] = serial(ct)
core = E.fromstring(pkg['docProps/core.xml'])
for tag, txt in (('title', C.TITULO), ('creator', '; '.join(a.split(' (')[0] for a in C.AUTORES))):
    el = core.find('{http://purl.org/dc/elements/1.1/}' + tag)
    if el is None:
        el = E.SubElement(core, '{http://purl.org/dc/elements/1.1/}' + tag)
    el.text = txt
pkg['docProps/core.xml'] = serial(core)
destino = OUT / (C.ARQUIVO + '.docx')
with ZipFile(destino, 'w', ZIP_DEFLATED) as z:
    for n, dados in pkg.items():
        z.writestr(n, dados)
with ZipFile(TPL) as orig:
    alteradas = [n for n in orig.namelist() if orig.read(n) != pkg[n]]
assert set(alteradas) <= {'word/document.xml', 'word/_rels/document.xml.rels', '[Content_Types].xml', 'docProps/core.xml'}, alteradas
assert hashlib.sha256(TPL.read_bytes()).hexdigest() == SHA_TPL, 'template alterado'
(QA / 'pacote_validacao.json').write_text(json.dumps(dict(partes_alteradas=alteradas, figuras=nfig, equacoes_editaveis=neq, tabelas=ntab,
                                                         template_sha256=SHA_TPL, docx_sha256=hashlib.sha256(destino.read_bytes()).hexdigest()),
                                                    indent=1), encoding='utf-8')
print(destino, f'{nfig} figuras, {neq} equacoes, {ntab} tabelas')
