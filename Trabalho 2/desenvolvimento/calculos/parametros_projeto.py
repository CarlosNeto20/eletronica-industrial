"""Confere os quatro exemplos de projeto do enunciado e deriva os parâmetros de simulação.

Reproduz as contas do documento do professor (Mathcad), calcula os conversores
equivalentes não isolados referidos ao secundário e os resistores do ensaio de
degrau de carga 20 % <-> 100 %. Rode com:  python parametros_projeto.py
"""
from math import pi

def linha(nome, valor, unidade=""):
    print(f"  {nome:<34s} {valor:>14.6g} {unidade}")

def cabecalho(t):
    print("\n" + t + "\n" + "-" * len(t))

def carga(Po, Vo):
    Ro = Vo**2 / Po
    R20 = 5 * Ro            # 20 % da potência nominal
    R80 = Ro * 5 / 4        # em paralelo com R20 fecha Ro (100 %)
    return Ro, R20, R80

# ---------------------------------------------------------------- Forward
cabecalho("1. FORWARD DE UMA CHAVE")
Po, Vi, Vo, fs, dIL, dVC, D = 500, 200, 54, 20e3, 1.5, 0.27, 0.4
n = Vo / (Vi * D); Io = Po / Vo
Lo = (n * Vi - Vo) * D / (dIL * fs)
Co = dIL / (8 * fs * dVC); Rse = dVC / dIL
Ro, R20, R80 = carga(Po, Vo)
Im = 0.02 * n * Io; XLm = Vi / Im; Lm = XLm / (2 * pi * fs)
for k, v, u in [("n = Ns/Np", n, ""), ("Io", Io, "A"), ("Lo", Lo, "H"), ("Co", Co, "F"),
                ("Rse", Rse, "ohm"), ("Ro", Ro, "ohm"), ("R 20 %", R20, "ohm"),
                ("R extra (80 %)", R80, "ohm"), ("Im", Im, "A"), ("Lm", Lm, "H"),
                ("Equiv. Buck: Vin = n.Vi", n * Vi, "V"), ("Equiv. Buck: D, fs", D, f"/ {fs:g} Hz"),
                ("iLo min a 20 % (CCM se > 0)", 0.2 * Io - dIL / 2, "A"),
                ("Dmax (desmag., Nt = Np)", 0.5, "")]:
    linha(k, v, u)

# ---------------------------------------------------------------- Full-bridge
cabecalho("2. PONTE COMPLETA (FULL-BRIDGE)")
Po, Vi, Vo, fs, dIL, dVC, D = 5000, 400, 54, 20e3, 18.52, 0.27, 0.4
a = Vo / Vi / (2 * D); Io = Po / Vo
Lo = Vo * (0.5 - D) / (fs * dIL)
Co = (1 - 2 * D) * Vo / (32 * Lo * fs**2 * dVC); Rc = dVC / dIL
Ro, R20, R80 = carga(Po, Vo)
Im_enunciado = 0.02 * 0.675 * Io      # o enunciado reaproveitou n = 0,675 do Forward
Im_correto = 0.02 * a * Io
Lm_enunciado = Vi / Im_enunciado / (2 * pi * fs)
Lm_correto = Vi / Im_correto / (2 * pi * fs)
for k, v, u in [("a = Ns/Np", a, ""), ("Io", Io, "A"), ("Lo", Lo, "H"), ("Co", Co, "F"),
                ("Rc", Rc, "ohm"), ("Ro", Ro, "ohm"), ("R 20 %", R20, "ohm"),
                ("R extra (80 %)", R80, "ohm"),
                ("Im (enunciado, usa n=0,675)", Im_enunciado, "A"), ("Lm (enunciado)", Lm_enunciado, "H"),
                ("Im (com a=0,169)", Im_correto, "A"), ("Lm (com a=0,169)", Lm_correto, "H"),
                ("Equiv. Buck: Vin = a.Vi", a * Vi, "V"), ("Equiv. Buck: D = 2D", 2 * D, ""),
                ("Equiv. Buck: f = 2fs", 2 * fs, "Hz"),
                ("iLo min a 20 % (CCM se > 0)", 0.2 * Io - dIL / 2, "A")]:
    linha(k, v, u)

# ---------------------------------------------------------------- Push-pull
cabecalho("3. PUSH-PULL ALIMENTADO EM CORRENTE")
Po, Vi, Vo, fs, dIL, dVC, D = 1000, 54, 400, 20e3, 3.7, 4, 0.7
a = Vo / Vi * 2 * (1 - D); Io = Po / Vo
Li = (2 * D - 1) * Vi / (2 * fs * dIL)
Co = (2 * D - 1) * Io / (2 * fs * dVC)
Ii = Po / Vi; ILmax = Ii + dIL / 2; Rc = dVC / ILmax * a
Ro, R20, R80 = carga(Po, Vo)
ILm = 0.01 * Ii; Vpri = Vo / a; Lm = Vpri / ILm / (2 * pi * fs)
for k, v, u in [("a = Ns/Np (cada meio primário)", a, ""), ("Io", Io, "A"), ("Li", Li, "H"),
                ("Co", Co, "F"), ("Ii", Ii, "A"), ("ILi_max", ILmax, "A"), ("Rc", Rc, "ohm"),
                ("Ro", Ro, "ohm"), ("R 20 %", R20, "ohm"), ("R extra (80 %)", R80, "ohm"),
                ("ILm", ILm, "A"), ("Vpri", Vpri, "V"), ("Lm", Lm, "H"),
                ("Equiv. Boost: Vin = a.Vi", a * Vi, "V"), ("Equiv. Boost: L = a^2.Li", a**2 * Li, "H"),
                ("Equiv. Boost: D = 2D-1", 2 * D - 1, ""), ("Equiv. Boost: f = 2fs", 2 * fs, "Hz"),
                ("iLi min a 20 % (CCM se > 0)", 0.2 * Ii - dIL / 2, "A")]:
    linha(k, v, u)

# ---------------------------------------------------------------- Flyback
cabecalho("4. FLYBACK DE UMA CHAVE")
Po, Vi, Vo, fs, dVC, D, eta = 200, 200, 54, 20e3, 0.54, 0.4, 1
a = Vo / Vi * (1 - D) / D; Io = Po / Vo; Pi = Po / eta
Lcrit = Vi**2 * D**2 / (2 * fs * Pi); Lmcd = 0.9 * Lcrit; Lmcc = 10 * Lmcd
Co = Io * D / (fs * dVC); Rse = dVC / (2 * Io / (1 - D))
Ro, R20, R80 = carga(Po, Vo)
# Tensão de saída em MCD, malha aberta: Vo = Vi.D.sqrt(R/(2.L.fs))
vo_mcd = lambda R: Vi * D * (R / (2 * Lmcd * fs)) ** 0.5
for k, v, u in [("a = Ns/Np", a, ""), ("Io", Io, "A"), ("Lm crítica (primário)", Lcrit, "H"),
                ("Lm MCD = 0,9 Lcrit", Lmcd, "H"), ("Lm MCC = 10 LmMCD", Lmcc, "H"),
                ("Co", Co, "F"), ("Rse", Rse, "ohm"), ("Ro", Ro, "ohm"), ("R 20 %", R20, "ohm"),
                ("R extra (80 %)", R80, "ohm"),
                ("Equiv. Buck-Boost: Vin = a.Vi", a * Vi, "V"),
                ("Equiv. L MCD = a^2.Lm", a**2 * Lmcd, "H"), ("Equiv. L MCC = a^2.Lm", a**2 * Lmcc, "H"),
                ("Vo MCD a 100 % (malha aberta)", vo_mcd(Ro), "V"),
                ("Vo MCD a 20 % (malha aberta)", vo_mcd(R20), "V")]:
    linha(k, v, u)
