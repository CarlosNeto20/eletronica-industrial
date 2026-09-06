# 02. Diodo de Potência

O diodo é o único dispositivo do trabalho cujo estado não é comandado: quem decide se ele conduz
ou bloqueia é o circuito externo. Por isso mesmo ele é o ponto de partida natural, já que todas
as expressões de perda dos demais dispositivos são variações do que se estabelece aqui, e a seção
correspondente do enunciado já vem desenvolvida justamente como modelo a seguir.

## 1. Características básicas

### 1.1 Estrutura e princípio físico

O diodo de potência é uma junção $p$–$n$ com dois terminais: o **anodo** (A), ligado à região $p$, e
o **catodo** (K), ligado à região $n$. Na formação da junção, elétrons difundem da região $n$ para a
$p$ e lacunas no sentido oposto, recombinando-se e deixando para trás cargas fixas que formam a
**região de depleção**. Essas cargas fixas criam um campo elétrico e uma barreira de potencial que
se opõe à difusão. O equilíbrio se estabelece quando a corrente de deriva imposta pelo campo cancela
exatamente a corrente de difusão.

A relação de Boltzmann governa a densidade de portadores em função dessa barreira, e dela decorre
a característica exponencial da junção:

$$I = I_s\left(e^{\,qV/KT} - 1\right)$$

onde $I_s$ é a corrente de saturação reversa, $q$ a carga do elétron, $K$ a constante de Boltzmann
e $T$ a temperatura absoluta da junção. É o caráter exponencial dessa relação, e não uma lei de
Ohm, que produz o "joelho" da curva característica.

O diodo de potência difere do diodo de sinal por uma camada adicional: entre a região $p^+$ e a
$n^+$ existe uma região $n^-$ de baixa dopagem e espessura considerável, chamada **região de
deriva**, cuja função é sustentar a tensão reversa. Quanto maior a tensão de bloqueio desejada,
mais espessa e menos dopada precisa ser essa camada, e maior a queda direta em condução. Esse
compromisso entre tensão de bloqueio e queda direta atravessa toda a eletrônica de potência e
reaparecerá no MOSFET (na forma do crescimento de $R_{DS(on)}$ com a classe de tensão) e no IGBT
(que existe precisamente para contorná-lo).

### 1.2 Curva característica e as três regiões

A curva $I_F \times V_F$ do diodo apresenta três regiões de operação:

| Região | Condição | Comportamento |
|---|---|---|
| **Direta** | $V_d > V_{TO} \approx 0{,}7$ V | Anodo mais positivo que o catodo; a corrente flui de A para K, limitada apenas pelo circuito externo |
| **Reversa** | $V_d < 0$ | Catodo mais positivo; circula apenas a corrente de fuga, da ordem de µA, idealmente considerada nula |
| **Ruptura** | $V_d < -V_{BR}$ | Os laços covalentes são rompidos, a corrente cresce abruptamente e o dispositivo passa a se comportar como condutor metálico |

A região de ruptura é **destrutiva** para um diodo retificador. Apenas o diodo Zener é projetado
para operar nela, dentro de limites especificados de tensão e potência. Em projeto, isso significa
que a tensão reversa de pico do circuito ($PIV$) precisa ficar com folga confortável abaixo de
$V_{RRM}$. A prática usual adota 1,5 a 2 vezes o $PIV$ calculado.

O livro-texto apresenta quatro níveis de modelo para essa curva, em ordem crescente de
simplicidade: (a) o modelo exponencial completo; (b) a característica ideal, com queda nula em
condução e bloqueio perfeito; (c) a característica real medida; (d) o **modelo linear por partes**.
É esse último que interessa ao cálculo de perdas.

### 1.3 Classificação por tempo de recuperação reversa

A grandeza que separa as famílias de diodos de potência não é a corrente nem a tensão, mas o
**tempo de recuperação reversa** $t_{rr}$, porque é ele que fixa a frequência máxima de operação.
Tanto o livro quanto os slides adotam a mesma classificação:

| Família | $t_{rr}$ | Faixa de frequência | Aplicação típica |
|---|---|---|---|
| Retificador padrão (*standard*) | µs | 60 Hz a 1 kHz | Retificação da rede |
| Rápido (*fast recovery*) | 200–500 ns | 1 a 10 kHz | Conversores de média frequência |
| Ultrarrápido (*ultrafast / soft recovery*) | 30–200 ns | > 10 kHz | Fontes chaveadas, PFC |
| Schottky (junção metal-semicondutor) | < 30 ns | > 10 kHz | Retificação de saída de baixa tensão |
| Carbeto de silício (SiC) | ~0 (sem $Q_{rr}$) | > 10 kHz | Barramentos de 600 V e acima |

O diodo Schottky merece nota à parte: por ser uma junção metal-semicondutor, sua condução se dá
apenas por portadores majoritários, e portanto **não há carga armazenada a remover**. A corrente
que se observa no seu bloqueio é apenas a de carga da capacitância de junção, não uma recuperação
reversa propriamente dita. Em compensação, a barreira Schottky limita a tensão de bloqueio prática
a algumas centenas de volts e a corrente de fuga é ordens de grandeza maior, e são essas duas
características que fizeram do SiC a alternativa natural em alta tensão.

## 2. Princípio de polarização

**Região direta.** Com $V_d > V_{TO} \approx 0{,}7$ V, a barreira de potencial é reduzida de
$\phi_b$ para $(\phi_b - \phi)$ e a concentração de portadores minoritários injetados cresce
exponencialmente. As lacunas atravessam da região $p$ para a $n$, onde se recombinam, e para cada
elétron que se recombina outro entra vindo da fonte externa. O transporte é predominantemente por
**difusão**, e o resultado macroscópico é a circulação de corrente do anodo para o catodo.

**Região reversa.** Com $V_d < 0$, a barreira sobe para $(\phi_b + \phi)$ e a concentração de
minoritários cai abaixo do valor de equilíbrio. Surge uma pequena corrente de difusão em sentido
contrário, a corrente de saturação reversa $I_s$, da ordem de microampères, que é idealmente
tomada como nula.

**Região de ruptura.** Uma tensão reversa suficientemente elevada rompe as ligações covalentes na
região de depleção e a corrente cresce sem limite. O mecanismo pode ser avalanche ou Zener,
conforme a dopagem.

O ponto essencial para o cálculo de perdas é que **o diodo não tem terminal de controle**: a
transição entre as regiões é imposta pela tensão anodo-catodo, que por sua vez é imposta pelo
circuito. Isso torna o diodo uma chave não controlada, e faz com que suas formas de onda de
corrente sejam consequência direta da topologia, o que reforça o passo 1 do roteiro do documento
01.

## 3. Perdas de condução

### 3.1 Dedução

Do modelo linear por partes da Figura 2-7 do enunciado, a tensão instantânea em condução é

$$v_F = V_{TO} + r_T\,i_F$$

com $r_T = 1/\tan\alpha$, a inclinação da reta ajustada à característica real na faixa de corrente
de operação. A potência instantânea dissipada vale $p_F = v_F\,i_F$, e a potência média em um
período é

$$P_F = \frac{1}{T}\int_0^T v_F\,i_F\,dt
     = \frac{1}{T}\int_0^T V_{TO}\,i_F\,dt + \frac{1}{T}\int_0^T r_T\,i_F^2\,dt$$

$$\boxed{\;P_F = V_{TO}\,I_{F(av)} + r_T\,I_{F(rms)}^2\;}$$

ou, em função do fator de forma $a = I_{F(rms)}/I_{F(av)}$,

$$P_F = V_{TO}\,I_{F(av)} + r_T\,a^2\,I_{F(av)}^2$$

Essa é exatamente a Eq. (2-4) reproduzida no enunciado e a expressão dos slides,
$P_{cond} = V_{TO}I_{Dmed} + r_T I_{Def}^2$.

### 3.2 Como extrair $V_{TO}$ e $r_T$ da folha de dados

Há três situações, em ordem decrescente de conveniência:

**(a) O fabricante fornece os parâmetros diretamente.** É o caso dos módulos Semikron e dos FRED
da IXYS/Littelfuse, que tabelam $V_{(TO)}$ e $r_T$ já na temperatura de junção quente, exatamente
para permitir o cálculo de perdas. Exemplos usados neste trabalho:

| Componente | $V_{(TO)}$ | $r_T$ | Condição |
|---|---|---|---|
| SKKD 46 (Semikron) | 0,85 V | 5 mΩ | $T_{vj} = 125$ °C |
| SKKD 81 (Semikron) | 0,85 V | 1,8 mΩ | $T_{vj} = 125$ °C |
| DSEI2×31-06C (IXYS) | 1,10 V | 7,9 mΩ | $T_{vj} = 150$ °C |

**(b) O fabricante fornece a curva $I_F \times V_F$.** Ajusta-se uma reta por dois pontos da curva
na faixa de corrente de operação. Tomando $(V_1, I_1)$ e $(V_2, I_2)$:

$$r_T = \frac{V_2 - V_1}{I_2 - I_1}, \qquad V_{TO} = V_1 - r_T\,I_1$$

A escolha dos dois pontos importa: eles devem cercar a corrente eficaz de operação, não a corrente
nominal do dispositivo. Um ajuste feito na faixa de 1 a 20 A produz parâmetros diferentes de um
ajuste feito na faixa de 10 a 15 A, e apenas o segundo é válido se o circuito opera em torno de
12 A.

**(c) O fabricante fornece apenas $V_F$ máximo em um ponto.** É o caso mais pobre, típico de
componentes de baixo custo. Resta o modelo de fonte de tensão pura, $P_F \approx V_F I_{F(av)}$,
que **subestima** a perda porque ignora a parcela resistiva. Para o MUR1560, por exemplo, sabe-se
apenas que $V_F \le 1{,}5$ V a 15 A e 25 °C, e $V_F \le 1{,}2$ V a 15 A e 150 °C, dois pontos que
informam a deriva térmica, mas não a inclinação.

Note o comportamento térmico revelado por esse último par de valores: **a queda direta do diodo
diminui com a temperatura**. Isso decorre do coeficiente negativo de $V_{TO}$, que domina sobre o
coeficiente positivo de $r_T$ em correntes moderadas. A consequência prática é que diodos em
paralelo **não se equilibram sozinhos**: o mais quente conduz mais, e aquece mais. Diodos em
paralelo exigem casamento térmico rigoroso (mesmo dissipador, mesmo lote) ou resistores de
equalização.

### 3.3 Exemplo 1. Retificador de 60 Hz com módulo SKKD 46/16

**Circuito.** Ponte monofásica completa alimentando carga fortemente indutiva que drena
$I_o = 30$ A contínuos. Cada diodo conduz 180° por período, com corrente retangular de amplitude
$I_o$.

**Passo 1, formas de onda.** Corrente retangular de amplitude 30 A e razão cíclica 0,5.

**Passo 2, valores característicos.**

$$I_{F(av)} = \frac{I_o}{2} = 15{,}00\ \text{A}, \qquad
I_{F(rms)} = \frac{I_o}{\sqrt{2}} = 21{,}213\ \text{A}, \qquad
a = \sqrt{2} = 1{,}414$$

**Passo 3, parâmetros a 125 °C.** Do catálogo, $V_{(TO)} = 0{,}85$ V e $r_T = 5$ mΩ.

**Passo 4, perda de condução.**

$$P_{cond} = 0{,}85 \times 15{,}00 + 0{,}005 \times 21{,}213^2 = 12{,}750 + 2{,}250 = 15{,}00\ \text{W}$$

Vale conferir a forma alternativa: $0{,}85 \times 15 + 0{,}005 \times 1{,}414^2 \times 15^2
= 12{,}750 + 2{,}250 = 15{,}00$ W. Idênticas, como esperado.

Repare na composição: **85 % da perda vem do termo de limiar**, não do resistivo. Em retificação
de rede com corrente moderada, o que importa é $V_{TO}$; a resistência dinâmica só passa a dominar
em correntes muito elevadas ou em formas de onda com fator de forma alto.

**Passo 5, perda de comutação.** Em 60 Hz com diodo de recuperação padrão, $P_{com} \approx 0$
(a justificativa quantitativa está na Seção 4.5).

**Passo 6, total.** $P_D = 15{,}00$ W por diodo; $4 \times 15{,}00 = 60{,}0$ W na ponte. Sobre uma
saída de aproximadamente $0{,}9 \times 220 \times 30 = 5{,}94$ kW, isso representa **1,01 %**,
número perfeitamente típico de um estágio retificador de rede.

**Passo 7, circuito térmico.** O SKKD 46 é um módulo com dois diodos, e a ponte usa dois módulos.
A folha de dados fornece $R_{th,jc} = 0{,}6$ °C/W por diodo e 0,3 °C/W por módulo, e
$R_{th,ch} = 0{,}2$ °C/W por diodo e 0,1 °C/W por módulo. Adotando $T_j = 110$ °C (margem de 15 °C
sobre o limite de 125 °C) e $T_a = 40$ °C:

$$T_c = T_j - P_{diodo}R_{th,jc} = 110 - 15{,}0 \times 0{,}6 = 101{,}0\ ^\circ\text{C}$$
$$T_d = T_c - P_{mod}R_{th,ch(mod)} = 101{,}0 - 30{,}0 \times 0{,}1 = 98{,}0\ ^\circ\text{C}$$
$$R_{th,da} = \frac{T_d - T_a}{P_{total}} = \frac{98{,}0 - 40}{60{,}0} = 0{,}967\ ^\circ\text{C/W}$$

Um dissipador de 0,97 °C/W para 60 W é um perfil extrudado de porte médio com convecção natural,
ou um perfil pequeno com ventilação forçada.

## 4. Perdas de comutação

### 4.1 Entrada em condução

Para passar do bloqueio à condução, o diodo precisa **adquirir** carga na região de difusão. Esse
processo é bem mais rápido que a remoção de carga do processo inverso, e o tempo de recuperação
direta não constitui problema prático na esmagadora maioria dos circuitos. Tanto o livro quanto os
slides são categóricos:

$$P_{ec} \approx 0$$

A ressalva vale para conversores muito rápidos, nos quais a indutância parasita associada ao
*forward recovery* produz um pico de tensão sobre o diodo no instante da entrada em condução. Esse
efeito é tratado como sobretensão a ser grampeada, não como perda a ser contabilizada.

### 4.2 Bloqueio: o fenômeno da recuperação reversa

Aqui está a perda. Um diodo em condução direta tem carga armazenada na região de difusão. Ao ser
reversamente polarizado, **essa carga precisa ser removida antes que a junção possa sustentar
tensão reversa**. Enquanto houver excesso de portadores, a junção permanece diretamente
polarizada, e a tensão sobre o diodo praticamente não muda.

A sequência, seguindo a Figura 1.5(c) do livro e a figura correspondente dos slides:

| Intervalo | O que acontece |
|---|---|
| $0$ a $t_0$ | Diodo diretamente polarizado, conduzindo $I_F$ |
| $t_0$ a $t_1$ | A corrente decresce com $di/dt$ imposta pelo circuito externo, cruza zero e torna-se negativa; o diodo **ainda conduz** |
| $t_1$ a $t_2$ | A corrente reversa cresce até o pico $I_{rr}$; nesse instante a carga excedente acabou e a junção começa a bloquear |
| $t_2$ a $t_3$ | A corrente reversa decai a zero enquanto a tensão sobe rapidamente para $-V_R$ |

A área hachurada sob a curva de corrente reversa é a **carga de recuperação reversa** $Q_{rr}$, e o
intervalo $t_1$ a $t_3$ é o **tempo de recuperação reversa** $t_{rr}$. O intervalo $t_1$–$t_2$ é
chamado tempo de armazenamento.

O ponto crítico é que **a corrente reversa e a tensão reversa são grandes simultaneamente** durante
$t_2$–$t_3$. É aí que a energia é dissipada.

### 4.3 As expressões e a diferença entre elas

Partindo de $P_{sw} = E_{sw} f_s$, o livro-texto escreve, nas Eqs. (1.10) a (1.12):

$$P_{sw} = \left(\tfrac{1}{2}Q_{rr}V_R\right) f_s$$

e, aproximando a área hachurada por um triângulo, $Q_{rr} = \tfrac{1}{2}t_{rr}I_{rr}$, de onde

$$P_{sw} = \tfrac{1}{4}\,I_{rr}\,V_R\,t_{rr}\,f_s$$

Já os slides de aula apresentam

$$P_{bloq} = V_R\,Q_{rr}\,f_s$$

**As duas diferem por um fator 2, e ambas estão certas dentro das suas hipóteses.** O fator $1/2$
do livro admite que apenas metade da carga $Q_{rr}$ é removida já com a tensão reversa plena
aplicada, e a outra metade é removida enquanto a tensão sobre o diodo ainda é pequena, no intervalo
$t_1$–$t_2$. A expressão dos slides supõe o caso extremo em que a tensão plena se estabelece desde
o início da recuperação. Ela é, portanto, um **critério conservador**, adequado a projeto; a do
livro é a estimativa física mais fiel.

Neste trabalho adota-se a expressão do livro como valor de referência e a dos slides como limite
superior, reportando ambas sempre que a parcela for significativa.

### 4.4 A armadilha da temperatura e do $di/dt$

$Q_{rr}$ **não é uma constante do dispositivo**. Ela cresce fortemente com:

- a **temperatura de junção**, porque a vida dos portadores minoritários aumenta;
- a **taxa de decrescimento da corrente** $di_F/dt$ imposta pelo circuito, porque menos carga se
  recombina naturalmente antes do bloqueio;
- a **corrente direta** que circulava antes do bloqueio.

Por isso as folhas de dados especificam $t_{rr}$ e $I_{rr}$ *sob condições declaradas*. Para o
DSEI2×31-06C, por exemplo, $t_{rr} = 35$ ns e $I_{RM} \le 9$ A a 25 °C, mas $I_{RM} \le 25$ A a
100 °C, sob $-di_F/dt = 200$ A/µs. Usar o valor de 25 °C em um projeto que opera a 100 °C
subestima a perda por um fator próximo de cinco.

### 4.5 Por que a comutação é desprezível em 60 Hz

Volte ao Exemplo 1. Mesmo admitindo, generosamente, $Q_{rr} = 100$ µC para um retificador padrão
de 45 A, valor muito acima do real, e $V_R = 311$ V:

$$P_{bloq} = \tfrac{1}{2} \times 100\times10^{-6} \times 311 \times 60 = 0{,}93\ \text{W}$$

contra 15,0 W de condução. Menos de 6 %, com uma hipótese deliberadamente pessimista. Fica
justificada a prática consagrada de **ignorar a comutação em retificadores de rede**, e fica
igualmente claro que essa prática deixa de valer assim que a frequência sobe, como o próximo
exemplo mostra.

### 4.6 Exemplo 2. Diodo de saída de um conversor boost a 50 kHz

**Circuito.** Conversor elevador (*boost*) de $V_{in} = 200$ V para $V_o = 400$ V, entregando
$P_o = 1$ kW a $f_s = 50$ kHz, em condução contínua. Diodo: **DSEI2×31-06C** (600 V, 2×30 A FRED),
com $V_{F0} = 1{,}10$ V, $r_F = 7{,}9$ mΩ, $t_{rr} = 35$ ns e $R_{th,jc} = 1{,}2$ K/W.

**Passo 1, formas de onda.** O diodo conduz durante $(1-D)$ do período, com a corrente do indutor.

$$D = 1 - \frac{V_{in}}{V_o} = 1 - \frac{200}{400} = 0{,}500$$
$$I_L = \frac{P_o}{V_{in}} = 5{,}00\ \text{A}, \qquad I_o = \frac{P_o}{V_o} = 2{,}50\ \text{A}$$

**Passo 2, valores característicos.** Desprezando a ondulação do indutor,

$$I_{D(av)} = I_o = 2{,}50\ \text{A}, \qquad
I_{D(rms)} = I_L\sqrt{1-D} = 5{,}00\sqrt{0{,}5} = 3{,}536\ \text{A}$$

**Passos 3 e 4, perda de condução.**

$$P_{cond} = 1{,}10 \times 2{,}50 + 0{,}0079 \times 3{,}536^2 = 2{,}750 + 0{,}099 = 2{,}849\ \text{W}$$

**Passo 5, perda de comutação.** A tensão reversa aplicada é $V_R = V_o = 400$ V. Estimando
$Q_{rr}$ pela aproximação triangular:

*A 25 °C* ($t_{rr} = 35$ ns, $I_{rr} = 9$ A):
$$Q_{rr} = \tfrac{1}{2}\times 35\times10^{-9}\times 9 = 158\ \text{nC}
\;\Rightarrow\; P_{bloq} = \tfrac{1}{2}\times 158\text{n}\times 400 \times 50\text{k} = 1{,}58\ \text{W}$$

*A 100 °C* ($t_{rr} \approx 60$ ns, $I_{rr} = 25$ A, pior caso de catálogo):
$$Q_{rr} = 750\ \text{nC} \;\Rightarrow\; P_{bloq} = 7{,}5\ \text{W}$$

O intervalo entre 1,6 W e 7,5 W parece desconfortavelmente largo, e é. **A recuperação reversa é
o parâmetro mais incerto de todo o cálculo de perdas**, porque depende de três variáveis que o
projetista só conhece aproximadamente: temperatura, $di/dt$ e corrente direta prévia. A conduta
correta é dimensionar pelo pior caso de catálogo e verificar em bancada.

**Passo 6, total e leitura do resultado.**

| Condição | $P_{cond}$ | $P_{bloq}$ | Total | Comutação |
|---|---|---|---|---|
| 25 °C | 2,85 W | 1,58 W | 4,42 W | 36 % |
| 100 °C (pior caso) | 2,85 W | 7,50 W | 10,29 W | 73 % |

E a varredura em frequência, no pior caso térmico, mostra o problema de frente:

| $f_s$ | $P_{cond}$ | $P_{com}$ | Total |
|---|---|---|---|
| 10 kHz | 2,85 W | 1,49 W | 4,34 W |
| 20 kHz | 2,85 W | 2,98 W | 5,82 W |
| 50 kHz | 2,85 W | 7,44 W | 10,29 W |
| 100 kHz | 2,85 W | 14,88 W | 17,72 W |
| 200 kHz | 2,85 W | 29,75 W | 32,60 W |

A perda de condução é uma reta horizontal; a de comutação é uma reta pela origem. **Acima de
20 kHz, o diodo de silício deixa de ser limitado pela sua queda direta e passa a ser limitado pela
sua recuperação reversa.** É exatamente essa constatação que justifica economicamente o diodo
Schottky de carbeto de silício, cuja carga de recuperação é essencialmente nula: substituir o
FRED por um SiC neste circuito eliminaria 7,5 W de perda, reduzindo a dissipação do diodo em 73 %.

**Passo 7, circuito térmico** (pior caso, $P_D = 10{,}29$ W). Com $T_j = 125$ °C, $T_a = 40$ °C,
$R_{th,jc} = 1{,}2$ °C/W e $R_{th,ch} = 0{,}5$ °C/W:

$$R_{th,da} = \frac{125 - 40}{10{,}29} - 1{,}2 - 0{,}5 = 8{,}26 - 1{,}70 = 6{,}56\ ^\circ\text{C/W}$$

## 5. Síntese das expressões do diodo

$$\boxed{
\begin{aligned}
P_{cond} &= V_{TO}\,I_{F(av)} + r_T\,I_{F(rms)}^2 = V_{TO}\,I_{F(av)} + r_T\,a^2 I_{F(av)}^2\\[4pt]
P_{ec} &\approx 0\\[4pt]
P_{bloq} &= \tfrac{1}{2}\,Q_{rr}\,V_R\,f_s = \tfrac{1}{4}\,I_{rr}\,V_R\,t_{rr}\,f_s
\qquad \big(V_R Q_{rr} f_s \text{ como limite conservador}\big)\\[4pt]
P_{D} &= P_{cond} + P_{bloq}
\end{aligned}}$$

**Parâmetros necessários da folha de dados:** $V_{TO}$ e $r_T$ (ou a curva $I_F \times V_F$) na
temperatura de junção de operação; $t_{rr}$ e $I_{rr}$ ou $Q_{rr}$ nas condições de $di/dt$ e
temperatura do circuito; $R_{th,jc}$; $V_{RRM}$; $I_{F(AV)}$; $I_{FSM}$ e $I^2t$ para coordenação
com fusível.

**Regra de bolso:** abaixo de 1 kHz, dimensione pela condução; acima de 20 kHz, dimensione pela
recuperação reversa; entre as duas faixas, calcule as duas parcelas.

---

**Documento anterior:** [01. Fundamentos de perdas](01-fundamentos-de-perdas-em-semicondutores.md)
**Próximo documento:** [03. Tiristor e TRIAC](03-tiristor-e-triac.md)
