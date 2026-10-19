"""Formas de onda teóricas do retificador em ponte com filtro capacitivo.

Redesenho da Figura 2 da planilha do professor, com letras maiores: recortada
do PDF e reduzida à largura de uma coluna do artigo, a original ficava ilegível.
Mesmo conteúdo: tensão no capacitor, correntes em dois diodos e corrente no
capacitor, com o pulso de carga aproximado por um retângulo. A ondulação está
exagerada (15 %) para que o ângulo de condução apareça.

Uso: python retificador_formas.py   ->   ../ret-formas-teoricas.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SAIDA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERM = "#d62728"
pi = np.pi


def main():
    vmin = 0.85                                   # V_C1min / V_C1max
    th = pi / 2 - np.arcsin(vmin)                 # ângulo de condução
    x = np.linspace(0, 4 * pi, 8000)
    fase = np.mod(x, pi)                          # o retificador repete a cada meio ciclo
    cond = (fase >= pi / 2 - th) & (fase <= pi / 2)
    # tensão no capacitor: segue a senoide na condução e decresce linearmente no resto
    desc = np.mod(fase - pi / 2, pi) / (pi - th)
    vc = np.where(cond, np.abs(np.sin(x)), 1 - (1 - vmin) * desc)
    ichg, io = 1.0, 0.22
    semi = np.floor(x / pi).astype(int)           # índice do semiciclo
    id1 = np.where(cond & (semi % 2 == 0), ichg, 0.0)
    id2 = np.where(cond & (semi % 2 == 1), ichg, 0.0)
    ic = np.where(cond, ichg - io, -io)

    with plt.rc_context({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False}):
        fig, ax = plt.subplots(4, 1, figsize=(3.5, 4.0), sharex=True,
                               gridspec_kw={"height_ratios": [1.5, 1, 1, 1]})
        ax[0].plot(x, np.abs(np.sin(x)), color="0.35", lw=0.7, ls="--")
        ax[0].plot(x, vc, color="k", lw=1.8)
        ax[0].set_yticks([0, vmin, 1])
        ax[0].set_yticklabels(["0", r"$V_{C1min}$", r"$V_{C1max}$"])
        ax[0].set_ylim(0, 1.22)
        ax[0].set_ylabel(r"$v_{C1}$")
        ax[0].annotate("", xy=(pi, 1.0), xytext=(pi, vmin),
                       arrowprops=dict(arrowstyle="<->", lw=0.8, shrinkA=0, shrinkB=0))
        ax[0].text(pi + 0.15, 1.04, r"$\Delta V_{C1}$", fontsize=9, va="bottom")
        for a, y, rot, ticks, labels, lim in (
                (ax[1], id1, r"$i_{D1}$", [0, ichg], ["0", r"$I_{chg}$"], (-0.25, 1.35)),
                (ax[2], id2, r"$i_{D2}$", [0, ichg], ["0", r"$I_{chg}$"], (-0.25, 1.35)),
                (ax[3], ic, r"$i_{C1}$", [-io, 0, ichg - io], [r"$-I_{oeq}$", "0", r"$I_{chg}-I_{oeq}$"],
                 (-0.5, 1.15))):
            a.plot(x, y, color=VERM, lw=1.6)
            a.set_yticks(ticks)
            a.set_yticklabels(labels)
            a.set_ylim(*lim)
            a.set_ylabel(rot)
        # ângulo de condução no primeiro pulso
        ax[1].annotate("", xy=(pi / 2, -0.13), xytext=(pi / 2 - th, -0.13),
                       arrowprops=dict(arrowstyle="<->", lw=0.8, shrinkA=0, shrinkB=0))
        ax[1].text(pi / 2 + 0.15, -0.13, r"$\theta$", fontsize=9, va="center")
        for a in ax:
            a.grid(True, axis="y", color="0.85", lw=0.5, ls=":")
            for k in range(1, 9):
                a.axvline(k * pi / 2, color="0.75", lw=0.5, ls=":")
            a.yaxis.set_label_coords(-0.27, 0.5)
            a.set_ylabel(a.get_ylabel(), rotation=0, va="center", ha="center", fontsize=10)
        ax[3].set_xticks([k * pi / 2 for k in range(1, 9)])
        ax[3].set_xticklabels([r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$", r"$5\pi/2$", r"$3\pi$",
                               r"$7\pi/2$", r"$4\pi$"], fontsize=8)
        ax[3].set_xlim(0, 4 * pi)
        ax[3].set_xlabel(r"$\omega t$ (rad)")
        fig.tight_layout(pad=0.5)
        fig.subplots_adjust(left=0.33)
        fig.savefig(os.path.join(SAIDA, "ret-formas-teoricas.png"), dpi=400)
        plt.close(fig)
    print("gravado:", os.path.join(SAIDA, "ret-formas-teoricas.png"))


if __name__ == "__main__":
    main()
