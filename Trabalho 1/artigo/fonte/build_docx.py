# -*- coding: utf-8 -*-
"""Monta o artigo IEEE em .docx a partir do template strict OOXML."""
import importlib.util, json, os, re, shutil, struct, subprocess, sys, zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLD  = os.path.join(BASE, "build")
PKG  = os.path.join(BLD, "pkg")
FIGS = os.path.join(BASE, "figuras")
OUTN = "artigo-perdas-semicondutores-trafo-af"

spec = importlib.util.spec_from_file_location("conteudo", os.path.join(BASE, "conteudo.py"))
K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)
OMML = json.load(open(os.path.join(BLD, "omml.json"), encoding="utf-8"))

# ---------------------------------------------------------------- pacote
if os.path.isdir(PKG): shutil.rmtree(PKG)
shutil.copytree(os.path.join(BASE, "tpl"), PKG)
os.makedirs(os.path.join(PKG, "word", "media"), exist_ok=True)

def rd(p): return open(os.path.join(PKG, p), encoding="utf-8").read()
def wr(p, s): open(os.path.join(PKG, p), "w", encoding="utf-8").write(s)

# numeracao das tabelas em portugues
n = rd("word/numbering.xml").replace('w:val="TABLE %1. "', 'w:val="Tabela %1. "')
wr("word/numbering.xml", n)

# idioma padrao pt-BR
s = rd("word/styles.xml").replace('<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>',
                                  '<w:lang w:val="pt-BR" w:eastAsia="en-US" w:bidi="ar-SA"/>')
wr("word/styles.xml", s)

# ---------------------------------------------------------------- figuras
def png_size(path):
    with open(path, "rb") as f:
        d = f.read(33)
    w, h = struct.unpack(">II", d[16:24])
    return w, h

FIGORDER = [b[1] for b in K.C if b[0] == "fig"]
RID = {}
rels = rd("word/_rels/document.xml.rels")
add = []
for i, name in enumerate(FIGORDER, start=1):
    src = os.path.join(FIGS, name + ".png")
    dst = "image%d.png" % i
    shutil.copy(src, os.path.join(PKG, "word", "media", dst))
    rid = "rIdImg%d" % i
    RID[name] = (rid, png_size(src))
    add.append('<Relationship Id="%s" Type="http://purl.oclc.org/ooxml/officeDocument/'
               'relationships/image" Target="media/%s"/>' % (rid, dst))
rels = rels.replace("</Relationships>", "".join(add) + "</Relationships>")
wr("word/_rels/document.xml.rels", rels)

ct = rd("[Content_Types].xml")
if 'Extension="png"' not in ct:
    ct = ct.replace('<Default Extension="rels"',
                    '<Default Extension="png" ContentType="image/png"/><Default Extension="rels"')
wr("[Content_Types].xml", ct)

# ---------------------------------------------------------------- runs
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _run(txt, rpr=""):
    if not txt: return ""
    sp = ' xml:space="preserve"' if txt != txt.strip() else ""
    return "<w:r>%s<w:t%s>%s</w:t></w:r>" % (rpr, sp, esc(txt))

BASECH = "A-Za-zΔΦΨΩαβγδεηθλμνρστφχψω"
SUPS   = "²³⁴⁻¹"
TOK = re.compile(r"([%s])([%s]*)_((?:[A-Za-z0-9]+|\([A-Za-z0-9,]+\))+)" % (BASECH, SUPS))
IT  = "<w:rPr><w:i/></w:rPr>"
SUB = '<w:rPr><w:vertAlign w:val="subscript"/></w:rPr>'

def runs(text, rpr=""):
    """Converte X_y em base italica com subscrito; o resto vira texto normal."""
    it_rpr  = rpr.replace("<w:rPr>", "<w:rPr><w:i/>") if rpr else IT
    sub_rpr = (rpr.replace("<w:rPr>", '<w:rPr><w:vertAlign w:val="subscript"/>')
               if rpr else SUB)
    out, pos, fim = [], 0, -1
    while True:
        m = TOK.search(text, pos)
        if not m: break
        i = m.start()
        if i > 0 and i != fim and (text[i - 1].isalnum() or text[i - 1] in "_/."):
            pos = m.end(); continue          # dentro de palavra ou de URL
        base, sup, sub = m.group(1), m.group(2), m.group(3)
        end = m.end()
        # nao engolir a letra que inicia outro simbolo (ex.: A_eA_w)
        while end < len(text) and text[end] == "_" and len(sub) > 1 and sub[-1].isalpha():
            sub = sub[:-1]; end -= 1
        out.append(_run(text[pos:m.start()], rpr))
        out.append(_run(base + sup, it_rpr))
        out.append(_run(sub, sub_rpr))
        pos = fim = end
    out.append(_run(text[pos:], rpr))
    return "".join(out)

# ---------------------------------------------------------------- blocos
ITEMS = []          # {'xml':..., 'sect':None|'2col'|'1col', 'p':bool}
def emit(xml, isp=True, sect=None):
    ITEMS.append({"xml": xml, "sect": sect, "p": isp})

def P(style, inner, extra="", rpr=""):
    ppr = "<w:pPr>"
    if style: ppr += '<w:pStyle w:val="%s"/>' % style
    ppr += extra
    if rpr: ppr += rpr
    ppr += "</w:pPr>"
    return "<w:p>%s%s</w:p>" % (ppr, inner)

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'

def eq_para(om, num):
    extra = ('<w:tabs><w:tab w:val="center" w:pos="115pt"/>'
             '<w:tab w:val="end" w:pos="243pt"/></w:tabs>'
             '<w:spacing w:line="11pt" w:lineRule="atLeast"/>')
    rpr = "<w:rPr>%s</w:rPr>" % TNR
    a = "<w:r><w:rPr>%s</w:rPr><w:tab/></w:r>" % TNR
    b = "<w:r><w:rPr>%s</w:rPr><w:tab/><w:t>(%s)</w:t></w:r>" % (TNR, num)
    return P("equation", a + om + b, extra, rpr)

def eq_para_wide(om, num):
    extra = ('<w:tabs><w:tab w:val="center" w:pos="245pt"/>'
             '<w:tab w:val="end" w:pos="500pt"/></w:tabs>')
    rpr = "<w:rPr>%s</w:rPr>" % TNR
    a = "<w:r><w:rPr>%s</w:rPr><w:tab/></w:r>" % TNR
    b = "<w:r><w:rPr>%s</w:rPr><w:tab/><w:t>(%s)</w:t></w:r>" % (TNR, num)
    return P("equation", a + om + b, extra, rpr)

W1, W2 = 237.0, 500.0     # larguras uteis em pt (1 coluna e 2 colunas)

def img_para(name, span):
    rid, (pw, ph) = RID[name]
    wpt = W1 if span == 1 else W2
    hpt = wpt * ph / pw
    cx, cy = int(round(wpt * 12700)), int(round(hpt * 12700))
    d = ('<w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
         '<wp:inline distT="0" distB="0" distL="0" distR="0">'
         '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
         '<wp:docPr id="%d" name="%s.png"/>'
         '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
         'xmlns:a="http://purl.oclc.org/ooxml/drawingml/main" noChangeAspect="1"/>'
         '</wp:cNvGraphicFramePr>'
         '<a:graphic xmlns:a="http://purl.oclc.org/ooxml/drawingml/main">'
         '<a:graphicData uri="http://purl.oclc.org/ooxml/drawingml/picture">'
         '<pic:pic xmlns:pic="http://purl.oclc.org/ooxml/drawingml/picture">'
         '<pic:nvPicPr><pic:cNvPr id="%d" name="%s.png"/><pic:cNvPicPr/></pic:nvPicPr>'
         '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch>'
         '</pic:blipFill>'
         '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
         '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
         '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
         % (cx, cy, 100 + len(RID), name, 100 + len(RID), name, rid, cx, cy))
    return P(None, d, '<w:keepNext/><w:spacing w:before="6pt" w:after="0pt"/>')

def cell(txt, style, jc=None, wpt=0.0):
    extra = '<w:jc w:val="%s"/>' % jc if jc else ""
    p = P(style, runs(txt), '<w:keepNext/>' + extra)
    return ('<w:tc><w:tcPr><w:tcW w:w="%.2fpt" w:type="dxa"/><w:vAlign w:val="center"/>'
            '</w:tcPr>%s</w:tc>' % (wpt, p))

def table_xml(rows, widths, span):
    tot = W1 if span == 1 else W2
    wpts = [tot * f for f in widths]
    grid = "".join('<w:gridCol w:w="%d"/>' % int(round(w * 20)) for w in wpts)
    tr = []
    for ri, row in enumerate(rows):
        head = (ri == 0)
        cells = []
        for ci, c in enumerate(row):
            st = "tablecolhead" if head else "tablecopy"
            jc = None if head else ("start" if ci == 0 else "center")
            cells.append(cell(c, st, jc, wpts[ci]))
        trpr = ('<w:trPr><w:cantSplit/>' + ("<w:tblHeader/>" if head else "") +
                '<w:jc w:val="center"/></w:trPr>')
        tr.append("<w:tr>%s%s</w:tr>" % (trpr, "".join(cells)))
    pr = ('<w:tblPr><w:tblW w:w="0pt" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>'
          '<w:top w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
          '<w:start w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
          '<w:bottom w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
          '<w:end w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
          '<w:insideH w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
          '<w:insideV w:val="single" w:sz="2" w:space="0" w:color="auto"/></w:tblBorders>'
          '<w:tblLayout w:type="fixed"/><w:tblCellMar>'
          '<w:top w:w="1pt" w:type="dxa"/><w:start w:w="2.50pt" w:type="dxa"/>'
          '<w:bottom w:w="1pt" w:type="dxa"/><w:end w:w="2.50pt" w:type="dxa"/>'
          '</w:tblCellMar><w:tblLook w:firstRow="0" w:lastRow="0" w:firstColumn="0" '
          'w:lastColumn="0" w:noHBand="0" w:noVBand="0"/></w:tblPr>')
    return "<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>" % (pr, grid, "".join(tr))

TITULO_STYLES = ('<w:pStyle w:val="Heading1"/>', '<w:pStyle w:val="Heading2"/>')

def abrir_ilha():
    """Encerra a secao de duas colunas antes de um elemento de largura plena.

    Titulos imediatamente anteriores acompanham o elemento para dentro da ilha,
    porque uma secao de duas colunas terminada em titulo seria equilibrada pelo
    editor e os titulos apareceriam lado a lado."""
    k = len(ITEMS) - 1
    while k >= 0 and ITEMS[k]["p"] and any(t in ITEMS[k]["xml"] for t in TITULO_STYLES):
        k -= 1
    if k < 0:
        emit(P(None, "", '<w:spacing w:after="0pt" w:line="1pt" w:lineRule="exact"/>'),
             sect="2col")
        return
    if ITEMS[k]["sect"] == "1col":
        ITEMS[k]["sect"] = None            # funde com a ilha anterior
    elif ITEMS[k]["p"]:
        ITEMS[k]["sect"] = "2col"
    else:                                   # tabela: precisa de paragrafo portador
        ITEMS.insert(k + 1, {"xml": P(None, "",
                     '<w:spacing w:after="0pt" w:line="1pt" w:lineRule="exact"/>'),
                     "sect": "2col", "p": True})

def fechar_ilha():
    ITEMS[-1]["sect"] = "1col"

# ---------------------------------------------------------------- corpo
emit(P("Abstract", '<w:r><w:rPr><w:i/></w:rPr><w:t>Resumo</w:t></w:r>'
                   '<w:r><w:t>—</w:t></w:r>' + runs(K.RESUMO)))
emit(P("Keywords", '<w:r><w:t>Palavras-chave—</w:t></w:r>' + runs(K.PALAVRAS)))

for b in K.C:
    k = b[0]
    if k == "h1":
        emit(P("Heading1", runs(b[1])))
    elif k == "h2":
        emit(P("Heading2", runs(b[1])))
    elif k == "p":
        emit(P("BodyText", runs(b[1])))
    elif k == "eq":
        om = OMML[b[2]][0]
        emit(eq_para(om, b[2]))
    elif k == "fig":
        name, cap, span = b[1], b[2], b[3]
        if span == 2: abrir_ilha()
        emit(img_para(name, span))
        emit(P("figurecaption", runs(cap)))
        if span == 2: fechar_ilha()
    elif k == "tab":
        cap, rows, widths, span, note = b[1], b[2], b[3], b[4], b[5]
        if span == 2: abrir_ilha()
        emit(P("tablehead", runs(cap), '<w:keepNext/>'))
        emit(table_xml(rows, widths, span), isp=False)
        if note:
            emit(P("tablefootnote", runs(note),
                   '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
                   '<w:ind w:start="0pt" w:firstLine="0pt"/><w:jc w:val="both"/>'))
        elif span == 2:
            emit(P(None, "", '<w:spacing w:after="0pt" w:line="1pt" w:lineRule="exact"/>'))
        if span == 2: fechar_ilha()
    elif k == "bul":
        for it in b[1]:
            emit(P("bulletlist", runs(it)))

emit(P("Heading5", '<w:r><w:t>Referências</w:t></w:r>'))
for r in K.REFS:
    emit(P("references", runs(r)))
# quebra continua no fim: faz o Word equilibrar as duas colunas da ultima pagina
emit(P(None, "", '<w:spacing w:after="0pt" w:line="1pt" w:lineRule="exact"/>'), sect="2col")

# ---------------------------------------------------------------- secoes
PG = '<w:pgSz w:w="595.30pt" w:h="841.90pt" w:code="9"/>'
def sect(cols, top, lr, space, extra=""):
    c = ('<w:cols w:space="%s"/>' % space if cols == 1 else
         '<w:cols w:num="%d" w:space="%s"/>' % (cols, space))
    return ('<w:sectPr><w:type w:val="continuous"/>%s%s'
            '<w:pgMar w:top="%s" w:right="%s" w:bottom="72pt" w:left="%s" '
            'w:header="36pt" w:footer="36pt" w:gutter="0pt"/>%s'
            '<w:docGrid w:linePitch="360"/></w:sectPr>'
            % (extra, PG, top, lr, lr, c))

S_TITULO = ('<w:sectPr><w:footerReference w:type="first" r:id="rId8"/>'
            '<w:type w:val="continuous"/>' + PG +
            '<w:pgMar w:top="27pt" w:right="44.65pt" w:bottom="72pt" w:left="44.65pt" '
            'w:header="36pt" w:footer="36pt" w:gutter="0pt"/><w:cols w:space="36pt"/>'
            '<w:titlePg/><w:docGrid w:linePitch="360"/></w:sectPr>')
S_AUTOR  = sect(2, "22.50pt", "44.65pt", "36pt")
S_2COL   = sect(2, "54pt", "45.35pt", "18pt")
S_1COL   = sect(1, "54pt", "45.35pt", "36pt")

def inject(xml, sectpr):
    i = xml.find("</w:pPr>")
    assert i > 0, xml[:200]
    return xml[:i] + sectpr + xml[i:]

# ---------------------------------------------------------------- frente
front = []
front.append(P("papertitle",
               '<w:r><w:t>%s</w:t></w:r>' % esc(K.TITULO.replace("\n", " ")),
               "", "") .replace("</w:pPr>", S_TITULO + "</w:pPr>"))

BR = '<w:r><w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr><w:br/></w:r>'
def linha(t, it=False, sz="18"):
    rpr = "<w:rPr>%s<w:sz w:val=\"%s\"/><w:szCs w:val=\"%s\"/></w:rPr>" % (
        "<w:i/>" if it else "", sz, sz)
    return "<w:r>%s<w:t>%s</w:t></w:r>" % (rpr, esc(t))

for idx, a in enumerate(K.AUTORES):
    inner = (linha(a["nome"], sz="20") + BR + linha(a["dep"], True) + BR +
             linha(a["org"], True) + BR + linha(a["cid"]) + BR + linha(a["mail"]))
    extra = '<w:spacing w:before="8pt" w:after="0pt"/>'
    x = P("Author", inner, extra)
    if idx == len(K.AUTORES) - 1:
        x = inject(x, S_AUTOR)
    front.append(x)

# ---------------------------------------------------------------- montagem
body = []
for it in ITEMS:
    x = it["xml"]
    if it["sect"]:
        x = inject(x, S_2COL if it["sect"] == "2col" else S_1COL)
    body.append(x)

HEAD = open(os.path.join(BASE, "tpl", "word", "document.xml"), encoding="utf-8").read()
HEAD = HEAD[:HEAD.find("<w:body>") + len("<w:body>")]
doc = HEAD + "".join(front) + "".join(body) + S_2COL + "</w:body></w:document>"
wr("word/document.xml", doc)

# ---------------------------------------------------------------- metadados
core = rd("docProps/core.xml")
core = re.sub(r"<dc:title>.*?</dc:title>",
              "<dc:title>%s</dc:title>" % esc(K.TITULO.replace("\n", " ")), core, flags=re.S)
core = re.sub(r"<dc:creator>.*?</dc:creator>",
              "<dc:creator>%s</dc:creator>" % esc("; ".join(a["nome"] for a in K.AUTORES)),
              core, flags=re.S)
core = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>",
              "<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % esc(K.AUTORES[0]["nome"]),
              core, flags=re.S)
core = re.sub(r"<cp:keywords>.*?</cp:keywords>",
              "<cp:keywords>%s</cp:keywords>" % esc(K.PALAVRAS), core, flags=re.S)
core = re.sub(r"<dc:subject>.*?</dc:subject>",
              "<dc:subject>%s</dc:subject>" % esc("Eletrônica Industrial"), core, flags=re.S)
wr("docProps/core.xml", core)

# ---------------------------------------------------------------- zip
out = os.path.join(BLD, OUTN + ".docx")
if os.path.exists(out): os.remove(out)
names = []
for root, _, fs in os.walk(PKG):
    for f in fs:
        p = os.path.join(root, f)
        names.append((p, os.path.relpath(p, PKG).replace(os.sep, "/")))
names.sort(key=lambda t: (t[1] != "[Content_Types].xml", t[1]))
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p, arc in names:
        z.write(p, arc)
print("gerado:", out, os.path.getsize(out), "bytes")
print("itens:", len(ITEMS), "| ilhas 1col:", sum(1 for i in ITEMS if i["sect"] == "1col"))
