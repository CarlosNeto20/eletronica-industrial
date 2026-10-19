"""Roda os ensaios do carregador no PLECS pela interface RPC e grava os CSV.

Pré-requisitos: PLECS Standalone aberto, com a interface RPC habilitada em
File > PLECS Preferences > General (porta 1080).

Uso:  python rodar_ensaios.py                 (todos os ensaios, 176 V e 264 V)
      python rodar_ensaios.py degrau          (um ensaio, nas duas tensões)
      python rodar_ensaios.py regime 220      (um ensaio, uma tensão)
      python rodar_ensaios.py --panoramas     (só as janelas do tipo "grade")

Cada linha de CASOS vira um CSV nesta pasta, <ensaio>_<Vrede><sufixo>.csv, com
a coluna de tempo seguida dos sinais de MEDIDAS (gerador/gerar_carregador.py).
Dois tipos de janela:
  "grade"  -> amostras em instantes igualmente espaçados (panorama do ensaio);
              o passo não é múltiplo do período de comutação, para que a faixa
              de ondulação apareça inteira no gráfico;
  "passos" -> todos os passos do integrador dentro da janela (detalhe).
Cada janela é uma simulação completa a partir de t = 0, encerrada no fim da
janela. Quem não tiver o RPC pode obter os mesmos dados à mão: fixar "Vrede"
e "ensaio" nos comandos de inicialização do modelo e simular.
"""
import os
import sys
import time
import xmlrpc.client
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "simulação PLECS", "gerador"))
from gerar_carregador import MEDIDAS  # noqa: E402

MODELO = os.path.join(RAIZ, "simulação PLECS", "carregador.plecs")
NOME = "carregador"
URL = "http://localhost:1080/RPC2"
COLUNAS = ["t"] + [n for n, _, _ in MEDIDAS]
T3 = 1.0 / 3.0            # período de comutação da carga (f_carga = 3 Hz)
TR = 1.0 / 60.0           # período da rede
N_GRADE = 43691           # pontos por segundo dos panoramas: passo de 22,89 us, que não é
                          # múltiplo do período de comutação (20 us) nem de uma fração simples dele

# ensaio -> (valor da variável "ensaio", [(sufixo, tipo, t0, t1, n)], variáveis extras)
CASOS = {
    # carga nominal fixa: dois ciclos de rede em regime permanente
    "regime": (0, [("", "passos", 0.30, 0.30 + 2 * TR, None)], {}),
    # degrau de carga: 100 % em [0, 1/6), 20 % em [1/6, 1/3), ...
    "degrau": (1, [("", "grade", 0.0, 1.0, N_GRADE),
                   ("_100-20", "passos", 0.5 - 0.002, 0.5 + 0.010, None),
                   ("_20-100", "passos", 2 * T3 - 0.002, 2 * T3 + 0.010, None)], {}),
    # o mesmo degrau com folga de 4 % no limite de corrente (Vrefi = 2,6 V -> 15,6 A): a malha
    # de tensão permanece no comando com 100 % de carga
    "degrau-folga": (1, [("", "grade", 0.0, 1.0, N_GRADE),
                         ("_100-20", "passos", 0.5 - 0.002, 0.5 + 0.010, None),
                         ("_20-100", "passos", 2 * T3 - 0.002, 2 * T3 + 0.010, None)],
                     {"Vrefi": 2.6}),
    # curto-circuito: aplicado em [0, 1/6), [1/3, 1/2), ...
    "curto": (2, [("", "grade", 0.0, 1.0, N_GRADE),
                  ("_entrada", "passos", T3 - 0.002, T3 + 0.010, None),
                  ("_saida", "passos", 0.5 - 0.002, 0.5 + 0.030, None)], {}),
    # recarga da bateria: corrente constante até 27 V, depois tensão constante
    "recarga": (3, [("", "grade", 0.0, 0.6, int(0.6 * (N_GRADE - 1)) + 1)], {}),
}
TENSOES = (176, 264)


def variaveis(vrede, ensaio):
    """Variáveis do modelo para um ensaio.

    O RPC substitui as variáveis DEPOIS de os comandos de inicialização terem
    sido executados; por isso as que derivam de "Vrede" e de "ensaio" precisam
    ser enviadas já calculadas (mesmas contas dos comandos de inicialização)."""
    vd, ro = 0.7, 27.0 / 15.0
    v = {"Vrede": float(vrede), "ensaio": float(ensaio),
         "Vpk": float(np.sqrt(2) * vrede), "VC1_0": float(np.sqrt(2) * vrede - 2 * vd)}
    v.update({0: dict(R9=ro, R10=1e6, hab_carga=0.0, hab_bat=0.0),
              1: dict(R9=5 * ro, R10=1.25 * ro, hab_carga=1.0, hab_bat=0.0),
              2: dict(R9=ro, R10=1e-3, hab_carga=1.0, hab_bat=0.0),
              3: dict(R9=1e6, R10=1e6, hab_carga=0.0, hab_bat=1.0)}[ensaio])
    return v


def simula(proxy, vrede, ensaio, tipo, t0, t1, n, extras=None):
    mv = variaveis(vrede, ensaio)
    mv.update(extras or {})
    if tipo == "grade":
        so = {"TimeSpan": float(t1), "OutputTimes": [float(x) for x in np.linspace(t0, t1, n)]}
    else:
        so = {"TimeSpan": float(t1), "OutputTimes": [float(t0), float(t1)],
              "OutputTimesOption": "range"}
    r = proxy.plecs.simulate(NOME, {"ModelVars": mv, "SolverOpts": so})
    d = np.column_stack([np.array(r["Time"])] + [np.array(v) for v in r["Values"]])
    assert d.shape[1] == len(COLUNAS), "número de sinais diferente de MEDIDAS: regenerar o modelo"
    return d


def grava(d, nome):
    caminho = os.path.join(AQUI, nome)
    np.savetxt(caminho, d, delimiter=",", fmt="%.8g", header=",".join(COLUNAS), comments="")
    return caminho


def main(args):
    casos = [a for a in args if a in CASOS] or list(CASOS)
    sys.stdout.reconfigure(line_buffering=True)
    tensoes = [int(a) for a in args if a.isdigit()] or list(TENSOES)
    proxy = xmlrpc.client.ServerProxy(URL)
    try:
        proxy.plecs.close(NOME)
    except Exception:
        pass
    proxy.plecs.load(MODELO.replace("\\", "/"))
    for caso in casos:
        num, janelas, extras = CASOS[caso]
        for v in tensoes:
            for suf, tipo, t0, t1, n in janelas:
                if "--panoramas" in args and tipo != "grade":
                    continue
                ini = time.time()
                try:
                    d = simula(proxy, v, num, tipo, t0, t1, n, extras)
                except xmlrpc.client.Fault as e:
                    print("%-8s %d V %-8s ERRO DO PLECS: %s" % (caso, v, suf, e.faultString))
                    continue
                nome = "%s_%d%s.csv" % (caso, v, suf)
                grava(d, nome)
                print("%-22s %6d pontos  %5.1f s  (Vbat %.2f a %.2f V; IL %.2f a %.2f A)" % (
                    nome, len(d), time.time() - ini,
                    d[:, COLUNAS.index("v_bat")].min(), d[:, COLUNAS.index("v_bat")].max(),
                    d[:, COLUNAS.index("i_L")].min(), d[:, COLUNAS.index("i_L")].max()))


if __name__ == "__main__":
    main(sys.argv[1:])
