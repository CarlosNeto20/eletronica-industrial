# 05. IGBT de Potência

O IGBT existe para resolver o problema exposto no fim do documento anterior: a resistência de canal
do MOSFET cresce com a potência 2,4 a 2,6 da tensão de bloqueio, o que o torna inviável acima de
algumas centenas de volts em correntes elevadas. A solução foi combinar a porta isolada do MOSFET
com a condução por portadores minoritários do transistor bipolar.

## 1. Características básicas

### 1.1 A ideia estrutural

O livro define o IGBT como a combinação das vantagens do MOSFET, que são alta impedância de
entrada, controle por tensão e comutação rápida, com as do BJT, que são baixa perda em condução e
alta capacidade de bloqueio. Os terminais são **coletor** (C), **emissor** (E) e **porta** (G).

Estruturalmente, o IGBT é um MOSFET ao qual se acrescentou uma camada $p$ no lado do coletor. Onde
o MOSFET tem três camadas ($n$–$p$–$n$), o IGBT tem quatro ($p$–$n$–$p$–$n$). Aplicando tensão
positiva na porta, forma-se a mesma camada de inversão do MOSFET, unindo as duas regiões $n$; a
camada $p$ do coletor, junto com esse $n$ equivalente, forma uma junção $p$–$n$ que se comporta
como um diodo.

Daí os dois circuitos equivalentes que os slides apresentam:

- **Diodo em série com MOSFET**, que explica a tensão de limiar em condução e a capacidade de
  bloqueio reverso;
- **PNP acionado por MOSFET**, que explica a condução por portadores minoritários e, com ela, a
  baixa queda em correntes altas.

A **injeção de portadores minoritários** na região de deriva é o mecanismo central. Ela modula a
condutividade dessa região, cancelando o crescimento da resistência com a tensão de bloqueio que
condena o MOSFET. O preço é que esses portadores precisam ser removidos no bloqueio, e é isso que
produz a corrente de cauda.

### 1.2 O tiristor parasita e o travamento

A estrutura de quatro camadas contém, inevitavelmente, um tiristor parasita entre coletor e
emissor. **Se ele travar, a porta perde o controle do dispositivo e o resultado é destrutivo.** Os
fabricantes evitam isso reduzindo drasticamente a resistência $R_s$ do corpo $p$ sob o emissor, de
modo que a queda sobre ela nunca alcance a tensão de condução da junção base-emissor do NPN
parasita. Esse cuidado de fabricação impõe limites de $di/dt$ e de corrente de curto-circuito que
constam das folhas de dados.

Ao contrário do MOSFET, o IGBT **não tem diodo de corpo intrínseco**. Quando um diodo antiparalelo
é necessário, e em cargas indutivas ele sempre é, o fabricante o integra separadamente no mesmo
encapsulamento. Os dispositivos assim construídos são chamados *co-pack*; o IRG4PC40UD usado no
exemplo deste documento é um deles.

### 1.3 As duas famílias: PT e NPT

Os slides destacam a classificação por tecnologia de fabricação:

| Tipo | Nome | Coeficiente de temperatura de $V_{CE(sat)}$ | Paralelismo |
|---|---|---|---|
| **NPT** | *Non-Punch-Through* | Positivo | **Favorável** |
| **PT** | *Punch-Through* | Negativo | **Péssimo** |

O critério é o mesmo do MOSFET: um coeficiente positivo de temperatura faz com que o dispositivo
mais quente conduza menos, redistribuindo a corrente e estabilizando o conjunto. Um coeficiente
negativo faz o contrário e leva à concentração de corrente no dispositivo mais quente. **IGBTs
NPT podem ser paralelados; IGBTs PT, não**, ou apenas com casamento rigoroso e resistores de
equalização.

### 1.4 Características estáticas

A curva $i_C \times V_{CE}$ mostra que o IGBT sustenta tensões diretas e reversas no estado
bloqueado, o que é uma vantagem sobre o MOSFET, cujo diodo de corpo impede o bloqueio reverso. A
curva $i_C \times V_{GE}$ mostra a tensão de limiar $V_{GE(th)}$, abaixo da qual o dispositivo está
desligado.

O livro registra a comparação que define o nicho do dispositivo: para uma dada corrente de coletor,

$$V_{CE(sat)}^{\text{IGBT}} < V_{DS(on)}^{\text{MOSFET comparável}}, \qquad
V_{CE(sat)}^{\text{IGBT}} > V_{CE(sat)}^{\text{BJT comparável}}$$

O IGBT fica entre os dois: conduz melhor que o MOSFET de mesma classe de tensão, pior que o BJT,
mas é comandado por tensão como o primeiro.

### 1.5 Comportamento dinâmico e a corrente de cauda

O livro sintetiza o IGBT em uma frase: *"IGBTs são mais parecidos com BJTs no bloqueio e com
MOSFETs na entrada em condução."*

**Entrada em condução.** Comporta-se como MOSFET. Quando $V_{GE}$ atinge $V_{GE(th)}$, a corrente
de coletor começa a subir. O intervalo entre 10 % de $V_{GE}$ e 10 % de $i_C$ é o atraso
$t_{d(on)}$; até 90 % de $i_C$, o tempo de subida $t_r$. **A maior parte da dissipação de entrada
em condução ocorre nesse intervalo**, e o livro faz duas advertências:

1. Ao fim de $t_{on}$, $V_{CE}$ frequentemente **ainda não caiu** ao valor de saturação, o que
   precisa ser considerado no cálculo;
2. O pico de corrente observado na entrada em condução é a **corrente de recuperação reversa do
   diodo de roda livre**, e essa energia é dissipada no IGBT.

**Bloqueio.** Comporta-se como BJT. Há um atraso $t_{d(off)}$ e um tempo de descida $t_f$, ao fim
do qual, e aqui está a diferença essencial, permanece uma **corrente de cauda** (*tail current*).
Ela é o escoamento dos portadores minoritários que ainda estão na região de deriva e que não podem
ser removidos pela porta: só desaparecem por recombinação.

A corrente de cauda dissipa energia **com a tensão de barramento plena aplicada**. E há um
compromisso de projeto embutido: *quanto menor a $V_{CE(sat)}$, maior a cauda*. Mais injeção de
minoritários significa melhor condução e pior bloqueio. O livro registra a escolha da indústria:
como acima de 10 a 20 kHz as perdas de comutação dominam, a maioria dos IGBTs é projetada para
cauda baixa, aceitando uma $V_{CE(sat)}$ um pouco acima do mínimo possível.

### 1.6 Observações comparativas do livro-texto

Vale reproduzir integralmente, porque são critérios de escolha:

1. O cálculo de perdas do IGBT segue o mesmo procedimento do BJT e do MOSFET;
2. A potência de comando é baixa, como no MOSFET;
3. **A capacidade de sobrecarga é muito superior à do MOSFET**: o pico admissível do MOSFET é de 5
   a 6 vezes a corrente contínua de dreno; o do IGBT chega a 20 vezes a corrente de coletor. Um
   IGBT suporta curto-circuito sobre um barramento de 600 V por cerca de 10 µs;
4. A robustez a sobretensão é **menor** que a do MOSFET;
5. IGBTs são como BJTs no bloqueio e como MOSFETs na entrada em condução;
6. Ao contrário do BJT, a corrente de coletor não é limitada pelo ganho, e sim apenas pela fonte
   externa.

Os itens 3 e 4 juntos descrevem o dispositivo com precisão: **muito tolerante a excesso de
corrente, pouco tolerante a excesso de tensão.** Daí a importância dos *snubbers* de sobretensão e
do controle da indutância parasita do barramento.

## 2. Perdas de condução

### 2.1 A expressão

Em condução o ponto de operação está na região de saturação, e o IGBT é modelado por uma fonte de
tensão constante $V_{CE(sat)}$, cujo valor o fabricante fornece. A expressão dos slides é

$$\boxed{\;P_{cond} = V_{CE(sat)}\,I_{C(av)}\;}$$

O livro chega ao mesmo resultado pela Eq. (1.20) e acrescenta a forma para corrente pulsada de topo
plano, Eq. (1.21):

$$P_{on} = V_{CE(sat)}\,I_C\,D$$

que é a mesma expressão, já que $I_{C(av)} = I_C D$ para pulso retangular.

**Compare com os três dispositivos anteriores.** O IGBT é o único cuja perda de condução depende
*apenas* do valor médio. Diodo e tiristor precisam de média e eficaz; o MOSFET, apenas da eficaz;
o IGBT, apenas da média. Isso decorre da modelagem por fonte de tensão pura.

### 2.2 Refinamento: o modelo de dois parâmetros

O modelo de fonte de tensão pura é o que os slides adotam, e é adequado para uma primeira
estimativa. Ele **subestima** a perda em correntes acima da nominal, porque a característica real
tem inclinação. Quando o catálogo fornece a curva $V_{CE} \times I_C$, ou quando o dispositivo
opera com fator de forma elevado, é preferível o modelo de dois parâmetros, idêntico ao do diodo:

$$P_{cond} = V_{CE0}\,I_{C(av)} + r_{CE}\,I_{C(rms)}^2$$

com $V_{CE0}$ e $r_{CE}$ extraídos por ajuste de reta na faixa de corrente de operação, exatamente
como descrito na Seção 3.2 do documento 02. Neste trabalho, seguindo os slides, adota-se o modelo
de fonte de tensão, com a ressalva registrada.

### 2.3 Correção térmica

A folha de dados do IRG4PC40UD indica que $V_{CE(sat)}$ **decresce** cerca de 0,5 mV/°C entre 25 °C
e 150 °C, coeficiente negativo característico da família PT. Sobre 1,72 V, os 125 °C de variação
representam apenas 62 mV, ou 3,6 %. O efeito é pequeno o bastante para ser desprezado em uma
primeira estimativa, mas o sinal negativo é o que importa: **é ele que desaconselha o paralelismo
de IGBTs PT**, conforme a Seção 1.3.

## 3. Perdas de comutação

### 3.1 O modelo linear dos slides

Idêntico ao do MOSFET, com os tempos de subida e descida da corrente de coletor:

$$P_{ec} = \tfrac{1}{2}\,V_{CE}\,I_C\,(1{,}2\,t_r)\,f_s, \qquad
P_{bloq} = \tfrac{1}{2}\,V_{CE}\,I_C\,(1{,}2\,t_f)\,f_s$$

### 3.2 O modelo por energias de catálogo

Os fabricantes de IGBT, ao contrário dos de MOSFET, quase sempre fornecem diretamente as
**energias de comutação** medidas em bancada:

$$P_{com} = (E_{on} + E_{off})\,f_s$$

Essa é a via preferível, e por uma razão de fundo: $E_{on}$ e $E_{off}$ medidos **incluem os dois
efeitos que o modelo linear ignora**, que são a corrente de cauda no bloqueio e a recuperação
reversa do diodo de roda livre na entrada em condução. O exemplo a seguir mostra o tamanho da
diferença.

Quando o ponto de operação difere do ensaio de catálogo, escala-se aproximadamente por

$$E_{sw}(V, I) \approx E_{sw}^{\text{cat}} \cdot \frac{V}{V^{\text{cat}}} \cdot \frac{I}{I^{\text{cat}}}$$

lembrando que a dependência com a corrente é próxima da linear, e com a tensão, entre linear e
quadrática.

### 3.3 Exemplo 6. Braço de inversor com IRG4PC40UD

**Circuito.** Braço de inversor trifásico, barramento $V_{CC} = 400$ V, corrente de coletor
$I_C = 20$ A, razão cíclica média 0,5, $f_s = 10$ kHz. Carga indutiva com diodo de roda livre
integrado.

**Componente.** IRG4PC40UD, de 600 V e 40 A a 25 °C (20 A a 100 °C), $V_{CE(sat)} = 1{,}72$ V típico
a $I_C = 20$ A e $V_{GE} = 15$ V, $t_r = 57$ ns, $t_f = 80$ ns típico,
$E_{on} = 0{,}71$ mJ, $E_{off} = 0{,}35$ mJ, $E_{ts} = 1{,}10$ mJ (ensaio a 480 V, 20 A,
$R_G = 10$ Ω, $T_j = 25$ °C), $R_{th,jc} = 0{,}77$ °C/W para o IGBT e 1,7 °C/W para o diodo,
$T_{j,max} = 150$ °C.

**Passos 1 e 2, formas de onda e valores característicos.**

$$I_{C(av)} = I_C \, D = 20 \times 0{,}5 = 10{,}0\ \text{A}$$

**Passos 3 e 4, perda de condução.**

$$P_{cond} = 1{,}72 \times 10{,}0 = 17{,}20\ \text{W}$$

**Passo 5, perda de comutação pelos dois caminhos.**

*Modelo linear dos slides:*
$$P_{ec} = \tfrac{1}{2} \times 20 \times 400 \times (1{,}2 \times 57\ \text{ns}) \times 10\ \text{kHz}
= 2{,}736\ \text{W}$$
$$P_{bloq} = \tfrac{1}{2} \times 20 \times 400 \times (1{,}2 \times 80\ \text{ns}) \times 10\ \text{kHz}
= 3{,}840\ \text{W}$$
$$P_{com} = 6{,}576\ \text{W}$$

*Energias de catálogo:*
$$P_{com} = (0{,}71 + 0{,}35)\ \text{mJ} \times 10\ \text{kHz} = 10{,}60\ \text{W}$$

**O modelo linear subestima a perda em 38 %.** A diferença é precisamente a corrente de cauda no
bloqueio e a recuperação reversa do diodo na entrada em condução, os dois fenômenos que os tempos
$t_r$ e $t_f$ não descrevem. Para o IGBT, portanto, **as energias de catálogo prevalecem sempre que
disponíveis**; o modelo linear serve como estimativa quando não há $E_{on}$ e $E_{off}$, e deve
então receber uma margem explícita.

**Passo 6, total.**

$$P_D = 17{,}20 + 10{,}60 = 27{,}80\ \text{W}
\qquad (\text{comutação} = 38\ \%)$$

**Passo 7, circuito térmico.** Com $T_j = 125$ °C, $T_a = 40$ °C, $R_{th,jc} = 0{,}77$ °C/W e
$R_{th,ch} = 0{,}24$ °C/W (módulo TO-247 com isolador fino):

$$R_{th,da} = \frac{125-40}{27{,}80} - 0{,}77 - 0{,}24 = 3{,}058 - 1{,}010 = 2{,}05\ ^\circ\text{C/W}$$

Um inversor trifásico tem seis IGBTs; com todos no mesmo dissipador e a mesma dissipação, a
resistência exigida cai para $2{,}05/6 \approx 0{,}34$ °C/W, já uma placa de porte considerável,
provavelmente com ventilação forçada.

**Varredura em frequência.** Aqui está a limitação estrutural do IGBT:

| $f_s$ | $P_{cond}$ | $P_{com}$ | Total |
|---|---|---|---|
| 2 kHz | 17,20 W | 2,12 W | 19,32 W |
| 5 kHz | 17,20 W | 5,30 W | 22,50 W |
| 10 kHz | 17,20 W | 10,60 W | 27,80 W |
| 20 kHz | 17,20 W | 21,20 W | 38,40 W |
| 50 kHz | 17,20 W | 53,00 W | 70,20 W |

As duas parcelas se igualam por volta de **16 kHz**. Acima de 20 kHz a dissipação torna-se
proibitiva para um dispositivo em TO-247, e é exatamente por isso que inversores de tração e
acionamentos industriais operam entre 2 e 16 kHz, faixa em que o IGBT reúne baixa perda de condução
e comutação ainda administrável. A comparação quantitativa com o MOSFET está no documento 06.

## 4. Síntese das expressões do IGBT

$$\boxed{
\begin{aligned}
P_{cond} &= V_{CE(sat)}\,I_{C(av)} = V_{CE(sat)}\,I_C\,D\\[4pt]
&\quad\big(\text{refinado: } V_{CE0}I_{C(av)} + r_{CE}I_{C(rms)}^2\big)\\[6pt]
P_{com} &= (E_{on} + E_{off})\,f_s \qquad \textbf{(preferencial)}\\[4pt]
P_{com} &= 0{,}6\,V_{CE}\,I_C\,(t_r + t_f)\,f_s \qquad
\big(\text{alternativa; subestima} \approx 40\ \%\big)
\end{aligned}}$$

**Parâmetros necessários da folha de dados:** $V_{CES}$; $I_C$ a 25 °C e a 100 °C;
$V_{CE(sat)}$ na corrente de operação e na temperatura de operação; $E_{on}$, $E_{off}$, $E_{ts}$
com as condições de ensaio; $t_r$, $t_f$; $R_{th,jc}$ do IGBT **e do diodo**, separadamente;
$T_{j,max}$; e, para o diodo *co-pack*, $V_F$ e $t_{rr}$.

**Advertência de projeto.** O diodo antiparalelo tem circuito térmico próprio, com $R_{th,jc}$ mais
que o dobro do IGBT (1,7 contra 0,77 °C/W no IRG4PC40UD). Em conversores com fator de potência
baixo ou operação regenerativa, a corrente circula predominantemente pelo diodo, e **é ele, não o
IGBT, que determina a temperatura de junção**. Calcular apenas o IGBT é um erro clássico de projeto
de inversores.

---

**Documento anterior:** [04. MOSFET de potência](04-mosfet-de-potencia.md)
**Próximo documento:** [06. Síntese comparativa e cálculo térmico](06-sintese-comparativa-e-calculo-termico.md)
