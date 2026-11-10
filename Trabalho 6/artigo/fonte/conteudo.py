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
    t = ('Os modelos foram simulados no PLECS 5.0 por interface XML-RPC, com solver implícito e saída em instantes '
         'especificados, e cada resultado está ligado ao arquivo do modelo, às opções do solver e ao CSV por resumo criptográfico. ')
    if tem('nb_176_nl'):
        nb = M['nb_176_nl']
        tr = nb.get('transferencia', {})
        t += (f"Na rede mínima com a carga não linear de referência, a saída fica em {f(nb['rede']['c_saida']['Vo_ef_V'])} V eficazes com "
              f"{f(nb['rede']['c_saida']['DHT_vo_pct'])}% de distorção, e na falta da rede o menor valor eficaz por semiciclo é "
              f"{f(tr.get('Vo_ef_semiciclo_min_V', 0))} V. ")
    if 'regulacao' in M and all(v in M['regulacao'] for v in ('176', '220', '264')):
        rr = M['regulacao']
        t += (f"O coeficiente de regulação de 0 a 2100 W fica em {f(rr['176']['RV_pct'])}%, {f(rr['220']['RV_pct'])}% e "
              f"{f(rr['264']['RV_pct'])}% para 176, 220 e 264 V. ")
    return t + 'As diferenças em relação ao cálculo são atribuídas aos elementos que a planilha não modela.'


def _c(x, n=2):
    """Numero com virgula decimal; 'n.d.' quando a grandeza nao se aplica ao ensaio."""
    return 'n.d.' if x is None else f(x, n)


def pct(a, b):
    """Diferenca relativa de a (simulado) para b (calculado), em porcentagem."""
    if a is None or not b:
        return 'n.d.'
    return f((a - b) / abs(b) * 100, 1) + '%'


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
      f"a 56 V a razão cíclica cai para {f(pc56['D'], 2)}. Cada enrolamento do primário fica com {f(pc42['V_Np'], 0)} V, "
      f"e as chaves bloqueiam {f(pc42['V_chave'], 0)} V, porque o dreno da chave aberta é grampeado em V_{{C8}} pelo seu "
      'próprio diodo; é a vantagem da célula de três estados frente a um elevador simples, que exigiria a tensão do '
      'barramento inteiro. O indutor opera em 40 kHz, com ondulação')
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
    B = []
    h = lambda x: B.append(('h', x))
    sub = lambda x: B.append(('sub', x))
    p = lambda x: B.append(('p', x))
    fig = lambda arq, leg: B.append(('fig', arq, leg))
    tab = lambda leg, lin, larg: B.append(('tab', leg, lin, larg))

    h('VII. Resultados de Simulação')
    if not M:
        p('Os cinco modelos do PLECS e a matriz de ensaios estão prontos, mas a simulação ainda não foi executada. '
          'Esta seção será escrita a partir dos arquivos de resultados.')
        return B

    n_ok = len([k for k in M if not k.startswith('_') and k != 'regulacao'])
    p('Os modelos são escritos como texto pelo gerador, a partir do mesmo arquivo de parâmetros usado nos cálculos, e '
      'executados no PLECS por interface XML-RPC. O solver é implícito, com passo máximo de 5 µs, tolerância relativa de '
      '10^{−6} e detecção de eventos de comutação independente da grade de saída, pedida em instantes especificados. Cada '
      f"ensaio grava o CSV, o retorno nativo e um registro com o resumo criptográfico do modelo, as opções do solver, a "
      f"duração e o número de amostras, de modo que todo valor desta seção pode ser refeito. Foram analisados {n_ok} ensaios "
      'além das curvas de regulação. As janelas de regime têm número inteiro de ciclos de 60 Hz e as integrais são trapezoidais.')
    p('Os blocos ficam em grade, por grupos funcionais e com o fluxo de potência da esquerda para a direita, e cada fio '
      'traz os seus pontos de passagem, de modo que todo segmento é horizontal ou vertical e nenhum passa sobre um bloco. '
      'Os sinais levados aos terminais de saída correm por uma faixa própria, entre o estágio de potência e o conversor '
      'de baterias, para não atravessar o circuito. As capturas dos cinco esquemas, em tamanho legível, acompanham o '
      'memorial do trabalho; aqui elas seriam reduzidas a ponto de não se ler nenhum rótulo.')

    # ---------------- retificador ----------------
    if tem('ret_176_anexo', 'ret_176_planilha'):
        ra, rp_ = M['ret_176_anexo'], M['ret_176_planilha']
        c = ra['comparacao_A']
        sub('A. Retificador e barramento')
        tab('Retificador a 176 V: cálculo e simulação', [
            ['Grandeza', 'Cálculo', 'Seção 3', 'Anexo 01'],
            ['Vale do barramento (V)', f(c['VC1min_V']), f(rp_['v_bus_min_V']), f(ra['v_bus_min_V'])],
            ['Ondulação (V)', f(R['dVC']), f(rp_['ondulacao_bus_Vpp']), f(ra['ondulacao_bus_Vpp'])],
            ['Pico em D1 (A)', f(c['ID1pk_2Ichg_A'], 1), f(rp_['i_D1_pico_A'], 1), f(ra['i_D1_pico_A'], 1)],
            ['Média em D1 (A)', f(c['ID1med_A'], 3), f(rp_['i_D1_media_A'], 3), f(ra['i_D1_media_A'], 3)],
            ['Eficaz em D1 (A)', f(c['ID1ef_A']), f(rp_['i_D1_ef_A']), f(ra['i_D1_ef_A'])],
            ['Eficaz em C4 (A)', f(c['IC1ef_A']), f(rp_['i_C4_ef_A']), f(ra['i_C4_ef_A'])],
            ['Condução por pulso (ms)', f(c['tC1_ms']), f(rp_['duracao_pulso_ms']), f(ra['duracao_pulso_ms'])]],
            [.37, .21, .21, .21])
        p(f"Nas condições idealizadas da seção 3 o vale fica em {f(rp_['v_bus_min_V'])} V, contra {f(c['VC1min_V'])} V do cálculo "
          f"({pct(rp_['v_bus_min_V'], c['VC1min_V'])}), o que confirma o dimensionamento de C1 e o ângulo de condução. Com os "
          f"1880 µF, a ESR, os 0,1 Ω e os diodos reais do Anexo 01, o vale sobe para {f(ra['v_bus_min_V'])} V, porque a "
          f"capacitância adotada é maior que a calculada. O efeito mais visível está no pico de corrente: a aproximação de "
          f"pulso retangular prevê {f(c['ID1pk_2Ichg_A'], 1)} A, enquanto a simulação dá {f(rp_['i_D1_pico_A'], 1)} A sem "
          f"resistência série e {f(ra['i_D1_pico_A'], 1)} A com os 0,1 Ω. A média e o valor eficaz, que dependem da carga "
          'transferida e não do formato do pulso, ficam próximos do cálculo. O fator de potência de entrada medido é '
          f"{f(ra['FP_entrada'], 3)}, típico de retificador com filtro capacitivo sem correção.")
        fig(FIG / 'retificador_176.png', 'Barramento e corrente em D1 a 176 V, nas condições da seção 3 e nas do Anexo 01. '
                                         'A linha pontilhada é a corrente de recarga calculada.')

    # ---------------- CC-CC ----------------
    if tem('elev_42', 'elev_56'):
        e42, e56 = M['elev_42'], M['elev_56']
        c42, c56 = e42['comparacao_A'], e56['comparacao_A']
        sub('B. Conversor CC-CC de alto ganho')
        tab('CC-CC em malha aberta, carga de 2250 W', [
            ['Grandeza', '42 V cálc.', '42 V sim.', '56 V cálc.', '56 V sim.'],
            ['Barramento (V)', f(c42['Vbus_V'], 1), f(e42['v_bus_media_V'], 1), f(c56['Vbus_V'], 1), f(e56['v_bus_media_V'], 1)],
            ['V em C8 (V)', f(c42['VC8_V'], 1), f(e42['v_C8_media_V'], 1), f(c56['VC8_V'], 1), f(e56['v_C8_media_V'], 1)],
            ['V em C7 (V)', f(c42['VC7_V'], 1), f(e42['v_C7_media_V'], 1), f(c56['VC7_V'], 1), f(e56['v_C7_media_V'], 1)],
            ['Corrente média (A)', f(c42['Iib_A'], 1), f(e42['i_bat_media_A'], 1), f(c56['Iib_A'], 1), f(e56['i_bat_media_A'], 1)],
            ['ΔI_{Lb} (A)', f(c42['dILb_pp_A']), _c(e42['dILb_pp_A']), f(c56['dILb_pp_A']), _c(e56['dILb_pp_A'])],
            ['Bloqueio da chave (V)', f(c42['V_chave_V'], 1), f(e42['v_S1_max_V'], 1), f(c56['V_chave_V'], 1), f(e56['v_S1_max_V'], 1)]],
            [.3, .175, .175, .175, .175])
        p(f"Com 42 V e D = 0,70 o barramento medido é {f(e42['v_bus_media_V'], 1)} V, contra {f(c42['Vbus_V'], 1)} V do modelo "
          f"ideal ({pct(e42['v_bus_media_V'], c42['Vbus_V'])}), e a repartição entre C8 e C7 segue a prevista. A diferença "
          'vem das quedas nos diodos rápidos, da resistência de condução das chaves e das resistências dos enrolamentos, '
          'nenhuma delas presente no balanço de volt-segundo ideal. A ondulação em L_{b} e a tensão de bloqueio das chaves '
          f"confirmam o dimensionamento: as chaves veem {f(e42['v_S1_max_V'], 1)} V, pouco mais que o valor de C8, o que é a "
          'vantagem central da célula de três estados. O rendimento do próprio conversor no modelo, sem perdas de comutação, '
          f"fica em {f(e42['rendimento_modelo'] * 100, 1)}% a 42 V e {f(e56['rendimento_modelo'] * 100, 1)}% a 56 V.")
        fig(FIG / 'elevador_42.png', 'CC-CC a 42 V em regime: comando de S_{1}, correntes de L_{b} e de S_{1} e tensão sobre S_{1} '
                                     'em três períodos de comutação.')

    # ---------------- inversor ----------------
    nomes_inv = [n for n in ('inv_373_res', 'inv_2116_res', 'inv_2116_nl', 'inv_2116_vazio') if n in M]
    if nomes_inv:
        sub('C. Inversor com barramento ideal')
        rot = {'inv_373_res': '373 V, 2100 W', 'inv_2116_res': '211,6 V, 2100 W',
               'inv_2116_nl': '211,6 V, não linear', 'inv_2116_vazio': '211,6 V, vazio'}
        linhas = [['Ensaio', 'V_{o} ef (V)', 'DHT (%)', 'M efet.', 'ΔI_{Lo} (A)']]
        for n in nomes_inv:
            m_ = M[n]
            linhas.append([rot[n], f(m_['Vo_ef_V']), f(m_['DHT_vo_pct']), f(m_['M_efetivo'], 3), _c(m_.get('dILo_pp_no_pico_A'))])
        tab('Inversor em malha fechada com barramento ideal', linhas, [.32, .18, .16, .16, .18])
        ir = M.get('inv_2116_res') or M[nomes_inv[0]]
        p(f"Com barramento ideal a saída fica em {f(ir['Vo_ef_V'])} V eficazes, dentro de 2% dos 115 V de referência, e a "
          f"distorção da tensão é de {f(ir['DHT_vo_pct'])}% com carga resistiva. O índice de modulação efetivo medido, "
          f"{f(ir['M_efetivo'], 3)}, confirma a previsão de {f(ir['comparacao_A']['M_pico'], 3)} obtida com o barramento no "
          'vale, e não o valor otimista da planilha, calculado com 223 V. A ondulação do indutor no pico da tensão de saída, '
          f"{_c(ir.get('dILo_pp_no_pico_A'))} A, fica abaixo do critério de {f(INV['dILo_criterio'])} A.")
        if 'inv_2116_nl' in M:
            nl = M['inv_2116_nl']
            p(f"Com a carga não linear de referência a corrente tem fator de crista {_c(nl.get('fator_crista'))} e a distorção "
              f"da tensão sobe para {f(nl['DHT_vo_pct'])}%, ainda dentro do limite de 8% adotado para esse tipo de carga. "
              'O compensador mantém a forma da tensão apesar dos pulsos estreitos de corrente, que são o caso mais severo '
              'para a malha porque excitam o filtro bem acima da frequência de cruzamento.')
        fig(FIG / 'inversor_2116.png', 'Tensão e corrente de saída do inversor a 211,6 V com carga resistiva de 2100 W e com a '
                                       'carga não linear de referência, em dois ciclos de 60 Hz.')
        if 'inv_degrau_2116' in M and 'degrau' in M['inv_degrau_2116']:
            dg = M['inv_degrau_2116']['degrau']
            p(f"No degrau de vazio para 2100 W aplicado no pico da tensão, o erro instantâneo fica entre "
              f"{f(dg['erro_min_V'])} V e {f(dg['erro_max_V'])} V e o valor eficaz passa de {f(dg['Vo_ef_antes_V'])} V para "
              f"{f(dg['Vo_ef_depois_V'])} V em dois ciclos, sem oscilação sustentada. É a verificação temporal da margem de "
              'fase calculada no ponto mais exigente do laço.')
            fig(FIG / 'degrau_2116.png', 'Degrau de vazio para 2100 W no pico da tensão de saída, a 211,6 V de barramento: '
                                         'tensão de saída com a referência e corrente de saída.')

    # ---------------- no-break completo ----------------
    casos = [n for n in ('nb_176_nl', 'nb_220_lin', 'nb_264_nl', 'nb_220_rl3k') if n in M]
    if casos:
        sub('D. No-break completo: rede, falta e bateria')
        rot = {'nb_176_nl': '176 V, n. lin.', 'nb_220_lin': '220 V, resist.',
               'nb_264_nl': '264 V, n. lin.', 'nb_220_rl3k': '220 V, RL 3 kVA'}
        linhas = [['Ensaio', 'Modo', 'V_{bus} méd. (V)', 'V_{o} ef (V)', 'DHT (%)', 'M efet.']]
        for n in casos:
            for modo, rmodo in (('rede', 'rede'), ('bateria', 'bat.')):
                if modo not in M[n]:
                    continue
                b_, c_ = M[n][modo]['b_barramento'], M[n][modo]['c_saida']
                linhas.append([rot[n] if modo == 'rede' else '', rmodo, f(b_['Vbus_media_V'], 1), f(c_['Vo_ef_V']),
                               f(c_['DHT_vo_pct']), f(c_['M_efetivo'], 3)])
        tab('No-break completo: grupos (b) e (c) da seção 6', linhas, [.26, .12, .2, .16, .13, .13])
        n0 = casos[0]
        nb = M[n0]
        p(f"Com a rede presente o barramento acompanha o retificador e a saída permanece regulada em torno de 115 V em todos "
          f"os casos. Na falta, o CC-CC assume e o barramento cai para o patamar de {f(nb['bateria']['b_barramento']['Vbus_media_V'], 1)} V, "
          f"com C8 em {f(nb['bateria']['b_barramento']['VC8_media_V'], 1)} V e C7 em {f(nb['bateria']['b_barramento']['VC7_media_V'], 1)} V. "
          f"O índice de modulação sobe de {f(nb['rede']['c_saida']['M_efetivo'], 3)} para "
          f"{f(nb['bateria']['c_saida']['M_efetivo'], 3)} nesse caso, porque o barramento é menor, e continua abaixo de 0,85. "
          f"A corrente média de bateria é {f(nb['bateria']['b_barramento']['Ibat_media_A'], 1)} A, com pico de "
          f"{f(nb['bateria']['b_barramento']['Ibat_pico_A'], 1)} A, valores compatíveis com o dimensionamento do banco.")
        fig(FIG / 'nb_176_nl.png', 'No-break completo a 176 V com carga não linear: (a) entrada, (b) barramento e bateria, '
                                   '(c) saída. A linha pontilhada marca a falta da rede em 100 ms.')
        if 'transferencia' in nb:
            tr = nb['transferencia']
            p(f"A transferência é o ponto crítico da especificação. Com a falta no cruzamento por zero, o menor valor eficaz por "
              f"semiciclo da tensão de saída é {f(tr['Vo_ef_semiciclo_min_V'])} V, contra "
              f"{f(tr['Vo_ef_semiciclo_max_V'])} V no melhor semiciclo, o que corresponde a uma queda de "
              f"{f((tr['Vo_ef_semiciclo_max_V'] - tr['Vo_ef_semiciclo_min_V']) / tr['Vo_ef_semiciclo_max_V'] * 100, 1)}% e atende "
              'ao critério de 10% adotado. O barramento não cai abaixo de '
              f"{f(tr['Vbus_min_apos_V'], 1)} V no transitório, e o pico de corrente de bateria chega a "
              f"{f(tr['Ibat_pico_A'], 1)} A enquanto o CC-CC recompõe a tensão.")
            fig(FIG / 'transferencia_176_nl.png', 'Transferência de rede para bateria a 176 V com carga não linear: saída e '
                                                  'referência, barramento e corrente de bateria entre 90 ms e 130 ms.')
        if 'nb_176_nl_pico' in M and 'transferencia' in M['nb_176_nl_pico']:
            tp = M['nb_176_nl_pico']['transferencia']
            p(f"Com a falta no pico positivo da rede, quando a ponte conduz, o menor eficaz por semiciclo é "
              f"{f(tp['Vo_ef_semiciclo_min_V'])} V, praticamente o mesmo caso anterior. O instante da falta importa pouco "
              'porque o capacitor do barramento sustenta a tensão durante o tempo de detecção, aqui idealizado como nulo.')
        if 'nb_220_retorno' in M and 'transferencia' in M['nb_220_retorno']:
            rt = M['nb_220_retorno']['transferencia']
            p(f"No retorno da rede a 220 V, o fechamento de SS2 produz um pico de corrente de entrada de {f(rt['Iin_pico_A'], 1)} A, "
              'limitado apenas pelos 0,1 Ω entre a ponte e o barramento. Esse valor é um resultado do modelo adotado e indica '
              'que um no-break construído assim precisa de limitação de corrente de entrada, por termistor ou por pré-carga '
              'comandada, assunto que o projeto de partida não trata.')
            fig(FIG / 'retorno_220.png', 'Retorno da rede a 220 V com carga resistiva: corrente de entrada, barramento e '
                                         'tensão de saída entre 190 ms e 240 ms.')
        if 'nb_176_nl_anexo' in M:
            an = M['nb_176_nl_anexo']
            p('A comparação com o comando permanente do circuito do professor mostra por que os ensaios principais mantêm o '
              f"CC-CC em espera: com a razão cíclica sempre aplicada, a bateria entrega {f(an['rede']['b_barramento']['Ibat_media_A'], 1)} A "
              'em média mesmo com a rede presente, porque o elevador em malha aberta disputa o barramento com o retificador.')

    # ---------------- regulacao ----------------
    if 'regulacao' in M:
        sub('E. Curvas de regulação')
        rr = M['regulacao']
        linhas = [['Rede', 'V_{o} em vazio (V)', 'V_{o} a 2100 W (V)', 'RV (%)']]
        rotr = {'176': '176 V', '220': '220 V', '264': '264 V', 'bat': 'Bateria 42 V'}
        for V in ('176', '220', '264', 'bat'):
            if V not in rr or 'RV_pct' not in rr[V]:
                continue
            pts = {q['Po_nominal_W']: q for q in rr[V]['pontos']}
            linhas.append([rotr[V], f(pts[0]['Vo_ef_V']), f(pts[2100]['Vo_ef_V']), f(rr[V]['RV_pct'])])
        tab('Coeficiente de regulação da tensão de saída', linhas, [.28, .26, .26, .2])
        valores = [rr[V]['RV_pct'] for V in rr if 'RV_pct' in rr[V]]
        p('As curvas V_{o} = f(P_{o}) foram levantadas em onze pontos de 0 a 2100 W para cada tensão de entrada, com a janela '
          'de regime de seis ciclos. O coeficiente de regulação, definido como a variação relativa entre vazio e plena carga, '
          f"fica entre {f(min(valores))}% e {f(max(valores))}%, abaixo do limite de 2% adotado. A tensão de entrada quase não "
          'altera a curva enquanto o barramento permanece acima do necessário para o índice de modulação, o que era esperado '
          'de uma malha com ganho elevado em 60 Hz. O ramo em bateria é o mais sensível, porque o barramento é o menor de todos.')
        fig(FIG / 'regulacao.png', 'Tensão eficaz de saída em função da potência de saída nominal, para 176, 220 e 264 V de '
                                   'entrada e para operação em bateria a 42 V. A escala vertical cobre 0,2 V em 115 V.')

    # ---------------- verificacao e limitacoes ----------------
    sub('F. Verificação numérica e limitações')
    if 'verificacao_convergencia' in M and M['verificacao_convergencia']:
        cv = M['verificacao_convergencia']
        nomes = {'Vo_ef_V': 'na tensão eficaz de saída', 'DHT_vo_pct': 'na distorção da tensão de saída',
                 'Vbus_media_V': 'na tensão média do barramento', 'Ibat_media_A': 'na corrente média da bateria',
                 'Iin_ef_A': 'na corrente eficaz de entrada'}
        pior = max(cv.items(), key=lambda kv: kv[1]['dif_rel'])
        modo, chave = pior[0].split('.')
        expo = int(f"{pior[1]['dif_rel'] * 100:e}".split('e')[1])
        p(f"O ensaio de refinamento repete o caso de 176 V com passo máximo de 1 µs, cinco vezes menor, e tolerância relativa "
          f"de 10^{{−7}}, dez vezes menor. A maior diferença entre as duas execuções, entre as cinco grandezas comparadas, é "
          f"da ordem de 10^{{{expo}}}%, {nomes.get(chave, chave)} no modo {modo}. Nenhuma conclusão deste trabalho, "
          'portanto, depende da escolha do passo ou da tolerância; a localização dos eventos de comutação pelo solver, '
          'independente da grade de saída, é o que garante isso.')
    diag = [k for k in M if k.startswith('diag_cc_')]
    if diag:
        falhos = [k for k in diag if M[k].get('status') != 'executado']
        p('O conversor de alto ganho exigiu um cuidado numérico. Sem nenhuma capacitância nos nós de comutação, o modelo trava '
          'quando a corrente de um ramo se anula com a chave e o diodo abertos, porque o nó fica sem referência. O grupo de '
          f"diagnóstico compara o circuito com e sem ramos RC de 33 Ω e 1 nF em paralelo com as chaves e com o secundário: "
          + ('o caso sem amortecimento estourou o limite de tempo de relógio em pelo menos um ensaio, '
             if falhos else 'os casos sem amortecimento foram os mais lentos, ')
          + 'enquanto os ensaios com os ramos RC terminam normalmente. Os ramos representam a capacitância de saída das '
            'chaves, da ordem de 1 nF, e a sua perda estimada é inferior a 1 W nos três, desprezível diante de 2250 W.')
    p('As limitações valem para todos os números desta seção. Os modelos não têm tempo morto nem perdas de comutação, os '
      'indutores são lineares, o transformador não satura, a bateria é uma fonte ideal e não há modelo térmico nem de '
      'interferência eletromagnética. A lógica de transferência é ideal, com detecção instantânea da falta. As condições '
      'iniciais evitam o transitório de partida e, portanto, não certificam a partida real, que exigiria pré-carga do '
      'barramento. Os rendimentos citados são do modelo e não medições.')
    return B


def conclusoes():
    C = ['A reconstrução da planilha confirmou os valores numéricos do professor e corrigiu pontos de texto e de interpretação: '
         'a ondulação de 15% do retificador, o corte do filtro em f_{s}/20, a atenuação de 26,22 dB e a margem de ganho finita. '
         'O índice de modulação deve ser avaliado no vale do retificador e na saída do CC-CC, onde chega a 0,774, ainda abaixo de 0,85.']
    if not M:
        return C
    if tem('ret_176_planilha', 'ret_176_anexo'):
        rp_, ra = M['ret_176_planilha'], M['ret_176_anexo']
        C.append('A simulação confirma o dimensionamento do estágio de entrada e mostra onde a aproximação da planilha deixa de '
                 f"valer. O vale do barramento nas condições da seção 3, {f(rp_['v_bus_min_V'])} V, está a "
                 f"{pct(rp_['v_bus_min_V'], rp_['comparacao_A']['VC1min_V'])} do calculado, mas o pico de corrente no diodo previsto "
                 f"por 2·I_{{chg}} subestima o valor simulado sem resistência série e superestima o valor com os 0,1 Ω do circuito "
                 'do professor. Esse é um resultado prático: o pico depende da impedância do laço de recarga, que a planilha não '
                 'inclui, e é ele que define o diodo e a corrente de partida.')
    if tem('elev_42'):
        e42 = M['elev_42']
        C.append('O conversor de alto ganho com célula de três estados entrega o barramento previsto com razão cíclica de 0,70 a '
                 f"42 V, {f(e42['v_bus_media_V'], 1)} V contra {f(e42['comparacao_A']['Vbus_V'], 1)} V do modelo ideal, e submete "
                 f"as chaves a {f(e42['v_S1_max_V'], 1)} V, cerca de dois terços do barramento, contra o barramento inteiro de um "
                 'elevador simples. A diferença em relação ao cálculo vem das quedas de condução, que o balanço de volt-segundo '
                 'não representa, e cresce com a corrente.')
    if tem('nb_176_nl') and 'transferencia' in M['nb_176_nl']:
        nb, tr = M['nb_176_nl'], M['nb_176_nl']['transferencia']
        C.append('No conjunto completo, a saída permanece regulada na rede e na bateria, e a transferência no pior caso ensaiado '
                 f"deixa o menor valor eficaz por semiciclo em {f(tr['Vo_ef_semiciclo_min_V'])} V, queda de "
                 f"{f((tr['Vo_ef_semiciclo_max_V'] - tr['Vo_ef_semiciclo_min_V']) / tr['Vo_ef_semiciclo_max_V'] * 100, 1)}%, dentro "
                 'do critério adotado. A distorção da tensão de saída fica dentro dos limites também com a carga não linear de '
                 f"referência, {f(nb['rede']['c_saida']['DHT_vo_pct'])}% com a rede presente.")
    if 'regulacao' in M:
        vals = [M['regulacao'][V]['RV_pct'] for V in M['regulacao'] if 'RV_pct' in M['regulacao'][V]]
        if vals:
            C.append(f"O coeficiente de regulação fica entre {f(min(vals))}% e {f(max(vals))}% nas quatro condições levantadas, "
                     'abaixo do limite de 2%, e praticamente não depende da tensão de entrada enquanto o barramento se mantém '
                     'acima do mínimo exigido pelo índice de modulação.')
    C.append('Dois pontos ficam como recomendação para a continuação. O retorno da rede produz, no modelo, um pico de corrente de '
             'entrada limitado apenas pela resistência de 0,1 Ω, o que indica a necessidade de limitação de corrente na recarga do '
             'barramento. E o elevador em malha aberta, comandado permanentemente como no circuito de partida, drena a bateria com '
             'a rede presente, de modo que a habilitação condicionada à falta, adotada aqui, é parte do projeto e não um detalhe '
             'de simulação. Perdas de comutação, tempo morto, saturação magnética e comportamento térmico continuam fora do escopo '
             'e são o passo natural seguinte.')
    return C


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
