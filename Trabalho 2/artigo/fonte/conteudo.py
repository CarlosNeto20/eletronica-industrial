# -*- coding: utf-8 -*-
"""Conteúdo do artigo IEEE do Trabalho 2. Blocos: h1, h2, p, eq, fig, tab, bul.

Fonte do texto: memorial em desenvolvimento/ (docs 01 a 09) e resultados do
PLECS em resultados PLECS/metricas_degraus.md. Figuras em artigo/figuras,
montadas por montar_figuras.py. A numeração das figuras segue a ordem das
chamadas fig() abaixo; a das equações é explícita.
"""

TITULO = ("Análise de Conversores CC-CC Isolados e Comparação\n"
          "com os Conversores Equivalentes Não Isolados")

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
    "Este trabalho analisa quatro conversores CC-CC isolados, o Forward de uma chave, a ponte "
    "completa, o push-pull alimentado em corrente e o Flyback de uma chave, e verifica por "
    "simulação que cada um deles é dinamicamente equivalente a um conversor básico não isolado, "
    "referido ao secundário do transformador. Para cada topologia são apresentadas a análise "
    "qualitativa, com formas de onda teóricas e etapas de operação, e um exemplo de projeto. "
    "Mostra-se que os equivalentes seguem três regras gerais: a fonte é refletida pela relação "
    "de espiras, uma indutância do primário pelo seu quadrado, e as topologias que excitam o "
    "transformador nos dois semiciclos têm equivalentes que comutam no dobro da frequência, com "
    "razão cíclica efetiva 2D na ponte completa e 2D − 1 no push-pull. Os oito circuitos foram "
    "simulados no PLECS com degraus de carga de 20 % para 100 % e vice-versa. Em todos os casos "
    "as tensões e correntes de saída do conversor isolado e do equivalente coincidem, com erro "
    "RMS máximo de 0,09 % e erro instantâneo máximo de 0,78 %, este último na ponte completa e "
    "atribuído à corrente magnetizante do transformador. No Flyback, os modos de condução "
    "contínua e descontínua produzem dinâmicas qualitativamente diferentes, de segunda e de "
    "primeira ordem, mas a equivalência com o Buck-Boost é exata em ambos. Os resultados "
    "justificam o uso das funções de transferência dos conversores básicos no projeto do "
    "controle dos conversores isolados."
)

PALAVRAS = ("conversores CC-CC isolados, Forward, ponte completa, push-pull alimentado em "
            "corrente, Flyback, conversor equivalente, transformador de alta frequência, "
            "degrau de carga, PLECS")

C = []
def h1(t): C.append(("h1", t))
def h2(t): C.append(("h2", t))
def p(t): C.append(("p", t))
def eq(t, n): C.append(("eq", t, n))
def fig(f, cap, span=1): C.append(("fig", f, cap, span))
def tab(cap, rows, widths, span=1, note=None):
    C.append(("tab", cap, rows, widths, span, note))
def bul(items): C.append(("bul", items))


# =====================================================================
h1("Introdução")
p("Quando a entrada de um conversor está ligada à rede ou a um barramento perigoso e a saída é "
  "acessível ao usuário, a norma exige isolação galvânica, e a solução é intercalar um "
  "transformador de alta frequência no conversor. O transformador, porém, faz mais do que "
  "isolar. Ele ajusta o nível de tensão pela relação de espiras, o que permite que um conversor "
  "de 400 V para 54 V opere com razão cíclica de 0,4, e não de 0,135 como um Buck, e em "
  "algumas topologias ele também armazena energia. Por isso os conversores isolados dominam as "
  "fontes chaveadas acima de algumas dezenas de watts.")
p("Todo conversor isolado deriva de um conversor básico. Olhando da carga para trás, o filtro de "
  "saída não sabe que existe um transformador: tudo o que ele enxerga é a forma de onda aplicada "
  "na sua entrada. Se um conversor básico, sem transformador, produzir a mesma forma de onda "
  "nesse ponto, a saída dos dois se comporta de modo idêntico, em regime e em transitório. Esse é "
  "o conversor equivalente referido ao secundário. A importância prática da equivalência é que "
  "ela permite projetar o controle do conversor isolado com as funções de transferência, já "
  "conhecidas, do conversor básico [2], [5], [9].")
p("O objetivo deste trabalho é verificar essa equivalência para quatro topologias: o Forward de "
  "uma chave e a ponte completa, derivados do Buck; o push-pull alimentado em corrente, derivado "
  "do Boost; e o Flyback de uma chave, derivado do Buck-Boost. Para cada uma são apresentadas a "
  "análise qualitativa e um exemplo de projeto, e o conversor isolado e o seu equivalente são "
  "simulados lado a lado, submetidos aos mesmos degraus de carga de 20 % para 100 % e de 100 % "
  "para 20 %. As simulações, originalmente propostas no PSIM [1], foram feitas no PLECS [8].")
p("A Seção II reúne o que é comum às quatro topologias: o modelo do transformador, a condição "
  "de desmagnetização, as regras de construção do equivalente e a metodologia de simulação. As "
  "Seções III a VI tratam de cada conversor, a Seção VII sintetiza os resultados e a Seção VIII "
  "apresenta as conclusões.")

# =====================================================================
h1("Conversores Isolados e seus Equivalentes")
h2("Modelo do transformador")
p("A relação de transformação é definida como secundário sobre primário, a = N_s/N_p, de modo que "
  "a tensão do secundário vale a vezes a do primário e a corrente do primário vale a vezes a do "
  "secundário. O modelo adotado é o transformador ideal acrescido da indutância magnetizante L_m "
  "em paralelo com o primário. A corrente do primário passa a ter duas parcelas, a refletida da "
  "carga e a magnetizante:")
eq(r"i_{pri} = a\,i_{sec} + i_{Lm}, \qquad L_m\frac{di_{Lm}}{dt} = v_{pri}", "1")
p("No Forward, na ponte completa e no push-pull a indutância magnetizante é um efeito parasita, "
  "dimensionada para que a corrente magnetizante seja de 1 % a 2 % da corrente de pico do "
  "primário. No Flyback é o contrário: L_m é o próprio elemento armazenador de energia. A "
  "indutância de dispersão foi desprezada, porque não altera a equivalência que se quer "
  "verificar e, com chaves ideais, apenas acrescentaria picos de tensão sem significado físico.")
h2("Desmagnetização do núcleo")
p("Em regime permanente o fluxo precisa voltar ao mesmo valor ao fim de cada período, sob pena de "
  "crescer ciclo a ciclo até a saturação. Como a tensão no enrolamento é proporcional à derivada "
  "do fluxo, isso exige tensão média nula sobre o primário, isto é, áreas iguais de tensão-tempo "
  "positiva e negativa, as áreas A+ e A− das formas de onda deste artigo. Cada topologia cumpre "
  "essa condição de um modo diferente, e isso é o que mais as distingue. O Forward precisa de um "
  "enrolamento terciário que devolve a energia magnetizante à fonte, o que limita a razão cíclica "
  "a 0,5 quando o terciário tem o mesmo número de espiras do primário. A ponte completa e o "
  "push-pull aplicam tensões opostas ao primário em semiciclos alternados e se desmagnetizam "
  "naturalmente. No Flyback a energia de L_m é entregue à própria carga.")
h2("Construção do conversor equivalente")
p("Para levar um elemento do primário ao secundário basta conservar a tensão por espira e a "
  "potência. Uma fonte de tensão V_i torna-se aV_i, uma corrente i torna-se i/a e uma indutância "
  "L torna-se a²L, já que a energia armazenada se conserva. A essas regras soma-se uma quarta, "
  "própria das topologias simétricas. Na ponte completa e no push-pull o retificador de onda "
  "completa entrega ao filtro dois pulsos por período de comutação, e o equivalente precisa "
  "comutar no dobro da frequência, com razão cíclica igual à fração de cada meio período ocupada "
  "pelo pulso [2]–[4]. Aplicando essas regras obtêm-se os equivalentes da Tabela I.")
tab("Conversores equivalentes referidos ao secundário",
    [["Conversor isolado", "Equivalente", "V_eq", "L_eq", "D_eq", "f_eq", "Ganho estático"],
     ["Forward", "Buck", "nV_i", "L_o", "D", "f_s", "V_o/V_i = nD"],
     ["Ponte completa", "Buck", "aV_i", "L_o", "2D", "2f_s", "V_o/V_i = 2aD"],
     ["Push-pull (corrente)", "Boost", "aV_i", "a²L_i", "2D − 1", "2f_s", "V_o/V_i = a/[2(1 − D)]"],
     ["Flyback (MCC)", "Buck-Boost", "aV_i", "a²L_m", "D", "f_s", "V_o/V_i = aD/(1 − D)"]],
    [0.17, 0.13, 0.09, 0.10, 0.09, 0.08, 0.34], span=2)
p("O equivalente reproduz a tensão e a corrente de saída, mas não representa o que existe apenas "
  "no primário: a corrente magnetizante (exceto no Flyback, em que ela é a própria corrente do "
  "indutor), as restrições de razão cíclica impostas pelo reset do núcleo, os esforços de tensão "
  "nas chaves e os efeitos da dispersão. Ele serve, portanto, à modelagem dinâmica e ao projeto "
  "do controle, e não ao dimensionamento dos semicondutores e do transformador.")
h2("Metodologia de simulação")
p("Para cada conversor, o circuito isolado e o equivalente foram montados no mesmo modelo PLECS, "
  "com os mesmos componentes de saída e com o degrau de carga comandado por um único gerador, o "
  "que garante que os dois sofrem a perturbação no mesmo instante. A carga é formada por um "
  "resistor de 5R_o, que sozinho consome 20 % da potência nominal, em paralelo com um resistor de "
  "1,25R_o comutado por uma onda quadrada; com os dois ligados a carga vale R_o. Os conversores "
  "operam em malha aberta, com razão cíclica fixa, porque o objetivo é comparar as plantas e um "
  "controlador mascararia as diferenças entre elas. Chaves e diodos são ideais e as resistências "
  "série dos capacitores são mantidas, por fazerem parte do projeto.")
p("As grandezas de saída são filtradas por uma média móvel de um período de comutação, que "
  "remove a ondulação e deixa apenas a dinâmica média. A equivalência é aceita quando os valores "
  "de regime dos dois circuitos coincidem entre si e com a previsão analítica, quando o erro RMS "
  "entre eles é menor que 1 % e quando extremos e tempos de acomodação diferem em menos de 2 %. "
  "A primeira condição é indispensável, porque dois circuitos podem concordar entre si e estar "
  "ambos errados.")

# =====================================================================
h1("Conversor Forward de Uma Chave")
h2("Análise qualitativa")
fig("fwd-topologia", "Topologia do conversor Forward de uma chave.")
p("O Forward, na Fig. 1, é composto pela fonte V_i, por um transformador de três enrolamentos "
  "(primário, secundário e terciário de desmagnetização), pela chave S_1, pelo diodo de "
  "transferência D_1, pelo diodo de roda livre D_2 e pelo filtro L_o–C_o que alimenta a carga R_o. "
  "Os pontos do primário e do secundário estão do mesmo lado, e a energia é transferida à carga "
  "enquanto a chave conduz, o que caracteriza o Forward.")
fig("fwd-formas", "Formas de onda teóricas do conversor Forward.")
fig("fwd-etapas", "Etapas de operação do conversor Forward: (a) transferência de energia; (b) "
    "desmagnetização do transformador e roda livre; (c) roda livre.")
p("As formas de onda da Fig. 2 e as etapas da Fig. 3 mostram três intervalos por período. Com S_1 "
  "conduzindo, D_1 aplica nV_i ao filtro e a corrente magnetizante cresce. Quando S_1 abre, a "
  "corrente do indutor passa a circular por D_2, e a corrente magnetizante é devolvida à fonte "
  "pelo terciário e por D_t; nesse intervalo S_1 suporta 2V_i. Terminada a desmagnetização, só D_2 "
  "conduz e S_1 suporta V_i. O balanço de tensão-tempo no primário limita a razão cíclica a")
eq(r"D \le \frac{1}{1 + N_t/N_p} = 0{,}5", "2")
h2("Projeto")
p("O exemplo converte 200 V em 54 V com 500 W, 20 kHz e D = 0,4, com ondulações de 1,5 A no "
  "indutor e 0,27 V no capacitor [1]. Do ganho estático V_o = nDV_i resulta n = 0,675, e o filtro "
  "é dimensionado como o de um Buck alimentado por nV_i:")
eq(r"L_o = \frac{(nV_i - V_o)\,D}{\Delta I_{Lo}\,f_s} = 1{,}08\ \mathrm{mH}, \qquad "
   r"C_o = \frac{\Delta I_{Lo}}{8\,f_s\,\Delta V_{Co}} = 34{,}72\ \mu\mathrm{F}", "3")
p("A resistência série máxima do capacitor vale 0,18 Ω, a carga nominal 5,832 Ω e a indutância "
  "magnetizante 13 mH. A chave suporta 400 V e conduz pico de 7,1 A, dos quais 0,31 A são "
  "corrente magnetizante.")
h2("Resultados de simulação")
fig("fwd-circuito", "Circuitos simulados no PLECS: Forward isolado (acima) e Buck equivalente (abaixo). À direita, os geradores de comando e do degrau de carga e as medições enviadas ao Scope e ao arquivo de dados.", 2)
fig("fwd-degraus", "Tensão e corrente de saída do Forward isolado (vermelho) e do Buck "
    "equivalente (azul) nos degraus de carga de (a) 20 % para 100 % e (b) 100 % para 20 %.")
p("Os circuitos simulados estão na Fig. 4. A simulação usou o transformador de 100:68:100 espiras do enunciado (n = 0,68) e, para o Buck "
  "equivalente, a mesma tensão refletida de 136 V. As respostas da Fig. 5 são idênticas. A tensão "
  "de regime, 54,4 V, é exatamente 0,68·200·0,4 e resulta do arredondamento das espiras. O vale "
  "de 31,8 V e o pico de 89,6 V concordam com os 31 V e 90 V obtidos no PSIM [1]. A oscilação tem "
  "o período da ressonância do filtro, cerca de 1,2 ms, e é bem amortecida no degrau de subida de "
  "carga porque a resistência série do capacitor é grande diante da impedância característica "
  "do filtro, de 5,6 Ω.")

# =====================================================================
h1("Conversor Ponte Completa")
h2("Análise qualitativa")
p("O conversor ponte completa é o isolado derivado do Buck mais usado em potências elevadas, de "
  "1 kW a dezenas de quilowatts, em fontes de telecomunicações, carregadores de veículos "
  "elétricos e fontes de soldagem. Ele excita o transformador nos dois sentidos com a tensão "
  "plena da fonte, usando quatro chaves que suportam apenas V_i, sem enrolamento de "
  "desmagnetização e aproveitando os dois quadrantes do laço B-H do núcleo. Em contrapartida, "
  "exige comando isolado para as chaves superiores e é sensível a desequilíbrios de "
  "tensão-tempo entre os semiciclos, que levam o núcleo à saturação.")
fig("fb-topologia", "Topologia do conversor ponte completa.")
p("A topologia, na Fig. 6, é formada pela fonte V_i, por dois braços de chaves (S_1–S_4 e S_3–S_2) "
  "cujos pontos médios alimentam o primário, pelo transformador de relação a, pelo retificador em "
  "ponte D_1–D_4 e pelo filtro L_o–C_o. As chaves são comandadas em diagonal: S_1 e S_2 conduzem "
  "durante DT e aplicam +V_i ao primário; meio período depois, S_3 e S_4 aplicam −V_i. Para que as "
  "chaves de um braço nunca conduzam juntas, D < 0,5.")
fig("fb-formas", "Formas de onda teóricas do conversor ponte completa.")
p("Nas formas de onda da Fig. 7, a entrada do filtro recebe aV_i durante cada pulso e zero no "
  "restante, e a corrente no indutor é triangular com frequência 2f_s. A corrente magnetizante é "
  "um trapézio simétrico em torno de zero, o que evidencia a desmagnetização natural. Na roda "
  "livre os quatro diodos conduzem, cada par com metade da corrente de carga, e cada chave "
  "bloqueada fica com V_i/2. A igualdade das áreas de tensão no indutor dá o ganho estático")
eq(r"(aV_i - V_o)\,DT = V_o\,\frac{(1-2D)\,T}{2} \;\Rightarrow\; \frac{V_o}{V_i} = 2aD", "4")
fig("fb-etapas", "Etapas de operação do conversor ponte completa, com o caminho da corrente em "
    "destaque: (a) e (c) transferência de energia; (b) e (d) roda livre.", 2)
p("A Fig. 8 mostra as quatro etapas de um período. Na primeira, S_1 e S_2 conduzem, D_1 e D_2 levam "
  "a corrente do indutor à carga e o indutor recebe aV_i − V_o. Na segunda, as chaves são "
  "bloqueadas, a corrente do indutor circula pelos quatro diodos, o secundário fica em curto e o "
  "indutor recebe −V_o. A terceira é simétrica à primeira, com S_3, S_4, D_3 e D_4, e excita o "
  "núcleo no sentido oposto. A quarta repete a segunda. Como o filtro vê um pulso de amplitude "
  "aV_i e duração DT a cada meio período, o equivalente é um Buck alimentado por aV_i, comutando "
  "em 2f_s com razão cíclica 2D.")
h2("Projeto")
p("O exemplo converte 400 V em 54 V com 5 kW, 20 kHz e D = 0,4 por diagonal [1]. Do ganho, "
  "a = 0,169 e I_o = 92,6 A. Na roda livre o indutor recebe −V_o durante (1 − 2D)T/2, e o "
  "capacitor filtra uma corrente triangular de frequência 2f_s:")
eq(r"L_o = \frac{V_o\,(0{,}5 - D)}{f_s\,\Delta I_{Lo}} = 14{,}58\ \mu\mathrm{H}, \qquad "
   r"C_o = \frac{(1-2D)\,V_o}{32\,L_o f_s^{2}\,\Delta V_{Co}} = 214{,}4\ \mu\mathrm{F}", "5")
p("A resistência série máxima vale 14,6 mΩ e a carga nominal 0,583 Ω. O critério de 2 % para a "
  "corrente magnetizante, aplicado com a relação a = 0,169, leva a L_m = 10,2 mH; o enunciado "
  "obtém 2,55 mH por reutilizar a relação do Forward, e o valor de 2,6 mH foi mantido na "
  "simulação para permitir a comparação com o material de referência. As chaves suportam 400 V e "
  "conduzem pico de 18,7 A; os diodos suportam 67,5 V e conduzem pico de 102 A.")
h2("Resultados de simulação")
fig("fb-circuito", "Circuitos simulados no PLECS: ponte completa isolada (acima) e Buck equivalente de 67,5 V e 40 kHz (abaixo).", 2)
fig("fb-degraus", "Tensão e corrente de saída da ponte completa isolada (vermelho) e do Buck "
    "equivalente de 67,5 V e 40 kHz (azul) nos degraus de carga de (a) 20 % para 100 % e "
    "(b) 100 % para 20 %.")
p("Os circuitos simulados estão na Fig. 9, e as curvas da Fig. 10 se sobrepõem. O vale de 40,8 V e o pico de 70,7 V reproduzem os valores de "
  "40 V e 71 V do material de referência [1], e a oscilação tem o período da ressonância do filtro, "
  "0,35 ms, pouco amortecida por operar em malha aberta. A única diferença perceptível, de 0,09 % "
  "RMS e 0,78 % no pior instante, ocorre no degrau para 20 % e vem da corrente magnetizante do "
  "circuito isolado, que circula pelo retificador e não existe no equivalente.")

# =====================================================================
h1("Conversor Push-Pull Alimentado em Corrente")
h2("Análise qualitativa")
p("O push-pull alimentado em corrente é o isolado derivado do Boost. O transformador é alimentado "
  "através de um indutor de entrada, o que o torna adequado a fontes de baixa tensão e corrente "
  "elevada que precisam ser elevadas, como bancos de baterias, células a combustível e painéis "
  "fotovoltaicos. A corrente de entrada é contínua, as duas chaves têm a fonte no mesmo "
  "potencial e, por ser alimentado em corrente, o conversor não sofre o desequilíbrio de fluxo do "
  "push-pull alimentado em tensão [6]. Em contrapartida, as chaves precisam conduzir com sobreposição, "
  "com D > 0,5, e suportam o dobro da tensão refletida.")
fig("pp-topologia", "Topologia do conversor push-pull alimentado em corrente.")
p("Na Fig. 11, o indutor L_b liga a fonte à derivação central do primário, cujas metades têm N_p "
  "espiras cada; S_1 e S_2 ligam as extremidades do primário ao negativo da fonte; o secundário, de "
  "N_s espiras, alimenta um retificador em ponte e um filtro apenas capacitivo. As chaves recebem "
  "pulsos de razão cíclica D > 0,5 defasados de meio período, e em cada período há dois "
  "intervalos de sobreposição e dois em que só uma chave conduz.")
fig("pp-formas", "Formas de onda teóricas do conversor push-pull alimentado em corrente.")
p("Nas sobreposições o primário fica em curto, porque as duas metades se cancelam, e o indutor "
  "recebe V_i; com uma só chave, recebe V_i − V_o/a. A igualdade das áreas na Fig. 12 dá")
eq(r"V_i\,\frac{(2D-1)\,T}{2} = \left(\frac{V_o}{a} - V_i\right)(1-D)\,T "
   r"\;\Rightarrow\; \frac{V_o}{V_i} = \frac{a}{2(1-D)}", "6")
p("A chave conduz metade da corrente de entrada nas sobreposições e toda ela quando conduz "
  "sozinha, e bloqueada suporta 2V_o/a. Nas sobreposições os quatro diodos ficam bloqueados, cada "
  "par com V_o/2, e o capacitor alimenta sozinho a carga.")
fig("pp-etapas", "Etapas de operação do conversor push-pull alimentado em corrente, com o "
    "caminho da corrente em destaque: (a) e (c) armazenamento de energia no indutor; (b) e (d) "
    "transferência de energia.", 2)
p("A Fig. 13 mostra as quatro etapas. Na primeira e na terceira as duas chaves conduzem, a "
  "corrente do indutor se divide entre as metades do primário, a tensão do transformador é nula "
  "e o indutor armazena energia. Na segunda só S_1 conduz: toda a corrente passa pela metade "
  "inferior, o transformador é excitado e D_1 e D_2 entregam a energia à saída. A quarta é "
  "simétrica, com S_2, D_3 e D_4, e desmagnetiza o núcleo. As sobreposições fazem o papel da chave "
  "fechada de um Boost e ocorrem duas vezes por período; referido ao secundário, o equivalente é "
  "um Boost alimentado por aV_i, com indutor a²L_b, frequência 2f_s e razão cíclica 2D − 1.")
h2("Projeto")
p("O exemplo eleva 54 V para 400 V com 1 kW, 20 kHz e D = 0,7 [1]. Do ganho, a = 4,444, com "
  "I_i = 18,5 A e I_o = 2,5 A. Na sobreposição, que dura (2D − 1)T/2, o indutor recebe V_i e o "
  "capacitor fornece sozinho a corrente de carga:")
eq(r"L_i = \frac{(2D-1)\,V_i}{2 f_s\,\Delta I_{Li}} = 145{,}9\ \mu\mathrm{H}, \qquad "
   r"C_o = \frac{(2D-1)\,I_o}{2 f_s\,\Delta V_{Co}} = 6{,}25\ \mu\mathrm{F}", "7")
p("A resistência série máxima, calculada com o pico da corrente do secundário, vale 0,873 Ω, e a "
  "carga nominal 160 Ω. As chaves suportam 180 V, 3,3 vezes a tensão de entrada, e conduzem pico "
  "de 20,4 A; os diodos suportam 400 V. O equivalente tem 240 V e indutor de 2,88 mH.")
h2("Resultados de simulação")
fig("pp-circuito", "Circuitos simulados no PLECS: push-pull alimentado em corrente isolado (acima), com o primário de derivação central representado por dois transformadores ideais, e Boost equivalente de 240 V e 40 kHz (abaixo).", 2)
fig("pp-degraus", "Tensão e corrente de saída do push-pull isolado (vermelho) e do Boost "
    "equivalente de 240 V, 2,88 mH e 40 kHz (azul) nos degraus de carga de (a) 20 % para 100 % e "
    "(b) 100 % para 20 %.")
p("Com os circuitos da Fig. 14, as respostas da Fig. 15 também se sobrepõem, com vale de 340,0 V e pico de 466,3 V, contra 338 V "
  "e 465 V no material de referência [1]. A oscilação, de cerca de 710 Hz, é a do par de polos do "
  "Boost, muito mais lenta que a da ponte porque o indutor refletido é grande. A tensão a plena "
  "carga, 398,5 V, é a mesma nos dois circuitos e se deve à perda na resistência série do "
  "capacitor, percorrida pela corrente pulsada do retificador; é uma não idealidade que o "
  "equivalente também reproduz. A diferença máxima, de 0,34 %, novamente vem da corrente "
  "magnetizante.")

# =====================================================================
h1("Conversor Flyback de Uma Chave")
h2("Análise qualitativa")
p("O Flyback é o isolado derivado do Buck-Boost e o mais simples de todos: uma chave, um diodo, um "
  "capacitor e um componente magnético que é ao mesmo tempo transformador e indutor. Domina as "
  "fontes de baixa potência, como carregadores e fontes auxiliares. Os pontos do primário e do "
  "secundário estão em lados opostos, e por isso a energia é primeiro armazenada na indutância "
  "magnetizante, com a chave fechada, e só depois transferida à carga, com a chave aberta. Toda "
  "a energia passa pelo núcleo a cada ciclo, o que limita a potência, e a energia da dispersão "
  "exige um grampeador [7].")
fig("fly-topologia", "Topologia do conversor Flyback de uma chave.")
fig("fly-formas", "Formas de onda teóricas do conversor Flyback em modo de condução "
    "descontínua.")
fig("fly-etapas", "Etapas de operação do conversor Flyback em modo de condução descontínua: "
    "(a) armazenamento de energia; (b) transferência de energia; (c) corrente nula nos "
    "indutores.")
p("A topologia está na Fig. 16, as formas de onda em modo de condução descontínua (MCD) na "
  "Fig. 17 e as etapas na Fig. 18. Com S_1 fechada o primário recebe V_i, a corrente magnetizante "
  "cresce linearmente até V_iDT/L_m e D_1 bloqueia com nV_i + V_o. Com S_1 aberta a corrente "
  "passa ao secundário, a tensão do primário se inverte para −V_o/n e a indutância se descarrega "
  "na saída até zerar. No intervalo restante nenhum enrolamento conduz e o capacitor alimenta a "
  "carga. Em modo de condução contínua (MCC) a terceira etapa desaparece. Referindo L_m e a fonte "
  "ao secundário obtém-se um Buck-Boost, com ganho que depende do modo de condução:")
eq(r"\frac{V_o}{V_i} = n\,\frac{D}{1-D}\ \ \text{(MCC)}, \qquad "
   r"\frac{V_o}{V_i} = D\sqrt{\frac{R_o}{2 L_m f_s}}\ \ \text{(MCD)}", "8")
p("Em MCD o indutor esvazia a cada período e entrega uma energia fixa por ciclo, "
  "independentemente da carga. Em malha aberta a tensão de saída sobe até que a potência na carga "
  "iguale essa energia, e o indutor deixa de ser uma variável de estado: a dinâmica de saída é de "
  "primeira ordem, com constante de tempo próxima de R_oC_o/2. Em MCC reaparece o par de polos "
  "do Buck-Boost.")
h2("Projeto")
p("O exemplo converte 200 V em 54 V com 200 W, 20 kHz e D = 0,4 [1]. A relação de espiras é "
  "calculada no modo crítico, fronteira entre os dois modos, e a indutância crítica decorre de "
  "igualar a energia armazenada por ciclo à potência:")
eq(r"n = \frac{V_o}{V_i}\,\frac{1-D}{D} = 0{,}405, \qquad "
   r"L_{crit} = \frac{V_i^{2} D^{2}}{2 f_s P_i} = 800\ \mu\mathrm{H}", "9")
p("Adota-se L_m = 0,9·L_crit = 720 µH, que garante MCD em toda a faixa de carga. Durante DT o "
  "capacitor fornece sozinho a corrente de carga, o que dá C_o = I_oD/(f_sΔV) = 137,2 µF, com "
  "resistência série de 0,044 Ω. Para a simulação em MCC, L_m é multiplicada por dez, o que "
  "mantém o MCC até cerca de 11 % de carga. Um efeito importante do MCD em malha aberta é que, com "
  "carga leve, a tensão de saída sobe e a tensão refletida sobre a chave chega a 514 V, contra "
  "340 V a plena carga.")
h2("Resultados de simulação")
fig("fly-circuito", "Circuitos simulados no PLECS: Flyback isolado (acima) e Buck-Boost equivalente (abaixo), cuja saída negativa é medida em relação ao terra para ser comparada com a do isolado.", 2)
fig("fly-mcd-degraus", "Tensão e corrente de saída do Flyback isolado (vermelho) e do Buck-Boost "
    "equivalente (azul) em modo de condução descontínua, L_m = 720 µH, nos degraus de carga de "
    "(a) 20 % para 100 % e (b) 100 % para 20 %.")
fig("fly-mcc-degraus", "Tensão e corrente de saída do Flyback isolado (vermelho) e do Buck-Boost "
    "equivalente (azul) em modo de condução contínua, L_m = 7,2 mH, nos degraus de carga de "
    "(a) 20 % para 100 % e (b) 100 % para 20 %.")
p("Os circuitos estão na Fig. 19, com L_m = 720 µH em MCD e 7,2 mH em MCC. Em MCD, na Fig. 20, a tensão de saída depende da carga: 127,1 V a 20 % e 56,8 V a 100 %, contra "
  "127,3 V e 56,9 V previstos pela Eq. (8). A resposta é exponencial, sem sobressinal, com "
  "acomodação em 4,6 ms no degrau de subida de carga e em 15,1 ms no de descida, na proporção das "
  "constantes de tempo R_oC_o/2 de 1,0 ms e 5,0 ms. O degrau de 100 % para 20 % em MCD, ausente "
  "no material de referência, é assim três vezes mais lento que o de subida. Em MCC, na Fig. 21, "
  "a tensão é praticamente independente da carga e o transitório é oscilatório, com vale de "
  "42,6 V e pico de 67,5 V, contra 43 V e 67 V no PSIM [1], na frequência do par de polos do "
  "Buck-Boost, cerca de 240 Hz. Nos dois modos as respostas do isolado e do equivalente são "
  "idênticas, porque no Flyback a corrente magnetizante é a própria corrente do indutor e o "
  "equivalente a representa integralmente.")

# =====================================================================
h1("Síntese dos Resultados")
tab("Comparação entre conversor isolado e equivalente nos degraus de carga",
    [["Conversor", "V_o antes / depois (V)", "Vale de V_o, 20 → 100 % (V)",
      "Pico de V_o, 100 → 20 % (V)", "PSIM [1] (V)", "Erro RMS máx.", "Erro inst. máx."],
     ["Forward", "54,4 / 54,4", "31,8", "89,6", "31 / 90", "0,000 %", "0,000 %"],
     ["Ponte completa", "54,0 / 54,0", "40,8", "70,7", "40 / 71", "0,088 %", "0,78 %"],
     ["Push-pull", "399,7 / 398,5", "340,0", "466,3", "338 / 465", "0,064 %", "0,34 %"],
     ["Flyback MCD", "127,1 / 56,8", "sem sobressinal", "sem sobressinal", "—", "0,000 %", "0,000 %"],
     ["Flyback MCC", "54,0 / 53,9", "42,6", "67,5", "43 / 67", "0,000 %", "0,000 %"]],
    [0.15, 0.14, 0.15, 0.15, 0.13, 0.14, 0.14], span=2,
    note="Valores médios por período de comutação. Os valores de vale e pico são iguais nos dois "
         "circuitos até a primeira casa decimal. Erros: diferença isolado − equivalente em "
         "porcentagem do valor final, nas grandezas V_o e I_o.")
p("A Tabela II reúne os resultados. Os quatro conversores, e o Flyback nos dois modos, cumprem os "
  "três critérios de aceitação com folga. As diferenças se concentram nas topologias em que a "
  "corrente magnetizante circula pelo retificador de saída, a ponte completa e o push-pull, e "
  "desaparecem naquelas em que ela não passa pelo filtro (Forward) ou é a própria corrente do "
  "indutor equivalente (Flyback). Os valores extremos concordam com os do material de referência "
  "com diferenças de 1 V a 2 V, compatíveis com a leitura gráfica.")
p("A comparação entre as topologias mostra também o compromisso que cada uma faz. O Flyback usa "
  "um único semicondutor comandado e nenhum indutor de filtro, mas processa toda a energia no "
  "núcleo. O Forward acrescenta o filtro e o terciário e submete a chave a 2V_i. A ponte completa "
  "usa quatro chaves submetidas apenas a V_i e aproveita o núcleo nos dois sentidos, e por isso "
  "aparece no exemplo de maior potência. O push-pull alimentado em corrente eleva a tensão com "
  "corrente de entrada contínua, ao custo de chaves com o triplo da tensão de entrada.")

# =====================================================================
h1("Conclusões")
p("Foi verificado, por simulação no PLECS, que o Forward de uma chave, a ponte completa, o "
  "push-pull alimentado em corrente e o Flyback de uma chave têm a mesma dinâmica de saída que os "
  "seus conversores equivalentes não isolados, referidos ao secundário, diante de degraus de "
  "carga de 20 % para 100 % e vice-versa. O erro RMS entre as respostas não passou de 0,09 %, e o "
  "erro instantâneo de 0,78 %, ambos atribuídos à corrente magnetizante.")
p("Os equivalentes seguem regras gerais simples: a fonte é refletida pela relação de espiras, as "
  "indutâncias do primário pelo seu quadrado, e as topologias simétricas comutam no dobro da "
  "frequência com razão cíclica efetiva 2D ou 2D − 1. Com isso, os modelos médios e as funções de "
  "transferência do Buck, do Boost e do Buck-Boost podem ser usados diretamente no projeto do "
  "controle dos conversores isolados, o que era a justificativa do ensaio.")
p("A equivalência tem limites claros: ela não representa a corrente magnetizante, o reset do "
  "núcleo, as restrições de razão cíclica, os esforços nas chaves do primário nem os efeitos da "
  "dispersão, que continuam exigindo o circuito isolado para o dimensionamento. O Flyback mostrou, "
  "ainda, que o modo de condução muda qualitativamente a planta, de segunda ordem em MCC para "
  "primeira ordem com ganho dependente da carga em MCD, embora a equivalência seja exata nos dois "
  "casos. Como continuação natural, propõe-se levantar as funções de transferência sobre os "
  "equivalentes, projetar os controladores e repetir o ensaio de degrau em malha fechada.")

# =====================================================================
REFS = [
 "R. P. Torrico Bascopé, Análise de Conversores CC-CC Isolados e Comparação com os Equivalentes "
 "(Trabalho 2). Notas de aula de Eletrônica Industrial, Universidade Federal do Ceará, "
 "Fortaleza, 2026.",
 "R. W. Erickson e D. Maksimović, Fundamentals of Power Electronics, 3rd ed. Cham: Springer, "
 "2020.",
 "N. Mohan, T. M. Undeland e W. P. Robbins, Power Electronics: Converters, Applications, and "
 "Design, 3rd ed. Hoboken: Wiley, 2003.",
 "I. Barbi, Projetos de Fontes Chaveadas, 3. ed. Florianópolis: Edição do Autor, 2015.",
 "I. Barbi e D. C. Martins, Conversores CC-CC Básicos Não Isolados, 4. ed. Florianópolis: "
 "Edição dos Autores, 2011.",
 "M. H. Rashid, Power Electronics: Devices, Circuits, and Applications, 4th ed. Harlow: "
 "Pearson, 2014.",
 "A. I. Pressman, K. Billings e T. Morey, Switching Power Supply Design, 3rd ed. Nova York: "
 "McGraw-Hill, 2009.",
 "Plexim GmbH, PLECS User Manual, versão 5.0. Zurique, 2025.",
 "R. D. Middlebrook e S. Ćuk, “A general unified approach to modelling switching-converter power "
 "stages,” em Proc. IEEE Power Electronics Specialists Conf., 1976, pp. 18–34.",
]
