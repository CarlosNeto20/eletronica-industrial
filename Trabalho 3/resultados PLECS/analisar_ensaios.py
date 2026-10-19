"""Pós-processamento dos ensaios do carregador exportados pelo PLECS.

Lê os CSV gravados por rodar_ensaios.py, gera as figuras do memorial e do
artigo (no estilo das Figs. 15 a 17 do professor: tensão em verde, corrente em
vermelho) e calcula as métricas de cada ensaio.

Uso:  python analisar_ensaios.py

Saídas:
  ../desenvolvimento/figuras/plecs-*.png   (300 dpi)
  metricas_ensaios.md                      (nesta pasta)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(AQUI), "desenvolvimento", "figuras")
VERDE, VERM, AZUL, CINZA = "#1a9a1a", "#d62728", "#1f3fbf", "0.45"
FS, FR, T3 = 50e3, 60.0, 1.0 / 3.0
TS = 1 / FS
TENSOES = (176, 264)
COR_V = {176: AZUL, 264: VERM, 220: VERDE}
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.color": "0.88", "grid.linewidth": 0.5,
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})


# ------------------------------------------------------------------ leitura e utilitários
def le(nome):
    caminho = os.path.join(AQUI, nome)
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as f:
        cols = f.readline().strip().split(",")
    d = np.loadtxt(caminho, delimiter=",", skiprows=1)
    return {c: d[:, k] for k, c in enumerate(cols)}


def trap(y, t):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(t)))


def media(d, s, a=None, b=None):
    t, y = recorte(d, s, a, b)
    return trap(y, t) / (t[-1] - t[0])


def eficaz(d, s, a=None, b=None):
    t, y = recorte(d, s, a, b)
    return np.sqrt(trap(y * y, t) / (t[-1] - t[0]))


def recorte(d, s, a=None, b=None):
    t = d["t"]
    y = d[s] if isinstance(s, str) else s
    m = np.ones(len(t), bool)
    if a is not None:
        m &= t >= a
    if b is not None:
        m &= t <= b
    return t[m], y[m]


def media_ts(t, y, janela=TS):
    """Média móvel sobre um período de comutação (vale para passo variável)."""
    acum = np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(t))])
    a = np.clip(t - janela / 2, t[0], t[-1])
    b = np.clip(t + janela / 2, t[0], t[-1])
    return (np.interp(b, t, acum) - np.interp(a, t, acum)) / np.maximum(b - a, 1e-12)


def salva(fig, nome):
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, nome), dpi=300)
    plt.close(fig)
    print("  figura:", nome)


def num(x, casas=2):
    return ("%.*f" % (casas, x)).replace(".", ",")


# ------------------------------------------------------------------ figuras: panoramas
def fig_panorama(caso, v, lim_v, lim_i, t0=0.1, sufixo=""):
    """Tensão de saída e corrente no indutor ao longo de todo o ensaio (estilo das Figs. 15 a 17)."""
    d = le("%s_%d.csv" % (caso, v))
    if d is None:
        return
    fig, ax = plt.subplots(2, 1, figsize=(3.3, 2.7), sharex=True)
    m = d["t"] >= t0
    ax[0].plot(d["t"][m], d["v_bat"][m], color=VERDE, lw=0.5)
    ax[1].plot(d["t"][m], d["i_L"][m], color=VERM, lw=0.5)
    ax[0].set_ylabel(r"$V_{bat}$ (V)")
    ax[1].set_ylabel(r"$i_{Lo}$ (A)")
    ax[1].set_xlabel("Tempo (s)")
    ax[0].set_ylim(*lim_v)
    ax[1].set_ylim(*lim_i)
    ax[1].set_xlim(t0, d["t"][-1])
    ax[0].set_title("PLECS, rede em %d V%s" % (v, sufixo), fontsize=9)
    fig.tight_layout(pad=0.4)
    salva(fig, "plecs-%s-%d.png" % (caso, v))


# ------------------------------------------------------------------ figuras: detalhes
def fig_detalhe(nome, casos, linhas, janelas, titulos=None, legenda="best", tam=(3.5, 4.2), fonte=7.5):
    """Grade de detalhes em largura de uma coluna do artigo.

    casos: lista de colunas; cada coluna é uma lista de (arquivo, rótulo, cor, t0).
    linhas: lista de (sinal, rótulo do eixo). Tempo em ms a partir de t0."""
    with plt.rc_context({"font.size": fonte}):
        fig, ax = plt.subplots(len(linhas), len(casos), figsize=tam, sharex="col", squeeze=False)
        for j, col in enumerate(casos):
            for arq, rot, cor, t0 in col:
                d = le(arq)
                if d is None:
                    continue
                tm = (d["t"] - t0) * 1e3
                m = (tm >= janelas[j][0]) & (tm <= janelas[j][1])
                for i, (sin, ylab) in enumerate(linhas):
                    ax[i, j].plot(tm[m], d[sin][m], color=cor, lw=0.5, label=rot)
                    if j == 0:
                        ax[i, j].set_ylabel(ylab)
            if titulos:
                ax[0, j].set_title(titulos[j], fontsize=fonte)
            ax[-1, j].set_xlabel("Tempo após o evento (ms)")
            ax[-1, j].set_xlim(*janelas[j])
            for i in range(len(linhas)):
                ax[i, j].axvline(0, color="0.5", lw=0.5, ls="--")
        ax[0, 0].legend(fontsize=fonte - 1, loc=legenda, handlelength=1.4)
        fig.align_ylabels(ax[:, 0])
        fig.tight_layout(pad=0.6)
        salva(fig, nome)


# ------------------------------------------------------------------ figuras: regime
def fig_retificador():
    with plt.rc_context({"font.size": 7.5}):
        fig, ax = plt.subplots(3, 1, figsize=(3.5, 3.6), sharex=True)
        for v in TENSOES:
            d = le("regime_%d.csv" % v)
            if d is None:
                continue
            tm = (d["t"] - d["t"][0]) * 1e3
            ax[0].plot(tm, np.abs(d["v_rede"]), color=COR_V[v], lw=0.5, ls="--")
            ax[0].plot(tm, d["v_C1"], color=COR_V[v], lw=0.9, label="%d V" % v)
            ax[1].plot(tm, d["i_rede"], color=COR_V[v], lw=0.7)
            ax[2].plot(tm, d["i_D11"], color=COR_V[v], lw=0.7)
        ax[0].set_ylim(200, 390)
        ax[0].set_ylabel(r"$v_{C1}$ e $|v_{rede}|$ (V)")
        ax[1].set_ylabel(r"$i_{rede}$ (A)")
        ax[2].set_ylabel(r"$i_{D11}$ (A)")
        ax[2].set_xlabel("Tempo (ms)")
        ax[2].set_xlim(0, 1e3 * 2 / FR)
        # legenda acima do gráfico: dentro dele, as curvas tracejadas passariam por ela
        ax[0].legend(fontsize=6.5, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
        fig.tight_layout(pad=0.4)
        salva(fig, "plecs-retificador.png")


def janela_comutacao(d, n_per, onde=0.5):
    """Recorte de n_per períodos de comutação iniciado numa borda de subida do PWM."""
    t, p = d["t"], d["pwm"]
    bordas = t[1:][(p[1:] > 0.5) & (p[:-1] <= 0.5)]
    t0 = bordas[int(len(bordas) * onde)]
    m = (t >= t0 - 0.1 * TS) & (t <= t0 + (n_per + 0.1) * TS)
    return (t[m] - t0) * 1e6, m


def fig_forward_regime():
    sinais = [("pwm", r"$v_{g}$"), ("v_pri", r"$v_{pri}$ (V)"), ("i_Lm", r"$i_{Lm}$ (A)"),
              ("i_S", r"$i_{S}$ (A)"), ("v_S", r"$v_{S}$ (V)"), ("i_L", r"$i_{Lo}$ (A)")]
    with plt.rc_context({"font.size": 7.5}):
        fig, ax = plt.subplots(len(sinais), 1, figsize=(3.5, 4.8), sharex=True)
        for v in TENSOES:
            d = le("regime_%d.csv" % v)
            if d is None:
                continue
            tu, m = janela_comutacao(d, 2.5)
            for i, (s, ylab) in enumerate(sinais):
                ax[i].plot(tu, d[s][m], color=COR_V[v], lw=0.9, label="%d V" % v)
                ax[i].set_ylabel(ylab)
        ax[5].set_ylim(12.5, 17.5)
        ax[-1].set_xlabel(r"Tempo ($\mu$s)")
        ax[-1].set_xlim(-2, 52)
        ax[0].legend(fontsize=6.5, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
        fig.tight_layout(pad=0.4)
        salva(fig, "plecs-forward-regime.png")


def fig_portadora():
    with plt.rc_context({"font.size": 7.5}):
        fig, ax = plt.subplots(2, 1, figsize=(3.5, 3.2), sharex=True)
        for a, v in zip(ax, TENSOES):
            d = le("regime_%d.csv" % v)
            if d is None:
                continue
            tu, m = janela_comutacao(d, 5)
            a.plot(tu, d["v_tri"][m], color=AZUL, lw=0.8, label="Portadora")
            a.plot(tu, d["v_c"][m], color=VERM, lw=1.0, label=r"Moduladora $v_c$")
            a.fill_between(tu, 0.5, 0.5 + 0.25 * d["pwm"][m], step="post", color=VERDE, alpha=0.35,
                           lw=0, label="PWM")
            a.set_ylabel("Rede em %d V\nTensão (V)" % v)
            a.set_ylim(0.45, 3.9)
        ax[1].set_xlabel(r"Tempo ($\mu$s)")
        ax[1].set_xlim(0, 100)
        ax[0].legend(fontsize=6.5, loc="upper center", ncol=3, handlelength=1.4)
        fig.tight_layout(pad=0.4)
        salva(fig, "plecs-portadora.png")


def fig_partida():
    with plt.rc_context({"font.size": 7.5}):
        fig, ax = plt.subplots(2, 1, figsize=(3.5, 2.8), sharex=True)
        for v in TENSOES:
            d = le("degrau_%d.csv" % v)
            if d is None:
                continue
            m = d["t"] <= 0.03
            ax[0].plot(d["t"][m] * 1e3, d["v_bat"][m], color=COR_V[v], lw=0.7, label="%d V" % v)
            ax[1].plot(d["t"][m] * 1e3, d["i_L"][m], color=COR_V[v], lw=0.4)
        ax[0].set_ylabel(r"$V_{bat}$ (V)")
        ax[1].set_ylabel(r"$i_{Lo}$ (A)")
        ax[1].set_xlabel("Tempo (ms)")
        ax[1].set_xlim(0, 30)
        ax[0].legend(fontsize=6.5, loc="lower right")
        fig.tight_layout(pad=0.4)
        salva(fig, "plecs-partida.png")


# ------------------------------------------------------------------ métricas
def metricas_regime(v):
    d = le("regime_%d.csv" % v)
    if d is None:
        return None
    t = d["t"]
    T = t[-1] - t[0]
    w = 2 * np.pi * FR
    r = {}
    r["Vc1_max"], r["Vc1_min"], r["Vc1_med"] = d["v_C1"].max(), d["v_C1"].min(), media(d, "v_C1")
    r["dVc1"] = r["Vc1_max"] - r["Vc1_min"]
    r["Irede_ef"], r["Irede_pk"] = eficaz(d, "i_rede"), np.abs(d["i_rede"]).max()
    r["Pin"] = media(d, d["v_rede"] * d["i_rede"])
    r["S"] = eficaz(d, "v_rede") * r["Irede_ef"]
    r["FP"] = r["Pin"] / r["S"]
    a = 2 / T * trap(d["i_rede"] * np.sin(w * t), t)
    b = 2 / T * trap(d["i_rede"] * np.cos(w * t), t)
    i1 = np.hypot(a, b) / np.sqrt(2)
    r["I1_ef"] = i1
    r["THD"] = np.sqrt(max(r["Irede_ef"] ** 2 - i1 ** 2, 0)) / i1
    r["cos_fi1"] = r["Pin"] / (eficaz(d, "v_rede") * i1)
    r["Ic1_ef"] = eficaz(d, "i_C1")
    r["Id_med"], r["Id_ef"], r["Id_pk"] = media(d, "i_D11"), eficaz(d, "i_D11"), d["i_D11"].max()
    r["Vd_rev"] = -d["v_D11"].min()
    cond = (d["i_D11"] > 0.05).astype(float)
    r["tc"] = trap(cond, t) / (T * FR)                        # tempo de condução por pulso
    r["D"] = media(d, "pwm")
    r["IL_med"] = media(d, "i_L")
    il_ts = media_ts(t, d["i_L"])
    r["dIL"] = 2 * np.sqrt(2) * np.sqrt(trap((d["i_L"] - il_ts) ** 2, t) / T) * np.sqrt(1.5)   # triangular
    r["IL_max"], r["IL_min"] = d["i_L"].max(), d["i_L"].min()
    r["Vbat_med"], r["Vbat_pp"] = media(d, "v_bat"), d["v_bat"].max() - d["v_bat"].min()
    r["VS_max"], r["IS_pk"], r["IS_ef"], r["IS_med"] = d["v_S"].max(), d["i_S"].max(), eficaz(d, "i_S"), media(d, "i_S")
    r["ILm_pk"], r["ID3_med"] = d["i_Lm"].max(), media(d, "i_D3")
    r["VD2_rev"], r["ID2_med"], r["ID2_ef"] = -d["v_D2"].min(), media(d, "i_D2"), eficaz(d, "i_D2")
    r["VD1_rev"], r["ID1_med"], r["ID1_ef"] = -d["v_D1"].min(), media(d, "i_D1"), eficaz(d, "i_D1")
    r["ICo_ef"] = eficaz(d, "i_Co")
    r["Po"] = media(d, d["v_bat"] * d["i_o"])
    r["rend"] = r["Po"] / r["Pin"]
    r["vc_min"], r["vc_max"] = d["v_c"].min(), d["v_c"].max()
    r["vCv"], r["vCi"] = media(d, "v_Cv"), media(d, "v_Ci")
    return r


def metricas_evento(arq, t0, faixa=0.27, fim=None):
    """Transitório em torno de t0: valores antes, extremos, final e acomodação de Vbat."""
    d = le(arq)
    if d is None:
        return None
    t = d["t"]
    vb = media_ts(t, d["v_bat"])
    il = media_ts(t, d["i_L"])
    fim = fim or t[-1]
    antes = (t >= t0 - 1.5e-3) & (t <= t0 - 0.1e-3)
    final = (t >= fim - 1.0e-3) & (t <= fim - TS)
    apos = (t >= t0) & (t <= fim - TS)
    r = dict(Vb_antes=vb[antes].mean(), Vb_final=vb[final].mean(),
             Vb_max=d["v_bat"][apos].max(), Vb_min=d["v_bat"][apos].min(),
             IL_antes=il[antes].mean(), IL_final=il[final].mean(),
             IL_max=d["i_L"][apos].max(), IL_min=d["i_L"][apos].min(),
             Io_max=d["i_o"][apos].max(), vCv_antes=d["v_Cv"][antes].mean(),
             vCi_antes=d["v_Ci"][antes].mean())
    fora = np.nonzero(apos & (np.abs(vb - r["Vb_final"]) > faixa))[0]
    r["t_acomod"] = (t[fora[-1]] - t0) if len(fora) else 0.0
    return r


def metricas_curto_saida(v):
    d = le("curto_%d_saida.csv" % v)
    if d is None:
        return None
    t = d["t"]
    t0 = 0.5
    vb = media_ts(t, d["v_bat"])
    vf = vb[(t >= t[-1] - 2e-3)].mean()
    apos = t >= t0
    t10 = t[apos][np.argmax(vb[apos] >= 0.1 * vf)] - t0
    t90 = t[apos][np.argmax(vb[apos] >= 0.9 * vf)] - t0
    il = media_ts(t, d["i_L"])
    return dict(Vf=vf, t10=t10, t90=t90, IL_subida=il[(t >= t0 + 1e-3) & (t <= t0 + t90)].mean(),
                IL_max=d["i_L"][apos].max())


def metricas_recarga(v):
    d = le("recarga_%d.csv" % v)
    if d is None:
        return None
    t = d["t"]
    vb = media_ts(t, d["v_bat"], 10 * TS)
    il = media_ts(t, d["i_L"], 10 * TS)
    cc = (t >= 0.05) & (t <= 0.30)
    k = np.argmax((il < 0.5 * il[cc].mean()) & (t > 0.05))
    fim = t >= t[-1] - 0.02
    return dict(Icc=il[cc].mean(), V0=vb[np.argmax(t >= 0.01)], inclinacao=np.polyfit(t[cc], vb[cc], 1)[0],
                t_trans=t[k], Vfim=vb[fim].mean(), Ifim=il[fim].mean(), Vmax=d["v_bat"].max(),
                IL_max=d["i_L"][t > 0.02].max())


def escreve_metricas():
    L = ["# Métricas dos ensaios do carregador (PLECS)\n",
         "Geradas por `analisar_ensaios.py` a partir dos CSV desta pasta. Médias e valores "
         "eficazes calculados por integração trapezoidal; nos transitórios, \"antes\" e \"final\" "
         "são médias por período de comutação e os extremos são valores instantâneos.\n"]
    # ---- regime
    reg = {v: metricas_regime(v) for v in (176, 220, 264)}
    reg = {v: r for v, r in reg.items() if r}
    if reg:
        vs = sorted(reg)
        L += ["\n## Regime permanente com carga nominal (1,8 Ω)\n",
              "| Grandeza | " + " | ".join("%d V" % v for v in vs) + " |",
              "|---|" + "---|" * len(vs)]
        linhas = [("Tensão máxima em C1 (V)", "Vc1_max", 1), ("Tensão mínima em C1 (V)", "Vc1_min", 1),
                  ("Tensão média em C1 (V)", "Vc1_med", 1), ("Ondulação em C1 (V)", "dVc1", 2),
                  ("Corrente eficaz da rede (A)", "Irede_ef", 2), ("Corrente de pico da rede (A)", "Irede_pk", 1),
                  ("Potência de entrada (W)", "Pin", 1), ("Potência aparente (VA)", "S", 0),
                  ("Fator de potência", "FP", 3), ("DHT da corrente", "THD", 2),
                  ("Fator de deslocamento", "cos_fi1", 3),
                  ("Corrente eficaz em C1 (A)", "Ic1_ef", 2), ("Corrente média num diodo da ponte (A)", "Id_med", 3),
                  ("Corrente eficaz num diodo da ponte (A)", "Id_ef", 2), ("Corrente de pico num diodo da ponte (A)", "Id_pk", 1),
                  ("Tensão reversa num diodo da ponte (V)", "Vd_rev", 1), ("Tempo de condução por pulso (ms)", "tc", 3),
                  ("Razão cíclica média", "D", 3), ("Corrente média em Lo (A)", "IL_med", 2),
                  ("Corrente máxima em Lo (A)", "IL_max", 2), ("Corrente mínima em Lo (A)", "IL_min", 2),
                  ("Tensão média na saída (V)", "Vbat_med", 2), ("Ondulação da tensão de saída (V)", "Vbat_pp", 3),
                  ("Tensão máxima nas chaves (V)", "VS_max", 1), ("Corrente de pico nas chaves (A)", "IS_pk", 2),
                  ("Corrente eficaz nas chaves (A)", "IS_ef", 2), ("Corrente média nas chaves (A)", "IS_med", 2),
                  ("Corrente magnetizante de pico (A)", "ILm_pk", 3),
                  ("Tensão reversa em D2 (V)", "VD2_rev", 1), ("Corrente média em D2 (A)", "ID2_med", 2),
                  ("Corrente eficaz em D2 (A)", "ID2_ef", 2),
                  ("Tensão reversa em D1 (V)", "VD1_rev", 1), ("Corrente média em D1 (A)", "ID1_med", 2),
                  ("Corrente eficaz em D1 (A)", "ID1_ef", 2), ("Corrente eficaz em C4 (A)", "ICo_ef", 2),
                  ("Potência de saída (W)", "Po", 1), ("Rendimento", "rend", 3),
                  ("Tensão de controle mínima (V)", "vc_min", 2), ("Tensão de controle máxima (V)", "vc_max", 2),
                  ("Saída do compensador de tensão (V)", "vCv", 2), ("Saída do compensador de corrente (V)", "vCi", 2)]
        for rot, ch, casas in linhas:
            esc = 1e3 if ch == "tc" else 1.0
            L.append("| %s | " % rot + " | ".join(num(reg[v][ch] * esc, casas) for v in vs) + " |")
    # ---- degraus
    for caso, tit in (("degrau", "Degrau de carga (valores nominais do projeto)"),
                      ("degrau-folga", "Degrau de carga com folga no limite de corrente (Vrefi = 2,6 V)")):
        tab = []
        for v in TENSOES:
            for suf, t0, rot in (("_100-20", 0.5, "100 → 20 %"), ("_20-100", 2 * T3, "20 → 100 %")):
                m = metricas_evento("%s_%d%s.csv" % (caso, v, suf), t0)
                if m:
                    tab.append("| %d V | %s | %s | %s | %s | %s | %s / %s | %s | %s | %s |" % (
                        v, rot, num(m["Vb_antes"]), num(m["Vb_max"]), num(m["Vb_min"]), num(m["Vb_final"]),
                        num(m["IL_antes"]), num(m["IL_final"]), num(m["IL_max"]),
                        num(m["t_acomod"] * 1e3), num(m["vCv_antes"])))
        if tab:
            L += ["\n## %s\n" % tit,
                  "| Rede | Degrau | Vbat antes (V) | Vbat máx (V) | Vbat mín (V) | Vbat final (V) | "
                  "IL antes / final (A) | IL máx (A) | Acomodação a ±1 % (ms) | vCv antes (V) |",
                  "|---|---|---|---|---|---|---|---|---|---|"] + tab
    # ---- curto
    tab = []
    for v in TENSOES:
        e = metricas_evento("curto_%d_entrada.csv" % v, T3)
        s = metricas_curto_saida(v)
        if e and s:
            tab.append("| %d V | %s | %s | %s | %s | %s | %s | %s |" % (
                v, num(e["IL_antes"]), num(e["IL_max"]), num(e["IL_final"]), num(e["Io_max"], 0),
                num(s["t90"] * 1e3, 1), num(s["Vf"]), num(s["IL_subida"])))
    if tab:
        L += ["\n## Curto-circuito na saída (1 mΩ)\n",
              "| Rede | IL antes (A) | IL máx no curto (A) | IL em curto (A) | Pico em D15 (A) | "
              "Subida de Vbat até 90 % (ms) | Vbat final (V) | IL durante a subida (A) |",
              "|---|---|---|---|---|---|---|---|"] + tab
    # ---- recarga
    tab = []
    for v in TENSOES:
        m = metricas_recarga(v)
        if m:
            tab.append("| %d V | %s | %s | %s | %s | %s | %s | %s |" % (
                v, num(m["Icc"]), num(m["V0"]), num(m["inclinacao"], 1), num(m["t_trans"], 3),
                num(m["Vfim"]), num(m["Ifim"], 3), num(m["Vmax"])))
    if tab:
        L += ["\n## Recarga da bateria (R22 = 10 mΩ, C2 = 0,8 F, VDC1 = 20 V)\n",
              "| Rede | Corrente de recarga (A) | Vbat inicial (V) | Inclinação (V/s) | "
              "Fim da corrente constante (s) | Vbat final (V) | IL final (A) | Vbat máx (V) |",
              "|---|---|---|---|---|---|---|---|"] + tab
    with open(os.path.join(AQUI, "metricas_ensaios.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    print("figuras em", FIG)
    for v in TENSOES:
        fig_panorama("degrau", v, (25.3, 29.7), (-2, 25))
        fig_panorama("degrau-folga", v, (25.3, 29.7), (-2, 25), sufixo=" (Vrefi = 2,6 V)")
        fig_panorama("curto", v, (-1, 31), (0, 22))
        fig_panorama("recarga", v, (19.5, 28.5), (-2, 22), t0=0.0)
    # degraus de carga: valores nominais nas duas tensões e o caso com folga no limite de corrente
    linhas = [("v_bat", r"$V_{bat}$ (V)"), ("i_L", r"$i_{Lo}$ (A)"), ("v_Cv", r"$v_{Cv}$ (V)")]
    # a legenda fica no canto livre do primeiro gráfico: em cima na retirada de carga (a tensão
    # sobe e volta a 27 V), embaixo na aplicação (a tensão afunda só no instante do degrau)
    for suf, t0, leg in (("100-20", 0.5, "upper right"), ("20-100", 2 * T3, "lower right")):
        fig_detalhe("plecs-degrau-%s.png" % suf,
                    [[("degrau_176_%s.csv" % suf, "176 V", AZUL, t0),
                      ("degrau_264_%s.csv" % suf, "264 V", VERM, t0),
                      ("degrau-folga_176_%s.csv" % suf, "176 V, com folga", VERDE, t0)]],
                    linhas, [(-0.5, 4.0)], legenda=leg)
    fig_detalhe("plecs-curto-detalhe.png",
                [[("curto_%d_entrada.csv" % v, "%d V" % v, COR_V[v], T3) for v in TENSOES],
                 [("curto_%d_saida.csv" % v, "%d V" % v, COR_V[v], 0.5) for v in TENSOES]],
                [("v_bat", r"$V_{bat}$ (V)"), ("i_L", r"$i_{Lo}$ (A)")], [(-0.5, 2.0), (-2.0, 30.0)],
                ["Aplicação do curto", "Retirada do curto"], legenda="upper right",
                tam=(3.5, 3.0), fonte=7)
    fig_retificador()
    fig_forward_regime()
    fig_portadora()
    fig_partida()
    escreve_metricas()


if __name__ == "__main__":
    main()
