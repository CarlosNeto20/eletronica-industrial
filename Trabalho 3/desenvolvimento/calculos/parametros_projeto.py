"""Confere a planilha do professor e estende o projeto do carregador de 15 A.

Uso:  python parametros_projeto.py            (imprime o relatório)
      python parametros_projeto.py --figuras  (também gera os diagramas de Bode
                                               em ../figuras/calc-*.png)

Partes:
  1. bateria e rede;
  2. retificador com filtro capacitivo, para 176 V e 264 V, com o capacitor
     calculado (545,7 uF), o adotado (2 x 470 uF) e o do esquemático (470 uF);
  3. Forward de duas chaves: relação de espiras, razão cíclica, Lo, Co e os
     esforços nos semicondutores (que a planilha não traz);
  4. malhas de tensão e de corrente pelo método do fator K, primeiro como na
     planilha e depois com os componentes comerciais e a portadora usados na
     simulação, nas duas tensões de rede.
Os valores marcados com "planilha" são os do documento do professor.
"""
import os
import sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(AQUI), "figuras")
pi = np.pi


def linha(rotulo, valor, unidade="", planilha=None, casas=4):
    txt = "  %-46s %12.*g %-5s" % (rotulo, casas, valor, unidade)
    if planilha is not None:
        erro = 100 * (valor - planilha) / planilha if planilha else 0.0
        txt += "  planilha: %-10g (%+.2f %%)" % (planilha, erro)
    print(txt)


def titulo(t):
    print("\n" + t + "\n" + "-" * len(t))


# ============================================================ 1. bateria e rede
C_Ah, Vbatmin, Vbatmax = 150.0, 20.0, 27.0
Irec = 0.1 * C_Ah
Pbat = Vbatmax * Irec
Vnom, Vmax_ef, Vmin_ef, fr = 220.0, 264.0, 176.0, 60.0


# ============================================================ 2. retificador
def retificador(Vef, Pret, C=None, dV_rel=0.1):
    """Retificador em ponte com filtro capacitivo (modelo de pulso retangular).

    Com C = None, dimensiona o capacitor para a ondulação dV_rel (como a
    planilha); com C dado, calcula a ondulação que ele produz."""
    Vmax = np.sqrt(2) * Vef

    def cap(Vmin):
        th = pi / 2 - np.arcsin(Vmin / Vmax)
        return Pret * (pi - th) / (pi * fr * (Vmax ** 2 - Vmin ** 2))

    if C is None:
        Vmin = Vmax * (1 - dV_rel)
        C = cap(Vmin)
    else:                       # bisseção: cap(Vmin) cresce com Vmin
        a, b = 0.2 * Vmax, Vmax * (1 - 1e-9)
        for _ in range(200):
            Vmin = 0.5 * (a + b)
            a, b = (Vmin, b) if cap(Vmin) < C else (a, Vmin)
    th = pi / 2 - np.arcsin(Vmin / Vmax)
    Vmed = 0.5 * (Vmax + Vmin)
    Io = Pret / Vmed
    Ichg = Io * pi / th
    r = dict(Vef=Vef, C=C, Vmax=Vmax, Vmin=Vmin, dV=Vmax - Vmin, theta=th,
             tc=th / (2 * pi * fr), Vmed=Vmed, Io=Io, Req=Vmed ** 2 / Pret, Ichg=Ichg,
             ICef=np.sqrt(((Ichg - Io) ** 2 * th + Io ** 2 * (pi - th)) / pi),
             IDmed=Ichg * th / (2 * pi), IDef=Ichg * np.sqrt(th / (2 * pi)),
             Iinef=Ichg * np.sqrt(th / pi))
    r["FP"] = Pret / (Vef * r["Iinef"])
    return r


eta_ret = 0.9
Pret = Pbat / eta_ret
RET_PROJ = retificador(Vmin_ef, Pret)                 # como a planilha
C1_adotado = 940e-6


# ============================================================ 3. Forward de duas chaves
Vimax_cc, Vimin_cc = 373.0, 225.0
Vo, Io = 27.0, 15.0
dIL, dVc, fs, Dmax = 3.0, 0.27, 50e3, 0.4
n = round(Vo / (Vimin_cc * Dmax), 4)
Dmin = Vo / (Vimax_cc * n)
Lo = Vimax_cc * n * Dmin * (1 - Dmin) / (fs * dIL)
Co_calc = Vimax_cc * n * (1 - Dmin) * Dmin / (8 * Lo * fs ** 2 * dVc)
Rse_max = dVc / dIL
Co, Rse = 2200e-6, 0.11                               # EPCOS B41821, 50 V
Ro = Vo / Io
Lm = 20e-3
Lo_sim = 136.6e-6


def esforcos(Vcc, Vd=0.7, Rsh=0.01):
    """Esforços nos semicondutores do Forward para a tensão de barramento Vcc."""
    Vx = Vo + Vd + Vd + Rsh * Io          # bateria + D15 + diodo do filtro + shunt
    D = Vx / (n * Vcc)
    dI = (Vx - 0 * Vd) * (1 - D) / (Lo_sim * fs)
    Im = Vcc * D / (Lm * fs)
    Ipk_sec = Io + dI / 2
    return dict(Vcc=Vcc, D=D, dI=dI, Im=Im, Ipk_sec=Ipk_sec,
                IS_pk=n * Ipk_sec + Im, IS_med=n * Io * D + Im * D / 2,
                IS_ef=n * Io * np.sqrt(D) * np.sqrt(1 + (dI / Io) ** 2 / 12),
                ID2_med=Io * D, ID2_ef=Io * np.sqrt(D),
                ID1_med=Io * (1 - D), ID1_ef=Io * np.sqrt(1 - D),
                VS=Vcc, VD34=Vcc, VD12=n * Vcc, ICo_ef=dI / np.sqrt(12))


# ============================================================ 4. controle
def planta(f, Vcc, R=Ro):
    """Funções de transferência da planta: Gv = vo/d e Gi = iL/d."""
    s = 2j * pi * np.asarray(f, dtype=float)
    den = s ** 2 * Lo * Co * (Rse / R + 1) + s * (Lo / R + Co * Rse) + 1
    return Vcc * n * (s * Co * Rse + 1) / den, Vcc * n / R * (s * Co * (R + Rse) + 1) / den


def tipo2(f, R1, R2, C1, C2):
    s = 2j * pi * np.asarray(f, dtype=float)
    return (1 + s * C1 * R2) / (R1 * s * (C1 + C2 + s * R2 * C1 * C2))


def fator_k(malha, fc, VD, H, Vcc, MF=60.0, K=None, R1=10e3, f_ganho=None):
    """Projeto do compensador tipo 2 pelo fator K. malha = 'v' ou 'i'.

    f_ganho: frequência em que o ganho da planta é lido (a planilha lê o ganho
    da malha de corrente em fcv, e não em fci)."""
    Gv, Gi = planta([fc], Vcc)
    G = (Gv if malha == "v" else Gi)[0] * H / VD
    Gg = G
    if f_ganho is not None:
        Gv2, Gi2 = planta([f_ganho], Vcc)
        Gg = (Gv2 if malha == "v" else Gi2)[0] * H / VD
    A_dB = 20 * np.log10(abs(Gg))
    P = np.degrees(np.angle(G))
    alfa = MF - P - 90
    K_exato = np.tan(np.radians((alfa + 90) / 2))
    K = K_exato if K is None else K
    return dict(A_dB=A_dB, P=P, alfa=alfa, K_exato=K_exato, K=K, Fz=fc / K, Fp=fc * K)


def componentes_k(fc, K, ganho, R1=10e3):
    C2 = 1 / (2 * pi * fc * ganho * K * R1)
    C1 = C2 * (K ** 2 - 1)
    R2 = K / (2 * pi * fc * C1)
    return dict(R1=R1, R2=R2, C1=C1, C2=C2)


def margens(malha, comp, VD, H, Vcc, R=Ro):
    """Frequência de cruzamento e margem de fase do laço compensado."""
    f = np.logspace(1, np.log10(fs), 40000)
    Gv, Gi = planta(f, Vcc, R)
    T = (Gv if malha == "v" else Gi) * H / VD * tipo2(f, **comp)
    mag = 20 * np.log10(abs(T))
    k = np.nonzero((mag[:-1] > 0) & (mag[1:] <= 0))[0]
    if not len(k):
        return np.nan, np.nan
    k = k[-1]
    fc = f[k] + (f[k + 1] - f[k]) * mag[k] / (mag[k] - mag[k + 1])
    fase = np.degrees(np.unwrap(np.angle(T)))
    return fc, 180 + np.interp(fc, f, fase)


VD_plan, Vrefv, Vrefi = 2.1, 2.5, 2.5
Hv = Vrefv / Vo
Rsh, Kdif = 0.01, 16.6667
Hi = Rsh * Kdif
fcv, fci = fs / 10, fs / 4

# como a planilha
KV = fator_k("v", fcv, VD_plan, Hv, Vimax_cc, K=4.7)
CV_plan = componentes_k(fcv, KV["K"], 10 ** (abs(KV["A_dB"]) / 20))
KI = fator_k("i", fci, VD_plan, Hi, Vimax_cc, K=3.7, f_ganho=fcv)
CI_plan = componentes_k(fci, KI["K"], 10 ** (abs(KI["A_dB"]) / 20))
KI_ok = fator_k("i", fci, VD_plan, Hi, Vimax_cc)       # ganho lido na frequência certa
CI_ok = componentes_k(fci, KI_ok["K"], 10 ** (-KI_ok["A_dB"] / 20))

# como a simulação (componentes comerciais e portadora de 2,4 V pico a pico)
VD_sim = 2.4
CV_sim = dict(R1=10e3, R2=82e3, C1=1.5e-9, C2=100e-12)
CI_sim = dict(R1=10e3, R2=18e3, C1=2.7e-9, C2=220e-12)
Hv_sim = 10.2e3 / (100e3 + 10.2e3)
Hi_sim = Rsh * 167e3 / 10e3


def relatorio():
    titulo("1. Bateria e rede")
    linha("Corrente de recarga 0,1 C", Irec, "A", 15)
    linha("Potência máxima na bateria", Pbat, "W", 405)

    titulo("2. Retificador com filtro capacitivo (planilha: 176 V, ondulação de 10 %)")
    r = RET_PROJ
    for rot, ch, un, pl in [("Ondulação dVC1", "dV", "V", 24.89), ("VC1max", "Vmax", "V", 248.902),
                            ("VC1min", "Vmin", "V", 224.011), ("Ângulo de condução", "theta", "rad", 0.451),
                            ("Capacitor C1", "C", "F", 5.457e-4), ("Tempo de condução", "tc", "s", 1.196e-3),
                            ("VC1 médio", "Vmed", "V", 236.457), ("Corrente equivalente Ioeq", "Io", "A", 1.903),
                            ("Resistência equivalente", "Req", "ohm", 124.248),
                            ("Corrente de pico Ichg", "Ichg", "A", 13.256),
                            ("Corrente eficaz em C1", "ICef", "A", 4.648)]:
        linha(rot, r[ch], un, pl)
    print("\n  Extensão (mesmo modelo): esforços nos diodos e fator de potência")
    print("  %-22s %8s %8s %8s %8s %8s %8s %8s %8s %8s" % (
        "caso", "dV (V)", "Vmin", "theta", "Ichg", "ICef", "IDmed", "IDef", "Iin ef", "FP"))
    for Vef in (Vmin_ef, Vnom, Vmax_ef):
        for C, nome in ((RET_PROJ["C"], "545,7 uF"), (C1_adotado, "940 uF"), (470e-6, "470 uF")):
            r = retificador(Vef, Pret, C)
            print("  %3.0f V, %-14s %8.2f %8.2f %8.4f %8.2f %8.3f %8.3f %8.3f %8.3f %8.3f" % (
                Vef, nome, r["dV"], r["Vmin"], r["theta"], r["Ichg"], r["ICef"], r["IDmed"],
                r["IDef"], r["Iinef"], r["FP"]))
    linha("Tensão reversa máxima nos diodos (264 V)", np.sqrt(2) * Vmax_ef, "V")

    titulo("3. Forward de duas chaves")
    linha("Relação de espiras n = Ns/Np", n, "", 0.3)
    linha("Razão cíclica mínima", Dmin, "", 0.241)
    linha("Indutor Lo", Lo, "H", 1.366e-4)
    linha("Capacitor Co calculado", Co_calc, "F", 2.778e-5)
    linha("RSE máxima", Rse_max, "ohm", 0.09)
    linha("Carga equivalente Ro", Ro, "ohm", 1.8)
    linha("fo = 1/(2 pi raiz(Lo Co))", 1 / (2 * pi * np.sqrt(Lo * Co)), "Hz", 290.358)
    linha("fz = 1/(2 pi Co Rse)", 1 / (2 * pi * Co * Rse), "Hz", 657.665)
    print("\n  Extensão: esforços nos semicondutores (quedas de 0,7 V nos diodos e shunt de 10 mohm)")
    print("  %-20s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s" % (
        "barramento", "D", "dIL", "Im pk", "IS pk", "IS med", "IS ef", "ID2 med", "ID1 med",
        "VS", "VD1/2", "ICo ef"))
    for nome, Vcc in (("225 V (mín. proj.)", 225.0), ("240,8 V (176 V sim.)", 240.8),
                      ("373 V (máx.)", 373.0)):
        e = esforcos(Vcc)
        print("  %-20s %7.3f %7.2f %7.3f %7.2f %7.2f %7.2f %7.2f %7.2f %7.0f %7.1f %7.2f" % (
            nome, e["D"], e["dI"], e["Im"], e["IS_pk"], e["IS_med"], e["IS_ef"], e["ID2_med"],
            e["ID1_med"], e["VS"], e["VD12"], e["ICo_ef"]))
    linha("Potência no shunt (15 A)", Rsh * Io ** 2, "W")

    titulo("4. Malha de tensão (planilha: Vimax = 373 V, VD = 2,1 V)")
    linha("Ganho de FTLAsc em fcv = 5 kHz", KV["A_dB"], "dB", -18.376)
    linha("Fase de FTLAsc em fcv", KV["P"], "graus", -95.67)
    linha("Avanço de fase", KV["alfa"], "graus", 65.67)
    linha("Fator K exato (planilha leu 4,7)", KV["K_exato"], "")
    linha("Zero Fz1", KV["Fz"], "Hz", 1.064e3)
    linha("Polo Fp1", KV["Fp"], "Hz", 2.35e4)
    linha("C2", CV_plan["C2"], "F", 8.165e-11)
    linha("C1", CV_plan["C1"], "F", 1.722e-9)
    linha("R2", CV_plan["R2"], "ohm", 8.688e4)
    fc, mf = margens("v", CV_plan, VD_plan, Hv, Vimax_cc)
    linha("Cruzamento obtido", fc, "Hz", 5e3)
    linha("Margem de fase obtida", mf, "graus", 60.307)

    titulo("5. Malha de corrente (planilha: Vimax = 373 V, VD = 2,1 V)")
    linha("Hi = Rsh Kdif", Hi, "V/A")
    linha("Ganho de FTLAsc lido em fcv = 5 kHz", KI["A_dB"], "dB", 6.343)
    linha("Ganho de FTLAsc em fci = 12,5 kHz", KI_ok["A_dB"], "dB")
    linha("Fase de FTLAsc em fci", KI["P"], "graus", -89.446)
    linha("Avanço de fase", KI["alfa"], "graus", 59.446)
    linha("Fator K exato (planilha leu 3,7)", KI["K_exato"], "")
    linha("Zero Fz1", KI["Fz"], "Hz", 3.378e3)
    linha("Polo Fp1", KI["Fp"], "Hz", 4.625e4)
    linha("C2", CI_plan["C2"], "F", 1.658e-10)
    linha("C1", CI_plan["C1"], "F", 2.104e-9)
    linha("R2", CI_plan["R2"], "ohm", 2.239e4)
    fc, mf = margens("i", CI_plan, VD_plan, Hi, Vimax_cc)
    linha("Cruzamento REAL com os valores da planilha", fc, "Hz")
    linha("Margem de fase REAL", mf, "graus")
    print("  Com o ganho lido na frequência certa (fci) e K exato:")
    for k, un in (("R2", "ohm"), ("C1", "F"), ("C2", "F")):
        linha("    " + k, CI_ok[k], un)
    fc, mf = margens("i", CI_ok, VD_plan, Hi, Vimax_cc)
    linha("    cruzamento", fc, "Hz")
    linha("    margem de fase", mf, "graus")

    titulo("6. Laços com os componentes da simulação (VD = 2,4 V)")
    linha("Hv = R12/(R11 + R12)", Hv_sim, "", Hv)
    linha("Hi = Rsh R4/R2", Hi_sim, "V/A", Hi)
    linha("Tensão regulada Vrefv/Hv", Vrefv / Hv_sim, "V")
    linha("Limite de corrente Vrefi/Hi", Vrefi / Hi_sim, "A")
    print("  %-34s %10s %10s %10s %10s" % ("barramento / carga", "fc tensão", "MF tensão",
                                             "fc corr.", "MF corr."))
    for nome, Vcc, R in (("240,8 V (176 V), 100 %", 240.8, Ro), ("240,8 V (176 V), 20 %", 240.8, 5 * Ro),
                         ("371,9 V (264 V), 100 %", 371.9, Ro), ("371,9 V (264 V), 20 %", 371.9, 5 * Ro)):
        fv, mv = margens("v", CV_sim, VD_sim, Hv_sim, Vcc, R)
        fi, mi = margens("i", CI_sim, VD_sim, Hi_sim, Vcc, R)
        print("  %-34s %8.0f Hz %8.1f gr %8.0f Hz %8.1f gr" % (nome, fv, mv, fi, mi))


def figuras():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG, exist_ok=True)
    f = np.logspace(0, 5, 2000)
    plt.rcParams.update({"font.size": 7.5})     # figuras na largura de uma coluna do artigo

    def bode(nome, curvas, tit):
        fig, ax = plt.subplots(2, 1, figsize=(3.5, 3.1), sharex=True)
        for T, rot, est in curvas:
            ax[0].semilogx(f, 20 * np.log10(abs(T)), est, label=rot, lw=1.1)
            ax[1].semilogx(f, np.degrees(np.unwrap(np.angle(T))), est, lw=1.1)
        ax[0].axhline(0, color="0.4", lw=0.6)
        ax[1].axhline(-180, color="0.4", lw=0.6, ls="--")
        ax[0].set_ylabel("Ganho (dB)")
        ax[1].set_ylabel("Fase (graus)")
        ax[1].set_xlabel("Frequência (Hz)")
        ax[1].set_yticks(np.arange(-180, 91, 45))
        for a in ax:
            a.grid(True, which="both", color="0.88", lw=0.5)
        # legenda acima do gráfico, fora da área das curvas (o título vai na legenda do artigo)
        ax[0].legend(fontsize=6.5, frameon=False, ncol=3 if len(curvas) == 3 else 2,
                     loc="lower center", bbox_to_anchor=(0.5, 1.0), handlelength=1.6,
                     columnspacing=1.0)
        fig.tight_layout(pad=0.4)
        fig.savefig(os.path.join(FIG, nome), dpi=300)
        plt.close(fig)

    Gv, Gi = planta(f, Vimax_cc)
    Tv = Gv * Hv / VD_plan
    Cv = tipo2(f, **CV_plan)
    bode("calc-bode-malha-tensao.png",
         [(Tv, "Sem compensador", "b-"), (Cv, "Compensador", "g--"),
          (Tv * Cv, "Com compensador", "r-")],
         "Malha de tensão (373 V, valores da planilha)")
    Ti = Gi * Hi / VD_plan
    Ci = tipo2(f, **CI_plan)
    bode("calc-bode-malha-corrente.png",
         [(Ti, "Sem compensador", "b-"), (Ci, "Compensador", "g--"),
          (Ti * Ci, "Com compensador", "r-")],
         "Malha de corrente (373 V, valores da planilha)")
    # laços reais da simulação, nas duas tensões
    curv_v, curv_i = [], []
    for Vcc, rot, est in ((240.8, "176 V", "b-"), (371.9, "264 V", "r-")):
        Gv, Gi = planta(f, Vcc)
        curv_v.append((Gv * Hv_sim / VD_sim * tipo2(f, **CV_sim), "Tensão, " + rot, est))
        curv_i.append((Gi * Hi_sim / VD_sim * tipo2(f, **CI_sim), "Corrente, " + rot, est + "-"))
    bode("calc-bode-lacos-simulados.png", curv_v + curv_i,
         "Laços com os componentes da simulação (portadora de 2,4 V)")
    # curva do fator K
    k = np.logspace(0, 2, 400)
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    ax.semilogx(k, np.degrees(2 * np.arctan(k) - pi / 2), "b-", label="Tipo 2")
    ax.semilogx(k, np.degrees(4 * np.arctan(np.sqrt(k)) - pi), "r--", label="Tipo 3")
    for a, kk, rot in ((KV["alfa"], KV["K_exato"], "tensão"), (KI["alfa"], KI["K_exato"], "corrente")):
        ax.plot([kk], [a], "ko", ms=4)
        ax.annotate("%s: K = %.2f" % (rot, kk), (kk, a), textcoords="offset points",
                    xytext=(6, -9), fontsize=6.5)
    ax.set_xlabel("Fator K")
    ax.set_ylabel("Avanço de fase (graus)")
    ax.grid(True, which="both", color="0.88", lw=0.5)
    ax.legend(fontsize=6.5, frameon=False)
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(FIG, "calc-fator-k.png"), dpi=300)
    plt.close(fig)
    print("\nfiguras gravadas em", FIG)


if __name__ == "__main__":
    relatorio()
    if "--figuras" in sys.argv:
        figuras()
