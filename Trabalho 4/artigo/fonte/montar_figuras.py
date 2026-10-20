"""Prepara as capturas dos esquemáticos PLECS para o artigo.

Entrada: simulação PLECS/simulacao-circuitos/plecs-circ-*.png, capturas feitas na janela do PLECS.
Saída: artigo/figuras/circuito_*.png, com o fundo amarelo-claro do PLECS trocado por branco e
recortadas no conteúdo. Para atualizar uma figura, substitua a captura e rode este script.
Uso: python montar_figuras.py
"""
from pathlib import Path
from PIL import Image, ImageChops
ROOT=Path(__file__).resolve().parents[2]
CIRC=ROOT/'simulação PLECS/simulacao-circuitos';OUT=ROOT/'artigo/figuras'
FUNDO_PLECS=204  # canal azul do fundo (255, 255, 204)
MARGEM=12
FIGURAS={'plecs-circ-rede':'circuito_rede','plecs-circ-bateria':'circuito_bateria','plecs-circ-barramento-cc':'circuito_barramento'}
def fundo_branco(img):
    """Reescala o canal azul para que o fundo vire branco; os traços anti-aliasing misturam sem halo."""
    r,g,b=img.split()
    return Image.merge('RGB',(r,g,b.point(lambda v:min(255,round(v*255/FUNDO_PLECS)))))
def recortar(img):
    caixa=ImageChops.difference(img,Image.new('RGB',img.size,'white')).point(lambda v:255 if v>24 else 0).getbbox()
    x0,y0,x1,y1=caixa
    tela=Image.new('RGB',(x1-x0+2*MARGEM,y1-y0+2*MARGEM),'white');tela.paste(img.crop(caixa),(MARGEM,MARGEM));return tela
for origem,destino in FIGURAS.items():
    img=recortar(fundo_branco(Image.open(CIRC/(origem+'.png')).convert('RGB')))
    img.save(OUT/(destino+'.png'),optimize=True);print(destino,img.size)
