"""Gera os modelos PLECS 5.0 do Trabalho 6 por edicao direta do texto .plecs.

Nao simula nada em Python. Le desenvolvimento/calculos/parametros.json, copia o
cabecalho de arquivo_exemplo.plecs (que permanece intacto), escreve componentes,
fios, sinais e terminais de saida de nivel superior, e grava:
  - <modelo>.plecs (quatro modelos)
  - modelos.json  (colunas exportadas por modelo, na ordem dos terminais de saida)
  - ensaios.json  (matriz de ensaios lida por resultados PLECS/executar_ensaios.py)
Os arquivos .plecs sao escritos somente com caracteres ASCII e quebras CRLF, porque
a gravacao pelo PLECS reinterpretou acentos no Trabalho 4.
Uso: python "simulação PLECS/gerar_modelos.py"
"""
from pathlib import Path
import json, re, math

ROOT = Path(__file__).resolve().parents[1]
SIM = Path(__file__).resolve().parent
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
S = P['simulacao']
BASE = SIM / 'arquivo_exemplo.plecs'


def q(s):
    t = json.dumps(str(s), ensure_ascii=True)
    assert t.isascii()
    return t


def par(k, v):
    return f'Parameter {{ Variable {q(k)} Value {q(v)} Show off }}'


class Modelo:
    def __init__(self, nome, init, x_saida=1900):
        self.nome = nome
        self.init = init
        self.x_saida = x_saida
        self.pos = {}
        self.comp = []          # (tipo, nome, texto)
        self.tipos = {}
        self.nets = {}
        self.sigs = {}
        self.saidas = []        # (indice, nome)

    def add(self, tipo, nome, x, y, params=None, direcao='right', extra=''):
        assert nome not in self.tipos, nome
        self.tipos[nome] = (tipo, params or {})
        self.pos[nome] = (int(x), int(y))
        txt = (f'Component {{ Type {tipo} Name {q(nome)} Show on Position [{int(x)}, {int(y)}] '
               f'Direction {direcao} Flipped off LabelPosition south '
               + ' '.join(par(k, v) for k, v in (params or {}).items()) + extra + ' }')
        self.comp.append(txt)

    def no(self, nome, *pinos):
        self.nets.setdefault(nome, []).extend(pinos)

    def sinal(self, origem, *destinos):
        self.sigs.setdefault(origem, []).extend(destinos)

    def saida(self, nome, origem):
        idx = len(self.saidas) + 1
        self.saidas.append((idx, nome))
        self.add('Output', nome, self.x_saida, 30 + 30 * idx, dict(Index=idx, Width=-1))
        self.sinal(origem, (nome, 1))

    def terminais(self, nome):
        tipo, p = self.tipos[nome]
        if tipo in ('ACVoltageSource', 'DCVoltageSource', 'Resistor', 'Inductor', 'Capacitor', 'Diode'):
            return [1, 2]
        if tipo in ('Voltmeter', 'Ammeter', 'MosfetWithDiode', 'Switch', 'Comparator'):
            return [1, 2, 3]
        if tipo in ('Ground', 'TriangleGenerator', 'Constant', 'Output'):
            return [1]
        if tipo == 'Transformer':
            return list(range(1, 2 * sum(int(x) for x in str(p['Windings']).strip('[]').split()) + 1))
        if tipo == 'CScript':
            return list(range(1, int(p['NumInputs']) + len(str(p['NumOutputs']).strip('[]').split()) + 1))
        raise KeyError(tipo)

    def verificar(self):
        """Todo terminal ligado (o PLECS recusa terminal solto sob fio ou bloco) e nenhum bloco sobre outro."""
        usados = set()
        for pinos in self.nets.values():
            usados.update(pinos)
        for o, d in self.sigs.items():
            usados.add(o)
            usados.update(d)
        soltos = [(c, t) for c in self.tipos for t in self.terminais(c) if (c, t) not in usados]
        assert not soltos, (self.nome, 'terminais sem ligacao', soltos)
        nomes = list(self.pos)
        for i, a in enumerate(nomes):
            for b in nomes[i + 1:]:
                (xa, ya), (xb, yb) = self.pos[a], self.pos[b]
                assert abs(xa - xb) >= 25 or abs(ya - yb) >= 25, (self.nome, 'blocos sobrepostos', a, b)

    def texto(self, opcoes):
        self.verificar()
        con = []
        for tipo, grupos in (('Wire', list(self.nets.values())), ('Signal', [[o, *d] for o, d in self.sigs.items()])):
            for pinos in grupos:
                assert len(pinos) >= 2, (self.nome, pinos)
                (c0, t0) = pinos[0]
                corpo = f'Type {tipo} SrcComponent {q(c0)} SrcTerminal {t0} '
                if len(pinos) == 2:
                    c1, t1 = pinos[1]
                    corpo += f'DstComponent {q(c1)} DstTerminal {t1}'
                else:
                    corpo += ' '.join(f'Branch {{ DstComponent {q(c)} DstTerminal {t} }}' for c, t in pinos[1:])
                con.append('Connection { ' + corpo + ' }')
        cab = BASE.read_text(encoding='utf-8').replace('\r\n', '\n').split('  Schematic {')[0]
        for chave, valor in dict(Name=self.nome, TimeSpan='Tstop', InitializationCommands=self.init, **opcoes).items():
            cab, n = re.subn(r'(?m)^  ' + chave + r'\s+"[^"\n]*"', lambda m: '  ' + chave + ' ' + q(valor), cab)
            assert n == 1, chave
        cab += ''.join(f'  Terminal {{ Type Output Index "{i}" }}\n' for i, _ in self.saidas)
        corpo = ('  Schematic { Location [40, 40; 1600, 900] ZoomFactor 0.7 SliderPosition [0, 0] ShowBrowser off BrowserWidth 100\n'
                 + '\n'.join('    ' + c for c in self.comp + con) + '\n  }\n}\n')
        txt = cab + corpo
        assert txt.isascii(), self.nome
        assert txt.count('{') == txt.count('}'), self.nome
        return txt

    def gravar(self, opcoes):
        caminho = SIM / f'{self.nome}.plecs'
        caminho.write_bytes(self.texto(opcoes).replace('\n', '\r\n').encode('ascii'))
        return caminho


# ---------------------------------------------------------------------------
# Blocos reutilizaveis
# ---------------------------------------------------------------------------
def rede_e_ponte(m, x0=40, y0=200):
    """Fonte, SS2, T1 1:1 ideal, ponte D1-D4, Rbus 0,1 ohm, C4 com ESR e voltimetro do barramento."""
    m.add('ACVoltageSource', 'Vrede', x0, y0 + 60, dict(V='sqrt(2)*Vrms', w='2*pi*fr', phi='phi_rede'), 'down')
    m.add('Voltmeter', 'Vm_rede', x0 - 30, y0 + 60, direcao='down')
    m.add('Ground', 'GND_rede', x0, y0 + 140)
    m.add('Switch', 'SS2', x0 + 60, y0, dict(s_init=1))
    m.add('Ammeter', 'Am_rede', x0 + 110, y0)
    m.add('Resistor', 'R_T1', x0 + 150, y0, dict(R='R_T1'))
    m.add('Transformer', 'T1', x0 + 200, y0 + 60, dict(Windings='[1 1]', n='[1 1]', Polarity='+', Lm='inf', im0=0))
    m.no('rede_f', ('Vrede', 1), ('Vm_rede', 1), ('SS2', 1))
    m.no('rede_n', ('Vrede', 2), ('Vm_rede', 2), ('GND_rede', 1), ('T1', 2))
    m.no('rede_ss2', ('SS2', 2), ('Am_rede', 1))
    m.no('rede_am', ('Am_rede', 2), ('R_T1', 1))
    m.no('rede_t1', ('R_T1', 2), ('T1', 1))
    # ponte: D1 e D4 conduzem no semiciclo positivo, D3 e D2 no negativo (Figura 2 da planilha)
    m.add('Ammeter', 'Am_D1', x0 + 280, y0 - 20, direcao='up')
    m.add('Diode', 'D1', x0 + 280, y0 - 60, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'up')
    m.add('Diode', 'D3', x0 + 330, y0 - 60, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'up')
    m.add('Diode', 'D2', x0 + 280, y0 + 120, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'up')
    m.add('Diode', 'D4', x0 + 330, y0 + 120, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'up')
    m.no('ca_a', ('T1', 3), ('Am_D1', 1), ('D2', 2))
    m.no('ca_d1', ('Am_D1', 2), ('D1', 1))
    m.no('ca_b', ('T1', 4), ('D3', 1), ('D4', 2))
    m.no('ponte_p', ('D1', 2), ('D3', 2), ('Am_ponte', 1))
    m.no('bus_n', ('D2', 1), ('D4', 1))
    m.add('Ammeter', 'Am_ponte', x0 + 380, y0 - 100)
    m.add('Resistor', 'Rbus', x0 + 420, y0 - 100, dict(R='Rbus'))
    m.no('ponte_r', ('Am_ponte', 2), ('Rbus', 1))
    m.no('bus_p', ('Rbus', 2))
    barramento(m, x0 + 470, y0)


def barramento(m, x, y):
    m.add('Ammeter', 'Am_C4', x, y - 40, direcao='down')
    m.add('Resistor', 'ESR_C4', x, y + 10, dict(R='ESR_C4'), 'down')
    m.add('Capacitor', 'C4', x, y + 60, dict(C='C4', v_init='Vbus0'), 'down')
    m.add('Voltmeter', 'Vm_bus', x + 40, y + 20, direcao='down')
    m.add('Ground', 'GND_bus', x + 20, y + 140)
    m.no('bus_p', ('Am_C4', 1), ('Vm_bus', 1))
    m.no('c4_a', ('Am_C4', 2), ('ESR_C4', 1))
    m.no('c4_b', ('ESR_C4', 2), ('C4', 1))
    m.no('bus_n', ('C4', 2), ('Vm_bus', 2), ('GND_bus', 1))


def conversor_cc(m, x0=620, y0=420, amortecedor=True):
    """Celula de tres estados com autotransformador, secundario 1:1 em ponte e C7 empilhado sobre C8 (Anexo 01).

    Com amortecedor=True, ramos RC (Rsn, Csn) em paralelo com S1, S2 e com o secundario de T32 representam a
    capacitancia de saida das chaves e evitam nos flutuantes quando a corrente de um ramo se anula (hipotese H)."""
    m.add('DCVoltageSource', 'Vbat', x0, y0 + 80, dict(V='Vbat'), 'up')
    m.add('Ammeter', 'Am_bat', x0, y0 + 20, direcao='up')
    m.add('Inductor', 'Lb', x0 + 40, y0 - 20, dict(L='Lb', i_init='ILb0'), 'up')
    m.add('Transformer', 'T32', x0 + 60, y0 - 90,
          dict(Windings='[2 1]', n='[1 1 1]', Polarity='+', Lm='T32_Lm', im0=0))
    # correntes iniciais coerentes com o corte indutivo Lb / Llk1 / Llk2 (metade de ILb0 em cada primario)
    for k, i0 in ((1, '-ILb0/2'), (2, 'ILb0/2'), (3, 0)):
        m.add('Inductor', f'Llk{k}', x0 - 60 + 80 * k, y0 - 170, dict(L='T32_Llk', i_init=i0))
        m.add('Resistor', f'Rw{k}', x0 - 20 + 80 * k, y0 - 170, dict(R='T32_R'))
    m.add('MosfetWithDiode', 'S1', x0 - 40, y0 + 20, dict(Ron='Ron_cc', s_init=0), 'up')
    m.add('MosfetWithDiode', 'S2', x0 + 140, y0 + 20, dict(Ron='Ron_cc', s_init=0), 'up')
    m.add('Ammeter', 'Am_S1', x0 - 40, y0 - 30, direcao='down')
    m.add('Ammeter', 'Am_S2', x0 + 140, y0 - 30, direcao='down')
    m.add('Voltmeter', 'Vm_S1', x0 - 80, y0 + 20, direcao='down')
    m.add('Diode', 'D17', x0 - 40, y0 - 230, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'up')
    m.add('Diode', 'D18', x0 + 140, y0 - 230, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'up')
    m.add('Ammeter', 'Am_D17', x0 - 40, y0 - 180, direcao='up')
    m.add('Capacitor', 'C8', x0 + 200, y0 - 120, dict(C='C8', v_init='VC8_0'), 'down')
    m.add('Capacitor', 'C7', x0 + 200, y0 - 260, dict(C='C7', v_init='VC7_0'), 'down')
    m.add('Voltmeter', 'Vm_C8', x0 + 240, y0 - 120, direcao='down')
    m.add('Voltmeter', 'Vm_C7', x0 + 240, y0 - 260, direcao='down')
    m.add('Ammeter', 'Am_sec', x0 + 100, y0 - 200)
    for nome, x, y in (('D13', 0, -330), ('D15', 0, -280), ('D14', 60, -330), ('D16', 60, -280)):
        m.add('Diode', nome, x0 + 300 + x, y0 + y, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'up')
    # bateria e indutor
    m.no('bus_n', ('Vbat', 2), ('S1', 2), ('S2', 2), ('Vm_S1', 2), ('C8', 2), ('Vm_C8', 2))
    m.no('bat_p', ('Vbat', 1), ('Am_bat', 1))
    m.no('bat_l', ('Am_bat', 2), ('Lb', 1))
    m.no('tap', ('Lb', 2), ('T32', 2), ('T32', 3))
    # enrolamento 1 (ponto no lado de S1) e enrolamento 2 (ponto na derivacao central): serie aditiva
    m.no('w1a', ('T32', 1), ('Llk1', 2))
    m.no('w1b', ('Llk1', 1), ('Rw1', 2))
    m.no('s1', ('Rw1', 1), ('Am_S1', 1), ('Vm_S1', 1), ('Am_D17', 1))
    m.no('s1d', ('Am_S1', 2), ('S1', 1))
    m.no('w2a', ('T32', 4), ('Llk2', 1))
    m.no('w2b', ('Llk2', 2), ('Rw2', 1))
    m.no('s2', ('Rw2', 2), ('Am_S2', 1), ('D18', 1))
    m.no('s2d', ('Am_S2', 2), ('S2', 1))
    m.no('d17', ('Am_D17', 2), ('D17', 1))
    m.no('meio', ('D17', 2), ('D18', 2), ('C8', 1), ('Vm_C8', 1), ('C7', 2), ('Vm_C7', 2), ('D15', 1), ('D16', 1))
    m.no('bus_p', ('C7', 1), ('Vm_C7', 1), ('D13', 2), ('D14', 2))
    # secundario em ponte
    m.no('w3a', ('T32', 5), ('Llk3', 1))
    m.no('w3b', ('Llk3', 2), ('Rw3', 1))
    m.no('w3c', ('Rw3', 2), ('Am_sec', 1))
    m.no('sec_a', ('Am_sec', 2), ('D13', 1), ('D15', 2))
    m.no('sec_b', ('T32', 6), ('D14', 1), ('D16', 2))
    if amortecedor:
        for nome, x, y, a, b in (('S1', x0 - 130, y0 - 10, 's1', 'bus_n'), ('S2', x0 + 190, y0 + 20, 's2', 'bus_n'),
                                 ('sec', x0 + 420, y0 - 330, 'sec_a', 'sec_b')):
            m.add('Resistor', f'Rsn_{nome}', x, y, dict(R='Rsn'), 'down')
            m.add('Capacitor', f'Csn_{nome}', x, y + 60, dict(C='Csn', v_init=0), 'down')
            m.no(a, (f'Rsn_{nome}', 1))
            m.no(f'sn_{nome}', (f'Rsn_{nome}', 2), (f'Csn_{nome}', 1))
            m.no(b, (f'Csn_{nome}', 2))


def pwm_cc(m, origem_dref, x0=300, y0=700):
    """Duas dentes de serra de fsb defasadas de 180 graus; gate ligado enquanto dref > portadora."""
    m.add('TriangleGenerator', 'Serra_S1', x0, y0, dict(Min=0, Max=1, f='fsb', DutyCycle=1, Delay=0))
    m.add('TriangleGenerator', 'Serra_S2', x0, y0 + 60, dict(Min=0, Max=1, f='fsb', DutyCycle=1, Delay='0.5/fsb'))
    m.add('Comparator', 'PWM_S1', x0 + 80, y0)
    m.add('Comparator', 'PWM_S2', x0 + 80, y0 + 60)
    m.sinal(origem_dref, ('PWM_S1', 1), ('PWM_S2', 1))
    m.sinal(('Serra_S1', 1), ('PWM_S1', 2))
    m.sinal(('Serra_S2', 1), ('PWM_S2', 2))
    m.sinal(('PWM_S1', 3), ('S1', 3))
    m.sinal(('PWM_S2', 3), ('S2', 3))


def inversor(m, x0=900, y0=200):
    for nome, x, y in (('QA_sup', 60, -60), ('QA_inf', 60, 80), ('QB_sup', 0, -60), ('QB_inf', 0, 80)):
        m.add('MosfetWithDiode', nome, x0 + x, y0 + y, dict(Ron='Ron_inv', s_init=0), 'up')
    m.add('Ammeter', 'Am_QA', x0 + 60, y0 - 110, direcao='up')
    m.add('Voltmeter', 'Vm_AB', x0 + 30, y0 + 160)
    m.add('Ammeter', 'Am_Lo', x0 + 110, y0 + 10)
    m.add('Inductor', 'Lo', x0 + 160, y0 + 10, dict(L='Lo', i_init=0))
    m.add('Resistor', 'ESR_Co', x0 + 210, y0 + 50, dict(R='ESR_Co'), 'down')
    m.add('Capacitor', 'Co', x0 + 210, y0 + 100, dict(C='Co', v_init=0), 'down')
    m.add('Voltmeter', 'Vm_o', x0 + 250, y0 + 70, direcao='down')
    m.add('Ammeter', 'Am_o', x0 + 290, y0 + 10)
    m.no('bus_p', ('Am_QA', 1), ('QB_sup', 1))
    m.no('qa_d', ('Am_QA', 2), ('QA_sup', 1))
    m.no('bus_n', ('QA_inf', 2), ('QB_inf', 2))
    m.no('perna_A', ('QA_sup', 2), ('QA_inf', 1), ('Vm_AB', 1), ('Am_Lo', 1))
    m.no('perna_B', ('QB_sup', 2), ('QB_inf', 1), ('Vm_AB', 2), ('Co', 2), ('Vm_o', 2))
    m.no('lo_a', ('Am_Lo', 2), ('Lo', 1))
    m.no('saida', ('Lo', 2), ('ESR_Co', 1), ('Vm_o', 1), ('Am_o', 1))
    m.no('co_a', ('ESR_Co', 2), ('Co', 1))
    m.no('carga', ('Am_o', 2), ('Sw_res', 1), ('Sw_nl', 1), ('Sw_rl', 1))
    # cargas: resistiva, nao linear (Anexo 01) e RL de 3 kVA com FP 0,7
    m.add('Switch', 'Sw_res', x0 + 340, y0 + 40, dict(s_init=0), 'down')
    m.add('Resistor', 'R_res', x0 + 340, y0 + 100, dict(R='Rres'), 'down')
    m.no('res_a', ('Sw_res', 2), ('R_res', 1))
    m.add('Switch', 'Sw_rl', x0 + 400, y0 + 40, dict(s_init=0), 'down')
    m.add('Resistor', 'R_rl', x0 + 400, y0 + 90, dict(R='R3k'), 'down')
    m.add('Inductor', 'L_rl', x0 + 400, y0 + 140, dict(L='L3k', i_init=0), 'down')
    m.no('rl_a', ('Sw_rl', 2), ('R_rl', 1))
    m.no('rl_b', ('R_rl', 2), ('L_rl', 1))
    m.add('Switch', 'Sw_nl', x0 + 460, y0 + 10)
    m.add('Resistor', 'Rs_nl', x0 + 510, y0 + 10, dict(R='nl_Rs'))
    for nome, x, y in (('Dn1', 560, -20), ('Dn3', 610, -20), ('Dn2', 560, 120), ('Dn4', 610, 120)):
        m.add('Diode', nome, x0 + x, y0 + y, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'up')
    m.add('Resistor', 'ESR_nl', x0 + 670, y0 + 30, dict(R='nl_ESR'), 'down')
    m.add('Capacitor', 'C_nl', x0 + 670, y0 + 80, dict(C='nl_C', v_init='VC3_0'), 'down')
    m.add('Resistor', 'R_nl', x0 + 720, y0 + 50, dict(R='nl_R'), 'down')
    m.add('Voltmeter', 'Vm_nl', x0 + 760, y0 + 50, direcao='down')
    m.no('nl_a', ('Sw_nl', 2), ('Rs_nl', 1))
    m.no('nl_ca', ('Rs_nl', 2), ('Dn1', 1), ('Dn2', 2))
    m.no('perna_B', ('R_res', 2), ('L_rl', 2), ('Dn3', 1), ('Dn4', 2))
    m.no('nl_p', ('Dn1', 2), ('Dn3', 2), ('ESR_nl', 1), ('R_nl', 1), ('Vm_nl', 1))
    m.no('nl_esr', ('ESR_nl', 2), ('C_nl', 1))
    m.no('nl_n', ('Dn2', 1), ('Dn4', 1), ('C_nl', 2), ('R_nl', 2), ('Vm_nl', 2))


def modulador(m, origem_vc, x0=900, y0=600):
    """Unipolar: portadoras triangulares +-Vd em fs, a segunda atrasada de meio periodo (180 graus)."""
    m.add('TriangleGenerator', 'Portadora_A', x0, y0, dict(Min='-Vd', Max='Vd', f='fs', DutyCycle=0.5, Delay=0))
    m.add('TriangleGenerator', 'Portadora_B', x0, y0 + 100, dict(Min='-Vd', Max='Vd', f='fs', DutyCycle=0.5, Delay='0.5/fs'))
    for nome, y in (('CMP_A_sup', -20), ('CMP_A_inf', 20), ('CMP_B_inf', 80), ('CMP_B_sup', 120)):
        m.add('Comparator', nome, x0 + 100, y0 + y)
    m.sinal(origem_vc, ('CMP_A_sup', 1), ('CMP_A_inf', 2), ('CMP_B_inf', 1), ('CMP_B_sup', 2))
    m.sinal(('Portadora_A', 1), ('CMP_A_sup', 2), ('CMP_A_inf', 1))
    m.sinal(('Portadora_B', 1), ('CMP_B_inf', 2), ('CMP_B_sup', 1))
    m.sinal(('CMP_A_sup', 3), ('QA_sup', 3))
    m.sinal(('CMP_A_inf', 3), ('QA_inf', 3))
    m.sinal(('CMP_B_inf', 3), ('QB_inf', 3))
    m.sinal(('CMP_B_sup', 3), ('QB_sup', 3))


DECL = r'''#include <math.h>
/* Compensador Tipo 3 da planilha: Cv(s) = Kc (s+wz1)(s+wz2) / (s (s+wp1)(s+wp2)).
   Estados em volts: x0 = Kc*integral(e); x1 e x2 = filtros dos dois avancos. */
#define HV      ParamRealData(0,0)
#define KC      ParamRealData(1,0)
#define WZ1     ParamRealData(2,0)
#define WZ2     ParamRealData(3,0)
#define WP1     ParamRealData(4,0)
#define WP2     ParamRealData(5,0)
#define VREFPK  ParamRealData(6,0)
#define WO      ParamRealData(7,0)
#define VSAT    ParamRealData(8,0)
#define TFALTA  ParamRealData(9,0)
#define TRET    ParamRealData(10,0)
#define MODOCC  ParamRealData(11,0)
#define TDET    ParamRealData(12,0)
#define DB      ParamRealData(13,0)
#define CARGA   ParamRealData(14,0)
#define TCARGA  ParamRealData(15,0)
#define Y1 (ContState(0))
#define Y2 (Y1 + (WZ1/WP1 - 1.0)*ContState(1))
#define Y3 (Y2 + (WZ2/WP2 - 1.0)*ContState(2))
#define VREF (VREFPK*sin(WO*CurrentTime))
static double limita(double u, double l) { return u > l ? l : (u < -l ? -l : u); }
'''
START = 'ContState(0) = 0.0;\nContState(1) = 0.0;\nContState(2) = 0.0;'
OUTPUT = r'''double t = CurrentTime;
double u = Y3;
int rede = (t < TFALTA) || (t >= TRET);
int cc = (MODOCC > 0.5) ? 1 : ((t >= TFALTA + TDET) && (t < TRET));
int liga = (t >= TCARGA);
OutputSignal(0,0) = limita(u, VSAT);
OutputSignal(1,0) = VREF;
OutputSignal(2,0) = rede ? 1.0 : 0.0;
OutputSignal(3,0) = cc ? DB : -1.0;
OutputSignal(4,0) = (liga && fabs(CARGA - 1.0) < 0.5) ? 1.0 : 0.0;
OutputSignal(5,0) = (liga && fabs(CARGA - 2.0) < 0.5) ? 1.0 : 0.0;
OutputSignal(6,0) = (liga && fabs(CARGA - 3.0) < 0.5) ? 1.0 : 0.0;
OutputSignal(7,0) = u;
ZCSignal(0) = t - TFALTA;
ZCSignal(1) = t - TRET;
ZCSignal(2) = t - TFALTA - TDET;
ZCSignal(3) = t - TCARGA;
ZCSignal(4) = u - VSAT;
ZCSignal(5) = u + VSAT;'''
DERIV = r'''double e = VREF - HV*InputSignal(0,0);
double u = Y3;
int trava = (u > VSAT && e > 0.0) || (u < -VSAT && e < 0.0);
ContDeriv(0) = trava ? 0.0 : KC*e;
ContDeriv(1) = WP1*(Y1 - ContState(1));
ContDeriv(2) = WP2*(Y2 - ContState(2));'''
CS_PARAMS = 'Hv,Kc,wz1,wz2,wp1,wp2,Vref_pk,2*pi*fo,Vsat,tfalta,tretorno,modo_cc,tdet,Db,carga,tcarga'


def controle(m, x0=1200, y0=700):
    m.add('CScript', 'Controle', x0, y0, dict(
        NumInputs=1, NumOutputs='[1 1 1 1 1 1 1 1]', NumContStates=3, NumDiscStates=0, NumZCSignals=6,
        DirectFeedthrough=0, Ts=0, Parameters=CS_PARAMS, LangStandard=2, GnuExtensions=2, RuntimeCheck=2,
        Declarations=DECL, StartFcn=START, OutputFcn=OUTPUT, DerivativeFcn=DERIV, UpdateFcn='', TerminateFcn=''))
    m.sinal(('Vm_o', 3), ('Controle', 1))
    # terminais de saida do C-Script: 2 vc, 3 vref, 4 rede, 5 dref_cc, 6 g_res, 7 g_nl, 8 g_rl, 9 vc sem limite
    m.sinal(('Controle', 6), ('Sw_res', 3))
    m.sinal(('Controle', 7), ('Sw_nl', 3))
    m.sinal(('Controle', 8), ('Sw_rl', 3))


# ---------------------------------------------------------------------------
# Comandos de inicializacao (valores padrao; ModelVars do executor sobrescrevem)
# ---------------------------------------------------------------------------
cp = S['comp']


def comum():
    return (f"fs={S['fs']:.10g}; fsb={S['fs']:.10g}; fr={S['fr']:.10g}; fo={S['fo']:.10g};\n"
            f"Lo={S['Lo']:.10g}; Co={S['Co']:.10g}; ESR_Co={S['ESR_Co']:.10g}; Ro={S['Ro']:.10g};\n"
            f"R3k={S['R3k']:.10g}; L3k={S['L3k']:.10g}; nl_Rs={S['nl_Rs']:.10g}; nl_C={S['nl_C']:.10g}; nl_ESR={S['nl_ESR']:.10g}; nl_R={S['nl_R']:.10g};\n"
            f"C4={S['C4']:.10g}; ESR_C4={S['ESR_C4']:.10g}; Rbus={S['Rbus']:.10g}; R_T1=0.002;\n"
            f"Vf_ponte={S['Vf_ponte']:.10g}; Ron_ponte={S['Ron_ponte']:.10g}; Vf_rapido={S['Vf_rapido']:.10g}; Ron_rapido={S['Ron_rapido']:.10g};\n"
            f"Ron_inv={S['Ron_inv']:.10g}; Ron_cc={S['Ron_cc']:.10g}; Lb={S['Lb']:.10g}; C7={S['C7']:.10g}; C8={S['C8']:.10g};\n"
            f"T32_Lm={S['T32_Lm']:.10g}; T32_Llk={S['T32_Llk']:.10g}; T32_R={S['T32_R']:.10g};\n"
            f"Hv={S['Hv']:.12g}; Vd={S['Vd']:.10g}; Vref_pk={S['Vref_pk']:.10g}; Vsat={S['Vsat_comp']:.10g};\n"
            f"Kc={cp['Kc']:.12g}; wz1={cp['wz1']:.12g}; wz2={cp['wz2']:.12g}; wp1={cp['wp1']:.12g}; wp2={cp['wp2']:.12g};\n")


def cc_extra():
    return f"Rsn={S['Rsn_cc']:.10g}; Csn={S['Csn_cc']:.10g};\n"


CENARIO = ("% Variaveis de cenario (sobrescritas por ModelVars):\n"
           "Vrms=220; phi_rede=0; Vcc=373.352; carga=1; Rres=6.297619; tcarga=0;\n"
           "tfalta=10; tretorno=100; tdet=0; modo_cc=0; Vbat=42; Db=0.7; Rcarga=19.6;\n"
           "Vbus0=310; VC8_0=206; VC7_0=103; ILb0=0; VC3_0=140; Tstop=0.2;\n")
CAB = '% Trabalho 6 - no-break de dupla conversao 3 kVA. Gerado por gerar_modelos.py; unidades SI.\n'
OPC = dict(Solver=S['solver']['Solver'], MaxStep=f"{S['solver']['MaxStep']:g}", RelTol=f"{S['solver']['RelTol']:g}",
           AbsTol=f"{S['solver']['AbsTol']:g}")


def modelo_retificador():
    m = Modelo('retificador_barramento', CAB + comum() + CENARIO, x_saida=1500)
    rede_e_ponte(m)
    m.add('Resistor', 'R_eq', 620, 260, dict(R='Rcarga'), 'down')
    m.no('bus_p', ('R_eq', 1))
    m.no('bus_n', ('R_eq', 2))
    m.add('Constant', 'SS2_fechada', 40, 120, dict(Value=1, DataType=10))
    m.sinal(('SS2_fechada', 1), ('SS2', 3))
    for nome, o in (('v_rede_V', ('Vm_rede', 3)), ('i_rede_A', ('Am_rede', 3)), ('i_D1_A', ('Am_D1', 3)),
                    ('i_ponte_A', ('Am_ponte', 3)), ('i_C4_A', ('Am_C4', 3)), ('v_bus_V', ('Vm_bus', 3))):
        m.saida(nome, o)
    return m


def modelo_elevador(nome='elevador_bateria', amortecedor=True):
    m = Modelo(nome, CAB + comum() + cc_extra() + CENARIO)
    barramento(m, 900, 300)
    conversor_cc(m, amortecedor=amortecedor)
    m.add('Resistor', 'R_eq', 980, 320, dict(R='Rcarga'), 'down')
    m.no('bus_p', ('R_eq', 1))
    m.no('bus_n', ('R_eq', 2))
    m.add('Constant', 'Dref', 200, 700, dict(Value='Db', DataType=10))
    pwm_cc(m, ('Dref', 1))
    for nome, o in (('v_bus_V', ('Vm_bus', 3)), ('i_bat_A', ('Am_bat', 3)), ('v_C8_V', ('Vm_C8', 3)),
                    ('v_C7_V', ('Vm_C7', 3)), ('v_S1_V', ('Vm_S1', 3)), ('i_S1_A', ('Am_S1', 3)),
                    ('i_S2_A', ('Am_S2', 3)), ('i_D17_A', ('Am_D17', 3)), ('i_sec_A', ('Am_sec', 3)),
                    ('i_C4_A', ('Am_C4', 3)), ('gate_S1', ('PWM_S1', 3))):
        m.saida(nome, o)
    return m


def modelo_inversor():
    m = Modelo('inversor_malha_fechada', CAB + comum() + CENARIO)
    m.add('DCVoltageSource', 'Vcc', 820, 220, dict(V='Vcc'), 'down')
    m.add('Voltmeter', 'Vm_bus', 780, 220, direcao='down')
    m.add('Ground', 'GND_bus', 820, 320)
    m.no('bus_p', ('Vcc', 1), ('Vm_bus', 1))
    m.no('bus_n', ('Vcc', 2), ('Vm_bus', 2), ('GND_bus', 1))
    inversor(m)
    controle(m)
    modulador(m, ('Controle', 2))
    for nome, o in (('v_o_V', ('Vm_o', 3)), ('i_o_A', ('Am_o', 3)), ('i_Lo_A', ('Am_Lo', 3)),
                    ('v_c_V', ('Controle', 2)), ('v_ref_V', ('Controle', 3)), ('v_c_livre_V', ('Controle', 9)),
                    ('v_AB_V', ('Vm_AB', 3)), ('i_QA_A', ('Am_QA', 3)), ('v_nl_V', ('Vm_nl', 3)), ('v_bus_V', ('Vm_bus', 3)),
                    ('rede_on', ('Controle', 4)), ('dref_cc', ('Controle', 5))):
        m.saida(nome, o)
    return m


def modelo_completo():
    m = Modelo('nobreak_completo', CAB + comum() + cc_extra() + CENARIO)
    rede_e_ponte(m)
    conversor_cc(m, 200, 850)
    inversor(m)
    controle(m)
    modulador(m, ('Controle', 2))
    pwm_cc(m, ('Controle', 5), 700, 950)
    m.sinal(('Controle', 4), ('SS2', 3))
    for nome, o in (('v_rede_V', ('Vm_rede', 3)), ('i_rede_A', ('Am_rede', 3)), ('i_D1_A', ('Am_D1', 3)),
                    ('i_ponte_A', ('Am_ponte', 3)), ('i_C4_A', ('Am_C4', 3)), ('v_bus_V', ('Vm_bus', 3)),
                    ('i_bat_A', ('Am_bat', 3)), ('v_C8_V', ('Vm_C8', 3)), ('v_C7_V', ('Vm_C7', 3)),
                    ('i_S1_A', ('Am_S1', 3)), ('v_S1_V', ('Vm_S1', 3)),
                    ('v_o_V', ('Vm_o', 3)), ('i_o_A', ('Am_o', 3)), ('i_Lo_A', ('Am_Lo', 3)),
                    ('v_c_V', ('Controle', 2)), ('v_ref_V', ('Controle', 3)), ('v_c_livre_V', ('Controle', 9)),
                    ('rede_on', ('Controle', 4)), ('dref_cc', ('Controle', 5)), ('v_nl_V', ('Vm_nl', 3)),
                    ('i_QA_A', ('Am_QA', 3)), ('i_S2_A', ('Am_S2', 3)), ('i_D17_A', ('Am_D17', 3)),
                    ('i_sec_A', ('Am_sec', 3)), ('v_AB_V', ('Vm_AB', 3))):
        m.saida(nome, o)
    return m


# ---------------------------------------------------------------------------
# Matriz de ensaios
# ---------------------------------------------------------------------------
R = P['retificador']
INV = P['inversor']
Ro = INV['Ro']
Vf2 = 2 * S['Vf_ponte']
T60 = 1 / 60


def grade(*faixas):
    """Lista de faixas [inicio, fim, passo] para a grade de saida."""
    return [[round(a, 9), round(b, 9), p] for a, b, p in faixas]


# Limite de tempo de relogio por simulacao (SolverOpts.Timeout, em segundos). Nao altera o resultado e por isso
# fica fora da assinatura das opcoes; serve para que uma simulacao travada termine com erro registrado.
TIMEOUT = dict(retificador_barramento=300, elevador_bateria=600, elevador_sem_amortecedor=600,
               inversor_malha_fechada=600, nobreak_completo=1200)


def ens(modelo, descricao, mv, tstop, faixas, maxstep=None, reltol=None, janelas=None, grupo='forma_de_onda', timeout=None):
    e = dict(modelo=modelo, descricao=descricao, ModelVars=dict(mv, Tstop=tstop), TimeSpan=tstop, grade=grade(*faixas),
             janelas=janelas or {}, grupo=grupo, Timeout=timeout or TIMEOUT[modelo])
    if maxstep:
        e['MaxStep'] = maxstep
    if reltol:
        e['RelTol'] = reltol
    return e


E = {}
# Diagnostico do CC-CC (executado antes dos demais): o elev_42 sem amortecedores ficou mais de 5 min sem
# terminar no PLECS, embora 2 ms tenham levado 0,125 s. Compara o modelo sem e com ramos RC, em regime e
# na partida com corrente nula (ramos em conducao descontinua), com limite de 90 s cada.
MV_CC = dict(Vbat=42.0, Db=0.7, Rcarga=round(210 ** 2 / 2250, 6), ILb0=round(2250 / 42.0, 4), Vbus0=210.0, VC8_0=140.0, VC7_0=70.0)
for nome, modelo, extra, tstop in (('diag_cc_sem_5ms', 'elevador_sem_amortecedor', {}, 0.005),
                                   ('diag_cc_sem_20ms', 'elevador_sem_amortecedor', {}, 0.02),
                                   ('diag_cc_sem_partida_5ms', 'elevador_sem_amortecedor', dict(ILb0=0.0), 0.005),
                                   ('diag_cc_amort_20ms', 'elevador_bateria', {}, 0.02),
                                   ('diag_cc_amort_partida_5ms', 'elevador_bateria', dict(ILb0=0.0), 0.005)):
    E[nome] = ens(modelo, f"Diagnostico do CC-CC ({'sem' if 'sem' in modelo else 'com'} amortecedores RC), "
                  f"{tstop * 1e3:.0f} ms, corrente inicial em Lb de {dict(MV_CC, **extra)['ILb0']:.1f} A",
                  dict(MV_CC, **extra), tstop, [(0.0, tstop, 1e-5)], janelas=dict(final=[tstop - 0.001, tstop]),
                  grupo='diagnostico', timeout=90)
# Retificador isolado: condicoes ideais da planilha e condicoes do Anexo 01
Vmed176 = R['planilha']['VC1medio']
for nome, V, ideal in (('ret_176_planilha', 176.0, True), ('ret_176_anexo', 176.0, False), ('ret_264_anexo', 264.0, False)):
    Vmed = Vmed176 if V == 176 else (R['vales_com_1880uF']['264']['Vpico'] + R['vales_com_1880uF']['264']['Vvale']) / 2
    mv = dict(Vrms=V, Rcarga=round(Vmed ** 2 / P['Prec'], 6), Vbus0=round(math.sqrt(2) * V - (0 if ideal else Vf2), 4))
    if ideal:
        mv.update(C4=R['planilha']['C1_F'], ESR_C4=1e-6, Rbus=1e-6, Vf_ponte=0.0, Ron_ponte=1e-4)
    E[nome] = ens('retificador_barramento', ('Retificador ideal da secao 3' if ideal else 'Retificador com 1880 uF, ESR, 0,1 ohm e diodos reais') +
                  f' a {V:.0f} V, carga equivalente a 2250 W', mv, 0.15, [(0.0, 0.15, 1e-5), (0.1, 0.11, 2e-6)],
                  janelas=dict(regime=[0.1, 0.15]), grupo='submodelo')
# Elevador isolado
for nome, Vb, D in (('elev_42', 42.0, 0.7), ('elev_56', 56.0, P['cc_cc']['planilha']['D_56'])):
    mv = dict(Vbat=Vb, Db=round(D, 6), Rcarga=round(210 ** 2 / 2250, 6), ILb0=round(2250 / Vb, 4), Vbus0=210.0, VC8_0=140.0, VC7_0=70.0)
    E[nome] = ens('elevador_bateria', f'CC-CC em malha aberta, bateria de {Vb:.0f} V, D = {D:.2f}, carga de 2250 W em 210 V',
                  mv, 0.1, [(0.0, 0.1, 1e-5), (0.098, 0.1, 2.5e-7)], janelas=dict(regime=[0.08, 0.1], detalhe=[0.098, 0.1]),
                  grupo='submodelo')
# Inversor com barramento ideal
pico5 = 5.25 * T60
for nome, Vcc, carga, desc in (('inv_373_res', 373.352, 1, '2100 W resistiva'), ('inv_2116_res', R['Vimin_cc'], 1, '2100 W resistiva'),
                               ('inv_373_vazio', 373.352, 0, 'vazio'), ('inv_2116_vazio', R['Vimin_cc'], 0, 'vazio'),
                               ('inv_2116_nl', R['Vimin_cc'], 2, 'carga nao linear do Anexo 01')):
    E[nome] = ens('inversor_malha_fechada', f'Inversor com barramento ideal de {Vcc:.2f} V, {desc}',
                  dict(Vcc=round(Vcc, 4), carga=carga, Rres=round(Ro, 6), tcarga=0), 0.1,
                  [(0.0, 0.1, 1e-5), (pico5 - 0.001, pico5 + 0.001, 2.5e-7)],
                  janelas=dict(regime=[0.05, 0.1], detalhe=[pico5 - 0.001, pico5 + 0.001]), grupo='submodelo')
tdeg = 3.25 * T60
E['inv_degrau_2116'] = ens('inversor_malha_fechada', 'Inversor a 211,57 V, degrau de vazio para 2100 W no pico da tensao',
                           dict(Vcc=round(R['Vimin_cc'], 4), carga=1, Rres=round(Ro, 6), tcarga=round(tdeg, 7)), 0.1,
                           [(0.0, 0.1, 1e-5), (tdeg - 0.001, tdeg + 0.004, 1e-6)],
                           janelas=dict(antes=[tdeg - 2 * T60, tdeg], depois=[tdeg + 2 * T60, tdeg + 4 * T60], degrau=[tdeg, tdeg + 0.004]),
                           grupo='submodelo')
# No-break completo: rede ate tfalta (cruzamento por zero), bateria depois
tf = 0.1


def nb(V, carga, extra=None, tstop=0.2):
    mv = dict(Vrms=V, phi_rede=0, carga=carga, Rres=round(Ro, 6), tcarga=0, tfalta=tf, tretorno=100, tdet=0, modo_cc=0,
              Vbat=42.0, Db=0.7, Vbus0=round(math.sqrt(2) * V - Vf2, 4), ILb0=0, VC3_0=140.0)
    mv['VC8_0'] = round(2 * mv['Vbus0'] / 3, 4)
    mv['VC7_0'] = round(mv['Vbus0'] / 3, 4)
    mv.update(extra or {})
    return mv


JAN_NB = dict(rede=[4 * T60, 6 * T60], bateria=[10 * T60, 12 * T60], transferencia=[tf - 0.005, tf + 0.02],
              detalhe_rede=[5.25 * T60 - 0.001, 5.25 * T60 + 0.001], detalhe_bateria=[11.25 * T60 - 0.001, 11.25 * T60 + 0.001])
FAIXAS_NB = [(0.0, 0.2, 2e-5), (5.25 * T60 - 0.001, 5.25 * T60 + 0.001, 5e-7), (11.25 * T60 - 0.001, 11.25 * T60 + 0.001, 5e-7),
             (tf - 0.001, tf + 0.004, 1e-6)]
nomes_carga = {1: 'resistiva 2100 W', 2: 'nao linear do Anexo 01', 3: 'RL de 3 kVA com FP 0,7'}
for V, carga, nome in ((176, 2, 'nb_176_nl'), (264, 1, 'nb_264_lin'), (264, 2, 'nb_264_nl'), (220, 1, 'nb_220_lin'),
                       (220, 2, 'nb_220_nl'), (176, 1, 'nb_176_lin'), (220, 3, 'nb_220_rl3k')):
    E[nome] = ens('nobreak_completo', f'Rede de {V} V com carga {nomes_carga[carga]}; falta da rede em 0,1 s (cruzamento por zero)',
                  nb(float(V), carga), 0.2, FAIXAS_NB, janelas=JAN_NB, grupo='secao_6')
E['nb_176_nl_anexo'] = ens('nobreak_completo', 'Como nb_176_nl, mas com o CC-CC sempre comandado (D = 0,7), como no circuito PSIM do Anexo 01',
                           nb(176.0, 2, dict(modo_cc=1)), 0.2, FAIXAS_NB, janelas=JAN_NB, grupo='secao_6')
tp = tf + 0.25 * T60
E['nb_176_nl_pico'] = ens('nobreak_completo', 'Como nb_176_nl, com a falta no pico positivo da tensao da rede',
                          nb(176.0, 2, dict(tfalta=round(tp, 7))), 0.2,
                          [(0.0, 0.2, 2e-5), (tp - 0.001, tp + 0.004, 1e-6), (11.25 * T60 - 0.001, 11.25 * T60 + 0.001, 5e-7)],
                          janelas=dict(JAN_NB, transferencia=[tp - 0.005, tp + 0.02]), grupo='secao_6')
E['nb_220_retorno'] = ens('nobreak_completo', 'Rede de 220 V, resistiva; falta em 0,1 s e retorno em 0,2 s, ambos no cruzamento por zero',
                          nb(220.0, 1, dict(tretorno=0.2)), 0.3,
                          [(0.0, 0.3, 2e-5), (0.199, 0.21, 1e-6)],
                          janelas=dict(rede=[4 * T60, 6 * T60], bateria=[10 * T60, 12 * T60], retorno=[0.2, 0.22], apos_retorno=[16 * T60, 18 * T60]),
                          grupo='secao_6')
E['conv_176_nl'] = ens('nobreak_completo', 'Refinamento numerico de nb_176_nl (passo maximo 1 us, RelTol 1e-7)',
                       nb(176.0, 2), 0.2, FAIXAS_NB, maxstep=1e-6, reltol=1e-7, janelas=JAN_NB, grupo='verificacao')
# Curvas de regulacao Vo = f(Po): rede presente, carga resistiva, janela de 6 ciclos
POTS = [0, 210, 420, 630, 840, 1050, 1260, 1470, 1680, 1890, 2100]
for V in (176, 220, 264):
    for Pw in POTS:
        mv = nb(float(V), 1 if Pw else 0, dict(tfalta=100, Rres=round(115.0 ** 2 / Pw, 6) if Pw else 1e6))
        E[f'reg_{V}_{Pw:04d}'] = ens('nobreak_completo', f'Regulacao: rede {V} V, carga resistiva nominal de {Pw} W',
                                     mv, 0.2, [(0.1, 0.2, 4e-5)], janelas=dict(regime=[0.1, 0.2]), grupo='regulacao')
for Pw in POTS:
    mv = nb(220.0, 1 if Pw else 0, dict(tfalta=0, Rres=round(115.0 ** 2 / Pw, 6) if Pw else 1e6, Vbus0=210.0, VC8_0=140.0, VC7_0=70.0,
                                        ILb0=round(Pw / 0.95 / 42, 4)))
    E[f'reg_bat_{Pw:04d}'] = ens('nobreak_completo', f'Regulacao em modo bateria (42 V, D = 0,7), carga resistiva nominal de {Pw} W',
                                 mv, 0.2, [(0.1, 0.2, 4e-5)], janelas=dict(regime=[0.1, 0.2]), grupo='regulacao_bateria')

if __name__ == '__main__':
    modelos = [modelo_retificador(), modelo_elevador(), modelo_elevador('elevador_sem_amortecedor', False),
               modelo_inversor(), modelo_completo()]
    info = {}
    for m in modelos:
        caminho = m.gravar(OPC)
        info[m.nome] = dict(arquivo=caminho.name, colunas=['tempo_s'] + [n for _, n in m.saidas],
                            componentes=len(m.comp), fios=len(m.nets), sinais=len(m.sigs))
        print(f'{caminho.name}: {len(m.comp)} componentes, {len(m.nets)} nos, {len(m.saidas)} saidas')
    (SIM / 'modelos.json').write_text(json.dumps(dict(solver=OPC, modelos=info), indent=1, ensure_ascii=False), encoding='utf-8')
    (SIM / 'ensaios.json').write_text(json.dumps(E, indent=1, ensure_ascii=False), encoding='utf-8')
    print(len(E), 'ensaios gravados em ensaios.json')
