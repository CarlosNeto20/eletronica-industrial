# -*- coding: utf-8 -*-
"""Conteúdo do artigo IEEE do Trabalho 3. Blocos: h1, h2, p, eq, fig, tab, bul.

Fonte dos números: desenvolvimento/calculos/parametros_projeto.py (conferência
da planilha do professor) e resultados PLECS/metricas_ensaios.md. Figuras em
artigo/figuras, montadas por montar_figuras.py. A numeração das figuras segue
a lista ORDEM abaixo (o texto usa N[...] para citar); a das equações é explícita.
"""
import os

TITULO = ("Projeto e Simulação de um Carregador de Baterias de 15 A\n"
          "Baseado no Conversor Forward de Duas Chaves")

AUTORES = [
    dict(nome="Jonatas Manoel Assunção Felix",
         dep="Departamento de Engenharia Elétrica",
         org="Universidade Federal do Ceará",
         cid="Fortaleza, Brasil",
         mail="jonatasmanoela@gmail.com"),
    dict(nome="José Carlos Moreira de Brito Neto",
         dep="Departamento de Engenharia Elétrica",
         org="Universidade Federal do Ceará",
         cid="Fortaleza, Brasil",
         mail="cneto3240@gmail.com"),
]

RESUMO = (
    "Este trabalho apresenta o projeto e a simulação de um carregador de baterias estacionárias "
    "de 24 V com corrente de recarga ajustável de 0 a 15 A. A rede de 220 V alimenta um "
    "retificador a diodos com filtro capacitivo, seguido de um conversor Forward de duas chaves "
    "que opera a 50 kHz. A partir da planilha de projeto fornecida na disciplina, são conferidos "
    "o capacitor de barramento, a relação de espiras, o filtro de saída e os compensadores das "
    "malhas de tensão e de corrente, projetados pelo método do fator K. São acrescentados a "
    "análise qualitativa do Forward de duas chaves, os esforços e a escolha dos semicondutores "
    "comerciais e a lista de componentes do controle com o UC3525A. O carregador foi simulado no "
    "PLECS com o controle analógico completo, nas tensões de rede de 176 V e de 264 V. Os "
    "resultados reproduzem os da planilha, obtidos no PSIM: tensão regulada em 27 V com vale de "
    "25,6 V no degrau de carga de 20 % para 100 %, corrente limitada em 15 A durante um "
    "curto-circuito na saída e recarga em corrente constante seguida de tensão constante. O "
    "fator de potência medido ficou entre 0,34 e 0,41. A simulação mostrou ainda que, com a "
    "carga nominal, o carregador opera na fronteira entre as duas malhas, o que satura o "
    "compensador de tensão e eleva de 28,4 V para 29,3 V o pico de tensão na retirada de carga. "
    "Uma folga de 4 % no limite de corrente elimina o efeito."
)

PALAVRAS = ("carregador de baterias, Forward de duas chaves, retificador com filtro capacitivo, "
            "fator de potência, fator K, compensador tipo 2, UC3525A, PLECS")

_T3 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEM_PLECS = os.path.exists(os.path.join(_T3, "simulação PLECS", "simulacao-circuitos",
                                        "plecs-circ-carregador.png"))

ORDEM = ["ret-topologia", "ret-formas", "ds-c1", "fwd-topologia", "fwd-etapas", "fwd-formas",
         "ds-co", "ds-semicondutores", "ctrl-blocos", "ctrl-tipo2", "ctrl-bode-tensao",
         "ctrl-bode-corrente", "ctrl-uc3525", "sim-circuito-psim"]
if TEM_PLECS:
    ORDEM.append("sim-circuito-plecs")
ORDEM += ["sim-retificador", "sim-forward", "sim-portadora", "sim-degrau", "sim-degrau-100-20",
          "sim-degrau-20-100", "sim-curto", "sim-curto-detalhe", "sim-recarga"]
N = {k: i + 1 for i, k in enumerate(ORDEM)}

C = []
def h1(t): C.append(("h1", t))
def h2(t): C.append(("h2", t))
def p(t): C.append(("p", t))
def eq(t, n): C.append(("eq", t, n))
def fig(f, cap, span=1):
    assert f == ORDEM[sum(1 for b in C if b[0] == "fig")], "figura fora da ordem: " + f
    C.append(("fig", f, cap, span))
def tab(cap, rows, widths, span=1, note=None):
    C.append(("tab", cap, rows, widths, span, note))
def bul(items): C.append(("bul", items))


# =====================================================================
h1("Introdução")
p("Baterias estacionárias de chumbo-ácido de 7 Ah a 150 Ah alimentam a iluminação de emergência "
  "de casas, edifícios e centros comerciais. Elas passam quase toda a vida em flutuação e são "
  "exigidas apenas quando a rede falta, de modo que a sua durabilidade depende de como são "
  "recarregadas: corrente excessiva aquece e deforma as placas, e tensão acima da de flutuação "
  "acelera a corrosão e a perda de água [3], [4]. O carregador precisa, portanto, limitar a "
  "corrente durante a recarga e regular a tensão quando a bateria se aproxima da carga plena.")
p("O objetivo deste trabalho é projetar e simular um carregador desse tipo, com corrente de "
  "recarga ajustável de 0 a 15 A por uma referência V_refi de 0 a 2,5 V, para um banco de 24 V "
  "[1]. A energia vem da rede por um retificador a diodos com filtro capacitivo, e a adaptação "
  "de tensão, a isolação e o controle ficam a cargo de um conversor CC-CC Forward de duas "
  "chaves. Essa topologia foi escolhida pela faixa de potência, por entregar à carga uma "
  "corrente filtrada por indutor e, principalmente, por submeter as chaves apenas à tensão de "
  "entrada, e não ao dobro dela como no Forward de uma chave. O ponto fraco do arranjo está na "
  "entrada: o retificador com filtro capacitivo drena da rede uma corrente pulsada, com fator "
  "de potência inferior a 0,5.")
p("O ponto de partida é a planilha de projeto do professor [1], que traz o dimensionamento do "
  "capacitor de barramento, do transformador e do filtro de saída, o projeto das duas malhas "
  "de controle e três ensaios simulados no PSIM com a rede em 176 V. Este artigo confere "
  "todos esses cálculos e desenvolve o que a planilha não traz: a análise qualitativa do "
  "Forward de duas chaves, com etapas de operação e formas de onda; os esforços nos diodos do "
  "retificador e nos semicondutores do conversor, com a escolha de componentes comerciais; o "
  "circuito de controle com o UC3525A e a sua lista de componentes; e a repetição dos ensaios "
  "também com a rede em 264 V. As simulações foram feitas no PLECS [10], e não no PSIM, e os "
  "resultados são comparados com os do professor.")
p("As Seções II e III reúnem as especificações da bateria e da rede. A Seção IV trata do "
  "retificador, a Seção V do Forward de duas chaves e a Seção VI do controle. A Seção VII "
  "apresenta os resultados de simulação e a Seção VIII, as conclusões.")

# =====================================================================
h1("Especificações Básicas da Bateria Estacionária")
p("O projeto é feito para a maior bateria da faixa, de 150 Ah, em um banco de 24 V formado por "
  "doze elementos. A tensão mínima adotada é de 20 V, o que corresponde a 1,67 V por elemento "
  "com a bateria descarregada, e a máxima é de 27 V, ou 2,25 V por elemento, que é a tensão de "
  "flutuação recomendada pelos fabricantes [3]. A corrente de recarga é de um décimo da "
  "capacidade, I_rec = 0,1·150 = 15 A, e a potência máxima entregue à bateria é o produto dessa "
  "corrente pela tensão máxima, P_bat = 27·15 = 405 W.")
p("O regime de carga é o usual para baterias reguladas a válvula [4]: corrente constante "
  "enquanto a tensão está abaixo do valor regulado e, a partir daí, tensão constante, com a "
  "corrente caindo naturalmente. Para baterias menores basta reduzir a referência de corrente. "
  "Como 2,5 V correspondem a 15 A, a sensibilidade é de 6 A/V, e uma bateria de 7 Ah, que pede "
  "0,7 A, é atendida com V_refi = 0,117 V.")

# =====================================================================
h1("Dados da Rede Elétrica")
p("A alimentação é a rede monofásica de 220 V e 60 Hz, com tolerância de 20 % para mais e para "
  "menos, isto é, de 176 V a 264 V eficazes. Os picos correspondentes, de 248,9 V e 373,4 V, "
  "definem os extremos da tensão do barramento CC. O limite inferior é ainda reduzido pela "
  "ondulação do capacitor de filtro, e por isso o conversor é projetado para operar de 225 V a "
  "373 V. A Tabela I resume as especificações.")
tab("Especificações do carregador",
    [["Grandeza", "Valor"],
     ["Capacidade da bateria", "150 Ah (faixa de 7 a 150 Ah)"],
     ["Tensão da bateria", "20 V a 27 V"],
     ["Corrente de recarga", "15 A (0 a 15 A por V_refi)"],
     ["Potência máxima na bateria", "405 W"],
     ["Tensão da rede", "220 V (176 V a 264 V), 60 Hz"],
     ["Barramento CC", "225 V a 373 V"],
     ["Frequência de comutação", "50 kHz"],
     ["Razão cíclica máxima", "0,4"],
     ["Ondulação de corrente em L_o", "3 A (20 %)"],
     ["Ondulação de tensão em C_o", "0,27 V (1 %)"]],
    [0.50, 0.50])

# =====================================================================
h1("Projeto do Retificador a Diodos com Filtro Capacitivo")
h2("Topologia e formas de onda")
p("O retificador é a ponte completa da Fig. %d. No semiciclo positivo conduzem os diodos D1 e "
  "D4 e, no negativo, D3 e D2. Os diodos só entram em condução quando a tensão da rede, em "
  "módulo, supera a do capacitor C1, o que acontece durante um intervalo curto em torno do "
  "pico da senoide. Nesse intervalo o capacitor é recarregado até o valor de pico e, no "
  "restante do semiciclo, alimenta sozinho a carga, com a tensão caindo quase linearmente. A "
  "Fig. %d mostra as formas de onda usadas no dimensionamento, nas quais o pulso de corrente "
  "dos diodos é aproximado por um retângulo de amplitude I_chg e duração angular θ [5]."
  % (N["ret-topologia"], N["ret-formas"]))
fig("ret-topologia", "Retificador monofásico em ponte completa com filtro capacitivo [1].")
fig("ret-formas", "Formas de onda básicas do retificador: tensão no capacitor, correntes nos "
    "diodos e corrente no capacitor, com o pulso de carga aproximado por um retângulo "
    "(adaptado de [1]).")

h2("Capacitor de filtro")
p("O pior caso é a rede em 176 V. A tensão máxima no capacitor é o pico da rede, "
  "V_C1max = 248,9 V, e admite-se uma ondulação de 10 % desse valor, ΔV_C1 = 24,89 V, o que "
  "leva a V_C1min = 224,0 V. O ângulo de condução dos diodos é o intervalo entre o instante em "
  "que a senoide alcança V_C1min e o seu pico:")
eq(r"\theta = \frac{\pi}{2} - \mathrm{arcsen}\left(\frac{V_{C1min}}{V_{C1max}}\right)", "1")
p("O resultado é θ = 0,451 rad, ou 1,196 ms. O capacitor é obtido igualando a energia que ele "
  "cede à carga, durante a fração do semiciclo em que os diodos estão bloqueados, à variação da "
  "sua energia armazenada:")
eq(r"C_1 = \frac{P_{ret}\,(\pi - \theta)}{\pi f_r\,(V_{C1max}^2 - V_{C1min}^2)}", "2")
p("Com rendimento estimado de 90 % para os estágios seguintes, a potência na saída do "
  "retificador é P_ret = 405/0,9 = 450 W, e (2) fornece C_1 = 545,7 µF. A carga equivalente "
  "drena I_oeq = P_ret/V_C1med = 1,903 A, com V_C1med = 236,5 V. Como toda a carga reposta em "
  "um semiciclo passa pelos diodos durante θ, a amplitude do pulso retangular e a corrente "
  "eficaz no capacitor valem")
eq(r"I_{chg} = \frac{\pi\,I_{oeq}}{\theta}", "3")
eq(r"I_{C1ef} = \sqrt{\frac{(I_{chg} - I_{oeq})^2\,\theta + I_{oeq}^2\,(\pi - \theta)}{\pi}}", "4")
p("o que dá I_chg = 13,26 A e I_C1ef = 4,65 A. Todos esses valores coincidem com os da "
  "planilha [1]. A corrente eficaz, e não a capacitância, é o que define o componente: no "
  "catálogo da Fig. %d, o capacitor de 470 µF e 450 V suporta 4,25 A a 60 °C e 3,20 A a 85 °C, "
  "valores insuficientes para um único componente. Adotam-se, por isso, dois capacitores TDK "
  "B43658 de 470 µF em paralelo, C_1 = 940 µF, que juntos suportam 8,5 A a 60 °C [11]."
  % N["ds-c1"])
fig("ds-c1", "Trecho do catálogo do capacitor do barramento, TDK B43658 de 450 V. Foram "
    "adotados dois capacitores de 470 µF em paralelo [1], [11].")
p("A capacitância adotada é 72 % maior que a calculada, e convém refazer as contas com ela. "
  "Resolvendo (1) e (2) para C_1 = 940 µF obtém-se ondulação de 14,7 V, ou 5,9 %, ângulo de "
  "condução menor e, por consequência, pulso de corrente mais alto. A Tabela II reúne os "
  "resultados para as duas tensões extremas da rede.")

h2("Diodos retificadores")
p("A planilha não dimensiona os diodos da ponte. No modelo de pulso retangular, cada diodo "
  "conduz um pulso por ciclo da rede, de modo que as suas correntes média e eficaz são")
eq(r"I_{Dmed} = \frac{I_{chg}\,\theta}{2\pi}, \qquad I_{Def} = I_{chg}\sqrt{\frac{\theta}{2\pi}}", "5")
p("e a tensão reversa máxima é o pico da rede em 264 V, 373,4 V. Com C_1 = 940 µF e a rede em "
  "176 V resultam 0,93 A médios e 3,97 A eficazes por diodo. Escolheu-se a ponte Vishay GBU8J, "
  "de 600 V e 8 A, cuja tabela de valores máximos aparece na Fig. %d(a) [12]. A folga de tensão "
  "é de 1,6 vez, e a corrente de surto admissível, de 200 A, cobre com sobra o pulso repetitivo. "
  "A corrente de energização do capacitor descarregado não foi tratada aqui e, numa montagem "
  "real, exige um limitador em série." % N["ds-semicondutores"])

h2("Fator de potência")
p("A corrente da rede é formada por dois pulsos por ciclo, um positivo e um negativo. O seu "
  "valor eficaz e o fator de potência seguem do mesmo modelo:")
eq(r"I_{ief} = I_{chg}\sqrt{\frac{\theta}{\pi}}, \qquad \mathrm{FP} = \frac{P_{ret}}{V_{ief}\,I_{ief}}", "6")
p("O fator de potência previsto é de 0,455 em 176 V e de 0,379 em 264 V. Ele piora com o "
  "aumento da tensão da rede, e também com o aumento do capacitor, porque nos dois casos o "
  "intervalo de condução encolhe e a mesma potência passa a ser transferida em pulsos mais "
  "estreitos e mais altos. Esse é o ponto negativo apontado na introdução: a corrente é rica "
  "em harmônicas e o valor eficaz drenado da rede é mais que o dobro do necessário. A correção "
  "exigiria um estágio pré-regulador, tipicamente um conversor Boost com controle da corrente "
  "de entrada, entre a ponte e o capacitor.")
tab("Retificador com filtro capacitivo: modelo de pulso retangular",
    [["Grandeza", "176 V, 545,7 µF (planilha)", "176 V, 940 µF", "264 V, 940 µF"],
     ["ΔV_C1 (V)", "24,89", "14,70", "10,03"],
     ["V_C1min (V)", "224,0", "234,2", "363,3"],
     ["θ (rad)", "0,451", "0,345", "0,232"],
     ["Tempo de condução (ms)", "1,196", "0,916", "0,616"],
     ["I_chg (A)", "13,26", "16,94", "16,52"],
     ["I_C1ef (A)", "4,65", "5,30", "4,32"],
     ["I_Dmed (A)", "0,95", "0,93", "0,61"],
     ["I_Def (A)", "3,55", "3,97", "3,18"],
     ["I_ief (A)", "5,02", "5,62", "4,49"],
     ["Fator de potência", "0,509", "0,455", "0,379"]],
    [0.34, 0.26, 0.20, 0.20])

# =====================================================================
h1("Projeto do Conversor Forward de Duas Chaves")
h2("Topologia e etapas de operação")
p("A Fig. %d mostra a topologia. O primário do transformador fica entre duas chaves, S1 ligada "
  "ao positivo do barramento e S2 ao negativo, comandadas pelo mesmo sinal. Dois diodos, D1 e "
  "D2, ligam em cruz os terminais do primário ao barramento. No secundário, D3 retifica e D4 "
  "faz a roda livre do indutor de filtro, como em um conversor Buck. O funcionamento em "
  "condução contínua tem as três etapas da Fig. %d, e as formas de onda idealizadas estão na "
  "Fig. %d [6], [7]." % (N["fwd-topologia"], N["fwd-etapas"], N["fwd-formas"]))
fig("fwd-topologia", "Topologia do conversor Forward de duas chaves.")
p("Na primeira etapa, de duração DT_s, as duas chaves conduzem e o primário recebe a tensão "
  "V_i. O secundário, com a mesma polaridade, polariza D3 diretamente e aplica nV_i à entrada "
  "do filtro, de modo que a corrente de L_o cresce. A corrente das chaves é a do indutor "
  "refletida ao primário, somada à corrente magnetizante, que cresce linearmente a partir de "
  "zero.")
p("Na segunda etapa as chaves são bloqueadas. A corrente magnetizante não pode ser "
  "interrompida e passa a circular por D1 e D2, que ligam o primário à fonte com a polaridade "
  "invertida. O transformador fica submetido a −V_i, a corrente magnetizante decresce e a "
  "energia armazenada no núcleo é devolvida à fonte. É essa etapa que distingue a topologia: "
  "a tensão sobre cada chave fica grampeada em V_i pelos diodos, sem enrolamento terciário e "
  "sem circuito de grampeamento dissipativo, e a energia da dispersão também é recuperada. No "
  "secundário, D3 bloqueia e D4 assume a corrente de L_o.")
p("A terceira etapa começa quando a corrente magnetizante se anula. O primário fica sem "
  "corrente, a tensão sobre o transformador é nula e cada chave suporta metade de V_i. A roda "
  "livre continua até o início do período seguinte. Como a tensão de desmagnetização tem o "
  "mesmo módulo da de magnetização, a segunda etapa dura o mesmo que a primeira, e as áreas A+ "
  "e A− da Fig. %d são iguais. Para que haja tempo de desmagnetizar o núcleo antes de um novo "
  "ciclo, a razão cíclica precisa ser menor que 0,5." % N["fwd-formas"])
fig("fwd-etapas", "Etapas de operação do Forward de duas chaves em condução contínua: (a) "
    "transferência de energia; (b) desmagnetização; (c) roda livre. O caminho da corrente está "
    "em traço grosso e as setas indicam o seu sentido.")
fig("fwd-formas", "Formas de onda teóricas do Forward de duas chaves: comando, tensão no "
    "primário, corrente magnetizante, corrente e tensão nas chaves, corrente em L_o e tensão na "
    "entrada do filtro.")

h2("Relação de transformação e razão cíclica")
p("Visto do secundário, o conversor é um Buck alimentado por nV_i. O ganho estático e a "
  "relação de espiras, definida para a razão cíclica máxima na tensão mínima de entrada, são")
eq(r"\frac{V_o}{V_i} = nD, \qquad n = \frac{N_s}{N_p} = \frac{V_o}{V_{imin}\,D_{max}}", "7")
p("Com V_o = 27 V, V_imin = 225 V e D_max = 0,4, resulta n = 0,3, e a simulação usa 100 "
  "espiras no primário e 30 no secundário. Na tensão máxima de entrada, de 373 V, a razão "
  "cíclica cai para D_min = 0,241.")

h2("Filtro de saída")
p("O indutor é calculado para a ondulação de 3 A na pior condição, que em um conversor da "
  "família Buck é a de maior tensão de entrada [5]:")
eq(r"L_o = \frac{n V_{imax}\,D_{min}\,(1 - D_{min})}{f_s\,\Delta I_{Lo}}", "8")
p("O resultado é L_o = 136,6 µH. A capacitância necessária para limitar a ondulação de tensão "
  "a 0,27 V, considerando apenas a carga e a descarga do capacitor, é")
eq(r"C_o = \frac{n V_{imax}\,D_{min}\,(1 - D_{min})}{8 L_o f_s^2\,\Delta V_c}", "9")
p("isto é, 27,8 µF. Na prática quem determina a ondulação é a resistência série equivalente, "
  "que não poderia passar de R_se = ΔV_c/ΔI_Lo = 0,09 Ω. Não existe capacitor eletrolítico de "
  "47 µF com resistência tão baixa, e a planilha adota o EPCOS B41821 de 2200 µF e 50 V, com "
  "R_se = 0,11 Ω, cuja tabela está na Fig. %d [11]. A capacitância fica oitenta vezes maior "
  "que a calculada e a ondulação prevista sobe para 0,11·3 = 0,33 V, pouco acima da "
  "especificada. A corrente eficaz admissível, de 1,98 A, é mais que o dobro da ondulação "
  "eficaz do indutor. O capacitor grande tem um efeito importante na dinâmica: leva a "
  "ressonância do filtro para 290 Hz e o zero da resistência série para 658 Hz, bem abaixo "
  "das frequências de cruzamento das malhas. A carga nominal é representada por "
  "R_o = 27/15 = 1,8 Ω." % N["ds-co"])
fig("ds-co", "Trecho do catálogo do capacitor de saída, EPCOS/TDK B41821 de 50 V. O de "
    "2200 µF tem resistência série máxima de 0,11 Ω e corrente eficaz admissível de 1,98 A "
    "[11].")

h2("Esforços nos semicondutores e componentes comerciais")
p("A planilha também não traz os esforços nos semicondutores. Eles foram calculados para os "
  "extremos do barramento, incluindo as quedas que existem no circuito simulado: 0,7 V em "
  "cada diodo e 10 mΩ no sensor de corrente. Com essas quedas, a razão cíclica real é")
eq(r"D = \frac{V_{bat} + 2V_F + R_{sh} I_o}{n\,V_{C1}}", "10")
p("em que as duas quedas V_F são a do diodo que estiver conduzindo no filtro e a do diodo de "
  "bloqueio em série com a bateria. As correntes eficaz e de pico em cada chave são")
eq(r"I_{Sef} = n I_o \sqrt{D}, \qquad I_{Spk} = n\left(I_o + \frac{\Delta I_{Lo}}{2}\right) + I_{Lmpk}", "11")
p("e a corrente magnetizante de pico vale")
eq(r"I_{Lmpk} = \frac{V_i\,D}{L_m f_s}", "12")
p("Como o produto V_iD é praticamente constante, a corrente magnetizante de pico não depende "
  "da tensão de entrada: com a indutância magnetizante de 20 mH usada na simulação, ela é de "
  "95 mA. As correntes médias nos diodos do secundário são I_oD no retificador e I_o(1 − D) no "
  "de roda livre, e a tensão reversa em ambos é nV_i. A Tabela III apresenta os esforços e os "
  "componentes escolhidos, cujas tabelas de valores máximos estão na Fig. %d [12]."
  % N["ds-semicondutores"])
tab("Esforços nos semicondutores do Forward e componentes escolhidos",
    [["Componente", "Tensão máxima", "Corrente (pior caso)", "Componente comercial"],
     ["Chaves S1 e S2", "373 V", "5,1 A de pico; 2,9 A eficazes", "IRFP460 (500 V; 20 A; 0,27 Ω)"],
     ["Diodos D1 e D2 (desmagnetização)", "373 V", "95 mA de pico", "UF4005 (600 V; 1 A; 75 ns)"],
     ["Diodo D3 (retificador)", "112 V", "6,3 A médios; 9,8 A eficazes",
      "VS-MUR3020WT (200 V; 2 × 15 A; 35 ns)"],
     ["Diodo D4 (roda livre)", "112 V", "11,2 A médios; 12,9 A eficazes", "VS-MUR3020WT"],
     ["Capacitor C_o", "27 V", "0,90 A eficazes", "B41821, 2200 µF, 50 V (1,98 A)"],
     ["Sensor R_sh", "0,15 V", "15 A (2,25 W)", "10 mΩ, 5 W"]],
    [0.25, 0.14, 0.27, 0.34], span=2)
fig("ds-semicondutores", "Tabelas de valores máximos dos semicondutores escolhidos: (a) ponte "
    "retificadora GBU8J; (b) MOSFET IRFP460; (c) diodo ultrarrápido UF4005; (d) diodo duplo "
    "ultrarrápido VS-MUR3020WT [12].", span=2)
p("As chaves ficam submetidas a 373 V no pior caso, e o IRFP460, de 500 V, opera com 75 % da "
  "sua tensão nominal. Isso só é aceitável porque, nessa topologia, a tensão é grampeada pelos "
  "diodos de desmagnetização. No Forward de uma chave, com terciário de mesma relação de "
  "espiras, a chave teria de suportar 746 V. As perdas de condução são pequenas, da ordem de "
  "2,9²·0,27 = 2,3 W por chave a 25 °C. Os diodos de desmagnetização conduzem apenas a "
  "corrente magnetizante e podem ser pequenos, mas precisam ser rápidos e suportar a tensão "
  "do barramento. No secundário, os dois diodos de um único VS-MUR3020WT atendem ao "
  "retificador e à roda livre, com folga de 1,8 vez na tensão. O dimensionamento físico do "
  "transformador e do indutor está fora do escopo da planilha e não foi feito.")

# =====================================================================
h1("Projeto do Circuito de Controle")
h2("Estrutura do controle")
p("O diagrama de blocos do controle é o da Fig. %d. Há duas malhas, uma de corrente e uma de "
  "tensão, que não atuam ao mesmo tempo. Cada uma tem o seu compensador, e as duas saídas são "
  "combinadas de modo que prevaleça a menor: o compensador de tensão chega ao modulador por um "
  "resistor, e o de corrente, por um diodo que só conduz quando a sua saída está abaixo da "
  "tensão de controle. Enquanto a bateria está descarregada, a malha de tensão pede mais "
  "corrente do que o permitido, o seu compensador satura e a malha de corrente mantém a "
  "recarga no valor fixado por V_refi. Quando a tensão alcança 27 V, a malha de tensão reduz "
  "a tensão de controle, o diodo bloqueia, o compensador de corrente satura e o carregador "
  "passa a regular a tensão." % N["ctrl-blocos"])
fig("ctrl-blocos", "Diagrama de blocos do controle do carregador: malha de corrente e malha "
    "de tensão [1].")
p("O modulador compara a tensão de controle com a portadora do UC3525A, cuja amplitude a "
  "planilha toma como V_D = 2,1 V, o que dá o ganho F_m = 1/V_D = 0,476. A tensão de saída é "
  "medida por um divisor resistivo, com ganho H_v = V_refv/V_o = 2,5/27 = 0,0926. A corrente do "
  "indutor é medida por um resistor de 10 mΩ no retorno do secundário, seguido de um "
  "amplificador diferencial de ganho 16,67, de modo que H_i = 0,1667 V/A e 15 A correspondem a "
  "2,5 V.")

h2("Compensador tipo 2 e método do fator K")
p("Os dois compensadores são do tipo 2, um integrador com um zero e um polo, montado com um "
  "amplificador operacional como na Fig. %d. A sua função de transferência é"
  % N["ctrl-tipo2"])
eq(r"C(s) = \frac{1 + s R_2 C_1}{s R_1\,(C_1 + C_2 + s R_2 C_1 C_2)}", "13")
fig("ctrl-tipo2", "Compensador tipo 2 (PI com filtro) [1].")
p("O projeto segue o método do fator K [8], [9]. Escolhida a frequência de cruzamento f_c, "
  "lê-se no diagrama de Bode do laço sem compensador o ganho e a fase P nessa frequência. O "
  "avanço de fase que o compensador deve fornecer para a margem de fase desejada e o fator K "
  "correspondente são")
eq(r"\alpha = \mathrm{MF} - P - 90^\circ, \qquad K = \tan\left(\frac{\alpha + 90^\circ}{2}\right)", "14")
p("O zero é posto em f_c/K e o polo em Kf_c, de modo que o avanço máximo ocorra exatamente no "
  "cruzamento. Sendo G o ganho que o compensador deve ter em f_c e fixado R_1, os demais "
  "componentes são")
eq(r"C_2 = \frac{1}{2\pi f_c\,G K R_1}, \qquad C_1 = C_2\,(K^2 - 1)", "15")
eq(r"R_2 = \frac{K}{2\pi f_c\,C_1}", "16")

h2("Malha de tensão")
p("A planta da malha de tensão é a função de transferência entre a razão cíclica e a tensão "
  "de saída do Buck equivalente, com a resistência série do capacitor:")
eq(r"G_v(s) = \frac{n V_i\,(1 + s C_o R_{se})}{\Delta(s)}", "17")
eq(r"\Delta(s) = s^2 L_o C_o\left(1 + \frac{R_{se}}{R_o}\right) + s\left(\frac{L_o}{R_o} + C_o R_{se}\right) + 1", "18")
p("O projeto é feito na tensão máxima de entrada, em que o ganho é maior. Para o cruzamento "
  "em f_cv = f_s/10 = 5 kHz, o laço sem compensador G_vF_mH_v tem ganho de −18,38 dB e fase de "
  "−95,67°. Com margem de fase de 60°, o avanço necessário é de 65,67° e (14) dá K = 4,64, "
  "que a planilha arredonda para 4,7. O zero fica em 1,06 kHz e o polo em 23,5 kHz. O "
  "compensador precisa de ganho G = 8,295 e, com R_1 = 10 kΩ, resultam C_2 = 81,65 pF, "
  "C_1 = 1,722 nF e R_2 = 86,88 kΩ. A Fig. %d mostra o laço antes e depois da compensação. A "
  "margem de fase obtida é de 60,3° e a de ganho é infinita, como na planilha."
  % N["ctrl-bode-tensao"])
fig("ctrl-bode-tensao", "Diagrama de Bode da malha de tensão com os valores da planilha: laço "
    "sem compensador, compensador e laço compensado. O cruzamento ocorre em 5 kHz, com margem "
    "de fase de 60,3°.")

h2("Malha de corrente")
p("A planta da malha de corrente relaciona a razão cíclica com a corrente do indutor e tem o "
  "mesmo denominador:")
eq(r"G_i(s) = \frac{n V_i}{R_o}\,\frac{1 + s C_o\,(R_o + R_{se})}{\Delta(s)}", "19")
p("A frequência de cruzamento escolhida é f_ci = f_s/4 = 12,5 kHz, maior que a da malha de "
  "tensão. Nessa frequência a fase do laço sem compensador é de −89,45°, o avanço necessário é "
  "de 59,45° e K = 3,66, arredondado para 3,7, com zero em 3,38 kHz e polo em 46,25 kHz. A "
  "planilha obtém C_2 = 165,8 pF, C_1 = 2,104 nF e R_2 = 22,39 kΩ.")
p("A conferência revelou uma divergência nesse ponto. O ganho usado na planilha, de 6,34 dB, "
  "é o do laço sem compensador em f_cv = 5 kHz, e não em f_ci. Em 12,5 kHz o laço tem −1,64 dB, "
  "de modo que o compensador deveria ter ganho de 1,21, e não de 2,08. Com os valores da "
  "planilha, o laço da Fig. %d cruza 0 dB em 20,0 kHz, e não em 12,5 kHz, com margem de fase de "
  "57,4°. A margem continua boa, porque o avanço do compensador é largo, mas o cruzamento "
  "passa a 40 %% da frequência de comutação, região em que o modelo médio já não é confiável. "
  "Lendo o ganho na frequência correta, o projeto daria R_2 = 13,05 kΩ, C_1 = 3,57 nF e "
  "C_2 = 288 pF." % N["ctrl-bode-corrente"])
fig("ctrl-bode-corrente", "Diagrama de Bode da malha de corrente com os valores da planilha. "
    "O laço compensado cruza 0 dB em 20,0 kHz, com margem de fase de 57,4°.")

h2("Componentes comerciais e laços resultantes")
p("O circuito de simulação do professor usa valores comerciais próximos dos calculados, "
  "reunidos na Tabela IV. Ele difere da planilha em mais dois pontos: a portadora tem 2,4 V "
  "de pico a pico, de 0,8 V a 3,2 V, e não 2,1 V, e os sensores têm ganhos ligeiramente "
  "diferentes dos ideais, H_v = 10,2/110,2 = 0,09256 e H_i = 0,167 V/A. Com isso a tensão "
  "regulada é de 27,01 V e o limite de corrente, de 14,97 A. As frequências de cruzamento e as "
  "margens de fase resultantes, calculadas com esses valores para as duas tensões da rede, "
  "também estão na tabela. O ganho dos laços é proporcional à tensão do barramento, e por "
  "isso os cruzamentos são mais baixos em 176 V. Em todos os casos a margem de fase fica "
  "entre 48° e 60°.")
tab("Compensadores: valores calculados, valores comerciais e laços resultantes",
    [["Grandeza", "Malha de tensão", "Malha de corrente"],
     ["Frequência de cruzamento de projeto", "5 kHz", "12,5 kHz"],
     ["Fator K (exato / adotado)", "4,64 / 4,7", "3,66 / 3,7"],
     ["R_1", "10 kΩ", "10 kΩ"],
     ["R_2 (calculado / comercial)", "86,88 kΩ / 82 kΩ", "22,39 kΩ / 18 kΩ"],
     ["C_1 (calculado / comercial)", "1,722 nF / 1,5 nF", "2,104 nF / 2,7 nF"],
     ["C_2 (calculado / comercial)", "81,65 pF / 100 pF", "165,8 pF / 220 pF"],
     ["Cruzamento e margem de fase, 176 V", "2,9 kHz; 48°", "10,0 kHz; 60°"],
     ["Cruzamento e margem de fase, 264 V", "4,2 kHz; 55°", "14,6 kHz; 59°"]],
    [0.44, 0.28, 0.28])

h2("Circuito com o UC3525A e lista de componentes")
p("O circuito de referência para a implementação é o da Fig. %d, do material da disciplina "
  "[2]: um UC3525A, quatro amplificadores operacionais e um acionador isolado. Ele foi "
  "projetado para 20 kHz e razão cíclica de até 100 %%, e precisa de quatro adaptações para "
  "este carregador. A primeira é a frequência do oscilador, dada por [9]" % N["ctrl-uc3525"])
eq(r"f_s = \frac{1}{C_T\,(0{,}7 R_T + 3 R_D)}", "20")
p("que, mantidos R_T = 10 kΩ e R_D = 100 Ω, pede C_T = 2,7 nF para 50,7 kHz. A segunda é o "
  "limite de razão cíclica. No circuito original as duas saídas do integrado são somadas por "
  "diodos para alcançar 100 %. Aqui deve-se usar uma única saída, o que limita a razão cíclica "
  "a menos de 50 % e garante a desmagnetização do transformador. A terceira é o acionamento: "
  "as duas chaves têm fontes em potenciais diferentes e cada uma precisa do seu acionador "
  "isolado, comandados pelo mesmo sinal. A quarta são os sensores e os compensadores, com os "
  "valores da Tabela IV. A Tabela V lista os componentes, com os designadores do circuito de "
  "simulação quando existem.")
fig("ctrl-uc3525", "Circuito de controle de referência com o UC3525A, malha de tensão e malha "
    "de corrente, projetado para 20 kHz [2]. As adaptações para este carregador estão no "
    "texto.", span=2)
tab("Lista de componentes do circuito de controle",
    [["Referência", "Componente ou valor", "Função"],
     ["U1", "UC3525A", "Modulador PWM, oscilador e referência de 5,1 V"],
     ["U2 a U5", "4 amplificadores operacionais (LM741 em [2])",
      "Seguidor, amplificador diferencial e dois compensadores"],
     ["U6, U7", "2 × FOD3184", "Acionadores isolados, um por chave"],
     ["R_T, C_T, R_D", "10 kΩ; 2,7 nF; 100 Ω", "Oscilador de 50,7 kHz"],
     ["C_SS", "1 µF", "Partida suave (pino 8)"],
     ["R11, R12", "100 kΩ; 10,2 kΩ", "Divisor da tensão de saída (27,01 V)"],
     ["R13, R14, C5, C6", "10 kΩ; 82 kΩ; 1,5 nF; 100 pF", "Compensador de tensão"],
     ["R_sh", "10 mΩ; 5 W", "Sensor de corrente"],
     ["R2, R3, R4, R5", "10 kΩ; 10 kΩ; 167 kΩ; 167 kΩ", "Amplificador diferencial (ganho de 16,7)"],
     ["R16, R18, C7, C8", "10 kΩ; 18 kΩ; 2,7 nF; 220 pF", "Compensador de corrente"],
     ["R7, D6", "1 kΩ; 1N5819", "Combinação das malhas (prevalece a menor)"],
     ["2 potenciômetros", "10 kΩ", "Ajuste de V_refv e de V_refi (0 a 2,5 V)"],
     ["Por chave", "22 Ω; 15 Ω; 2 × 1N4148; 2,2 kΩ; 1N4744", "Circuito de gatilho"],
     ["Desacoplamento", "100 nF e 100 µF, 35 V", "Alimentações de 15 V"]],
    [0.20, 0.42, 0.38], span=2)

# =====================================================================
h1("Resultados de Simulação")
h2("Modelo de simulação")
_txt_circ = ("O circuito simulado pelo professor no PSIM é o da Fig. %d. " % N["sim-circuito-psim"])
if TEM_PLECS:
    _txt_circ += ("Ele foi reproduzido no PLECS com os mesmos designadores e valores, e o "
                  "resultado é o esquemático da Fig. %d. " % N["sim-circuito-plecs"])
else:
    _txt_circ += "Ele foi reproduzido no PLECS com os mesmos designadores e valores. "
p(_txt_circ + "O modelo contém o retificador, o Forward de duas chaves e o controle analógico "
  "completo, com amplificadores operacionais de saída limitada entre 0 e 5 V. A carga é "
  "trocada conforme o ensaio: resistores para o degrau de carga, um resistor de 1 mΩ para o "
  "curto-circuito, ou o modelo da bateria, formado por uma fonte de 20 V em série com um "
  "capacitor e com a resistência interna de 10 mΩ.")
p("Quatro ajustes foram necessários ou convenientes na passagem para o PLECS. O PLECS trabalha "
  "com chaves ideais e passo variável, e não aceita que um capacitor fique em paralelo com uma "
  "fonte por meio de chaves ideais: a indutância de dispersão do transformador do PSIM, de "
  "0,1 µH por enrolamento, foi mantida, referida ao secundário, e os diodos da ponte receberam "
  "5 mΩ de resistência de condução. O valor do diodo Zener que limita a tensão de controle não "
  "é legível no esquemático, e adotou-se 1,95 V, o que limita a razão cíclica a 0,48. O "
  "capacitor do barramento é o adotado na planilha, de 940 µF, embora o esquemático mostre "
  "470 µF. O capacitor do modelo da bateria é de 0,8 F, valor que reproduz o tempo de recarga "
  "da figura do professor, embora o esquemático mostre 400 mF. Cada ensaio foi feito com a "
  "rede em 176 V e em 264 V.")
fig("sim-circuito-psim", "Circuito de simulação do carregador usado pelo professor no PSIM, "
    "com o estágio de potência, o compensador de corrente, o compensador de tensão e o "
    "modulador PWM [1].", span=2)
if TEM_PLECS:
    fig("sim-circuito-plecs", "Modelo do carregador no PLECS, com os mesmos designadores do "
        "circuito do professor.", span=2)

h2("Regime permanente")
p("A Fig. %d mostra a tensão do barramento e as correntes da rede e de um diodo da ponte com "
  "carga nominal, e a Tabela VI compara os valores medidos com os calculados. A ondulação do "
  "barramento, de 14,0 V em 176 V e de 9,6 V em 264 V, concorda com a prevista pelo modelo "
  "para 940 µF, e a diferença se deve à potência de entrada, que na simulação é de 430 W e "
  "não de 450 W. O fator de potência medido é de 0,405 em 176 V e de 0,335 em 264 V, com "
  "distorção harmônica total da corrente de 220 %% e de 278 %%. O fator de deslocamento é "
  "praticamente unitário, e o baixo fator de potência se deve inteiramente à distorção."
  % N["sim-retificador"])
p("Dois valores medidos se afastam do modelo, e os dois por causa da forma do pulso. A "
  "corrente de pico é de 30,8 A, contra 16,9 A do pulso retangular: o pulso real começa no "
  "valor máximo e decresce até zero, e a sua amplitude é quase o dobro da de um retângulo de "
  "mesma área. A corrente eficaz no capacitor é de 6,17 A, contra 5,30 A, porque ao pulso mais "
  "agudo se soma a corrente pulsada de 50 kHz drenada pelo Forward. O valor medido supera o "
  "que um único capacitor de 470 µF suporta, o que confirma a decisão de usar dois em "
  "paralelo.")
fig("sim-retificador", "Retificador em regime permanente com carga nominal, no PLECS: tensão "
    "no capacitor C1 (traço cheio) e módulo da tensão da rede (tracejado), corrente da rede e "
    "corrente em um diodo da ponte, com a rede em 176 V (azul) e em 264 V (vermelho).")
p("As formas de onda do Forward, na Fig. %d, coincidem com as teóricas da Fig. %d. A tensão "
  "sobre a chave fica grampeada na do barramento durante a desmagnetização e cai à metade na "
  "terceira etapa, a desmagnetização dura o mesmo que a condução, e a corrente magnetizante "
  "chega a 95 mA nas duas tensões. A corrente nas chaves vai de 4,1 A a 5,0 A. A razão cíclica "
  "média é de 0,396 em 176 V e de 0,259 em 264 V, e (10) prevê 0,395 e 0,259 com as tensões "
  "médias de barramento medidas. O rendimento da simulação é de 94 %%. Como as chaves são "
  "ideais, ele reflete apenas as quedas nos diodos e nos resistores, e o valor real será "
  "menor." % (N["sim-forward"], N["fwd-formas"]))
fig("sim-forward", "Formas de onda do Forward de duas chaves em regime permanente, no PLECS: "
    "comando, tensão no primário, corrente magnetizante, corrente e tensão na chave inferior e "
    "corrente em L_o, com a rede em 176 V (azul) e em 264 V (vermelho).")
tab("Regime permanente com carga nominal: valores calculados e simulados no PLECS",
    [["Grandeza", "Calculado, 176 V", "PLECS, 176 V", "Calculado, 264 V", "PLECS, 264 V"],
     ["Ondulação em C1 (V)", "14,70", "13,99", "10,03", "9,55"],
     ["Tempo de condução dos diodos (ms)", "0,916", "0,946", "0,616", "0,629"],
     ["Corrente eficaz da rede (A)", "5,62", "6,03", "4,49", "4,85"],
     ["Corrente de pico da rede (A)", "16,9", "30,8", "16,5", "30,0"],
     ["Fator de potência", "0,455", "0,405", "0,379", "0,335"],
     ["Corrente eficaz em C1 (A)", "5,30", "6,17", "4,32", "5,11"],
     ["Corrente média em um diodo da ponte (A)", "0,93", "0,89", "0,61", "0,58"],
     ["Razão cíclica", "0,395", "0,396", "0,259", "0,259"],
     ["Ondulação de corrente em L_o (A)", "2,53", "2,57", "3,10", "3,11"],
     ["Tensão máxima nas chaves (V)", "248,9", "248,2", "373,4", "372,6"],
     ["Corrente de pico nas chaves (A)", "4,97", "4,97", "5,06", "5,05"],
     ["Corrente eficaz nas chaves (A)", "2,83", "2,86", "2,29", "2,32"],
     ["Corrente média em D3 / D4 (A)", "5,93 / 9,07", "5,93 / 9,04", "3,89 / 11,11",
      "3,89 / 11,09"],
     ["Tensão reversa em D3 e D4 (V)", "74,7", "74,0", "112,0", "111,3"],
     ["Ondulação da tensão de saída (V)", "0,28", "0,27", "0,34", "0,32"]],
    [0.36, 0.16, 0.16, 0.16, 0.16], span=2,
    note="Calculado com C_1 = 940 µF, P_ret = 450 W e, no Forward, com a tensão média de "
         "barramento medida (240,8 V e 367,3 V). D3 e D4 são os diodos retificador e de roda "
         "livre da Fig. %d, que no circuito de simulação se chamam D2 e D1." % N["fwd-topologia"])
p("A Fig. %d atende à sugestão de observar cinco períodos da portadora e da moduladora. A "
  "tensão de controle não é constante: carrega uma ondulação de 0,44 V em 176 V e de 0,48 V em "
  "264 V, que é a ondulação da corrente do indutor amplificada pelo compensador de corrente. "
  "Mesmo assim há um único cruzamento por rampa da portadora, os pulsos são todos iguais e a "
  "forma de onda se repete a cada período, sem sinal de oscilação sub-harmônica. A inclinação "
  "máxima da ondulação, de 0,07 V/µs em 176 V e de 0,11 V/µs em 264 V, é menor que a da "
  "portadora, de 0,24 V/µs."
  % N["sim-portadora"])
fig("sim-portadora", "Cinco períodos da portadora triangular e da moduladora, com o sinal PWM "
    "resultante (faixa verde), em regime permanente com carga nominal.")

h2("Degrau de carga")
p("No primeiro ensaio a carga alterna entre 100 %% e 20 %% a cada 167 ms: um resistor de 9 Ω "
  "fica sempre ligado e outro, de 2,25 Ω, é comutado a 3 Hz. A Fig. %d compara o resultado do "
  "PLECS, nas duas tensões da rede, com o do professor. A tensão permanece em 27 V, com um "
  "afundamento breve a cada aplicação de carga e uma elevação a cada retirada, e a corrente do "
  "indutor alterna entre 15 A e 3 A. O vale de tensão é de 25,62 V nas duas tensões da rede, "
  "contra cerca de 25,7 V na figura do professor. Ele corresponde ao degrau de corrente no "
  "capacitor multiplicado pela resistência série, 12·0,11 = 1,32 V, o que mostra que nos "
  "primeiros instantes quem sustenta a saída é o capacitor. A corrente do indutor ultrapassa "
  "o valor final e chega a 22,6 A em 176 V e a 20,8 A em 264 V, contra cerca de 23 A do "
  "professor." % N["sim-degrau"])
fig("sim-degrau", "Degrau de carga de 100 % para 20 % e vice-versa, tensão de saída e "
    "corrente no indutor de filtro: (a) PLECS, rede em 176 V; (b) PLECS, rede em 264 V; (c) "
    "resultado do professor no PSIM, rede em 176 V [1].", span=2)
p("O detalhe dos transitórios está nas Figs. %d e %d. Na aplicação de carga a tensão se "
  "recupera em menos de 0,4 ms. Na retirada, porém, o pico chega a 29,3 V em 176 V e a 29,5 V "
  "em 264 V, um volt acima dos cerca de 28,3 V da figura do professor, e a tensão demora "
  "1,6 ms para voltar à faixa de 1 %%." % (N["sim-degrau-100-20"], N["sim-degrau-20-100"]))
p("A causa é uma coincidência do projeto. Com a carga de 1,8 Ω, a malha de tensão regula "
  "27,01 V e pede 15,006 A, mas o limite da malha de corrente é de 14,97 A. As duas malhas "
  "disputam o comando, e a de corrente acaba assumindo: o compensador de tensão satura em 5 V "
  "cerca de 3 ms depois de cada aplicação de carga em 176 V, e cerca de 30 ms depois em 264 V, "
  "e a tensão cai para 26,95 V. Quando a carga é "
  "retirada, a malha de corrente continua impondo 15 A a uma carga que só consome 3 A, e os "
  "12 A excedentes carregam o capacitor de saída até que o compensador de tensão saia da "
  "saturação e retome o comando.")
fig("sim-degrau-100-20", "Retirada de carga, de 100 % para 20 %, no PLECS: tensão de saída, "
    "corrente no indutor e saída do compensador de tensão. Em azul e em vermelho, o projeto "
    "nominal com a rede em 176 V e em 264 V; em verde, 176 V com folga de 4 % no limite de "
    "corrente.")
p("Para confirmar a explicação, o ensaio foi repetido com V_refi = 2,6 V, o que eleva o limite "
  "de corrente para 15,6 A, uma folga de 4 %%. O resultado é a curva verde das Figs. %d e %d. "
  "Com a folga, o "
  "compensador de tensão permanece ativo com a carga nominal, em 1,76 V, o pico na retirada de "
  "carga cai para 28,4 V, valor que é só o degrau na resistência série do capacitor, e a "
  "tensão volta à faixa de 1 %% em menos de 0,1 ms. O resultado passa a coincidir com o do "
  "professor, o que indica que na simulação dele a malha de tensão estava no comando com a "
  "carga nominal." % (N["sim-degrau-100-20"], N["sim-degrau-20-100"]))
fig("sim-degrau-20-100", "Aplicação de carga, de 20 % para 100 %, no PLECS, com as mesmas "
    "grandezas e cores da figura anterior. No projeto nominal em 176 V, o compensador de tensão "
    "satura em 5 V cerca de 3 ms depois do degrau.")

h2("Curto-circuito na saída")
p("No segundo ensaio a carga nominal fica ligada e a saída é curto-circuitada por 1 mΩ durante "
  "metade de cada período de 333 ms. A Fig. %d mostra que, em curto, a tensão cai a zero e a "
  "corrente do indutor é mantida em 14,97 A pela malha de corrente, com ondulação muito menor "
  "porque a razão cíclica fica pequena. O resultado é igual nas duas tensões da rede e "
  "coincide com o do professor." % N["sim-curto"])
fig("sim-curto", "Curto-circuito na saída, tensão de saída e corrente no indutor de filtro: "
    "(a) PLECS, rede em 176 V; (b) PLECS, rede em 264 V; (c) resultado do professor no PSIM, "
    "rede em 176 V [1].", span=2)
p("O detalhe da Fig. %d mostra os dois transitórios. Na aplicação do curto, a corrente do "
  "indutor sobe a 17,6 A e volta a 15 A em 0,4 ms, tempo que a malha de corrente leva para "
  "reduzir a razão cíclica. Na retirada, a tensão se restabelece com a corrente limitada em "
  "15 A e alcança 90 %% do valor final em 9,4 ms, crescimento exponencial com a constante de "
  "tempo R_oC_o = 4 ms. Um efeito não aparece na corrente do indutor: no instante do curto, o "
  "capacitor de saída se descarrega pelo diodo de bloqueio D15, com pico de 256 A, limitado "
  "apenas pela resistência série do capacitor. Esse diodo precisa ser escolhido pela corrente "
  "de surto, e não só pelos 15 A de regime." % N["sim-curto-detalhe"])
fig("sim-curto-detalhe", "Detalhe da aplicação e da retirada do curto-circuito no PLECS, nas "
    "duas tensões da rede.")

h2("Recarga da bateria")
p("No terceiro ensaio os resistores são retirados e a carga é o modelo da bateria, inicialmente "
  "com 20 V. A Fig. %d mostra as duas fases da recarga. Na primeira, a malha de corrente mantém "
  "14,97 A e a tensão cresce linearmente, a 18,7 V/s, que é a corrente dividida pela "
  "capacitância do modelo. Em 0,378 s a tensão nos terminais alcança o valor regulado, a malha "
  "de tensão assume e a corrente cai a zero em cerca de 20 ms, com a tensão mantida em "
  "27,02 V. A transição ocorre no mesmo instante que na figura do professor, cerca de 0,375 s, "
  "e não depende da tensão da rede." % N["sim-recarga"])
fig("sim-recarga", "Recarga da bateria, tensão nos terminais e corrente de recarga: (a) PLECS, "
    "rede em 176 V; (b) PLECS, rede em 264 V; (c) resultado do professor no PSIM, rede em "
    "176 V [1].", span=2)

h2("Comparação com os resultados do professor")
tab("Resultados dos ensaios: PLECS e professor (PSIM)",
    [["Grandeza", "PLECS, 176 V", "PLECS, 264 V", "Professor, 176 V"],
     ["Tensão de saída com 20 % de carga (V)", "27,01", "27,01", "≈ 27"],
     ["Tensão de saída com 100 % de carga (V)", "26,95", "26,95", "≈ 27"],
     ["Vale de tensão, 20 % → 100 % (V)", "25,62", "25,62", "≈ 25,7"],
     ["Pico de tensão, 100 % → 20 % (V)", "29,33", "29,47", "≈ 28,3"],
     ["Idem, com folga de 4 % no limite de corrente (V)", "28,42", "28,44", "—"],
     ["Pico de corrente em L_o, 20 % → 100 % (A)", "22,6", "20,8", "≈ 23"],
     ["Corrente em L_o durante o curto-circuito (A)", "14,97", "14,97", "≈ 15"],
     ["Pico de corrente em L_o ao aplicar o curto (A)", "17,6", "17,5", "≈ 18"],
     ["Retorno da tensão após o curto, 90 % (ms)", "9,4", "9,4", "≈ 10"],
     ["Corrente de recarga (A)", "14,97", "14,97", "≈ 15"],
     ["Fim da recarga em corrente constante (s)", "0,378", "0,379", "≈ 0,375"],
     ["Tensão final da bateria (V)", "27,02", "27,02", "≈ 27"]],
    [0.46, 0.18, 0.18, 0.18], span=2)
p("A Tabela VII reúne os valores característicos dos três ensaios. Os do professor foram lidos "
  "nas figuras da planilha e são aproximados. A concordância é boa em todos os pontos, com a "
  "única diferença já discutida, do pico na retirada de carga. Os resultados em 264 V, que a "
  "planilha não traz, praticamente repetem os de 176 V: o controle compensa a variação da "
  "tensão de entrada, e o que muda é a razão cíclica, a ondulação de corrente e o ganho dos "
  "laços. Na partida, que as figuras do professor não mostram, a corrente do indutor chega a "
  "25 A antes de a malha de corrente atuar, porque o circuito simulado não tem partida suave. "
  "O UC3525A tem esse recurso, e ele está previsto na Tabela V.")

# =====================================================================
h1("Conclusão")
p("O carregador de 15 A baseado no Forward de duas chaves foi projetado, conferido e simulado. "
  "Todos os valores da planilha do professor foram reproduzidos, e as simulações no PLECS, com "
  "o controle analógico completo, repetem os três ensaios feitos por ele no PSIM: a tensão é "
  "regulada em 27 V diante de degraus de carga entre 20 % e 100 %, a corrente é limitada em "
  "15 A mesmo com a saída em curto-circuito, e a recarga da bateria ocorre em corrente "
  "constante seguida de tensão constante. Os mesmos resultados foram obtidos com a rede em "
  "264 V, o que mostra que o projeto atende a toda a faixa de tensão de entrada.")
p("A topologia cumpre o que se esperava dela. A tensão sobre as chaves ficou grampeada na do "
  "barramento, 373 V no pior caso, o que permite usar MOSFETs de 500 V, e a desmagnetização do "
  "transformador se completa em um tempo igual ao de condução. Os esforços calculados "
  "concordam com os simulados dentro de 2 %, e os componentes comerciais escolhidos operam com "
  "folga. O retificador com filtro capacitivo confirmou a sua limitação: o fator de potência "
  "medido foi de 0,41 em 176 V e de 0,34 em 264 V, com corrente de pico de 30 A, quase o dobro "
  "da prevista pelo modelo de pulso retangular. A corrente eficaz no capacitor do barramento, "
  "de 6,2 A, justifica os dois capacitores em paralelo.")
p("A conferência e a simulação trouxeram três observações que a planilha não registra. O ganho "
  "do compensador de corrente foi calculado com o valor do laço em 5 kHz, e não em 12,5 kHz, "
  "de modo que o cruzamento real fica acima do pretendido, embora com margem de fase "
  "adequada. A carga nominal coincide com o limite de corrente, o que deixa o carregador na "
  "fronteira entre as duas malhas e, por causa da saturação do compensador de tensão, eleva "
  "em um volt o pico de tensão na retirada de carga. Uma folga de 4 % no limite resolve o "
  "problema. Por fim, o diodo de bloqueio em série com a bateria sofre um surto de 256 A "
  "quando a saída é curto-circuitada, e deve ser dimensionado por essa corrente.")
p("Como continuação, propõem-se o projeto físico do transformador e do indutor, a inclusão de "
  "partida suave e de um limitador da corrente de energização, e a substituição do retificador "
  "por um estágio com correção do fator de potência, que é a principal deficiência do "
  "carregador como está.")

# =====================================================================
REFS = [
 "R. P. Torrico-Bascopé, Projeto de um Carregador de Baterias de 15 A Baseado no Conversor "
 "Forward de Duas Chaves. Planilha de projeto da disciplina de Eletrônica Industrial, "
 "Universidade Federal do Ceará, Fortaleza, 2026.",
 "R. P. Torrico-Bascopé, Mini-curso de Controle Básico para Conversores Estáticos, Parte IV, "
 "Anexo. Universidade Federal do Ceará, Fortaleza.",
 "Baterias Estacionárias Freedom, Catálogo Técnico.",
 "Y. S. Wong, W. G. Hurley e W. H. Wölfle, “Charge regimes for valve-regulated lead-acid "
 "batteries: Performance overview inclusive of temperature compensation,” Journal of Power "
 "Sources, 2008.",
 "M. H. Rashid, Power Electronics: Devices, Circuits, and Applications, 4th ed. Harlow: "
 "Pearson, 2014.",
 "I. Barbi, Projetos de Fontes Chaveadas, 3. ed. Florianópolis: Edição do Autor, 2015.",
 "R. W. Erickson e D. Maksimović, Fundamentals of Power Electronics, 3rd ed. Cham: Springer, "
 "2020.",
 "H. D. Venable, “The K factor: A new mathematical tool for stability analysis and synthesis,” "
 "em Proc. Powercon 10, 1983.",
 "Texas Instruments, UC1525A, UC2525A, UC3525A Regulating Pulse Width Modulators. Folha de "
 "dados.",
 "Plexim GmbH, PLECS User Manual, versão 5.0. Zurique, 2025.",
 "TDK Electronics, Aluminum Electrolytic Capacitors: séries B43658 e B41821. Folhas de dados.",
 "Vishay Intertechnology, folhas de dados GBU8A a GBU8M, IRFP460, UF4001 a UF4007 e "
 "VS-MUR3020WT-N3.",
 "R. P. Torrico-Bascopé, Modelado y Control de Convertidores Estáticos. Notas de aula, "
 "Universidade Federal do Ceará, Fortaleza.",
]
