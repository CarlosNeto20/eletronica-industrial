"""Figuras autorais do artigo que nao vem de dados: diagrama de blocos e circuito do CC-CC.

O diagrama de blocos redesenha a ideia da Figura 1 da planilha com os elementos deste
trabalho; o circuito do CC-CC e desenhado com schemdraw a partir da topologia identificada
no Anexo 01. Nenhum valor numerico e inventado: os rotulos vem de parametros.json.
Uso: python artigo/fonte/gerar_figuras_artigo.py   (requer matplotlib e schemdraw)
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / 'artigo' / 'figuras'
FIG.mkdir(parents=True, exist_ok=True)
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
TINTA = '#1f1f1f'
AZUL, LARANJA, VERDE, VIOLETA = '#2a78d6', '#eb6834', '#1baf7a', '#6250d6'
plt.rcParams.update({'font.family': 'serif', 'font.size': 7.6})


def caixa(ax, x, y, w, h, txt, cor, fs=7.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.06', fc='white', ec=cor, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', color=TINTA, fontsize=fs, linespacing=1.15)


def seta(ax, x0, y0, x1, y1, cor=TINTA, estilo='-|>'):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=estilo, color=cor, lw=1.0, shrinkA=0, shrinkB=0))


def arquitetura():
    fig, ax = plt.subplots(figsize=(3.45, 2.5))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 7.3)
    ax.axis('off')
    s = P['especificacoes']
    cc = P['cc_cc']['planilha']
    caixa(ax, 0.05, 5.2, 1.95, 1.4, 'Rede\n%d a %d V\n60 Hz' % (s['Viminef'], s['Vimaxef']), TINTA, fs=6.4)
    caixa(ax, 2.45, 5.2, 2.0, 1.4, 'Retificador\nem ponte\ne C4', AZUL)
    caixa(ax, 6.05, 5.2, 1.75, 1.4, 'Inversor\nunipolar\n20 kHz', LARANJA, fs=7.0)
    caixa(ax, 8.25, 5.2, 2.3, 1.4, 'Filtro LC\ne carga\n115 V', LARANJA, fs=7.0)
    caixa(ax, 0.05, 2.3, 1.95, 1.4, 'Baterias\n%d a %d V' % (cc['Vibmin'], cc['Vibmax']), TINTA, fs=6.6)
    caixa(ax, 2.45, 2.3, 2.0, 1.4, 'CC-CC de\nalto ganho\n(3 estados)', VERDE)
    caixa(ax, 5.8, 0.2, 4.75, 1.35, 'Controle: $H_v$ e $C_v(s)$ Tipo 3;\nportadoras a 180° (unipolar)', VIOLETA, fs=6.7)
    seta(ax, 2.0, 5.9, 2.45, 5.9)
    ax.text(2.22, 6.75, 'SS2', ha='center', fontsize=6.8)
    ax.plot([2.22, 2.22], [6.1, 6.6], color=TINTA, lw=.8)
    ax.plot([4.45, 5.2], [5.9, 5.9], color=TINTA, lw=1.0)
    ax.plot([5.2, 5.2], [3.0, 5.9], color=TINTA, lw=2.2)
    seta(ax, 5.2, 5.9, 6.05, 5.9)
    seta(ax, 2.0, 3.0, 2.45, 3.0)
    seta(ax, 4.45, 3.0, 5.2, 3.0)
    ax.text(5.34, 4.45, 'barramento\n210 a 373 V', rotation=90, va='center', ha='left', fontsize=6.4)
    seta(ax, 7.8, 5.9, 8.25, 5.9)
    seta(ax, 9.35, 5.2, 9.35, 1.55, cor=VIOLETA)
    seta(ax, 6.9, 1.55, 6.9, 5.2, cor=VIOLETA)
    ax.text(9.45, 3.4, '$v_o$', fontsize=7.4, color=VIOLETA)
    ax.text(7.0, 3.4, 'PWM', fontsize=7.0, color=VIOLETA)
    ax.text(3.45, 4.6, 'modo rede', ha='center', fontsize=6.6, color=AZUL)
    ax.text(3.45, 1.7, 'modo bateria', ha='center', fontsize=6.6, color=VERDE)
    fig.tight_layout(pad=.1)
    for ext in ('png', 'pdf'):
        fig.savefig(FIG / f'arquitetura.{ext}', dpi=300)
    plt.close(fig)


def circuito_cc():
    """Celula de tres estados com autotransformador, secundario em ponte e C7 empilhado sobre C8."""
    import schemdraw
    import schemdraw.elements as elm
    schemdraw.config(fontsize=9, lw=1.1, font='serif', bgcolor='white')
    yb, yw, yM, yT = 0.0, 4.4, 6.6, 8.8
    xA, xT, xB, xM, xo = 1.0, 3.2, 5.4, 7.6, 9.0
    with schemdraw.Drawing(show=False) as d:
        d.add(elm.Battery().reverse().at((xT, yb)).to((xT, 1.6)).label('$V_{bat}$', loc='bottom', ofst=0.15))
        d.add(elm.Inductor2(loops=3).at((xT, 1.6)).to((xT, yw - 0.05)).label('$L_b$', loc='bottom', ofst=0.15))
        d.add(elm.Dot().at((xT, yw)))
        d.add(elm.Inductor2(loops=2).at((xA, yw)).to((xT, yw)).label('$N_p$', loc='top'))
        d.add(elm.Inductor2(loops=2).at((xT, yw)).to((xB, yw)).label('$N_p$', loc='top'))
        d.add(elm.Dot().at((xA, yw)))
        d.add(elm.Dot().at((xB, yw)))
        f1 = d.add(elm.NFet(bulk=False).theta(0).reverse().anchor('drain').at((xA, yw)))
        d.add(elm.Line().at(f1.source).to((xA, yb)))
        d.add(elm.Label().at((f1.gate[0] - 0.1, f1.gate[1] + 0.45)).label('$S_1$'))
        f2 = d.add(elm.NFet(bulk=False).theta(0).anchor('drain').at((xB, yw)))
        d.add(elm.Line().at(f2.source).to((xB, yb)))
        d.add(elm.Label().at((f2.gate[0] + 0.1, f2.gate[1] + 0.45)).label('$S_2$'))
        d.add(elm.Diode().at((xA, yw)).to((xA, yM)).label('$D_{17}$', loc='bottom'))
        d.add(elm.Diode().at((xB, yw)).to((xB, yM)).label('$D_{18}$', loc='top'))
        d.add(elm.Line().at((xA, yM)).to((xM, yM)))
        d.add(elm.Dot().at((xM, yM)).label('M', loc='right', ofst=0.1))
        d.add(elm.Capacitor().at((xM, yM)).to((xM, yb)).label('$C_8$', loc='bottom'))
        d.add(elm.Capacitor().at((xM, yM)).to((xM, yT)).label('$C_7$', loc='bottom'))
        d.add(elm.Line().at((xA, yb)).to((xo, yb)))
        d.add(elm.Dot().at((xM, yb)))
        d.add(elm.Dot().at((xT, yb)))
        d.add(elm.Dot().at((xB, yb)))
        d.add(elm.Dot(open=True).at((xo, yb)).label('$-$', loc='right'))
        # secundario e ponte D13-D16
        d.add(elm.Inductor2(loops=2).at((2.6, 7.2)).to((2.6, 8.4)).label('$N_s$', loc='bottom'))
        d.add(elm.Line().at((2.6, 8.4)).to((3.3, 8.4)))
        d.add(elm.Line().at((2.6, 7.2)).to((3.3, 7.2)))
        ponte = d.add(elm.Ic(pins=[elm.IcPin(side='L', anchorname='a1', slot='2/2'), elm.IcPin(side='L', anchorname='a2', slot='1/2'),
                                   elm.IcPin(side='R', anchorname='p', slot='2/2'), elm.IcPin(side='R', anchorname='n', slot='1/2')],
                                   size=(1.6, 1.2), label='D13 a D16', lblsize=8, pinspacing=1.2).anchor('a1').at((3.3, 8.4)))
        d.add(elm.Line().at(ponte.p).to((ponte.p[0] + 0.4, ponte.p[1])))
        d.add(elm.Line().at((ponte.p[0] + 0.4, ponte.p[1])).to((ponte.p[0] + 0.4, yT)))
        d.add(elm.Line().at((ponte.p[0] + 0.4, yT)).to((xo, yT)))
        d.add(elm.Dot().at((xM, yT)))
        d.add(elm.Dot(open=True).at((xo, yT)).label('$+V_{bus}$', loc='right'))
        d.add(elm.Line().at(ponte.n).to((ponte.n[0] + 0.4, ponte.n[1])))
        d.add(elm.Line().at((ponte.n[0] + 0.4, ponte.n[1])).to((ponte.n[0] + 0.4, yM)))
        d.add(elm.Dot().at((ponte.n[0] + 0.4, yM)))
        d.save(str(FIG / 'circuito_cc.svg'))
        d.save(str(FIG / 'circuito_cc.png'), dpi=300)


if __name__ == '__main__':
    arquitetura()
    try:
        circuito_cc()
    except Exception as ex:  # o circuito e opcional; o diagrama de blocos e obrigatorio
        print('circuito do CC-CC nao gerado:', repr(ex))
    print('figuras em', FIG)
