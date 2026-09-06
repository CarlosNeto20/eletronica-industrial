# -*- coding: utf-8 -*-
"""Confere se cada numero do artigo aparece tambem no memorial em .md."""
import glob, importlib.util, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = "/mnt/user-data/outputs/desenvolvimento"

spec = importlib.util.spec_from_file_location("conteudo", os.path.join(BASE, "conteudo.py"))
K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)

memo = ""
for f in sorted(glob.glob(os.path.join(MD, "*.md"))):
    memo += open(f, encoding="utf-8").read()
memo = memo.replace("{,}", ",").replace("{.}", ".").replace("\\,", "")
memo_n = set(re.findall(r"\d+(?:[.,]\d+)*", memo))

def numeros(t):
    t = t.replace("{,}", ",").replace("{.}", ".").replace("\\,", "")
    return re.findall(r"\d+(?:[.,]\d+)*", t)

art = []
art.append(("resumo", K.RESUMO))
for b in K.C:
    if b[0] in ("p", "h1", "h2"): art.append((b[0], b[1]))
    elif b[0] == "eq":            art.append(("eq" + b[2], b[1]))
    elif b[0] == "fig":           art.append(("fig", b[2]))
    elif b[0] == "tab":
        art.append(("tab", b[1]))
        for r in b[2]:
            for c in r: art.append(("tab:" + b[1][:18], c))
        if b[5]: art.append(("tabnota", b[5]))

IGNORA = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
          "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "0", "100", "50",
          "1000", "1.5", "1.10", "1.12", "1.35", "1.36", "1.6.5"}
faltando = []
for onde, txt in art:
    for n in numeros(txt):
        if n in IGNORA or n in memo_n: continue
        # tolera equivalencias de formatacao (1.010,20 vs 1010,20)
        alt = n.replace(".", "")
        if alt in memo_n: continue
        faltando.append((onde, n, txt[:70]))
for onde, n, t in faltando:
    print("AUSENTE  %-14s %-12s | %s" % (onde, n, t))
print("numeros do artigo sem correspondencia no memorial:", len(faltando))
