"""Gera os quatro modelos PLECS do Trabalho 2 a partir do guia 07.

Uso (a partir desta pasta):   python gerar_modelos.py
Saída: forward.plecs, fullbridge.plecs, pushpull.plecs e flyback.plecs na
pasta "simulação PLECS". Cada arquivo contém o conversor isolado (em cima), o
equivalente não isolado (embaixo), os geradores de comando, o gerador de
degrau de carga, um Scope com as curvas sobrepostas e um bloco To File que
grava o CSV em "resultados PLECS".

Todos os valores entram por variáveis definidas nos comandos de
inicialização (Simulation > Simulation Parameters > Initialization).
"""
import os
from plecs_lib import Model

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.dirname(AQUI)
CABECALHO = os.path.join(AQUI, "cabecalho_plecs50.txt")
Y_EQ = 480  # deslocamento vertical do circuito equivalente


# ------------------------------------------------------------------ blocos comuns
def estagio_saida(m, suf, x0, yt, yb, cap="Co", esr="Rse", ground=True):
    """RSE + Co, voltímetro, amperímetro e cargas R20 // (R80 + chave).

    Retorna (terminais do barramento positivo, terminais do barramento
    negativo). O barramento positivo fica em y = yt e o negativo em y = yb.
    """
    ym = (yt + yb) // 2
    m.add("Resistor", "Rse" + suf, x0, yt + 60, R=esr)
    m.add("Capacitor", "Co" + suf, x0, yt + 140, C=cap, v_init="VC0")
    m.wire(("Rse" + suf, 2), ("Co" + suf, 1))
    m.add("Voltmeter", "Vm" + suf, x0 + 60, ym)
    m.goto("GVo" + suf, x0 + 130, ym, "Vo" + suf, ("Vm" + suf, 3))
    m.add("Ammeter", "Am" + suf, x0 + 140, yt, "left")
    m.goto("GIo" + suf, x0 + 175, yt - 40, "Io" + suf, ("Am" + suf, 3))
    m.add("Resistor", "R20" + suf, x0 + 190, ym, R="R20")
    m.add("Resistor", "R80" + suf, x0 + 300, yt + 60, R="R80")
    m.add("Switch", "Sc" + suf, x0 + 300, yt + 140)
    m.wire(("R80" + suf, 2), ("Sc" + suf, 1))
    m.from_("Fc" + suf, x0 + 230, yt + 140, "carga", ("Sc" + suf, 3))
    m.net([("Am" + suf, 2), ("R20" + suf, 1), ("R80" + suf, 1)], rail=yt)
    pos = [("Rse" + suf, 1), ("Vm" + suf, 1), ("Am" + suf, 1)]
    neg = [("Co" + suf, 2), ("Vm" + suf, 2), ("R20" + suf, 2), ("Sc" + suf, 2)]
    return pos, neg


def terra(m, nome, x, y):
    m.add("Ground", nome, x, y, show=False)
    return (nome, 1)


def gatilho(m, chave, tag):
    """From com o sinal de comando ligado ao gatilho de um MOSFET vertical."""
    c = m.comps[chave]
    m.from_("F" + chave, c["x"] - 80, c["y"] + 45, tag, (chave, 3))


def gerador(m, nome, x, y, tag, f, dc, atraso="0"):
    m.add("PulseGenerator", nome, x, y, "right", Hi="1", Lo="0", f=f, DutyCycle=dc,
          Delay=atraso)
    m.goto("G" + nome, x + 65, y, tag, (nome, 1))


def probe_corrente(m, nome, x, y, indutor, tag, ganho=None):
    m.probe(nome, x, y, indutor, ["Inductor current"])
    if ganho is None:
        m.goto("G" + nome, x + 60, y, tag, (nome, 1))
    else:
        m.add("Gain", "K" + nome, x + 60, y, "right", show=False, K=ganho)
        m.signal((nome, 1), ("K" + nome, 1))
        m.goto("G" + nome, x + 120, y, tag, ("K" + nome, 2))


def painel_medidas(m, x, y, arquivo, ts):
    """Scope com 3 gráficos (Vo, Io, IL: isolado x equivalente) e To File."""
    grupos = [("Vo", "Vo / V"), ("Io", "Io / A"), ("IL", "IL / A (secundário)")]
    m.scope("Scope", x + 230, y + 170, [g[1] for g in grupos])
    colunas = [x + 170, x + 155, x + 170]   # colunas de subida/descida sem sobreposição
    for k, (g, _) in enumerate(grupos):
        ym = y + 80 * k + 60 + (80 if k == 2 else 0)
        mux = m.mux("Mux" + g, x + 100, ym, 2)
        m.from_("F%s_iso" % g, x + 20, ym - 20, g + "_iso")
        m.from_("F%s_eq" % g, x + 20, ym + 20, g + "_eq")
        m.signal(("F%s_iso" % g, 1), (mux, 2))
        m.signal(("F%s_eq" % g, 1), (mux, 3))
        m.signal((mux, 1), ("Scope", k + 1), via=[(colunas[k], ym)])
    # To File: tempo + Vo_iso, Vo_eq, Io_iso, Io_eq, IL_iso, IL_eq
    yf = y + 440
    mux = m.mux("MuxArq", x + 100, yf, 6)
    col = [x + 65, x + 55, x + 45, x + 45, x + 55, x + 65]
    for k, tag in enumerate(["Vo_iso", "Vo_eq", "Io_iso", "Io_eq", "IL_iso", "IL_eq"]):
        yk = yf - 75 + 30 * k
        m.from_("Farq%d" % k, x, yk, tag)
        m.signal(("Farq%d" % k, 1), (mux, k + 2), via=[(col[k], yk)])
    m.add("ToFile", "ToFile", x + 180, yf, "right",
          Filename="'../resultados PLECS/%s'" % arquivo, FileType="1",
          WriteSignalNames="2", SampleTime=ts)
    m.signal((mux, 1), ("ToFile", 1))


def buck_equivalente(m, dy, x_mos=200):
    """Buck referido ao secundário (Forward e Full-bridge)."""
    y_pin, y_sw, y_gnd = 100 + dy, 180 + dy, 380 + dy
    m.add("DCVoltageSource", "Vi_eq", 40, 280 + dy, V="Vi_eq")
    m.add("MosfetWithDiode", "S_eq", x_mos, y_sw - 40)
    gatilho(m, "S_eq", "g_eq")
    m.add("Diode", "D_eq", 300, 280 + dy, "down")
    m.add("Inductor", "L_eq", 380, y_sw, "left", L="L_eq", i_init="IL_eq0")
    probe_corrente(m, "P_Leq", 360, y_sw - 60, "L_eq", "IL_eq")
    pos, neg = estagio_saida(m, "_eq", 460, y_sw, y_gnd)
    m.net([("Vi_eq", 1), ("S_eq", 1)], rail=y_pin)
    m.net([("S_eq", 2), ("D_eq", 2), ("L_eq", 1)], rail=y_sw)
    m.net([("L_eq", 2)] + pos, rail=y_sw)
    m.net([("Vi_eq", 2), ("D_eq", 1)] + neg + [terra(m, "Gnd_eq", 350, y_gnd + 30)], rail=y_gnd)


# ------------------------------------------------------------------ Forward
INIT_FORWARD = """% ---- Forward de uma chave (enunciado, seção 1.3)
Po = 500;  Vi = 200;  Vo = 54;  fs = 20e3;  D = 0.4;
n  = Vo/(Vi*D);            % 0.675 = Ns/Np
Np = 100;  Ns = 68;  Nt = 100;   % espiras usadas pelo professor
Lo  = 1080e-6;
Co  = 34.72e-6;  Rse = 0.18;
Lm  = 13e-3;               % magnetizante, referida ao primário
Ro  = Vo^2/Po;
R20 = 5*Ro;  R80 = 1.25*Ro;
f_carga = 10;              % degraus: 0.05 s (100->20 %) e 0.10 s (20->100 %)
% ---- Buck equivalente, referido ao secundário
Vi_eq = Vi*Ns/Np;          % 136 V com 100:68 (135 V com n exato)
L_eq = Lo;  fs_eq = fs;  D_eq = D;
% ---- condições iniciais (regime a 100 %)
IL0 = Po/Vo;  IL_eq0 = IL0;  VC0 = Vo;
"""


def forward():
    m = Model("forward", "0.11", "1e-6", init_cmds=INIT_FORWARD)
    # primário
    m.add("DCVoltageSource", "Vi", 40, 260, V="Vi")
    m.add("Transformer", "T_ter", 170, 200, "right", "on", Windings="[1 1]",
          n="[Np -Nt]", Polarity="+", Lm="inf", im0="0")
    m.add("Diode", "Dt", 230, 320, "down")
    m.add("Inductor", "Lm", 280, 200, L="Lm", i_init="0")
    m.add("Transformer", "T_sec", 370, 200, "right", "on", Windings="[1 1]",
          n="[Np Ns]", Polarity="+", Lm="inf", im0="0")
    m.add("MosfetWithDiode", "S1", 360, 310)
    gatilho(m, "S1", "g_S1")
    m.net([("Vi", 1), ("T_ter", 1), ("T_ter", 3), ("Lm", 1), ("T_sec", 1)], rail=100)
    m.net([("T_ter", 2), ("Lm", 2), ("T_sec", 2), ("S1", 1)], rail=260)
    m.wire(("T_ter", 4), ("Dt", 2))
    m.net([("Vi", 2), ("Dt", 1), ("S1", 2), terra(m, "Gnd_p", 150, 440)], rail=420)
    # secundário
    m.add("Diode", "D1", 440, 180, "left")
    m.add("Diode", "D2", 500, 270, "down")
    m.add("Inductor", "Lo", 580, 180, "left", L="Lo", i_init="IL0")
    probe_corrente(m, "P_Lo", 560, 120, "Lo", "IL_iso")
    pos, neg = estagio_saida(m, "_iso", 660, 180, 380)
    m.wire(("T_sec", 3), ("D1", 1))
    m.net([("D1", 2), ("D2", 2), ("Lo", 1)], rail=180)
    m.net([("Lo", 2)] + pos, rail=180)
    m.net([("T_sec", 4), ("D2", 1)] + neg + [terra(m, "Gnd_s", 550, 410)], rail=380)
    # equivalente
    buck_equivalente(m, Y_EQ)
    # comando e medidas
    gerador(m, "PG_S1", 1120, 100, "g_S1", "fs", "D")
    gerador(m, "PG_eq", 1120, 160, "g_eq", "fs_eq", "D_eq")
    gerador(m, "PG_carga", 1120, 220, "carga", "f_carga", "0.5")
    painel_medidas(m, 1100, 300, "forward_degrau", "2e-6")
    return m


# ------------------------------------------------------------------ Full-bridge
INIT_FULLBRIDGE = """% ---- Ponte completa (enunciado, seção 2.3)
Po = 5000;  Vi = 400;  Vo = 54;  fs = 20e3;  D = 0.4;
a  = Vo/(Vi*2*D);          % 0.16875 = Ns/Np
Np = 100;  Ns = Np*a;      % o professor usou 17
Lo  = 14.58e-6;
Co  = 214.4e-6;  Rse = 0.015;     % Rse = Rc do enunciado
Lm  = 2.6e-3;              % valor do enunciado (ver divergência 1 do doc 00)
Ro  = Vo^2/Po;
R20 = 5*Ro;  R80 = 1.25*Ro;
f_carga = 5;               % degraus: 0.1/0.3 s (100->20 %) e 0.2 s (20->100 %)
% ---- Buck equivalente
Vi_eq = a*Vi;  L_eq = Lo;  fs_eq = 2*fs;  D_eq = 2*D;
% ---- condições iniciais (regime a 100 %)
IL0 = Po/Vo;  IL_eq0 = IL0;  VC0 = Vo;
"""


def fullbridge():
    m = Model("fullbridge", "0.31", "5e-7", init_cmds=INIT_FULLBRIDGE)
    m.add("DCVoltageSource", "Vi", 40, 260, V="Vi")
    m.add("MosfetWithDiode", "S1", 200, 180)
    m.add("MosfetWithDiode", "S4", 200, 340)
    m.add("MosfetWithDiode", "S3", 300, 180)
    m.add("MosfetWithDiode", "S2", 300, 340)
    for s in ("S1", "S2", "S3", "S4"):
        gatilho(m, s, "g_" + s)
    m.add("Transformer", "Tr", 410, 260, "right", "on", Windings="[1 1]",
          n="[Np Ns]", Polarity="+", Lm="Lm", im0="0")
    m.net([("Vi", 1), ("S1", 1), ("S3", 1)], rail=100)
    m.net([("Vi", 2), ("S4", 2), ("S2", 2), terra(m, "Gnd_p", 130, 450)], rail=420)
    m.net([("S1", 2), ("S4", 1), ("Tr", 1)], rail=200, axis="v")
    m.net([("S3", 2), ("S2", 1), ("Tr", 2)], rail=300, axis="v")
    # retificador em ponte e filtro
    m.add("Diode", "D1", 500, 200, "down")
    m.add("Diode", "D4", 500, 340, "down")
    m.add("Diode", "D3", 560, 200, "down")
    m.add("Diode", "D2", 560, 340, "down")
    m.net([("Tr", 3), ("D1", 1), ("D4", 2)], rail=500, axis="v")
    m.net([("Tr", 4), ("D3", 1), ("D2", 2)], rail=560, axis="v")
    m.add("Inductor", "Lo", 640, 160, "left", L="Lo", i_init="IL0")
    probe_corrente(m, "P_Lo", 620, 110, "Lo", "IL_iso")
    pos, neg = estagio_saida(m, "_iso", 720, 160, 400)
    m.net([("D1", 2), ("D3", 2), ("Lo", 1)], rail=160)
    m.net([("Lo", 2)] + pos, rail=160)
    m.net([("D4", 1), ("D2", 1)] + neg + [terra(m, "Gnd_s", 620, 430)], rail=400)
    buck_equivalente(m, Y_EQ + 40)
    # comando (variante B do guia: braços complementares)
    gerador(m, "PG_A", 1180, 100, "g_S1", "fs", "D")
    gerador(m, "PG_B", 1180, 200, "g_S3", "fs", "D", "1/(2*fs)")
    m.add("LogicalOperator", "NOT_A", 1180, 150, show=False, Operator="6", Inputs="1")
    m.add("LogicalOperator", "NOT_B", 1180, 250, show=False, Operator="6", Inputs="1")
    m.from_("F_notA", 1120, 150, "g_S1", ("NOT_A", 2))
    m.from_("F_notB", 1120, 250, "g_S3", ("NOT_B", 2))
    m.goto("G_S4", 1240, 150, "g_S4", ("NOT_A", 1))
    m.goto("G_S2", 1240, 250, "g_S2", ("NOT_B", 1))
    gerador(m, "PG_eq", 1180, 300, "g_eq", "fs_eq", "D_eq")
    gerador(m, "PG_carga", 1180, 350, "carga", "f_carga", "0.5")
    painel_medidas(m, 1160, 420, "fullbridge_degrau", "1e-6")
    return m


# ------------------------------------------------------------------ Push-pull
INIT_PUSHPULL = """% ---- Push-pull alimentado em corrente (enunciado, seção 3.3)
Po = 1000;  Vi = 54;  Vo = 400;  fs = 20e3;  D = 0.7;
a  = Vo/Vi*2*(1-D);        % 4.444 = Ns/Np (Np = cada metade do primário)
Np = 22.5;  Ns = 100;
Li  = 146e-6;
Co  = 6.25e-6;  Rse = 0.873;      % Rse = Rc do enunciado
Lm  = 200e-3;              % referida ao secundário (100 espiras), como no PSIM
Lm_p = Lm*(Np/Ns)^2;       % a mesma, referida a meio primário
Ro  = Vo^2/Po;
R20 = 5*Ro;  R80 = 1.25*Ro;
f_carga = 2;               % degraus: 0.75/1.25 s (100->20 %) e 1.0 s (20->100 %)
% ---- Boost equivalente
Vi_eq = a*Vi;  L_eq = a^2*Li;  fs_eq = 2*fs;  D_eq = 2*D-1;
% ---- condições iniciais (regime a 100 %)
ILi0 = Po/Vi;  IL_eq0 = ILi0/a;  VC0 = Vo;
"""


def pushpull():
    m = Model("pushpull", "1.3", "5e-7", init_cmds=INIT_PUSHPULL)
    m.add("DCVoltageSource", "Vi", 40, 260, V="Vi")
    m.add("Inductor", "Li", 130, 100, "left", L="Li", i_init="ILi0")
    probe_corrente(m, "P_Li", 110, 40, "Li", "IL_iso", ganho="1/a")
    # primário com derivação central = dois transformadores ideais com os
    # secundários em paralelo (equivale a um transformador de 3 enrolamentos)
    m.add("Transformer", "TA", 280, 200, "right", "on", Windings="[1 1]",
          n="[Np Ns]", Polarity="+", Lm="Lm_p", im0="0")
    m.add("Transformer", "TB", 280, 300, "right", "on", Windings="[1 1]",
          n="[Np Ns]", Polarity="+", Lm="inf", im0="0")
    m.add("MosfetWithDiode", "S2", 170, 380)
    m.add("MosfetWithDiode", "S1", 350, 380)
    gatilho(m, "S1", "g_S1")
    gatilho(m, "S2", "g_S2")
    m.wire(("Vi", 1), ("Li", 1))
    m.net([("Li", 2), ("TA", 2), ("TB", 1)], rail=230, axis="v")
    m.wire(("TA", 1), ("S2", 1))
    m.wire(("TB", 2), ("S1", 1), via=[(250, 340)])
    m.net([("Vi", 2), ("S2", 2), ("S1", 2), terra(m, "Gnd_p", 260, 470)], rail=440)
    # secundário: ponte de diodos
    m.add("Diode", "D1", 420, 140, "down")
    m.add("Diode", "D4", 420, 420, "down")
    m.add("Diode", "D3", 480, 140, "down")
    m.add("Diode", "D2", 480, 420, "down")
    m.net([("TA", 3), ("TB", 3), ("D1", 1), ("D4", 2)], rail=420, axis="v")
    m.net([("TA", 4), ("TB", 4), ("D3", 1), ("D2", 2)], rail=480, axis="v")
    pos, neg = estagio_saida(m, "_iso", 560, 100, 460)
    m.net([("D1", 2), ("D3", 2)] + pos, rail=100)
    m.net([("D4", 1), ("D2", 1)] + neg + [terra(m, "Gnd_s", 540, 490)], rail=460)
    # Boost equivalente
    dy = Y_EQ + 80
    m.add("DCVoltageSource", "Vi_eq", 40, 280 + dy, V="Vi_eq")
    m.add("Inductor", "L_eq", 130, 180 + dy, "left", L="L_eq", i_init="IL_eq0")
    probe_corrente(m, "P_Leq", 110, 120 + dy, "L_eq", "IL_eq")
    m.add("MosfetWithDiode", "S_eq", 230, 270 + dy)
    gatilho(m, "S_eq", "g_eq")
    m.add("Diode", "D_eq", 300, 180 + dy, "left")
    pos, neg = estagio_saida(m, "_eq", 400, 180 + dy, 380 + dy)
    m.wire(("Vi_eq", 1), ("L_eq", 1))
    m.net([("L_eq", 2), ("S_eq", 1), ("D_eq", 1)], rail=180 + dy)
    m.net([("D_eq", 2)] + pos, rail=180 + dy)
    m.net([("Vi_eq", 2), ("S_eq", 2)] + neg + [terra(m, "Gnd_eq", 330, 410 + dy)], rail=380 + dy)
    gerador(m, "PG_S1", 1080, 100, "g_S1", "fs", "D")
    gerador(m, "PG_S2", 1080, 160, "g_S2", "fs", "D", "1/(2*fs)")
    gerador(m, "PG_eq", 1080, 220, "g_eq", "fs_eq", "D_eq")
    gerador(m, "PG_carga", 1080, 280, "carga", "f_carga", "0.5")
    painel_medidas(m, 1060, 360, "pushpull_degrau", "1e-6")
    return m


# ------------------------------------------------------------------ Flyback
INIT_FLYBACK = """% ---- Flyback de uma chave (enunciado, seção 4.3)
Po = 200;  Vi = 200;  Vo = 54;  fs = 20e3;  D = 0.4;
a  = Vo/Vi*(1-D)/D;        % 0.405 = Ns/Np
Np = 100;  Ns = 40.5;
Lcrit = Vi^2*D^2/(2*fs*Po);       % 800e-6, fronteira MCD/MCC
kL = 1;                    % 1 -> MCD (720 uH); 10 -> MCC (7200 uH)
Lm  = 0.9*Lcrit*kL;        % referida ao primário
Co  = 137.2e-6;  Rse = 0.044;
Ro  = Vo^2/Po;
R20 = 5*Ro;  R80 = 1.25*Ro;
f_carga = 2;               % degraus: 0.75 s (100->20 %) e 0.5 s (20->100 %)
% ---- Buck-Boost equivalente
Vi_eq = a*Vi;  L_eq = a^2*Lm;  fs_eq = fs;  D_eq = D;
% ---- condições iniciais
VC0 = Vo;
ILm0 = (kL>1)*a*(Po/Vo)/(1-D);    % MCC: 2.5 A; MCD: 0
IL_eq0 = ILm0/a;
arquivo_saida = 'flyback_mcd_degrau';  if kL>1, arquivo_saida = 'flyback_mcc_degrau'; end
"""


def flyback():
    m = Model("flyback", "0.8", "1e-6", init_cmds=INIT_FLYBACK)
    m.add("DCVoltageSource", "Vi", 40, 260, V="Vi")
    m.add("Inductor", "Lm", 150, 200, L="Lm", i_init="ILm0")
    probe_corrente(m, "P_Lm", 110, 40, "Lm", "IL_iso", ganho="1/a")
    # espiras negativas no secundário invertem a polaridade (flyback)
    m.add("Transformer", "Tr", 250, 200, "right", "on", Windings="[1 1]",
          n="[Np -Ns]", Polarity="+", Lm="inf", im0="0")
    m.add("MosfetWithDiode", "S1", 240, 310)
    gatilho(m, "S1", "g_S1")
    m.net([("Vi", 1), ("Lm", 1), ("Tr", 1)], rail=100)
    m.net([("Lm", 2), ("Tr", 2), ("S1", 1)], rail=260)
    m.net([("Vi", 2), ("S1", 2), terra(m, "Gnd_p", 120, 440)], rail=420)
    m.add("Diode", "D1", 320, 180, "left")
    pos, neg = estagio_saida(m, "_iso", 420, 180, 380)
    m.wire(("Tr", 3), ("D1", 1))
    m.net([("D1", 2)] + pos, rail=180)
    m.net([("Tr", 4)] + neg + [terra(m, "Gnd_s", 380, 410)], rail=380)
    # Buck-Boost equivalente: a saída é negativa em relação ao terra; o
    # barramento "positivo" do estágio de saída é o próprio terra, e o
    # voltímetro lê +Vo.
    dy = Y_EQ
    m.add("DCVoltageSource", "Vi_eq", 40, 280 + dy, V="Vi_eq")
    m.add("MosfetWithDiode", "S_eq", 140, 160 + dy)
    gatilho(m, "S_eq", "g_eq")
    m.add("Inductor", "L_eq", 230, 280 + dy, L="L_eq", i_init="IL_eq0")
    probe_corrente(m, "P_Leq", 250, 120 + dy, "L_eq", "IL_eq")
    m.add("Diode", "D_eq", 300, 200 + dy, "right")
    pos, neg = estagio_saida(m, "_eq", 420, 80 + dy, 360 + dy)
    m.net([("Vi_eq", 1), ("S_eq", 1)], rail=100 + dy)
    m.net([("S_eq", 2), ("L_eq", 1), ("D_eq", 2)], rail=200 + dy)
    m.net([("Vi_eq", 2), ("L_eq", 2), terra(m, "Gnd_eq1", 150, 430 + dy)], rail=400 + dy)
    m.net(pos + [terra(m, "Gnd_eq2", 380, 110 + dy)], rail=80 + dy)
    m.net([("D_eq", 1)] + neg, rail=360 + dy)
    gerador(m, "PG_S1", 1060, 100, "g_S1", "fs", "D")
    gerador(m, "PG_eq", 1060, 160, "g_eq", "fs_eq", "D_eq")
    gerador(m, "PG_carga", 1060, 220, "carga", "f_carga", "0.5")
    painel_medidas(m, 1040, 300, "flyback_degrau", "2e-6")
    # nome do arquivo depende de kL
    m.comps["ToFile"]["params"]["Filename"] = "['../resultados PLECS/' arquivo_saida]"
    return m


if __name__ == "__main__":
    ok = True
    for fab in (forward, fullbridge, pushpull, flyback):
        m = fab()
        prob = m.check()
        destino = os.path.join(PASTA, m.name + ".plecs")
        m.write(destino, CABECALHO)
        print("%-12s %3d componentes, %3d ligações -> %s" % (
            m.name, len(m.comps), len(m.conns), os.path.basename(destino)))
        for p in prob:
            ok = False
            print("   PROBLEMA:", p)
    print("OK" if ok else "HÁ PROBLEMAS")
