"""Gera o modelo PLECS do carregador de baterias do Trabalho 3.

Uso (a partir desta pasta):   python gerar_carregador.py [--previa]
Saída: ../carregador.plecs  (PLECS Standalone 5.0)

O circuito reproduz a Fig. 14 do professor (PSIM), com os mesmos designadores:
retificador em ponte com filtro capacitivo (V1, D11 a D14, C1), Forward de
duas chaves (MOS3, MOS1, D3, D4, T1), filtro de saída (D2, D1, L2, R8 + C4),
sensor de corrente (Rsh), diodo de bloqueio (D15), cargas (R9, R10 comutado,
modelo da bateria R22 + C2 + VDC1) e o controle analógico com amplificadores
operacionais saturados em 0 e 5 V: amplificador diferencial (OP_AMP2),
compensador de corrente (OP_AMP14), seguidor de tensão (OP_AMP3), compensador
de tensão (OP_AMP1), combinação das malhas por R7 e D6, grampo (DZ) e
modulador PWM (COMP3 + VTRI1).

Todos os valores entram por variáveis dos comandos de inicialização
(Simulation > Simulation Parameters > Initialization). As duas que definem o
ensaio são "Vrede" (176 ou 264) e "ensaio" (1, 2 ou 3).
"""
import os
import sys
from plecs_lib import Model

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.dirname(AQUI)
CABECALHO = os.path.join(AQUI, "cabecalho_plecs50.txt")

OPAMP = "Components/Electrical/Electronics/Lim. Op-Amp"
ZENER = "Components/Electrical/Power Semiconductors/Z1"
T_OPAMP = [(-25, -10, "left"), (-25, 10, "left"), (25, 0, "right"), (0, 15, "down")]
T_ZENER = [(15, 0, "right"), (-15, 0, "left")]        # 1 = catodo, 2 = anodo

# sinais gravados pela porta de saída "Out", nesta ordem (colunas do CSV).
# Dentro de um mesmo componente o PLECS usa a sua própria ordem (diodo e capacitor:
# tensão, corrente; indutor: corrente, tensão), que é a seguida aqui.
MEDIDAS = [
    ("v_rede", "V1", "Source voltage"),
    ("i_rede", "V1", "Source current"),
    ("v_C1", "C1", "Capacitor voltage"),
    ("i_C1", "C1", "Capacitor current"),
    ("v_D11", "D11", "Diode voltage"),
    ("i_D11", "D11", "Diode current"),
    ("v_S", "MOS1", "Device voltage"),
    ("i_S", "MOS1", "Device current"),
    ("i_D3", "D3", "Diode current"),
    ("i_Lm", "Lm", "Inductor current"),
    ("v_pri", "Lm", "Inductor voltage"),
    ("v_D2", "D2", "Diode voltage"),
    ("i_D2", "D2", "Diode current"),
    ("v_D1", "D1", "Diode voltage"),
    ("i_D1", "D1", "Diode current"),
    ("i_L", "L2", "Inductor current"),
    ("i_Co", "C4", "Capacitor current"),
    ("v_Co", "V11", "Measured voltage"),
    ("v_bat", "Vbat", "Measured voltage"),
    ("i_o", "D15", "Diode current"),
    ("i_bat", "R22", "Resistor current"),
    ("v_c", "V9", "Measured voltage"),
    ("v_tri", "VTRI1", "Output"),
    ("pwm", "COMP3", "Output"),
    ("v_Cv", "R15", "Resistor voltage"),
    ("v_Ci", "R19", "Resistor voltage"),
    ("v_Hi", "R6", "Resistor voltage"),
    ("v_Hv", "R20", "Resistor voltage"),
]

INIT = """% ================= CARREGADOR DE BATERIAS DE 15 A - FORWARD DE DUAS CHAVES =================
% ---- as duas variaveis que definem o ensaio
Vrede  = 176;     % tensao eficaz da rede (V): 176 = minima, 220 = nominal, 264 = maxima
ensaio = 1;       % 0 = regime a 100 %; 1 = degrau de carga 100 % <-> 20 %; 2 = curto-circuito;
                  % 3 = recarga da bateria
% ---- rede e retificador com filtro capacitivo
fr  = 60;
Vpk = sqrt(2)*Vrede;
C1  = 940e-6;     % 2 x 470 uF/450 V (planilha); o esquematico do professor mostra 470 uF
Vd  = 0.7;        % queda dos diodos, como no PSIM
Rd  = 5e-3;       % resistencia de conducao dos diodos da ponte: o PLECS nao aceita fonte ideal
                  % em paralelo com C1 atraves de chaves ideais (no PSIM o professor usou 0)
% ---- Forward de duas chaves
fs = 50e3;  Np = 100;  Ns = 30;  Lm = 20e-3;
Lk = 0.1e-6 + 0.1e-6*(Ns/Np)^2;   % dispersao do PSIM (0,1 uH por enrolamento), referida ao secundario
Lo = 136.6e-6;  Co = 2200e-6;  Rse = 0.11;  Rsh = 0.01;
% ---- saida, carga e bateria
Vo = 27;  Io = 15;  Ro = Vo/Io;
f_carga = 3;      % comutacao da carga (Hz), razao ciclica 0,5; comeca ligada
R9 = 5*Ro;  R10 = 1.25*Ro;  hab_carga = 1;  hab_bat = 0;      % ensaio 1: 20 % fixo + 80 % comutado
if ensaio == 0, R9 = Ro;  R10 = 1e6; hab_carga = 0; end        % carga nominal fixa
if ensaio == 2, R9 = Ro;  R10 = 1e-3; end                      % curto-circuito de 1 mOhm
if ensaio == 3, R9 = 1e6; R10 = 1e6; hab_carga = 0; hab_bat = 1; end
Vbat0 = 20;  Rbat = 10e-3;
Cbat  = 0.8;      % emula o tempo de recarga (0,8 F reproduz a Fig. 17; o esquematico mostra 400 mF)
% ---- controle
Vrefv = 2.5;      % referencia de tensao (27 V na saida)
Vrefi = 2.5;      % referencia de corrente: 0 a 2,5 V ajusta a recarga de 0 a 15 A
R11 = 100e3;  R12 = 10.2e3;                           % divisor da tensao de saida
R13 = 10e3;  R14 = 82e3;  C5 = 1.5e-9;  C6 = 100e-12; % compensador de tensao (tipo 2)
R2 = 10e3;  R3 = 10e3;  R4 = 167e3;  R5 = 167e3;      % amplificador diferencial do shunt
R16 = 10e3;  R18 = 18e3;  C7 = 2.7e-9;  C8 = 220e-12; % compensador de corrente (tipo 2)
R7 = 1e3;  Rpd = 100e3;  Vd6 = 0.5;
Vtri_min = 0.8;  Vtri_max = 3.2;                      % portadora triangular (2,4 V pico a pico)
Dmax = 0.48;  Vz = Vtri_min + Dmax*(Vtri_max - Vtri_min);   % grampo da tensao de controle
Aop = 1e5;  Vsat = [0 5];                             % amplificadores operacionais
% ---- condicoes iniciais
VC1_0 = Vpk - 2*Vd;  VCo_0 = 0;
"""


def terra(m, nome, x, y):
    m.add("Ground", nome, x, y, show=False)
    return (nome, 1)


def aterra(m, term, nome):
    """Símbolo de terra logo abaixo de um terminal que aponta para baixo."""
    (x, y), _ = m.term(*term)
    m.direct(term, terra(m, nome, x, y + 30))


def opamp(m, nome, x, y):
    m.add_ref(nome, OPAMP, x, y, T_OPAMP, ((-20, -20), (20, 20)),
              [("A", "Aop"), ("Vlim", "Vsat")], label="north")
    aterra(m, (nome, 4), "G_" + nome)


def carregador():
    m = Model("carregador", "1.0", "2e-6", rel_tol="1e-4", init_cmds=INIT)
    P, N = 100, 380                     # barramentos superior e inferior do estágio de potência

    # ------------------------------------------------ retificador com filtro capacitivo
    m.add("ACVoltageSource", "V1", 60, 240, V="Vpk", w="2*pi*fr", phi="0")
    for nome, x, y in (("D13", 140, 160), ("D14", 140, 320), ("D11", 200, 160), ("D12", 200, 320)):
        m.add("Diode", nome, x, y, "down", Vf="Vd", Ron="Rd")
    m.add("Capacitor", "C1", 270, 240, C="C1", v_init="VC1_0")
    m.star(("V1", 1), [(140, 220)], [([], ("D13", 1)), ([], ("D14", 2))])
    m.star(("V1", 2), [(200, 260)], [([], ("D11", 1)), ([], ("D12", 2))])

    # ------------------------------------------------ Forward de duas chaves (primário)
    m.add("MosfetWithDiode", "MOS3", 380, 160)
    m.add("Diode", "D3", 380, 320, "down", Vf="Vd")
    m.add("Diode", "D4", 520, 160, "down", Vf="Vd")
    m.add("MosfetWithDiode", "MOS1", 520, 320)
    m.add("Inductor", "Lm", 600, 240, L="Lm", i_init="0")
    m.add("Transformer", "T1", 670, 240, "right", "on", Windings="[1 1]", n="[Np Ns]",
          Polarity="+", Lm="inf", im0="0")
    m.from_("F_MOS3", 300, 160, "pwm", ("MOS3", 3))
    m.from_("F_MOS1", 440, 320, "pwm", ("MOS1", 3))
    m.net([("D13", 2), ("D11", 2), ("C1", 1), ("MOS3", 1), ("D4", 2)], rail=P)
    m.net([("D14", 1), ("D12", 1), ("C1", 2), ("D3", 1), ("MOS1", 2)], rail=N)
    m.star(("MOS3", 2), [(380, 220)], [([], ("D3", 2)), ([], ("Lm", 1)), ([], ("T1", 1))])
    m.star(("MOS1", 1), [(520, 260)], [([], ("D4", 1)), ([], ("Lm", 2)), ([], ("T1", 2))])

    # ------------------------------------------------ secundário e filtro de saída
    m.add("Diode", "D2", 760, P, "left", Vf="Vd")
    m.add("Diode", "D1", 820, 240, "down", Vf="Vd")
    m.add("Inductor", "L2", 890, P, "left", L="Lo", i_init="0")
    m.add("Resistor", "R8", 960, 160, R="Rse")
    m.add("Capacitor", "C4", 960, 260, C="Co", v_init="VCo_0")
    m.add("Voltmeter", "V11", 1020, 240)
    m.add("Resistor", "Rsh", 880, N, "left", R="Rsh")
    m.add("Diode", "D15", 1090, P, "left", Vf="Vd")
    m.add("Inductor", "Lk", 700, 160, "down", L="Lk", i_init="0")
    m.direct(("T1", 3), ("Lk", 1), [(700, 220)])
    m.direct(("Lk", 2), ("D2", 1), [(700, P)])
    m.net([("D2", 2), ("D1", 2), ("L2", 1)], rail=P)
    m.net([("L2", 2), ("R8", 1), ("V11", 1), ("D15", 1)], rail=P)
    m.direct(("R8", 2), ("C4", 1))

    # ------------------------------------------------ cargas e modelo da bateria
    m.add("Resistor", "R9", 1160, 240, R="R9")
    m.add("Resistor", "R10", 1280, 170, R="R10")
    m.add("Switch", "MOS6", 1280, 280)
    m.from_("F_carga", 1210, 280, "carga", ("MOS6", 3))
    m.add("Switch", "S_bat", 1380, 150)
    m.from_("F_bat", 1310, 150, "bat", ("S_bat", 3))
    m.add("Resistor", "R22", 1380, 210, R="Rbat")
    m.add("Capacitor", "C2", 1380, 270, C="Cbat", v_init="0")
    m.add("DCVoltageSource", "VDC1", 1380, 330, V="Vbat0")
    m.add("Voltmeter", "Vbat", 1450, 240)
    m.add("Resistor", "R11", 1520, 170, R="R11")
    m.add("Resistor", "R12", 1520, 300, R="R12")
    m.direct(("R10", 2), ("MOS6", 1))
    m.direct(("S_bat", 2), ("R22", 1))
    m.direct(("R22", 2), ("C2", 1))
    m.direct(("C2", 2), ("VDC1", 1))
    m.net([("D15", 2), ("R9", 1), ("R10", 1), ("S_bat", 1), ("Vbat", 1), ("R11", 1)], rail=P)

    # ------------------------------------------------ amplificador diferencial do shunt
    m.add("Resistor", "R2", 850, 450, R="R2")
    m.add("Resistor", "R3", 910, 450, R="R3")
    m.add("Resistor", "R5", 940, 480, R="R5")
    opamp(m, "OP_AMP2", 990, 540)
    m.add("Resistor", "R4", 990, 640, "left", R="R4")
    m.add("Resistor", "R6", 1040, 460, "down", R="Rpd")
    m.add("Resistor", "R16", 1100, 540, "left", R="R16")
    m.star(("R2", 2), [(850, 550), (950, 550)], [([], ("OP_AMP2", 2)), ([(950, 640)], ("R4", 1))])
    m.star(("R3", 2), [(910, 530), (940, 530)], [([], ("OP_AMP2", 1)), ([], ("R5", 2))])
    m.star(("OP_AMP2", 3), [(1040, 540)],
           [([(1040, 640)], ("R4", 2)), ([], ("R6", 1)), ([], ("R16", 1))])

    # ------------------------------------------------ compensador de corrente (tipo 2)
    m.add("DCVoltageSource", "VDC3", 1160, 440, "down", V="Vrefi")
    opamp(m, "OP_AMP14", 1210, 530)
    m.add("Resistor", "R18", 1180, 620, "left", R="R18")
    m.add("Capacitor", "C7", 1240, 620, "left", C="C7", v_init="0")
    m.add("Capacitor", "C8", 1210, 680, "left", C="C8", v_init="0")
    m.add("Resistor", "R19", 1290, 460, "down", R="Rpd")
    m.add("Diode", "D6", 1290, 740, "down", Vf="Vd6")
    m.direct(("VDC3", 1), ("OP_AMP14", 1), [(1160, 520)])
    m.star(("R16", 2), [(1150, 540)],
           [([], ("OP_AMP14", 2)), ([(1150, 620)], ("R18", 1)), ([(1150, 680)], ("C8", 1))])
    m.direct(("R18", 2), ("C7", 1))
    m.star(("OP_AMP14", 3), [(1290, 530)],
           [([(1290, 620)], ("C7", 2)), ([(1290, 680)], ("C8", 2)), ([], ("R19", 1)),
            ([], ("D6", 2))])

    # ------------------------------------------------ divisor e seguidor de tensão
    opamp(m, "OP_AMP3", 1610, 245)
    m.add("Resistor", "R20", 1700, 300, R="Rpd")
    m.add("Label", "Hv_a", 1740, 245, "right", show=False, Tag="Hv", Visibility="1")
    m.star(("R11", 2), [(1520, 235)], [([], ("R12", 1)), ([], ("OP_AMP3", 1))])
    m.star(("OP_AMP3", 3), [(1660, 245)],
           [([(1660, 320), (1570, 320), (1570, 255)], ("OP_AMP3", 2)),
            ([(1700, 245)], ("R20", 1)), ([], ("Hv_a", 1))])

    # ------------------------------------------------ compensador de tensão (tipo 2)
    m.add("Label", "Hv_b", 850, 810, "left", show=False, Tag="Hv", Visibility="1")
    m.add("Resistor", "R13", 910, 810, "left", R="R13")
    m.add("DCVoltageSource", "VDC2", 940, 700, V="Vrefv")
    opamp(m, "OP_AMP1", 1010, 800)
    m.add("Resistor", "R14", 980, 890, "left", R="R14")
    m.add("Capacitor", "C5", 1040, 890, "left", C="C5", v_init="0")
    m.add("Capacitor", "C6", 1010, 950, "left", C="C6", v_init="0")
    m.add("Resistor", "R15", 1130, 860, R="Rpd")
    m.add("Resistor", "R7", 1190, 800, "left", R="R7")
    m.direct(("Hv_b", 1), ("R13", 1))
    m.direct(("VDC2", 1), ("OP_AMP1", 1), [(965, 680), (965, 790)])
    aterra(m, ("VDC2", 2), "G_VDC2")
    m.star(("R13", 2), [(950, 810)],
           [([], ("OP_AMP1", 2)), ([(950, 890)], ("R14", 1)), ([(950, 950)], ("C6", 1))])
    m.direct(("R14", 2), ("C5", 1))
    m.star(("OP_AMP1", 3), [(1090, 800)],
           [([(1090, 890)], ("C5", 2)), ([(1090, 950)], ("C6", 2)), ([(1130, 800)], ("R15", 1)),
            ([], ("R7", 1))])
    aterra(m, ("R15", 2), "G_R15")

    # ------------------------------------------------ nó da tensão de controle e modulador PWM
    m.add("Resistor", "R17", 1340, 860, R="Rpd")
    m.add_ref("DZ", ZENER, 1400, 860, T_ZENER, ((-10, -10), (10, 10)),
              [("Vz", "Vz"), ("Rz", "1"), ("Vf", "Vd"), ("Rf", "1")], direction="left",
              label="east")
    m.add("Voltmeter", "V9", 1460, 860)
    m.net([("R7", 2), ("D6", 1), ("R17", 1), ("DZ", 1), ("V9", 1)], rail=800)
    aterra(m, ("R17", 2), "G_R17")
    aterra(m, ("DZ", 2), "G_DZ")
    aterra(m, ("V9", 2), "G_V9")
    m.add("Comparator", "COMP3", 1580, 860, "right")
    m.add("TriangleGenerator", "VTRI1", 1500, 940, "right", Min="Vtri_min", Max="Vtri_max",
          f="fs", DutyCycle="0.5", Delay="0")
    m.signal(("V9", 3), ("COMP3", 1))
    m.signal(("VTRI1", 1), ("COMP3", 2))
    m.goto("G_pwm", 1660, 860, "pwm", ("COMP3", 3))

    # ------------------------------------------------ retorno do secundário e terra
    m.net([("T1", 4), ("D1", 1), ("Rsh", 1), ("R2", 1)], rail=N)
    m.net([("Rsh", 2), ("R3", 1), ("R5", 1), ("C4", 2), ("V11", 2), ("R6", 2), ("R9", 2),
           ("VDC3", 2), ("MOS6", 2), ("R19", 2), ("VDC1", 2), ("Vbat", 2), ("R12", 2),
           ("R20", 2), terra(m, "GND", 1090, 410)], rail=N)

    # ------------------------------------------------ comandos da carga
    m.add("PulseGenerator", "VSQ3", 1820, 100, "right", Hi="hab_carga", Lo="0", f="f_carga",
          DutyCycle="0.5", Delay="0")
    m.goto("G_carga", 1890, 100, "carga", ("VSQ3", 1))
    m.add("Constant", "Bateria", 1820, 170, "right", Value="hab_bat")
    m.goto("G_bat", 1890, 170, "bat", ("Bateria", 1))

    # ------------------------------------------------ medidas (porta de saída, lida por RPC)
    grupos = []                         # um bloco Probe{} por componente, sinais em ordem
    for _, comp, sinal in MEDIDAS:
        if grupos and grupos[-1][0] == comp:
            grupos[-1][1].append(sinal)
        else:
            grupos.append((comp, [sinal]))
    assert len({g[0] for g in grupos}) == len(grupos), "sinais do mesmo componente devem ser vizinhos"
    m.probe("Medidas", 1820, 260, grupos, show=True)
    m.add("Output", "Out", 1900, 260, "right", Index="1", Width="-1")
    m.signal(("Medidas", 1), ("Out", 1))

    # ------------------------------------------------ osciloscópios
    def osciloscopio(nome, y, eixos, probes):
        m.scope(nome, 1930, y, eixos)
        for k, (pn, itens) in enumerate(probes):
            m.probe(pn, 1820, y - 20 + 40 * k, itens)
            m.signal((pn, 1), (nome, k + 1))

    osciloscopio("Saida", 360, ["Vbat / V", "IL / A"],
                 [("P_vbat", [("Vbat", ["Measured voltage"])]),
                  ("P_iL", [("L2", ["Inductor current"])])])
    osciloscopio("Controle", 480, ["vc e portadora / V", "PWM"],
                 [("P_vc", [("V9", ["Measured voltage"]), ("VTRI1", ["Output"])]),
                  ("P_pwm", [("COMP3", ["Output"])])])
    osciloscopio("Retificador", 600, ["vC1 e v_rede / V", "i_rede / A"],
                 [("P_vC1", [("C1", ["Capacitor voltage"]), ("V1", ["Source voltage"])]),
                  ("P_irede", [("V1", ["Source current"])])])
    return m


def previa(m, destino):
    """Desenho aproximado do esquemático (confere o roteamento antes de abrir no PLECS)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(22, 11))
    for c in m.comps.values():
        cor = {"Ground": "0.5", "From": "g", "Goto": "g", "Label": "m"}.get(c["type"], "k")
        ax.plot(c["x"], c["y"], "s", ms=9, mfc="none", mec=cor)
        if c["show"]:
            ax.text(c["x"] + 8, c["y"] - 8, c["name"], fontsize=6, color="b")
    for k in m.conns:
        cor = "g" if k["kind"] == "Signal" else "k"
        p0 = m.term(*k["src"])[0]
        tr = [p0] + list(k["pts"])
        fim = tr[-1]
        if k["dst"] is not None:
            tr.append(m.term(*k["dst"])[0])
        ax.plot([p[0] for p in tr], [p[1] for p in tr], "-", color=cor, lw=0.7)
        for b in k["branches"]:
            br = [fim] + list(b["pts"]) + [m.term(*b["dst"])[0]]
            ax.plot([p[0] for p in br], [p[1] for p in br], "-", color=cor, lw=0.7)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(destino, dpi=110)


if __name__ == "__main__":
    m = carregador()
    problemas = m.check()
    destino = os.path.join(PASTA, m.name + ".plecs")
    m.write(destino, CABECALHO)
    print("%s: %d componentes, %d ligações -> %s" % (m.name, len(m.comps), len(m.conns),
                                                      os.path.basename(destino)))
    # a saída de sinal dos voltímetros lidos por Probe pode ficar aberta
    problemas = [p for p in problemas if not p.startswith(("V11 terminal 3", "Vbat terminal 3"))]
    for p in problemas:
        print("   PROBLEMA:", p)
    print("OK" if not problemas else "HÁ PROBLEMAS")
    if "--previa" in sys.argv:
        previa(m, os.path.join(AQUI, "previa_carregador.png"))
