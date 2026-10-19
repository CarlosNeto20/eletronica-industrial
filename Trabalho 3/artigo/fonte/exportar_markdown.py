# -*- coding: utf-8 -*-
"""Exporta o texto do artigo (conteudo.py) para o memorial em Markdown.

Uso (a partir desta pasta):  python exportar_markdown.py
Saída: ../../desenvolvimento/01-*.md a 05-*.md

No Trabalho 2 o memorial foi escrito antes do artigo. Aqui o texto nasceu em
conteudo.py, e o memorial é gerado dele para que os dois nunca divirjam: cada
seção de primeiro nível do artigo vai para um arquivo, com as equações em
LaTeX, as tabelas em Markdown e as figuras apontando para artigo/figuras.
"""
import importlib.util
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "desenvolvimento")
spec = importlib.util.spec_from_file_location("conteudo", os.path.join(AQUI, "conteudo.py"))
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

# seções do artigo (pelo índice do título de primeiro nível) -> arquivo do memorial
ARQUIVOS = [
    ("01-especificacoes-e-retificador.md", "Especificações e retificador com filtro capacitivo", (0, 1, 2, 3)),
    ("02-forward-de-duas-chaves.md", "Conversor Forward de duas chaves", (4,)),
    ("03-circuito-de-controle.md", "Circuito de controle", (5,)),
    ("04-resultados-de-simulacao.md", "Resultados de simulação", (6,)),
    ("05-conclusoes-e-referencias.md", "Conclusões e referências", (7,)),
]
ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
BASE = "A-Za-zΔΦΨΩαβγδεηθλμνρστφχψω"
TOK = re.compile(r"(?<![%s0-9_.])([%s])_((?:[A-Za-z0-9]+)+)" % (BASE, BASE))


def simbolos(t):
    """X_y -> $X_{y}$, como o artigo mostra (base em itálico, índice subscrito)."""
    return TOK.sub(lambda m: "$%s_{%s}$" % (m.group(1), m.group(2)), t)


def tabela(rows):
    L = ["| " + " | ".join(simbolos(c) for c in rows[0]) + " |", "|" + "---|" * len(rows[0])]
    L += ["| " + " | ".join(simbolos(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(L)


def main():
    secoes, atual = [], None
    n_fig = n_tab = 0
    for b in K.C:
        if b[0] == "h1":
            atual = [b]
            secoes.append(atual)
            continue
        if b[0] == "fig":
            n_fig += 1
            b = b + (n_fig,)
        elif b[0] == "tab":
            n_tab += 1
            b = b + (n_tab,)
        atual.append(b)
    for nome, titulo, idx in ARQUIVOS:
        L = ["# %s" % titulo, "",
             "> Gerado por `artigo/fonte/exportar_markdown.py` a partir de `conteudo.py`. Para "
             "alterar o texto, edite `conteudo.py` e gere de novo. A numeração de seções, figuras, "
             "tabelas e equações é a do artigo.", ""]
        for i in idx:
            for b in secoes[i]:
                k = b[0]
                if k == "h1":
                    L += ["## %s. %s" % (ROMANOS[i], b[1]), ""]
                elif k == "h2":
                    L += ["### %s" % b[1], ""]
                elif k == "p":
                    L += [simbolos(b[1]), ""]
                elif k == "eq":
                    L += ["$$%s \\tag{%s}$$" % (b[1], b[2]), ""]
                elif k == "fig":
                    L += ["![Fig. %d](../artigo/figuras/%s.png)" % (b[4], b[1]), "",
                          "**Fig. %d.** %s" % (b[4], simbolos(b[2])), ""]
                elif k == "tab":
                    L += ["**Tabela %s.** %s" % (ROMANOS[b[6] - 1], simbolos(b[1])), "", tabela(b[2]), ""]
                    if b[5]:
                        L += ["*%s*" % simbolos(b[5]), ""]
        if idx[-1] == len(secoes) - 1:
            L += ["## Referências", ""] + ["[%d] %s" % (n + 1, r) + "\n" for n, r in enumerate(K.REFS)]
        with open(os.path.join(DEV, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(L).rstrip() + "\n")
        print(nome)


if __name__ == "__main__":
    main()
