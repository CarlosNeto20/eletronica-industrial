# -*- coding: utf-8 -*-
"""Gera as figuras do artigo IEEE do Trabalho 1 de Eletronica Industrial."""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Nimbus Roman"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.labelsize": 8,
    "axes.titlesize": 8.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.2,
    "lines.linewidth": 1.25,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "grid.linewidth": 0.4,
    "grid.alpha": 0.35,
    "figure.dpi": 400,
    "savefig.dpi": 400,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

K = "#1a1a1a"
G1 = "#5a5a5a"
G2 = "#9a9a9a"
FILL = "#c9c9c9"

COL1 = 3.45
COL2 = 7.16


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p + ".png")
    fig.savefig(p + ".pdf")
    plt.close(fig)
    print("  ", name)


def clean(ax, spines=("top", "right")):
    for s in spines:
        ax.spines[s].set_visible(False)


def axes_cross(ax, xlab, ylab, xlab_off=(0, 0), ylab_off=(0, 0)):
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, ms=3)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, ms=3)
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    ax.text(x1 + (x1 - x0) * 0.005 + xlab_off[0], 0 + (y1 - y0) * 0.05 + xlab_off[1],
            xlab, fontsize=8, ha="right", va="bottom")
    ax.text(0 + (x1 - x0) * 0.012 + ylab_off[0], y1 + ylab_off[1], ylab,
            fontsize=8, ha="left", va="top")
    ax.set_xticks([]); ax.set_yticks([])


# ---------------------------------------------------------------- Fig. 1
def fig01():
    fig, (a, b) = plt.subplots(1, 2, figsize=(COL2, 2.35))

    # ---- (a) caracteristica real, tres regioes
    v = np.linspace(-1.30, 0.95, 900)
    i = np.where(v > 0, 0.02 * (np.exp(np.clip(v / 0.052, -50, 50)) - 1), -0.05)
    i = np.clip(i, -0.05, 3.0)
    a.plot(v, i, color=K)
    a.plot([-1.30, -1.30], [-0.05, -3.05], color=K)
    a.set_xlim(-2.05, 1.45); a.set_ylim(-3.9, 4.0)
    axes_cross(a, r"$V_F$", r"$I_F$", xlab_off=(-0.02, 0.12))
    a.annotate("polarização\ndireta", xy=(0.30, 2.35), xytext=(0.60, 1.05),
               ha="left", fontsize=7, color=G1,
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.annotate("polarização\nreversa", xy=(-0.70, -0.05), xytext=(-1.15, 1.65),
               fontsize=7, color=G1, ha="center",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.annotate("ruptura", xy=(-1.30, -2.30), xytext=(-0.90, -3.10),
               fontsize=7, color=G1, ha="left", va="center",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.plot([-1.30, -1.30], [-0.05, 0.16], color=K, lw=0.6)
    a.text(-1.34, 0.30, r"$-V_{BR}$", fontsize=7.5, ha="center")
    a.set_title("(a)", y=-0.15, fontsize=8)

    # ---- (b) modelo linear por partes
    rT, VTO = 0.16, 0.72
    vv = np.linspace(-0.35, 1.62, 600)
    ii = np.where(vv > VTO, (vv - VTO) / rT, 0.0)
    ireal = 5.6 / (1 + np.exp(-(vv - 0.90) / 0.085))
    ireal = np.where(vv > 0.35, ireal, 0.0)
    b.plot(vv, np.clip(ireal, 0, 5.6), color=G2, lw=1.0)
    b.plot(vv, np.clip(ii, 0, 5.6), color=K)
    b.set_xlim(-0.45, 2.05); b.set_ylim(-1.05, 7.4)
    axes_cross(b, r"$V_F$", r"$I_F$", xlab_off=(-0.02, 0.12))
    b.annotate("característica real", xy=(0.93, 4.30), xytext=(0.02, 6.55),
               fontsize=7, color=G1, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    b.annotate("modelo linear\npor partes", xy=(1.42, 4.35), xytext=(1.52, 6.15),
               fontsize=7, color=K, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    b.plot([VTO, VTO], [0, -0.28], color=K, lw=0.6)
    b.text(VTO, -0.48, r"$V_{TO}$", ha="center", va="top", fontsize=7.5)
    iF = 3.6
    vF = VTO + rT * iF
    b.plot([0, vF], [iF, iF], ls=":", lw=0.6, color=G1)
    b.plot([vF, vF], [0, iF], ls=":", lw=0.6, color=G1)
    b.plot([vF], [iF], "o", ms=2.8, color=K)
    b.text(-0.07, iF, r"$I_F$", ha="right", va="center", fontsize=7.5)
    b.text(vF, -0.48, r"$V_F$", ha="center", va="top", fontsize=7.5)
    th = np.linspace(0, math.atan2(1 / rT, 1.0), 50)
    Rr = 0.30
    b.plot(VTO + Rr * np.cos(th), 2.30 * Rr * np.sin(th), lw=0.6, color=G1)
    b.text(VTO + 0.14, 0.72, r"$\alpha$", fontsize=7.5)
    b.annotate(r"$r_T = 1/\tan\alpha$", xy=(VTO + 0.30, 0.42),
               xytext=(1.12, 1.05), fontsize=7.5, color=K, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    b.set_title("(b)", y=-0.15, fontsize=8)
    fig.subplots_adjust(wspace=0.20)
    save(fig, "fig01-diodo-caracteristica")


# ---------------------------------------------------------------- Fig. 2
def fig02():
    fig, (a, b) = plt.subplots(2, 1, figsize=(COL1, 2.6), sharex=True,
                               gridspec_kw=dict(height_ratios=[1.3, 1.0], hspace=0.20))
    t0, t1, t2, t3, tend = 0.0, 1.0, 1.9, 2.75, 4.2
    IF, IRR = 1.0, -0.78
    t = np.linspace(-0.9, tend, 1600)
    i = np.piecewise(
        t, [t < t0, (t >= t0) & (t < t2), t >= t2],
        [IF, lambda x: IF + (IRR - IF) * (x - t0) / (t2 - t0),
         lambda x: IRR * np.exp(-(x - t2) / 0.30)])
    a.plot(t, i, color=K)
    a.axhline(0, color=K, lw=0.6)
    msk = t >= t1
    a.fill_between(t[msk], 0, np.minimum(i[msk], 0), color=FILL, lw=0)
    a.text(2.30, -0.30, r"$Q_{rr}$", fontsize=8, ha="center")
    a.annotate("", xy=(t1, 0.34), xytext=(t3, 0.34),
               arrowprops=dict(arrowstyle="<->", lw=0.7, color=K))
    a.text((t1 + t3) / 2, 0.44, r"$t_{rr}$", ha="center", fontsize=8)
    for tt, lab in ((t1, r"$t_1$"), (t2, r"$t_2$"), (t3, r"$t_3$")):
        a.plot([tt, tt], [0, -0.07], color=K, lw=0.6)
        a.text(tt, 0.07, lab, ha="center", fontsize=7.5)
    a.plot([-0.9, t0], [IF, IF], color=K)
    a.text(-0.85, IF + 0.12, r"$I_F$", fontsize=7.5)
    a.plot([t2, tend], [IRR, IRR], ls=":", lw=0.6, color=G1)
    a.text(tend, IRR + 0.10, r"$I_{rr}$", ha="right", va="bottom", fontsize=7.5)
    a.annotate(r"$di/dt$", xy=(0.62, 0.28), xytext=(0.02, 1.02),
               fontsize=7.5, color=G1,
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.set_ylim(-1.20, 1.50); a.set_xlim(-0.9, tend)
    a.set_ylabel(r"$i_D$", rotation=0, labelpad=9, fontsize=8)
    a.set_yticks([]); clean(a, ("top", "right", "bottom"))

    VF, VR = 0.20, -1.0
    vt = np.piecewise(
        t, [t < t2, (t >= t2) & (t < t2 + 0.35), t >= t2 + 0.35],
        [VF, lambda x: VF + (VR - VF) * (x - t2) / 0.35, VR])
    b.plot(t, vt, color=K)
    b.axhline(0, color=K, lw=0.6)
    b.text(-0.85, VF + 0.12, r"$V_F$", fontsize=7.5)
    b.plot([t2 + 0.35, tend], [VR, VR], ls=":", lw=0.6, color=G1)
    b.text(tend, VR + 0.10, r"$-V_R$", ha="right", va="bottom", fontsize=7.5)
    b.set_ylim(-1.45, 0.70); b.set_xlim(-0.9, tend)
    b.set_ylabel(r"$v_D$", rotation=0, labelpad=9, fontsize=8)
    b.set_yticks([]); b.set_xticks([])
    clean(b, ("top", "right", "bottom"))
    b.text(tend, -1.40, r"$t$", fontsize=8, ha="right")
    save(fig, "fig02-recuperacao-reversa")


# ---------------------------------------------------------------- Fig. 3
def fig03():
    fig, axs = plt.subplots(2, 2, figsize=(COL2, 2.75), sharex="col",
                            gridspec_kw=dict(height_ratios=[1, 0.75], hspace=0.20,
                                             wspace=0.20))
    t = np.linspace(0, 1, 600)
    v, i = 1 - t, t
    axs[0, 0].plot(t, v, color=K)
    axs[0, 0].plot(t, i, color=G1, ls="--")
    axs[0, 0].text(0.10, 0.80, r"$v$", fontsize=8.5, color=K)
    axs[0, 0].text(0.88, 0.80, r"$i$", fontsize=8.5, color=G1)
    axs[1, 0].plot(t, v * i, color=K)
    axs[1, 0].fill_between(t, 0, v * i, color=FILL, lw=0)
    axs[1, 0].text(0.5, 0.075, r"$E=\dfrac{1}{6}\,V I\,t_r$", ha="center",
                   fontsize=8)
    axs[0, 0].set_title("(a) carga resistiva", fontsize=8)

    v2 = np.where(t < 0.5, 1.0, 1 - (t - 0.5) / 0.5)
    i2 = np.where(t < 0.5, t / 0.5, 1.0)
    axs[0, 1].plot(t, v2, color=K)
    axs[0, 1].plot(t, i2, color=G1, ls="--")
    axs[0, 1].text(0.16, 0.86, r"$v$", fontsize=8.5, color=K)
    axs[0, 1].text(0.30, 0.42, r"$i$", fontsize=8.5, color=G1)
    axs[1, 1].plot(t, v2 * i2, color=K)
    axs[1, 1].fill_between(t, 0, v2 * i2, color=FILL, lw=0)
    axs[1, 1].text(0.5, 0.075, r"$E=\dfrac{1}{2}\,V I\,t_r$", ha="center",
                   fontsize=8)
    axs[0, 1].set_title("(b) carga indutiva grampeada", fontsize=8)

    for r in range(2):
        for c in range(2):
            ax = axs[r, c]
            ax.set_xlim(-0.02, 1.02); ax.set_xticks([]); ax.set_yticks([])
            clean(ax, ("top", "right"))
    for c in range(2):
        axs[0, c].set_ylim(-0.05, 1.15)
        axs[1, c].set_ylim(-0.02, 0.72)
        axs[1, c].set_xlabel(r"intervalo de transição $t_r$", fontsize=7.5)
    axs[0, 0].set_ylabel(r"$v,\ i$", fontsize=8)
    axs[1, 0].set_ylabel(r"$p = v\,i$", fontsize=8)
    save(fig, "fig03-modelos-comutacao")


# ---------------------------------------------------------------- Fig. 4
def fig04():
    fig, (a, b) = plt.subplots(1, 2, figsize=(COL2, 2.25),
                               gridspec_kw=dict(width_ratios=[1.20, 1.0]))

    # ---- (a) caracteristica do SCR, curva em S
    def scr_curve(ax, VBO, color, lw=1.15, ls="-"):
        VH, iBO, i0, imax = 0.17, 0.055, 0.42, 3.3
        vb = np.linspace(0.0, VBO, 200)
        ib = iBO * (vb / VBO) ** 9
        ax.plot(vb, ib, color=color, lw=lw, ls=ls)
        ii = np.linspace(iBO, imax, 400)
        vv = VH + (VBO - VH) * np.exp(-(ii - iBO) / i0)
        ax.plot(vv, ii, color=color, lw=lw, ls=ls)

    for VBO, col in ((1.10, K), (0.70, G1), (0.38, G2)):
        scr_curve(a, VBO, col)
    a.plot(np.linspace(-1.15, 0, 100), -0.03 * np.ones(100), color=K, lw=1.15)
    a.plot([-1.15, -1.15], [-0.03, -2.3], color=K, lw=1.15)
    a.plot([-1.15, -1.27], [-2.3, -2.45], color=K, lw=1.15)
    a.set_xlim(-1.65, 1.55); a.set_ylim(-2.9, 3.9)
    axes_cross(a, r"$V_{AK}$", r"$i_A$", xlab_off=(-0.02, 0.12))
    a.plot([1.10], [0.055], "o", ms=2.6, color=K)
    a.text(1.14, 0.16, r"$V_{BO}$", fontsize=7.5, ha="left")
    a.text(-1.62, -2.62, r"$-V_{RRM}$", fontsize=7.5, ha="left")
    a.annotate(r"$I_G$ crescente", xy=(0.30, 0.90), xytext=(-1.60, 2.30),
               fontsize=7.2, color=G1, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1,
                               connectionstyle="arc3,rad=0.15"))
    a.annotate("estado\nconduzindo", xy=(0.22, 2.55), xytext=(0.62, 2.95),
               fontsize=7.2, color=G1, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.annotate("bloqueio\ndireto", xy=(0.72, 0.02), xytext=(0.30, -1.55),
               fontsize=7.2, color=G1, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=G1))
    a.set_title("(a)", y=-0.14, fontsize=8)

    # ---- (b) modelo de dois transistores
    b.set_xlim(1.2, 8.9); b.set_ylim(0.6, 10.4); b.axis("off")
    LW = 1.0

    def bar(ax, x, y, h=0.85):
        ax.plot([x, x], [y - h, y + h], color=K, lw=1.4)

    def lead(ax, p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=K, lw=LW)

    def arrow(ax, p, q):
        ax.annotate("", xy=q, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color=K,
                                    mutation_scale=7))

    # Q1: PNP, barra em x=3.6, corpo a esquerda, base para a direita
    x1, y1 = 3.60, 6.90
    bar(b, x1, y1)
    lead(b, (x1, y1 + 0.34), (2.70, y1 + 1.30))   # emissor (sobe p/ anodo)
    lead(b, (x1, y1 - 0.34), (2.70, y1 - 1.30))   # coletor
    arrow(b, (2.98, y1 + 1.00), (3.32, y1 + 0.64))  # PNP: seta para a base
    b.text(x1 + 0.22, y1 + 1.05, r"$Q_1$", fontsize=8.5, ha="left")

    # Q2: NPN, barra em x=6.60, corpo a direita, base para a esquerda
    x2, y2 = 6.60, 3.90
    bar(b, x2, y2)
    lead(b, (x2, y2 + 0.34), (7.50, y2 + 1.30))   # coletor
    lead(b, (x2, y2 - 0.34), (7.50, y2 - 1.30))   # emissor (desce p/ catodo)
    arrow(b, (7.10, y2 - 0.90), (7.42, y2 - 1.22))  # NPN: seta saindo da base
    b.text(x2 - 0.22, y2 - 1.05, r"$Q_2$", fontsize=8.5, ha="right")

    # anodo
    lead(b, (2.70, y1 + 1.30), (2.70, 9.30))
    lead(b, (2.70, 9.30), (5.10, 9.30))
    b.plot([5.10], [9.30], "o", ms=3.4, color=K)
    b.text(5.10, 9.62, "A", ha="center", fontsize=9)

    # coletor de Q1 -> base de Q2
    lead(b, (2.70, y1 - 1.30), (2.70, y2))
    lead(b, (2.70, y2), (x2, y2))

    # coletor de Q2 -> base de Q1
    lead(b, (7.50, y2 + 1.30), (7.50, y1))
    lead(b, (7.50, y1), (x1, y1))

    # catodo
    lead(b, (7.50, y2 - 1.30), (7.50, 1.30))
    lead(b, (7.50, 1.30), (5.10, 1.30))
    b.plot([5.10], [1.30], "o", ms=3.4, color=K)
    b.text(5.10, 0.98, "K", ha="center", va="top", fontsize=9)

    # porta, derivada do no da base de Q2
    b.plot([4.70], [y2], "o", ms=2.8, color=K)
    lead(b, (4.70, y2), (4.70, 2.50))
    lead(b, (4.70, 2.50), (3.10, 2.50))
    b.plot([3.10], [2.50], "o", ms=3.4, color=K)
    b.text(2.85, 2.50, "G", ha="right", va="center", fontsize=9)
    b.set_title("(b)", y=-0.14, fontsize=8)
    fig.subplots_adjust(wspace=0.06)
    save(fig, "fig04-scr-caracteristica")


# ---------------------------------------------------------------- Fig. 5
def fig05():
    V, R, V0, Rs = 220.0, 10.0, 1.063, 0.0074
    al = np.linspace(0, math.pi * 0.94, 400)
    Irms = (V / R) * np.sqrt((1 / math.pi) * ((math.pi - al) + np.sin(2 * al) / 2))
    Iav = (math.sqrt(2) * V / (math.pi * R)) * (1 + np.cos(al))
    P = V0 * Iav + Rs * Irms ** 2
    Pl = R * Irms ** 2
    ad = np.degrees(al)

    fig, ax = plt.subplots(figsize=(COL1, 2.05))
    ax2 = ax.twinx()
    l1, = ax.plot(ad, P, color=K, label=r"$P_{cond}$ no TRIAC")
    l2, = ax2.plot(ad, Pl / 1000, color=G1, ls="--", label=r"$P_{carga}$")
    ax.set_xlabel(r"ângulo de disparo $\alpha$  (graus)")
    ax.set_ylabel(r"$P_{cond}$  (W)")
    ax2.set_ylabel(r"$P_{carga}$  (kW)")
    ax.set_xlim(0, 170); ax.set_ylim(0, 30); ax2.set_ylim(0, 6.0)
    ax.grid(True, ls=":", color=G2)
    ax.plot([0], [24.64], "o", ms=3.2, color=K)
    ax.annotate("caso dimensionante\n24,64 W", xy=(0, 24.64), xytext=(26, 24.0),
                fontsize=6.8, color=K, va="center",
                arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    ax.plot([90], [12.32], "o", ms=3.2, color=K)
    ax.annotate("exemplo do texto\n12,32 W", xy=(90, 12.32), xytext=(98, 16.5),
                fontsize=6.8, color=K,
                arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    ax.legend(handles=[l1, l2], frameon=False, loc="lower left",
              bbox_to_anchor=(0.01, 0.01), handlelength=1.8)
    clean(ax, ("top",)); clean(ax2, ("top",))
    save(fig, "fig05-triac-alpha")


# ---------------------------------------------------------------- Fig. 6
def fig06():
    fig, axs = plt.subplots(4, 1, figsize=(COL1, 3.55), sharex=True,
                            gridspec_kw=dict(hspace=0.16))
    ts = [0, 0.9, 1.7, 3.1, 3.9, 6.3, 7.1, 8.5, 9.4]
    xmax = 10.6
    t = np.linspace(0, xmax, 2400)
    VTH, VMIL, VFULL = 0.30, 0.55, 1.0

    def seg(t, pts):
        return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])

    vgs = seg(t, [(0, 0), (ts[1], VTH), (ts[2], VMIL), (ts[3], VMIL),
                  (ts[4], VFULL), (ts[5], VFULL), (ts[6], VMIL), (ts[7], VMIL),
                  (ts[8], 0.0), (xmax, 0.0)])
    idd = seg(t, [(0, 0), (ts[1], 0), (ts[2], 1.0), (ts[7], 1.0),
                  (ts[8], 0.0), (xmax, 0)])
    vds = seg(t, [(0, 1.0), (ts[2], 1.0), (ts[3], 0.06), (ts[6], 0.06),
                  (ts[7], 1.0), (xmax, 1.0)])
    ig = np.where((t < ts[4]) & (t > 0), 1.0,
                  np.where((t > ts[5]) & (t < ts[8]), -1.0, 0.0))

    for ax, y, lab in ((axs[0], vgs, r"$v_{GS}$"), (axs[1], idd, r"$i_D$"),
                       (axs[2], vds, r"$v_{DS}$"), (axs[3], ig, r"$i_G$")):
        ax.plot(t, y, color=K)
        ax.set_ylabel(lab, rotation=0, labelpad=12, fontsize=8, va="center")
        ax.set_xlim(0, xmax); ax.set_yticks([]); ax.set_xticks([])
        clean(ax, ("top", "right"))
        for tt in ts[1:]:
            ax.axvline(tt, color=G2, lw=0.35, ls=":")
    axs[3].axhline(0, color=K, lw=0.6)
    axs[3].set_ylim(-1.6, 1.6)
    axs[0].set_ylim(-0.05, 1.55)
    axs[0].axhline(VMIL, color=G2, lw=0.5, ls="--")
    axs[0].axhline(VTH, color=G2, lw=0.5, ls=":")
    axs[0].text(xmax * 0.99, VMIL + 0.05, "patamar de Miller", fontsize=6.5,
                color=G1, ha="right")
    axs[0].text(xmax * 0.99, VTH - 0.20, r"$V_{GS(th)}$", fontsize=6.8,
                color=G1, ha="right")
    axs[1].set_ylim(-0.08, 1.42)
    axs[2].set_ylim(-0.08, 1.30)
    for i, tt in enumerate(ts):
        axs[3].text(tt, -2.05, r"$t_%d$" % i, ha="center", fontsize=6.8)
    axs[1].annotate("", xy=(ts[1], 1.22), xytext=(ts[2], 1.22),
                    arrowprops=dict(arrowstyle="<->", lw=0.6, color=K))
    axs[1].text((ts[1] + ts[2]) / 2, 1.27, r"$t_r$", ha="center", fontsize=7)
    axs[1].annotate("", xy=(ts[7], 1.22), xytext=(ts[8], 1.22),
                    arrowprops=dict(arrowstyle="<->", lw=0.6, color=K))
    axs[1].text((ts[7] + ts[8]) / 2, 1.27, r"$t_f$", ha="center", fontsize=7)
    axs[3].text(xmax, -2.05, r"$t$", fontsize=8, ha="right")
    save(fig, "fig06-mosfet-comutacao")


# ---------------------------------------------------------------- Fig. 7
def fig07():
    f = np.logspace(3.7, 5.5, 300)
    d_c, d_s = 2.849, 0.5 * 750e-9 * 400 * f
    m_c, m_s = 12.528, 0.5 * 8 * 200 * 1.2 * 94e-9 * f
    i_c, i_s = 17.20, 1.06e-3 * f

    fig, ax = plt.subplots(figsize=(COL1, 2.2))
    ax.plot(f / 1e3, d_c + d_s, color=K, label="Diodo FRED")
    ax.plot(f / 1e3, m_c + m_s, color=G1, ls="--", label="MOSFET")
    ax.plot(f / 1e3, i_c + i_s, color=K, ls=":", lw=1.5, label="IGBT")
    for val, col in ((d_c, K), (m_c, G1), (i_c, K)):
        ax.axhline(val, color=col, lw=0.45, alpha=0.4)
    ax.plot([50], [10.29], "o", ms=3.2, color=K)
    ax.plot([50], [17.04], "s", ms=3.0, color=G1)
    ax.plot([10], [27.80], "^", ms=3.4, color=K)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"frequência de comutação  $f_s$  (kHz)")
    ax.set_ylabel("perda total no dispositivo  (W)")
    ax.set_xlim(5, 320); ax.set_ylim(2, 400)
    ax.grid(True, which="both", ls=":", color=G2, alpha=0.5)
    ax.legend(frameon=False, loc="upper left", handlelength=2.0)
    ax.text(5.6, 2.35, "patamares de condução", fontsize=6.4, color=G1)
    clean(ax)
    save(fig, "fig07-perda-vs-frequencia")


# ---------------------------------------------------------------- Fig. 8
def fig08():
    fig, ax = plt.subplots(figsize=(COL2, 2.0))
    ax.set_xlim(0, 22); ax.set_ylim(0, 7.6); ax.axis("off")

    def res(x, y, w=2.0, h=0.62, label="", sub=""):
        ax.add_patch(Rectangle((x, y - h / 2), w, h, fill=False, lw=0.9,
                               edgecolor=K))
        ax.text(x + w / 2, y + h / 2 + 0.22, label, ha="center", fontsize=7.5)
        if sub:
            ax.text(x + w / 2, y - h / 2 - 0.55, sub, ha="center", fontsize=6.8,
                    color=G1)

    def node(x, y, lab, dy=0.42, ha="center"):
        ax.plot([x], [y], "o", ms=3.2, color=K)
        ax.text(x, y + dy, lab, ha=ha, fontsize=7.5)

    def src(x, y, lab):
        ax.add_patch(Circle((x, y), 0.42, fill=False, lw=0.9, edgecolor=K))
        ax.annotate("", xy=(x, y + 0.30), xytext=(x, y - 0.30),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color=K,
                                    mutation_scale=8))
        ax.text(x - 0.62, y, lab, ha="right", va="center", fontsize=7.5)

    y1, y2 = 5.6, 2.4
    for y, s in ((y1, "1"), (y2, "2")):
        src(1.2, y, r"$P_%s$" % s)
        ax.plot([1.62, 2.6], [y, y], color=K, lw=0.9)
        node(2.6, y, r"$T_{j%s}$" % s)
        ax.plot([2.6, 3.4], [y, y], color=K, lw=0.9)
        res(3.4, y, label=r"$R_{th,jc%s}$" % s)
        ax.plot([5.4, 6.2], [y, y], color=K, lw=0.9)
        node(6.2, y, r"$T_{c%s}$" % s)
        ax.plot([6.2, 7.0], [y, y], color=K, lw=0.9)
        res(7.0, y, label=r"$R_{th,cd%s}$" % s)
        ax.plot([9.0, 12.2], [y, y], color=K, lw=0.9)
    ax.plot([12.2, 12.2], [y2, y1], color=K, lw=0.9)
    ym = (y1 + y2) / 2
    ax.plot([12.2], [ym], "o", ms=3.2, color=K)
    ax.text(11.95, ym, r"$T_d$", ha="right", va="center", fontsize=7.5)
    ax.plot([12.2, 13.6], [ym, ym], color=K, lw=0.9)
    res(13.6, ym, w=2.4, label=r"$R_{th,da}$", sub="incógnita do projeto")
    ax.plot([16.0, 17.6], [ym, ym], color=K, lw=0.9)
    node(17.6, ym, r"$T_a$")
    ax.plot([17.6, 17.6], [ym, 1.15], color=K, lw=0.9)
    ax.plot([16.9, 18.3], [1.15, 1.15], color=K, lw=1.1)
    ax.plot([17.15, 18.05], [0.90, 0.90], color=K, lw=1.1)
    ax.plot([17.4, 17.8], [0.65, 0.65], color=K, lw=1.1)
    ax.text(18.55, 0.98, "ambiente", fontsize=7, color=G1, va="center")
    ax.text(0.2, 7.05, "dissipação", fontsize=7, color=G1)
    ax.text(11.2, 7.05, "dissipador comum", fontsize=7, color=G1)
    save(fig, "fig08-circuito-termico")


# ---------------------------------------------------------------- Fig. 9
def fig09():
    Rds, Vb, D = 0.285, 400.0, 0.5
    tr, tf = 5e-9, 4.5e-9
    Vsat, esw = 1.72, 1.06e-3 / 20
    fig, (a, b) = plt.subplots(1, 2, figsize=(COL2, 2.2))

    I = np.linspace(0.5, 30, 400)
    f = 20e3
    Pm = Rds * D * I ** 2 + 0.6 * Vb * (tr + tf) * f * I
    Pi = Vsat * D * I + esw * I * f
    a.plot(I, Pm, color=K, label="MOSFET (SPW20N60C3)")
    a.plot(I, Pi, color=G1, ls="--", label="IGBT (IRG4PC40UD)")
    Icr = (Vsat * D + esw * f - 0.6 * Vb * (tr + tf) * f) / (Rds * D)
    Pcr = Rds * D * Icr ** 2 + 0.6 * Vb * (tr + tf) * f * Icr
    a.plot([Icr], [Pcr], "o", ms=3.6, color=K)
    a.axvline(Icr, color=G2, lw=0.6, ls=":")
    a.annotate(r"$I_{cruz}=13{,}2$ A", xy=(Icr, Pcr), xytext=(16.0, 13.5),
               fontsize=7, ha="left",
               arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    a.set_xlabel(r"corrente comutada  $I$  (A)")
    a.set_ylabel("perda total  (W)")
    a.set_xlim(0, 30); a.set_ylim(0, 95)
    a.grid(True, ls=":", color=G2)
    a.legend(frameon=False, loc="upper left", handlelength=1.9,
             bbox_to_anchor=(-0.01, 0.86))
    a.text(1.6, 3.5, "MOSFET vence", fontsize=6.6, color=G1)
    a.text(19.0, 3.5, "IGBT vence", fontsize=6.6, color=G1)
    a.set_title(r"(a)  $V=400$ V,  $f_s=20$ kHz", fontsize=8)
    clean(a)

    fs = np.logspace(3.2, 5.05, 300)
    Icross = (Vsat * D + esw * fs - 0.6 * Vb * (tr + tf) * fs) / (Rds * D)
    b.plot(fs / 1e3, Icross, color=K)
    b.fill_between(fs / 1e3, 0, Icross, color=FILL, alpha=0.55, lw=0)
    for fp, ip in ((2, 6.75), (10, 9.59), (20, 13.15), (50, 23.83), (100, 41.63)):
        b.plot([fp], [ip], "o", ms=3.0, color=K)
    b.set_xscale("log")
    b.set_xlabel(r"frequência de comutação  $f_s$  (kHz)")
    b.set_ylabel(r"corrente de cruzamento  $I_{cruz}$  (A)")
    b.set_xlim(1.6, 110); b.set_ylim(0, 46)
    b.grid(True, which="both", ls=":", color=G2, alpha=0.5)
    b.text(2.2, 3.0, "domínio do MOSFET", fontsize=6.6, color=G1)
    b.text(2.2, 37.5, "domínio do IGBT", fontsize=6.6, color=G1)
    b.set_title(r"(b)  $V=400$ V,  $d=0{,}5$", fontsize=8)
    clean(b)
    fig.subplots_adjust(wspace=0.32)
    save(fig, "fig09-fronteira-mosfet-igbt")


# ---------------------------------------------------------------- Fig. 10
def fig10():
    def up(H, sh):
        return np.tanh((H - sh) / 0.40)

    fig, (a, b) = plt.subplots(1, 2, figsize=(COL2, 2.25), sharey=True)

    # (a) Forward: laco unipolar no primeiro quadrante
    Hu = np.linspace(0.05, 1.45, 300)
    up_b = 0.30 + 0.70 * np.tanh((Hu - 0.75) / 0.34)
    dn_b = 0.30 + 0.70 * np.tanh((Hu - 0.45) / 0.34)
    a.plot(Hu, up_b, color=K); a.plot(Hu, dn_b, color=K)
    a.plot([Hu[0], Hu[0]], [up_b[0], dn_b[0]], color=K)
    a.plot([Hu[-1], Hu[-1]], [up_b[-1], dn_b[-1]], color=K)
    a.fill_between(Hu, up_b, dn_b, color=FILL, alpha=0.7, lw=0)
    Bmin, Bmax = dn_b[0], up_b[-1]
    a.set_xlim(-0.75, 1.85); a.set_ylim(-1.25, 1.25)
    axes_cross(a, r"$H$", r"$B$", xlab_off=(-0.02, 0.06))
    a.annotate("", xy=(-0.30, Bmax), xytext=(-0.30, Bmin),
               arrowprops=dict(arrowstyle="<->", lw=0.8, color=K))
    a.plot([-0.30, Hu[-1]], [Bmax, Bmax], ls=":", lw=0.5, color=G1)
    a.plot([-0.30, Hu[0]], [Bmin, Bmin], ls=":", lw=0.5, color=G1)
    a.text(-0.38, (Bmin + Bmax) / 2, r"$\Delta B$", ha="right", va="center",
           fontsize=8)
    a.text(0.95, -0.55, "apenas o 1.º\nquadrante", fontsize=6.8, color=G1,
           ha="center")
    a.set_title("(a) Forward: assimétrico", fontsize=7.8)

    # (b) simetrico
    H = np.linspace(-1.55, 1.55, 400)
    ub = np.tanh((H - 0.26) / 0.42)
    db = np.tanh((H + 0.26) / 0.42)
    b.plot(H, ub, color=K); b.plot(H, db, color=K)
    b.fill_between(H, ub, db, color=FILL, alpha=0.7, lw=0)
    b.set_xlim(-2.05, 2.05); b.set_ylim(-1.25, 1.25)
    axes_cross(b, r"$H$", r"$B$", xlab_off=(-0.02, 0.06))
    Bp = np.tanh((1.55 - 0.26) / 0.42)
    b.annotate("", xy=(-1.30, Bp), xytext=(-1.30, -Bp),
               arrowprops=dict(arrowstyle="<->", lw=0.8, color=K))
    b.plot([-1.30, 1.55], [Bp, Bp], ls=":", lw=0.5, color=G1)
    b.plot([-1.30, -1.55], [-Bp, -Bp], ls=":", lw=0.5, color=G1)
    b.text(-1.40, 0, r"$\Delta B$", ha="right", va="center", fontsize=8)
    b.text(1.62, Bp, r"$+B_{ac}$", fontsize=7, va="center")
    b.text(-1.62, -Bp, r"$-B_{ac}$", fontsize=7, va="center", ha="right")
    b.set_title("(b) Ponte completa: simétrico", fontsize=7.8)
    fig.subplots_adjust(wspace=0.14)
    save(fig, "fig10-laco-bh")


# ---------------------------------------------------------------- Fig. 11
def fig11():
    f = np.logspace(1.6, 6.3, 400)
    eps = 6.62 / np.sqrt(f) * 10
    awg = {20: 0.812, 24: 0.511, 26: 0.405, 30: 0.255}

    fig, ax = plt.subplots(figsize=(COL1, 2.15))
    ax.plot(f / 1e3, 2 * eps, color=K, label=r"$D_{max}=2\varepsilon$")
    for g, d in awg.items():
        ax.axhline(d, color=G2, lw=0.45, ls=":")
        ax.text(1.15e-2, d * 1.06, f"{g} AWG", fontsize=6.3, color=G1)
    ax.axvline(100, color=K, lw=0.6, ls="--")
    ax.plot([100], [0.4187], "o", ms=3.4, color=K)
    ax.annotate("100 kHz:  0,419 mm\n(26 AWG)", xy=(100, 0.4187),
                xytext=(2.2, 0.115), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"frequência  (kHz)")
    ax.set_ylabel(r"diâmetro do fio  (mm)")
    ax.set_xlim(1e-2, 1e3); ax.set_ylim(0.06, 22)
    ax.grid(True, which="major", ls=":", color=G2, alpha=0.4)
    ax.legend(frameon=False, loc="upper right")
    clean(ax)
    save(fig, "fig11-efeito-pelicular")


# ---------------------------------------------------------------- Fig. 12
def fig12():
    fig = plt.figure(figsize=(COL2, 2.85))
    gs = fig.add_gridspec(4, 2, width_ratios=[1.85, 1.0], hspace=0.18, wspace=0.12)
    ax = fig.add_subplot(gs[:, 0])
    ax.set_xlim(0.3, 21.4); ax.set_ylim(0.4, 14.4); ax.axis("off")
    LW = 0.95
    TOP, BOT, MID = 13.6, 1.2, 7.5
    XL, XR = 4.4, 10.4
    SWT, SWB = 11.0, 3.2          # centros das chaves
    HB = 0.95                     # meia altura da caixa
    RTOP, RBOT = 12.4, 2.6        # trilhos CC do retificador
    XA, XB = 13.4, 16.2           # colunas da ponte
    YA, YB = 8.60, 6.60           # nos CA da ponte

    def wire(pts):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=K, lw=LW,
                solid_capstyle="round")

    def dot(x, y):
        ax.plot([x], [y], "o", ms=2.6, color=K)

    def hop(x, y, r=0.30):
        """Salto sobre fio horizontal, indicando ausencia de conexao."""
        th = np.linspace(0, np.pi, 40)
        ax.plot(x + r * np.cos(th), y + r * np.sin(th), color=K, lw=LW)

    def sw(x, y, lab):
        ax.add_patch(Rectangle((x - 0.58, y - HB), 1.16, 2 * HB, fill=False,
                               lw=LW, edgecolor=K))
        wire([(x - 1.30, y), (x - 0.58, y)])
        ax.text(x + 0.88, y, lab, fontsize=7.5, va="center", ha="left")

    # ---- fonte CC
    for yy, w in ((MID + 0.90, 0.90), (MID + 0.45, 0.45),
                  (MID - 0.45, 0.90), (MID - 0.90, 0.45)):
        ax.plot([1.5 - w, 1.5 + w], [yy, yy], color=K, lw=1.3)
    ax.text(0.45, MID, r"$V_{in}$", ha="left", va="center", fontsize=8)
    wire([(1.5, MID + 0.90), (1.5, TOP), (XR, TOP)])
    wire([(1.5, MID - 0.90), (1.5, BOT), (XR, BOT)])

    # ---- bracos
    for x, lt, lb in ((XL, r"$S_1$", r"$S_4$"), (XR, r"$S_3$", r"$S_2$")):
        sw(x, SWT, lt); sw(x, SWB, lb)
        wire([(x, TOP), (x, SWT + HB)])
        wire([(x, SWT - HB), (x, SWB + HB)])
        wire([(x, SWB - HB), (x, BOT)])
        dot(x, TOP); dot(x, BOT)

    # ---- transformador
    XP, XS = 6.60, 8.40
    for yy in (MID - 1.13, MID - 0.38, MID + 0.38, MID + 1.13):
        ax.add_patch(Circle((XP, yy), 0.38, fill=False, lw=0.85, edgecolor=K))
        ax.add_patch(Circle((XS, yy), 0.38, fill=False, lw=0.85, edgecolor=K))
    ax.plot([7.38, 7.38], [MID - 1.85, MID + 1.85], color=K, lw=1.0)
    ax.plot([7.62, 7.62], [MID - 1.85, MID + 1.85], color=K, lw=1.0)
    ax.text(7.50, MID + 2.30, r"$60{:}10$", ha="center", fontsize=7.2)

    # primario: terminal superior -> braco esquerdo
    wire([(XP, MID + 1.51), (XP, 9.95), (XL, 9.95)])
    dot(XL, 9.95)
    # primario: terminal inferior -> braco direito, por baixo do secundario
    wire([(XP, MID - 1.51), (XP, 4.35), (XR, 4.35)])
    dot(XR, 4.35)

    # secundario: terminal superior -> coluna A (salta o braco direito)
    wire([(XS, MID + 1.51), (XS, YA), (XR - 0.28, YA)])
    hop(XR, YA)
    wire([(XR + 0.28, YA), (XA, YA)])
    dot(XA, YA)
    # secundario: terminal inferior -> coluna B (salta o braco e a coluna A)
    wire([(XS, MID - 1.51), (XS, YB), (XR - 0.28, YB)])
    hop(XR, YB)
    wire([(XR + 0.28, YB), (XA - 0.28, YB)])
    hop(XA, YB)
    wire([(XA + 0.28, YB), (XB, YB)])
    dot(XB, YB)

    # ---- ponte de diodos
    def diode(x, y, up=True):
        s = 1 if up else -1
        ax.add_patch(Polygon([[x - 0.46, y - 0.40 * s], [x + 0.46, y - 0.40 * s],
                              [x, y + 0.36 * s]], closed=True, fill=False,
                             lw=0.85, edgecolor=K))
        ax.plot([x - 0.46, x + 0.46], [y + 0.36 * s, y + 0.36 * s], color=K,
                lw=1.1)

    for x, ymid in ((XA, YA), (XB, YB)):
        yu = (ymid + RTOP) / 2
        yl = (RBOT + ymid) / 2
        diode(x, yu, up=True)
        diode(x, yl, up=True)
        wire([(x, ymid), (x, yu - 0.40)])
        wire([(x, yu + 0.36), (x, RTOP)])
        wire([(x, RBOT), (x, yl - 0.40)])
        wire([(x, yl + 0.36), (x, ymid)])
    wire([(XA, RTOP), (20.9, RTOP)])
    wire([(XA, RBOT), (20.9, RBOT)])
    dot(XB, RTOP); dot(XB, RBOT)
    ax.text((XA + XB) / 2, RTOP + 0.45, "ponte de Schottky", ha="center",
            fontsize=6.9, color=G1)

    # ---- filtro e carga
    ax.add_patch(Rectangle((17.9, RBOT), 3.0, RTOP - RBOT, fill=False, lw=LW,
                           edgecolor=K, linestyle=(0, (3.5, 2))))
    ax.text(19.4, MID + 1.05, "filtro", ha="center", fontsize=7.3)
    ax.text(19.4, MID + 0.05, "LC e", ha="center", fontsize=7.3)
    ax.text(19.4, MID - 0.95, "carga", ha="center", fontsize=7.3)
    ax.text(19.4, MID - 2.15, "54 V", ha="center", fontsize=6.9, color=G1)
    ax.text(19.4, MID - 3.00, "9,26 A", ha="center", fontsize=6.9, color=G1)

    # ---- formas de onda
    t = np.linspace(0, 2, 1600)
    D = 0.4103
    vp = np.zeros_like(t)
    for k in range(3):
        vp += np.where((t >= k) & (t < k + D), 1.0, 0.0)
        vp += np.where((t >= k + 0.5) & (t < k + 0.5 + D), -1.0, 0.0)
    dt = t[1] - t[0]
    Bv = np.cumsum(vp) * dt
    Bv -= Bv.mean()
    ip = np.where(np.abs(vp) > 0.5, np.sign(vp), 0.0)
    isec = np.where(np.abs(vp) > 0.5, 1.0, 0.0)

    for r, (y, lab, yl) in enumerate((
            (vp, r"$v_p$", (-1.55, 1.60)),
            (Bv / np.abs(Bv).max(), r"$B$", (-1.55, 1.55)),
            (ip, r"$i_p$", (-1.55, 1.55)),
            (isec, r"$i_s$", (-0.45, 1.55)))):
        axw = fig.add_subplot(gs[r, 1])
        axw.plot(t, y, color=K, lw=1.1)
        axw.axhline(0, color=G2, lw=0.5)
        axw.set_ylabel(lab, rotation=0, labelpad=10, fontsize=8, va="center")
        axw.set_xlim(0, 2); axw.set_ylim(*yl)
        axw.set_xticks([]); axw.set_yticks([])
        clean(axw, ("top", "right", "bottom", "left"))
        for kk in (0.5, 1.0, 1.5):
            axw.axvline(kk, color=G2, lw=0.35, ls=":")
        if r == 0:
            axw.annotate("", xy=(0, 1.32), xytext=(D, 1.32),
                         arrowprops=dict(arrowstyle="<->", lw=0.6, color=K))
            axw.text(D / 2 + 0.02, 1.36, r"$DT$", ha="center", fontsize=6.8)
        if r == 3:
            axw.text(1.0, -0.37, r"$T = 10\ \mu$s", ha="center", fontsize=6.8,
                     color=G1)
    save(fig, "fig12-full-bridge")


# ---------------------------------------------------------------- Fig. 13
def fig13():
    Vin, Vo, Po, fs, eta, Dn, Vd = 400., 54., 500., 1e5, 0.98, 0.40, 0.70
    Ae, Aw, lt, Ve = 2.40, 1.57, 10.5, 23.30
    Scu, Sis = 0.001287, 0.001603
    rho = 1.724e-6 * (1 + 0.00393 * 80)
    KH, KE = 4e-5, 4e-10
    Io = Po / Vo; Pin = Po / eta; T = 1 / fs
    B = np.arange(0.040, 0.1105, 0.005)
    Pcu, Pnu, Ku, Pt = [], [], [], []
    for Bac in B:
        Np = math.ceil(Vin * 1e4 / (4.0 * Bac * fs * Ae))
        nt = (Vo + Vd) / (Vin * 2 * Dn)
        Ns = max(1, round(nt * Np)); nr = Ns / Np
        D = (Vo + Vd) / (Vin * nr * 2)
        dB = Vin * D * T / (Np * Ae * 1e-4)
        Ip = (Pin / Vin) / math.sqrt(2 * D); Is = Io * math.sqrt(2 * D)
        npp = math.ceil((Ip / 400.) / Scu); nss = math.ceil((Is / 400.) / Scu)
        Ku.append((Np * npp + Ns * nss) * Sis / Aw)
        Rp = rho * lt * Np / (npp * Scu); Rs = rho * lt * Ns / (nss * Scu)
        pc = Rp * Ip ** 2 + Rs * Is ** 2
        pn = (dB ** 2.4) * (KH * fs + KE * fs ** 2) * Ve
        Pcu.append(pc); Pnu.append(pn); Pt.append(pc + pn)
    B = B * 1e3
    Pcu, Pnu, Ku, Pt = map(np.array, (Pcu, Pnu, Ku, Pt))

    fig, (a, b) = plt.subplots(2, 1, figsize=(COL1, 3.0), sharex=True,
                               gridspec_kw=dict(height_ratios=[1.6, 1.0],
                                                hspace=0.13))
    a.plot(B, Pcu, color=G1, ls="--", marker="s", ms=2.6, label=r"$P_{cu}$")
    a.plot(B, Pnu, color=G1, ls=":", lw=1.4, marker="^", ms=2.8,
           label=r"$P_{n\acute{u}cleo}$")
    a.plot(B, Pt, color=K, marker="o", ms=3.0, label=r"$P_{\Sigma}$")
    a.axvline(70, color=K, lw=0.7, ls="--")
    a.set_ylabel("perda no transformador  (W)")
    a.set_ylim(0, 4.6)
    a.grid(True, ls=":", color=G2, alpha=0.6)
    a.legend(frameon=False, loc="upper center", ncol=3, handlelength=1.7,
             columnspacing=1.0, bbox_to_anchor=(0.52, 1.20))
    a.annotate("adotado\n2,514 W", xy=(70, 2.514), xytext=(83, 3.15),
               fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6, color=K))
    clean(a)

    b.plot(B, Ku, color=K, marker="o", ms=3.0)
    b.axhline(0.40, color=K, lw=0.8, ls="-.")
    b.fill_between(B, 0.40, Ku, where=Ku > 0.40, color=FILL, alpha=0.75, lw=0)
    b.axvline(70, color=K, lw=0.7, ls="--")
    b.text(43.5, 0.500, "não cabe\nna janela", fontsize=6.8, color=G1,
           ha="left")
    b.text(107, 0.425, r"limite  $K_u=0{,}40$", fontsize=6.8, color=G1,
           ha="right")
    b.plot([70], [0.3574], "o", ms=4.0, color=K, mfc="white", mew=1.0)
    b.set_xlabel(r"densidade de fluxo  $B_{ac}$  (mT)")
    b.set_ylabel(r"ocupação  $K_u$")
    b.set_xlim(38, 113); b.set_ylim(0.15, 0.72)
    b.grid(True, ls=":", color=G2, alpha=0.6)
    clean(b)
    save(fig, "fig13-varredura-bac")


# ---------------------------------------------------------------- Fig. 14
def fig14():
    fig, ax = plt.subplots(figsize=(COL1, 2.1))
    ax.set_xlim(0, 13.2); ax.set_ylim(0, 8.6); ax.axis("off")
    CORE = "#e0e0e0"

    # nucleo E-E em corte
    ax.add_patch(Rectangle((0.5, 1.0), 1.15, 5.6, facecolor=CORE, edgecolor=K,
                           lw=0.9))
    ax.add_patch(Rectangle((7.55, 1.0), 1.15, 5.6, facecolor=CORE, edgecolor=K,
                           lw=0.9))
    ax.add_patch(Rectangle((1.65, 5.75), 5.90, 0.85, facecolor=CORE,
                           edgecolor=K, lw=0.9))
    ax.add_patch(Rectangle((1.65, 1.0), 5.90, 0.85, facecolor=CORE,
                           edgecolor=K, lw=0.9))
    ax.add_patch(Rectangle((5.55, 1.85), 2.0, 3.90, facecolor=CORE,
                           edgecolor=K, lw=0.9))
    ax.text(6.55, 3.80, "perna\ncentral", ha="center", va="center",
            fontsize=6.5, color=G1)
    ax.text(1.07, 3.80, "núcleo", ha="center", va="center", fontsize=6.5,
            color=G1, rotation=90)

    # camadas na janela
    x = 1.95
    for lab, w, hatch, fc in (("½ P", 0.72, "", "#ffffff"),
                              ("S", 1.05, "///", "#bdbdbd"),
                              ("½ P", 0.72, "", "#ffffff")):
        ax.add_patch(Rectangle((x, 2.10), w, 3.40, facecolor=fc, edgecolor=K,
                               lw=0.85, hatch=hatch))
        ax.text(x + w / 2, 3.80, lab, ha="center", va="center", fontsize=7.2)
        x += w + 0.22
    ax.annotate("", xy=(1.95, 1.72), xytext=(x - 0.22, 1.72),
                arrowprops=dict(arrowstyle="<->", lw=0.6, color=K))
    ax.text((1.95 + x - 0.22) / 2, 7.05, "sequência intercalada", ha="center",
            fontsize=7.2)
    ax.plot([(1.95 + x - 0.22) / 2, (1.95 + x - 0.22) / 2], [6.80, 5.60],
            color=G2, lw=0.6)

    # legenda a direita, fora do nucleo
    ax.add_patch(Rectangle((9.30, 4.95), 0.55, 0.42, facecolor="#ffffff",
                           edgecolor=K, lw=0.85))
    ax.text(10.05, 5.16, "primário", fontsize=7.2, va="center")
    ax.text(9.30, 4.45, "60 espiras", fontsize=6.6, color=G1)
    ax.text(9.30, 3.95, "3 fios 26 AWG", fontsize=6.6, color=G1)
    ax.add_patch(Rectangle((9.30, 2.90), 0.55, 0.42, facecolor="#bdbdbd",
                           edgecolor=K, lw=0.85, hatch="///"))
    ax.text(10.05, 3.11, "secundário", fontsize=7.2, va="center")
    ax.text(9.30, 2.40, "10 espiras", fontsize=6.6, color=G1)
    ax.text(9.30, 1.90, "17 fios 26 AWG", fontsize=6.6, color=G1)
    ax.text((1.95 + x - 0.22) / 2, 1.32, "30 / 10 / 30 espiras", fontsize=6.6,
            color=G1, ha="center")
    save(fig, "fig14-bobinagem")


# ---------------------------------------------------------------- Fig. 15
def fig15():
    labels = ["Ponte de Schottky\nno secundário",
              "Derivação central\nno secundário"]
    mos = np.array([4.148, 4.148])
    ret = np.array([12.222, 6.111])
    tra = np.array([2.514, 2.514])
    tot = mos + ret + tra
    eta = [96.36, 97.51]

    fig, ax = plt.subplots(figsize=(COL1, 2.05))
    y = np.arange(2); h = 0.38
    ax.barh(y, mos, h, color="#ffffff", edgecolor=K, lw=0.8, label="4 MOSFETs")
    ax.barh(y, ret, h, left=mos, color="#9e9e9e", edgecolor=K, lw=0.8,
            label="retificador de saída")
    ax.barh(y, tra, h, left=mos + ret, color="#4d4d4d", edgecolor=K, lw=0.8,
            label="transformador")
    for i in range(2):
        ax.text(tot[i] + 0.5, y[i],
                f"{tot[i]:.1f} W".replace(".", ",") + "\n" +
                r"$\eta$ = " + f"{eta[i]:.1f} %".replace(".", ","),
                va="center", fontsize=7, linespacing=1.35)
        ax.text(mos[i] / 2, y[i], f"{mos[i]:.1f}".replace(".", ","), va="center",
                ha="center", fontsize=6.5)
        ax.text(mos[i] + ret[i] / 2, y[i], f"{ret[i]:.1f}".replace(".", ","),
                va="center", ha="center", fontsize=6.5)
        ax.text(mos[i] + ret[i] + tra[i] / 2, y[i],
                f"{tra[i]:.1f}".replace(".", ","), va="center", ha="center",
                fontsize=6.5, color="white")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("perda (W)")
    ax.set_xlim(0, 27)
    ax.set_ylim(1.75, -0.85)
    ax.legend(frameon=False, loc="upper center", fontsize=6.9, handlelength=1.3,
              ncol=3, columnspacing=0.9, bbox_to_anchor=(0.46, 1.20))
    ax.grid(True, axis="x", ls=":", color=G2)
    ax.set_axisbelow(True)
    clean(ax)
    save(fig, "fig15-reparticao-perdas")


if __name__ == "__main__":
    print("gerando figuras em", OUT)
    for fn in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08,
               fig09, fig10, fig11, fig12, fig13, fig14, fig15):
        fn()
    print("ok")
