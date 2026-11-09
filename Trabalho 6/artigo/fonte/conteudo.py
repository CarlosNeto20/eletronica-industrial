"""Conteudo autoral do artigo. Todo numero vem de parametros.json (A) ou de metricas.json (S).

As funcoes de formatacao usam virgula decimal. A secao de resultados so e escrita quando
metricas.json existe e contem os ensaios citados; sem dados do PLECS ela informa que a
simulacao esta pendente, em vez de apresentar resultados inexistentes.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
_mp = ROOT / 'resultados PLECS' / 'metricas.json'
M = json.loads(_mp.read_text(encoding='utf-8')) if _mp.exists() else {}
FIG = ROOT / 'artigo' / 'figuras'
FIGC = ROOT / 'desenvolvimento' / 'calculos' / 'figuras'


def f(x, n=2):
    """Numero com virgula decimal, n casas, sem separador de milhar e com sinal de menos tipografico."""
    s = f'{x:.{n}f}'.replace('.', ',')
    return s.replace('-', '\u2212')


def g(x, n=3):
    """Numero com n algarismos significativos e virgula decimal."""
    s = f'{x:.{n}g}'
    if 'e' in s:
        return f(x, 0)
    return s.replace('.', ',').replace('-', '\u2212')


E = P['especificacoes']
R = P['retificador']['planilha']
RV = P['retificador']['vales_com_1880uF']
INV = P['inversor']
MAL = P['malha']
CC = P['cc_cc']
ESF = {e['carga']: e for e in INV['esforcos']}
PT = MAL['pontos']

ARQUIVO = 'Trabalho6_NoBreak_3kVA'
TITULO = 'Projeto e Verificação de um No-Break de Dupla Conversão Monofásico de 3 kVA com Conversor Elevador de Alto Ganho'
AUTORES = ['Jonatas Manoel Assunção Felix (539729)', 'Jose Carlos Moreira de Brito Neto (536962)']
AFILIACAO = ['Departamento de Engenharia Elétrica, Universidade Federal do Ceará, Fortaleza, Brasil',
             'Eletrônica Industrial (TH0263), Prof. Dr. René Pastor Torrico-Bascopé, novembro de 2026']
PALAVRAS = 'no-break de dupla conversão; inversor unipolar; compensador Tipo 3; célula de comutação de três estados; PLECS.'


def tem(*ns):
    return all(n in M for n in ns)


def resumo():
    base = ('Este trabalho completa e verifica o projeto de um no-break de dupla conversão monofásico de 3 kVA e 2,1 kW, '
            'com entrada de 176 a 264 V, saída de 115 V e banco de baterias de 42 a 56 V. O sistema combina retificador '
            'em ponte com filtro capacitivo, conversor elevador de alto ganho baseado na célula de comutação de três estados '
            'e inversor em ponte completa com modulação unipolar e compensador Tipo 3. A reconstrução da planilha de projeto '
            'confirmou os valores numéricos e apontou inconsistências de texto, o barramento mínimo usado no índice de '
            'modulação, a ondulação real do indutor e margens de ganho finitas. ')
    if not M:
        return base + 'Os modelos para o PLECS foram preparados, e os resultados de simulação estão pendentes de execução.'
    return base + RESUMO_RESULTADOS()


def RESUMO_RESULTADOS():
    return 'Os resultados de simulação no PLECS são apresentados e comparados com os valores analíticos.'


RESUMO = resumo()


def blocos():
    B = []
    h = lambda x: B.append(('h', x))
    sub = lambda x: B.append(('sub', x))
    p = lambda x: B.append(('p', x))
    eq = lambda x: B.append(('eq', x))
    fig = lambda arq, leg: B.append(('fig', arq, leg))
    tab = lambda leg, lin, larg: B.append(('tab', leg, lin, larg))

    h('I. Introdução')
    p('No-breaks de dupla conversão alimentam cargas críticas por um inversor permanentemente em operação, que recebe energia '
      'de um barramento CC. Com a rede presente, o barramento é mantido por um retificador; na falta, por um banco de baterias '
      'e um conversor elevador, sem interrupção na saída [1], [2]. A carga típica, formada por fontes com retificador capacitivo, '
      'impõe correntes de pico elevadas e é representada nas normas por uma carga não linear de referência [3].')
    p('O projeto de partida é a planilha didática da disciplina [4], que dimensiona os três conversores e define a malha de tensão '
      'do inversor, mas deixa os resultados e as conclusões em aberto. Este trabalho reconstrói todos os cálculos, audita cada '
      'valor impresso, verifica o laço de controle em vários pontos de operação, identifica a topologia do conversor de baterias '
      'a partir do circuito de simulação do professor e substitui a simulação em PSIM por modelos nativos no PLECS, executados '
      'por interface XML-RPC. Os valores calculados, os dados do professor e os resultados do solver são mantidos separados.')
    fig(FIG / 'arquitetura.png', 'Arquitetura do no-break de dupla conversão. A chave SS2 emula a falta da rede; o CC-CC fica em espera em modo rede.')

    h('II. Especificações')
    tab('Especificações do no-break', [
        ['Grandeza', 'Valor'],
        ['Rede (nominal; faixa)', f"{E['Vinomef']:.0f} V; {E['Viminef']:.0f} a {E['Vimaxef']:.0f} V, 60 Hz"],
        ['Saída', f"{E['Voef']:.0f} V, 60 Hz"],
        ['Potência ativa; aparente', f"{E['Po']:.0f} W; {E['So']:.0f} VA"],
        ['Banco de baterias', f"{CC['planilha']['Vibmin']:.0f} a {CC['planilha']['Vibmax']:.0f} V"],
        ['Comutação (inversor e CC-CC)', '20 kHz'],
        ['Orçamento de potência do barramento', f"{P['Prec']:.0f} W (rendimento de 0,933)"]], [.52, .48])
    p(f"O rendimento de 0,933 do inversor é usado apenas para dimensionar a potência do retificador, {f(P['Prec'], 0)} W; não é um "
      'rendimento medido. As cargas de ensaio são a resistiva de 2100 W, uma RL de 3 kVA com fator de potência 0,7 e a carga '
      'não linear do circuito do professor, formada por ponte de diodos, 0,2 Ω em série, 1880 µF com 0,05 Ω e 9,5 Ω.')

    h('III. Retificador e Barramento')
    p(f"Na rede mínima o pico do barramento é {f(R['VC1max'])} V. A planilha fixa ondulação de {f(R['dVC'])} V, o que leva o vale a "
      f"{f(R['VC1min'])} V e o ângulo de condução a {f(R['thetaC1_rad'], 3)} rad. O texto fala em 10% do pico, mas o número usado "
      'corresponde a 15%; o valor foi mantido porque todo o projeto depende dele. Igualando a energia retirada do capacitor durante '
      'a descarga à potência da carga, obtém-se')
    eq('C_{1}=\\frac{P_{rec}(π−θ_{C1})}{π f_{r}(V_{C1max}^{2}−V_{C1min}^{2})}')
    p(f"que resulta em {f(R['C1_F'] * 1e3, 3)} mF. Adotam-se quatro eletrolíticos de 470 µF, 1880 µF, com os quais o vale a 176 V passa a "
      f"{f(RV['176']['Vvale'])} V. Na aproximação de pulso retangular, o balanço de carga dá a corrente de recarga")
    eq('I_{chg}=\\frac{I_{oeq}π}{θ_{C1}}')
    p(f"igual a {f(R['Ichg'])} A, com corrente média por diodo de {f(R['ID1med'], 3)} A, eficaz de {f(R['ID1ef'])} A e eficaz no capacitor de "
      f"{f(R['IC1ef'])} A. A planilha estima o pico real do diodo em 2·I_{{chg}} = {f(R['ID1pk_2Ichg'], 1)} A. Cada diodo bloqueia "
      f"{f(P['retificador']['VDrrevpk'])} V na rede máxima. O circuito do professor inclui 0,1 Ω entre a ponte e o barramento, que "
      'representa a impedância da rede e reduz o pico do pulso; esse efeito é medido na simulação.')

    h('IV. Inversor e Filtro')
    p(f"Na modulação unipolar com duas portadoras de ±5 V defasadas de 180°, a tensão entre braços alterna entre 0 e ±V_{{cc}} com "
      'frequência aparente de 40 kHz, e o valor médio por período é V_{cc}·v_{c}/V_{d}. Com o barramento oscilando entre o vale '
      'e o pico, o índice de modulação no pico da saída varia de '
      f"{f(INV['indices_modulacao']['373,35 V (pico a 264 V)']['M_pico'], 3)} a {f(INV['indices_modulacao']['210 V (saida do CC-CC)']['M_pico'], 3)} "
      '(barramento de 210 V do CC-CC), abaixo do limite de 0,85. A planilha usa 223 V e obtém 0,729, valor que subestima o índice '
      'no vale. No pico da tensão de saída, o pulso com v_{AB} = V_{cc} dura m/(2f_{s}), e a ondulação do indutor é')
    eq('ΔI_{Lo}=\\frac{(V_{cc}−v_{o})v_{o}}{2f_{s}L_{o}V_{cc}}')
    p(f"A planilha dimensiona L_{{o}} = {f(INV['Lo'] * 1e6, 1)} µH com um intervalo de 0,5(1 + m)/(2f_{{s}}), maior que m/(2f_{{s}}); com o valor "
      f"adotado, a ondulação máxima a 373 V é {f(INV['dILo_real_373'])} A, contra o critério de {f(INV['dILo_criterio'])} A. O capacitor de "
      f"{f(INV['Co'] * 1e6, 0)} µF põe a ressonância em {f(INV['f0_LC'], 0)} Hz, um vigésimo de f_{{s}}; o texto da planilha cita "
      'f_{s}/40 por engano. A Tabela II mostra que dimensionar com 2100 W resistivos subestima os esforços de 3 kVA.')
    e1, e2, e3 = ESF['Resistiva 2100 W'], ESF['Linear 3 kVA, FP 0,7 indutivo'], ESF['Nao linear 3 kVA (FC = 3, referencia)']
    tab('Esforços nos interruptores do inversor (cálculo)', [
        ['Carga', 'I_{o} ef (A)', 'I_{Lo} ef (A)', 'Chave ef (A)', 'Pico (A)'],
        ['Resistiva 2100 W', f(e1['Io_rms_A']), f(e1['ILo_rms_A']), f(e1['I_chave_rms_A']), f(e1['I_chave_pk_A'], 1)],
        ['RL 3 kVA, FP 0,7', f(e2['Io_rms_A']), f(e2['ILo_rms_A']), f(e2['I_chave_rms_A']), f(e2['I_chave_pk_A'], 1)],
        ['Não linear, FC 3', f(e3['Io_rms_A']), f(e3['ILo_rms_A']), f(e3['I_chave_rms_A']), f(e3['I_chave_pk_A'], 1)]],
        [.31, .16, .17, .18, .18])

    h('V. Malha de Tensão')
    p(f"O sensor tem ganho H_{{v}} = 4/(√2·115) = {f(MAL['Hv'], 5)}, o modulador 1/V_{{d}} = 1/5 e a planta, para o filtro carregado por R_{{o}},")
    eq('G_{v}(s)=\\frac{V_{cc}}{L_{o}C_{o}s^{2}+(L_{o}/R_{o})s+1}')
    p(f"Com cruzamento em f_{{cv}} = 2f_{{s}}/6 = {f(MAL['fcv'] / 1e3, 2)} kHz, a planta atenua {f(abs(MAL['Av_dB']))} dB a 373 V e plena carga "
      f"(o texto da planilha cita 33,23 dB por engano) e tem fase de {f(MAL['P_graus'])}°. Para 60° de margem, o avanço necessário é "
      f"{f(MAL['alfa'])}°, o que exige um compensador Tipo 3. Pelo método do fator K, K = 47 (o exato seria {f(MAL['K_exato'])}) coloca os "
      f"zeros duplos em {f(MAL['fz_Hz'][0], 1)} Hz e os polos duplos em {f(MAL['fp_Hz'][0] / 1e3, 1)} kHz:")
    eq('C_{v}(s)=\\frac{K_{c}(s+ω_{z})^{2}}{s(s+ω_{p})^{2}}')
    p(f"com K_{{c}} = {g(MAL['polos_zeros']['Kc'] / 1e7, 4)}·10^{{7}} s^{{−1}}. No ponto de projeto a margem de fase é {f(MAL['MF_projeto'], 1)}°. "
      'Como o ganho da planta é proporcional a V_{cc} e a carga altera o amortecimento do filtro, o laço foi verificado em nove pontos '
      '(Tabela III). Há um único cruzamento por 0 dB em todos; a margem de fase mínima ocorre em vazio com barramento baixo, onde o '
      'filtro fica praticamente sem amortecimento. A fase cruza −180° perto de 48 kHz, o que torna a margem de ganho finita, ao '
      'contrário do que afirma a planilha; esse cruzamento ocorre acima da frequência de ondulação, onde o modelo médio perde validade.')
    linhas = [['Ponto', 'f_{c} (kHz)', 'MF (°)', 'MG (dB)']]
    for nome, rot in (('373 V, plena 2100 W', '373 V, 2100 W'), ('373 V, vazio', '373 V, vazio'),
                      ('211,57 V, plena', '211,6 V, 2100 W'), ('210 V, vazio', '210 V, vazio')):
        c, m_ = PT[nome]['cruzamentos_0dB'][0], PT[nome]['cruzamentos_fase_180'][0]
        linhas.append([rot, f(c['f_Hz'] / 1e3), f(c['MF_graus'], 1), f(m_['MG_dB'], 1)])
    tab('Laço de tensão compensado (cálculo, com ESR de C_{o})', linhas, [.36, .22, .2, .22])
    fig(FIGC / 'bode_laco.png', 'Bode do laço compensado em quatro pontos de operação. Os círculos marcam os cruzamentos por 0 dB.')
    p(f"Duas ressalvas completam a análise. Os polos do compensador ficam acima de f_{{s}} e perto de 40 kHz, de modo que o ganho de "
      f"{f(MAL['Cv_40kHz'], 1)} nessa frequência leva a ondulação de saída ao sinal modulante. E o modelo médio ignora o atraso do "
      f"modulador: um atraso de 1/(4f_{{s}}) reduziria a margem a 373 V para {f(MAL['pontos_com_atraso']['373 V, plena 2100 W']['cruzamentos_0dB'][0]['MF_graus'], 1)}°. "
      'Os componentes comerciais do circuito PSIM do professor deslocam os zeros para 861 e 865 Hz e o cruzamento para 7,85 kHz; por isso '
      'aquela simulação não valida exatamente a função publicada.')

    h('VI. Conversor CC-CC de Alto Ganho')
    p('O circuito do professor revela um elevador com célula de comutação de três estados (Fig. 3): o indutor L_{b} alimenta a '
      'derivação central de um autotransformador cujas extremidades vão às chaves S_{1} e S_{2} e, por D_{17} e D_{18}, ao capacitor '
      'C_{8}. Um terceiro enrolamento alimenta uma ponte que carrega C_{7}, empilhado sobre C_{8}. É a topologia de [5], da mesma '
      'família de conversores de alto ganho para no-breaks e fontes de baixa tensão [6] a [8]. Com D > 0,5, o balanço de volt-segundo '
      'em L_{b} e a reflexão no secundário dão')
    eq('V_{bus}=V_{C8}+V_{C7}=\\frac{V_{bat}}{1−D}(1+\\frac{a}{2})')
    fig(FIG / 'circuito_cc.png', 'Conversor CC-CC elevador identificado no circuito do professor: célula de três estados com secundário 1:1 em ponte e C_{7} empilhado sobre C_{8}.')
    pc42, pc56 = CC['pontos']['42'], CC['pontos']['56']
    p(f"Com a = 1 e 42 V, D = 0,7 leva a {f(pc42['VC8'], 0)} V em C_{{8}}, {f(pc42['VC7'], 0)} V em C_{{7}} e {f(pc42['Vbus'], 0)} V no barramento; "
      f"a 56 V a razão cíclica cai para {f(pc56['D'], 2)}. As chaves bloqueiam apenas {f(pc42['V_chave'], 0)} V. O indutor opera em 40 kHz, "
      'com ondulação')
    eq('ΔI_{Lb}=\\frac{V_{bat}(2D−1)}{2f_{s}L_{b}}')
    p(f"igual a {f(pc42['dILb_pp'])} A com L_{{b}} = 39,2 µH. A corrente média da bateria é {f(pc42['Iib'])} A sem considerar o rendimento "
      f"do próprio conversor e {f(pc42['Iib_com_eta095'], 1)} A com 0,95 (hipótese). Os 210 V ficam só "
      f"{f(P['retificador']['Vimin_cc'] - 210)} V abaixo do vale do retificador; em malha aberta, como no circuito do professor, o "
      'elevador continuaria drenando a bateria com a rede presente. Por isso os ensaios principais mantêm o CC-CC em espera e o '
      'habilitam no instante da falta.')

    B.extend(secao_resultados())

    h('VIII. Conclusões')
    for par in conclusoes():
        p(par)
    return B


def secao_resultados():
    B = [('h', 'VII. Resultados de Simulação')]
    if not M:
        B.append(('p', 'Os quatro modelos do PLECS e a matriz de ensaios estão prontos, mas a simulação ainda não foi executada. '
                       'Esta seção será escrita a partir dos arquivos de resultados.'))
    return B


def conclusoes():
    return ['A reconstrução da planilha confirmou os valores numéricos do professor e corrigiu pontos de texto e de interpretação: '
            'a ondulação de 15% do retificador, o corte do filtro em f_{s}/20, a atenuação de 26,22 dB e a margem de ganho finita. '
            'O índice de modulação deve ser avaliado no vale do retificador e na saída do CC-CC, onde chega a 0,774, ainda abaixo de 0,85.']


REFERENCIAS = [
    'S. B. Bekiarov e A. Emadi, “Uninterruptible power supplies: classification, operation, dynamics, and control,” em Proc. IEEE APEC, 2002, v. 1, pp. 597–604, doi: 10.1109/APEC.2002.989305.',
    'A. Emadi, A. Nasiri e S. B. Bekiarov, Uninterruptible Power Supplies and Active Filters. Boca Raton, FL, EUA: CRC Press, 2005.',
    'Uninterruptible Power Systems (UPS), Part 3: Method of Specifying the Performance and Test Requirements, IEC 62040-3, ed. 2.0, 2011.',
    'R. P. Torrico-Bascopé, “Projeto de um no-break dupla conversão monofásico de 3 kVA,” planilha de projeto, Eletrônica Industrial (TH0263), UFC, Fortaleza, out. 2026 (material didático não publicado).',
    'S. V. Araújo, R. P. Torrico-Bascopé e G. V. Torrico-Bascopé, “Highly efficient high step-up converter for fuel-cell power processing based on three-state commutation cell,” IEEE Trans. Ind. Electron., v. 57, n. 6, pp. 1987–1997, jun. 2010, doi: 10.1109/TIE.2009.2029521.',
    'C. E. A. Silva, R. P. T. Bascopé e D. S. Oliveira Jr., “Proposal of a new high step-up converter for UPS applications,” em Proc. IEEE ISIE, 2006, pp. 1288–1292, doi: 10.1109/ISIE.2006.295658.',
    'Y. J. A. Alcazar, D. S. Oliveira, F. L. Tofoli e R. P. Torrico-Bascopé, “DC–DC nonisolated boost converter based on the three-state switching cell and voltage multiplier cells,” IEEE Trans. Ind. Electron., v. 60, n. 10, pp. 4438–4449, out. 2013.',
    'C. G. C. Branco, R. P. Torrico-Bascopé, F. L. Tofoli e C. M. T. Cruz, “Three-state switching cell (3SSC)-based non-isolated dc–dc boost-type converter with balanced output voltage and wide voltage conversion range,” IET Power Electron., v. 11, n. 7, pp. 1217–1223, 2018, doi: 10.1049/iet-pel.2017.0551.',
    'F. M. A. Linard, “Sistema ininterrupto de energia de dupla conversão com integração do retificador e do inversor,” dissertação de mestrado, Universidade Federal do Ceará, Fortaleza, 2009.',
    'M. F. Apolinário, “Nobreak dupla conversão monofásico isolado em alta frequência com tensão de entrada bivolt e potência de 1 kVA, baseado no conceito de circuito multi-portas,” dissertação de mestrado, Universidade Federal do Ceará, Fortaleza, 2017.',
    'Plexim GmbH, PLECS 5.0 Documentation. Zurique, Suíça (documentação instalada com o PLECS Standalone 5.0).',
]
