"""Trabalho 6 - No-break de dupla conversao monofasico de 3 kVA.

Reconstrucao analitica da planilha do professor, auditoria dos valores impressos e
calculos complementares (pontos de operacao, Bodes, esforcos e CC-CC).
Este script NAO simula a dinamica dos conversores: todas as curvas aqui sao
expressoes analiticas avaliadas em frequencia ou em funcao de parametros.
Saidas: calculos/parametros.json (fonte numerica unica), calculos/auditoria.csv,
calculos/bode_*.csv, calculos/figuras/*.png|pdf e calculos/execucao_calculos.txt.
Uso: python desenvolvimento/calculos.py
"""
from pathlib import Path
import json, math, csv, sys, platform, datetime
import numpy as np
from numpy import pi, sqrt
from scipy.optimize import brentq
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker

DEV = Path(__file__).resolve().parent
OUT = DEV / 'calculos'
FIG = OUT / 'figuras'
FIG.mkdir(parents=True, exist_ok=True)
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print(s)


def r(x, n=6):
    """Arredonda para o JSON sem perder a rastreabilidade."""
    if isinstance(x, (float, np.floating)):
        if not np.isfinite(x):
            return None if np.isnan(x) else ('inf' if x > 0 else '-inf')
        return float(f'{x:.{n}g}')
    return x


# ---------------------------------------------------------------------------
# 1. Especificacoes (secao 2 da planilha, pagina 2)
# ---------------------------------------------------------------------------
E = dict(Vinomef=220.0, Vimaxef=264.0, Viminef=176.0, fr=60.0,
         Voef=115.0, Po=2100.0, So=3000.0, fo=60.0)
E['FP_carga'] = E['Po'] / E['So']
eta_inv = 0.933                      # usado apenas como orcamento de potencia
AUD = []                             # linhas da auditoria


def aud(local, item, impresso, recalculado, decisao, justificativa, unidade=''):
    if isinstance(impresso, (int, float)) and isinstance(recalculado, (int, float)) and impresso not in (0,):
        desvio = (recalculado - impresso) / abs(impresso) * 100
    else:
        desvio = None
    AUD.append(dict(local=local, item=item, unidade=unidade, impresso=impresso,
                    recalculado=r(recalculado, 6) if isinstance(recalculado, float) else recalculado,
                    desvio_pct=r(desvio, 3) if desvio is not None else None,
                    decisao=decisao, justificativa=justificativa))


# ---------------------------------------------------------------------------
# 2. Retificador com filtro capacitivo (secao 3, paginas 3 a 7)
# ---------------------------------------------------------------------------
def retificador_ideal(Vrms, P, dV=None, frac=None, fr=60.0):
    Vmax = sqrt(2) * Vrms
    if dV is None:
        dV = frac * Vmax
    Vmin = Vmax - dV
    th = pi / 2 - math.asin(Vmin / Vmax)
    C = P * (pi - th) / (pi * fr * (Vmax ** 2 - Vmin ** 2))
    tc = th / (2 * pi * fr)
    Vmed = (Vmax + Vmin) / 2
    Io = P / Vmed
    Roeq = Vmed ** 2 / P
    Ichg = Io * pi / th
    IC = sqrt((quad(lambda x: (Ichg - Io) ** 2, 0, th)[0] + quad(lambda x: Io ** 2, 0, pi - th)[0]) / pi)
    IDmed = Ichg * th / (2 * pi)
    IDef = sqrt(Ichg ** 2 * th / (2 * pi))
    return dict(Vrms=Vrms, P=P, VC1max=Vmax, dVC=dV, VC1min=Vmin, thetaC1_rad=th, C1_F=C, tC1_s=tc,
                VC1medio=Vmed, Ioeq=Io, Roeq=Roeq, Ichg=Ichg, IC1ef=IC, ID1med=IDmed, ID1ef=IDef,
                ID1pk_2Ichg=2 * Ichg)


def vale_com_C(Vrms, P, C, fr=60.0):
    """Vale do barramento para C dado, mesma hipotese da planilha (descarga a potencia constante)."""
    Vmax = sqrt(2) * Vrms
    f = lambda Vmin: C * (Vmax ** 2 - Vmin ** 2) - P * (pi - math.acos(Vmin / Vmax)) / (pi * fr)
    Vmin = brentq(f, 1e-3 * Vmax, Vmax * (1 - 1e-9))
    return Vmin


Prec = 2250.0
ret = retificador_ideal(E['Viminef'], Prec, dV=37.33)
ret_15 = retificador_ideal(E['Viminef'], Prec, frac=0.15)
ret_10 = retificador_ideal(E['Viminef'], Prec, frac=0.10)
C1_adot = 4 * 470e-6
Rse_C1 = 0.05
VDrrevpk = E['Vimaxef'] * sqrt(2)
Vimin_cc = ret['VC1min']
Vimax_cc = sqrt(2) * E['Vimaxef']
vales = {}
for V in (176.0, 220.0, 264.0):
    Vmin = vale_com_C(V, Prec, C1_adot)
    vales[str(int(V))] = dict(Vpico=sqrt(2) * V, Vvale=Vmin, ondulacao=sqrt(2) * V - Vmin,
                              ondulacao_pct=(1 - Vmin / (sqrt(2) * V)) * 100)
vale_tol = vale_com_C(176.0, Prec, 0.8 * C1_adot)
log('Retificador (176 V, 2250 W, dV=37,33 V):', {k: r(v) for k, v in ret.items()})
log('Vales com 1880 uF:', {k: {a: r(b) for a, b in v.items()} for k, v in vales.items()})
log('Vale com 1880 uF -20% (1504 uF) a 176 V:', r(vale_tol))

aud('p.3, sec. 3.1', 'Prec = Po/0,933', 2250, E['Po'] / eta_inv, 'Mantido',
    '2100/0,933 = 2250,8 W; arredondamento aceito. O rendimento e orcamento de potencia, nao medicao.', 'W')
aud('p.3, sec. 3.2', 'Ondulacao dVC (texto: 10% do pico)', 37.33, 0.10 * sqrt(2) * 176, 'Mantido 37,33 V (15%)',
    'O valor usado e 0,15*1,4142*176 = 37,33 V, isto e 15%; 10% daria 24,89 V. O texto esta inconsistente, o numero e coerente com todo o restante.', 'V')
aud('p.4', 'VC1max = raiz(2)*176', 248.902, ret['VC1max'], 'Mantido', 'Confere.', 'V')
aud('p.4', 'VC1min', 211.572, ret['VC1min'], 'Mantido', 'Confere.', 'V')
aud('p.4', 'thetaC1 = pi/2 - asin(VC1min/VC1max)', 0.555, ret['thetaC1_rad'], 'Mantido', 'Confere (= acos 0,85).', 'rad')
aud('p.5', 'C1 = Prec(pi-theta)/(pi fr (Vmax^2-Vmin^2))', 1.796e-3, ret['C1_F'], 'Mantido; adotado 4x470 uF = 1880 uF',
    'Confere. 1880 uF supera 1796 uF em 4,7%%; com tolerancia de -20%% (1504 uF) o vale cai para %.1f V.' % vale_tol, 'F')
aud('p.5', 'tC1', 1.472e-3, ret['tC1_s'], 'Mantido', 'Confere.', 's')
aud('p.5', 'VC1medio', 230.237, ret['VC1medio'], 'Mantido', 'Confere.', 'V')
aud('p.5', 'Ioeq', 9.773, ret['Ioeq'], 'Mantido', 'Confere.', 'A')
aud('p.5', 'Roeq', 23.56, ret['Roeq'], 'Mantido', 'Confere; a unidade impressa [W] deve ser ohm.', 'ohm')
aud('p.5', 'Ichg = Ioeq*pi/theta', 55.341, ret['Ichg'], 'Mantido como aproximacao',
    'Confere; pulso retangular sem impedancia de rede. O PLECS mede o pulso real com 0,1 ohm.', 'A')
aud('p.5', 'IC1ef', 21.103, ret['IC1ef'], 'Mantido', 'Confere a integral do pulso retangular.', 'A')
aud('p.6', 'ID1med', 4.886, ret['ID1med'], 'Mantido', 'Confere.', 'A')
aud('p.6', 'ID1ef', 16.444, ret['ID1ef'], 'Mantido', 'Confere.', 'A')
aud('p.6', 'ID1pk = 2*Ichg', 110.681, ret['ID1pk_2Ichg'], 'Mantido como estimativa',
    'Fator 2 e heuristico sobre o pulso retangular; comparado com o pico medido no PLECS.', 'A')
aud('p.6', 'VDrrevpk = raiz(2)*264', 373.352, VDrrevpk, 'Mantido', 'Confere.', 'V')

# ---------------------------------------------------------------------------
# 3. Inversor em ponte completa unipolar (secao 4, paginas 7 a 9)
# ---------------------------------------------------------------------------
fs = 20e3
Vopk = sqrt(2) * E['Voef']
Ioef = E['Po'] / E['Voef']
Iopk = sqrt(2) * Ioef
dILo = 0.4 * Iopk
Vcc_max_inv = 373.0                    # valor da secao 4.1
Vcc_min_inv = 223.0                    # valor da secao 4.1 (rotulado tensao eficaz nominal)
Mmax_223 = Vopk / Vcc_min_inv
Mmin = Vopk / Vcc_max_inv
Lo = (Vcc_max_inv - Vopk) * 0.5 * (1 + Mmin) / (2 * fs * dILo)
Lo_adot = 365.6e-6
Co_fs20 = (20 / (2 * pi * fs)) ** 2 / Lo
Co_fs40 = (40 / (2 * pi * fs)) ** 2 / Lo
Co = 60e-6
ESR_Co = 5e-3
Ro = E['Voef'] ** 2 / E['Po']
f0 = 1 / (2 * pi * sqrt(Lo_adot * Co))
Z0 = sqrt(Lo_adot / Co)


def ripple_unipolar(Vcc, vo, L=Lo_adot, f=fs):
    """Ondulacao pico a pico no indutor (modulacao unipolar, intervalo vAB = Vcc de m/(2fs))."""
    m = vo / Vcc
    return (Vcc - vo) * m / (2 * f * L)


def ripple_max(Vcc, L=Lo_adot, f=fs):
    vo = min(Vopk, Vcc / 2)
    return ripple_unipolar(Vcc, vo, L, f), vo


pontos_bus = {'373,35 V (pico a 264 V)': Vimax_cc, '373 V (planilha)': 373.0, '248,9 V (pico a 176 V)': ret['VC1max'],
              '230,2 V (media a 176 V)': ret['VC1medio'], '223 V (planilha)': 223.0,
              '211,57 V (vale a 176 V)': ret['VC1min'], '210 V (saida do CC-CC)': 210.0}
indices = {k: dict(Vcc=v, M_pico=Vopk / v) for k, v in pontos_bus.items()}
ripples = {k: dict(zip(('dILo_max_App', 'vo_no_max_V'), ripple_max(v))) for k, v in pontos_bus.items()}
dILo_planilha_Vcc373 = ripple_unipolar(373.0, Vopk)
log('Inversor: Lo=%.4e H, Co(fs/20)=%.4e, Co(fs/40)=%.4e, f0=%.1f Hz' % (Lo, Co_fs20, Co_fs40, f0))
log('Ondulacao real no pico a 373 V: %.3f A (projeto 10,33 A)' % dILo_planilha_Vcc373)

aud('p.7, sec. 4.1', 'Vimin_cc = 223 V (rotulado tensao eficaz nominal)', 223, Vimin_cc, 'Revisado para analise: 211,57 V em rede e 210 V em bateria',
    '223 V nao e deduzido no documento e nao e eficaz; e grandeza CC entre o vale (211,57 V) e a media (230,24 V) a 176 V.', 'V')
aud('p.7', 'Mmax = Vopk/223', 0.729, Mmax_223, 'Complementado', 'Com 211,57 V: %.3f; com 210 V: %.3f. Ambos < 0,85.' % (Vopk / Vimin_cc, Vopk / 210), '')
aud('p.7', 'Mmin = Vopk/373', 0.436, Mmin, 'Mantido', 'Confere.', '')
aud('p.7', 'dILo = 0,4*Iopk', 10.33, dILo, 'Mantido como criterio', 'Confere.', 'A')
aud('p.8, sec. 4.3', 'Lo [Rashid]', 3.656e-4, Lo, 'Mantido 365,6 uH',
    'A conta confere, mas usa dt = 0,5(1+M)/(2fs). Na unipolar o intervalo com vAB = Vcc no pico dura M/(2fs); a ondulacao real a 373 V e %.2f A (%.0f%% de Iopk), logo o projeto e conservador.' % (dILo_planilha_Vcc373, 100 * dILo_planilha_Vcc373 / Iopk), 'H')
aud('p.8, sec. 4.4', 'Co (texto fs/40, conta fs/20)', 69.294e-6, Co_fs20, 'Mantido 60 uF; texto corrigido para fs/20',
    'fc = 2fs/4 e corte = fc/10 levam a 2fs/40 = fs/20 = 1 kHz, que e o que a conta usa. Com fs/40 seria %.0f uF. Com 60 uF, f0 = %.0f Hz.' % (Co_fs40 * 1e6, f0), 'F')
aud('p.8, sec. 4.5', 'Ro = Voef^2/Po', 6.298, Ro, 'Mantido', 'Confere; unidade impressa [W] deve ser ohm.', 'ohm')

# Cargas e esforcos ---------------------------------------------------------
Vbus_max = Vimax_cc


def ripple_rms(Vcc, L=Lo_adot, f=fs):
    """Valor eficaz da ondulacao triangular ao longo de meio ciclo de 60 Hz."""
    th = np.linspace(0, pi, 2001)
    d = ripple_unipolar(Vcc, Vopk * np.sin(th) + 1e-12, L, f)
    return float(np.sqrt(np.mean(d ** 2) / 12))


I_Co_60 = E['Voef'] * 2 * pi * E['fo'] * Co
dI_pk373 = ripples['373,35 V (pico a 264 V)']['dILo_max_App']
Irip_rms373 = ripple_rms(Vbus_max)


def esforcos(nome, Io_fasor, nl=None, Vbus=Vbus_max):
    """A ponte conduz iLo = io + iCo (fasores de 60 Hz). Corrente eficaz por interruptor
    (MOSFET + diodo) = ILo/raiz(2) na ponte unipolar. nl = (pico, eficaz) para carga nao linear."""
    ILo = Io_fasor + 1j * I_Co_60
    ILo_rms = math.sqrt(abs(ILo) ** 2 + Irip_rms373 ** 2)
    if nl is None:
        Irms, Ipk = abs(Io_fasor), math.sqrt(2) * abs(Io_fasor)
        ILo_pk = math.sqrt(2) * abs(ILo) + dI_pk373 / 2
    else:
        Ipk, Irms = nl
        ILo_pk = Ipk + dI_pk373 / 2
    return dict(carga=nome, Io_rms_A=Irms, Io_pk_A=Ipk, fator_crista=Ipk / Irms, ILo_rms_A=ILo_rms, ILo_pk_A=ILo_pk,
                I_chave_rms_A=ILo_rms / sqrt(2), I_chave_pk_A=ILo_pk, V_chave_max_V=Vbus)


S3k = E['So']
Z3k = E['Voef'] ** 2 / S3k
R3k = Z3k * E['FP_carga']
X3k = Z3k * sqrt(1 - E['FP_carga'] ** 2)
L3k = X3k / (2 * pi * E['fo'])
Irms3k = S3k / E['Voef']
# carga nao linear de referencia da IEC 62040-3 (anexo E): Rs = 0,04 U^2/S, Uc = 1,22 U,
# R1 = Uc^2/(0,66 S), C = 7,5/(f R1). Usada apenas como referencia de comparacao.
iec = dict(Rs=0.04 * E['Voef'] ** 2 / S3k, Uc=1.22 * E['Voef'])
iec['R1'] = iec['Uc'] ** 2 / (0.66 * S3k)
iec['C'] = 7.5 / (E['fo'] * iec['R1'])
iec['P_R1'] = iec['Uc'] ** 2 / iec['R1']
anexo_nl = dict(Rs=0.2, C=1880e-6, ESR=0.05, R=9.5)
anexo_nl['P_R_com_Uc_IEC'] = iec['Uc'] ** 2 / anexo_nl['R']
anexo_nl['tau_RC_ms'] = anexo_nl['R'] * anexo_nl['C'] * 1e3
Io_rl = Irms3k * complex(E['FP_carga'], -sqrt(1 - E['FP_carga'] ** 2))
cargas = [esforcos('Resistiva 2100 W', complex(Ioef, 0)),
          esforcos('Linear 3 kVA, FP 0,7 indutivo', Io_rl),
          esforcos('Nao linear 3 kVA (FC = 3, referencia)', complex(Irms3k, 0), nl=(3 * Irms3k, Irms3k))]
log('Carga 3 kVA FP 0,7: R=%.3f ohm, L=%.3f mH' % (R3k, L3k * 1e3))
log('IEC 62040-3 referencia 3 kVA/115 V:', {k: r(v) for k, v in iec.items()})

# ---------------------------------------------------------------------------
# 4. Malha de tensao (secao 4.5, paginas 9 a 15)
# ---------------------------------------------------------------------------
Vref_pk = 4.0
Hv = Vref_pk / (sqrt(2) * E['Voef'])
Hv_divisor = 25.22e3 / (1000e3 + 25.22e3)
Vd = 5.0
fcv = 2 * fs / 6


def Gplanta(s, Vcc, R=Ro, L=Lo_adot, C=Co, esr=0.0):
    """vo/d: filtro LC com carga R (R=inf para vazio). esr do capacitor opcional."""
    Zc = 1 / (s * C) + esr
    Zp = Zc if not np.isfinite(R) else Zc * R / (Zc + R)
    return Vcc * Zp / (s * L + Zp)


def FTLAscv(s, Vcc=373.0, R=Ro, esr=0.0):
    return Gplanta(s, Vcc, R, esr=esr) / Vd * Hv


w_cv = 2 * pi * fcv
Lsc = FTLAscv(1j * w_cv)
Av_dB = 20 * np.log10(abs(Lsc))
P_fase = np.degrees(np.angle(Lsc))
MF_alvo = 60.0
alfa = MF_alvo - P_fase - 90
alfa_K = lambda K: (4 * np.arctan(np.sqrt(K)) - pi) * 180 / pi
K_exato = math.tan(math.radians((alfa + 180) / 4)) ** 2
K = 47.0
Gv = 10 ** (abs(Av_dB) / 20)
R1c = 10e3
comp = dict(R1=R1c, R2=sqrt(K) / (K - 1) * Gv * R1c, R3=R1c / (K - 1),
            C1=(K - 1) / (2 * pi * fcv * Gv * R1c), C2=1 / (2 * pi * fcv * Gv * R1c),
            C3=(K - 1) / sqrt(K) / (2 * pi * fcv * R1c))
comp_psim = dict(R1=10e3, R2=33e3, R3=220.0, C1=5.6e-9, C2=120e-12, C3=18e-9)


def polos_zeros(c):
    R1, R2, R3, C1, C2, C3 = (c[k] for k in ('R1', 'R2', 'R3', 'C1', 'C2', 'C3'))
    return dict(Kc=(R1 + R3) / (R1 * R3 * C2), wz1=1 / (R2 * C1), wz2=1 / ((R1 + R3) * C3),
                wp1=1 / (R3 * C3), wp2=(C1 + C2) / (R2 * C1 * C2))


def Cv(s, c=comp):
    p = polos_zeros(c)
    return p['Kc'] * (s + p['wz1']) * (s + p['wz2']) / (s * (s + p['wp1']) * (s + p['wp2']))


pz = polos_zeros(comp)
pz_psim = polos_zeros(comp_psim)
Lcc = FTLAscv(1j * w_cv) * Cv(1j * w_cv)
MF_projeto = 180 + np.degrees(np.angle(Lcc))
log('Malha: Av=%.3f dB, P=%.3f graus, alfa=%.3f, K exato=%.2f, alfa(47)=%.3f, Gv=%.4f, MF=%.3f' %
    (Av_dB, P_fase, alfa, K_exato, alfa_K(K), Gv, MF_projeto))
log('Componentes calculados:', {k: r(v) for k, v in comp.items()})
log('Polos/zeros (Hz): fz1=%.1f fz2=%.1f fp1=%.0f fp2=%.0f' % tuple(pz[k] / (2 * pi) for k in ('wz1', 'wz2', 'wp1', 'wp2')))

aud('p.9, sec. 4.5', 'Hv = 4/(raiz(2)*115)', None, Hv, 'Mantido', 'Divisor do Anexo 01 (25,22k/1025,22k) da %.6f, diferenca de %.3f%%.' % (Hv_divisor, (Hv_divisor / Hv - 1) * 100), '')
aud('p.9', 'Gv(s): termo de amortecimento L1/Ro', 'L1/Ro', 'Lo/Ro', 'Corrigido no texto', 'Na forma em s aparece L1; na forma em w, Lo. O correto e Lo/Ro.', '')
aud('p.11, passo 2', 'fcv = 2fs/6', 6666.667, fcv, 'Mantido', 'Confere; 6,67 kHz = fs/3, acima da ressonancia LC (%.0f Hz).' % f0, 'Hz')
aud('p.11, passo 3', 'P = arg(FTLAscv)', -176.289, P_fase, 'Mantido', 'Confere com Vcc = 373 V e Ro = 6,298 ohm.', 'graus')
aud('p.11, passo 4', 'Atenuacao em fcv (texto 33,23 dB)', -33.23, Av_dB, 'Corrigido para -26,22 dB',
    'O valor calculado na propria planilha e -26,223 dB; 33,23 dB e erro de texto.', 'dB')
aud('p.11, passo 6', 'alfa = MF - P - 90', 146.289, alfa, 'Mantido', 'Confere.', 'graus')
aud('p.12, passo 8', 'K = 47', 47, K_exato, 'Mantido K = 47',
    'O K exato para alfa = 146,29 graus e %.1f; K = 47 da alfa = %.2f graus e eleva a MF para %.2f graus.' % (K_exato, alfa_K(K), MF_projeto), '')
aud('p.12, passo 9', 'Fz1 = fcv/raiz(K)', 972.433, fcv / sqrt(K), 'Mantido', 'Confere.', 'Hz')
aud('p.12', 'Fp2 = fcv*raiz(K)', 4.57e4, fcv * sqrt(K), 'Mantido', 'Confere; polo duplo acima de fs = 20 kHz e proximo da ondulacao unipolar (40 kHz).', 'Hz')
aud('p.12', 'Gv = 10^(|Av|/20)', 20.472, Gv, 'Mantido', 'Valido porque a planta atenua em fcv (Av < 0); com Av > 0 o modulo inverteria o ganho.', '')
for k, v in [('R2', 3.051e4), ('R3', 217.391), ('C1', 5.364e-9), ('C2', 1.166e-10), ('C3', 1.602e-8)]:
    aud('p.13', k + ' (Tipo 3)', v, comp[k], 'Mantido', 'Confere.', 'ohm' if k[0] == 'R' else 'F')
aud('p.15', 'Margem de fase', 60.516, MF_projeto, 'Mantido em 373 V e plena carga',
    'Confere; nos demais pontos a MF real e menor (ver 05).', 'graus')
aud('p.15', 'Margem de ganho = infinito', 'inf', 'finita', 'Corrigido', 'A fase cruza -180 graus perto de 44 kHz; a MG e finita (ver 05).', 'dB')
aud('p.18, Anexo 01', 'Compensador no PSIM (RF, CFV2, C9, CI, RIP, RIZ)', '33k;5,6n;120p;18n;220;10k',
    '30,5k;5,36n;117p;16,0n;217;10k', 'Nao usado como validacao',
    'Valores comerciais proximos, mas zeros em %.0f/%.0f Hz e polos em %.1f/%.1f kHz; a simulacao do professor nao valida exatamente a funcao publicada.' %
    (pz_psim['wz1'] / 2 / pi, pz_psim['wz2'] / 2 / pi, pz_psim['wp1'] / 2e3 / pi, pz_psim['wp2'] / 2e3 / pi), '')


def analise_laco(Vcc, R, c=comp, esr=ESR_Co, atraso=0.0, f=None):
    f = np.logspace(0, 6, 120001) if f is None else f
    s = 2j * pi * f
    L = FTLAscv(s, Vcc, R, esr) * Cv(s, c) * np.exp(-s * atraso)
    m = 20 * np.log10(np.abs(L))
    ph = np.unwrap(np.angle(L)) * 180 / pi
    cruz = []
    for i in np.where(np.diff(np.sign(m)) != 0)[0]:
        fi = f[i] - m[i] * (f[i + 1] - f[i]) / (m[i + 1] - m[i])
        phi = np.interp(fi, f[i:i + 2], ph[i:i + 2])
        cruz.append(dict(f_Hz=r(fi, 5), fase_graus=r(phi, 5), MF_graus=r(180 + phi, 4)))
    mg = []
    for i in np.where(np.diff(np.sign(ph + 180)) != 0)[0]:
        fi = np.interp(-180, ph[i:i + 2][::np.sign(ph[i + 1] - ph[i]).astype(int)],
                       f[i:i + 2][::np.sign(ph[i + 1] - ph[i]).astype(int)])
        mi = np.interp(fi, f[i:i + 2], m[i:i + 2])
        mg.append(dict(f_Hz=r(fi, 5), MG_dB=r(-mi, 4)))
    # estabilidade em malha fechada pelo polinomio caracteristico (sem atraso)
    pzc = polos_zeros(c)
    num_c = pzc['Kc'] * np.polymul([1, pzc['wz1']], [1, pzc['wz2']])
    den_c = np.polymul([1, 0], np.polymul([1, pzc['wp1']], [1, pzc['wp2']]))
    # planta com ESR: vo/d = Vcc (1 + s esr C) / (L C s^2 (1+esr/R) + s (L/R + esr C) + 1), R finita
    if np.isfinite(R):
        num_p = Vcc * np.array([esr * Co, 1.0])
        den_p = np.array([Lo_adot * Co * (1 + esr / R), Lo_adot / R + esr * Co, 1.0])
    else:
        num_p = Vcc * np.array([esr * Co, 1.0])
        den_p = np.array([Lo_adot * Co, esr * Co, 1.0])
    num = np.polymul(num_c, num_p) * Hv / Vd
    den = np.polymul(den_c, den_p)
    car = np.polyadd(den, num)
    polos = np.roots(car)
    est = bool(np.all(polos.real < 0))
    s60 = 2j * pi * 60
    L60 = FTLAscv(s60, Vcc, R, esr) * Cv(s60, c)
    T60 = L60 / (1 + L60)
    return dict(Vcc=r(Vcc), R=r(R), cruzamentos_0dB=cruz, cruzamentos_fase_180=mg,
                estavel_malha_fechada=est, parte_real_max_polos=r(float(np.max(polos.real))),
                L60_modulo=r(abs(L60)), L60_fase=r(np.degrees(np.angle(L60))),
                Vo_previsto_rms=r(abs(T60) * Vref_pk / Hv / sqrt(2)), defasagem_60Hz_graus=r(np.degrees(np.angle(T60)))), (f, m, ph)


pontos_laco = [('373 V, plena 2100 W', 373.0, Ro), ('373 V, vazio', 373.0, np.inf),
               ('248,9 V, plena', ret['VC1max'], Ro), ('211,57 V, plena', ret['VC1min'], Ro),
               ('211,57 V, vazio', ret['VC1min'], np.inf), ('210 V, plena', 210.0, Ro), ('210 V, vazio', 210.0, np.inf),
               ('373 V, R 3 kVA FP=1 (4,41 ohm)', 373.0, Z3k), ('210 V, R 4,41 ohm', 210.0, Z3k)]
laco = {}
bodes = {}
for nome, V, R in pontos_laco:
    res, curva = analise_laco(V, R)
    laco[nome] = res
    bodes[nome] = curva
    log('Laco', nome, res['cruzamentos_0dB'], res['cruzamentos_fase_180'], 'estavel', res['estavel_malha_fechada'],
        'Vo prev %.4f' % res['Vo_previsto_rms'])
laco_psim = {}
for nome, V, R in pontos_laco[:2] + pontos_laco[3:5]:
    res, _ = analise_laco(V, R, c=comp_psim)
    laco_psim[nome] = res
Td = 1 / (4 * fs)
laco_atraso = {}
for nome, V, R in [pontos_laco[0], pontos_laco[3], pontos_laco[6]]:
    res, _ = analise_laco(V, R, atraso=Td)
    laco_atraso[nome] = dict(cruzamentos_0dB=res['cruzamentos_0dB'], cruzamentos_fase_180=res['cruzamentos_fase_180'])
Cv40 = abs(Cv(2j * pi * 2 * fs))
dVo_pp = ripples['373,35 V (pico a 264 V)']['dILo_max_App'] / (8 * 2 * fs * Co)
vc_ripple_pp = dVo_pp * Hv * Cv40
portadora_inclinacao = 2 * Vd / (1 / (2 * fs))          # V/s
vc_inclinacao = pi * 2 * fs * vc_ripple_pp               # estimativa senoidal, V/s
log('|Cv| em 40 kHz = %.2f; ondulacao de vo %.3f Vpp; em vc %.3f Vpp; inclinacao vc/portadora = %.3f' %
    (Cv40, dVo_pp, vc_ripple_pp, vc_inclinacao / portadora_inclinacao))

# ---------------------------------------------------------------------------
# 5. CC-CC de alto ganho (secao 5, paginas 16 e 17)
# ---------------------------------------------------------------------------
cc = dict(Vibmin=42.0, Vibmax=56.0, Vob=210.0, Pob=2250.0, Dbmax=0.7, fsb=20e3)
cc['Iibmax'] = cc['Pob'] / cc['Vibmin']
cc['dIibmax'] = 0.2 * cc['Iibmax']
cc['Lb'] = cc['Vibmin'] * (2 * cc['Dbmax'] - 1) / (2 * cc['fsb'] * cc['dIibmax'])
cc['Lb_adot'] = 39.2e-6
cc['VC1'] = cc['Vibmin'] / (1 - cc['Dbmax'])
cc['VNp'] = cc['VC1'] / 2
cc['VSec'] = 70.0
cc['a'] = cc['VSec'] / cc['VNp']
n = cc['a']
ganho = lambda D: (1 + n / 2) / (1 - D)
D_para = lambda Vi: 1 - (1 + n / 2) * Vi / cc['Vob']
cc['D_42'] = D_para(42.0)
cc['D_56'] = D_para(56.0)
eta_cc_H = 0.95
pontos_cc = {}
for Vi in (42.0, 56.0):
    D = D_para(Vi)
    Ii = cc['Pob'] / Vi
    dI = Vi * (2 * D - 1) / (2 * cc['fsb'] * cc['Lb_adot'])
    pontos_cc[str(int(Vi))] = dict(D=D, VC8=Vi / (1 - D), VC7=n * Vi / (2 * (1 - D)), Vbus=ganho(D) * Vi,
                                   Iib=Ii, Iib_com_eta095=Ii / eta_cc_H, dILb_pp=dI, ILb_pico=Ii + dI / 2,
                                   V_chave=Vi / (2 * (1 - D)), V_D17_D18=Vi / (1 - D), V_ponte_sec=n * Vi / (2 * (1 - D)),
                                   I_chave_media=Ii / 2)
ripple_bus_bat = cc['Pob'] / (2 * pi * E['fo'] * C1_adot * cc['Vob'])
log('CC-CC:', {k: r(v) for k, v in cc.items()})
log('CC-CC pontos:', {k: {a: r(b) for a, b in v.items()} for k, v in pontos_cc.items()})
aud('p.16, sec. 5.2', 'Iibmax = Pob/Vibmin', 53.571, cc['Iibmax'], 'Mantido como limite inferior',
    'Pob = 2250 W e potencia de saida do CC-CC; sem rendimento proprio. Com eta = 0,95 (H) a bateria fornece %.1f A.' % (cc['Iibmax'] / eta_cc_H), 'A')
aud('p.16', 'dIibmax = 0,2*Iibmax', 10.714, cc['dIibmax'], 'Mantido', 'Confere.', 'A')
aud('p.16, sec. 5.3', 'Lb = Vib(2D-1)/(2 fsb dI)', 3.92e-5, cc['Lb'], 'Mantido', 'Confere; indutor ve 2fsb na regiao D > 0,5 da celula de tres estados.', 'H')
aud('p.16', 'VC1 = Vib/(1-D) (capacitor inferior)', 140, cc['VC1'], 'Mantido', 'Confere; e o C8 do Anexo 01.', 'V')
aud('p.16', 'VNp = VC1/2', 70, cc['VNp'], 'Mantido', 'Confere.', 'V')
aud('p.17', 'a = VSec/VNp', 1, cc['a'], 'Mantido', 'Vob = VC8 + VC7 = 140 + 70 = 210 V: o retificador do secundario empilha C7 sobre C8.', '')
aud('p.16', 'Razao ciclica a 56 V', 'nao calculada', cc['D_56'], 'Complementado', 'D = 1 - 1,5*56/210 = 0,60, ainda acima de 0,5.', '')
aud('p.16 e p.6', 'Vob = 210 V frente ao vale do retificador', 210, Vimin_cc, 'Registrado',
    'Margem de apenas %.2f V; a coerencia depende da logica de transferencia (ver 06).' % (Vimin_cc - 210), 'V')

# ---------------------------------------------------------------------------
# 6. Figuras analiticas
# ---------------------------------------------------------------------------
COR = ['#2a78d6', '#eb6834', '#1baf7a', '#6250d6', '#e34948', '#008300', '#eda100']
ESTILO = ['-', '--', '-.', ':', (0, (5, 1, 1, 1)), (0, (3, 1)), '-']
plt.rcParams.update({'font.size': 8.5, 'axes.labelsize': 8.5, 'legend.fontsize': 7.2, 'xtick.labelsize': 8,
                     'ytick.labelsize': 8, 'axes.grid': True, 'grid.alpha': .3, 'grid.linewidth': .5,
                     'lines.linewidth': 1.3, 'axes.spines.top': False, 'axes.spines.right': False,
                     'font.family': 'serif', 'savefig.dpi': 300, 'axes.titlesize': 8.5})


def virgula(*eixos):
    """Separador decimal brasileiro nos eixos lineares."""
    fmt = matplotlib.ticker.FuncFormatter(lambda v, p: ('%g' % v).replace('.', ','))
    for e in eixos:
        e.set_major_formatter(fmt)


def salvar(fig, nome):
    fig.tight_layout(pad=.4)
    fig.savefig(FIG / (nome + '.png'), dpi=300)
    fig.savefig(FIG / (nome + '.pdf'))
    plt.close(fig)


f = np.logspace(0, 5.8, 3000)
s = 2j * pi * f
fig, ax = plt.subplots(2, 1, figsize=(3.45, 3.3), sharex=True)
for i, (nome, V, R) in enumerate([('373 V, 2100 W', 373.0, Ro), ('373 V, vazio', 373.0, np.inf),
                                   ('211,6 V, 2100 W', ret['VC1min'], Ro)]):
    L = FTLAscv(s, V, R, ESR_Co)
    ax[0].semilogx(f, 20 * np.log10(abs(L)), color=COR[i], ls=ESTILO[i], label=nome)
    ax[1].semilogx(f, np.unwrap(np.angle(L)) * 180 / pi, color=COR[i], ls=ESTILO[i])
ax[0].axvline(fcv, color='0.4', lw=.7, ls=':')
ax[1].axvline(fcv, color='0.4', lw=.7, ls=':')
ax[0].set_ylabel('Ganho (dB)')
ax[0].set_ylim(-80, 60)
ax[1].set_ylabel('Fase (graus)')
ax[1].set_xlabel('Frequência (Hz)')
ax[1].set_yticks([0, -45, -90, -135, -180])
ax[0].legend(loc='lower left', frameon=False)
ax[0].annotate('$f_{cv}$', (fcv, 40), fontsize=7.5, ha='left')
salvar(fig, 'bode_planta')

fig, ax = plt.subplots(2, 1, figsize=(3.45, 3.1), sharex=True)
for i, (nome, c) in enumerate([('Calculado (planilha)', comp), ('Comercial do PSIM', comp_psim)]):
    C_ = Cv(s, c)
    ax[0].semilogx(f, 20 * np.log10(abs(C_)), color=COR[i], ls=ESTILO[i], label=nome)
    ax[1].semilogx(f, np.angle(C_) * 180 / pi, color=COR[i], ls=ESTILO[i])
ax[0].set_ylabel('Ganho (dB)')
ax[1].set_ylabel('Fase (graus)')
ax[1].set_xlabel('Frequência (Hz)')
ax[0].legend(loc='upper center', frameon=False)
salvar(fig, 'bode_compensador')

fig, ax = plt.subplots(2, 1, figsize=(3.45, 3.5), sharex=True)
sel = ['373 V, plena 2100 W', '373 V, vazio', '211,57 V, plena', '210 V, vazio']
rot = ['373 V, 2100 W', '373 V, vazio', '211,6 V, 2100 W', '210 V, vazio']
for i, nome in enumerate(sel):
    V, R = next((v, rr) for n_, v, rr in pontos_laco if n_ == nome)
    L = FTLAscv(s, V, R, ESR_Co) * Cv(s)
    ax[0].semilogx(f, 20 * np.log10(abs(L)), color=COR[i], ls=ESTILO[i], label=rot[i])
    ax[1].semilogx(f, np.unwrap(np.angle(L)) * 180 / pi, color=COR[i], ls=ESTILO[i])
    for c_ in laco[nome]['cruzamentos_0dB']:
        ax[0].plot(c_['f_Hz'], 0, 'o', ms=3.5, color=COR[i])
ax[0].axhline(0, color='0.3', lw=.6)
ax[1].axhline(-180, color='0.3', lw=.6)
ax[0].set_ylim(-60, 100)
ax[0].set_ylabel('Ganho (dB)')
ax[1].set_ylabel('Fase (graus)')
ax[1].set_xlabel('Frequência (Hz)')
ax[1].set_ylim(-280, 0)
ax[1].set_yticks([0, -90, -180, -270])
ax[0].legend(loc='lower left', frameon=False, ncol=1)
salvar(fig, 'bode_laco')

fig, ax = plt.subplots(figsize=(3.45, 2.2))
Ks = np.logspace(0, 4, 400)
ax.semilogx(Ks, alfa_K(Ks), color=COR[0])
ax.axhline(alfa, color=COR[1], ls='--', lw=.9)
ax.plot([K], [alfa_K(K)], 'o', color=COR[1], ms=4)
ax.annotate(('K = 47; α = %.1f°' % alfa_K(K)).replace('.', ','), (K, alfa_K(K)), xytext=(60, 95), fontsize=7.5,
            arrowprops=dict(arrowstyle='-', lw=.6))
ax.set_xlabel('Fator K')
ax.set_ylabel('Avanço de fase α (graus)')
salvar(fig, 'avanco_fase_K')

fig, ax = plt.subplots(figsize=(3.45, 2.4))
th = np.linspace(0, pi, 400)
for i, (nome, V) in enumerate([('373,4 V', Vimax_cc), ('248,9 V', ret['VC1max']), ('210 V', 210.0)]):
    vo = Vopk * np.sin(th)
    ax.plot(th * 180 / pi, ripple_unipolar(V, vo), color=COR[i], ls=ESTILO[i], label=nome)
ax.axhline(dILo, color='0.35', lw=.8, ls=':')
ax.annotate('critério da planilha (10,33 A)', (5, dILo - .9), fontsize=7.2)
ax.set_xlabel('Ângulo da tensão de saída (graus)')
ax.set_ylabel('$\\Delta I_{Lo}$ pico a pico (A)')
ax.set_xlim(0, 180)
ax.set_ylim(0, 11.5)
ax.legend(frameon=False, loc='center right')
salvar(fig, 'ondulacao_Lo')

fig, ax = plt.subplots(figsize=(3.45, 2.3))
Ds = np.linspace(0.5, 0.8, 200)
for i, Vi in enumerate((42.0, 56.0)):
    ax.plot(Ds, ganho(Ds) * Vi, color=COR[i], ls=ESTILO[i], label='$V_{bat}$ = %d V' % Vi)
    ax.plot([D_para(Vi)], [210], 'o', color=COR[i], ms=4)
ax.axhline(210, color='0.35', lw=.8, ls=':')
ax.axhline(Vimin_cc, color=COR[4], lw=.8, ls='--')
ax.annotate('vale do retificador a 176 V (211,6 V)', (0.505, Vimin_cc + 22), fontsize=7.2, color='0.2')
ax.annotate('alvo 210 V', (0.74, 186), fontsize=7.2, color='0.2')
virgula(ax.xaxis)
ax.set_xlabel('Razão cíclica D')
ax.set_ylabel('Tensão do barramento (V)')
ax.set_ylim(0, 450)
ax.legend(frameon=False, loc='upper left')
salvar(fig, 'ganho_cc')

# Bodes do laco em CSV (grade logaritmica reduzida)
with open(OUT / 'bode_laco_pontos.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['ponto', 'f_Hz', 'ganho_dB', 'fase_graus'])
    for nome, (ff, m, ph) in bodes.items():
        idx = np.unique(np.round(np.logspace(0, np.log10(len(ff) - 1), 600)).astype(int))
        for i in idx:
            w.writerow([nome, f'{ff[i]:.6g}', f'{m[i]:.6g}', f'{ph[i]:.6g}'])

# ---------------------------------------------------------------------------
# 7. Parametros para os modelos PLECS (hipoteses H explicitas)
# ---------------------------------------------------------------------------
sim = dict(
    classe='H',
    nota='Hipoteses de simulacao. Valores do Anexo 01 quando existem; demais escolhidos e justificados no 07-guia-plecs.md.',
    fs=fs, fr=60.0, fo=60.0, Vref_pk=Vref_pk, Hv=Hv, Vd=Vd, Vsat_comp=5.0,
    Lo=Lo_adot, Co=Co, ESR_Co=ESR_Co, Ro=Ro, R3k=R3k, L3k=L3k,
    C4=C1_adot, ESR_C4=Rse_C1, Rbus=0.1, T1_relacao=1.0,
    Vf_ponte=0.8, Ron_ponte=0.01, Vf_rapido=0.8, Ron_rapido=0.005,
    Ron_inv=0.05, Ron_cc=0.01, Lb=cc['Lb_adot'], C7=10e-6, C8=10e-6,
    T32_Lm=10e-3, T32_Llk=1e-6, T32_R=1e-3, n_T32=1.0,
    # amortecedores RC nas chaves S1, S2 e no secundario de T32 (capacitancia de saida da ordem de 1 nF);
    # Rsn escolhido para amortecimento ~0,5 com a dispersao: zeta = (Rsn/2)*sqrt(Csn/Llk)
    Rsn_cc=33.0, Csn_cc=1e-9, zeta_sn=33.0 / 2 * math.sqrt(1e-9 / 1e-6),
    Vbat=42.0, Db=0.7, Vbat_alt=56.0, Db_alt=cc['D_56'],
    nl_Rs=anexo_nl['Rs'], nl_C=anexo_nl['C'], nl_ESR=anexo_nl['ESR'], nl_R=anexo_nl['R'],
    comp=dict(Kc=pz['Kc'], wz1=pz['wz1'], wz2=pz['wz2'], wp1=pz['wp1'], wp2=pz['wp2']),
    solver=dict(Solver='radau', MaxStep=5e-6, RelTol=1e-6, AbsTol=1e-8))

P = dict(
    meta=dict(trabalho='Trabalho 6 - No-break dupla conversao 3 kVA', gerado_em=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
              python=platform.python_version(), numpy=np.__version__, script='desenvolvimento/calculos.py',
              classes=dict(F='dado do professor (pagina)', A='resultado analitico deste script', S='resultado do PLECS', H='hipotese')),
    especificacoes=E, eta_inv_orcamento=eta_inv, Prec=Prec,
    retificador=dict(planilha=ret, alternativa_10pct=ret_10, C1_adotado=C1_adot, Rse=Rse_C1, VDrrevpk=VDrrevpk,
                     Vimin_cc=Vimin_cc, Vimax_cc=Vimax_cc, vales_com_1880uF=vales, vale_176_C_menos20pct=vale_tol),
    inversor=dict(fs=fs, Vopk=Vopk, Ioef=Ioef, Iopk=Iopk, dILo_criterio=dILo, Mmax_223=Mmax_223, Mmin=Mmin,
                  Lo_calc=Lo, Lo=Lo_adot, Co_fs20=Co_fs20, Co_fs40=Co_fs40, Co=Co, ESR_Co=ESR_Co, Ro=Ro,
                  f0_LC=f0, Z0=Z0, Q_plena=Ro / Z0, Q_vazio_ESR=Z0 / ESR_Co, I_Co_60Hz=I_Co_60,
                  indices_modulacao=indices, ondulacao_Lo=ripples, dILo_real_373=dILo_planilha_Vcc373,
                  carga_3kVA=dict(Z=Z3k, R=R3k, X=X3k, L=L3k, Irms=Irms3k), iec_62040_ref=iec, nao_linear_anexo=anexo_nl,
                  esforcos=cargas),
    malha=dict(Vref_pk=Vref_pk, Hv=Hv, Hv_divisor_anexo=Hv_divisor, Vd=Vd, fcv=fcv, Av_dB=Av_dB, P_graus=P_fase,
               MF_alvo=MF_alvo, alfa=alfa, K=K, K_exato=K_exato, alfa_K47=alfa_K(K), Gv=Gv,
               componentes=comp, componentes_psim=comp_psim, polos_zeros=pz, polos_zeros_psim=pz_psim,
               fz_Hz=[pz['wz1'] / 2 / pi, pz['wz2'] / 2 / pi], fp_Hz=[pz['wp1'] / 2 / pi, pz['wp2'] / 2 / pi],
               MF_projeto=MF_projeto, pontos=laco, pontos_psim=laco_psim, atraso_PWM_s=Td, pontos_com_atraso=laco_atraso,
               Cv_40kHz=Cv40, dVo_pp_373=dVo_pp, vc_ondulacao_pp=vc_ripple_pp, razao_inclinacao_vc_portadora=vc_inclinacao / portadora_inclinacao),
    cc_cc=dict(planilha=cc, pontos=pontos_cc, eta_H=eta_cc_H, ondulacao_bus_120Hz_bateria_Vpp=ripple_bus_bat,
               topologia='Celula de comutacao de tres estados com autotransformador (dois primarios), secundario 1:1 em ponte e capacitor C7 empilhado sobre C8'),
    simulacao=sim,
    figuras=sorted(p.name for p in FIG.glob('*.png')))


def limpa(o):
    if isinstance(o, dict):
        return {k: limpa(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpa(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return r(float(o), 10)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


(OUT / 'parametros.json').write_text(json.dumps(limpa(P), indent=1, ensure_ascii=False), encoding='utf-8')
with open(OUT / 'auditoria.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(AUD[0].keys()))
    w.writeheader()
    for a in AUD:
        w.writerow(a)
(OUT / 'auditoria.json').write_text(json.dumps(limpa(AUD), indent=1, ensure_ascii=False), encoding='utf-8')
LOG.insert(0, 'execucao: %s | Python %s | numpy %s' % (P['meta']['gerado_em'], platform.python_version(), np.__version__))
(OUT / 'execucao_calculos.txt').write_text('\n'.join(LOG) + '\n', encoding='utf-8')
print('OK:', len(AUD), 'itens auditados;', len(P['figuras']), 'figuras;', OUT / 'parametros.json')
