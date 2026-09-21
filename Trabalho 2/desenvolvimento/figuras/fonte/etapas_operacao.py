"""Etapas de operação do Full-bridge e do Push-pull alimentado em corrente.

Atende ao pedido do enunciado: "colocar 4 conversores e marcar em negrito por
onde percorre a corrente". Gera, em desenvolvimento/figuras:
    etapas-fullbridge-1.png ... etapas-fullbridge-4.png
    etapas-pushpull-1.png   ... etapas-pushpull-4.png
Uso: python etapas_operacao.py
"""
import os
from esquema import Esquema

SAIDA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =================================================================== Full-bridge
def fullbridge(etapa):
    """Etapas (comando da Fig. 7): 1 = S1,S2; 2 = roda livre; 3 = S3,S4; 4 = roda livre."""
    diag12, diag34 = etapa == 1, etapa == 3
    rl = etapa in (2, 4)
    e = Esquema(13.5, 7.2)
    # ---- primário
    ativo_p = diag12 or diag34
    e.ramo_v(0, 6, 0, "fonte", on=ativo_p, rotulo="Vi", lado=-0.45)
    e.fio([(0, 6), (1.5, 6)], ativo_p)
    e.fio([(1.5, 6), (3.5, 6)], diag34)
    e.fio([(0, 0), (1.5, 0)], ativo_p)
    e.fio([(1.5, 0), (3.5, 0)], diag12)
    e.ramo_v(1.5, 6, 3.6, "mosfet", on=diag12, rotulo="S1", lado=0.3)
    e.ramo_v(1.5, 3.6, 0, "mosfet", on=diag34, rotulo="S4", lado=0.3)
    e.ramo_v(3.5, 6, 2.4, "mosfet", on=diag34, rotulo="S3", lado=0.3)
    e.ramo_v(3.5, 2.4, 0, "mosfet", on=diag12, rotulo="S2", lado=0.3)
    e.fio_salto([(1.5, 3.6), (5.25, 3.6)], 3.5, on=ativo_p)       # nó a -> primário
    e.fio([(3.5, 2.4), (5.25, 2.4)], ativo_p)                     # nó b -> primário
    for p in [(1.5, 6), (1.5, 0), (1.5, 3.6), (3.5, 2.4)]:
        e.no(*p)
    # ---- transformador
    e.bobina(5.25, 3.6, 2.4, +1, on=ativo_p)
    e.nucleo(5.6, 3.7, 2.3)
    e.bobina(5.95, 3.6, 2.4, -1, on=ativo_p)
    e.ponto(5.05, 3.55); e.ponto(6.15, 3.55)
    e.texto(5.6, 4.0, "Tr")
    # ---- retificador em ponte
    e.fio([(5.95, 3.6), (7, 3.6)], diag12 or diag34)                   # p
    e.fio_salto([(5.95, 2.4), (8, 2.4)], 7, on=diag12 or diag34)       # q
    e.ramo_v(7, 5, 3.6, "diodo", on=diag12 or rl, rotulo="D1", lado=-0.35, h=0.7)
    e.fio([(7, 3.6), (7, 1.95)], diag34 or rl)
    e.ramo_v(7, 1.95, 1, "diodo", on=diag34 or rl, rotulo="D4", lado=-0.35, h=0.7)
    e.ramo_v(8, 5, 2.4, "diodo", on=diag34 or rl, rotulo="D3", lado=0.35, h=0.7)
    e.ramo_v(8, 2.4, 1, "diodo", on=diag12 or rl, rotulo="D2", lado=0.35, h=0.7)
    e.fio([(7, 5), (8, 5)], diag12 or rl)
    e.fio([(7, 1), (8, 1)], diag34 or rl)
    for p in [(7, 3.6), (8, 2.4), (8, 5), (8, 1)]:
        e.no(*p)
    # ---- filtro e carga (sempre com corrente)
    e.ramo_h(5, 8, 10.6, "ind", on=True, rotulo="Lo", h=1.2)
    e.ramo_v(10.6, 5, 1, "cap", on=True, rotulo="Co", lado=0.3)
    e.fio([(10.6, 5), (11.8, 5)], True)
    e.ramo_v(11.8, 5, 1, "res", on=True, rotulo="Ro", lado=0.3)
    e.fio([(8, 1), (11.8, 1)], True)
    e.no(10.6, 5); e.no(10.6, 1)
    e.texto(13.0, 4.6, "+"); e.texto(13.0, 3.0, "vo"); e.texto(13.0, 1.4, "−")
    # ---- setas de corrente
    if diag12:
        e.seta(0.75, 6, "right", "iVi", dy_rot=0.35)
        e.seta(4.4, 3.6, "right", "ipri", dy_rot=0.35)
        e.seta(6.5, 3.6, "right", "isec", dy_rot=0.35)
    if diag34:
        e.seta(0.75, 6, "right", "iVi", dy_rot=0.35)
        e.seta(4.4, 2.4, "right", "ipri", dy_rot=-0.35)
        e.seta(6.5, 2.4, "right", "isec", dy_rot=-0.35)
    if rl:
        e.seta(7, 3.0, "up", "iLo/2", dx_rot=-0.7)
        e.seta(8, 1.6, "up", "iLo/2", dx_rot=0.75)
    e.seta(9.3, 5, "right", "iLo", dy_rot=0.75)
    titulos = {1: "a) Primeira etapa (transferência de energia, S1 e S2 conduzem)",
               2: "b) Segunda etapa (roda livre, chaves bloqueadas)",
               3: "c) Terceira etapa (transferência de energia, S3 e S4 conduzem)",
               4: "d) Quarta etapa (roda livre, chaves bloqueadas)"}
    e.salvar(os.path.join(SAIDA, "etapas-fullbridge-%d.png" % etapa), titulos[etapa])


# =================================================================== Push-pull
def pushpull(etapa):
    """Etapas (D > 0,5): 1 = S1 e S2 (armazenamento); 2 = só S1; 3 = S1 e S2; 4 = só S2."""
    s1 = etapa in (1, 2, 3)
    s2 = etapa in (1, 3, 4)
    ambas = s1 and s2
    so1, so2 = s1 and not s2, s2 and not s1
    e = Esquema(12.0, 7.4)
    # ---- entrada e indutor
    e.ramo_v(0, 6, 0, "fonte", on=True, rotulo="Vi", lado=-0.45)
    e.fio([(0, 6), (0.5, 6)], True)
    e.ramo_h(6, 0.5, 2.3, "ind", on=True, rotulo="Lb", h=1.2)
    e.fio([(2.3, 6), (2.9, 6), (2.9, 3.6), (3.25, 3.6)], True)       # até a derivação central
    # ---- primário com derivação central (duas metades)
    e.bobina(3.25, 4.8, 3.6, +1, on=s2)      # metade superior (S2)
    e.bobina(3.25, 3.6, 2.4, +1, on=s1)      # metade inferior (S1)
    e.ponto(3.05, 4.75); e.ponto(3.05, 3.5)
    e.no(3.25, 3.6)
    e.nucleo(3.6, 4.9, 2.3)
    e.bobina(3.95, 4.8, 2.4, -1, on=not ambas)
    e.ponto(4.15, 4.75)
    # x1 -> S2 (passa por cima, cruzando o fio do indutor)
    e.fio([(3.25, 4.8), (3.25, 5.3)], s2)
    e.fio_salto([(3.25, 5.3), (1.4, 5.3)], 2.9, on=s2)
    e.ramo_v(1.4, 5.3, 0, "mosfet", on=s2, rotulo="S2", lado=0.3)
    # x2 -> S1
    e.fio([(3.25, 2.4), (2.3, 2.4)], s1)
    e.ramo_v(2.3, 2.4, 0, "mosfet", on=s1, rotulo="S1", lado=0.3)
    e.fio([(0, 0), (1.4, 0)], True)
    e.fio([(1.4, 0), (2.3, 0)], s1)
    e.no(1.4, 0)
    # ---- retificador
    e.fio([(3.95, 4.8), (5.2, 4.8)], not ambas)                          # p
    e.fio_salto([(3.95, 2.4), (6.2, 2.4)], 5.2, on=not ambas)            # q
    e.ramo_v(5.2, 6, 4.8, "diodo", on=so1, rotulo="D1", lado=-0.35, h=0.7)
    e.fio([(5.2, 4.8), (5.2, 1.6)], so2)
    e.ramo_v(5.2, 1.6, 0.6, "diodo", on=so2, rotulo="D4", lado=-0.35, h=0.7)
    e.ramo_v(6.2, 6, 2.4, "diodo", on=so2, rotulo="D3", lado=0.35, h=0.7)
    e.ramo_v(6.2, 2.4, 0.6, "diodo", on=so1, rotulo="D2", lado=0.35, h=0.7)
    e.fio([(5.2, 6), (6.2, 6)], so1)
    e.fio([(5.2, 0.6), (6.2, 0.6)], so2)
    e.fio([(6.2, 6), (7.4, 6)], not ambas)
    e.fio([(6.2, 0.6), (7.4, 0.6)], not ambas)
    for p in [(5.2, 4.8), (6.2, 2.4), (6.2, 6), (6.2, 0.6)]:
        e.no(*p)
    # ---- saída
    e.ramo_v(7.4, 6, 0.6, "cap", on=True, rotulo="Co", lado=0.3)
    e.fio([(7.4, 6), (8.6, 6)], True)
    e.fio([(7.4, 0.6), (8.6, 0.6)], True)
    e.ramo_v(8.6, 6, 0.6, "res", on=True, rotulo="Ro", lado=0.3)
    e.no(7.4, 6); e.no(7.4, 0.6)
    e.texto(9.9, 5.6, "+"); e.texto(9.9, 3.3, "vo"); e.texto(9.9, 1.0, "−")
    # ---- setas
    e.seta(1.4, 6, "right", "iLb", dy_rot=0.75)
    if s1:
        e.seta(2.3, 2.0, "down", "iS1", dx_rot=-0.5)
    if s2:
        e.seta(1.4, 4.4, "down", "iS2", dx_rot=-0.5)
    if so1:
        e.seta(4.6, 4.8, "right", "isec", dy_rot=0.35)
    if so2:
        e.seta(4.6, 2.4, "right", "isec", dy_rot=-0.35)
    if ambas:
        e.seta(8.0, 6, "right", "io", dy_rot=0.35)
        e.texto(8.0, 3.3, "Co\nalimenta\na carga", cor="#d62728", tam=7.5)
    titulos = {1: "a) Primeira etapa (armazenamento em Lb, S1 e S2 conduzem)",
               2: "b) Segunda etapa (transferência de energia, só S1 conduz)",
               3: "c) Terceira etapa (armazenamento em Lb, S1 e S2 conduzem)",
               4: "d) Quarta etapa (transferência de energia, só S2 conduz)"}
    e.salvar(os.path.join(SAIDA, "etapas-pushpull-%d.png" % etapa), titulos[etapa])


if __name__ == "__main__":
    for k in (1, 2, 3, 4):
        fullbridge(k)
        pushpull(k)
    print("8 figuras geradas em", SAIDA)
