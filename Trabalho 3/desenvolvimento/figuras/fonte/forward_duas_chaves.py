"""Topologia, etapas de operação e formas de onda teóricas do Forward de duas chaves.

A planilha do professor parte direto das especificações; estas figuras cobrem a
parte qualitativa que faltava. Gera, em desenvolvimento/figuras:
    fwd2-topologia.png
    fwd2-etapa-1.png, fwd2-etapa-2.png, fwd2-etapa-3.png
    fwd2-formas-teoricas.png
Uso: python forward_duas_chaves.py

Designadores usados nas figuras e os correspondentes no modelo de simulação
(Fig. 14 do professor): S1 = MOS3, S2 = MOS1, D1 = D4, D2 = D3, D3 = D2,
D4 = D1, Lo = L2, Co = C4.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import esquema
from esquema import Esquema

esquema.ESC = 2.0     # as figuras entram no artigo reduzidas à largura de uma coluna

SAIDA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def circuito(etapa):
    """etapa 0 = topologia (sem destaque); 1 = transferência; 2 = desmagnetização; 3 = roda livre."""
    t1, t2 = etapa == 1, etapa == 2
    pri = t1 or t2                 # há corrente no primário
    rl = etapa in (2, 3)           # diodo de roda livre conduz
    sai = etapa != 0               # filtro de saída sempre com corrente
    e = Esquema(14.6, 7.2)
    # ---- primário: duas chaves e dois diodos de desmagnetização
    e.ramo_v(0, 6, 0, "fonte", on=pri, rotulo="Vi", lado=-0.5)
    e.fio([(0, 6), (2, 6)], pri)
    e.fio([(2, 6), (4, 6)], t2)
    e.fio([(0, 0), (2, 0)], pri)
    e.fio([(2, 0), (4, 0)], t1)
    e.ramo_v(2, 6, 3.6, "mosfet", on=t1, rotulo="S1", lado=0.35)
    e.ramo_v(2, 3.6, 0, "diodo", on=t2, rotulo="D2", lado=-0.4, para="up")
    e.ramo_v(4, 6, 2.4, "diodo", on=t2, rotulo="D1", lado=0.4, para="up")
    e.ramo_v(4, 2.4, 0, "mosfet", on=t1, rotulo="S2", lado=0.35)
    e.fio_salto([(2, 3.6), (5.75, 3.6)], 4, on=pri)
    e.fio([(4, 2.4), (5.75, 2.4)], pri)
    for p in [(2, 6), (2, 0), (2, 3.6), (4, 2.4), (4, 6), (4, 0)]:
        e.no(*p)
    # ---- transformador (a magnetizante é a que circula na etapa 2)
    e.bobina(5.75, 3.6, 2.4, +1, on=pri)
    e.nucleo(6.1, 3.7, 2.3)
    e.bobina(6.45, 3.6, 2.4, -1, on=t1)
    e.ponto(5.55, 3.55)
    e.ponto(6.65, 3.55)
    e.texto(6.1, 4.15, "T1")
    # ---- secundário: retificador, roda livre e filtro
    e.fio([(6.45, 3.6), (7, 3.6), (7, 5)], t1)
    e.ramo_h(5, 7, 8.4, "diodo", on=t1, rotulo="D3", h=0.7)
    e.ramo_v(8.4, 5, 1, "diodo", on=rl, para="up")
    e.texto(8.8, 3.0, "D4", ha="left")
    e.fio([(6.45, 2.4), (7, 2.4), (7, 1), (8.4, 1)], t1)
    e.ramo_h(5, 8.4, 11.0, "ind", on=sai, rotulo="Lo", h=1.2)
    e.ramo_v(11.0, 5, 1, "cap", on=sai)
    e.texto(10.6, 3.0, "Co", ha="right")
    e.fio([(11.0, 5), (12.4, 5)], sai)
    e.ramo_v(12.4, 5, 1, "res", on=sai, rotulo="Ro", lado=0.35)
    e.fio([(8.4, 1), (12.4, 1)], sai)
    for p in [(8.4, 5), (8.4, 1), (11.0, 5), (11.0, 1)]:
        e.no(*p)
    e.texto(14.2, 4.6, "+")
    e.texto(14.2, 3.0, "Vo")
    e.texto(14.2, 1.4, "−")
    # ---- sentido das correntes: várias setas ao longo de cada caminho
    if t1:                                           # fonte -> S1 -> primário -> S2 -> fonte
        e.seta(1.0, 6, "right", "iVi", dy_rot=0.5)
        e.seta(2, 5.6, "down")
        e.seta(3.0, 3.6, "right", "ipri", dy_rot=0.5)
        e.seta(4.9, 2.4, "left")
        e.seta(4, 0.4, "down")
        e.seta(1.0, 0, "left")
        e.seta(7.0, 4.3, "up", "isec", dx_rot=0.75)   # secundário -> D3 -> Lo
        e.seta(7.7, 1, "left")
    if t2:                                           # D2 -> primário -> D1 -> fonte (devolve energia)
        e.seta(1.0, 0, "right")
        e.seta(2, 0.7, "up")
        e.seta(2, 2.9, "up")
        e.seta(3.0, 3.6, "right", "iLm", dy_rot=0.5)
        e.seta(4.9, 2.4, "left")
        e.seta(4, 3.0, "up")
        e.seta(4, 5.3, "up")
        e.seta(1.0, 6, "left", "iLm", dy_rot=0.5)
    if rl:                                           # roda livre: D4 -> Lo -> carga -> D4
        e.seta(8.4, 2.0, "up")
        e.seta(8.4, 4.2, "up")
    if sai:
        e.seta(8.78, 5, "right", "iLo", dy_rot=0.5)
        e.seta(11.7, 5, "right")
        e.seta(12.4, 4.2, "down")
        e.seta(9.7, 1, "left")
    titulos = {0: None,
               1: "a) Primeira etapa: transferência de energia",
               2: "b) Segunda etapa: desmagnetização",
               3: "c) Terceira etapa: roda livre"}
    nome = "fwd2-topologia.png" if etapa == 0 else "fwd2-etapa-%d.png" % etapa
    e.salvar(os.path.join(SAIDA, nome), titulos[etapa])


def formas_teoricas():
    """Formas de onda idealizadas, em valores normalizados, para D = 0,4."""
    D, Ts, n_per = 0.4, 1.0, 2
    t = np.linspace(0, n_per * Ts, 4000)
    fase = (t % Ts) / Ts
    on = fase < D
    dm = (fase >= D) & (fase < 2 * D)        # desmagnetização dura DTs (tensão de reset = Vi)
    vg = on.astype(float)
    vpri = np.where(on, 1.0, np.where(dm, -1.0, 0.0))
    ilm = np.where(on, fase / D, np.where(dm, (2 * D - fase) / D, 0.0))
    dI = 0.25                                 # ondulação relativa de iLo
    ilo = np.where(on, 1 - dI / 2 + dI * fase / D, 1 + dI / 2 - dI * (fase - D) / (1 - D))
    k_m = 0.12                                # magnetizante relativa à corrente refletida
    i_s = np.where(on, ilo + k_m * ilm, 0.0)
    vs = np.where(on, 0.0, np.where(dm, 1.0, 0.5))
    vd4 = np.where(on, 1.0, 0.0)

    fig, ax = plt.subplots(6, 1, figsize=(3.6, 4.6), sharex=True)
    cor = "#d62728"

    def traco(a, y, rot, ylim, ticks, labels):
        a.plot(t, y, color=cor, lw=1.2)
        a.set_ylabel(rot, rotation=0, ha="right", va="center", fontsize=9)
        a.set_ylim(*ylim)
        a.set_yticks(ticks)
        a.set_yticklabels(labels, fontsize=7.5)
        a.grid(True, color="0.88", lw=0.5)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)

    traco(ax[0], vg, r"$v_{g1}, v_{g2}$", (-0.15, 1.3), [0, 1], ["0", "1"])
    traco(ax[1], vpri, r"$v_{pri}$", (-1.3, 1.3), [-1, 0, 1], [r"$-V_i$", "0", r"$V_i$"])
    ax[1].text(0.2, 0.45, "A+", ha="center", fontsize=8, style="italic")
    ax[1].text(0.6, -0.6, "A−", ha="center", fontsize=8, style="italic")
    traco(ax[2], ilm, r"$i_{Lm}$", (-0.15, 1.3), [0, 1], ["0", r"$I_{Lm,pk}$"])
    ax[2].text(0.66, 0.75, r"$i_{D1} = i_{D2}$", fontsize=7.5)
    traco(ax[3], i_s, r"$i_{S1} = i_{S2}$", (-0.15, 1.5), [0, 1], ["0", r"$nI_o$"])
    traco(ax[4], vs, r"$v_{S1} = v_{S2}$", (-0.15, 1.3), [0, 0.5, 1], ["0", r"$V_i/2$", r"$V_i$"])
    traco(ax[5], ilo, r"$i_{Lo}$", (0, 1.4), [0, 1], ["0", r"$I_o$"])
    ax[5].plot(t, vd4 * 0.55, color="#1f3fbf", lw=1.0)
    ax[5].text(0.2, 0.62, r"$v_{D4} = nV_i$", ha="center", color="#1f3fbf", fontsize=7.5)
    ax[5].text(0.2, 1.22, r"$i_{D3}$", ha="center", fontsize=7.5)
    ax[5].text(0.72, 1.22, r"$i_{D4}$", ha="center", fontsize=7.5)
    for a in ax:
        for k in range(n_per):
            for x in (k * Ts + D * Ts, k * Ts + 2 * D * Ts):
                a.axvline(x, color="0.6", lw=0.5, ls=":")
    ax[5].set_xticks([0, D, 2 * D, 1, 1 + D, 1 + 2 * D, 2])
    ax[5].set_xticklabels(["0", r"$DT_s$", r"$2DT_s$", r"$T_s$", "", "", r"$2T_s$"], fontsize=8)
    ax[5].set_xlim(0, n_per * Ts)
    for xc, rot in ((0.2, "1ª etapa"), (0.6, "2ª"), (0.9, "3ª")):
        ax[0].text(xc, 1.12, rot, ha="center", fontsize=7)
    fig.tight_layout(pad=0.4)
    fig.subplots_adjust(left=0.27)
    fig.savefig(os.path.join(SAIDA, "fwd2-formas-teoricas.png"), dpi=400)
    plt.close(fig)


if __name__ == "__main__":
    for k in (0, 1, 2, 3):
        circuito(k)
    formas_teoricas()
    print("figuras gravadas em", SAIDA)
