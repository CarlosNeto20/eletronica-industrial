# 08. Especificações e Metodologia do Transformador

Este documento fecha as especificações da Parte 2, justifica cada hipótese de projeto e define o
roteiro. É o documento que separa o que foi **dado** do que foi **escolhido**, distinção que o
artigo final precisa deixar clara.

## 1. O que o enunciado fixa e o que o projetista escolhe

O enunciado do trabalho pede "projeto de transformador de alta frequência usando ferrite da
Thornton" e não fornece especificações elétricas. Duas coisas, portanto, estão fixadas:

- **A frequência é alta**, o que exclui aço-silício e impõe ferrite;
- **O fabricante do núcleo é a Thornton**, o que fixa a tabela de núcleos disponíveis e o material.

Todo o resto é escolha de projeto e precisa ser justificado.

### 1.1 Escolha do ponto de operação

Adotou-se deliberadamente o **mesmo ponto de operação do exemplo resolvido na Seção 1.6.5 da
Apostila 01** do professor: conversor CC-CC em ponte completa, 400 V de entrada, 54 V de saída,
500 W, 100 kHz. A razão é metodológica: com o ponto de operação idêntico, a única variável entre
este trabalho e o material de referência é **o núcleo**, com Thornton IP12R no lugar do Magnetics
EE-75. Isso permite confrontar diretamente os resultados e identificar exatamente onde as
diferenças vêm do material e onde vêm do método.

A topologia em ponte completa é, além disso, a escolha natural para 500 W: processamento simétrico
do laço $B$–$H$ (documento 07, Seção 2.4), tensão sobre cada chave igual à do barramento (e não ao
dobro, como no push-pull), e aproveitamento pleno do núcleo.

## 2. Especificações

| Parâmetro | Símbolo | Valor | Origem |
|---|---|---|---|
| Topologia | | Ponte completa (*full-bridge*) | Escolha |
| Tensão de entrada (barramento CC) | $V_{in}$ | 400 V | Escolha |
| Tensão de saída | $V_o$ | 54 V | Escolha |
| Potência ativa de saída | $P_o$ | 500 W | Escolha |
| Corrente de saída | $I_o$ | 9,259 A | $P_o/V_o$ |
| Frequência de comutação | $f_s$ | 100 kHz | Escolha |
| Período de comutação | $T$ | 10 µs | $1/f_s$ |
| Razão cíclica nominal por diagonal | $D$ | 0,40 | Escolha |
| Razão cíclica máxima admitida | $D_{max}$ | 0,45 | Escolha |
| Rendimento admitido do transformador | $\eta$ | 98 % | Escolha |
| Fabricante e material do núcleo | | Thornton, IP12R | Enunciado |
| Fator de forma de onda | $K_f$ | 4,00 | Onda quadrada |
| Fator de utilização da janela | $K_u$ | 0,40 | Escolha |
| Densidade de corrente | $J$ | 400 A/cm² | Escolha |
| Densidade de fluxo (amplitude) | $B_{ac}$ | 0,07 T | Escolha, ver Seção 4 |
| Temperatura ambiente | $T_a$ | 40 °C | Escolha |
| Elevação de temperatura admitida | $\Delta T$ | ≤ 40 °C | Critério |

## 3. Hipóteses de cálculo

**H1. Ondulação de corrente desprezível no indutor de saída.** As correntes de secundário e de
primário são tratadas como retangulares de topo plano. A hipótese é boa para indutor de saída
dimensionado com ondulação de 20 % ou menos, e o erro sobre o valor eficaz é inferior a 1 %.

**H2. Corrente de magnetização desprezível frente à corrente refletida da carga.** Isso permite
tratar o primário como conduzindo apenas a corrente da carga refletida. A hipótese é verificada
quantitativamente no documento 10, Seção 5.

**H3. Indutância de dispersão desprezível no cálculo de fluxo e de corrente.** A dispersão afeta
a comutação (sobretensões, perda de razão cíclica efetiva) mas não o dimensionamento magnético.
Ela é tratada como recomendação construtiva no documento 10.

**H4. Resistência dos enrolamentos avaliada em corrente contínua, a 100 °C.** O efeito de
proximidade eleva $R_{ac}/R_{cc}$ acima de 1 e é tratado por recomendação de construção
(intercalamento), não por cálculo, postura coerente com o nível do material de referência. A
correção da resistividade com a temperatura, porém, **é** feita.

**H5. Queda direta do retificador de saída de 0,70 V por diodo**, valor compatível com Schottky de
baixa tensão em temperatura de operação. Essa queda entra no cálculo da relação de transformação.

**H6. Distribuição uniforme de temperatura no conjunto núcleo-enrolamento.** O modelo de
resistência térmica única é uma simplificação; na prática o ponto quente fica no interior do
enrolamento.

## 4. Justificativa das escolhas de projeto

### 4.1 Densidade de fluxo $B_{ac}$, o parâmetro mais delicado

Esta é a escolha que mais influencia o resultado, e merece desenvolvimento.

**O limite superior absoluto é a saturação.** O IP12R satura em 0,51 T a 23 °C, caindo para a faixa
de 0,33 a 0,38 T a 100 °C. Esse limite não é o que restringe o projeto.

**O limite prático é a perda no núcleo.** Aplicando o critério de 100 mW/cm³ da apostila
(documento 07, Seção 4.4) com a expressão de dois coeficientes:

$$\Delta B^{2{,}4}\left(K_H f_s + K_E f_s^2\right) \le 0{,}1\ \text{W/cm}^3$$

Em $f_s = 100$ kHz, $K_H f_s = 4{,}0$ e $K_E f_s^2 = 4{,}0$, de modo que

$$\Delta B \le \left(\frac{0{,}1}{8{,}0}\right)^{1/2{,}4} = 0{,}161\ \text{T}$$

**A referência da apostila.** O exemplo da Seção 1.6.5 adota $B_{ac} = 0{,}05$ T ($\Delta B = 0{,}1$
T) em 100 kHz, valor extraído da curva de $B$ recomendado da Magnetics. Esse valor é conservador:
corresponde a apenas 32 mW/cm³.

**A escolha deste trabalho: $B_{ac} = 0{,}07$ T** ($\Delta B = 0{,}14$ T no pior caso $D = 0{,}5$).
A justificativa é o **equilíbrio entre perda no núcleo e perda no cobre**, e o argumento é o
seguinte. Aumentar $B_{ac}$ reduz o número de espiras (Faraday), o que reduz a resistência dos
enrolamentos e a perda no cobre; mas aumenta a perda no núcleo com expoente 2,4. Existe, portanto,
um mínimo da soma. A varredura completa, executada no documento 09, dá para o núcleo escolhido:

| $B_{ac}$ | $A_p$ req. | $N_p$ | $K_u$ | $P_{cu}$ | $P_{núcleo}$ | $P_{total}$ | $\Delta T$ | Situação |
|---|---|---|---|---|---|---|---|---|
| 0,04 T | 3,946 cm⁴ | 105 | 0,634 | 2,658 W | 0,248 W | 2,906 W | 40,9 °C | $A_p$ e $K_u$ violados |
| 0,05 T | 3,157 cm⁴ | 84 | 0,500 | 2,097 W | 0,453 W | 2,550 W | 35,9 °C | não cabe na janela |
| 0,06 T | 2,631 cm⁴ | 70 | 0,423 | 1,772 W | 0,656 W | 2,428 W | 34,2 °C | não cabe na janela |
| **0,07 T** | **2,255 cm⁴** | **60** | **0,357** | **1,498 W** | **1,015 W** | **2,514 W** | **35,4 °C** | **adotado** |
| 0,08 T | 1,973 cm⁴ | 53 | 0,319 | 1,336 W | 1,308 W | 2,643 W | 37,2 °C | viável |
| 0,09 T | 1,754 cm⁴ | 47 | 0,283 | 1,186 W | 1,735 W | 2,920 W | 41,1 °C | $\Delta T$ no limite |
| 0,10 T | 1,578 cm⁴ | 42 | 0,250 | 1,049 W | 2,390 W | 3,439 W | 48,4 °C | $\Delta T$ excedido |

Todos os valores são calculados para o núcleo NEE-42/21/20 ($A_eA_w = 3{,}768$ cm⁴), de modo que a
coluna "$A_p$ requerido" é satisfeita a partir de $B_{ac} = 0{,}05$ T.

O mínimo de perda total ocorre em torno de $B_{ac} = 0{,}06$ T, mas nessa condição o enrolamento não
cabe na janela do núcleo. **O valor de 0,07 T é o menor $B_{ac}$ que satisfaz simultaneamente as
três restrições**, que são produto de áreas, ocupação de janela e elevação de temperatura, mantendo
a perda total a 3,5 % do mínimo teórico, e é onde as duas parcelas ficam mais próximas de se
equilibrar (1,50 W de cobre contra 1,02 W de núcleo).

Vale destacar a lição: **o ótimo do projeto não é o mínimo de perda, é o mínimo de perda
compatível com a execução física.**

### 4.2 Densidade de corrente $J = 400$ A/cm²

A apostila usa 250 A/cm² nos seus dois exemplos. McLyman recomenda a faixa de 250 a 500 A/cm²;
Barbi, de 300 a 450 A/cm² para transformadores de alta frequência.

Adotaram-se 400 A/cm² por dois motivos. Primeiro, o produto de áreas requerido é inversamente
proporcional a $J$: com 250 A/cm² o critério exigiria $A_p = 3{,}61$ cm⁴, o que empurraria o
projeto para o NEE-55/28/21, quase o dobro da massa. Segundo, e mais importante, **a densidade de
corrente não é um critério em si; ela é um atalho para limitar a perda no cobre**, e o critério real
é a elevação de temperatura, que é verificada explicitamente no documento 10. Um $J$ mais elevado é
admissível desde que a verificação térmica passe, e ela passa com 35,4 °C contra o limite de 40 °C.

### 4.3 Fator de utilização da janela $K_u = 0{,}40$

Valor padrão de McLyman e da apostila. Ele representa a fração da área geométrica da janela do
carretel efetivamente ocupada por **cobre com isolação**. O restante se perde em:

- espaço entre fios redondos (empacotamento hexagonal ideal ocupa 90,7 %; na prática, 75 a 85 %);
- espessura das paredes do carretel;
- isolação entre camadas e entre enrolamentos (fita de poliéster);
- espaço para os terminais e para a saída dos fios.

Para enrolamentos com muitos fios em paralelo enrolados manualmente, 0,40 é um limite otimista mas
alcançável. O projeto fecha em $K_u = 0{,}357$, com 11 % de folga.

### 4.4 Razão cíclica $D = 0{,}40$ e $D_{max} = 0{,}45$

Numa ponte completa, cada diagonal conduz durante $D\,T$ e a tensão retificada no secundário tem
razão cíclica $2D$. O limite absoluto é $D = 0{,}5$, no qual as duas diagonais se encontram e há
curto de braço.

O valor nominal de 0,40 é o mesmo da apostila e deixa 20 % de margem para o controlador compensar
queda de tensão de entrada e aumento de carga. O limite de projeto $D_{max} = 0{,}45$ reserva
0,05 do período, ou 500 ns em 100 kHz, para o **tempo morto** entre as chaves de um mesmo braço,
folgadamente suficiente para os 100 ns de $t_{d(off)}$ do SPW20N60C3.

**A verificação de fluxo é feita em $D = 0{,}5$**, e não em $D = 0{,}4$, pelo argumento do
documento 07, Seção 3.3: o pior caso de fluxo é o de razão cíclica máxima.

### 4.5 Rendimento $\eta = 98$ %

Este valor entra apenas no cálculo da potência total $P_t = P_o(1/\eta + 1)$, que dimensiona o
núcleo. É o **rendimento do transformador**, e não o do conversor, distinção que o documento 11
trata em detalhe, porque as duas coisas são frequentemente confundidas.

O valor de 98 % é o da apostila e é conservador: o projeto fechado atinge 99,50 %. Sendo
conservador, ele apenas superdimensiona levemente o núcleo, em 1,5 % a mais de $P_t$, o que é
seguro.

### 4.6 Temperatura ambiente $T_a = 40$ °C e $\Delta T \le 40$ °C

$T_a = 40$ °C representa o interior de um gabinete ventilado. O limite de $\Delta T = 40$ °C é o
critério de McLyman citado na apostila, associado à densidade de perdas de 100 mW/cm³. A
temperatura resultante no núcleo, 80 °C, é confortável para o IP12R (Curie acima de 210 °C) e está
próxima do mínimo de perdas do material, que ocorre em torno de 90 °C para ferrites de potência
tipo R.

## 5. A tabela de núcleos Thornton

O catálogo da Thornton fornece, para os núcleos NEE de uso corrente, os dados necessários ao
projeto. A tabela abaixo reúne os que interessam à faixa de potência deste trabalho, com $A_w$ e
$l_t$ referidos ao **carretel**, e não à janela geométrica do núcleo:

| Núcleo | $A_e$ [cm²] | $A_w$ [cm²] | $A_eA_w$ [cm⁴] | $l_t$ (MLT) [cm] | $l_e$ [cm] | $V_e$ [cm³] | massa (2 peças) [g] |
|---|---|---|---|---|---|---|---|
| NEE-20/10/5 | 0,312 | 0,26 | 0,081 | 3,8 | 4,30 | 1,34 | 7,0 |
| NEE-30/15/7 | 0,600 | 0,80 | 0,480 | 5,6 | 6,70 | 4,00 | 20,2 |
| NEE-30/15/14 | 1,220 | 0,85 | 1,037 | 6,7 | 6,70 | 8,17 | 42,0 |
| NEE-42/21/15 | 1,810 | 1,57 | 2,842 | 8,7 | 9,70 | 17,60 | 88,0 |
| **NEE-42/21/20** | **2,400** | **1,57** | **3,768** | **10,5** | **9,70** | **23,30** | **112,0** |
| NEE-55/28/21 | 3,540 | 2,50 | 8,850 | 11,6 | 12,00 | 42,50 | 218,0 |
| NEE-65/33/26 | 5,320 | 3,70 | 19,684 | 14,8 | 14,70 | 78,20 | 387,0 |

Repare na coluna $A_w$: os dois núcleos da família 42/21 têm **a mesma janela**, porque partilham o
carretel; o que muda é a espessura da perna central, e com ela $A_e$, $V_e$, $l_t$ e a massa. Essa
particularidade tem consequência direta no projeto, como o documento 09 mostra.

## 6. Tabela de fios de cobre esmaltado

| AWG | Diâmetro [cm] | $S_{cobre}$ [cm²] | $S_{isolado}$ [cm²] | $\rho_{20}$ [µΩ/cm] | Uso em 100 kHz |
|---|---|---|---|---|---|
| 20 | 0,0812 | 0,005176 | 0,006065 | 333 | não (muito grosso) |
| 22 | 0,0644 | 0,003255 | 0,003857 | 530 | não |
| 24 | 0,0511 | 0,002047 | 0,002514 | 842 | não |
| 25 | 0,0455 | 0,001624 | 0,002002 | 1062 | não |
| **26** | **0,0405** | **0,001287** | **0,001603** | **1340** | **sim, é o limite** |
| 27 | 0,0361 | 0,001021 | 0,001313 | 1689 | sim |
| 28 | 0,0321 | 0,000811 | 0,001057 | 2127 | sim |
| 30 | 0,0255 | 0,000510 | 0,000679 | 3381 | sim |

A resistividade tabelada é a 20 °C ($\rho_{20} = 1{,}724\times10^{-6}$ Ω·cm), convenção de McLyman
e da apostila. A correção para a temperatura de operação é feita no cálculo.

## 7. Roteiro de cálculo adotado

O roteiro segue o dos exemplos da apostila, com quatro acréscimos assinalados:

| Passo | Grandeza | Expressão |
|---|---|---|
| 1 | Potência total | $P_t = P_o(1/\eta + 1)$ |
| 2 | Produto de áreas | $A_p = P_t(10^4)/(K_uK_fJB_{ac}f)$ |
| 3 | Seleção do núcleo | tabela Thornton, $A_eA_w \ge A_p$ |
| 4 | Espiras do primário | $N_p = V_p(10^4)/(K_fB_{ac}fA_e)$ |
| **5** | **Verificação da excursão de fluxo** | $\Delta B = V_{in}D\,T/(N_pA_e)$, em $D$ nominal e em $D=0{,}5$ |
| 6 | Relação e espiras do secundário | $n = (V_o+V_d)/(V_{in}\cdot 2D)$; $N_s = nN_p$ |
| **7** | **Razão cíclica requerida e margem** | $D_{req} = (V_o+V_d)/(2V_{in}n_{real})$ |
| 8 | Correntes eficazes | $I_p = (P_{in}/V_{in})/\sqrt{2D}$; $I_s = I_o\sqrt{2D}$ |
| 9 | Profundidade de penetração e bitola | $\varepsilon = 6{,}62/\sqrt{f}$; $D_{fio} \le 2\varepsilon$ |
| 10 | Fios em paralelo | $n_{fios} = \lceil (I_{rms}/J)/S_{cu} \rceil$ |
| **11** | **Verificação da ocupação da janela** | $K_u = (N_pn_p + N_sn_s)S_{iso}/A_w \le 0{,}40$ |
| 12 | Resistências e perdas no cobre | $R = \rho l_tN/(nS_{cu})$; $P_{cu} = RI_{rms}^2$ |
| 13 | Perdas no núcleo | $P_{fe} = \Delta B^{2{,}4}(K_Hf_s + K_Ef_s^2)V_e$ |
| 14 | Elevação de temperatura | $R_t = 23(A_eA_w)^{-0{,}37}$; $\Delta T = R_tP_\Sigma$ |
| **15** | **Indutância e corrente de magnetização** | $L_m = \mu_0\mu_iN_p^2A_e/l_e$; $I_{mag} = V_{in}DT/L_m$ |

Os passos 5, 7, 11 e 15 são acréscimos a este trabalho. O passo 11 é o mais importante: a apostila
o executa *a posteriori*, apenas para constatar se o núcleo foi bem aproveitado (no exemplo dela,
$K_u = 0{,}24$, subaproveitado); aqui ele é tratado como **restrição** que pode obrigar a iterar a
escolha do núcleo, e de fato obrigou.

---

**Documento anterior:** [07. Fundamentos de magnéticos em alta frequência](07-fundamentos-de-magneticos-em-alta-frequencia.md)
**Próximo documento:** [09. Dimensionamento passo a passo](09-dimensionamento-passo-a-passo.md)
