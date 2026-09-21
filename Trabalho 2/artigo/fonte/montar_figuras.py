"""Monta as figuras do artigo em artigo/figuras a partir de:
  - documento explicativo/imagens   (figuras recortadas do enunciado do professor)
  - desenvolvimento/figuras          (etapas desenhadas e resultados do PLECS)
Figuras compostas (etapas, pares de degraus) são montadas lado a lado ou em grade.
Uso: python montar_figuras.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(AQUI)
T2 = os.path.dirname(ART)
PROF = os.path.join(T2, "documento explicativo", "imagens")
DEV = os.path.join(T2, "desenvolvimento", "figuras")
OUT = os.path.join(ART, "figuras")


def abrir(pasta, nome):
    return Image.open(os.path.join(pasta, nome + ".png")).convert("RGB")


def rotulo(img, texto):
    """Acrescenta um rótulo centralizado abaixo da imagem, ex. '(a)'."""
    h = max(40, img.height // 12)
    novo = Image.new("RGB", (img.width, img.height + h), "white")
    novo.paste(img, (0, 0))
    d = ImageDraw.Draw(novo)
    try:
        fonte = ImageFont.truetype("times.ttf", int(h * 0.6))
    except OSError:
        fonte = ImageFont.load_default()
    w = d.textlength(texto, font=fonte)
    d.text(((img.width - w) / 2, img.height + h * 0.15), texto, fill="black", font=fonte)
    return novo


def fundo_branco(img):
    """Troca o fundo amarelo-claro do esquemático do PLECS por branco (melhor para impressão)."""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            if r > 235 and g > 235 and 170 < b < 245:
                px[x, y] = (255, 255, 255)
    return img


def largura(img, w):
    return img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)


def grade(imgs, colunas, margem=30):
    """Grade de imagens com a mesma largura de célula."""
    w = max(i.width for i in imgs)
    imgs = [largura(i, w) for i in imgs]
    linhas = [imgs[k:k + colunas] for k in range(0, len(imgs), colunas)]
    alturas = [max(i.height for i in ln) for ln in linhas]
    W = colunas * w + (colunas - 1) * margem
    H = sum(alturas) + (len(linhas) - 1) * margem
    tela = Image.new("RGB", (W, H), "white")
    y = 0
    for ln, h in zip(linhas, alturas):
        for c, im in enumerate(ln):
            tela.paste(im, (c * (w + margem), y))
        y += h + margem
    return tela


def salvar(img, nome, max_largura=3000):
    if img.width > max_largura:
        img = largura(img, max_largura)
    img.save(os.path.join(OUT, nome + ".png"), dpi=(300, 300))
    print("%-28s %5d x %5d" % (nome, img.width, img.height))


def main():
    os.makedirs(OUT, exist_ok=True)
    # ---------------- cópias diretas (topologias e formas de onda do enunciado)
    for origem, destino in [("fig01-forward-topologia", "fwd-topologia"),
                            ("fig02-forward-formas-onda", "fwd-formas"),
                            ("fig06-fullbridge-topologia", "fb-topologia"),
                            ("fig07-fullbridge-formas-onda", "fb-formas"),
                            ("fig10-pushpull-topologia", "pp-topologia"),
                            ("fig11-pushpull-formas-onda", "pp-formas"),
                            ("fig15-flyback-topologia", "fly-topologia"),
                            ("fig16-flyback-formas-onda", "fly-formas")]:
        salvar(abrir(PROF, origem), destino)
    # ---------------- etapas de operação
    salvar(grade([abrir(PROF, "fig03%s-forward-etapa%d" % (l, k))
                  for l, k in (("a", 1), ("b", 2), ("c", 3))], 1), "fwd-etapas")
    salvar(grade([abrir(DEV, "etapas-fullbridge-%d" % k) for k in (1, 2, 3, 4)], 2), "fb-etapas")
    salvar(grade([abrir(DEV, "etapas-pushpull-%d" % k) for k in (1, 2, 3, 4)], 2), "pp-etapas")
    salvar(grade([abrir(PROF, "fig17%s-flyback-etapa%d" % (l, k))
                  for l, k in (("a", 1), ("b", 2), ("c", 3))], 1), "fly-etapas")
    # ---------------- esquemáticos do PLECS (capturas feitas pela equipe), fundo branco
    circ = os.path.join(T2, "simulação PLECS", "simulacao-circuitos")
    for caso, nome in [("forward", "fwd"), ("fullbridge", "fb"), ("pushpull", "pp"),
                       ("flyback", "fly")]:
        salvar(fundo_branco(abrir(circ, "plecs-circ-%s" % caso)), nome + "-circuito")
    # ---------------- degraus de carga (PLECS): (a) 20->100 %, (b) 100->20 %
    for caso, nome in [("forward", "fwd"), ("fullbridge", "fb"), ("pushpull", "pp"),
                       ("flyback-mcd", "fly-mcd"), ("flyback-mcc", "fly-mcc")]:
        a = rotulo(abrir(DEV, "plecs-%s-degrau-20-100" % caso), "(a)")
        b = rotulo(abrir(DEV, "plecs-%s-degrau-100-20" % caso), "(b)")
        salvar(grade([a, b], 1, margem=40), nome + "-degraus")


if __name__ == "__main__":
    main()
