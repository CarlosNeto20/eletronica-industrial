"""Gera os esquemáticos nativos PLECS 5.0 do Trabalho 4; não simula o circuito em Python.

Os cinco modelos usam o mesmo desenho: entrada à esquerda, ponte assimétrica do Forward de
duas chaves, transformador, filtro de saída e carga à direita, controle embaixo. Todos os
fios são ortogonais e roteados à mão; os sinais de controle que cruzariam a potência
(realimentações, PWM e seleção do degrau) usam etiquetas Goto/From.

Uso: python gerar_modelos.py [pasta_de_saida]   (padrão: a pasta deste script)
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PARAM = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))

# ---------------------------------------------------------------------------------------
# Geometria dos terminais. Posições relativas ao centro do componente com direction=up e
# sem espelhar; "direction" diz para que lado fica o terminal 1. Espelhar (Flipped) troca
# as pontas ao longo do eixo do componente. Calibrado com modelos salvos pelo próprio
# PLECS; só a coordenada transversal importa, pois todo fio sai do terminal em linha reta
# até um vértice mais distante.
# ---------------------------------------------------------------------------------------
_DOIS = {1: (0, -20), 2: (0, 20)}
BASE = {
    'Resistor': _DOIS, 'Inductor': _DOIS, 'Capacitor': _DOIS, 'Diode': _DOIS,
    'DCVoltageSource': _DOIS, 'ACVoltageSource': _DOIS,
    'Voltmeter': {**_DOIS, 3: (20, 0)}, 'Ammeter': {**_DOIS, 3: (20, 0)},
    'Switch': {**_DOIS, 3: (-20, 0)}, 'Mosfet': {**_DOIS, 3: (-20, 0)},
    'Ground': {1: (0, -20)},
    'Transformer': {1: (-20, -20), 2: (20, -20), 3: (-20, 20), 4: (20, 20)},
}
# Blocos de sinal, sempre desenhados com direction=right (posições finais).
FIXOS = {
    'CScript': {1: (-30, -5), 2: (-30, 5), 3: (30, -15), 4: (30, -5), 5: (30, 5), 6: (30, 15)},
    'Comparator': {1: (-20, -5), 2: (-20, 5), 3: (20, 0)},
    'TriangleGenerator': {1: (20, 0)},
    'Output': {1: (-20, 0)}, 'From': {1: (20, 0)}, 'Goto': {1: (-20, 0)},
    'PlecsProbe': {1: (20, 0)},
}
ROT = {'up': lambda x, y: (x, y), 'left': lambda x, y: (y, -x),
       'down': lambda x, y: (-x, -y), 'right': lambda x, y: (-y, x)}

HEADER = [
    ('Name', '"arquivo_exemplo"'), ('Version', '"5.0"'), ('CircuitModel', '"ContStateSpace"'),
    ('StartTime', '"0.0"'), ('TimeSpan', '"1.0"'), ('Timeout', '""'), ('Solver', '"auto"'),
    ('MaxStep', '"1e-3"'), ('InitStep', '"-1"'), ('FixedStep', '"1e-3"'), ('Refine', '"1"'),
    ('ZCStepSize', '"1e-9"'), ('RelTol', '"1e-3"'), ('AbsTol', '"-1"'), ('TurnOnThreshold', '"0"'),
    ('NonIdealSwitchResistance', '"1"'), ('SyncFixedStepTasks', '"2"'),
    ('UseSingleCommonBaseRate', '"2"'), ('LossVariableLimitExceededMsg', '"3"'),
    ('NegativeSwitchLossMsg', '"3"'), ('DivisionByZeroMsg', '"3"'), ('DatatypeOverflowMsg', '"3"'),
    ('DatatypeInheritanceConflictMsg', '"2"'), ('ContSampleTimeConflictMsg', '"2"'),
    ('StiffnessDetectionMsg', '"2"'), ('MaxConsecutiveZCs', '"1000"'),
    ('AlgebraicLoopWithStateMachineMsg', '"3"'), ('AssertionAction', '"1"'),
    ('FixedPointDatatypeOverride', '"1"'), ('InitializationCommands', '""'),
    ('InitialState', '"1"'), ('SystemState', '""'), ('JacobianComputation', '"2"'),
    ('TaskingMode', '"1"'), ('TaskConfigurations', '""'), ('CodeGenParameterInlining', '"2"'),
    ('CodeGenFloatingPointFormat', '"2"'), ('CodeGenAbsTimeUsageMsg', '"3"'),
    ('CodeGenBaseName', '""'), ('CodeGenOutputDir', '""'), ('CodeGenExtraOpts', '""'),
    ('CodeGenTarget', '"Generic"'), ('CodeGenTargetSettings', '""'),
    ('ExtendedMatrixPrecision', '"1"'), ('MatrixSignificanceCheck', '"2"'),
    ('RemoveUnusedStateSpaceOutputs', '"2"'), ('EnableStateSpaceSplitting', '"2"'),
    ('DisplayStateSpaceSplitting', '"1"'), ('DiscretizationMethod', '"2"'),
    ('ExternalModeSettings', '""'), ('AlgebraicLoopMethod', '"1"'),
    ('AlgebraicLoopTolerance', '"1e-6"'), ('ScriptsDialogGeometry', '""'),
    ('ScriptsDialogSplitterPos', '"0"'), ('MixedSignalSolverBypassOperatingPoint', '"1"'),
    ('MixedSignalSolverInitialConditions', '"2"'),
    ('MixedSignalSolverMaxNewtonIterations', '"25"'), ('MixedSignalSolverNumThreads', '"-1"'),
    ('OperatingPointMaxNewtonIterations', '"50"'),
    ('OperatingPointRelativeNewtonTolerance', '"1e-3"'),
    ('OperatingPointAbsoluteNewtonTolerance', '"1e-12"'),
    ('OperatingPointNodalVoltageNewtonTolerance', '"1e-6"'), ('SpiceTemperature', '"27"'),
    ('SpiceGMin', '"0"'), ('SpiceInductorRPar', '"0"'), ('SpiceInductorRSer', '"0"'),
    ('SpiceCapacitorGPar', '"0"'), ('SpiceCapacitorRSer', '"0"'), ('NetlistParserDetails', '"2"'),
    ('InvalidNetlistFunctionEvaluationMsg', '"1"'), ('IncompatibleInitialConditionMsg', '"2"'),
]


def q(s):
    return json.dumps(str(s), ensure_ascii=False)


def kv(indent, key, value):
    """Linha 'Chave  valor' com a mesma tabulação que o PLECS usa ao salvar."""
    return ' ' * indent + (key.ljust(14) if len(key) < 14 else key + ' ') + value


class Schematic:
    def __init__(self, name, init):
        self.name, self.init = name, init
        self.comps = {}
        self.nets = []
        self.outindices = []

    def add(self, typ, name, x, y, direction='up', flipped=False, params=None, show=True,
            label='east', extra=''):
        if name in self.comps:
            raise ValueError(f'componente repetido: {name}')
        if typ in FIXOS:
            direction = 'right'
        self.comps[name] = dict(typ=typ, x=x, y=y, dir=direction, flip=flipped,
                                params=params or {}, show=show, label=label, extra=extra)

    def pin(self, name, term):
        c = self.comps[name]
        if c['typ'] in FIXOS:
            dx, dy = FIXOS[c['typ']][term]
        else:
            bx, by = BASE[c['typ']][term]
            dx, dy = ROT[c['dir']](bx, -by if c['flip'] else by)
        return c['x'] + dx, c['y'] + dy

    def wire(self, *lines):
        self.nets.append(('Wire', lines))

    def signal(self, *lines):
        """O primeiro nó da primeira linha deve ser a saída que origina o sinal."""
        self.nets.append(('Signal', lines))

    def output(self, name, x, y, index):
        self.outindices.append(index)
        self.add('Output', name, x, y, params=dict(Index=index, Width=-1), label='south')

    # -- conexões -------------------------------------------------------------------------
    def _graph(self, lines):
        """Grafo de uma conexão: nós = terminais ('P', comp, term) ou vértices ('V', (x, y))."""
        xy, edges = {}, set()
        for line in lines:
            keys = []
            for node in line:
                if isinstance(node[0], str):
                    k, p = ('P', node[0], node[1]), self.pin(*node)
                else:
                    k, p = ('V', tuple(node)), tuple(node)
                if xy.setdefault(k, p) != p:
                    raise ValueError(f'nó {k} com duas posições')
                keys.append(k)
            for a, b in zip(keys, keys[1:]):
                if xy[a] == xy[b]:
                    raise ValueError(f'segmento de comprimento zero em {a} -> {b}')
                if xy[a][0] != xy[b][0] and xy[a][1] != xy[b][1]:
                    raise ValueError(f'segmento diagonal {a} {xy[a]} -> {b} {xy[b]}')
                edges.add((a, b))
        # parte cada segmento nos vértices que caem no seu interior (junções em T)
        adj = {k: set() for k in xy}
        for a, b in edges:
            (ax, ay), (bx, by) = xy[a], xy[b]
            inside = [k for k, (x, y) in xy.items() if k not in (a, b)
                      and min(ax, bx) <= x <= max(ax, bx) and min(ay, by) <= y <= max(ay, by)
                      and (x == ax == bx or y == ay == by)]
            if any(k[0] == 'P' for k in inside):
                raise ValueError(f'terminal sobre o fio {a} -> {b}')
            chain = [a] + sorted(inside, key=lambda k: abs(xy[k][0] - ax) + abs(xy[k][1] - ay)) + [b]
            for u, v in zip(chain, chain[1:]):
                adj[u].add(v)
                adj[v].add(u)
        return xy, adj

    def _tree(self, lines):
        xy, adj = self._graph(lines)
        if not isinstance(lines[0][0][0], str):
            raise ValueError(f'a primeira linha deve começar num terminal: {lines}')
        root = ('P', *lines[0][0])
        seen, todo = {root}, [root]
        while todo:
            for n in adj[todo.pop()]:
                if n not in seen:
                    seen.add(n)
                    todo.append(n)
        edges = sum(len(v) for v in adj.values()) // 2
        if seen != set(adj) or edges != len(adj) - 1:
            raise ValueError(f'conexão desconexa ou com laço: {lines}')
        for k, v in adj.items():
            if k[0] == 'P' and len(v) != 1:
                raise ValueError(f'terminal {k} com {len(v)} fios; use um vértice de junção')

        def ramo(u, nxt):
            pts, prev, cur = [], u, nxt
            while True:
                if cur[0] == 'P':
                    return dict(points=pts, dst=cur[1:], branches=[])
                nexts = sorted(n for n in adj[cur] if n != prev)
                if not nexts:
                    raise ValueError(f'fio solto em {xy[cur]}')
                reto = len(nexts) == 1 and (
                    (xy[prev][0] == xy[cur][0] == xy[nexts[0]][0]) or
                    (xy[prev][1] == xy[cur][1] == xy[nexts[0]][1]))
                if not reto:
                    pts.append(xy[cur])
                if len(nexts) == 1:
                    prev, cur = cur, nexts[0]
                    continue
                return dict(points=pts, dst=None, branches=[ramo(cur, n) for n in nexts])

        (first,) = adj[root]
        return root, ramo(root, first)

    def _connection(self, kind, lines):
        root, body = self._tree(lines)
        out = ['    Connection {', kv(6, 'Type', kind),
               kv(6, 'SrcComponent', q(root[1])), kv(6, 'SrcTerminal', str(root[2]))]

        def emit(node, ind):
            if node['points']:
                out.append(kv(ind, 'Points', '[' + '; '.join(f'{x}, {y}' for x, y in node['points']) + ']'))
            if node['dst']:
                out.append(kv(ind, 'DstComponent', q(node['dst'][0])))
                out.append(kv(ind, 'DstTerminal', str(node['dst'][1])))
            for b in node['branches']:
                out.append(' ' * ind + 'Branch {')
                emit(b, ind + 2)
                out.append(' ' * ind + '}')
        emit(body, 6)
        out.append('    }')
        return out

    def _component(self, name, c):
        out = ['    Component {', kv(6, 'Type', c['typ']), kv(6, 'Name', q(name)),
               kv(6, 'Show', 'on' if c['show'] else 'off'), kv(6, 'Position', f"[{c['x']}, {c['y']}]"),
               kv(6, 'Direction', c['dir']), kv(6, 'Flipped', 'on' if c['flip'] else 'off'),
               kv(6, 'LabelPosition', c['label'])]
        for k, v in c['params'].items():
            out += ['      Parameter {', kv(8, 'Variable', q(k)), kv(8, 'Value', q(v)),
                    kv(8, 'Show', 'off'), '      }']
        for comp, sigs in c['extra']:
            out += ['      Probe {', kv(8, 'Component', q(comp)), kv(8, 'Path', '""'),
                    kv(8, 'Signals', '{' + ', '.join(q(s) for s in sigs) + '}'), '      }']
        out.append('    }')
        return out

    def write(self, pasta):
        pts = [(c['x'], c['y']) for c in self.comps.values()]
        largura = max(x for x, _ in pts) + 120
        altura = max(y for _, y in pts) + 80
        zoom = min(1.0, int(100 * min(1480 / largura, 690 / altura)) / 100)
        valores = dict(Name=self.name, TimeSpan='Tstop', MaxStep='2e-6', RelTol='1e-6',
                       AbsTol='1e-8', Solver='radau', InitializationCommands=self.init)
        txt = ['Plecs {']
        for k, v in HEADER:
            txt.append(kv(2, k, q(valores[k]) if k in valores else v))
        for i in sorted(self.outindices):
            txt += ['  Terminal {', kv(4, 'Type', 'Output'), kv(4, 'Index', f'"{i}"'), '  }']
        txt += ['  Schematic {', kv(4, 'Location', '[0, 23; 1536, 773]'), kv(4, 'ZoomFactor', f'{zoom:g}'),
                kv(4, 'SliderPosition', '[0, 0]'), kv(4, 'ShowBrowser', 'off'), kv(4, 'BrowserWidth', '100')]
        for name, c in self.comps.items():
            txt += self._component(name, c)
        for kind, lines in self.nets:
            txt += self._connection(kind, lines)
        txt += ['  }', '}', '']
        (Path(pasta) / f'{self.name}.plecs').write_text('\n'.join(txt), encoding='utf-8')


def build(pasta, name='forward_degrau', mode=0, ac=True, original=False):
    cv = PARAM['controle']['final_v']['componentes']
    ci = PARAM['controle']['final_i']['componentes']
    init = f'''% Trabalho 4 - parametros SI; modos: 0 degrau, 1 curto, 2 bateria
Vrms=220; Vbus=310; fs=50000; Tstop={0.6 if mode == 2 else 0.36};
Lo=136.6e-6; Co={.0022 if original else .0044}; ESR={.11 if original else .055}; Cin=940e-6;
Lm=19.08e-3; Rcu=0.02; Rline=0.5; Lline=100e-6; Rbat=0.01; Cbat=0.4;
mode={mode}; Iref=15; Vref=27; Dlim=0.45; Tsoft=0.005;
Kiv={cv['Ki']}; Kpv={cv['Kp']}; wpv={cv['wp']};
Kii={ci['Ki']}; Kpi={ci['Kp']}; wpi={ci['wp']};
'''
    s = Schematic(name, init)

    # ---- grade do desenho --------------------------------------------------------------
    YT, YB = 100, 400            # trilhos de barramento (+ em cima, - embaixo)
    YP, YM = 180, 300            # nós do primário: pri+ (perna A) e pri- (perna B)
    YS, YG = 220, 480            # trilho de saída (CC) e retorno do secundário
    ox = 480 if ac else 0        # a ponte retificadora empurra o estágio de potência
    XA = 360 + ox                # perna A: Q1 em cima, ResetInferior embaixo
    XB = XA + 170                # perna B: ResetSuperior em cima, Q2 embaixo
    XL = XB + 90                 # indutância de magnetização
    XT = XA + 390                # centro do transformador
    XV = XA - 200                # voltímetro do barramento

    # ---- entrada ---------------------------------------------------------------------
    if ac:
        RL, RR, yac = 60, 480, 250     # colunas da ponte e linha da rede (dentro da ponte)
        for k, (x, y) in {1: (RL, 160), 2: (RL, 340), 3: (RR, 160), 4: (RR, 340)}.items():
            s.add('Diode', f'Ponte{k}', x, y, 'down', params=dict(Vf=.7, Ron=.01),
                  label='east' if x == RL else 'west')
        s.add('Ammeter', 'Irede', 140, yac, 'right', label='north')
        s.add('Inductor', 'Lrede', 220, yac, 'right', params=dict(L='Lline', i_init=0), label='north')
        s.add('Resistor', 'Rrede', 300, yac, 'right', params=dict(R='Rline'), label='north')
        s.add('ACVoltageSource', 'Rede', 380, yac, 'left',
              params=dict(V='sqrt(2)*Vrms', w='2*pi*60', phi='pi/2'), label='north')
        XC = XV - 90
        s.add('Capacitor', 'Cbus', XC, yac, 'up', params=dict(C='Cin', v_init='sqrt(2)*Vrms-1.4'),
              label='west')
        s.output('i_rede_A', 200, 320, 10)
        s.wire([('Irede', 2), (RL, yac), ('Ponte1', 1)], [(RL, yac), ('Ponte2', 2)])
        s.wire([('Rede', 2), (RR, yac), ('Ponte3', 1)], [(RR, yac), ('Ponte4', 2)])
        s.wire([('Irede', 1), ('Lrede', 2)])
        s.wire([('Lrede', 1), ('Rrede', 2)])
        s.wire([('Rrede', 1), ('Rede', 1)])
        s.signal([('Irede', 3), (140, 320), ('i_rede_A', 1)])
        bus_mais = [[('Ponte1', 2), (RL, YT), (XB, YT)], [('Ponte3', 2), (RR, YT)],
                    [('Cbus', 1), (XC, YT)]]
        bus_menos = [[('Ponte2', 1), (RL, YB), (XB, YB)], [('Ponte4', 1), (RR, YB)],
                     [('Cbus', 2), (XC, YB)]]
    else:
        XIN = XV - 100
        s.add('DCVoltageSource', 'Ventrada', XIN, 250, 'up', params=dict(V='Vbus'), label='west')
        bus_mais = [[('Ventrada', 1), (XIN, YT), (XB, YT)]]
        bus_menos = [[('Ventrada', 2), (XIN, YB), (XB, YB)]]
    s.add('Voltmeter', 'Vbarramento', XV, 250, 'up', label='west')
    s.output('v_bus_V', XV + 90, 250, 3)
    s.signal([('Vbarramento', 3), ('v_bus_V', 1)])
    bus_mais.append([('Vbarramento', 1), (XV, YT)])
    bus_menos.append([('Vbarramento', 2), (XV, YB)])

    # ---- primário: pernas A (P) e B (M) do Forward de duas chaves ----------------------
    mos = dict(Ron=.15, s_init=0)
    s.add('Mosfet', 'Q1', XA, 140, 'up', params=mos)
    s.add('Diode', 'ResetInferior', XA, 240, 'down', params=dict(Vf=.7, Ron=.01))
    s.add('Diode', 'ResetSuperior', XB, 240, 'down', params=dict(Vf=.7, Ron=.01))
    s.add('Mosfet', 'Q2', XB, 340, 'up', params=mos)
    s.add('Inductor', 'Lmag', XL, 240, 'up', params=dict(L='Lm', i_init=0))
    s.add('Transformer', 'T1', XT, 240, 'right', True,
          params=dict(Windings='[1 1]', n='[60 18]', Polarity='+', Lm='inf', im0=0), label='south')
    bus_mais += [[('Q1', 1), (XA, YT)], [('ResetSuperior', 2), (XB, YT)]]
    bus_menos += [[('ResetInferior', 1), (XA, YB)], [('Q2', 2), (XB, YB)]]
    s.wire(*bus_mais)
    s.wire(*bus_menos)
    # pri+ cruza a perna B (único cruzamento do esquema) e chega ao transformador
    s.wire([('Q1', 2), (XA, YP), (XT - 50, YP), (XT - 50, YS), ('T1', 1)],
           [(XA, YP), ('ResetInferior', 2)], [(XL, YP), ('Lmag', 1)])
    s.wire([('Q2', 1), (XB, YM), (XT - 50, YM), (XT - 50, YS + 40), ('T1', 2)],
           [(XB, YM), ('ResetSuperior', 1)], [(XL, YM), ('Lmag', 2)])
    # comando das chaves: etiqueta 'pwm' (gerada no bloco de controle)
    for q_, x in (('Q1', XA), ('Q2', XB)):
        y = 140 if q_ == 'Q1' else 340
        s.add('From', f'F_{q_}', x - 100, y, params=dict(Tag='pwm', Visibility=1,
              NoMatchingCounterpartAction=1), show=False)
        s.signal([(f'F_{q_}', 1), (q_, 3)])
    s.add('PlecsProbe', 'Esforcos', XL + 40, 50, label='north',
          extra=[('Q1', ['MOSFET voltage', 'MOSFET current']),
                 ('Lmag', ['Inductor current', 'Inductor voltage'])])
    s.output('esforcos', XL + 130, 50, 9)
    s.signal([('Esforcos', 1), ('esforcos', 1)])

    # ---- secundário: retificador, filtro LC e saída -----------------------------------
    xsw = XT + 160
    xlo, xrl, xil, xdb = XT + 220, XT + 280, XT + 340, XT + 400
    xo = XT + 460                # nó de saída (antes do filtro e da carga)
    xr = xsw + 100               # shunt de corrente
    xgn = xr + 80                # canto do retorno
    s.add('Diode', 'Dforward', XT + 100, YS, 'left', params=dict(Vf=.7, Ron=.005), label='south')
    s.add('Diode', 'Dlivre', xsw, 300, 'down', params=dict(Vf=.7, Ron=.005), label='east')
    s.add('Inductor', 'Lo', xlo, YS, 'left', params=dict(L='Lo', i_init=0), label='south')
    s.add('Resistor', 'RLo', xrl, YS, 'left', params=dict(R='Rcu'), label='south')
    s.add('Ammeter', 'IL', xil, YS, 'left', label='south')
    s.add('Diode', 'Dbloqueio', xdb, YS, 'left', params=dict(Vf=.7, Ron=.005), label='south')
    s.add('Resistor', 'Rsh', xr, 380, 'left', params=dict(R=.01), label='south')
    s.wire([('T1', 3), ('Dforward', 1)])
    s.wire([('Dforward', 2), (xsw, YS), ('Lo', 1)], [(xsw, YS), ('Dlivre', 2)])
    s.wire([('Lo', 2), ('RLo', 1)])
    s.wire([('RLo', 2), ('IL', 1)])
    s.wire([('IL', 2), ('Dbloqueio', 1)])
    s.wire([('T1', 4), (XT + 50, YS + 40), (XT + 50, 380), (xsw, 380), ('Rsh', 1)],
           [(xsw, 380), ('Dlivre', 1)])
    # medição da corrente do indutor: saída + etiqueta de realimentação
    s.output('i_indutor_A', xil + 60, 160, 2)
    s.add('Goto', 'G_IL', xil + 60, 120, params=dict(Tag='IL_fb', Visibility=1,
          NoMatchingCounterpartAction=2), show=False)
    s.signal([('IL', 3), (xil, 160), ('i_indutor_A', 1)], [(xil, 160), (xil, 120), ('G_IL', 1)])

    # colunas penduradas entre o trilho de saída (YS) e o retorno (YG): (x, terminal de cima, de baixo)
    c1 = XT + 500                # ESR + Co
    s.add('Resistor', 'ESR', c1, 300, 'up', params=dict(R='ESR'))
    s.add('Capacitor', 'Co', c1, 380, 'up', params=dict(C='Co', v_init=20 if mode == 2 else 27))
    s.wire([('ESR', 2), ('Co', 1)])
    colunas = [(c1, ('ESR', 1), ('Co', 2))]
    c3 = XT + 590                # primeira coluna de carga
    if mode == 2:
        c5 = XT + 800            # voltímetro à direita da bateria
        s.add('Ammeter', 'Ibat', c3, 265, 'up')
        s.add('Resistor', 'Rbat', c3, 325, 'up', params=dict(R='Rbat'))
        s.add('Capacitor', 'Cbat', c3, 385, 'up', params=dict(C='Cbat', v_init=0))
        s.add('DCVoltageSource', 'Ebat', c3, 445, 'up', params=dict(V=20))
        s.output('i_bateria_A', c3 + 90, 265, 11)
        s.signal([('Ibat', 3), ('i_bateria_A', 1)])
        s.wire([('Ibat', 2), ('Rbat', 1)])
        s.wire([('Rbat', 2), ('Cbat', 1)])
        s.wire([('Cbat', 2), ('Ebat', 1)])
        colunas.append((c3, ('Ibat', 1), ('Ebat', 2)))
    else:
        c4 = c3 + 190
        c5 = c4 + 110
        s.add('Resistor', 'Rbase', c3, 350, 'up', params=dict(R=9 if mode == 0 else 1.8))
        s.add('Resistor', 'Rdegrau', c4, 290, 'up', params=dict(R=2.25 if mode == 0 else .001))
        s.add('Switch', 'Scarga', c4, 380, 'up', params=dict(s_init=0, SwitchModel=1, f_grid=0))
        s.add('From', 'F_sel', c4 - 90, 380, params=dict(Tag='sel_carga', Visibility=1,
              NoMatchingCounterpartAction=1), show=False)
        s.signal([('F_sel', 1), ('Scarga', 3)])
        s.wire([('Rdegrau', 2), ('Scarga', 1)])
        colunas += [(c3, ('Rbase', 1), ('Rbase', 2)), (c4, ('Rdegrau', 1), ('Scarga', 2))]
    s.add('Voltmeter', 'Vo', c5, 350, 'up')
    s.output('v_saida_V', c5 + 110, 350, 1)
    s.add('Goto', 'G_Vo', c5 + 110, 410, params=dict(Tag='Vo_fb', Visibility=1,
          NoMatchingCounterpartAction=2), show=False)
    s.signal([('Vo', 3), (c5 + 50, 350), ('v_saida_V', 1)], [(c5 + 50, 350), (c5 + 50, 410), ('G_Vo', 1)])
    colunas.append((c5, ('Vo', 1), ('Vo', 2)))
    s.add('Ground', 'GND', xgn, 520, 'up')
    xs = [x for x, _, _ in colunas]
    s.wire([('Dbloqueio', 2)] + [(x, YS) for x in xs], *[[(x, YS), top] for x, top, _ in colunas])
    s.wire([('Rsh', 2), (xgn, 380), (xgn, YG)] + [(x, YG) for x in xs], [(xgn, YG), ('GND', 1)],
           *[[(x, YG), bottom] for x, _, bottom in colunas])

    # ---- controle: CC-CV, portadora e modulador PWM ----------------------------------
    CX, CY = 300 + ox, 660
    declarations = '''#include <math.h>
#define EV (2.5-InputSignal(0,0)*(2.5/27.0))
#define EI ((ParamRealData(0,0)/6.0)*fmin(1.0,CurrentTime/ParamRealData(9,0))-InputSignal(1,0)/6.0)
#define UV (ContState(0)+ParamRealData(2,0)*ContState(1))
#define UI (ContState(2)+ParamRealData(5,0)*ContState(3))
#define U (fmax(0.0,fmin(2.1*ParamRealData(8,0),fmin(UV,UI))))
'''
    # Tracking prevents the inactive regulator from winding up at the selector.
    deriv = '''ContDeriv(0)=ParamRealData(1,0)*EV+30000.0*(U-UV);
ContDeriv(1)=ParamRealData(3,0)*(EV-ContState(1));
ContDeriv(2)=ParamRealData(4,0)*EI+30000.0*(U-UI);
ContDeriv(3)=ParamRealData(6,0)*(EI-ContState(3));'''
    output = '''OutputSignal(0,0)=U;
OutputSignal(1,0)=((CurrentTime>=0.12)&&(CurrentTime<0.24)) ? 1.0 : 0.0;
OutputSignal(2,0)=UV;
OutputSignal(3,0)=UI;'''
    s.add('CScript', 'Controle_CC_CV', CX, CY, 'right', label='south', params=dict(
        NumInputs='[1 1]', NumOutputs='[1 1 1 1]', NumContStates=4, NumDiscStates=0, NumZCSignals=2,
        DirectFeedthrough=1, Ts=0, Parameters='Iref,Kiv,Kpv,wpv,Kii,Kpi,wpi,mode,Dlim,Tsoft',
        LangStandard=2, GnuExtensions=2, RuntimeCheck=2, Declarations=declarations,
        StartFcn='for(int k=0;k<4;k++) ContState(k)=0;',
        OutputFcn=output + '\nZCSignal(0)=CurrentTime-0.12; ZCSignal(1)=CurrentTime-0.24;',
        DerivativeFcn=deriv, UpdateFcn='', TerminateFcn=''))
    s.add('From', 'F_Vo', CX - 190, CY - 40, params=dict(Tag='Vo_fb', Visibility=1,
          NoMatchingCounterpartAction=1), show=False)
    s.add('From', 'F_IL', CX - 190, CY + 40, params=dict(Tag='IL_fb', Visibility=1,
          NoMatchingCounterpartAction=1), show=False)
    s.signal([('F_Vo', 1), (CX - 80, CY - 40), (CX - 80, CY - 5), ('Controle_CC_CV', 1)])
    s.signal([('F_IL', 1), (CX - 100, CY + 40), (CX - 100, CY + 5), ('Controle_CC_CV', 2)])
    s.add('Comparator', 'PWM', CX + 400, CY - 10, label='south')
    s.add('TriangleGenerator', 'Portadora', CX + 250, CY + 80,
          params=dict(Min=0, Max=2.1, f='fs', DutyCycle=.5, Delay=0), label='south')
    s.output('controle_V', CX + 210, CY - 60, 4)
    s.signal([('Controle_CC_CV', 3), ('PWM', 1)], [(CX + 150, CY - 15), (CX + 150, CY - 60), ('controle_V', 1)])
    s.output('u_tensao_V', CX + 170, CY + 80, 7)
    s.output('u_corrente_V', CX + 170, CY + 120, 8)
    s.signal([('Controle_CC_CV', 5), (CX + 90, CY + 5), (CX + 90, CY + 80), ('u_tensao_V', 1)])
    s.signal([('Controle_CC_CV', 6), (CX + 70, CY + 15), (CX + 70, CY + 120), ('u_corrente_V', 1)])
    if mode != 2:
        s.add('Goto', 'G_sel', CX + 170, CY + 40, params=dict(Tag='sel_carga', Visibility=1,
              NoMatchingCounterpartAction=2), show=False)
        s.signal([('Controle_CC_CV', 4), (CX + 110, CY - 5), (CX + 110, CY + 40), ('G_sel', 1)])
    s.output('portadora_V', CX + 420, CY + 80, 5)
    s.signal([('Portadora', 1), (CX + 340, CY + 80), (CX + 340, CY - 5), ('PWM', 2)],
             [(CX + 340, CY + 80), ('portadora_V', 1)])
    s.add('Goto', 'G_pwm', CX + 500, CY - 10, params=dict(Tag='pwm', Visibility=1,
          NoMatchingCounterpartAction=2), show=False)
    s.output('PWM_01', CX + 510, CY - 55, 6)
    s.signal([('PWM', 3), ('G_pwm', 1)], [(CX + 450, CY - 10), (CX + 450, CY - 55), ('PWM_01', 1)])
    s.write(pasta)


if __name__ == '__main__':
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    build(pasta)
    build(pasta, 'forward_curto', 1)
    build(pasta, 'forward_bateria', 2)
    build(pasta, 'forward_barramento_cc', 0, False)
    build(pasta, 'forward_capacitor_original', 0, False, True)
    print('5 modelos nativos escritos em', pasta)
