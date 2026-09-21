"""Primitivas de desenho de esquemáticos (matplotlib) no estilo das Figs. 3 e 17.

Cada ramo do circuito é desenhado com um estado "ativo": ramos ativos (por
onde circula corrente na etapa) saem em traço grosso vinho; os demais, em
traço fino. Os símbolos ficam em azul e os rótulos de corrente em vermelho,
como nas figuras do enunciado.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIO = "#9c6b86"        # fio inativo
ATIVO = "#6d1a36"      # caminho de corrente
SIMB = "#1a3fa0"       # símbolos
CORR = "#d62728"       # setas e rótulos de corrente
LW_FIO, LW_ATIVO, LW_SIMB = 1.0, 3.4, 1.3


class Esquema:
    def __init__(self, largura=12, altura=6.5):
        self.fig, self.ax = plt.subplots(figsize=(largura * 0.62, altura * 0.62))
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    # ------------------------------------------------------------ básicos
    def fio(self, pts, on=False):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=ATIVO if on else FIO, lw=LW_ATIVO if on else LW_FIO,
                     solid_capstyle="round", solid_joinstyle="round", zorder=2)

    def no(self, x, y):
        self.ax.plot(x, y, "o", color="#e040c0", ms=3.2, zorder=5)

    def texto(self, x, y, s, cor=SIMB, tam=9, ha="center", va="center"):
        self.ax.text(x, y, s, color=cor, fontsize=tam, ha=ha, va=va, family="serif", zorder=6)

    def seta(self, x, y, direcao, rotulo=None, dx_rot=0.0, dy_rot=0.0):
        """Seta vermelha de corrente centrada em (x, y)."""
        v = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[direcao]
        L = 0.45
        self.ax.annotate("", xy=(x + v[0] * L / 2, y + v[1] * L / 2),
                         xytext=(x - v[0] * L / 2, y - v[1] * L / 2),
                         arrowprops=dict(arrowstyle="-|>", color=CORR, lw=1.6,
                                         mutation_scale=11), zorder=7)
        if rotulo:
            self.texto(x + dx_rot, y + dy_rot, rotulo, cor=CORR, tam=8.5)

    # ------------------------------------------------------------ ramos verticais
    def ramo_v(self, x, y1, y2, simbolo, on=False, rotulo=None, lado=0.45, **kw):
        """Ramo vertical de y1 a y2 (y1 > y2) com um símbolo no meio."""
        ym = (y1 + y2) / 2
        h = kw.pop("h", 0.8)
        self.fio([(x, y1), (x, ym + h / 2)], on)
        self.fio([(x, ym - h / 2), (x, y2)], on)
        getattr(self, "_" + simbolo)(x, ym, h, on, **kw)
        if rotulo:
            self.texto(x + lado, ym, rotulo, ha="left" if lado > 0 else "right")

    def ramo_h(self, y, x1, x2, simbolo, on=False, rotulo=None, **kw):
        """Ramo horizontal de x1 a x2 com um símbolo no meio (desenhado girado)."""
        xm = (x1 + x2) / 2
        h = kw.pop("h", 0.8)
        self.fio([(x1, y), (xm - h / 2, y)], on)
        self.fio([(xm + h / 2, y), (x2, y)], on)
        getattr(self, "_" + simbolo + "_h")(xm, y, h, on, **kw)
        if rotulo:
            self.texto(xm, y + 0.45, rotulo)

    # ------------------------------------------------------------ símbolos
    def _cor(self, on):
        return (ATIVO if on else SIMB), (LW_SIMB + 0.8 if on else LW_SIMB)

    def _fonte(self, x, y, h, on):
        c, lw = self._cor(on)
        for k, (w, dy) in enumerate([(0.5, 0.15), (0.3, 0.05), (0.5, -0.05), (0.3, -0.15)]):
            self.ax.plot([x - w / 2, x + w / 2], [y + dy, y + dy], color=c, lw=lw)
        self.fio([(x, y + h / 2), (x, y + 0.15)], on)
        self.fio([(x, y - 0.15), (x, y - h / 2)], on)
        self.texto(x + 0.35, y + 0.3, "+", tam=8)

    def _res(self, x, y, h, on):
        c, lw = self._cor(on)
        n = 6
        ys = np.linspace(y + h / 2, y - h / 2, 2 * n + 1)
        xs = [x] + [x + (0.18 if k % 2 else -0.18) for k in range(1, 2 * n)] + [x]
        self.ax.plot(xs, ys, color=c, lw=lw)

    def _ind(self, x, y, h, on):
        c, lw = self._cor(on)
        n = 4
        r = h / (2 * n)
        for k in range(n):
            yc = y + h / 2 - r * (2 * k + 1)
            t = np.linspace(-np.pi / 2, np.pi / 2, 30)
            self.ax.plot(x + r * np.cos(t), yc + r * np.sin(t), color=c, lw=lw)

    def _ind_h(self, x, y, h, on):
        c, lw = self._cor(on)
        n = 4
        r = h / (2 * n)
        for k in range(n):
            xc = x - h / 2 + r * (2 * k + 1)
            t = np.linspace(0, np.pi, 30)
            self.ax.plot(xc + r * np.cos(t), y + r * np.sin(t), color=c, lw=lw)

    def _cap(self, x, y, h, on):
        c, lw = self._cor(on)
        self.fio([(x, y + h / 2), (x, y + 0.08)], on)
        self.fio([(x, y - 0.08), (x, y - h / 2)], on)
        self.ax.plot([x - 0.25, x + 0.25], [y + 0.08] * 2, color=c, lw=lw + 0.6)
        self.ax.plot([x - 0.25, x + 0.25], [y - 0.08] * 2, color=c, lw=lw + 0.6)
        self.texto(x + 0.3, y + 0.25, "+", tam=7)

    def _diodo(self, x, y, h, on, para="up"):
        """Diodo vertical; 'para' é o sentido de condução (anodo -> catodo)."""
        c, lw = self._cor(on)
        s = 1 if para == "up" else -1
        tri = [(x - 0.22, y - s * 0.16), (x + 0.22, y - s * 0.16), (x, y + s * 0.16)]
        self.ax.fill(*zip(*tri), color=c, zorder=4)
        self.ax.plot([x - 0.22, x + 0.22], [y + s * 0.16] * 2, color=c, lw=lw + 0.4)
        self.fio([(x, y + h / 2), (x, y + 0.16)], on)
        self.fio([(x, y - 0.16), (x, y - h / 2)], on)

    def _diodo_h(self, x, y, h, on, para="right"):
        c, lw = self._cor(on)
        s = 1 if para == "right" else -1
        tri = [(x - s * 0.16, y - 0.22), (x - s * 0.16, y + 0.22), (x + s * 0.16, y)]
        self.ax.fill(*zip(*tri), color=c, zorder=4)
        self.ax.plot([x + s * 0.16] * 2, [y - 0.22, y + 0.22], color=c, lw=lw + 0.4)
        self.fio([(x - h / 2, y), (x - 0.16, y)], on)
        self.fio([(x + 0.16, y), (x + h / 2, y)], on)

    def _mosfet(self, x, y, h, on, gate="left"):
        """MOSFET de canal N (dreno em cima), com gatilho do lado indicado."""
        c, lw = self._cor(on)
        g = -1 if gate == "left" else 1
        # canal
        self.ax.plot([x + g * 0.05] * 2, [y - 0.25, y + 0.25], color=c, lw=lw + 0.6)
        self.ax.plot([x, x + g * 0.05], [y + 0.2, y + 0.2], color=c, lw=lw)
        self.ax.plot([x, x + g * 0.05], [y - 0.2, y - 0.2], color=c, lw=lw)
        self.fio([(x, y + h / 2), (x, y + 0.2)], on)
        self.fio([(x, y - 0.2), (x, y - h / 2)], on)
        # gatilho
        self.ax.plot([x + g * 0.15] * 2, [y - 0.22, y + 0.22], color=SIMB, lw=LW_SIMB)
        self.ax.plot([x + g * 0.15, x + g * 0.5], [y - 0.15, y - 0.15], color="#d0302a", lw=LW_SIMB)

    def _trafo(self, x, y, h, on_p, on_s, n_esp=4, pontos=("top", "top")):
        """Transformador: primário em x-0.35, secundário em x+0.35, núcleo no meio."""
        for dx, on in ((-0.35, on_p), (0.35, on_s)):
            c, lw = self._cor(on)
            r = h / (2 * n_esp)
            for k in range(n_esp):
                yc = y + h / 2 - r * (2 * k + 1)
                t = np.linspace(-np.pi / 2, np.pi / 2, 30)
                sgn = 1 if dx < 0 else -1
                self.ax.plot(x + dx + sgn * r * np.cos(t), yc + r * np.sin(t), color=c, lw=lw)
        for dx in (-0.06, 0.06):
            self.ax.plot([x + dx] * 2, [y - h / 2, y + h / 2], color=SIMB, lw=1.4)
        for dx, p in ((-0.35, pontos[0]), (0.35, pontos[1])):
            yy = y + (h / 2 - 0.05) if p == "top" else y - (h / 2 - 0.05)
            self.ax.plot(x + dx + (-0.22 if dx < 0 else 0.22), yy, "o", color="k", ms=3.5)

    def bobina(self, x, y1, y2, lado, on=False, n_esp=None):
        """Enrolamento vertical de y1 (alto) a y2; lado = +1 (ondas à direita) ou -1."""
        c, lw = self._cor(on)
        h = y1 - y2
        n = n_esp or max(2, int(round(h / 0.3)))
        r = h / (2 * n)
        for k in range(n):
            yc = y1 - r * (2 * k + 1)
            t = np.linspace(-np.pi / 2, np.pi / 2, 30)
            self.ax.plot(x + lado * r * np.cos(t), yc + r * np.sin(t), color=c, lw=lw)

    def nucleo(self, x, y1, y2):
        for dx in (-0.06, 0.06):
            self.ax.plot([x + dx] * 2, [y2, y1], color=SIMB, lw=1.4)

    def ponto(self, x, y):
        self.ax.plot(x, y, "o", color="k", ms=3.5, zorder=6)

    def fio_salto(self, pts, x_salto, on=False, r=0.13):
        """Fio horizontal de pts[0] a pts[1] com um salto (cruzamento sem ligação) em x_salto."""
        (x1, y), (x2, _) = pts
        s = 1 if x2 > x1 else -1
        self.fio([(x1, y), (x_salto - s * r, y)], on)
        self.fio([(x_salto + s * r, y), (x2, y)], on)
        t = np.linspace(np.pi, 0, 20) if s > 0 else np.linspace(0, np.pi, 20)
        self.ax.plot(x_salto + r * np.cos(t), y + r * np.sin(t),
                     color=ATIVO if on else FIO, lw=LW_ATIVO if on else LW_FIO)

    # ------------------------------------------------------------ saída
    def salvar(self, caminho, titulo=None):
        if titulo:
            self.ax.set_title(titulo, fontsize=10, family="serif", pad=18)
        self.fig.tight_layout()
        self.fig.savefig(caminho, dpi=400, bbox_inches="tight")
        plt.close(self.fig)
