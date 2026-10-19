"""Recorta dos datasheets as tabelas dos componentes comerciais escolhidos.

Uso (a partir desta pasta):  python recortar_datasheets.py
Saída: ../../desenvolvimento/figuras/ds-*.png  (300 dpi)

Cada figura junta o cabeçalho da primeira página (fabricante e código) com a
tabela de valores máximos. Coordenadas em pontos tipográficos (1/72 pol).
Os PDF foram baixados dos sites dos fabricantes (ver LEIA-ME.txt desta pasta).
"""
import os
import io
import pymupdf
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "desenvolvimento", "figuras")

# nome da figura -> (arquivo, [(página, (x0, y0, x1, y1)), ...]) empilhados na vertical
RECORTES = {
    "ds-gbu8": ("GBU8-Vishay.pdf", [(1, (45, 27, 553, 100)), (1, (45, 466, 553, 636))]),
    "ds-irfp460": ("IRFP460-Vishay.pdf", [(1, (54, 27, 560, 100)), (1, (54, 461, 560, 635))]),
    "ds-uf4005": ("UF4001-UF4007-Vishay.pdf", [(1, (45, 27, 553, 100)), (1, (45, 470, 553, 622))]),
    "ds-mur3020wt": ("MUR3020WT-Vishay.pdf", [(1, (54, 27, 560, 104)), (1, (54, 410, 560, 527))]),
    "ds-b41821": ("B41821-B43821-TDK.pdf", [(12, (36, 20, 560, 238))]),
}


def recorte(doc, pag, r, dpi=300):
    pm = doc[pag - 1].get_pixmap(dpi=dpi, clip=pymupdf.Rect(*r))
    return Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for nome, (arq, partes) in RECORTES.items():
        doc = pymupdf.open(os.path.join(AQUI, arq))
        imgs = [recorte(doc, p, r) for p, r in partes]
        w = max(i.width for i in imgs)
        imgs = [i if i.width == w else i.resize((w, int(i.height * w / i.width)), Image.LANCZOS)
                for i in imgs]
        tela = Image.new("RGB", (w, sum(i.height for i in imgs) + 20 * (len(imgs) - 1)), "white")
        y = 0
        for i in imgs:
            tela.paste(i, (0, y))
            y += i.height + 20
        tela.save(os.path.join(SAIDA, nome + ".png"), dpi=(300, 300))
        print("%-16s %d x %d" % (nome, tela.width, tela.height))


if __name__ == "__main__":
    main()
