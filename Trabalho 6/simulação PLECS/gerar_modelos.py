"""Gera os modelos PLECS 5.0 do Trabalho 6 por edicao direta do texto .plecs.

Nao simula nada em Python. Le desenvolvimento/calculos/parametros.json, copia o
cabecalho de arquivo_exemplo.plecs (que permanece intacto), escreve componentes,
fios, sinais e terminais de saida de nivel superior, e grava:
  - <modelo>.plecs (cinco modelos)
  - modelos.json  (colunas exportadas por modelo, na ordem dos terminais de saida)
  - ensaios.json  (matriz de ensaios lida por resultados PLECS/executar_ensaios.py)
Os arquivos .plecs sao escritos somente com caracteres ASCII e quebras CRLF, porque
a gravacao pelo PLECS reinterpretou acentos no Trabalho 4.

Layout. Os blocos ficam em grupos funcionais com o fluxo de potencia da esquerda para a
direita, em grade de 10: rede, SS2, T1 e ponte a esquerda; barramento C4 no centro;
inversor, filtro LC e cargas a direita; CC-CC da bateria abaixo do barramento; modulacao,
PWM e C-Script numa faixa inferior; terminais Output numa coluna a direita. O barramento
positivo ocupa uma linha horizontal no alto e o negativo uma linha embaixo. Cada conexao
recebe Points calculados por roteador.py, de modo que todo fio e todo sinal e ortogonal e
nenhum passa sobre um bloco. A geometria dos terminais de cada tipo esta em TERMINAIS,
medida nos modelos que o proprio PLECS gravou (desenvolvimento/inspecionar_biblioteca.py
grava a medida em desenvolvimento/blocos_biblioteca.json).

Uso: python "simulação PLECS/gerar_modelos.py"
"""
from pathlib import Path
import json, re, math, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roteador

ROOT = Path(__file__).resolve().parents[1]
SIM = Path(__file__).resolve().parent
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
S = P['simulacao']
BASE = SIM / 'arquivo_exemplo.plecs'

# ---------------------------------------------------------------------------
# Geometria dos blocos no referencial proprio (Direction right, Flipped off).
# Para cada terminal: (deslocamento x, deslocamento y, sentido de saida).
# O deslocamento transversal e exato (define a coordenada do segmento de chegada);
# o deslocamento ao longo do eixo e conservador, pois alongar ou encurtar o primeiro
# segmento nao tira a ortogonalidade. Flipped espelha ao longo do eixo do bloco,
# trocando as duas pontas; Direction gira o bloco.
# ---------------------------------------------------------------------------
BIPOLO = [(20, 0, (1, 0)), (-20, 0, (-1, 0))]
TERMINAIS = {
    'Resistor': BIPOLO,
    'Inductor': BIPOLO,
    'Capacitor': BIPOLO,
    'Diode': BIPOLO,
    'ACVoltageSource': BIPOLO,
    'DCVoltageSource': BIPOLO,
    'Ammeter': BIPOLO + [(0, 15, (0, 1))],
    'Voltmeter': BIPOLO + [(0, 15, (0, 1))],
    'Switch': BIPOLO + [(0, 20, (0, 1))],
    'MosfetWithDiode': BIPOLO + [(0, -35, (0, -1))],
    'Ground': [(20, 0, (1, 0))],
    'Constant': [(15, 0, (1, 0))],
    'TriangleGenerator': [(20, 0, (1, 0))],
    'Comparator': [(-25, -5, (-1, 0)), (-25, 5, (-1, 0)), (25, 0, (1, 0))],
    'Output': [(-10, 0, (-1, 0))],
}
# meia caixa ocupada pelo bloco (ao longo do eixo, transversal), sem a folga do roteador
CAIXA = {'Ground': (12, 12), 'Constant': (14, 14), 'TriangleGenerator': (16, 16),
         'Comparator': (18, 14), 'Output': (9, 9), 'Transformer': (18, 0), 'CScript': (40, 0)}
CAIXA_PADRAO = (17, 13)
GIRO = dict(right=lambda x, y: (x, y), down=lambda x, y: (-y, x),
            left=lambda x, y: (-x, -y), up=lambda x, y: (y, -x))


def enrolamentos(valor):
    return [int(v) for v in str(valor).strip('[]').replace(',', ' ').split()]


def term_transformador(windings):
    """Lado 1 em x = +10 e lado 2 em x = -10; o enrolamento k de um lado com n
    enrolamentos tem centro em y = (k - (n+1)/2)*40 e terminais em centro -+15."""
    lados = enrolamentos(windings)
    n1 = lados[0]
    saida = []
    for lado, (n, x, s) in enumerate(((n1, 10, (1, 0)), (sum(lados) - n1, -10, (-1, 0)))):
        for k in range(1, n + 1):
            c = (k - (n + 1) / 2) * 40
            for dy in (-15, 15):
                saida.append((x, int(c + dy), s))
    return saida


def term_cscript(n_in, n_out):
    """Entradas a esquerda e saidas a direita, passo de 20 e centradas."""
    saida = []
    for n, x, s in ((n_in, -40, (-1, 0)), (n_out, 40, (1, 0))):
        for k in range(1, n + 1):
            saida.append((x, int((k - (n + 1) / 2) * 20), s))
    return saida


def q(s):
    t = json.dumps(str(s), ensure_ascii=True)
    assert t.isascii()
    return t


def par(k, v):
    return f'Parameter {{ Variable {q(k)} Value {q(v)} Show off }}'


class Modelo:
    def __init__(self, nome, init, x_saida=2200, y_saida=200, passo_saida=40):
        self.nome = nome
        self.init = init
        self.x_saida, self.y_saida, self.passo_saida = x_saida, y_saida, passo_saida
        self.pos = {}
        self.geo = {}           # nome -> (direcao, flip)
        self.comp = []          # nome, na ordem de insercao
        self.extras = {}
        self.tipos = {}
        self.nets = {}
        self.sigs = {}
        self.saidas = []

    # --- montagem ----------------------------------------------------------
    def add(self, tipo, nome, x, y, params=None, direcao='right', flip='off', extra=''):
        assert nome not in self.tipos, nome
        assert int(x) % 10 == 0 and int(y) % 10 == 0, (self.nome, nome, x, y)
        self.tipos[nome] = (tipo, params or {})
        self.pos[nome] = (int(x), int(y))
        self.geo[nome] = (direcao, flip)
        self.extras[nome] = extra
        self.comp.append(nome)

    def deslocar(self, dx, dy):
        self.pos = {n: (x + dx, y + dy) for n, (x, y) in self.pos.items()}

    def texto_componente(self, nome):
        tipo, params = self.tipos[nome]
        d, flip = self.geo[nome]
        x, y = self.pos[nome]
        return (f'Component {{ Type {tipo} Name {q(nome)} Show on Position [{x}, {y}] '
                f'Direction {d} Flipped {flip} LabelPosition south '
                + ' '.join(par(k, v) for k, v in params.items()) + self.extras[nome] + ' }')

    def no(self, nome, *pinos):
        self.nets.setdefault(nome, []).extend(pinos)

    def sinal(self, origem, *destinos):
        self.sigs.setdefault(origem, []).extend(destinos)

    def saida(self, nome, origem):
        idx = len(self.saidas) + 1
        self.saidas.append((idx, nome))
        self.add('Output', nome, self.x_saida, self.y_saida + self.passo_saida * idx,
                 dict(Index=idx, Width=-1))
        self.sinal(origem, (nome, 1))

    # --- geometria ---------------------------------------------------------
    def tabela(self, nome):
        tipo, p = self.tipos[nome]
        if tipo == 'Transformer':
            return term_transformador(p['Windings'])
        if tipo == 'CScript':
            return term_cscript(int(p['NumInputs']), len(enrolamentos(p['NumOutputs'])))
        return TERMINAIS[tipo]

    def terminais(self, nome):
        return list(range(1, len(self.tabela(nome)) + 1))

    def terminal(self, nome, t):
        """(ponto absoluto, sentido de saida) do terminal t do bloco nome."""
        d, flip = self.geo[nome]
        x0, y0 = self.pos[nome]
        dx, dy, s = self.tabela(nome)[t - 1]
        if flip == 'on':
            dx, dy, s = -dx, dy, (-s[0], s[1])
        g = GIRO[d]
        ox, oy = g(dx, dy)
        sx, sy = g(*s)
        return (x0 + ox, y0 + oy), (sx, sy)

    def caixa(self, nome):
        tipo, p = self.tipos[nome]
        ao_longo, transversal = CAIXA.get(tipo, CAIXA_PADRAO)
        if tipo == 'Transformer':
            transversal = max(abs(y) for _, y, _ in self.tabela(nome)) + 12
        elif tipo == 'CScript':
            transversal = max(abs(y) for _, y, _ in self.tabela(nome)) + 15
        d, _ = self.geo[nome]
        x0, y0 = self.pos[nome]
        a, b = (ao_longo, transversal) if d in ('right', 'left') else (transversal, ao_longo)
        return (x0 - a, y0 - b, x0 + a, y0 + b)

    def verificar(self):
        """Todo terminal ligado (o PLECS recusa terminal solto) e nenhuma caixa sobre outra."""
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
            xa, ya, xb, yb = self.caixa(a)
            for b in nomes[i + 1:]:
                xc, yc, xd, yd = self.caixa(b)
                assert xb + 10 < xc or xd + 10 < xa or yb + 10 < yc or yd + 10 < ya, \
                    (self.nome, 'blocos proximos', a, self.pos[a], b, self.pos[b])

    # --- roteamento --------------------------------------------------------
    def conexoes(self):
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        tela = roteador.Tela(min(xs) - 160, min(ys) - 160, max(xs) + 160, max(ys) + 160)
        for nome in self.pos:
            tela.obstaculo(self.caixa(nome), nome)
        saida = []
        grupos = [('Wire', nome, pinos) for nome, pinos in self.nets.items()]
        grupos += [('Signal', f'sinal:{o[0]}:{o[1]}', [o, *d]) for o, d in self.sigs.items()]
        for tipo, rede, pinos in grupos:
            assert len(pinos) >= 2, (self.nome, rede, pinos)
            terms = []
            for c, t in pinos:
                p, s = self.terminal(c, t)
                terms.append((c, t, p, s))
            caminhos = roteador.rotear(tela, rede, terms)
            corpo = (f'Type {tipo} SrcComponent {q(pinos[0][0])} SrcTerminal {pinos[0][1]} '
                     + roteador.arvore(caminhos, q))
            saida.append('Connection { ' + corpo + ' }')
        return saida

    def texto(self, opcoes):
        self.verificar()
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        self.deslocar(60 - min(xs), 60 - min(ys))      # origem perto do canto da janela
        con = self.conexoes()
        cab = BASE.read_text(encoding='utf-8').replace('\r\n', '\n').split('  Schematic {')[0]
        for chave, valor in dict(Name=self.nome, TimeSpan='Tstop', InitializationCommands=self.init, **opcoes).items():
            cab, n = re.subn(r'(?m)^  ' + chave + r'\s+"[^"\n]*"', lambda m: '  ' + chave + ' ' + q(valor), cab)
            assert n == 1, chave
        cab += ''.join(f'  Terminal {{ Type Output Index "{i}" }}\n' for i, _ in self.saidas)
        larg = max(p[0] for p in self.pos.values()) + 120
        alt = max(p[1] for p in self.pos.values()) + 120
        zoom = round(min(0.9, 1500 / larg, 820 / alt), 3)
        corpo = (f'  Schematic {{ Location [40, 40; 1600, 900] ZoomFactor {zoom} SliderPosition [0, 0] '
                 f'ShowBrowser off BrowserWidth 100\n'
                 + '\n'.join('    ' + self.texto_componente(c) for c in self.comp)
                 + '\n' + '\n'.join('    ' + c for c in con) + '\n  }\n}\n')
        txt = cab + corpo
        assert txt.isascii(), self.nome
        assert txt.count('{') == txt.count('}'), self.nome
        self.extensao = (larg, alt, zoom)
        return txt

    def gravar(self, opcoes):
        caminho = SIM / f'{self.nome}.plecs'
        caminho.write_bytes(self.texto(opcoes).replace('\n', '\r\n').encode('ascii'))
        return caminho


# ---------------------------------------------------------------------------
# Blocos reutilizaveis. BUSP e a linha do barramento positivo e BUSN a do negativo.
# ---------------------------------------------------------------------------
BUSP, BUSN = 140, 700


def rede_e_ponte(m, x0=0, y0=0):
    """Fonte, SS2, T1 1:1 ideal, ponte D1-D4, Rbus 0,1 ohm, C4 com ESR e voltimetro do barramento.

    Linha da fase em y0+300, do neutro em y0+520; bracos da ponte em x0+720 (no a) e
    x0+900 (no b), com os catodos para cima e os anodos para baixo."""
    m.add('Voltmeter', 'Vm_rede', x0 + 60, y0 + 420, direcao='up')
    m.add('ACVoltageSource', 'Vrede', x0 + 140, y0 + 420,
          dict(V='sqrt(2)*Vrms', w='2*pi*fr', phi='phi_rede'), 'up')
    m.add('Ground', 'GND_rede', x0 + 140, y0 + 600, direcao='up')
    m.add('Switch', 'SS2', x0 + 250, y0 + 300, dict(s_init=1), 'right', 'on')
    m.add('Ammeter', 'Am_rede', x0 + 360, y0 + 300, direcao='right', flip='on')
    m.add('Resistor', 'R_T1', x0 + 470, y0 + 300, dict(R='R_T1'), 'right', 'on')
    m.add('Transformer', 'T1', x0 + 580, y0 + 420,
          dict(Windings='[1 1]', n='[1 1]', Polarity='+', Lm='inf', im0=0), 'right', 'on')
    m.no('rede_f', ('Vrede', 1), ('Vm_rede', 1), ('SS2', 1))
    m.no('rede_n', ('Vrede', 2), ('Vm_rede', 2), ('GND_rede', 1), ('T1', 2))
    m.no('rede_ss2', ('SS2', 2), ('Am_rede', 1))
    m.no('rede_am', ('Am_rede', 2), ('R_T1', 1))
    m.no('rede_t1', ('R_T1', 2), ('T1', 1))
    # ponte: D1 e D4 conduzem no semiciclo positivo, D3 e D2 no negativo (Figura 2 da planilha)
    m.add('Ammeter', 'Am_D1', x0 + 720, y0 + 420, direcao='down')
    m.add('Diode', 'D1', x0 + 720, y0 + 250, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'down')
    m.add('Diode', 'D3', x0 + 900, y0 + 250, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'down')
    m.add('Diode', 'D2', x0 + 720, y0 + 580, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'down')
    m.add('Diode', 'D4', x0 + 900, y0 + 580, dict(Vf='Vf_ponte', Ron='Ron_ponte'), 'down')
    m.no('ca_a', ('T1', 3), ('Am_D1', 1), ('D2', 2))
    m.no('ca_d1', ('Am_D1', 2), ('D1', 1))
    m.no('ca_b', ('T1', 4), ('D3', 1), ('D4', 2))
    m.no('ponte_p', ('D1', 2), ('D3', 2), ('Am_ponte', 1))
    m.no('bus_n', ('D2', 1), ('D4', 1))
    m.add('Ammeter', 'Am_ponte', x0 + 1010, y0 + 190, direcao='right', flip='on')
    m.add('Resistor', 'Rbus', x0 + 1110, y0 + 190, dict(R='Rbus'), 'right', 'on')
    m.no('ponte_r', ('Am_ponte', 2), ('Rbus', 1))
    m.no('bus_p', ('Rbus', 2))
    barramento(m, x0 + 1220, y0)


def barramento(m, x, y0=0):
    """C4 com ESR e medidores, entre as duas linhas do barramento."""
    m.add('Ammeter', 'Am_C4', x, y0 + 240, direcao='up')
    m.add('Resistor', 'ESR_C4', x, y0 + 360, dict(R='ESR_C4'), 'up')
    m.add('Capacitor', 'C4', x, y0 + 480, dict(C='C4', v_init='Vbus0'), 'up')
    m.add('Voltmeter', 'Vm_bus', x + 100, y0 + 420, direcao='up')
    m.add('Ground', 'GND_bus', x + 100, y0 + 800, direcao='up')
    m.no('bus_p', ('Am_C4', 1), ('Vm_bus', 1))
    m.no('c4_a', ('Am_C4', 2), ('ESR_C4', 1))
    m.no('c4_b', ('ESR_C4', 2), ('C4', 1))
    m.no('bus_n', ('C4', 2), ('Vm_bus', 2), ('GND_bus', 1))


def conversor_cc(m, x0=0, y0=900, amortecedor=True):
    """Celula de tres estados com autotransformador, secundario 1:1 em ponte e C7 empilhado sobre C8.

    Faixa propria abaixo do barramento: linha do no meio em y0+240, bateria e Lb a direita de
    T32, colunas s1 em x0+360 e s2 em x0+1140, ponte do secundario em x0+1420 e 1540, C7 e C8
    em x0+1660. Com amortecedor=True, ramos RC (Rsn, Csn) em paralelo com S1, S2 e com o
    secundario de T32 representam a capacitancia de saida das chaves e evitam nos flutuantes
    quando a corrente de um ramo se anula (hipotese H)."""
    MEIO = y0 + 240
    m.add('Transformer', 'T32', x0 + 760, y0 + 340,
          dict(Windings='[2 1]', n='[1 1 1]', Polarity='+', Lm='T32_Lm', im0=0), 'left')
    m.add('Inductor', 'Lb', x0 + 900, y0 + 340, dict(L='Lb', i_init='ILb0'), 'right')
    m.add('Ammeter', 'Am_bat', x0 + 1000, y0 + 500, direcao='down')
    m.add('DCVoltageSource', 'Vbat', x0 + 1000, y0 + 660, dict(V='Vbat'), 'up')
    # correntes iniciais coerentes com o corte indutivo Lb / Llk1 / Llk2 (metade de ILb0 em cada primario)
    for k, i0, x, y in ((1, '-ILb0/2', x0 + 600, y0 + 460), (2, 'ILb0/2', x0 + 900, y0 + 200),
                        (3, 0, x0 + 900, y0 + 400)):
        m.add('Inductor', f'Llk{k}', x, y, dict(L='T32_Llk', i_init=i0), 'left')
        m.add('Resistor', f'Rw{k}', x - 120 if k == 1 else x + 120, y, dict(R='T32_R'), 'left')
    m.add('MosfetWithDiode', 'S1', x0 + 360, y0 + 640, dict(Ron='Ron_cc', s_init=0), 'up')
    m.add('MosfetWithDiode', 'S2', x0 + 1140, y0 + 640, dict(Ron='Ron_cc', s_init=0), 'up')
    m.add('Ammeter', 'Am_S1', x0 + 360, y0 + 520, direcao='up')
    m.add('Ammeter', 'Am_S2', x0 + 1140, y0 + 520, direcao='up')
    m.add('Voltmeter', 'Vm_S1', x0 + 240, y0 + 580, direcao='up')
    m.add('Diode', 'D17', x0 + 360, y0 + 160, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'down')
    m.add('Diode', 'D18', x0 + 1140, y0 + 160, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'down')
    m.add('Ammeter', 'Am_D17', x0 + 360, y0 + 300, direcao='down')
    m.add('Capacitor', 'C8', x0 + 1660, y0 + 400, dict(C='C8', v_init='VC8_0'), 'up')
    m.add('Capacitor', 'C7', x0 + 1660, y0 + 120, dict(C='C7', v_init='VC7_0'), 'up')
    m.add('Voltmeter', 'Vm_C8', x0 + 1780, y0 + 400, direcao='up')
    m.add('Voltmeter', 'Vm_C7', x0 + 1780, y0 + 120, direcao='up')
    m.add('Ammeter', 'Am_sec', x0 + 1280, y0 + 400, direcao='left')
    for nome, x, y, direcao in (('D13', 1420, 60, 'down'), ('D15', 1420, 180, 'down'),
                                ('D14', 1540, 60, 'down'), ('D16', 1540, 180, 'down')):
        m.add('Diode', nome, x0 + x, y0 + y, dict(Vf='Vf_rapido', Ron='Ron_rapido'), direcao)
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
        for nome, x, y, a, b in (('S1', x0 + 120, y0 + 520, 's1', 'bus_n'),
                                 ('S2', x0 + 1020, y0 + 760, 's2', 'bus_n'),
                                 ('sec', x0 + 1540, y0 + 400, 'sec_a', 'sec_b')):
            m.add('Resistor', f'Rsn_{nome}', x, y, dict(R='Rsn'), 'up')
            m.add('Capacitor', f'Csn_{nome}', x, y + 120, dict(C='Csn', v_init=0), 'up')
            m.no(a, (f'Rsn_{nome}', 1))
            m.no(f'sn_{nome}', (f'Rsn_{nome}', 2), (f'Csn_{nome}', 1))
            m.no(b, (f'Csn_{nome}', 2))


def pwm_cc(m, origem_dref, x0=0, y0=1900):
    """Duas dentes de serra de fsb defasadas de 180 graus; gate ligado enquanto dref > portadora."""
    m.add('TriangleGenerator', 'Serra_S1', x0 + 160, y0, dict(Min=0, Max=1, f='fsb', DutyCycle=1, Delay=0))
    m.add('TriangleGenerator', 'Serra_S2', x0 + 160, y0 + 120, dict(Min=0, Max=1, f='fsb', DutyCycle=1, Delay='0.5/fsb'))
    m.add('Comparator', 'PWM_S1', x0 + 320, y0)
    m.add('Comparator', 'PWM_S2', x0 + 320, y0 + 120)
    m.sinal(origem_dref, ('PWM_S1', 1), ('PWM_S2', 1))
    m.sinal(('Serra_S1', 1), ('PWM_S1', 2))
    m.sinal(('Serra_S2', 1), ('PWM_S2', 2))
    m.sinal(('PWM_S1', 3), ('S1', 3))
    m.sinal(('PWM_S2', 3), ('S2', 3))


def inversor(m, x0=1450, y0=0):
    """Ponte completa, filtro LC e as tres cargas; linha de saida em y0+420 e retorno em y0+800."""
    for nome, x, y in (('QB_sup', 10, 260), ('QB_inf', 10, 580), ('QA_sup', 130, 300), ('QA_inf', 130, 580)):
        m.add('MosfetWithDiode', nome, x0 + x, y0 + y, dict(Ron='Ron_inv', s_init=0), 'up')
    m.add('Ammeter', 'Am_QA', x0 + 130, y0 + 190, direcao='up')
    m.add('Voltmeter', 'Vm_AB', x0 + 70, y0 + 470)
    m.add('Ammeter', 'Am_Lo', x0 + 250, y0 + 420, direcao='right', flip='on')
    m.add('Inductor', 'Lo', x0 + 360, y0 + 420, dict(L='Lo', i_init=0), 'right', 'on')
    m.add('Resistor', 'ESR_Co', x0 + 470, y0 + 500, dict(R='ESR_Co'), 'up')
    m.add('Capacitor', 'Co', x0 + 470, y0 + 620, dict(C='Co', v_init=0), 'up')
    m.add('Voltmeter', 'Vm_o', x0 + 560, y0 + 560, direcao='up')
    m.add('Ammeter', 'Am_o', x0 + 660, y0 + 420, direcao='right', flip='on')
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
    m.add('Switch', 'Sw_res', x0 + 780, y0 + 500, dict(s_init=0), 'up')
    m.add('Resistor', 'R_res', x0 + 780, y0 + 620, dict(R='Rres'), 'up')
    m.no('res_a', ('Sw_res', 2), ('R_res', 1))
    m.add('Switch', 'Sw_rl', x0 + 900, y0 + 460, dict(s_init=0), 'up')
    m.add('Resistor', 'R_rl', x0 + 900, y0 + 560, dict(R='R3k'), 'up')
    m.add('Inductor', 'L_rl', x0 + 900, y0 + 660, dict(L='L3k', i_init=0), 'up')
    m.no('rl_a', ('Sw_rl', 2), ('R_rl', 1))
    m.no('rl_b', ('R_rl', 2), ('L_rl', 1))
    m.add('Switch', 'Sw_nl', x0 + 1020, y0 + 420, direcao='right', flip='on')
    m.add('Resistor', 'Rs_nl', x0 + 1130, y0 + 420, dict(R='nl_Rs'), 'right', 'on')
    for nome, x, y in (('Dn1', 1240, 330), ('Dn3', 1360, 330), ('Dn2', 1240, 510), ('Dn4', 1360, 510)):
        m.add('Diode', nome, x0 + x, y0 + y, dict(Vf='Vf_rapido', Ron='Ron_rapido'), 'down')
    m.add('Resistor', 'ESR_nl', x0 + 1480, y0 + 310, dict(R='nl_ESR'), 'up')
    m.add('Capacitor', 'C_nl', x0 + 1480, y0 + 430, dict(C='nl_C', v_init='VC3_0'), 'up')
    m.add('Resistor', 'R_nl', x0 + 1580, y0 + 420, dict(R='nl_R'), 'up')
    m.add('Voltmeter', 'Vm_nl', x0 + 1680, y0 + 420, direcao='up')
    m.no('nl_a', ('Sw_nl', 2), ('Rs_nl', 1))
    m.no('nl_ca', ('Rs_nl', 2), ('Dn1', 1), ('Dn2', 2))
    m.no('perna_B', ('R_res', 2), ('L_rl', 2), ('Dn3', 1), ('Dn4', 2))
    m.no('nl_p', ('Dn1', 2), ('Dn3', 2), ('ESR_nl', 1), ('R_nl', 1), ('Vm_nl', 1))
    m.no('nl_esr', ('ESR_nl', 2), ('C_nl', 1))
    m.no('nl_n', ('Dn2', 1), ('Dn4', 1), ('C_nl', 2), ('R_nl', 2), ('Vm_nl', 2))


def modulador(m, origem_vc, x0=900, y0=1900):
    """Unipolar: portadoras triangulares +-Vd em fs, a segunda atrasada de meio periodo (180 graus)."""
    m.add('TriangleGenerator', 'Portadora_A', x0, y0, dict(Min='-Vd', Max='Vd', f='fs', DutyCycle=0.5, Delay=0))
    m.add('TriangleGenerator', 'Portadora_B', x0, y0 + 240, dict(Min='-Vd', Max='Vd', f='fs', DutyCycle=0.5, Delay='0.5/fs'))
    for nome, y in (('CMP_A_sup', -60), ('CMP_A_inf', 60), ('CMP_B_inf', 180), ('CMP_B_sup', 300)):
        m.add('Comparator', nome, x0 + 160, y0 + y)
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


def controle(m, x0=1700, y0=2100):
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
    m = Modelo('retificador_barramento', CAB + comum() + CENARIO, x_saida=1700, y_saida=820)
    rede_e_ponte(m)
    m.add('Resistor', 'R_eq', 1420, 420, dict(R='Rcarga'), 'up')
    m.no('bus_p', ('R_eq', 1))
    m.no('bus_n', ('R_eq', 2))
    m.add('Constant', 'SS2_fechada', 250, 140, dict(Value=1, DataType=10))
    m.sinal(('SS2_fechada', 1), ('SS2', 3))
    for nome, o in (('v_rede_V', ('Vm_rede', 3)), ('i_rede_A', ('Am_rede', 3)), ('i_D1_A', ('Am_D1', 3)),
                    ('i_ponte_A', ('Am_ponte', 3)), ('i_C4_A', ('Am_C4', 3)), ('v_bus_V', ('Vm_bus', 3))):
        m.saida(nome, o)
    return m


def modelo_elevador(nome='elevador_bateria', amortecedor=True):
    m = Modelo(nome, CAB + comum() + cc_extra() + CENARIO, x_saida=2500, y_saida=1500)
    barramento(m, 1980)
    conversor_cc(m, 0, 300, amortecedor=amortecedor)
    m.add('Resistor', 'R_eq', 2200, 420, dict(R='Rcarga'), 'up')
    m.no('bus_p', ('R_eq', 1))
    m.no('bus_n', ('R_eq', 2))
    m.add('Constant', 'Dref', 20, 1500, dict(Value='Db', DataType=10))
    pwm_cc(m, ('Dref', 1), 0, 1500)
    for nome, o in (('v_bus_V', ('Vm_bus', 3)), ('i_bat_A', ('Am_bat', 3)), ('v_C8_V', ('Vm_C8', 3)),
                    ('v_C7_V', ('Vm_C7', 3)), ('v_S1_V', ('Vm_S1', 3)), ('i_S1_A', ('Am_S1', 3)),
                    ('i_S2_A', ('Am_S2', 3)), ('i_D17_A', ('Am_D17', 3)), ('i_sec_A', ('Am_sec', 3)),
                    ('i_C4_A', ('Am_C4', 3)), ('gate_S1', ('PWM_S1', 3))):
        m.saida(nome, o)
    return m


def modelo_inversor():
    m = Modelo('inversor_malha_fechada', CAB + comum() + CENARIO, x_saida=3400, y_saida=950, passo_saida=30)
    m.add('DCVoltageSource', 'Vcc', 1240, 420, dict(V='Vcc'), 'up')
    m.add('Voltmeter', 'Vm_bus', 1340, 420, direcao='up')
    m.add('Ground', 'GND_bus', 1340, 800, direcao='up')
    m.no('bus_p', ('Vcc', 1), ('Vm_bus', 1))
    m.no('bus_n', ('Vcc', 2), ('Vm_bus', 2), ('GND_bus', 1))
    inversor(m, 1450, 0)
    controle(m, 1800, 1700)
    modulador(m, ('Controle', 2), 2400, 1600)
    for nome, o in (('v_o_V', ('Vm_o', 3)), ('i_o_A', ('Am_o', 3)), ('i_Lo_A', ('Am_Lo', 3)),
                    ('v_c_V', ('Controle', 2)), ('v_ref_V', ('Controle', 3)), ('v_c_livre_V', ('Controle', 9)),
                    ('v_AB_V', ('Vm_AB', 3)), ('i_QA_A', ('Am_QA', 3)), ('v_nl_V', ('Vm_nl', 3)), ('v_bus_V', ('Vm_bus', 3)),
                    ('rede_on', ('Controle', 4)), ('dref_cc', ('Controle', 5))):
        m.saida(nome, o)
    return m


def modelo_completo():
    m = Modelo('nobreak_completo', CAB + comum() + cc_extra() + CENARIO, x_saida=3800, y_saida=950, passo_saida=30)
    rede_e_ponte(m)
    conversor_cc(m, 0, 1800)
    inversor(m, 1450, 0)
    controle(m, 2400, 2900)
    modulador(m, ('Controle', 2), 2900, 2800)
    pwm_cc(m, ('Controle', 5), 2400, 3350)
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
                           # a janela de depois termina no fim do ensaio: dois ciclos inteiros dentro
                           # do tempo simulado, comecando tres quartos de ciclo apos o degrau
                           janelas=dict(antes=[tdeg - 2 * T60, tdeg], depois=[0.1 - 2 * T60, 0.1], degrau=[tdeg, tdeg + 0.004]),
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
                            componentes=len(m.comp), fios=len(m.nets), sinais=len(m.sigs),
                            largura=m.extensao[0], altura=m.extensao[1], zoom=m.extensao[2])
        print(f'{caminho.name}: {len(m.comp)} componentes, {len(m.nets)} nos, {len(m.saidas)} saidas, '
              f'{m.extensao[0]} x {m.extensao[1]}, zoom {m.extensao[2]}')
    (SIM / 'modelos.json').write_text(json.dumps(dict(solver=OPC, modelos=info), indent=1, ensure_ascii=False), encoding='utf-8')
    (SIM / 'ensaios.json').write_text(json.dumps(E, indent=1, ensure_ascii=False), encoding='utf-8')
    print(len(E), 'ensaios gravados em ensaios.json')
