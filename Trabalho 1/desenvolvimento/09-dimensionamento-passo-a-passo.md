# 09. Dimensionamento Passo a Passo

Este documento executa o roteiro de quinze passos definido no documento 08. Cada passo traz a
expressão, a substituição numérica e a leitura do resultado. A iteração de núcleo que o passo 11
impôs está documentada integralmente na Seção 11, porque ela é a parte mais instrutiva do projeto.

## Passo 1. Potência total processada

O núcleo precisa acomodar tanto o enrolamento primário quanto o secundário, e portanto é
dimensionado pela **soma** das potências de entrada e de saída, não apenas pela de saída:

$$P_t = P_{in} + P_o = P_o\left(\frac{1}{\eta} + 1\right)$$

$$P_t = 500\left(\frac{1}{0{,}98} + 1\right) = 500 \times 2{,}0204 = 1010{,}20\ \text{W}$$

Para um transformador de um primário e um secundário, essa é a expressão correta da Tabela 7 da
apostila. Configurações com múltiplos enrolamentos usam expressões diferentes: dois secundários,
por exemplo, dão $P_t = P_{in}(1 + \sqrt2)$.

## Passo 2. Produto de áreas requerido

$$A_p = \frac{P_t\,(10^4)}{K_u\,K_f\,J\,B_{ac}\,f}$$

$$A_p = \frac{1010{,}20 \times 10^4}{0{,}40 \times 4{,}0 \times 400 \times 0{,}07 \times 100\times10^3}
= \frac{1{,}0102\times10^7}{4{,}48\times10^6} = 2{,}255\ \text{cm}^4$$

## Passo 3. Seleção do núcleo

Da tabela Thornton (documento 08, Seção 5), os candidatos com $A_eA_w \ge 2{,}255$ cm⁴ são:

| Núcleo | $A_eA_w$ | Folga sobre o requerido | Massa |
|---|---|---|---|
| NEE-42/21/15 | 2,842 cm⁴ | 26 % | 88 g |
| **NEE-42/21/20** | **3,768 cm⁴** | **67 %** | **112 g** |
| NEE-55/28/21 | 8,850 cm⁴ | 292 % | 218 g |

O NEE-42/21/15 satisfaz o critério com folga de 26 %, mas a verificação do passo 11 o reprova por
ocupação de janela (Seção 11). **Adota-se o NEE-42/21/20**, com os parâmetros:

| Grandeza | Símbolo | Valor |
|---|---|---|
| Área efetiva da seção | $A_e$ | 2,40 cm² |
| Área da janela do carretel | $A_w$ | 1,57 cm² |
| Produto de áreas | $A_eA_w$ | 3,768 cm⁴ |
| Comprimento médio de uma espira | $l_t$ | 10,5 cm |
| Comprimento efetivo do caminho magnético | $l_e$ | 9,70 cm |
| Volume efetivo | $V_e$ | 23,30 cm³ |
| Massa (par de peças) | $m$ | 112 g |
| Material | | IP12R |

## Passo 4. Número de espiras do primário

Aplicando a lei de Faraday na forma de McLyman, com $K_f = 4{,}0$ (onda quadrada) e $B_{ac}$ a
amplitude em torno de zero:

$$N_p = \frac{V_{in}\,(10^4)}{K_f\,B_{ac}\,f_s\,A_e}
= \frac{400 \times 10^4}{4{,}0 \times 0{,}07 \times 100\times10^3 \times 2{,}40}
= \frac{4{,}0\times10^6}{6{,}72\times10^4} = 59{,}52$$

$$\boxed{N_p = 60\ \text{espiras}}$$

Arredonda-se **para cima**: mais espiras significam menor excursão de fluxo, portanto mais margem
contra saturação.

## Passo 5. Verificação da excursão de fluxo

Este passo é um acréscimo deste trabalho, pela razão discutida no documento 07, Seção 3.3: a
expressão de McLyman embute $D = 0{,}5$, e a excursão real depende da razão cíclica de operação.
Aplicando a lei de Faraday na forma direta:

$$\Delta B = \frac{V_{in}\,D\,T}{N_p\,A_e}$$

**Na razão cíclica de operação** ($D = 0{,}4103$, valor obtido no passo 7):

$$\Delta B = \frac{400 \times 0{,}4103 \times 10\times10^{-6}}{60 \times 2{,}40\times10^{-4}}
= \frac{1{,}641\times10^{-3}}{1{,}440\times10^{-2}} = 0{,}1140\ \text{T}
\qquad (B_{ac} = 0{,}0570\ \text{T})$$

**No pior caso** ($D = 0{,}5$):

$$\Delta B_{max} = \frac{400 \times 0{,}5 \times 10\times10^{-6}}{60 \times 2{,}40\times10^{-4}}
= 0{,}1389\ \text{T} \qquad (B_{ac} = 0{,}0694\ \text{T})$$

**Verificação contra a saturação.** Mesmo no pior caso, 0,139 T está a mais de 2,4 vezes de
distância dos 0,33 T de saturação do IP12R a 100 °C, considerando que a excursão é simétrica em
torno de zero e o pico vale $\Delta B_{max}/2 = 0{,}069$ T. **Margem de saturação superior a
4,7 vezes**, folgada como convém a um transformador que pode sofrer transitórios de carga.

## Passo 6. Relação de transformação e espiras do secundário

Num conversor em ponte completa com filtro LC na saída, a tensão média retificada vale

$$V_o = n\,V_{in}\,(2D) - V_d$$

onde $n = N_s/N_p$ e $V_d$ é a queda do retificador de saída. Isolando $n$ com os valores nominais:

$$n = \frac{V_o + V_d}{V_{in}\,(2D)} = \frac{54 + 0{,}70}{400 \times 0{,}80}
= \frac{54{,}70}{320} = 0{,}17094$$

$$N_s = n\,N_p = 0{,}17094 \times 60 = 10{,}26$$

$$\boxed{N_s = 10\ \text{espiras}}$$

A relação real fica

$$n_{real} = \frac{N_s}{N_p} = \frac{10}{60} = 0{,}166667
\qquad\text{isto é, uma relação de } \boxed{6{:}1}$$

Arredondar de 10,26 para 10 (e não para 11) significa **elevar** a razão cíclica necessária, o que
é preferível a reduzi-la: uma razão cíclica maior aproxima o conversor do seu ponto de melhor
aproveitamento do transformador, e o passo 7 verifica que a margem continua adequada.

## Passo 7. Razão cíclica requerida e verificação de margem

Com a relação de transformação arredondada, a razão cíclica que o controlador precisa impor é

$$D_{req} = \frac{V_o + V_d}{2\,V_{in}\,n_{real}}
= \frac{54{,}70}{2 \times 400 \times 0{,}166667} = \frac{54{,}70}{133{,}33} = 0{,}4103$$

**Margem até o limite de projeto** $D_{max} = 0{,}45$:

$$\frac{0{,}45 - 0{,}4103}{0{,}45} = 8{,}8\ \%$$

**Margem até o limite absoluto** $D = 0{,}5$: 17,9 %.

Uma folga de 8,8 % sobre $D_{max}$ significa que o conversor tolera uma queda de aproximadamente 9 %
na tensão de barramento antes de perder a regulação, isto é, de 400 V para cerca de 365 V. Para uma
fonte alimentada por PFC regulado em 400 V, com ondulação de barramento de baixa frequência, é uma
margem adequada. Se a especificação exigisse tolerância maior, o caminho seria reduzir $N_p$ ou
aumentar $N_s$, ao custo de mais fluxo ou mais cobre.

**Tensão de pico no secundário:**

$$V_{s,pk} = V_{in}\,n_{real} = 400 \times 0{,}166667 = 66{,}67\ \text{V}$$

o que fixa a tensão reversa de pico sobre os diodos do retificador:

| Configuração | PIV | Diodos conduzindo | Queda total |
|---|---|---|---|
| Ponte completa no secundário | 66,7 V | 2 | $2V_d$ |
| Secundário com derivação central | 133,3 V | 1 | $V_d$ |

A escolha entre as duas é feita na Seção 10 deste documento, por critério de ocupação da janela.

## Passo 8. Correntes

**Corrente de saída:** $I_o = P_o/V_o = 500/54 = 9{,}259$ A.

**Corrente de entrada:** $P_{in} = P_o/\eta = 500/0{,}98 = 510{,}20$ W, logo o patamar de corrente
no primário durante a condução vale

$$I_{p,patamar} = \frac{P_{in}/V_{in}}{2D_{req}}
= \frac{510{,}20/400}{0{,}8206} = \frac{1{,}2755}{0{,}8206} = 1{,}5546\ \text{A}$$

**Valores eficazes.** A corrente é retangular ocupando a fração $2D$ do período em ambos os
enrolamentos:

$$I_{p(rms)} = I_{p,patamar}\sqrt{2D_{req}} = 1{,}5546\sqrt{0{,}8206} = 1{,}4081\ \text{A}$$

$$I_{s(rms)} = I_o\sqrt{2D_{req}} = 9{,}259\sqrt{0{,}8206} = 8{,}3872\ \text{A}$$

Vale registrar a conferência pela relação de transformação:
$I_{p(rms)}/I_{s(rms)} = 1{,}4081 / 8{,}3872 = 0{,}16789$, contra $n_{real} = 0{,}166667$, com
diferença de apenas 0,73 %. Ela resulta de dois efeitos que
quase se cancelam: o rendimento de 98 % eleva a corrente do primário em 2,04 %, enquanto a queda de
0,70 V do retificador, já embutida na relação de transformação, a reduz em 1,28 %. O produto
$1{,}0204 \times 0{,}9872 = 1{,}0073$ reproduz exatamente o desvio observado.

## Passo 9. Efeito pelicular e escolha da bitola

$$\varepsilon = \frac{6{,}62}{\sqrt{f_s}} = \frac{6{,}62}{\sqrt{100\times10^3}}
= \frac{6{,}62}{316{,}23} = 0{,}02093\ \text{cm} = 0{,}209\ \text{mm}$$

$$D_{fio} \le 2\varepsilon = 0{,}4187\ \text{mm}$$

Consultando a tabela de fios:

| AWG | Diâmetro | $\le 2\varepsilon$? |
|---|---|---|
| 24 | 0,511 mm | não |
| 25 | 0,455 mm | não |
| **26** | **0,405 mm** | **sim, o mais grosso admissível** |
| 27 | 0,361 mm | sim |
| 28 | 0,321 mm | sim |

$$\boxed{\text{Fio adotado: 26 AWG} \quad
S_{cu} = 0{,}001287\ \text{cm}^2, \quad S_{iso} = 0{,}001603\ \text{cm}^2}$$

O 26 AWG é a escolha ótima: qualquer fio mais grosso desperdiça cobre no centro, que não conduz;
qualquer fio mais fino aumenta desnecessariamente o número de condutores em paralelo e piora o
fator de empacotamento.

## Passo 10. Condutores em paralelo

**Primário:**

$$S_{wp} = \frac{I_{p(rms)}}{J} = \frac{1{,}4081}{400} = 0{,}003520\ \text{cm}^2$$
$$n_p = \frac{S_{wp}}{S_{cu}} = \frac{0{,}003520}{0{,}001287} = 2{,}74
\;\Longrightarrow\; \boxed{n_p = 3\ \text{fios}}$$

**Secundário:**

$$S_{ws} = \frac{I_{s(rms)}}{J} = \frac{8{,}3872}{400} = 0{,}020968\ \text{cm}^2$$
$$n_s = \frac{S_{ws}}{S_{cu}} = \frac{0{,}020968}{0{,}001287} = 16{,}29
\;\Longrightarrow\; \boxed{n_s = 17\ \text{fios}}$$

**Densidades de corrente efetivamente realizadas:**

$$J_p = \frac{1{,}4081}{3 \times 0{,}001287} = 364{,}7\ \text{A/cm}^2$$
$$J_s = \frac{8{,}3872}{17 \times 0{,}001287} = 383{,}3\ \text{A/cm}^2$$

Ambas abaixo dos 400 A/cm² adotados, em consequência do arredondamento para cima. O enrolamento
secundário com 17 fios de 26 AWG em paralelo equivale, em seção de cobre, a um único fio de
aproximadamente 14 AWG, mas com resistência CA muitas vezes menor.

## Passo 11. Verificação da ocupação da janela

$$K_{up} = \frac{N_p\,n_p\,S_{iso}}{A_w} = \frac{60 \times 3 \times 0{,}001603}{1{,}57}
= \frac{0{,}28854}{1{,}57} = 0{,}1838$$

$$K_{us} = \frac{N_s\,n_s\,S_{iso}}{A_w} = \frac{10 \times 17 \times 0{,}001603}{1{,}57}
= \frac{0{,}27251}{1{,}57} = 0{,}1736$$

$$\boxed{K_u = K_{up} + K_{us} = 0{,}3574 \le 0{,}40 \quad\checkmark}$$

Equivalentemente, a área de janela mínima necessária é

$$A_{w,min} = \frac{(N_pn_p + N_sn_s)\,S_{iso}}{K_u^{max}}
= \frac{0{,}56105}{0{,}40} = 1{,}403\ \text{cm}^2 \;\le\; 1{,}57\ \text{cm}^2 \quad\checkmark$$

**O enrolamento cabe, com 11 % de folga.** Repare no equilíbrio: primário e secundário ocupam
praticamente a mesma área (0,1838 contra 0,1736), o que é a assinatura de um projeto bem
balanceado, e é exatamente o que a dedução do produto de áreas prevê quando as duas metades
processam a mesma potência.

## Seção 10. A escolha da configuração do secundário

O passo 7 deixou em aberto a escolha entre ponte completa e derivação central no retificador de
saída. A decisão é tomada aqui porque ela afeta a ocupação da janela.

| Configuração | Enrolamentos | $I_{rms}$ por enrolamento | Fios | $K_{us}$ | $K_u$ total | PIV | Queda |
|---|---|---|---|---|---|---|---|
| **Ponte completa** | 1 × 10 esp. | $I_o\sqrt{2D} = 8{,}387$ A | 17 | 0,1736 | **0,3574** | 66,7 V | $2V_d$ |
| Derivação central | 2 × 10 esp. | $I_o\sqrt{D} = 5{,}931$ A | 12 | 0,2450 | 0,4288 | 133,3 V | $V_d$ |

A derivação central conduz corrente eficaz menor em cada enrolamento, porque cada metade opera
apenas em um semiciclo, mas exige **dois** enrolamentos completos, e o saldo é desfavorável:
$K_u = 0{,}4288$ **excede o limite de 0,40 e não cabe na janela do NEE-42/21/20**.

$$\boxed{\text{Adota-se retificador em ponte completa no secundário}}$$

A contrapartida é conhecida e será quantificada no documento 11: a ponte tem dois diodos em série
no caminho da corrente, e portanto o dobro da perda de condução do retificador. Para uma saída de
54 V a queda dupla representa 2,6 % da tensão, contra 1,3 % da derivação central. **O projeto
magnético e o projeto do retificador estão acoplados**, e a escolha aqui privilegia a viabilidade
do magnético, que é o objeto do trabalho, e registra o custo.

Se o requisito de rendimento fosse mais severo, o caminho seria migrar para o NEE-55/28/21
($A_w = 2{,}50$ cm²), no qual a derivação central caberia com $K_u = 0{,}27$, ao custo de 218 g de
núcleo contra 112 g.

## Seção 11. A iteração de núcleo

Esta seção documenta a tentativa que **falhou**, porque ela expõe a limitação mais importante do
método do produto de áreas.

### 11.1 A primeira tentativa

O projeto começou seguindo literalmente o exemplo da apostila, com $B_{ac} = 0{,}05$ T e
$J = 400$ A/cm². O critério do produto de áreas deu

$$A_p = \frac{1010{,}20 \times 10^4}{0{,}40 \times 4{,}0 \times 400 \times 0{,}05 \times 10^5}
= 3{,}157\ \text{cm}^4$$

O NEE-42/21/20, com $A_eA_w = 3{,}768$ cm⁴, satisfazia com 19 % de folga. O número de espiras
resultou

$$N_p = \frac{400 \times 10^4}{4{,}0 \times 0{,}05 \times 10^5 \times 2{,}40} = 83{,}33
\;\Rightarrow\; N_p = 84, \quad N_s = 14$$

e a verificação de janela deu:

$$K_{up} = \frac{84 \times 3 \times 0{,}001603}{1{,}57} = 0{,}2573, \qquad
K_{us} = \frac{14 \times 17 \times 0{,}001603}{1{,}57} = 0{,}2430$$
$$K_u = 0{,}5003 \;\gg\; 0{,}40 \qquad \textbf{reprovado}$$

O enrolamento exigiria uma janela de 1,96 cm² contra os 1,57 cm² disponíveis, ou seja, **125 % do
espaço útil**. O núcleo satisfazia o critério de $A_p$ e mesmo assim o transformador não podia ser
construído.

### 11.2 Por que o critério falhou

A causa está exposta no documento 07, Seção 6.2: **o produto de áreas fixa apenas o produto, não a
repartição.** O NEE-42/21/20 tem $A_e = 2{,}40$ cm² e $A_w = 1{,}57$ cm², uma razão
$A_e/A_w = 1{,}53$. É um núcleo de seção grande e janela pequena, pensado para aplicações em que
a limitação é o fluxo, não o cobre.

Com $B_{ac}$ baixo, o número de espiras é alto, e a limitação passa a ser o cobre. O critério de
$A_p$, que trata as duas áreas como intercambiáveis, não enxerga isso.

Note que o exemplo da própria apostila termina com $K_u = 0{,}24$, muito **abaixo** dos 0,4
adotados, e a apostila conclui: *"já que o fator de utilização da janela do núcleo é 0,24, o mesmo
muito menor que o valor adotado de 0,4, é possível usar um núcleo menor ao escolhido."* É o mesmo
fenômeno, com o sinal invertido: o núcleo Magnetics EE-75 tem janela relativamente grande, e o
projeto sobrou. **Em ambos os casos o critério de $A_p$ acertou o produto e errou a repartição.**

### 11.3 Os três caminhos de correção

| Caminho | Consequência |
|---|---|
| **(a)** Aumentar $B_{ac}$ | Menos espiras, menos cobre, mais perda no núcleo |
| **(b)** Migrar para núcleo de janela maior | Mais massa e volume |
| **(c)** Aumentar $J$ | Menos cobre, mais perda no cobre, verificação térmica mais apertada |

A varredura completa dos caminhos (a) e (b), apresentada no documento 08, Seção 4.1, e reproduzida
abaixo para os candidatos viáveis, mostra o campo de escolha:

| Núcleo | $B_{ac}$ | $N_p$ | $N_s$ | $K_u$ | $P_{total}$ | $\Delta T$ | Massa |
|---|---|---|---|---|---|---|---|
| NEE-55/28/21 | 0,05 T | 57 | 10 | 0,212 | 2,392 W | 24,6 °C | 218 g |
| NEE-55/28/21 | 0,04 T | 71 | 12 | 0,267 | 2,443 W | 25,1 °C | 218 g |
| **NEE-42/21/20** | **0,07 T** | **60** | **10** | **0,357** | **2,514 W** | **35,4 °C** | **112 g** |
| NEE-65/33/26 | 0,04 T | 47 | 8 | 0,120 | 2,533 W | 19,3 °C | 387 g |
| NEE-42/21/15 | 0,09 T | 62 | 11 | 0,370 | 2,565 W | 40,1 °C | 88 g |
| NEE-42/21/20 | 0,08 T | 53 | 9 | 0,319 | 2,643 W | 37,2 °C | 112 g |

**A escolha adotada**, ou seja, NEE-42/21/20 com $B_{ac} = 0{,}07$ T pelo caminho (a), dissipa apenas 5 % mais
que a melhor opção da tabela e usa **metade da massa** do NEE-55/28/21. O NEE-42/21/15, com 88 g,
seria ainda mais leve, mas fecha em $\Delta T = 40{,}1$ °C, exatamente no limite, sem margem.

### 11.4 A lição de método

O roteiro do documento 08 foi escrito **já com o passo 11 dentro**, e não como verificação final,
justamente por causa desta iteração. A formulação correta do método do produto de áreas é:

> $A_p$ fornece o **menor núcleo possível**; a verificação de $K_u$ fornece o **menor núcleo
> viável**. Quando os dois discordam, é a segunda que prevalece.

## Resumo dos parâmetros dimensionados

| Grandeza | Símbolo | Valor |
|---|---|---|
| Núcleo | | Thornton NEE-42/21/20, IP12R |
| Espiras do primário | $N_p$ | 60 |
| Espiras do secundário | $N_s$ | 10 |
| Relação de transformação | $N_p{:}N_s$ | 6:1 |
| Condutor | | 26 AWG |
| Fios em paralelo, primário | $n_p$ | 3 |
| Fios em paralelo, secundário | $n_s$ | 17 |
| Excursão de fluxo em operação | $\Delta B$ | 0,1140 T |
| Excursão de fluxo, pior caso | $\Delta B_{max}$ | 0,1389 T |
| Razão cíclica requerida | $D_{req}$ | 0,4103 |
| Corrente eficaz do primário | $I_{p(rms)}$ | 1,4081 A |
| Corrente eficaz do secundário | $I_{s(rms)}$ | 8,3872 A |
| Ocupação da janela | $K_u$ | 0,3574 |
| Retificador de saída | | Ponte completa, PIV 66,7 V |

---

**Documento anterior:** [08. Especificações e metodologia](08-especificacoes-e-metodologia-do-transformador.md)
**Próximo documento:** [10. Verificação: perdas e térmica](10-verificacao-perdas-e-termica.md)
