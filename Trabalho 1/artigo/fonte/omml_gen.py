# -*- coding: utf-8 -*-
"""Converte as equacoes LaTeX de conteudo.py em OMML (strict OOXML) via pandoc."""
import importlib.util, os, re, subprocess, zipfile, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(BASE, "build", "omml_work")
os.makedirs(WORK, exist_ok=True)

spec = importlib.util.spec_from_file_location("conteudo", os.path.join(BASE, "conteudo.py"))
cont = importlib.util.module_from_spec(spec); spec.loader.exec_module(cont)
EQS = [(b[2], b[1]) for b in cont.C if b[0] == "eq"]

# markdown com uma equacao display por bloco, separada por paragrafo marcador
md = []
for n, t in EQS:
    md.append("MARCA%sMARCA\n\n$$%s$$\n" % (n, t))
src = os.path.join(WORK, "eqs.md")
open(src, "w", encoding="utf-8").write("\n".join(md))

out = os.path.join(WORK, "eqs.docx")
subprocess.run(["pandoc", "-f", "markdown", "-t", "docx", src, "-o", out], check=True)

with zipfile.ZipFile(out) as z:
    doc = z.read("word/document.xml").decode("utf-8")

# separa por paragrafos e casa marcador -> oMath seguinte
paras = re.findall(r"<w:p\b.*?</w:p>|<w:p\b[^>]*/>", doc, re.S)
res, pend = {}, None
for p in paras:
    txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
    mk = re.match(r"^MARCA(.+?)MARCA$", txt.strip())
    if mk:
        pend = mk.group(1); continue
    ms = re.findall(r"<m:oMath>.*?</m:oMath>", p, re.S)
    if ms and pend is not None:
        res[pend] = ms
        pend = None

missing = [n for n, _ in EQS if n not in res]
if missing:
    print("FALTANDO:", missing); sys.exit(1)

# Palavras reservadas do StarMath: se um <m:r> fundido coincidir com uma delas,
# o LibreOffice interpreta como operador e imprime o marcador de erro.
RESERVADAS = set("""abs acute aleph alignb alignc alignl alignr alignt and approx arccos
arccot arcsin arctan arcosh arcoth arsinh artanh backepsilon bar binom bold boper breve
bslash cdot check circ circle color coprod cos cosh cot coth csub csup dddot ddot def div
divides dlarrow dlrarrow dot downarrow drarrow emptyset equiv exists exp fact fixed font
forall from func ge geslant gg grave gt hat hbar iiint iint in infinite infinity int intd
ital italic lambdabar langle lbrace lceil ldbracket ldline le left leftarrow leslant lfloor
lim liminf limsup lint ll llint lllint ln log lsub lsup matrix minusplus mline nabla nbold
ncirc ndivides neg neq newline ni nitalic nospace notin nroot nsubset nsubseteq nsupset
nsupseteq odivide odot ominus oper oplus or ortho otimes over overbrace overline overstrike
owns parallel partial phantom plusminus prod prop rangle rbrace rceil rdbracket rdline re
red rfloor right rightarrow rsub rsup sans serif setc setminus setn setq setr setz sim
simeq sin sinh size slash sqrt stack sub subset subseteq sum sup supset supseteq tan tanh
tilde times to toward transl transr uoper underbrace underline uparrow vec weierp widebar
widehat widetilde widevec wp black blue green cyan magenta yellow gray lime maroon navy
olive purple silver teal aqua fuchsia nospace""".split())

RUN = re.compile(r"<m:r>(?P<pr>(?:<m:rPr>.*?</m:rPr>)?)<m:t(?:\s[^>]*)?>(?P<t>.*?)</m:t></m:r>", re.S)
CAM = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'

def _run(pr, t):
    sp = ' xml:space="preserve"' if t != t.strip() or "  " in t else ""
    return "<m:r>%s%s<m:t%s>%s</m:t></m:r>" % (pr, CAM, sp, t)

def junta(x):
    """Funde <m:r> adjacentes de mesmas propriedades e injeta a fonte matematica."""
    out, pos, ms, i = [], 0, list(RUN.finditer(x)), 0
    while i < len(ms):
        m = ms[i]
        out.append(x[pos:m.start()])
        pr, t, end, j = m.group("pr"), m.group("t"), m.end(), i + 1
        while j < len(ms) and ms[j].start() == end and ms[j].group("pr") == pr:
            t += ms[j].group("t"); end = ms[j].end(); j += 1
        t = t.replace("  ", "\u2003\u2003")   # \qquad -> dois quadratins
        if t.lower() in RESERVADAS and len(t) > 1:
            out.extend(_run(pr, ch) for ch in t)   # evita colisao com o StarMath
        else:
            out.append(_run(pr, t))
        pos, i = end, j
    out.append(x[pos:])
    return "".join(out)

def limpa(x):
    # remove declaracoes de namespace: o documento final declara m: e w: no nivel raiz
    x = re.sub(r'\sxmlns:(m|w|mc|w14)="[^"]*"', "", x)
    x = re.sub(r'\smc:Ignorable="[^"]*"', "", x)
    return junta(x)

final = {n: [limpa(x) for x in res[n]] for n, _ in EQS}
json.dump(final, open(os.path.join(BASE, "build", "omml.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("OK: %d equacoes convertidas" % len(final))
for n, _ in EQS[:3]:
    print(n, "->", final[n][0][:150])
