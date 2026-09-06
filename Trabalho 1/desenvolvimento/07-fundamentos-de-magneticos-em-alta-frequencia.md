# 07. Fundamentos de Magnéticos em Alta Frequência

Este documento estabelece o ferramental da Parte 2: as leis que governam o transformador, os
mecanismos de perda no núcleo e no cobre e, sobretudo, a **dedução** do critério do produto de
áreas, que é o coração do método de projeto adotado. Como no documento 01, nenhum valor numérico do
projeto é calculado aqui.

## 1. Por que alta frequência

O transformador é o mesmo dispositivo desde Faraday, mas o seu tamanho não é. A lei da indução
relaciona a tensão aplicada ao produto de três grandezas: número de espiras, área do núcleo e
**taxa de variação** do fluxo. Para uma dada tensão, aumentar a frequência permite reduzir
proporcionalmente o produto $N \cdot A_e$, isto é, reduzir o volume e a massa.

Em números: um transformador de 500 W em 60 Hz pesa alguns quilogramas e usa lâminas de aço-silício
com $A_e$ da ordem de dezenas de cm². O transformador equivalente em 100 kHz, projetado neste
trabalho, usa um núcleo de ferrite de 2,4 cm² e pesa 112 g. **A razão de massa é superior a vinte
para um.** É esse ganho que justifica a fonte chaveada e toda a complexidade que ela acarreta.

O preço é pago em três moedas: perdas no núcleo que crescem com a frequência elevada a um expoente
próximo de 2, efeito pelicular que impede o uso de condutores grossos, e interferência
eletromagnética. As três aparecem no projeto do documento 09.

## 2. Materiais magnéticos

### 2.1 Por que ferrite, e não aço-silício

Em 60 Hz, as correntes parasitas (Eddy) induzidas no material do núcleo são controladas laminando o
aço e isolando as lâminas entre si. Quanto maior a frequência, mais finas precisariam ser as
lâminas, até um ponto em que a laminação deixa de ser viável, tanto mecânica quanto economicamente.

O ferrite resolve o problema por outro caminho: é um material **cerâmico**, composto de óxidos,
principalmente óxido de ferro, cuja resistividade é milhões de vezes maior que a do aço. Sem
caminho condutor macroscópico, as correntes parasitas praticamente não existem, e o núcleo pode ser
maciço.

Os ferrites moles dividem-se em duas famílias, conforme a apostila do professor:

| Família | Permeabilidade | $B_{sat}$ | Resistividade | Faixa de uso |
|---|---|---|---|---|
| **Manganês-zinco (Mn-Zn)** | Alta (1000–15000) | Alta (0,4–0,5 T) | Moderada | Até ~2 MHz, em **conversores de potência** |
| **Níquel-zinco (Ni-Zn)** | Baixa (10–1000) | Baixa | Muito alta | Acima de 1 MHz, em filtros de EMI e RF |

Transformadores de potência em 100 kHz usam Mn-Zn. O material IP12R da Thornton, adotado neste
projeto, pertence a essa família.

### 2.2 Propriedades do IP12R

Do catálogo da Thornton Eletrônica:

| Propriedade | Valor |
|---|---|
| Permeabilidade inicial $\mu_i$ (23 °C) | 2100 ± 25 % |
| Densidade de fluxo de saturação (15 Oe, 23 °C) | 5100 G = 0,51 T |
| Densidade de fluxo (20 kHz, 80 °C) | 2000 G = 0,20 T |
| Temperatura de Curie | > 210 °C |
| Densidade | 4800 kg/m³ = 4,8 g/cm³ |
| Perdas no núcleo | 20 mW/g |

Duas leituras importantes:

**A saturação cai com a temperatura.** Os 0,51 T medidos a 23 °C caem para a faixa de 0,33 a 0,38 T
a 100 °C, valor típico dos ferrites Mn-Zn de potência, e vão a zero na temperatura de Curie. Um
projeto que use $B$ próximo de 0,5 T saturaria assim que o núcleo aquecesse, e a saturação de um
transformador em ponte completa é catastrófica, porque a
indutância de magnetização desaba e a corrente do primário é limitada apenas pela resistência do
enrolamento e pelas chaves.

**O limite prático não é a saturação, é a perda.** Como a Seção 4 mostra, a densidade de fluxo
utilizável em 100 kHz é da ordem de 0,05 a 0,1 T, ou seja, **cinco a dez vezes abaixo da
saturação**. Quem limita é a dissipação no núcleo, não o joelho da curva $B$–$H$.

### 2.3 Curva de magnetização e laço de histerese

Aplicando a um material ferromagnético uma intensidade de campo $H$ crescente a partir de zero, a
densidade de fluxo $B$ cresce lentamente até um ponto A, depois rapidamente até o **joelho** da
curva (ponto B), e então praticamente estaciona (ponto C, saturação). Na região saturada,

$$\frac{B}{H} = 1\ \text{[gauss/oersted]}$$

isto é, o material passa a se comportar como o ar, pois "a partir do ponto B o enrolamento
comporta-se como se tivesse núcleo de ar", nas palavras da apostila.

Ao percorrer ciclicamente a excitação, o material não volta pelo mesmo caminho: forma-se o **laço
de histerese**, caracterizado pela densidade remanescente $B_r$ (fluxo que permanece com $H = 0$) e
pelo campo coercitivo $H_c$ (campo necessário para anular $B$). **A área fechada do laço é a
energia perdida por ciclo e por unidade de volume.** Multiplicada pela frequência, dá a potência
dissipada por histerese, que é a primeira das duas parcelas de perda no núcleo.

### 2.4 A dinâmica do laço nos conversores isolados

Este ponto é essencial para escolher $\Delta B$, e a apostila o trata explicitamente. Os
conversores isolados dividem-se em dois grupos conforme o modo de excitar o núcleo:

**Processamento assimétrico** (*Forward*): a energia é transferida em apenas um semiciclo; o outro é
usado para desmagnetizar o transformador. A corrente de magnetização é **sempre positiva**, e o laço
percorrido é unipolar, ocupando apenas o primeiro quadrante do plano $B$–$H$. Por isso a razão
cíclica precisa ser menor que 0,5, e por isso a excursão útil de fluxo é aproximadamente metade da
disponível.

**Processamento simétrico** (*Push-pull*, *Half-bridge*, *Full-bridge*): em cada período há duas
transferências de energia à carga, uma em cada semiciclo. A corrente de magnetização é **positiva e
negativa**, e o laço é percorrido simetricamente em torno da origem, ocupando o primeiro e o
terceiro quadrantes.

A consequência quantitativa é direta: **para a mesma excursão total $\Delta B$, o conversor
simétrico aproveita o dobro da capacidade do núcleo**. É por isso que a ponte completa é a
topologia natural acima de algumas centenas de watts, e é por isso que este projeto adota
$B_{ac} = \Delta B/2$ como amplitude em torno de zero.

Há um risco associado: qualquer assimetria entre os dois semiciclos, seja atraso diferente entre as
diagonais ou queda desigual nas chaves, produz uma componente contínua de tensão sobre o primário,
que integra e desloca o ponto médio do laço até a saturação. É o fenômeno do **caminhamento de
fluxo** (*flux walking*), combatido com capacitor de bloqueio CC em série com o primário ou com
controle por modo corrente.

## 3. Lei de Faraday e o número de espiras

### 3.1 A forma geral

A lei da indução, aplicada a um enrolamento de $N$ espiras sobre um núcleo de seção $A_e$:

$$v(t) = N\,A_e\,\frac{dB}{dt}$$

Integrando ao longo do intervalo em que a tensão é aplicada:

$$\Delta B = \frac{1}{N A_e}\int v\,dt$$

**A excursão de fluxo é determinada pelo produto tensão-segundo aplicado, dividido por $N A_e$.**
Toda a escolha do número de espiras decorre desta única equação.

### 3.2 Para onda quadrada: a forma de McLyman

Se a tensão é uma onda quadrada de amplitude $V_p$ ocupando o semiperíodo inteiro, o produto
tensão-segundo em meio período vale $V_p \cdot T/2 = V_p/(2f)$, e a excursão correspondente é
$\Delta B = 2B_{ac}$, com $B_{ac}$ a amplitude em torno de zero. Substituindo:

$$2B_{ac} = \frac{V_p}{2f\,N A_e} \;\Longrightarrow\; V_p = 4\,f\,N\,A_e\,B_{ac}$$

Generalizando com o **fator de forma de onda** $K_f$, e com $A_c$ em cm² (unidade da apostila),
chega-se à expressão usada no material do professor:

$$\boxed{\;N_p = \frac{V_p\,(10^4)}{K_f\,B_{ac}\,f\,A_c}\;}$$

com

| Forma de onda | $K_f$ |
|---|---|
| Quadrada | 4,00 |
| Senoidal | 4,44 |

O valor 4,44 da senoide é simplesmente $2\pi/\sqrt2$, e a razão $4{,}44/4 = 1{,}11$ é o fator de
forma da senoide, o mesmo que aparece em transformadores de 60 Hz.

### 3.3 Para razão cíclica menor que 0,5: a forma de Barbi

Num conversor em ponte completa com razão cíclica $D < 0{,}5$ por diagonal, a tensão só é aplicada
ao primário durante $D\,T$ em cada semiciclo. O produto tensão-segundo é menor, e a expressão
direta a partir da lei de Faraday fica

$$\boxed{\;\Delta B = \frac{V_{in}\,D}{N_p\,A_e\,f_s} \;\Longleftrightarrow\;
N_p = \frac{V_{in}\,D}{\Delta B\,A_e\,f_s}\;}$$

**As duas formas coincidem para $D = 0{,}5$**, com $\Delta B = 2B_{ac}$. A relação entre elas é

$$\frac{N_p^{\text{McLyman}}}{N_p^{\text{Barbi}}} = \frac{0{,}5}{D}$$

de modo que o cálculo por McLyman com $D = 0{,}5$ implícito é o **pior caso**: produz mais espiras
do que o estritamente necessário na razão cíclica nominal, e portanto uma excursão de fluxo menor,
com margem. É essa a postura adotada no documento 09, que dimensiona por McLyman e **verifica** com
Faraday a excursão real e a de pior caso.

Essa distinção não é uma sutileza de notação. Em um conversor com controle em malha fechada, a
razão cíclica sobe quando a tensão de entrada cai ou a carga aumenta. Se o núcleo foi dimensionado
exatamente para $D = 0{,}4$, um transitório que leve $D$ a 0,48 aumenta o fluxo em 20 % e pode
saturar. **O pior caso de fluxo é sempre $D = D_{max}$, e é ele que deve ser verificado.**

## 4. Perdas no núcleo

### 4.1 Os dois mecanismos

**Histerese.** A cada ciclo, a energia correspondente à área do laço $B$–$H$ é convertida em calor.
A potência é proporcional à frequência e à área do laço, que por sua vez cresce com $\Delta B$
elevado a um expoente entre 1,6 e 2,5, dependendo do material.

**Correntes parasitas (Eddy).** O fluxo variável induz tensões no próprio material do núcleo, que
produzem correntes e dissipação por efeito Joule. A potência é proporcional ao quadrado da
frequência e ao quadrado de $\Delta B$. É essa parcela que a alta resistividade do ferrite mantém
sob controle.

### 4.2 As duas formas de expressão

**Forma de Steinmetz (McLyman / Magnetics)**, adotada na apostila:

$$\frac{W}{\text{kg}} = k\,f^{m}\,B^{n}$$

com $k$, $m$ e $n$ tabelados pelo fabricante para cada material. A perda total é
$P_{fe} = (W/\text{kg}) \cdot W_{tfe}$, com $W_{tfe}$ a massa do núcleo. A apostila exemplifica com
o aço-silício M6X: $W/\text{kg} = 0{,}000557\,f^{1{,}68}B^{1{,}86}$.

**Forma de dois coeficientes (Barbi)**, específica para ferrite, que separa explicitamente os dois
mecanismos:

$$\boxed{\;P_{n\acute{u}cleo} = \Delta B^{2{,}4}\left(K_H\,f_s + K_E\,f_s^{2}\right)V_e\;}$$

com $\Delta B$ em tesla, $f_s$ em hertz, $V_e$ o volume efetivo do núcleo em cm³, e os coeficientes
para ferrite $K_H = 4\times10^{-5}$ (histerese) e $K_E = 4\times10^{-10}$ (correntes parasitas). O
resultado sai em watts.

A segunda forma foi adotada neste trabalho por três razões: separa os mecanismos, o que permite ver
qual domina em cada frequência; usa o volume, que o catálogo Thornton fornece diretamente; e está
expressa em $\Delta B$, a grandeza que a lei de Faraday entrega.

### 4.3 Qual mecanismo domina

Igualando as duas parcelas:

$$K_H f = K_E f^2 \;\Longrightarrow\; f = \frac{K_H}{K_E} = \frac{4\times10^{-5}}{4\times10^{-10}}
= 100\ \text{kHz}$$

**Exatamente na frequência deste projeto, histerese e correntes parasitas contribuem igualmente.**
Abaixo de 100 kHz domina a histerese; acima, as correntes parasitas, e a partir daí a perda cresce
com o quadrado da frequência, o que estabelece o limite prático do ferrite Mn-Zn em algumas
centenas de quilohertz.

### 4.4 O critério de 100 mW/cm³

A apostila registra a prática da indústria: as curvas de $B$ recomendado versus frequência
fornecidas pelos fabricantes são traçadas para uma **densidade de perdas de 100 mW/cm³**, valor que
permite uma elevação de temperatura de cerca de 40 °C em núcleos de tamanho médio.

Esse é o critério de projeto adotado no documento 08 para escolher $\Delta B$: em vez de partir de
um valor arbitrário, escolhe-se $\Delta B$ tal que

$$\frac{P_{n\acute{u}cleo}}{V_e} = \Delta B^{2{,}4}\left(K_H f_s + K_E f_s^2\right) \le 100\ \text{mW/cm}^3$$

Em 100 kHz, isso dá $\Delta B \le 0{,}161$ T, bem abaixo da saturação a quente,
confirmando que **é a perda, e não a saturação, que limita o projeto em alta frequência**.

A apostila registra ainda um detalhe do material: a curva de perdas versus temperatura tem mínimo
em torno de 30 °C para o material tipo F e em torno de 90 °C para os tipos P e R. Ferrites de
potência são deliberadamente formulados para dissipar **menos** quando quentes, o que estabiliza
termicamente o componente.

## 5. Perdas no cobre e o efeito pelicular

### 5.1 O fenômeno

Em corrente contínua, a densidade de corrente é uniforme na seção do condutor. Em alta frequência
não é. O fluxo magnético interno ao próprio fio induz correntes de Eddy que **cancelam a corrente
no centro e a reforçam na superfície**. O resultado é que a corrente se concentra numa casca
externa, e a seção efetivamente útil do condutor é muito menor que a geométrica.

### 5.2 A profundidade de penetração

A espessura dessa casca é a **profundidade de penetração** $\varepsilon$. A apostila apresenta, para
o cobre,

$$\varepsilon = \frac{6{,}62}{\sqrt{f}}\ \text{[cm]}$$

e a regra de dimensionamento

$$D_{fio} \le 2\,\varepsilon$$

Barbi usa a variante $\Delta = 7{,}5/\sqrt{f_s}$ cm. A diferença é apenas a temperatura na qual a
resistividade do cobre é avaliada: 6,62 corresponde a 20 °C e 7,5 a aproximadamente 100 °C. Neste
trabalho adota-se a expressão da apostila (6,62), por ser a do material do professor, e o resultado
é o mais conservador dos dois, pois exige fio mais fino.

A tabela da apostila mostra a severidade do efeito:

| Frequência | $\varepsilon$ | Fio máximo |
|---|---|---|
| 60 Hz | 8,53 mm | qualquer |
| 1 kHz | 2,53 mm | ~ 4 AWG |
| 10 kHz | 0,66 mm | ~ 19 AWG |
| 20 kHz | 0,467 mm | ~ 22 AWG |
| **100 kHz** | **0,209 mm** | **~ 26 AWG** |
| 1 MHz | 0,066 mm | ~ 39 AWG |

Em 100 kHz, o fio mais grosso admissível é o 26 AWG, com 0,405 mm de diâmetro e apenas
0,001287 cm² de cobre. Um enrolamento que precise conduzir 8 A a 400 A/cm² exige 0,02 cm², ou
seja, **dezessete desses fios em paralelo**.

### 5.3 Fio Litz e a alternativa prática

A solução industrial é o **fio Litz**: muitos filamentos finos, individualmente esmaltados e
transpostos entre si, de modo que cada filamento ocupe todas as posições ao longo do comprimento e
todos vejam a mesma indutância. Na falta dele, a apostila recomenda a prática de bancada: vários
fios em paralelo, levemente torcidos para manter-se juntos.

Há uma diferença real entre as duas soluções que vale registrar. Fios simplesmente paralelos, sem
transposição, ficam sujeitos ao **efeito de proximidade**: o campo magnético dos condutores
vizinhos produz correntes de Eddy adicionais, e os filamentos das camadas externas conduzem mais
que os das internas. A resistência CA resultante pode ser várias vezes a resistência CC calculada
pela seção total. Duas medidas atenuam o problema:

- **Intercalar os enrolamentos** (primário / secundário / primário), o que reduz o campo máximo na
  janela e, com ele, o efeito de proximidade;
- **Limitar o número de camadas**, preferindo o núcleo com janela mais larga e rasa.

O método de Dowell permite quantificar o fator $F_R = R_{ac}/R_{cc}$ em função do número de
camadas e da razão entre a espessura do condutor e $\varepsilon$. Neste trabalho o cálculo é feito
com $R_{cc}$ e o efeito é tratado qualitativamente, como recomendação de construção, postura
coerente com o nível do material de referência.

### 5.4 A resistência e a perda

Conhecido o comprimento médio de uma espira $l_t$ (MLT, *mean length per turn*), tabelado no
catálogo do núcleo, a resistência de um enrolamento de $N$ espiras com $n$ fios em paralelo de
seção $S_{cu}$ vale

$$R = \frac{\rho\,l_t\,N}{n\,S_{cu}}, \qquad P_{cu} = R\,I_{rms}^2$$

com a resistividade do cobre corrigida para a temperatura de operação:

$$\rho(T) = \rho_{20}\left[1 + \alpha(T - 20)\right],
\qquad \rho_{20} = 1{,}724\times10^{-6}\ \Omega\cdot\text{cm},
\qquad \alpha = 0{,}00393\ /^\circ\text{C}$$

A 100 °C, $\rho = 2{,}266\times10^{-6}$ Ω·cm, ou seja, **31 % maior** que a 20 °C. Como no caso da
$R_{DS(on)}$ do MOSFET, ignorar essa correção subestima sistematicamente a perda.

## 6. Dedução do produto de áreas

Este é o passo central do método, e a apostila o desenvolve integralmente. Vale reproduzir a
dedução, porque ela explica por que o critério tem a forma que tem.

**Ponto de partida 1, lei de Faraday.** O número de espiras do primário é

$$N_p = \frac{V_p(10^4)}{A_c\,B_{ac}\,f\,K_f}$$

**Ponto de partida 2, ocupação da janela.** A área da janela é integralmente utilizada quando

$$K_u\,W_a = N_p\,A_{wp} + N_s\,A_{ws}$$

onde $K_u$ é o **fator de utilização da janela**, isto é, a fração da área geométrica efetivamente
ocupada por cobre, tipicamente 0,4, com o restante perdido em isolação, carretel, espaçamentos e
vazios entre fios redondos.

**Ponto de partida 3, densidade de corrente.** Por definição, $A_w = I/J$.

Substituindo 3 em 2:

$$K_u W_a = N_p\left(\frac{I_p}{J}\right) + N_s\left(\frac{I_s}{J}\right)$$

e substituindo 1 (aplicada a ambos os enrolamentos):

$$K_u W_a = \frac{V_p(10^4)}{A_c B_{ac} f K_f}\left(\frac{I_p}{J}\right)
          + \frac{V_s(10^4)}{A_c B_{ac} f K_f}\left(\frac{I_s}{J}\right)$$

Rearranjando, com $A_c$ aparecendo no denominador de ambos os termos:

$$W_a A_c = \frac{\left[(V_pI_p) + (V_sI_s)\right](10^4)}{K_u\,B_{ac}\,f\,J\,K_f}\ \text{[cm}^4\text{]}$$

Reconhecendo $P_{in} = V_pI_p$, $P_o = V_sI_s$ e definindo a **potência total processada**
$P_t = P_{in} + P_o$, chega-se ao resultado:

$$\boxed{\;A_p = W_a A_c = \frac{P_t\,(10^4)}{K_u\,K_f\,J\,B_{ac}\,f}\ \text{[cm}^4\text{]}\;}$$

### 6.1 A leitura física do resultado

O produto de áreas é o único parâmetro geométrico que aparece, e não $A_c$ sozinho, nem $W_a$
sozinho. E a razão é elegante: **$A_c$ determina quanta tensão o núcleo suporta por espira, e $W_a$
determina quanta corrente cabe na janela.** A potência é o produto dos dois, e portanto proporcional
a $A_c W_a$.

Cada grandeza do denominador tem um efeito claro:

| Aumentar... | Efeito sobre $A_p$ | Contrapartida |
|---|---|---|
| $f$ | reduz proporcionalmente | mais perda no núcleo, efeito pelicular pior |
| $B_{ac}$ | reduz proporcionalmente | mais perda no núcleo (com expoente 2,4) |
| $J$ | reduz proporcionalmente | mais perda no cobre (com expoente 2) |
| $K_u$ | reduz proporcionalmente | dificuldade de execução |
| $K_f$ | reduz proporcionalmente | fixado pela forma de onda |

O projeto é, portanto, um exercício de **equilíbrio entre perda no núcleo e perda no cobre**, e o
ótimo clássico ocorre quando as duas se aproximam. O documento 08 usa esse critério explicitamente.

### 6.2 A limitação do critério, que o método não revela

Há uma armadilha que a apostila não destaca e que este trabalho encontrou na prática (documento 09):
**o produto de áreas fixa apenas o produto, não a repartição entre $A_e$ e $A_w$.** Dois núcleos com
o mesmo $A_p$ podem ter geometrias muito diferentes, um com núcleo grosso e janela pequena, outro
com núcleo fino e janela grande.

O núcleo de seção grande exige menos espiras (Faraday), mas cada espira é mais comprida; o de
janela grande acomoda mais cobre. Se a repartição for desfavorável, o critério $A_p$ é satisfeito
mas **o enrolamento não cabe na janela**. Por isso o roteiro do documento 08 inclui uma verificação
explícita de $K_u$ *a posteriori*, e o documento 09 documenta a iteração de núcleo que ela impôs.

## 7. Regulação e o coeficiente de geometria

A apostila apresenta um critério alternativo de escolha de núcleo, baseado na regulação de tensão:

$$\alpha = \frac{V_o(\text{vazio}) - V_o(\text{plena carga})}{V_o(\text{plena carga})}\times 100\ [\%]
\;\approx\; \frac{P_{cu}}{P_o}\times 100$$

e relaciona a regulação à geometria do núcleo por meio de duas constantes:

$$\alpha = \frac{P_t}{2\,K_g\,K_e}\ [\%]$$

com o **coeficiente de geometria do núcleo**

$$K_g = \frac{W_a A_c^2 K_u}{MLT}\ \text{[cm}^5\text{]}$$

e o **coeficiente elétrico**

$$K_e = 0{,}145\,K_f^2\,f^2\,B_m^2\,(10^{-4})$$

Note que $K_g$ depende de $A_c^2$, e não apenas de $A_c$, ao contrário de $A_p$. Isso ocorre porque
a regulação depende da resistência do enrolamento, e portanto do comprimento médio da espira, o que
introduz uma segunda dependência geométrica. Os dois critérios são complementares: **$A_p$
dimensiona pela capacidade de processar potência; $K_g$ dimensiona pela regulação**. Neste trabalho
adota-se $A_p$, seguindo o exemplo da apostila, e a regulação é verificada *a posteriori* no
documento 10.

## 8. Elevação de temperatura

A apostila apresenta o método de McLyman, baseado na densidade superficial de perdas:

$$\psi = \frac{P_\Sigma}{A_t}\ \text{[W/cm}^2\text{]}, \qquad
T_r = 450\,\psi^{\,0{,}826}\ [^\circ\text{C}]$$

com $A_t$ a área de superfície do conjunto montado. Barbi apresenta a forma equivalente, mais
conveniente porque dispensa $A_t$, que o catálogo Thornton não fornece, e usa diretamente o
produto de áreas:

$$\boxed{\;R_t = 23\,(A_e A_w)^{-0{,}37}\ [^\circ\text{C/W}], \qquad
\Delta T = R_t\,P_\Sigma\;}$$

As duas expressões descrevem o mesmo fenômeno: a superfície de troca cresce com o tamanho do
núcleo, e portanto a resistência térmica cai com uma potência fracionária do produto de áreas. A
segunda forma é a adotada no documento 10.

O critério de aceitação é $\Delta T \le 40$ °C, o mesmo que fundamenta a regra dos 100 mW/cm³ da
Seção 4.4, e as duas condições são, na verdade, formulações complementares do mesmo limite térmico.

## 9. Roteiro de projeto

Consolidando, o método do produto de áreas tem quinze passos, que o documento 09 executa:

1. Determinar a potência total $P_t = P_o(1/\eta + 1)$;
2. Calcular o produto de áreas requerido $A_p$;
3. Selecionar o núcleo comercial com $A_eA_w \ge A_p$;
4. Calcular o número de espiras do primário pela lei de Faraday;
5. Verificar a excursão de fluxo real e a de pior caso;
6. Calcular a relação de transformação e o número de espiras do secundário;
7. Recalcular a razão cíclica necessária e verificar a margem;
8. Calcular as correntes eficazes de primário e secundário;
9. Calcular a profundidade de penetração e escolher a bitola do fio;
10. Calcular a seção de cobre necessária e o número de fios em paralelo;
11. **Verificar a ocupação da janela**, e iterar o núcleo se não couber;
12. Calcular as resistências e as perdas no cobre;
13. Calcular as perdas no núcleo;
14. Calcular a elevação de temperatura e verificar o critério;
15. Verificar a indutância de magnetização e a corrente correspondente.

---

**Documento anterior:** [06. Síntese comparativa e cálculo térmico](06-sintese-comparativa-e-calculo-termico.md)
**Próximo documento:** [08. Especificações e metodologia](08-especificacoes-e-metodologia-do-transformador.md)
