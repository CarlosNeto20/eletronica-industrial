"""Compõe o artigo usando o pacote IEEE original OOXML Strict sem alterar estilos."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from copy import deepcopy
import re,struct,json,hashlib
from lxml import etree as E
import conteudo as C
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artigo';QA=OUT/'qa';QA.mkdir(exist_ok=True)
TPL=ROOT/'documentos de referência/template-a4.docx'
NS={'w':'http://purl.oclc.org/ooxml/wordprocessingml/main',
    'm':'http://purl.oclc.org/ooxml/officeDocument/math',
    'r':'http://purl.oclc.org/ooxml/officeDocument/relationships',
    'wp':'http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing',
    'a':'http://purl.oclc.org/ooxml/drawingml/main',
    'pic':'http://purl.oclc.org/ooxml/drawingml/picture'}
def node(tag,attrs=None,text=None):
    pre,key=tag.split(':');o=E.Element('{'+NS[pre]+'}'+key)
    for k,v in (attrs or {}).items():
        if ':' in k:a,b=k.split(':');k='{'+NS[a]+'}'+b
        o.set(k,str(v))
    if text is not None:o.text=text
    return o
def add(parent,tag,attrs=None,text=None):o=node(tag,attrs,text);parent.append(o);return o
def serial(x):return E.tostring(x,encoding='UTF-8',xml_declaration=True,standalone=True)
def run(txt,size=None,bold=False):
    r=node('w:r');pr=add(r,'w:rPr');add(pr,'w:color',{'w:val':'000000'});add(pr,'w:lang',{'w:val':'pt-BR'})
    if size:add(pr,'w:sz',{'w:val':round(2*size)})
    if bold:add(pr,'w:b')
    t=add(r,'w:t',text=txt);t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');return r
def para(text='',style='BodyText',align=None,keep=False,size=None,after=None,first=None):
    p=node('w:p');pr=add(p,'w:pPr');add(pr,'w:pStyle',{'w:val':style})
    num=add(pr,'w:numPr');add(num,'w:numId',{'w:val':0})
    if keep:add(pr,'w:keepNext')
    add(pr,'w:widowControl')
    if align:add(pr,'w:jc',{'w:val':align})
    if after is not None:add(pr,'w:spacing',{'w:after':f'{after}pt'})
    if style=='Author':
        spacing=pr.find('w:spacing',NS)
        if spacing is None:spacing=add(pr,'w:spacing')
        spacing.set('{'+NS['w']+'}before','0pt')
    if first is not None:add(pr,'w:ind',{'w:firstLine':f'{first}pt','w:start':'0pt','w:end':'0pt'})
    if text:p.append(run(text,size))
    return p

# Small, deterministic native OMML parser: fractions, groups, sub/superscripts.
def mathparse(s):
    i=0
    def group():
        nonlocal i
        if i<len(s) and s[i]=='{':i+=1;v=seq('}');i+=1;return v
        if i<len(s):c=s[i];i+=1;return [mr(c)]
        return []
    def mr(t):
        r=node('m:r');pr=add(r,'w:rPr');add(pr,'w:rFonts',{'w:ascii':'Cambria Math','w:hAnsi':'Cambria Math'});add(pr,'w:sz',{'w:val':19});add(r,'m:t',text=t);return r
    def seq(end=None):
        nonlocal i
        out=[]
        while i<len(s) and s[i]!=end:
            if s.startswith('\\frac',i):
                i+=5;nu=group();de=group();f=node('m:f');n=add(f,'m:num');n.extend(nu);d=add(f,'m:den');d.extend(de);out.append(f)
            elif s[i] in '_^':
                op=s[i];i+=1;g=group();base=out.pop();t=node('m:sSub' if op=='_' else 'm:sSup');e=add(t,'m:e');e.append(base);q=add(t,'m:sub' if op=='_' else 'm:sup');q.extend(g);out.append(t)
            elif s[i]=='{':out.extend(group())
            else:out.append(mr(s[i]));i+=1
        return out
    return seq()
def equation(text,n):
    p=para('',style='equation',align='center',first=0,after=6)
    pr=p[0];add(pr,'w:keepLines');add(pr,'w:spacing',{'w:before':'4pt','w:after':'6pt','w:line':'12pt','w:lineRule':'atLeast'})
    mp=add(p,'m:oMathPara');mpp=add(mp,'m:oMathParaPr');add(mpp,'m:jc',{'m:val':'center'})
    om=add(mp,'m:oMath');om.extend(mathparse(text));rr=add(om,'m:r');add(rr,'m:t',text=f'   ({n})');return p

with ZipFile(TPL) as z:pkg={n:z.read(n) for n in z.namelist()}
doc=E.fromstring(pkg['word/document.xml']);body=doc.find('w:body',NS)
sects=body.findall('.//w:sectPr',NS);title_sec=deepcopy(sects[0]);body_sec=deepcopy(next(s for s in sects if s.find('w:cols',NS).get('{'+NS['w']+'}num')=='2'))
for sec in [title_sec,body_sec]:
    for el in list(sec):
        if E.QName(el).localname in ['headerReference','footerReference','titlePg']:sec.remove(el)
    for k in list(sec.attrib):del sec.attrib[k]
for el in list(body):body.remove(el)
body.append(para(C.TITLE,'papertitle',align='center',keep=True,first=0))
for a in C.AUTHORS:body.append(para(a,'Author',align='center',keep=True,first=0,after=1))
body.append(para('Universidade Federal do Ceará — Eletrônica Industrial','Author',align='center',keep=True,first=0,size=10,after=1))
last=para('Prof. Dr. René Pastor Torrico-Bascopé • Outubro de 2026','Author',align='center',first=0,size=9,after=12)
last[0].append(title_sec);body.append(last)
body.append(para('Resumo—'+C.ABSTRACT,'Abstract',first=0,after=6))
body.append(para('Palavras-chave—'+C.KEYWORDS,'Keywords',first=0,after=6))
rels=E.fromstring(pkg['word/_rels/document.xml.rels']);rns=E.QName(rels).namespace
ct=E.fromstring(pkg['[Content_Types].xml']);ctns=E.QName(ct).namespace
if not any(e.get('Extension')=='png' for e in ct):E.SubElement(ct,'{'+ctns+'}Default',Extension='png',ContentType='image/png')
LARGURA={1:234,2:504}  # pt: uma coluna e largura útil da página (A4 menos margens de 45,35 pt)
def figure(name,no,span=1):
    blob=(OUT/'figuras'/(name+'.png')).read_bytes();pw,ph=struct.unpack('>II',blob[16:24]);cx=round(LARGURA[span]*12700);cy=round(cx*ph/pw)
    rid='rIdArtigo'+str(no);target=f'media/artigo_fig_{no}.png';pkg['word/'+target]=blob
    E.SubElement(rels,'{'+rns+'}Relationship',Id=rid,Type=NS['r']+'/image',Target=target)
    p=para('',align='center',keep=True,first=0,after=0);r=add(p,'w:r');draw=add(r,'w:drawing');inline=add(draw,'wp:inline',{'distT':0,'distB':0,'distL':0,'distR':0})
    add(inline,'wp:extent',{'cx':cx,'cy':cy});add(inline,'wp:docPr',{'id':1000+no,'name':name,'descr':name.replace('_',' ')})
    g=add(inline,'a:graphic');d=add(g,'a:graphicData',{'uri':NS['pic']});pic=add(d,'pic:pic')
    nv=add(pic,'pic:nvPicPr');add(nv,'pic:cNvPr',{'id':1000+no,'name':name});add(nv,'pic:cNvPicPr')
    bf=add(pic,'pic:blipFill');add(bf,'a:blip',{'r:embed':rid});st=add(bf,'a:stretch');add(st,'a:fillRect')
    sp=add(pic,'pic:spPr');xf=add(sp,'a:xfrm');add(xf,'a:off',{'x':0,'y':0});add(xf,'a:ext',{'cx':cx,'cy':cy});pr=add(sp,'a:prstGeom',{'prst':'rect'});add(pr,'a:avLst');return p
def table(rows,widths):
    widths=widths or [1/len(rows[0])]*len(rows[0]);ws=[round(w*234*20) for w in widths]
    t=node('w:tbl');pr=add(t,'w:tblPr');add(pr,'w:tblW',{'w:w':4680,'w:type':'dxa'});add(pr,'w:tblLayout',{'w:type':'fixed'})
    borders=add(pr,'w:tblBorders')
    for edge in ['top','bottom','insideH']:add(borders,'w:'+edge,{'w:val':'single','w:sz':4,'w:color':'888888'})
    mar=add(pr,'w:tblCellMar')
    for edge,val in [('top',35),('bottom',35),('start',50),('end',50)]:add(mar,'w:'+edge,{'w:w':val,'w:type':'dxa'})
    grid=add(t,'w:tblGrid')
    for w in ws:add(grid,'w:gridCol',{'w:w':w})
    for ri,row in enumerate(rows):
        tr=add(t,'w:tr');trpr=add(tr,'w:trPr');add(trpr,'w:cantSplit')
        if ri==0:add(trpr,'w:tblHeader')
        for ci,txt in enumerate(row):
            tc=add(tr,'w:tc');tcpr=add(tc,'w:tcPr');add(tcpr,'w:tcW',{'w:w':ws[ci],'w:type':'dxa'});add(tcpr,'w:vAlign',{'w:val':'center'})
            if ri==0:add(tcpr,'w:shd',{'w:fill':'EEEEEE'})
            pa=para(txt,'tablecopy',align='start' if ci==0 else 'center',size=8,first=0,after=0)
            if ri<len(rows)-1:add(pa[0],'w:keepNext')
            add(pa[0],'w:spacing',{'w:line':'10pt','w:lineRule':'atLeast','w:after':'0pt'})
            tc.append(pa)
    return t
W_='{'+NS['w']+'}'
def encerrar_secao(sec):
    """Encerra a seção atual no último parágrafo, que precisa ser de texto corrido.
    Uma figura de largura total fica numa "ilha" de uma coluna entre duas seções de duas colunas; o Word
    equilibra as colunas antes da ilha, como nos artigos dos trabalhos anteriores."""
    ult=body[-1];estilo=ult.find('w:pPr/w:pStyle',NS) if ult.tag==W_+'p' else None
    assert estilo is not None and estilo.get(W_+'val')=='BodyText' and ult.find('w:pPr/w:sectPr',NS) is None,'figura de largura total deve seguir um parágrafo de texto'
    ult.find('w:pPr',NS).append(deepcopy(sec))
secao_1col=deepcopy(body_sec);secao_1col.find('w:cols',NS).set(W_+'num','1')
fn=en=0
for b in C.B:
    k=b[0]
    if k=='h':body.append(para(b[1],'Heading1',keep=True,first=0))
    elif k=='sub':body.append(para(b[1],'Heading2',keep=True,first=0))
    elif k=='p':body.append(para(b[1]))
    elif k=='eq':en+=1;body.append(equation(b[1],en))
    elif k=='fig':
        fn+=1;span=b[3];pf=figure(b[1],fn,span);pc=para(f'Fig. {fn}. '+b[2],'figurecaption',first=0,after=7)
        if span==2:encerrar_secao(body_sec)
        body.append(pf);body.append(pc)
        if span==2:
            pc.find('w:pPr',NS).append(deepcopy(secao_1col))
    elif k=='table':body.append(para(b[1],'tablehead',align='center',keep=True,first=0));body.append(table(b[2],b[3]));body.append(para('',after=2))
body.append(para('Referências','Heading1',keep=True,first=0))
for ref in C.REFS:
    # Zero-width break opportunities keep long URLs within one column.
    ref=re.sub(r'https://\S+',lambda m:m[0].replace('/','/\u200b').replace('_','_\u200b').replace('-','-\u200b'),ref)
    body.append(para(ref,'references',first=0,size=8,after=4))
body.append(para('Fontes on-line consultadas em 19 de outubro de 2026.','references',first=0,size=8,after=0))
body[-1][0].append(body_sec)
final_sec=deepcopy(body_sec);final_sec.find('w:cols',NS).set('{'+NS['w']+'}num','1')
body.append(final_sec)
pkg['word/document.xml']=serial(doc);pkg['word/_rels/document.xml.rels']=serial(rels);pkg['[Content_Types].xml']=serial(ct)
core=E.fromstring(pkg['docProps/core.xml'])
for tag,txt in [('title',C.TITLE),('creator','; '.join(C.AUTHORS))]:
    el=core.find('{http://purl.org/dc/elements/1.1/}'+tag)
    if el is None:el=E.SubElement(core,'{http://purl.org/dc/elements/1.1/}'+tag)
    el.text=txt
pkg['docProps/core.xml']=serial(core)
dest=OUT/'Trabalho4_Forward_15A.docx'
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
    for n,data in pkg.items():z.writestr(n,data)
with ZipFile(TPL) as original:
    changed=[n for n in original.namelist() if original.read(n)!=pkg[n]]
assert set(changed)<=set(['word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','docProps/core.xml']),changed
assert hashlib.sha256(TPL.read_bytes()).hexdigest()=='9d0153f7121508f585eff77c6fc112234a9d289c0390bf54a5296d15d01b04d3'
(QA/'pacote_validacao.json').write_text(json.dumps(dict(partes_alteradas=changed,figuras=fn,equacoes_editaveis=en,template_sha256=hashlib.sha256(TPL.read_bytes()).hexdigest(),docx_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()),indent=2),encoding='utf8')
print(dest)
