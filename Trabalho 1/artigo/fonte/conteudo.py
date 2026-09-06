# -*- coding: utf-8 -*-
"""Conteudo do artigo IEEE. Blocos: h1, h2, p, eq, fig, tab, bul, ref."""

TITULO = ("Expressões de Perdas em Semicondutores de Potência e Projeto de\n"
          "Transformador de Alta Frequência com Núcleo de Ferrite")

AUTORES = [
    dict(nome="José Carlos Moreira de Brito Neto",
         dep="Departamento de Engenharia Elétrica",
         org="Universidade Federal do Ceará",
         cid="Fortaleza, Brasil",
         mail="cneto3240@gmail.com"),
    dict(nome="Jonatas Manoel Assunção Felix",
         dep="Departamento de Engenharia Elétrica",
         org="Universidade Federal do Ceará",
         cid="Fortaleza, Brasil",
         mail="jonatasmanoela@gmail.com"),
]

RESUMO = (
    "Este trabalho reúne em uma única formulação as expressões de perdas dos quatro "
    "dispositivos semicondutores de potência de uso corrente e aplica esse ferramental ao "
    "projeto de um transformador de alta frequência com núcleo de ferrite Thornton. Na "
    "primeira parte são deduzidas as perdas de condução e de comutação do diodo, do tiristor "
    "e do TRIAC, do MOSFET e do IGBT, cada uma verificada em exemplo numérico com componente "
    "comercial e parâmetros de catálogo. Mostra-se que o modelo de comutação com carga "
    "indutiva grampeada conduz a perdas 3,6 vezes maiores que o modelo com carga resistiva, "
    "que o modelo linear subestima em 38 % a comutação do IGBT por ignorar a corrente de "
    "cauda, e que a fronteira de escolha entre MOSFET e IGBT em 400 V se desloca de 6,75 A em "
    "2 kHz para 41,6 A em 100 kHz. Na segunda parte, o método do produto de áreas é aplicado "
    "ao transformador de um conversor em ponte completa de 500 W, 400 V para 54 V, operando em "
    "100 kHz. O núcleo NEE-42/21/20 de material IP12R, com 60 espiras no primário e 10 no "
    "secundário em fio 26 AWG, resulta em 2,514 W de perdas, 35,4 °C de elevação de "
    "temperatura e 99,50 % de rendimento. Registra-se que o critério do produto de áreas é "
    "necessário mas não suficiente, pois a primeira tentativa de projeto o satisfazia com "
    "19 % de folga e ainda assim exigiria 125 % da janela disponível. Aplicando as expressões "
    "da primeira parte ao conversor da segunda, o rendimento estimado é de 96,4 %, com o "
    "retificador de saída respondendo por 65 % das perdas de semicondutor."
)

PALAVRAS = ("perdas em semicondutores, recuperação reversa, cálculo térmico, dissipador de "
            "calor, transformador de alta frequência, núcleo de ferrite, produto de áreas, "
            "conversor em ponte completa")

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
p("Todo conversor estático desperdiça uma fração da energia que processa, e essa fração "
  "aparece como calor em um número reduzido de componentes. Saber quanto calor cada "
  "dispositivo produz é o que permite escolher o semicondutor, dimensionar o dissipador, "
  "estimar o rendimento e, em última análise, decidir se a topologia é viável. O primeiro "
  "objetivo deste trabalho é reunir, em uma formulação única e verificável, as expressões que "
  "quantificam essas perdas nos quatro dispositivos de uso corrente em eletrônica de potência.")
p("O segundo objetivo é o projeto de um transformador de alta frequência com núcleo de ferrite "
  "do fabricante nacional Thornton. À primeira vista os dois temas não se conversam, mas eles "
  "são as duas metades do mesmo problema. Um transformador de alta frequência só existe porque "
  "os semicondutores comutam rápido, e a frequência que permite reduzir o seu volume é a mesma "
  "que faz crescer a perda de comutação nas chaves. Por isso o trabalho se fecha com um exemplo "
  "em que as duas partes se encontram: as expressões da primeira parte são aplicadas ao "
  "conversor cujo transformador foi projetado na segunda.")
p("A abordagem adotada procura ser simultaneamente aprofundada e legível. Cada expressão é "
  "deduzida a partir da definição de potência média, e não apenas enunciada, e cada dispositivo "
  "recebe ao final um exemplo numérico completo com componente comercial e parâmetros extraídos "
  "de folhas de dados reais. Nenhum valor foi arbitrado.")
p("O texto está organizado em duas partes. A Seção II estabelece o modelo geral de perdas e as "
  "Seções III a VI o particularizam para o diodo, o tiristor e o TRIAC, o MOSFET e o IGBT. A "
  "Seção VII consolida as expressões, desenvolve o cálculo térmico e responde quantitativamente "
  "à questão de escolha entre MOSFET e IGBT. A Seção VIII apresenta os fundamentos de "
  "magnéticos em alta frequência e deduz o critério do produto de áreas, aplicado na Seção IX ao "
  "projeto do transformador. A Seção X reúne as duas partes no balanço de perdas do conversor "
  "completo.")

# =====================================================================
h1("Modelo Geral de Perdas")
h2("A chave ideal como referência")
p("A eletrônica de potência se apoia na ideia de processar energia comutando e não dissipando. "
  "Uma chave ideal do tipo SPST teria resistência de condução nula, resistência de bloqueio "
  "infinita, transição instantânea entre os dois estados, controle pleno das duas transições e "
  "consumo nulo no circuito de comando [3]. Nenhum dispositivo real reúne essas características, "
  "e essa lista funciona como grade de leitura, porque cada perda quantificada adiante é a "
  "violação de um de seus itens. A queda de condução viola o primeiro item, a corrente de fuga "
  "viola o segundo, os tempos finitos de transição violam o quinto e a potência de comando viola "
  "o oitavo.")
p("A potência total dissipada decompõe-se em três parcelas, conforme a Eq. (1.5) do capítulo de "
  "referência [3]. Adotando a notação do material da disciplina [1], escreve-se")
eq(r"\begin{gathered} P_{\mathrm{total}} = P_{\mathrm{cond}} + P_{\mathrm{com}} \\ "
   r"P_{\mathrm{com}} = P_{\mathrm{ec}} + P_{\mathrm{bloq}} \end{gathered}", "1")
p("em que a perda de estado bloqueado foi absorvida por ser desprezível na quase totalidade dos "
  "casos práticos. A distinção essencial entre as duas parcelas restantes é o comportamento com "
  "a frequência: a perda de condução independe de f_s, ao passo que a perda de comutação é "
  "energia perdida por evento de chaveamento e cresce linearmente com f_s. Essa assimetria é o "
  "que organiza toda a escolha de dispositivos.")

h2("Perda de condução e as duas correntes")
p("Em condução, a característica de um dispositivo bipolar não é uma reta pela origem. A junção "
  "impõe uma barreira de potencial, de modo que existe uma tensão de limiar abaixo da qual "
  "praticamente não há corrente e acima da qual a queda cresce de forma quase linear. O modelo "
  "linear por partes captura esse comportamento com dois parâmetros, a tensão de limiar V_TO e a "
  "resistência dinâmica r_T, conforme a Fig. 2(b).")
eq(r"v(t) = V_{\mathrm{TO}} + r_{T}\,i(t)", "2")
p("A potência média em um período resulta da integral do produto entre tensão e corrente. "
  "Separando os dois termos,")
eq(r"P_{\mathrm{cond}} = \frac{1}{T}\int_{0}^{T} V_{\mathrm{TO}}\,i(t)\,dt "
   r"+ \frac{1}{T}\int_{0}^{T} r_{T}\,i^{2}(t)\,dt", "3")
p("O primeiro integrando é linear em i e o segundo é quadrático. Reconhecendo as definições de "
  "valor médio e de valor eficaz, chega-se à expressão que será usada em todo o trabalho.")
eq(r"P_{\mathrm{cond}} = V_{\mathrm{TO}}\,I_{(av)} + r_{T}\,I_{(rms)}^{2}", "4")
p("São necessários dois valores de corrente, e não um. A parcela de limiar contabiliza a carga "
  "que atravessou o dispositivo, uma informação de valor médio, enquanto a parcela resistiva "
  "contabiliza o aquecimento por efeito Joule, uma informação de valor eficaz. Um projetista que "
  "use apenas a corrente média subestima a perda, e um que use apenas a eficaz a superestima. "
  "Quando a folha de dados fornece somente o valor médio, é comum escrever a mesma expressão em "
  "função do fator de forma a igual à razão entre os dois valores, resultando em "
  "V_TO I_(av) + r_T a² I²_(av).")
p("O MOSFET é a exceção ao modelo de dois parâmetros. Na região ôhmica ele se comporta como "
  "resistor puro, sem tensão de limiar, porque a condução se dá por portadores majoritários "
  "através de um canal induzido e não há junção diretamente polarizada no caminho da corrente. "
  "A expressão colapsa em R_DS(on) I²_(rms) e passa a depender exclusivamente do valor eficaz.")

h2("Perda de comutação e a influência da carga")
p("Durante uma transição, tensão e corrente são simultaneamente não nulas por um intervalo de "
  "dezenas a centenas de nanossegundos. A energia perdida é a integral do produto instantâneo, e "
  "a potência média é essa energia multiplicada pelo número de transições por segundo. O "
  "resultado da integral, porém, depende do tipo de carga, e esse é o ponto que mais gera erro "
  "de projeto. A Fig. 1 confronta os dois casos.")
fig("fig03-modelos-comutacao",
    "Sobreposição de tensão e corrente durante a entrada em condução. Com carga resistiva as "
    "duas grandezas variam simultaneamente e a energia é um sexto do produto; com carga "
    "indutiva grampeada elas variam em sequência e a energia é a metade.", 2)
p("Com carga resistiva, tensão e corrente variam ao mesmo tempo. Admitindo variação linear, a "
  "energia de entrada em condução resulta da integral do produto de duas rampas de sentidos "
  "opostos, o que dá o fator um sexto da Eq. (1.36) do livro-texto [3]:")
eq(r"P_{\mathrm{com}} = \frac{1}{6}\,V_{DS}\,I_{D}\,(t_{r} + t_{f})\,f_{s}", "5")
p("Na esmagadora maioria dos conversores, entretanto, a carga vista pela chave é indutiva e "
  "existe um diodo de roda livre grampeando o nó. Na entrada em condução a corrente sobe de zero "
  "até o valor de carga enquanto a tensão permanece no valor do barramento, porque o diodo de "
  "roda livre só bloqueia depois que toda a corrente migrou para a chave. No bloqueio ocorre o "
  "inverso. Em ambos os casos a área sob o produto é a de um triângulo de altura V I e base igual "
  "ao tempo de transição, três vezes maior que no caso resistivo. É esse o modelo do material da "
  "disciplina [1], com acréscimo de 20 % nos tempos para cobrir atrasos de propagação e "
  "dispersão de fabricação.")
eq(r"\begin{gathered} P_{\mathrm{ec}} = \frac{1}{2}\,V_{DS}\,I_{D}\,(1{,}2\,t_{r})\,f_{s} \\ "
   r"P_{\mathrm{bloq}} = \frac{1}{2}\,V_{DS}\,I_{D}\,(1{,}2\,t_{f})\,f_{s} \end{gathered}", "6")
p("A razão entre os dois modelos, para os mesmos tempos, vale 3,6. Sempre que houver diodo de "
  "roda livre, o modelo da Eq. (6) é o correto, e o modelo da Eq. (5) fica reservado a cargas "
  "efetivamente resistivas e, mesmo aí, como limite inferior.")
p("Há ainda uma parcela que nenhum dos dois modelos captura. A capacitância de saída do "
  "dispositivo armazena energia enquanto ele está bloqueado, e essa energia é dissipada "
  "internamente na entrada em condução.")
eq(r"P_{\mathrm{cap}} = \frac{1}{2}\,C_{o(er)}\,V_{DS}^{2}\,f_{s}", "7")
p("O parâmetro relevante é a capacitância equivalente de energia na tensão de operação, e não o "
  "valor de C_oss tabelado a 25 V, que é fortemente não linear e cai por uma ordem de grandeza "
  "até 400 V. Em conversores de alta tensão, baixa corrente e frequência elevada essa parcela "
  "pode superar a de cruzamento, como a Seção X demonstra.")

# =====================================================================
h1("Diodo de Potência")
h2("Características e princípio de polarização")
fig("fig01-diodo-caracteristica",
    "Diodo de potência. (a) Característica real com as três regiões de operação. (b) Modelo "
    "linear por partes, do qual se extraem a tensão de limiar e a resistência dinâmica.", 2)
p("O diodo é o único dispositivo do trabalho cujo estado não é comandado. Quem decide se ele "
  "conduz ou bloqueia é o circuito externo, e por isso ele é o ponto de partida natural, já que "
  "as expressões dos demais dispositivos são variações do que se estabelece aqui. A curva "
  "característica da Fig. 2(a) apresenta três regiões. Na polarização direta, com tensão acima "
  "de aproximadamente 0,7 V, a corrente flui do anodo para o catodo limitada apenas pelo "
  "circuito externo. Na polarização reversa circula somente a corrente de fuga, da ordem de "
  "microampères, idealmente tomada como nula. A região de ruptura é destrutiva para um diodo "
  "retificador, e apenas o diodo Zener é projetado para operar nela.")
p("A grandeza que separa as famílias de diodos de potência não é a corrente nem a tensão, mas o "
  "tempo de recuperação reversa, porque é ele que fixa a frequência máxima de operação. Tanto o "
  "livro-texto [3] quanto o material da disciplina [1] adotam a mesma classificação, que vai do "
  "retificador padrão, com t_rr na faixa de microssegundos e uso restrito a 60 Hz, até o diodo "
  "Schottky, com t_rr abaixo de 30 ns. O diodo Schottky merece nota à parte, porque a sua "
  "condução se dá apenas por portadores majoritários e portanto não há carga armazenada a "
  "remover.")

h2("Perda de condução")
p("Aplicando a Eq. (4) ao diodo, com os parâmetros tomados na temperatura de junção quente,")
eq(r"P_{F} = V_{\mathrm{TO}}\,I_{F(av)} + r_{T}\,I_{F(rms)}^{2}", "8")
p("A extração dos dois parâmetros admite três situações. Na mais conveniente, o fabricante os "
  "fornece diretamente, prática comum nos módulos Semikron [11] e nos diodos de recuperação "
  "rápida da IXYS [12], que os tabelam já na temperatura de operação. Na situação intermediária, "
  "ajusta-se uma reta por dois pontos da curva característica, cercando a corrente eficaz de "
  "operação e não a corrente nominal do dispositivo. Na situação mais pobre, dispõe-se apenas de "
  "um valor máximo de queda direta, e resta o modelo de fonte de tensão pura, que subestima a "
  "perda por ignorar a parcela resistiva.")
p("Vale registrar o comportamento térmico. A queda direta do diodo diminui com a temperatura, "
  "porque o coeficiente negativo de V_TO domina sobre o coeficiente positivo de r_T em correntes "
  "moderadas. A consequência prática é que diodos em paralelo não se equilibram sozinhos, e "
  "exigem casamento térmico rigoroso ou resistores de equalização.")

h2("Perda de comutação")
fig("fig02-recuperacao-reversa",
    "Formas de onda de corrente e de tensão no bloqueio do diodo. A área hachurada é a carga de "
    "recuperação reversa, removida com a tensão reversa já aplicada.")
p("Para passar do bloqueio à condução, o diodo precisa adquirir carga na região de difusão, "
  "processo bem mais rápido que a remoção de carga do processo inverso. Tanto o livro quanto o "
  "material da disciplina são categóricos ao adotar perda desprezível na entrada em condução.")
p("O bloqueio é outra história. Um diodo em condução tem carga armazenada na região de difusão, "
  "e essa carga precisa ser removida antes que a junção possa sustentar tensão reversa. Enquanto "
  "houver excesso de portadores, a junção permanece diretamente polarizada e a tensão sobre o "
  "diodo praticamente não muda. A Fig. 3 mostra a sequência. Entre t₁ e t₂ a corrente reversa "
  "cresce até o pico, instante em que a carga excedente acabou e a junção começa a bloquear; "
  "entre t₂ e t₃ a corrente reversa decai a zero enquanto a tensão sobe rapidamente. É nesse "
  "último intervalo, com corrente e tensão reversas simultaneamente elevadas, que a energia é "
  "dissipada. Partindo das Eqs. (1.10) a (1.12) de [3],")
eq(r"P_{\mathrm{bloq}} = \frac{1}{2}\,Q_{rr}\,V_{R}\,f_{s} "
   r"= \frac{1}{4}\,I_{rr}\,V_{R}\,t_{rr}\,f_{s}", "9")
p("O material da disciplina apresenta a forma V_R Q_rr f_s, sem o fator um meio. As duas "
  "expressões diferem por um fator dois e ambas estão corretas dentro das suas hipóteses. O "
  "fator um meio admite que apenas metade da carga é removida já com a tensão reversa plena "
  "aplicada, enquanto a outra metade é removida no intervalo t₁ a t₂, no qual a tensão sobre o "
  "diodo ainda é pequena. A expressão sem o fator supõe o caso extremo e constitui, portanto, um "
  "critério conservador de projeto. Adota-se aqui a Eq. (9) como valor de referência.")
p("A carga de recuperação não é uma constante do dispositivo. Ela cresce fortemente com a "
  "temperatura de junção, com a taxa de decrescimento da corrente imposta pelo circuito e com a "
  "corrente direta prévia. Por isso as folhas de dados especificam t_rr e I_rr sob condições "
  "declaradas, e usar o valor de 25 °C em um projeto que opera a 100 °C subestima a perda por um "
  "fator próximo de cinco.")

h2("Resultados numéricos")
p("O primeiro exemplo trata de uma ponte monofásica de 60 Hz alimentando carga fortemente "
  "indutiva que drena 30 A contínuos, com módulos Semikron SKKD 46/16. Cada diodo conduz 180° "
  "por período, de modo que a corrente média vale 15,00 A e a eficaz 21,213 A. Com V_TO igual a "
  "0,85 V e r_T igual a 5 mΩ a 125 °C, a perda de condução resulta em 12,750 W de parcela de "
  "limiar mais 2,250 W de parcela resistiva, totalizando 15,00 W por diodo e 60,0 W na ponte. "
  "Note-se que 85 % da perda vem do termo de limiar, o que é característico de retificação de "
  "rede com corrente moderada.")
p("O segundo exemplo mostra o outro extremo. Um conversor elevador de 200 V para 400 V "
  "entregando 1 kW a 50 kHz, com diodo DSEI2x31-06C, tem corrente média de 2,50 A e eficaz de "
  "3,536 A no diodo. Com V_F0 igual a 1,10 V e r_F igual a 7,9 mΩ, a perda de condução vale "
  "2,849 W. A perda de bloqueio, calculada pela Eq. (9) com a carga estimada pela aproximação "
  "triangular, vale 1,58 W a 25 °C e alcança 7,50 W no pior caso de catálogo a 100 °C. A "
  "comutação passa de 36 % para 73 % da perda total apenas pela mudança de temperatura, o que "
  "faz da recuperação reversa o parâmetro mais incerto de todo o cálculo. Acima de 20 kHz o "
  "diodo de silício deixa de ser limitado pela sua queda direta e passa a ser limitado pela sua "
  "recuperação reversa, constatação que justifica economicamente o diodo Schottky de carbeto de "
  "silício.")

# =====================================================================
h1("Tiristor e TRIAC de Potência")
h2("Características e princípio de polarização")
fig("fig04-scr-caracteristica",
    "Tiristor. (a) Característica com a corrente de porta como parâmetro, mostrando a redução da "
    "tensão de disparo. (b) Modelo de dois transistores acoplados, que explica o travamento.", 2)
p("O tiristor introduz uma categoria que não existia no diodo, a do dispositivo semicontrolado. "
  "É possível decidir quando ele entra em condução, mas não quando ele sai, porque o bloqueio "
  "depende do circuito. Com o anodo positivo e a porta aberta, as junções J₁ e J₃ ficam "
  "diretamente polarizadas e J₂ reversamente, de modo que o dispositivo sustenta tensão direta. "
  "Essa é a propriedade que define a família tiristor, pois nenhum outro dispositivo de potência "
  "bloqueia tensão direta com polarização direta aplicada.")
p("O comportamento é explicado pelo modelo de dois transistores acoplados da Fig. 4(b). Um pulso "
  "positivo de corrente na porta torna-se corrente de base do NPN, cujo coletor fornece corrente "
  "de base ao PNP, cujo coletor realimenta a base do NPN. A realimentação positiva sustenta a "
  "condução mesmo depois que o sinal de porta é retirado. Daí decorrem as três consequências que "
  "governam o projeto: a porta perde o controle após o disparo e o único modo de bloquear é levar "
  "a corrente de anodo abaixo da corrente de manutenção; o pulso de porta pode ser curto desde "
  "que a corrente de anodo ultrapasse a corrente de travamento antes de o pulso terminar; e o "
  "disparo é sempre por corrente, nunca por tensão [1].")
p("O TRIAC é bidirecional em corrente e em tensão, funcionalmente equivalente a dois tiristores "
  "em antiparalelo com porta comum. Necessita de disparo a cada semiciclo e bloqueia naturalmente "
  "na passagem por zero da corrente. Os dois métodos de acionamento têm consequências opostas "
  "sobre a qualidade de energia. O controle de fase permite variação contínua da potência ao "
  "custo de elevado conteúdo harmônico na corrente de entrada, ao passo que a comutação no "
  "cruzamento por zero reduz drasticamente a injeção de harmônicas mas oferece controle discreto.")
p("A classificação desses dispositivos como de baixa frequência é quantitativa e está no tempo de "
  "recuperação comutada, o intervalo de que o dispositivo precisa para recuperar a capacidade de "
  "bloqueio direto. Em 60 Hz o semiperíodo é de 8,33 ms e um tempo de 50 µs consome 0,6 % dele, "
  "o que é irrelevante. A 1 kHz o semiperíodo cai para 500 µs e o mesmo tempo já consome 10 %. "
  "Acima disso o dispositivo não recupera a tempo, e uma tensão direta reaplicada com dv/dt "
  "elevado o redispara.")

h2("Perdas e resultados numéricos")
p("Em condução o tiristor comporta-se como um diodo, e o livro-texto é explícito ao afirmar que "
  "a potência dissipada é calculada da mesma forma, acrescentando apenas a perda de porta [3]. "
  "Vale portanto a Eq. (4), com a ressalva de que no TRIAC o valor médio deve ser entendido como "
  "média do módulo da corrente, já que a queda de limiar se opõe à circulação nos dois sentidos. "
  "Essa sutileza passa despercebida com frequência, porque o valor médio da corrente de um TRIAC "
  "em controle de fase simétrico é rigorosamente zero.")
eq(r"P_{G} = V_{GT}\,I_{GT}\,\delta_{G}", "10")
p("A perda de porta, dada pela Eq. (10) com a razão cíclica do pulso de disparo, é da ordem de "
  "miliwatts em 60 Hz e sempre desprezível frente à condução.")
p("No terceiro exemplo, uma ponte monofásica totalmente controlada com tiristores TYN1225 "
  "alimenta carga fortemente indutiva de 15 A. Cada tiristor conduz 180°, com corrente média de "
  "7,50 A e eficaz de 10,607 A. Com V_TO igual a 0,77 V e r_T igual a 14 mΩ, a perda de condução "
  "vale 7,350 W. A perda de porta, com pulso de 200 µs, resulta em 0,62 mW. As perdas de "
  "comutação, estimadas por limites superiores generosos, somam cerca de 1,05 W, e a condução "
  "responde por 87,5 % do total de 8,40 W. Confirma-se a regra de que em 60 Hz dimensiona-se "
  "tiristor pela condução.")
p("Um resultado que merece destaque é que a corrente do tiristor é retangular de 180° qualquer "
  "que seja o ângulo de disparo, de modo que a perda de condução não depende dele. A potência "
  "entregue à carga, ao contrário, cai com o cosseno do ângulo, e o rendimento do conversor "
  "degrada-se conforme se afasta do disparo pleno, passando de 0,99 % de perda relativa em 0° "
  "para 3,82 % em 75°.")
fig("fig05-triac-alpha",
    "Perda de condução no TRIAC BTA41-600B e potência entregue à carga, em função do ângulo de "
    "disparo, para controlador de tensão alternada de 220 V sobre carga resistiva de 10 Ω.")
p("O quarto exemplo trata de um controlador de tensão alternada com TRIAC BTA41-600B, 220 V "
  "sobre carga resistiva de 10 Ω. A Fig. 5 mostra o comportamento com o ângulo de disparo. Para "
  "90°, a corrente eficaz vale 15,556 A e a média do módulo 9,904 A, resultando em 12,318 W de "
  "perda contra 2420 W entregues à carga, ou 0,51 %. O caso dimensionante do dissipador é o "
  "disparo pleno, com 24,64 W. A perda relativa permanece próxima de 0,5 % em toda a faixa útil, "
  "o que faz do controle de fase uma solução muito eficiente do ponto de vista térmico. O seu "
  "problema não é rendimento, e sim qualidade de energia.")

# =====================================================================
h1("MOSFET de Potência")
h2("Características e princípio de polarização")
p("O MOSFET é o primeiro dispositivo plenamente controlado deste trabalho, e o único cuja perda "
  "de condução não tem tensão de limiar. Na estrutura de canal n do tipo intensificação, a "
  "aplicação de tensão positiva na porta cria um canal induzido que interliga as regiões de "
  "dreno e de fonte. Duas consequências estruturais importam ao projeto. A primeira é o diodo de "
  "corpo, formado pelo curto-circuito entre o substrato e a fonte, útil como roda livre mas de "
  "recuperação muito lenta, com t_rr de até 710 ns e carga de 7,5 µC no IRFP460A [15]. A segunda "
  "é a condução por portadores majoritários, razão física da ausência de tensão de limiar.")
p("A característica de saída apresenta duas regiões. Na região ativa a corrente de dreno "
  "independe da tensão dreno-fonte, e é a região a evitar em chaveamento. Na região ôhmica a "
  "relação é linear, e é nela que o MOSFET opera como chave fechada. A resistência do canal nessa "
  "região é o parâmetro de seleção mais importante do dispositivo.")
fig("fig06-mosfet-comutacao",
    "Os seis intervalos de comutação do MOSFET. Os tempos de subida e de descida da corrente são "
    "os intervalos em que tensão e corrente se sobrepõem, e são eles que entram no cálculo de "
    "perdas.")
p("O comportamento dinâmico é inteiramente governado pelas capacitâncias parasitas. A Fig. 6 "
  "divide o chaveamento nos seis intervalos descritos em [3]. Três conclusões de projeto saem "
  "daí. Os tempos t_r e t_f são os intervalos em que tensão e corrente se sobrepõem, e são eles, "
  "e não os atrasos de propagação, que entram no cálculo de perdas. A velocidade de comutação é "
  "ajustável pelo resistor de porta, o que constitui um compromisso entre perda e interferência "
  "eletromagnética, e não uma constante do dispositivo. E a corrente de porta precisa ter caminho "
  "de retorno no bloqueio, sob pena de o dispositivo permanecer na região ativa por tempo demais.")

h2("Perdas e resultados numéricos")
p("Sem tensão de limiar, a Eq. (1.35) do livro-texto e a expressão do material da disciplina "
  "coincidem:")
eq(r"P_{\mathrm{cond}} = R_{DS(on)}(T_{j})\,I_{D(rms)}^{2}", "11")
p("A correção térmica da resistência de canal não é refinamento, e sim requisito. O material da "
  "disciplina é explícito ao exigir que o valor de catálogo, normalmente fornecido a 25 °C, seja "
  "corrigido para a temperatura de junção de 100 °C usando a curva normalizada [1]. A razão "
  "física é a queda da mobilidade dos portadores com a temperatura, quantificada em "
  "aproximadamente 0,6 % por grau [3], o que permite a estimativa analítica")
eq(r"\begin{gathered} R_{DS(on)}(T_{j}) = k_{T}\,R_{DS(on)}(25\,^{\circ}\mathrm{C}) \\ "
   r"k_{T} = 1 + 0{,}006\,(T_{j} - 25) \end{gathered}", "12")
p("Para 100 °C o fator k_T vale 1,45, e ignorar essa correção subestima a perda de condução em "
  "45 %. Há um lado positivo nesse coeficiente positivo de temperatura, que é tornar o paralelismo de "
  "MOSFETs auto-equalizante e eliminar a segunda ruptura.")
p("O quinto exemplo trata de um conversor abaixador alimentado em 200 V, entregando 8 A com "
  "razão cíclica 0,5 a 50 kHz, com MOSFET IRFP460A. A corrente eficaz vale 5,657 A e a "
  "resistência corrigida 0,3915 Ω, resultando em 12,528 W de perda de condução. Aplicando a Eq. "
  "(6) com t_r igual a 55 ns e t_f igual a 39 ns, a perda de comutação vale 4,512 W, dos quais "
  "2,640 W na entrada em condução e 1,872 W no bloqueio. O total de 17,040 W tem 26,5 % de "
  "comutação. Para contraste, o modelo de carga resistiva da Eq. (5) daria 1,253 W, ou 3,6 vezes "
  "menos, e conduziria a um erro de 23 % na temperatura de junção estimada.")

# =====================================================================
h1("IGBT de Potência")
h2("Características e princípio de polarização")
p("O IGBT existe para resolver um problema estrutural do MOSFET. A resistência de canal cresce "
  "com a tensão de bloqueio elevada a uma potência entre 2,4 e 2,6, porque a região de deriva "
  "precisa ser mais espessa e menos dopada para suportar o campo elétrico. A solução foi "
  "acrescentar uma camada p no lado do coletor, combinando a porta isolada do MOSFET com a "
  "condução por portadores minoritários do transistor bipolar. A injeção de minoritários na "
  "região de deriva modula a sua condutividade e cancela aquele crescimento.")
p("O preço é que esses portadores precisam ser removidos no bloqueio, e é isso que produz a "
  "corrente de cauda. Ela é o escoamento dos minoritários que ainda estão na região de deriva e "
  "que não podem ser removidos pela porta, desaparecendo apenas por recombinação, com a tensão "
  "de barramento plena aplicada. Há um compromisso embutido, pois quanto menor a tensão de "
  "saturação, maior a cauda. O livro registra a escolha da indústria de projetar para cauda "
  "baixa, aceitando tensão de saturação um pouco acima do mínimo possível, já que acima de 10 a "
  "20 kHz as perdas de comutação dominam [3].")
p("A estrutura de quatro camadas contém, inevitavelmente, um tiristor parasita entre coletor e "
  "emissor, cujo travamento faria a porta perder o controle do dispositivo. Os fabricantes o "
  "evitam reduzindo a resistência do corpo p sob o emissor. Ao contrário do MOSFET, o IGBT não "
  "tem diodo de corpo intrínseco, e quando um diodo antiparalelo é necessário, o fabricante o "
  "integra separadamente no mesmo encapsulamento.")
p("A classificação por tecnologia de fabricação tem consequência direta de projeto. Os "
  "dispositivos do tipo NPT têm coeficiente de temperatura positivo da tensão de saturação e são "
  "favoráveis ao paralelismo, ao passo que os do tipo PT têm coeficiente negativo e não devem ser "
  "paralelados sem casamento rigoroso [1].")

h2("Perdas e resultados numéricos")
p("Em condução o ponto de operação está na região de saturação, e o IGBT é modelado por uma "
  "fonte de tensão constante cujo valor o fabricante fornece.")
eq(r"P_{\mathrm{cond}} = V_{CE(sat)}\,I_{C(av)} = V_{CE(sat)}\,I_{C}\,D", "13")
p("Comparando com os três dispositivos anteriores, o IGBT é o único cuja perda de condução "
  "depende apenas do valor médio. Diodo e tiristor precisam de média e de eficaz, o MOSFET "
  "apenas da eficaz e o IGBT apenas da média, o que decorre da modelagem por fonte de tensão "
  "pura. Quando o catálogo fornece a curva completa, é preferível o modelo de dois parâmetros, "
  "idêntico ao do diodo, que corrige a subestimação em correntes acima da nominal.")
p("Para a comutação, os fabricantes de IGBT quase sempre fornecem diretamente as energias "
  "medidas em bancada, e essa é a via preferível:")
eq(r"P_{\mathrm{com}} = \left(E_{on} + E_{off}\right) f_{s}", "14")
p("A razão de fundo é que as energias medidas incluem os dois efeitos que o modelo linear "
  "ignora, a corrente de cauda no bloqueio e a recuperação reversa do diodo de roda livre na "
  "entrada em condução.")
p("O sexto exemplo trata de um braço de inversor com barramento de 400 V, corrente de coletor de "
  "20 A, razão cíclica média 0,5 e frequência de 10 kHz, com IGBT IRG4PC40UD. A perda de "
  "condução vale 17,20 W. O modelo linear da Eq. (6), com t_r igual a 57 ns e t_f igual a 80 ns, "
  "dá 6,576 W de comutação, ao passo que as energias de catálogo, de 0,71 mJ e 0,35 mJ, dão "
  "10,60 W. O modelo linear subestima a perda em 38 %, e a diferença é precisamente a corrente "
  "de cauda e a recuperação reversa do diodo. Para o IGBT, portanto, as energias de catálogo "
  "prevalecem sempre que disponíveis. O total de 27,80 W tem 38 % de comutação, e as duas "
  "parcelas se igualam por volta de 16 kHz, o que explica por que inversores industriais operam "
  "entre 2 e 16 kHz.")
p("Vale a advertência de que o diodo antiparalelo tem circuito térmico próprio, com resistência "
  "junção-cápsula mais que o dobro da do IGBT, 1,7 contra 0,77 °C/W no dispositivo usado. Em "
  "conversores com fator de potência baixo ou operação regenerativa, é o diodo, e não o IGBT, "
  "que determina a temperatura de junção.")

# =====================================================================
h1("Síntese Comparativa e Cálculo Térmico")
h2("Grade unificada das expressões")
tab("Expressões de Perdas Consolidadas",
    [["Dispositivo", "Perda de condução", "Perda de comutação"],
     ["Diodo", "V_TO I_(av) + r_T I²_(rms)", "½ Q_rr V_R f_s"],
     ["Tiristor e TRIAC", "V_TO I_(av) + r_T I²_(rms)", "desprezível para f_s < 1 kHz"],
     ["MOSFET", "R_DS(on)(T_j) I²_(rms)", "0,6 V I (t_r + t_f) f_s + ½ C_o(er) V² f_s"],
     ["IGBT", "V_CE(sat) I_(av)", "(E_on + E_off) f_s"]],
    [0.20, 0.35, 0.45], span=2,
    note="No TRIAC, o valor médio é o da corrente em módulo. No diodo, a perda de entrada em "
         "condução é desprezível.")
p("A Tabela I reúne as expressões deduzidas nas seções anteriores. A coluna da direita da "
  "expressão de condução revela uma diferença física real: onde há junção diretamente "
  "polarizada, existe tensão de limiar e a corrente média importa; onde a condução é por canal "
  "resistivo, importa apenas o valor eficaz. A Fig. 7 traduz em curvas a assimetria "
  "entre as duas parcelas.")
fig("fig07-perda-vs-frequencia",
    "Perda total nos três dispositivos comutados dos exemplos, em função da frequência. As "
    "linhas horizontais são os patamares de condução, independentes da frequência; a inclinação "
    "unitária em escala logarítmica é a assinatura da perda de comutação.")

h2("Circuito térmico e dimensionamento do dissipador")
fig("fig08-circuito-termico",
    "Circuito térmico equivalente para dois dispositivos montados no mesmo dissipador. A "
    "potência faz o papel da corrente, a temperatura o da tensão e a resistência térmica o da "
    "resistência elétrica.", 2)
p("Calcular a perda não é um fim em si. O objetivo é responder se o dispositivo sobrevive e que "
  "dissipador é necessário. O caminho é o circuito térmico equivalente da Fig. 8, no qual a "
  "potência dissipada faz o papel da corrente e a temperatura o da tensão. Percorrendo a cadeia a "
  "partir da junção,")
eq(r"\begin{gathered} T_{c} = T_{j} - P_{av}R_{th,jc} \\ T_{d} = T_{c} - P_{av}R_{th,cd} \\ "
   r"R_{th,da} = \frac{T_{d} - T_{a}}{P_{av}} \end{gathered}", "15")
p("O material da disciplina fixa as convenções de projeto. A resistência junção-cápsula vem do "
  "catálogo do semicondutor, a resistência cápsula-dissipador vale aproximadamente 0,5 °C/W para "
  "isolador de mica ou silicone, a temperatura de junção é escolhida entre 100 °C e 120 °C como "
  "margem sobre o limite de catálogo, e a temperatura ambiente entre 25 °C e 70 °C conforme o "
  "local [1]. Convém insistir que a temperatura ambiente relevante é a do interior do gabinete, "
  "e não a da sala, sob pena de erro grosseiro no dimensionamento.")
p("Quando vários dispositivos compartilham o mesmo dissipador, situação normal em conversores, o "
  "procedimento correto é calcular para cada dispositivo a temperatura de dissipador que ele "
  "exige, tomar o menor valor e dividi-lo pela soma de todas as potências.")
eq(r"R_{th,da} = \frac{\mathrm{min}\{T_{d,k}\} - T_{a}}{P_{1} + P_{2} + \cdots + P_{n}}", "16")
p("A lógica é direta, pois o dissipador é um só e tem uma única temperatura, que precisa ser "
  "baixa o bastante para o dispositivo mais exigente e capaz de escoar o calor de todos. O erro "
  "clássico é dividir a resistência pelo número de dispositivos, o que só vale no caso "
  "particular em que todos dissipam a mesma potência e têm as mesmas resistências térmicas.")
p("O sétimo exemplo ilustra o procedimento em um retificador semicontrolado com dois tiristores "
  "TYN1225 e dois diodos SKKD 46, alimentando carga de 15 A com temperatura ambiente de 40 °C. "
  "Os tiristores dissipam 7,350 W e os diodos 6,938 W. Adotando temperatura de junção de 110 °C "
  "para ambos, a temperatura de dissipador exigida vale 91,6 °C para o tiristor e 102,4 °C para o "
  "diodo. O tiristor é o dispositivo dimensionante, apesar de dissipar apenas 6 % a mais, porque "
  "a sua resistência junção-cápsula é mais de três vezes maior. Com 28,58 W de perda total, "
  "resulta uma exigência de 1,81 °C/W para o dissipador, e a verificação confirma 110,1 °C na "
  "junção do tiristor e 99,3 °C na do diodo.")

h2("A fronteira entre MOSFET e IGBT")
fig("fig09-fronteira-mosfet-igbt",
    "Fronteira de escolha entre MOSFET e IGBT em barramento de 400 V. (a) Perda total em função "
    "da corrente comutada a 20 kHz. (b) Corrente de cruzamento em função da frequência.", 2)
p("Este é o cálculo que decide o projeto na prática. Igualando as perdas totais dos dois "
  "dispositivos no mesmo ponto de operação e dividindo por I, uma vez que as parcelas do IGBT "
  "são todas lineares na corrente e a de condução do MOSFET é quadrática,")
eq(r"I_{\mathrm{cruz}} = \frac{V_{CE(sat)}D + e_{sw}f_{s} "
   r"- 0{,}6\,V(t_{r}+t_{f})f_{s}}{R_{DS(on)}\,D}", "17")
p("em que e_sw é a energia de comutação por ampère do IGBT. Abaixo dessa corrente o MOSFET "
  "vence, e acima dela o IGBT. Comparando o SPW20N60C3 com o IRG4PC40UD em 400 V e razão cíclica "
  "0,5, a corrente de cruzamento vale 6,75 A em 2 kHz, 13,2 A em 20 kHz e 41,6 A em 100 kHz.")
p("Três conclusões saem daí, e a terceira é contra-intuitiva. Em corrente baixa o MOSFET é "
  "imbatível, porque a perda cai com o quadrado enquanto a do IGBT cai apenas linearmente, e a "
  "tensão de limiar do IGBT é um custo fixo que não desaparece em carga leve. Em corrente alta o "
  "IGBT é imbatível, pela lei que relaciona a resistência de canal à tensão de bloqueio. E a "
  "fronteira se desloca para cima com a frequência, porque quanto maior a frequência mais "
  "severamente a energia de comutação penaliza o IGBT, ampliando a faixa de corrente em que o "
  "MOSFET compensa a sua pior condução com a sua comutação muito mais rápida. A Fig. 9(b) mostra "
  "também que a partir de 50 kHz a perda no ponto de cruzamento já é tão alta que nenhum dos dois "
  "é utilizável naquela corrente, e a resposta correta passa a ser mudar de topologia ou de "
  "tecnologia.")

tab("Resultados Numéricos dos Sete Exemplos",
    [["#", "Componente", "Aplicação", "f_s", "P_cond", "P_com", "P_total"],
     ["1", "SKKD 46/16", "Ponte de 60 Hz, 30 A", "60 Hz", "15,00 W", "~0", "15,00 W"],
     ["2", "DSEI2x31-06C", "Elevador de 1 kW", "50 kHz", "2,85 W", "7,44 W", "10,29 W"],
     ["3", "TYN1225", "Retificador controlado, 15 A", "60 Hz", "7,35 W", "1,05 W", "8,40 W"],
     ["4", "BTA41-600B", "Controlador CA, 2,4 kW", "60 Hz", "12,32 W", "~0", "12,32 W"],
     ["5", "IRFP460A", "Abaixador de 200 V, 8 A", "50 kHz", "12,53 W", "4,51 W", "17,04 W"],
     ["6", "IRG4PC40UD", "Braço de inversor, 400 V, 20 A", "10 kHz", "17,20 W", "10,60 W",
      "27,80 W"],
     ["7", "TYN1225 e SKKD 46", "Ponte mista, 15 A", "60 Hz", "28,58 W", "~0", "28,58 W"]],
    [0.04, 0.17, 0.30, 0.10, 0.13, 0.13, 0.13], span=2,
    note="O exemplo 4 é apresentado no ângulo de disparo de 90°; o caso dimensionante do "
         "dissipador é o disparo pleno, com 24,64 W.")
p("A Tabela II consolida os sete exemplos. A fração de comutação cresce monotonicamente com a "
  "frequência, de praticamente zero em 60 Hz a mais de 70 % em 50 kHz. É essa progressão que "
  "separa as famílias de dispositivos e que justifica o esforço de modelar corretamente uma "
  "perda que dura nanossegundos.")

# =====================================================================
h1("Fundamentos do Transformador de Alta Frequência")
h2("Materiais magnéticos e dinâmica do laço")
p("O transformador é o mesmo dispositivo desde Faraday, mas o seu tamanho não é. A lei da indução "
  "relaciona a tensão aplicada ao produto entre número de espiras, área do núcleo e taxa de "
  "variação do fluxo, de modo que aumentar a frequência permite reduzir proporcionalmente o "
  "produto entre espiras e área. O transformador de 500 W projetado adiante usa um núcleo de "
  "2,4 cm² e pesa 112 g, contra alguns quilogramas de um equivalente em 60 Hz.")
p("Em 60 Hz as correntes parasitas são controladas laminando o aço, solução que deixa de ser "
  "viável conforme a frequência sobe. O ferrite resolve o problema por outro caminho, sendo um "
  "material cerâmico composto de óxidos cuja resistividade é milhões de vezes maior que a do "
  "aço [2]. Os ferrites moles dividem-se em manganês-zinco, de alta permeabilidade e uso em "
  "conversores de potência, e níquel-zinco, de altíssima resistividade e uso em filtros de "
  "interferência. O material IP12R da Thornton, adotado neste projeto, pertence à primeira "
  "família, com permeabilidade inicial de 2100 e densidade de saturação de 0,51 T a 23 °C [9].")
fig("fig10-laco-bh",
    "Dinâmica do laço B-H nos conversores isolados. O processamento assimétrico do Forward "
    "percorre apenas o primeiro quadrante, ao passo que o processamento simétrico da ponte "
    "completa aproveita o dobro da capacidade do núcleo.", 2)
p("A escolha da excursão de fluxo depende do modo de excitar o núcleo, e a Fig. 10 mostra os dois "
  "casos tratados em [2]. No processamento assimétrico do conversor Forward a energia é "
  "transferida em apenas um semiciclo e o outro é usado para desmagnetizar, de modo que a "
  "corrente de magnetização é sempre positiva e o laço percorrido é unipolar. No processamento "
  "simétrico da ponte completa há duas transferências por período e o laço é percorrido "
  "simetricamente em torno da origem. Para a mesma excursão total, o conversor simétrico "
  "aproveita o dobro da capacidade do núcleo, e é essa a razão pela qual a ponte completa é a "
  "topologia natural acima de algumas centenas de watts.")

h2("Lei de Faraday e número de espiras")
p("Aplicando a lei da indução a um enrolamento de N espiras sobre núcleo de seção A_e e "
  "integrando ao longo do intervalo em que a tensão é aplicada, a excursão de fluxo é "
  "determinada pelo produto tensão-segundo dividido pelo produto entre espiras e área. Para onda "
  "quadrada que ocupe o semiperíodo inteiro, generalizando com o fator de forma de onda K_f, "
  "resulta a expressão do material de referência [2]:")
eq(r"N_{p} = \frac{V_{p}\,10^{4}}{K_{f}\,B_{ac}\,f_{s}\,A_{e}}", "18")
p("com K_f igual a 4,0 para onda quadrada e 4,44 para senoide. Num conversor em ponte completa "
  "com razão cíclica menor que 0,5 por diagonal, porém, a tensão só é aplicada durante uma "
  "fração do semiperíodo, e a forma direta a partir de Faraday fica")
eq(r"\Delta B = \frac{V_{in}\,D}{N_{p}\,A_{e}\,f_{s}}", "19")
p("As duas formas coincidem para razão cíclica igual a 0,5, com a excursão total valendo o dobro "
  "da amplitude. O cálculo pela Eq. (18) embute portanto o pior caso e produz mais espiras do que "
  "o estritamente necessário na razão cíclica nominal, o que constitui margem. Essa distinção "
  "não é sutileza de notação: em malha fechada a razão cíclica sobe quando a tensão de entrada "
  "cai, e o pior caso de fluxo é sempre a razão cíclica máxima. Adota-se aqui dimensionar pela "
  "Eq. (18) e verificar pela Eq. (19).")

h2("Perdas no núcleo e efeito pelicular")
p("As perdas no núcleo têm dois mecanismos. A histerese converte em calor, a cada ciclo, a "
  "energia correspondente à área do laço, e é proporcional à frequência. As correntes parasitas "
  "resultam das tensões induzidas no próprio material e são proporcionais ao quadrado da "
  "frequência. Para ferrite, a forma que separa explicitamente os dois mecanismos é [5]")
eq(r"P_{\mathrm{núcleo}} = \Delta B^{2{,}4}"
   r"\left(K_{H}f_{s} + K_{E}f_{s}^{2}\right)V_{e}", "20")
p("com ΔB em tesla, f_s em hertz, volume efetivo em cm³ e os coeficientes 4×10⁻⁵ para histerese e "
  "4×10⁻¹⁰ para correntes parasitas. Igualando as duas parcelas obtém-se 100 kHz, exatamente a "
  "frequência deste projeto, de modo que os dois mecanismos contribuem igualmente. Abaixo dessa "
  "frequência domina a histerese e acima dominam as correntes parasitas, e a partir daí a perda "
  "cresce com o quadrado da frequência, o que estabelece o teto prático do ferrite manganês-zinco.")
p("O material de referência registra a prática da indústria de traçar as curvas de densidade de "
  "fluxo recomendada para uma densidade de perdas de 100 mW/cm³, valor que permite elevação de "
  "temperatura de cerca de 40 °C em núcleos de porte médio [2]. Aplicando esse critério à "
  "Eq. (20) em 100 kHz resulta um limite de 0,161 T para a excursão de fluxo, bem abaixo da "
  "saturação a quente. Confirma-se assim que em alta frequência quem limita a densidade de fluxo "
  "é a perda, e não o joelho da curva de magnetização.")
fig("fig11-efeito-pelicular",
    "Diâmetro máximo de condutor admissível em função da frequência, com as bitolas AWG "
    "indicadas. Em 100 kHz o limite é o fio 26 AWG.")
p("No cobre, a alta frequência traz o efeito pelicular. O fluxo magnético interno ao próprio fio "
  "induz correntes que cancelam a corrente no centro e a reforçam na superfície, de modo que a "
  "seção efetivamente útil é menor que a geométrica. A profundidade de penetração e a regra de "
  "dimensionamento correspondente são")
eq(r"\begin{gathered} \varepsilon = \frac{6{,}62}{\sqrt{f_{s}}}\ \mathrm{[cm]} \\ "
   r"D_{\mathrm{fio}} \le 2\,\varepsilon \end{gathered}", "21")
p("A Fig. 11 mostra a severidade do efeito. Em 100 kHz o fio mais grosso admissível é o 26 AWG, "
  "com 0,405 mm de diâmetro e apenas 0,001287 cm² de cobre, de modo que um enrolamento que "
  "precise conduzir 8 A a 400 A/cm² exige dezessete desses fios em paralelo. A solução "
  "industrial é o fio Litz, e na sua falta a prática de bancada recomenda vários fios em "
  "paralelo levemente torcidos [2]. Convém registrar que fios simplesmente paralelos ficam "
  "sujeitos ao efeito de proximidade, atenuado pelo intercalamento dos enrolamentos.")

h2("Dedução do produto de áreas")
p("O critério que dimensiona o núcleo decorre de três pontos de partida. O primeiro é a lei de "
  "Faraday na forma da Eq. (18). O segundo é a condição de ocupação plena da janela, em que a "
  "área disponível multiplicada pelo fator de utilização iguala a soma das áreas de cobre dos "
  "dois enrolamentos. O terceiro é a definição de densidade de corrente. Substituindo o terceiro "
  "no segundo e depois o primeiro no resultado, e reconhecendo a potência total processada como "
  "a soma das potências de entrada e de saída, chega-se a [2]")
eq(r"A_{p} = A_{e}A_{w} = \frac{P_{t}\,10^{4}}"
   r"{K_{u}\,K_{f}\,J\,B_{ac}\,f_{s}}\ \mathrm{[cm^{4}]}", "22")
p("A leitura física do resultado é elegante. Aparece o produto das duas áreas, e não cada uma "
  "isoladamente, porque a seção do núcleo determina quanta tensão o núcleo suporta por espira e a "
  "área da janela determina quanta corrente cabe no enrolamento. A potência é o produto dos dois "
  "efeitos. O projeto passa a ser um exercício de equilíbrio entre perda no núcleo, que cresce "
  "com a densidade de fluxo elevada a 2,4, e perda no cobre, que cresce com o quadrado da "
  "densidade de corrente, e o ótimo clássico ocorre quando as duas se aproximam.")
p("Há, contudo, uma limitação que o método não revela e que este trabalho encontrou na prática. O "
  "produto de áreas fixa apenas o produto, e não a repartição entre seção e janela. Dois núcleos "
  "com o mesmo produto podem ter geometrias muito diferentes, e se a repartição for desfavorável "
  "o critério é satisfeito mas o enrolamento não cabe. Por isso o roteiro adotado na Seção IX "
  "trata a verificação da ocupação da janela como restrição durante o dimensionamento, e não "
  "como constatação posterior.")

# =====================================================================
h1("Projeto do Transformador")
h2("Especificações e hipóteses")
fig("fig12-full-bridge",
    "Conversor CC-CC em ponte completa de 500 W e formas de onda no transformador. A tensão "
    "aplicada ao primário é uma onda quadrada alternada de razão cíclica D por diagonal, e a "
    "densidade de fluxo é a sua integral.", 2)
p("O enunciado do trabalho fixa apenas que a frequência é alta e que o núcleo é de ferrite "
  "Thornton. Todo o restante é escolha de projeto. Adotou-se deliberadamente o mesmo ponto de "
  "operação do exemplo resolvido na Seção 1.6.5 do material de referência [2], um conversor CC-CC "
  "em ponte completa de 400 V para 54 V e 500 W em 100 kHz, cuja topologia e formas de onda estão "
  "na Fig. 12. A razão é metodológica: com o ponto de operação idêntico, a única variável entre "
  "este trabalho e o material de referência passa a ser o núcleo, o que permite confrontar "
  "diretamente os resultados.")
tab("Especificações e Escolhas de Projeto",
    [["Parâmetro", "Símbolo", "Valor"],
     ["Tensão de entrada", "V_in", "400 V"],
     ["Tensão de saída", "V_o", "54 V"],
     ["Potência de saída", "P_o", "500 W"],
     ["Frequência de comutação", "f_s", "100 kHz"],
     ["Razão cíclica nominal por diagonal", "D", "0,40"],
     ["Razão cíclica máxima admitida", "D_max", "0,45"],
     ["Rendimento admitido do transformador", "η", "98 %"],
     ["Fator de forma de onda", "K_f", "4,00"],
     ["Fator de utilização da janela", "K_u", "0,40"],
     ["Densidade de corrente", "J", "400 A/cm²"],
     ["Densidade de fluxo, amplitude", "B_ac", "0,07 T"],
     ["Temperatura ambiente", "T_a", "40 °C"],
     ["Elevação de temperatura admitida", "ΔT", "≤ 40 °C"]],
    [0.52, 0.16, 0.32])
p("As hipóteses adotadas são as usuais. Despreza-se a ondulação de corrente no indutor de saída, "
  "de modo que as correntes são tratadas como retangulares de topo plano, com erro inferior a "
  "1 % sobre o valor eficaz. Despreza-se a corrente de magnetização frente à corrente refletida "
  "da carga, hipótese verificada adiante. Despreza-se a indutância de dispersão no cálculo "
  "magnético, tratando-a como recomendação construtiva. As resistências dos enrolamentos são "
  "avaliadas em corrente contínua mas com a resistividade corrigida para 100 °C. E admite-se "
  "queda direta de 0,70 V por diodo no retificador de saída, valor compatível com Schottky de "
  "baixa tensão em temperatura de operação.")
p("A escolha da densidade de fluxo merece justificativa, por ser o parâmetro que mais influencia "
  "o resultado. O limite superior absoluto é a saturação, que não restringe o projeto. O limite "
  "prático é a perda no núcleo, que pelo critério de 100 mW/cm³ admite até 0,161 T de excursão em "
  "100 kHz. O valor adotado, 0,07 T de amplitude, decorre da varredura da Fig. 13, discutida "
  "adiante.")

h2("Dimensionamento passo a passo")
p("O núcleo precisa acomodar os dois enrolamentos e por isso é dimensionado pela soma das "
  "potências de entrada e de saída, e não apenas pela de saída. Com rendimento admitido de 98 %, "
  "a potência total processada vale 1010,20 W. Aplicando a Eq. (22) com os valores da Tabela III,")
eq(r"\begin{gathered} A_{p} = \frac{1010{,}20 \times 10^{4}}{0{,}40 \times 4{,}0 \times 400 "
   r"\times 0{,}07 \times 10^{5}} \\ A_{p} = 2{,}255\ \mathrm{cm^{4}} \end{gathered}", "23")
tab("Núcleos Thornton NEE Considerados",
    [["Núcleo", "A_e (cm²)", "A_w (cm²)", "A_eA_w (cm⁴)", "l_t (cm)", "V_e (cm³)", "massa (g)"],
     ["NEE-30/15/14", "1,22", "0,85", "1,037", "6,7", "8,17", "42,0"],
     ["NEE-42/21/15", "1,81", "1,57", "2,842", "8,7", "17,60", "88,0"],
     ["NEE-42/21/20", "2,40", "1,57", "3,768", "10,5", "23,30", "112,0"],
     ["NEE-55/28/21", "3,54", "2,50", "8,850", "11,6", "42,50", "218,0"],
     ["NEE-65/33/26", "5,32", "3,70", "19,684", "14,8", "78,20", "387,0"]],
    [0.22, 0.13, 0.13, 0.15, 0.12, 0.13, 0.12], span=2,
    note="Área da janela e comprimento médio de espira referidos ao carretel. Massa do par de "
         "peças. Fonte: catálogo do fabricante [9], [10].")
p("Da Tabela IV, adota-se o núcleo NEE-42/21/20, com produto de áreas de 3,768 cm⁴, ou 67 % de "
  "folga sobre o requerido. O número de espiras do primário resulta da Eq. (18) e vale 59,52, "
  "arredondado para cima em 60 espiras, já que mais espiras significam menor excursão de fluxo e "
  "portanto mais margem contra saturação. A verificação pela Eq. (19) dá excursão de 0,1140 T na "
  "razão cíclica de operação e 0,1389 T no pior caso, o que corresponde a um pico de 0,069 T e "
  "deixa margem de saturação superior a quatro vezes.")
p("A relação de transformação decorre da tensão média retificada na saída, incluindo a queda do "
  "retificador. O valor calculado de 10,26 espiras é arredondado para 10, resultando na relação "
  "de 6 para 1 e elevando a razão cíclica necessária para 0,4103. A margem até o limite de "
  "projeto é de 8,8 %, o que significa que o conversor tolera queda de aproximadamente 9 % na "
  "tensão de barramento antes de perder a regulação.")
p("As correntes eficazes valem 1,4081 A no primário e 8,3872 A no secundário. A profundidade de "
  "penetração em 100 kHz limita o condutor a 0,419 mm, o que seleciona o fio 26 AWG. Dividindo as "
  "seções necessárias pela seção de cobre desse fio resultam 3 condutores em paralelo no primário "
  "e 17 no secundário, com densidades de corrente realizadas de 364,7 e 383,3 A/cm².")
p("A verificação da ocupação da janela fecha o dimensionamento. As parcelas valem 0,1838 para o "
  "primário e 0,1736 para o secundário, somando 0,3574 contra o limite de 0,40, com 11 % de "
  "folga. O equilíbrio entre as duas parcelas é a assinatura de um projeto bem balanceado, e é "
  "exatamente o que a dedução do produto de áreas prevê quando as duas metades processam a mesma "
  "potência.")
p("Registre-se ainda a escolha da configuração do retificador de saída, que afeta o projeto "
  "magnético. A derivação central conduz corrente eficaz menor em cada enrolamento, porque cada "
  "metade opera em um semiciclo, mas exige dois enrolamentos completos. O saldo é desfavorável, "
  "pois a ocupação da janela subiria para 0,4288 e excederia o limite. Adota-se portanto o "
  "retificador em ponte completa no secundário, registrando o custo de dois diodos em série no "
  "caminho da corrente.")

h2("A iteração de núcleo")
fig("fig13-varredura-bac",
    "Varredura da densidade de fluxo para o núcleo NEE-42/21/20. O mínimo de perda total ocorre "
    "em 60 mT, mas nessa condição o enrolamento não cabe na janela. O valor adotado é o menor "
    "que satisfaz as três restrições simultaneamente.")
p("Esta seção documenta a tentativa que falhou, porque ela expõe a limitação mais importante do "
  "método. O projeto começou seguindo literalmente o exemplo de referência, com amplitude de "
  "0,05 T. O critério do produto de áreas exigia 3,157 cm⁴ e o núcleo escolhido oferecia "
  "3,768 cm⁴, com 19 % de folga. O número de espiras resultava em 84 no primário e 14 no "
  "secundário, e a verificação da janela dava ocupação de 0,5003, ou 125 % do espaço útil "
  "disponível. O núcleo satisfazia o critério e mesmo assim o transformador não podia ser "
  "construído.")
p("A causa está na repartição das áreas. O núcleo adotado tem razão entre seção e janela igual a "
  "1,53, sendo portanto de seção grande e janela pequena, pensado para aplicações em que a "
  "limitação é o fluxo e não o cobre. Com densidade de fluxo baixa o número de espiras é alto e a "
  "limitação passa a ser o cobre, situação que o critério do produto de áreas não enxerga. Vale "
  "notar que o exemplo do próprio material de referência termina com ocupação de 0,24, muito "
  "abaixo do valor adotado, e conclui que seria possível usar um núcleo menor. É o mesmo fenômeno "
  "com o sinal invertido.")
p("A Fig. 13 mostra o campo de escolha. O mínimo de perda total ocorre em torno de 60 mT, "
  "inatingível por falta de janela. O valor adotado de 70 mT é o menor que satisfaz "
  "simultaneamente o produto de áreas, a ocupação da janela e a elevação de temperatura, mantendo "
  "a perda total a 3,5 % do mínimo teórico. A formulação correta do método passa a ser que o "
  "produto de áreas fornece o menor núcleo possível e a verificação da ocupação fornece o menor "
  "núcleo viável, prevalecendo a segunda quando as duas discordam.")

h2("Verificação de perdas e comportamento térmico")
fig("fig14-bobinagem",
    "Corte da janela do núcleo com a sequência de bobinagem intercalada, adotada para reduzir o "
    "efeito de proximidade e a indutância de dispersão.")
p("A bobinagem intercalada da Fig. 14 foi adotada para reduzir o efeito de proximidade. "
  "A resistividade do cobre corrigida para 100 °C vale 2,266 µΩ·cm, ou 31,4 % acima do valor "
  "tabelado a 20 °C. Com o comprimento médio de espira do carretel, as resistências resultam em "
  "369,75 mΩ no primário e 10,87 mΩ no secundário. A razão entre elas, 34,0, é próxima do "
  "quadrado da relação de transformação, como deve ser em enrolamentos igualmente bem projetados. "
  "As perdas correspondentes valem 0,7332 W e 0,7650 W, praticamente iguais.")
eq(r"P_{cu} = R_{p}I_{p(rms)}^{2} + R_{s}I_{s(rms)}^{2} = 1{,}4981\ \mathrm{W}", "24")
p("As perdas no núcleo, pela Eq. (20) com a excursão de operação, valem 1,0154 W, o que "
  "corresponde a 43,6 mW/cm³ e confirma o critério de projeto com folga. No pior caso de razão "
  "cíclica a densidade sobe para 70,1 mW/cm³, ainda 30 % abaixo do limite. As duas parcelas do "
  "mecanismo, histerese e correntes parasitas, contribuem com 0,5081 W cada, como previsto para "
  "100 kHz.")
p("A perda total de 2,5135 W corresponde a rendimento de 99,50 % no transformador, repartida em "
  "59,6 % no cobre e 40,4 % no núcleo, próxima do ótimo teórico. Convém observar que o rendimento "
  "obtido supera a hipótese de 98 % adotada no dimensionamento, o que é a direção segura do erro, "
  "pois a hipótese conservadora apenas superdimensionou o núcleo em 1,5 %.")
p("A elevação de temperatura segue a expressão de resistência térmica em função do produto de "
  "áreas [5]:")
eq(r"\begin{gathered} R_{t} = 23\,(A_{e}A_{w})^{-0{,}37} = 14{,}08\ ^{\circ}\mathrm{C/W} \\ "
   r"\Delta T = R_{t}P_{\Sigma} = 35{,}4\ ^{\circ}\mathrm{C} \end{gathered}", "25")
p("O resultado atende ao critério de 40 °C com 4,6 °C de folga, situando o núcleo em 75,4 °C. "
  "Dois cenários adversos foram verificados. No pior caso de razão cíclica a elevação sobe para "
  "44,1 °C, e admitindo fator de resistência alternada de 1,4 por efeito de proximidade ela sobe "
  "para 43,8 °C. Ambos levam o componente a cerca de 84 °C, ainda perfeitamente seguro para o "
  "material, cuja temperatura de Curie supera 210 °C, e próximo do ponto de mínima perda dos "
  "ferrites de potência. Somente a combinação dos dois cenários exigiria ventilação forçada.")
p("A última verificação trata da magnetização. Com a permeabilidade inicial do material e a "
  "geometria do núcleo, o fator de indutância vale 6529 nH por espira ao quadrado e a indutância "
  "de magnetização 23,51 mH. A corrente de magnetização de pico resulta em 69,8 mA, ou 4,5 % do "
  "patamar de corrente refletida, o que confirma a hipótese adotada. Vale registrar que a "
  "densidade de fluxo calculada a partir dessa corrente coincide com a obtida por Faraday, o que "
  "constitui verificação cruzada de todo o encadeamento de cálculo.")
tab("Resumo do Projeto e Verificação dos Critérios",
    [["Grandeza", "Obtido", "Critério"],
     ["Núcleo", "NEE-42/21/20, IP12R", "Thornton"],
     ["Espiras primário e secundário", "60 e 10 (6:1)", "—"],
     ["Condutor", "26 AWG, 3 e 17 fios", "≤ 2ε = 0,419 mm"],
     ["Produto de áreas", "3,768 cm⁴", "≥ 2,255 cm⁴"],
     ["Excursão de fluxo, operação", "0,1140 T", "—"],
     ["Excursão de fluxo, pior caso", "0,1389 T", "margem 4,7×"],
     ["Razão cíclica requerida", "0,4103", "≤ 0,45"],
     ["Ocupação da janela", "0,3574", "≤ 0,40"],
     ["Densidade de perdas no núcleo", "43,6 mW/cm³", "≤ 100 mW/cm³"],
     ["Perda no cobre", "1,4981 W", "—"],
     ["Perda no núcleo", "1,0154 W", "—"],
     ["Perda total", "2,5135 W", "—"],
     ["Elevação de temperatura", "35,4 °C", "≤ 40 °C"],
     ["Rendimento do transformador", "99,50 %", "—"],
     ["Regulação", "0,30 %", "≤ 0,5 %"],
     ["Corrente de magnetização", "69,8 mA (4,5 %)", "≤ 10 %"]],
    [0.44, 0.30, 0.26])
p("A Tabela V reúne o projeto fechado e a verificação dos critérios de aceitação. Todos são "
  "atendidos, e o mais apertado é a ocupação da janela, com 89 % do espaço útil consumido, "
  "consequência direta da opção por adotar o menor núcleo viável.")

# =====================================================================
h1("Aplicação Integrada")
p("O transformador projetado pertence a um conversor em ponte completa, e as expressões da "
  "primeira parte permitem calcular as perdas dos seus semicondutores. Adotam-se quatro MOSFETs "
  "SPW20N60C3 no primário, com 650 V sobre barramento de 400 V, e retificador de saída com "
  "diodos Schottky MBR20200CT, com tensão reversa de pico de 66,7 V e margem de três vezes.")
p("Cada chave conduz durante a razão cíclica de operação com patamar de 1,5546 A, o que dá "
  "corrente eficaz de 0,9957 A. Com a resistência de canal corrigida para 100 °C, a perda de "
  "condução vale 0,2826 W. Aplicando a Eq. (6) com os tempos de catálogo, a perda de cruzamento "
  "vale 0,3544 W. A parcela capacitiva da Eq. (7), adotando 50 pF de capacitância equivalente de "
  "energia em 400 V, acrescenta 0,400 W. O total por chave é de 1,0370 W, ou 4,148 W nas quatro.")
p("O resultado merece destaque, pois a parcela capacitiva responde sozinha por 39 % da perda de "
  "cada chave, mais que a condução, que responde por 27 %, e mais que o cruzamento de tensão e "
  "corrente, que responde por 34 %. Este é exatamente o regime de alta tensão, baixa corrente e "
  "alta frequência em que o modelo linear de comutação, isoladamente, dá resposta incompleta. "
  "Registre-se também que a incerteza sobre a capacitância equivalente é a maior de todo o "
  "balanço, pois entre 50 e 150 pF a perda total das quatro chaves varia de 4,15 W a 7,35 W.")
fig("fig15-reparticao-perdas",
    "Repartição das perdas do conversor completo nas duas configurações de retificador de saída. "
    "O retificador domina o balanço em ambos os casos.")
p("No retificador de saída, com queda de 0,66 V por diodo a 125 °C e dois diodos em série, a "
  "perda vale 12,222 W. O balanço final, resumido na Fig. 15, soma 18,884 W, dos quais 22,0 % "
  "nas chaves do primário, "
  "64,7 % no retificador de saída e 13,3 % no transformador, resultando em rendimento estimado de "
  "96,36 % para o conjunto.")
p("Três leituras se impõem. A primeira é que o retificador de saída domina, respondendo por quase "
  "dois terços da perda de semicondutor e por 2,4 % da potência de saída. A causa é estrutural, "
  "pois a saída é de baixa tensão e alta corrente, e a queda de cada Schottky representa 1,2 % da "
  "tensão de saída. Em fontes de baixa tensão o retificador de saída é sempre o gargalo de "
  "rendimento, e é por isso que fontes comerciais acima de algumas centenas de watts usam "
  "retificação síncrona. Com resistência de canal de 5 mΩ, a queda cairia de 660 mV para 46 mV e "
  "a perda de 12,2 W para 0,86 W.")
p("A segunda leitura é que a escolha feita no projeto magnético tem custo mensurável. Adotar a "
  "ponte no secundário, para caber no núcleo menor, custa 6,1 W ou 1,15 ponto percentual de "
  "rendimento, e economiza 106 g de ferrite. O projeto magnético e o projeto do retificador estão "
  "acoplados, e a decisão correta depende de qual restrição pesa mais na aplicação.")
p("A terceira leitura diz respeito à hipótese que abriu o dimensionamento. O rendimento de 98 % "
  "adotado é o do transformador, e o projeto entregou 99,50 %, confirmando que a hipótese era "
  "conservadora e portanto segura. O rendimento do conversor, 96,4 %, é grandeza distinta e não "
  "deve ser confundida com aquela. Essa distinção é a fonte de erro mais comum na aplicação do "
  "método, pois usar o rendimento do conversor completo no cálculo da potência total "
  "superdimensionaria o núcleo sem necessidade.")

# =====================================================================
h1("Conclusão")
p("O trabalho reuniu as expressões de perdas dos quatro dispositivos semicondutores de potência "
  "de uso corrente e as aplicou, junto com o método do produto de áreas, ao projeto de um "
  "transformador de alta frequência com núcleo de ferrite nacional.")
p("Da primeira parte destacam-se três resultados. A frequência é a variável que organiza toda a "
  "escolha de dispositivos, e a fração de comutação na perda total cresce de praticamente zero em "
  "60 Hz a mais de 70 % em 50 kHz. O tipo de carga muda o resultado do cálculo de comutação por "
  "um fator 3,6, de modo que aplicar o modelo de carga resistiva a um conversor com diodo de roda "
  "livre subestima grosseiramente a perda. E a correção térmica dos parâmetros de catálogo não é "
  "refinamento, e sim requisito, porque a resistência de canal de um MOSFET de 500 V cresce 45 % "
  "entre 25 °C e 100 °C e a resistividade do cobre cresce 31 % no mesmo intervalo, com os dois "
  "erros apontando no sentido de subestimar a perda.")
p("Da segunda parte destacam-se outros três. O critério do produto de áreas é necessário mas não "
  "suficiente, pois fixa o produto e não a repartição entre seção e janela, e a primeira "
  "tentativa deste projeto o satisfazia com 19 % de folga e ainda assim exigiria 125 % da janela "
  "disponível. Em alta frequência quem limita a densidade de fluxo é a perda no núcleo, e não a "
  "saturação, com o projeto operando cinco vezes abaixo do joelho da curva de magnetização. E o "
  "ótimo de projeto não é o mínimo de perda, e sim o mínimo de perda compatível com a execução "
  "física, situação em que as duas parcelas de perda ficam próximas de se equilibrar.")
p("O transformador projetado, sobre núcleo NEE-42/21/20 de material IP12R com 60 e 10 espiras em "
  "fio 26 AWG, dissipa 2,514 W, eleva-se 35,4 °C sobre o ambiente e atinge rendimento de 99,50 %, "
  "atendendo aos nove critérios de aceitação verificados. Aplicando as expressões da primeira "
  "parte ao conversor completo, o rendimento estimado é de 96,4 %, com o retificador de saída "
  "respondendo por 65 % das perdas de semicondutor, o que aponta a retificação síncrona como o "
  "próximo passo natural de otimização.")
p("Como limitações, registram-se que a resistência em corrente alternada dos enrolamentos foi "
  "tratada por recomendação construtiva e não por cálculo de Dowell, que a indutância de "
  "dispersão foi especificada como critério de ensaio e não calculada, que a capacitância "
  "equivalente de energia do MOSFET foi estimada e constitui a maior incerteza do balanço, e que "
  "todos os resultados são analíticos, sem verificação experimental ou por simulação.")

# =====================================================================
REFS = [
 "R. P. Torrico Bascopé, Eletrônica Industrial, Unidade I: Dispositivos de Eletrônica de "
 "Potência. Notas de aula, Universidade Federal do Ceará, Fortaleza, 2025.",
 "R. P. Torrico Bascopé, Transformadores e Indutores de Baixa e Alta Frequência. Apostila 01, "
 "Universidade Federal do Ceará, Fortaleza, 2015.",
 "L. Umanand, Power Electronics: Essentials and Applications, cap. 1: Power Semiconductor "
 "Switches. Nova Delhi: Wiley India, 2009.",
 "C. W. T. McLyman, Transformer and Inductor Design Handbook, 3rd ed. Nova York: Marcel Dekker, "
 "2004.",
 "I. Barbi, Projeto de Fontes Chaveadas, 3. ed. Florianópolis: Edição do Autor, 2007.",
 "R. L. Boylestad e L. Nashelsky, Dispositivos Eletrônicos e Teoria de Circuitos, 11. ed. São "
 "Paulo: Pearson, 2013.",
 "C. A. Petry, Especificação de Semicondutores e Cálculo Térmico, cap. 4 de Eletrônica de "
 "Potência. Florianópolis, 2013, revisado em 2020.",
 "M. K. Kazimierczuk, High-Frequency Magnetic Components, 2nd ed. Chichester: John Wiley and "
 "Sons, 2014.",
 "Thornton Eletrônica Ltda., Catálogo de Ferrite. Vinhedo, SP. Disponível em "
 "www.thornton.com.br.",
 "Thornton Eletrônica Ltda., Product Catalog (versão em inglês). Vinhedo, SP. Disponível "
 "em www.thornton.com.br.",
 "Semikron, SEMIPACK 1 Rectifier Diode Modules SKKD 46 e SKKD 81, folha de dados, 2007.",
 "Littelfuse/IXYS, DSEI2x31-06C Fast Recovery Epitaxial Diode, folha de dados, 2019.",
 "STMicroelectronics, TN2540, TXN625, TYN625, TYN825, TYN1225 SCRs, folha de dados, 2011.",
 "STMicroelectronics, BTA41-600B 4Q Triac, folha de dados, 2017.",
 "Vishay Siliconix, IRFP460A e SiHFP460 Power MOSFET, folha de dados, 2022.",
 "Infineon Technologies, SPW20N60C3 CoolMOS Power Transistor, folha de dados, 2002.",
 "International Rectifier, IRG4PC40UD Insulated Gate Bipolar Transistor with Ultrafast Soft "
 "Recovery Diode, folha de dados, 2003.",
 "ON Semiconductor, MBR20200CT Switch-mode Power Rectifier, folha de dados, 2011.",
]
