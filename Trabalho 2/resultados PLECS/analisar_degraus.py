"""Pós-processamento dos ensaios de degrau de carga exportados pelo PLECS.

Lê os CSV gravados pelos modelos de "simulação PLECS" (colunas: tempo,
Vo_iso, Vo_eq, Io_iso, Io_eq, IL_iso, IL_eq), gera as figuras no estilo das
Figs. 5, 9, 14, 19 e 21 do enunciado (vermelho = isolado, azul = equivalente)
e calcula as métricas de equivalência de cada degrau.

Uso:  python analisar_degraus.py            (processa todos os CSV presentes)
      python analisar_degraus.py forward    (só um conversor)

Saídas:
  ../desenvolvimento/figuras/plecs-<caso>-degrau-<de>-<para>.png  (300 dpi)
  metricas_degraus.csv e metricas_degraus.md (nesta pasta)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(AQUI), "desenvolvimento", "figuras")

# caso: (arquivo, fs do isolado, previsão de Vo, degraus)
# degrau: (rótulo, instante, janela do gráfico, instante do próximo evento)
CASOS = {
    "forward": ("forward_degrau.csv", 20e3, 54.0, [
        ("100-20", 0.05, (0.0475, 0.061), 0.10),
        ("20-100", 0.10, (0.0975, 0.105), 0.11)]),
    "fullbridge": ("fullbridge_degrau.csv", 20e3, 54.0, [
        ("20-100", 0.20, (0.1995, 0.2025), 0.30),
        ("100-20", 0.30, (0.2995, 0.305), 0.31)]),
    "pushpull": ("pushpull_degrau.csv", 20e3, 400.0, [
        ("20-100", 1.00, (0.991, 1.02), 1.25),
        ("100-20", 1.25, (1.231, 1.281), 1.30)]),
    "flyback_mcd": ("flyback_mcd_degrau.csv", 20e3, None, [
        ("20-100", 0.50, (0.477, 0.541), 0.75),
        ("100-20", 0.75, (0.727, 0.791), 0.80)]),
    "flyback_mcc": ("flyback_mcc_degrau.csv", 20e3, 54.0, [
        ("20-100", 0.50, (0.488, 0.536), 0.75),
        ("100-20", 0.75, (0.74, 0.80), 0.80)]),
}
NOMES = {"forward": "Forward", "fullbridge": "Full-bridge", "pushpull": "Push-pull",
         "flyback_mcd": "Flyback (MCD)", "flyback_mcc": "Flyback (MCC)"}


def ler_csv(caminho, t_ini=0.0):
    """Lê o CSV do PLECS a partir de t_ini (economiza memória nos arquivos grandes)."""
    linhas = []
    with open(caminho, encoding="utf-8") as f:
        f.readline()  # cabeçalho
        for ln in f:
            if float(ln[:ln.index(",")]) >= t_ini:
                linhas.append(ln)
    return np.loadtxt(linhas, delimiter=",")


def media_periodo(t, x, Ts):
    """Média móvel sobre um período de comutação (remove a ondulação)."""
    dt = np.median(np.diff(t))
    n = max(1, int(round(Ts / dt)))
    k = np.ones(n) / n
    return np.convolve(x, k, mode="same")


def metricas(t, x_iso, x_eq, t0, t_prox, Ts, busca_max):
    """Métricas de um degrau para um par de sinais (isolado, equivalente).

    busca_max: True se o extremo de interesse é um pico (máximo), False se é
    um vale (mínimo). Ex.: tensão de saída no degrau 20->100 % tem um vale.
    """
    res = {}
    for lab, x in (("iso", x_iso), ("eq", x_eq)):
        xm = media_periodo(t, x, Ts)
        antes = (t >= t0 - 2e-3) & (t < t0 - Ts)
        fim = min(t_prox, t[-1])
        janela_final = min(5e-3, (fim - t0) / 4)
        final = (t >= fim - janela_final) & (t < fim - Ts)
        x0, xf = xm[antes].mean(), xm[final].mean()
        apos = (t >= t0) & (t < fim - Ts)
        tt, xx = t[apos], xm[apos]
        # extremo = pico ou vale da resposta (ignora o primeiro período, em que a
        # média móvel ainda mistura valores de antes do degrau)
        v = (tt >= t0 + Ts)
        i_ext = np.nonzero(v)[0][np.argmax(xx[v]) if busca_max else np.argmin(xx[v])]
        faixa = 0.02 * abs(xf) if xf != 0 else 0.02
        fora = np.nonzero(np.abs(xx - xf) > faixa)[0]
        t_acomod = (tt[fora[-1]] - t0) if len(fora) else 0.0
        res[lab] = dict(antes=x0, final=xf, extremo=xx[i_ext], t_extremo=tt[i_ext] - t0,
                        t_acomod=t_acomod)
    sel = (t >= t0) & (t < min(t_prox, t[-1]))
    dif = x_iso[sel] - x_eq[sel]
    ref = max(abs(res["iso"]["final"]), 1e-9)
    res["erro_rms_pct"] = 100 * np.sqrt(np.mean(dif ** 2)) / ref
    res["erro_max_pct"] = 100 * np.max(np.abs(dif)) / ref
    return res


def figura(caso, rot, t, d, janela, t0):
    s = (t >= janela[0]) & (t <= janela[1])
    tm = (t[s] - t0) * 1e3  # ms relativos ao degrau
    fig, ax = plt.subplots(2, 1, figsize=(7.0, 4.6), sharex=True)
    for a, (ci, ce, ylab) in zip(ax, [(1, 2, r"$V_o$ (V)"), (3, 4, r"$I_o$ (A)")]):
        a.plot(tm, d[s, ci], color="#d62728", lw=2.4, label="Isolado")
        a.plot(tm, d[s, ce], color="#1f3fbf", lw=1.0, label="Equivalente")
        a.set_ylabel(ylab)
        a.grid(True, color="0.85", lw=0.6)
        a.axvline(0, color="0.5", lw=0.6, ls="--")
    ax[0].legend(loc="best", fontsize=8, frameon=False)
    ax[1].set_xlabel("Tempo após o degrau (ms)")
    de, para = rot.split("-")
    ax[0].set_title("%s: degrau de carga de %s %% para %s %%" % (NOMES[caso], de, para),
                    fontsize=10)
    fig.tight_layout()
    nome = "plecs-%s-degrau-%s-%s.png" % (caso.replace("_", "-"), de, para)
    fig.savefig(os.path.join(FIG, nome), dpi=300)
    plt.close(fig)
    return nome


def main(filtro=None):
    os.makedirs(FIG, exist_ok=True)
    linhas = []
    for caso, (arq, fs, vprev, degraus) in CASOS.items():
        if filtro and caso != filtro:
            continue
        caminho = os.path.join(AQUI, arq)
        if not os.path.exists(caminho):
            print("%-12s (sem CSV, pulado)" % caso)
            continue
        t_ini = min(dg[1] for dg in degraus) - 0.03
        d = ler_csv(caminho, max(0.0, t_ini))
        t = d[:, 0]
        for rot, t0, janela, t_prox in degraus:
            nome = figura(caso, rot, t, d, janela, t0)
            carga_sobe = rot == "20-100"
            for grandeza, (ci, ce) in (("Vo", (1, 2)), ("Io", (3, 4)), ("IL", (5, 6))):
                # Vo: vale quando a carga sobe, pico quando desce; correntes: o contrário
                busca_max = (not carga_sobe) if grandeza == "Vo" else carga_sobe
                m = metricas(t, d[:, ci], d[:, ce], t0, t_prox, 1 / fs, busca_max)
                linhas.append((caso, rot, grandeza, m))
            print("%-12s %-7s -> %s" % (caso, rot, nome))
    if not linhas:
        return
    # CSV
    with open(os.path.join(AQUI, "metricas_degraus.csv"), "w", encoding="utf-8") as f:
        f.write("caso,degrau,grandeza,antes_iso,antes_eq,final_iso,final_eq,extremo_iso,"
                "extremo_eq,t_extremo_iso_ms,t_extremo_eq_ms,t_acomod_iso_ms,t_acomod_eq_ms,"
                "erro_rms_pct,erro_max_pct\n")
        for caso, rot, g, m in linhas:
            i, e = m["iso"], m["eq"]
            f.write("%s,%s,%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.4g,%.4g,%.4g,%.4g,%.4g,%.4g\n" % (
                caso, rot, g, i["antes"], e["antes"], i["final"], e["final"], i["extremo"],
                e["extremo"], 1e3 * i["t_extremo"], 1e3 * e["t_extremo"], 1e3 * i["t_acomod"],
                1e3 * e["t_acomod"], m["erro_rms_pct"], m["erro_max_pct"]))
    # Markdown (só Vo e Io, que são as grandezas das figuras do professor)
    with open(os.path.join(AQUI, "metricas_degraus.md"), "w", encoding="utf-8") as f:
        f.write("# Métricas dos degraus de carga (PLECS)\n\n")
        f.write("Valores médios por período de comutação. Extremo = vale de Vo (e pico de Io) "
                "no degrau 20 → 100 %, pico de Vo (e vale de Io) no degrau 100 → 20 %; se "
                "coincide com o valor final, a resposta não tem sobressinal. Acomodação = último instante fora da faixa de ±2 % do "
                "valor final. Erros = diferença isolado − equivalente, em % do valor final.\n\n")
        f.write("| Caso | Degrau | Grandeza | Antes (iso / eq) | Final (iso / eq) | Extremo (iso / eq) "
                "| t extremo (ms) | Acomodação (ms) | Erro RMS | Erro máx |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for caso, rot, g, m in linhas:
            if g == "IL":
                continue
            i, e = m["iso"], m["eq"]
            linha = ("| %s | %s %% | %s | %.3f / %.3f | %.3f / %.3f | %.3f / %.3f | %.3f / %.3f "
                     "| %.2f / %.2f | %.3f %% | %.3f %% |\n") % (
                        NOMES[caso], rot.replace("-", " → "), g, i["antes"], e["antes"],
                        i["final"], e["final"], i["extremo"], e["extremo"],
                        1e3 * i["t_extremo"], 1e3 * e["t_extremo"],
                        1e3 * i["t_acomod"], 1e3 * e["t_acomod"],
                        m["erro_rms_pct"], m["erro_max_pct"])
            f.write(linha.replace(".", ","))  # vírgula decimal
    print("métricas: metricas_degraus.csv e metricas_degraus.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
