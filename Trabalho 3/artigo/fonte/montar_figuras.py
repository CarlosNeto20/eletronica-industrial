"""Monta as figuras do artigo em artigo/figuras a partir de:
  - documento explicativo/imagens   (figuras recortadas da planilha e do anexo do professor)
  - desenvolvimento/figuras          (figuras desenhadas, Bode, datasheets e resultados do PLECS)
  - simulação PLECS/simulacao-circuitos (captura do esquemático feita pela equipe, se existir)
Figuras compostas (etapas, comparações com o professor, datasheets) são montadas em grade.
Uso: python montar_figuras.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(AQUI)
T3 = os.path.dirname(ART)
PROF = os.path.join(T3, "documento explicativo", "imagens")
DEV = os.path.join(T3, "desenvolvimento", "figuras")
CIRC = os.path.join(T3, "simulação PLECS", "simulacao-circuitos")
OUT = os.path.join(ART, "figuras")
PRINT_PLECS = "plecs-circ-carregador"


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
            tela.paste(im, (c * (w + margem), y + (h - im.height) // 2))
        y += h + margem
    return tela


def com_margens(img, fracao):
    """Centraliza a imagem numa tela mais larga: no artigo ela ocupa só a fração dada da
    largura da página (figuras de largura total muito altas deixam vazios antes delas)."""
    w = int(img.width / fracao)
    tela = Image.new("RGB", (w, img.height), "white")
    tela.paste(img, ((w - img.width) // 2, 0))
    return tela


def salvar(img, nome, max_largura=3000):
    if img.width > max_largura:
        img = largura(img, max_largura)
    img.save(os.path.join(OUT, nome + ".png"), dpi=(300, 300))
    print("%-22s %5d x %5d" % (nome, img.width, img.height))


def tem_print_plecs():
    return os.path.exists(os.path.join(CIRC, PRINT_PLECS + ".png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    # ---------------- cópias diretas
    for pasta, origem, destino in [
            (PROF, "fig01-retificador-topologia", "ret-topologia"),
            (DEV, "ret-formas-teoricas", "ret-formas"),      # redesenho da Fig. 2 do professor
            (PROF, "fig-datasheet-tdk-b43658", "ds-c1"),
            (DEV, "ds-b41821", "ds-co"),
            (DEV, "fwd2-topologia", "fwd-topologia"),
            (DEV, "fwd2-formas-teoricas", "fwd-formas"),
            (PROF, "fig03-diagrama-blocos-controle", "ctrl-blocos"),
            (PROF, "fig06-compensador-tipo2", "ctrl-tipo2"),
            (DEV, "calc-bode-malha-tensao", "ctrl-bode-tensao"),
            (DEV, "calc-bode-malha-corrente", "ctrl-bode-corrente"),
            (PROF, "anexo-circuito3-tensao-corrente", "ctrl-uc3525"),
            (DEV, "plecs-retificador", "sim-retificador"),
            (DEV, "plecs-forward-regime", "sim-forward"),
            (DEV, "plecs-portadora", "sim-portadora"),
            (DEV, "plecs-degrau-100-20", "sim-degrau-100-20"),
            (DEV, "plecs-degrau-20-100", "sim-degrau-20-100"),
            (DEV, "plecs-curto-detalhe", "sim-curto-detalhe")]:
        salvar(abrir(pasta, origem), destino)
    # ---------------- etapas de operação do Forward de duas chaves
    salvar(grade([abrir(DEV, "fwd2-etapa-%d" % k) for k in (1, 2, 3)], 1), "fwd-etapas")
    # ---------------- datasheets dos semicondutores
    salvar(grade([rotulo(abrir(DEV, n), r) for n, r in (("ds-gbu8", "(a)"), ("ds-irfp460", "(b)"),
                                                        ("ds-uf4005", "(c)"), ("ds-mur3020wt", "(d)"))],
                 2, margem=60), "ds-semicondutores")
    # ---------------- esquemático do professor (PSIM), reduzido a 70 % da largura da página
    salvar(com_margens(abrir(PROF, "fig14-circuito-psim"), 0.70), "sim-circuito-psim", 3600)
    # ---------------- esquemático do PLECS (captura feita pela equipe), fundo branco
    if tem_print_plecs():
        salvar(fundo_branco(abrir(CIRC, PRINT_PLECS)), "sim-circuito-plecs")
    else:
        print("AVISO: falta %s.png em 'simulação PLECS/simulacao-circuitos'; o artigo sai só "
              "com o esquemático do professor." % PRINT_PLECS)
    # ---------------- ensaios: (a) PLECS 176 V, (b) PLECS 264 V, (c) professor (PSIM, 176 V)
    for caso, prof in (("degrau", "fig15-psim-degrau-carga"), ("curto", "fig16-psim-curto-circuito"),
                       ("recarga", "fig17-psim-recarga")):
        a = rotulo(abrir(DEV, "plecs-%s-176" % caso), "(a)")
        b = rotulo(abrir(DEV, "plecs-%s-264" % caso), "(b)")
        c = rotulo(largura(abrir(PROF, prof), a.width), "(c)")
        salvar(grade([a, b, c], 3, margem=40), "sim-" + caso, max_largura=3600)


if __name__ == "__main__":
    main()
