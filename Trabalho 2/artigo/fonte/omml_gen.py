# -*- coding: utf-8 -*-
"""Converte as equações LaTeX de conteudo.py em OMML (equação nativa do Word).

Diferente do Trabalho 1, não usa o pandoc: LaTeX -> MathML pela biblioteca
latex2mathml e MathML -> OMML pela folha de estilo MML2OMML.XSL que acompanha
o Microsoft Office. As declarações de namespace são removidas porque o
documento final (template OOXML strict) já declara o prefixo m: na raiz.

Dependências: pip install latex2mathml lxml ; Microsoft Office instalado.
"""
import importlib.util, json, os, re, sys, glob
from latex2mathml.converter import convert
from lxml import etree

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
BLD = os.path.join(BASE, "build")
os.makedirs(BLD, exist_ok=True)

XSL = None
for c in glob.glob(r"C:\Program Files*\Microsoft Office\root\Office*\MML2OMML.XSL"):
    XSL = c
    break
if XSL is None:
    sys.exit("MML2OMML.XSL não encontrado: é preciso ter o Microsoft Office instalado.")
TRANSF = etree.XSLT(etree.parse(XSL))

spec = importlib.util.spec_from_file_location("conteudo", os.path.join(AQUI, "conteudo.py"))
K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)
EQS = [(b[2], b[1]) for b in K.C if b[0] == "eq"]

CAM = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'


def para_omml(tex):
    mml = convert(tex)
    om = TRANSF(etree.fromstring(mml.encode("utf-8")))
    x = etree.tostring(om.getroot(), encoding="unicode")
    x = re.sub(r'\sxmlns:\w+="[^"]*"', "", x)
    # fonte matemática em cada trecho de texto, como no template
    x = re.sub(r"<m:r>(<m:rPr>.*?</m:rPr>)?<m:t", lambda m: "<m:r>%s%s<m:t" % (m.group(1) or "", CAM), x)
    return x


res = {}
for n, t in EQS:
    try:
        res[n] = [para_omml(t)]
    except Exception as e:
        sys.exit("Equação (%s) falhou: %s\n  %s" % (n, e, t))
json.dump(res, open(os.path.join(BLD, "omml.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("OK: %d equações convertidas" % len(res))
