# 04. MOSFET de Potência

O MOSFET é o primeiro dispositivo plenamente controlado deste trabalho: a porta comanda tanto a
entrada em condução quanto o bloqueio, e o faz sem consumir corrente contínua. É também o único
cuja perda de condução não tem tensão de limiar, e essa é uma diferença estrutural, não de grau,
que reorganiza toda a lógica de escolha de dispositivos.

## 1. Características básicas

### 1.1 Estrutura e princípio de operação

O MOSFET (*metal oxide semiconductor field effect transistor*) tem três terminais: **dreno** (D),
**fonte** (S) e **porta** (G). Existem dois tipos, e os slides são diretos quanto ao uso:

- **Depleção**, pouco usado em potência;
- **Intensificação** (*enhancement*), amplamente usado.

Na estrutura de canal $n$ tipo intensificação, uma camada $n$ ligada ao dreno e outra $n$ ligada à
fonte são separadas por um substrato $p$. A porta é um condutor metálico isolado do corpo do
dispositivo por uma camada de óxido, tipicamente dióxido de silício.

Aplicando tensão positiva na porta, o campo elétrico através do óxido polariza as cargas nessa
camada, que por sua vez atraem elétrons do material $p$. Forma-se um **canal $n$ induzido**, a
chamada *camada de inversão*, que interliga as duas regiões $n$. Aplicando então tensão positiva
entre dreno e fonte, a corrente circula por esse canal. Quanto maior $V_{GS}$, mais larga a camada
de inversão; o dispositivo atinge a **plena intensificação** (*full enhancement*) quando essa
largura é máxima.

Duas consequências estruturais importam ao projeto:

**O diodo de corpo.** O substrato $p$ é internamente curto-circuitado com a fonte, para impedir
que o BJT parasita NPN entre dreno e fonte entre em condução. Esse curto cria uma junção $p$–$n$
entre dreno e fonte, o **diodo de corpo** (*body diode*), com anodo na fonte e catodo no dreno.
Ele é útil como roda livre em inversores acionando cargas indutivas, dispensando um diodo externo;
mas é um diodo lento, de recuperação ruim. Para o IRFP460A, $t_{rr}$ chega a 710 ns e
$Q_{rr}$ a 7,5 µC, números que inviabilizam o uso do diodo de corpo em comutação dura acima de
algumas dezenas de quilohertz e explicam a existência de topologias com comutação suave.

**Condução por portadores majoritários.** Não há junção $p$–$n$ diretamente polarizada no caminho
da corrente principal. É essa a razão física da ausência de tensão de limiar em condução.

### 1.2 Capacitâncias parasitas

O comportamento dinâmico do MOSFET é inteiramente governado por três capacitâncias: $C_{gs}$
(porta-fonte), $C_{gd}$ (porta-dreno, também chamada de Miller) e $C_{ds}$ (dreno-fonte). As folhas
de dados não as fornecem diretamente; fornecem as combinações que se medem em bancada:

| Parâmetro de catálogo | Relação com as capacitâncias físicas |
|---|---|
| $C_{iss}$ (entrada) | $C_{gs} + C_{gd}$ |
| $C_{oss}$ (saída) | $C_{ds} + C_{gd}$ |
| $C_{rss}$ (reversa, ou de realimentação) | $C_{gd}$ |

$C_{gd}$ é a mais importante e a mais fortemente dependente da tensão, porque é composta pela série
da capacitância do óxido com a capacitância da região de depleção:

$$\frac{1}{C_{gd}} = \frac{1}{C_{g,ox}} + \frac{1}{C_{gd,bulk}}$$

À medida que $V_{DS}$ aumenta, a depleção se alarga, $C_{gd,bulk}$ cai e $C_{gd}$ cai com ela.
Essa não linearidade é responsável tanto pelo **patamar de Miller** na forma de onda de $V_{GS}$
quanto pelo fato de que $C_{oss}$ tabelada a 25 V superestima grosseiramente o valor efetivo em
400 V. Para o SPW20N60C3, $C_{oss} = 780$ pF a 25 V; a capacitância equivalente de energia em
400 V é uma fração pequena disso, ponto retomado no documento 11.

### 1.3 Características estáticas

A **curva de transferência** $i_D \times V_{GS}$ mostra uma tensão de limiar $V_{GS(th)}$,
tipicamente de 3 a 4 V em MOSFETs de potência, abaixo da qual o dispositivo está bloqueado. Acima
dela,

$$i_D \propto (V_{GS} - V_{GS(th)})^2$$

A **característica de saída** $i_D \times V_{DS}$ tem duas regiões:

- **Região ativa**, para $V_{DS} > (V_{GS} - V_{GS(th)})$: a corrente de dreno independe de $V_{DS}$
  e depende apenas de $V_{GS}$. É a região de operação em amplificação, e a região a evitar em
  chaveamento;
- **Região ôhmica**, para $V_{DS} < (V_{GS} - V_{GS(th)})$: a relação $i_D \times V_{DS}$ é linear.
  **É nesta região que o MOSFET opera como chave fechada.**

A resistência do canal na região ôhmica é a $R_{DS(on)}$, o parâmetro de seleção mais importante do
dispositivo. Para minimizá-la é preciso levar o MOSFET à plena intensificação: $V_{GS} \approx 10$ V
já basta para ligar, mas a prática de projeto usa 15 V. O limite é $\pm 20$ V, imposto pela
rigidez dielétrica da fina camada de óxido.

### 1.4 A cautela de manuseio, e por que ela é quantitativa

Os slides e o livro alertam para o manuseio. O argumento é aritmético e vale reproduzir. Para um
MOSFET com $C_{iss} = 4000$ pF, uma carga estática corporal típica de 1 µC produziria

$$V_{GS} = \frac{Q}{C_{iss}} = \frac{1\times10^{-6}}{4\times10^{-9}} = 250\ \text{V}$$

contra um limite de 20 V. **Tocar a porta de um MOSFET pode destruí-lo permanentemente.** Daí as
práticas: transporte em espuma condutiva, curto-circuito entre porta e fonte quando fora de uso, e
diodo Zener de 15 V junto aos terminais de porta no circuito final.

## 2. Princípio de polarização e a dinâmica de comutação

O livro-texto divide o processo de chaveamento em seis intervalos, descritos em função da carga
transferida à porta. Compreendê-los é o que permite interpretar corretamente $t_r$ e $t_f$ das
folhas de dados.

| Intervalo | Carga | O que acontece |
|---|---|---|
| $t_0$–$t_1$ | $Q_1 - Q_0$ | $C_{gs}$ carrega até $V_{GS(th)}$. Nada acontece no circuito de potência: é o **atraso de entrada em condução** $t_{d(on)}$ |
| $t_1$–$t_2$ | $Q_2 - Q_1$ | $V_{GS}$ sobe acima do limiar e a corrente de dreno cresce até $i_D$ pleno. **$V_{DS}$ ainda é alta**, e este é o $t_r$ |
| $t_2$–$t_3$ | $Q_3 - Q_2$ | Quase toda a corrente de porta desvia por $C_{gd}$, a carga em $C_{gs}$ fica constante e $V_{GS}$ apresenta o **patamar de Miller**. $V_{DS}$ cai, com $dV_{DS}/dt = i_g/C_{gd}$ |
| $t_3$–$t_4$ | $Q_4 - Q_3$ | $V_{DS}$ já atingiu $i_D R_{DS(on)}$; $C_{gs}$ termina de carregar até a plena intensificação |
| $t_4$–$t_5$ | 0 | MOSFET plenamente conduzindo; corrente de porta nula |
| $t_5$–$t_8$ | $Q_6 - Q_4$ | Processo inverso: sai da plena intensificação, $V_{DS}$ sobe (descarga de $C_{gd}$) e a corrente cai a zero, e este último trecho é o $t_f$ |

Três conclusões de projeto saem daí:

1. **$t_r$ e $t_f$ são os intervalos em que $v$ e $i$ se sobrepõem**, e são eles, e não os atrasos
   $t_{d(on)}$ e $t_{d(off)}$, que entram no cálculo de perdas. Os atrasos importam para o tempo
   morto entre chaves de um mesmo braço, não para a dissipação.
2. **A velocidade de comutação é ajustável pela corrente de porta**, isto é, pelo resistor $R_G$.
   Reduzir $R_G$ acelera a comutação e diminui a perda, ao custo de maior $dv/dt$, mais
   interferência eletromagnética e maior risco de oscilação. É um compromisso de projeto, não uma
   constante do dispositivo, motivo pelo qual as folhas de dados sempre declaram o $R_G$ do ensaio.
3. **A corrente de porta precisa ter caminho de retorno no bloqueio.** O *driver* tem de ser capaz
   de *drenar* corrente, não apenas fornecê-la; caso contrário $C_{gs}$ descarrega lentamente e o
   dispositivo permanece na região ativa por tempo demais.

## 3. Perdas de condução

### 3.1 A expressão

Na região ôhmica o MOSFET é um resistor. Sem tensão de limiar, a Eq. (1.35) do livro-texto e a
expressão dos slides coincidem:

$$\boxed{\;P_{cond} = R_{DS(on)}\,I_{D(rms)}^2\;}$$

Note o que desapareceu: a corrente média. **A perda de condução de um MOSFET depende apenas do
valor eficaz.**

### 3.2 A correção térmica, que não é opcional

Os slides são explícitos: *"a resistência do canal do MOSFET, $R_{DS(on)}$, deve ser ajustada para
a temperatura de junção de 100 °C. Normalmente, o valor fornecido pelo fabricante é na temperatura
de 25 °C, então deve ser corrigido usando a curva normalizada do catálogo."*

A razão física é a mobilidade dos portadores no canal, que decresce com a temperatura. O livro
quantifica o efeito em **aproximadamente 0,6 % por °C**, o que permite a estimativa analítica

$$R_{DS(on)}(T_j) \approx R_{DS(on)}(25\,^\circ\text{C})\left[1 + 0{,}006\,(T_j - 25)\right]$$

Para $T_j = 100$ °C, o fator é 1,45. Verificando contra a curva normalizada do IRFP460A, que indica
aproximadamente 1,5 a 100 °C, os dois caminhos concordam dentro de 3 %.

**Ignorar essa correção subestima a perda de condução em 45 %**, e como é justamente a perda que
determina a temperatura, o erro se realimenta.

Há um lado positivo nesse coeficiente positivo de temperatura: ele torna o paralelismo de MOSFETs
**auto-equalizante**. Se um dispositivo conduzir mais que os demais, aquece, sua $R_{DS(on)}$ sobe,
e a corrente migra para os outros. Os slides e o livro registram o mesmo: resistores de equalização
em série com a fonte, obrigatórios em BJTs, são dispensáveis em MOSFETs. Pelo mesmo mecanismo, o
MOSFET **não sofre segunda ruptura** (*second breakdown*). O único cuidado no paralelismo é
inserir resistores de porta individuais de 10 a 100 Ω, para amortecer oscilações de alta frequência
entre as indutâncias das trilhas de porta e as capacitâncias do dispositivo.

### 3.3 O preço da classe de tensão

O livro registra um fato que o projetista precisa ter internalizado: para uma mesma corrente
nominal, a queda em condução de um MOSFET de alta tensão ($R_{DS(on)}$ de 1 a 2 Ω) é muito maior
que a de um de baixa tensão ($R_{DS(on)} \approx 0{,}1$ Ω). A causa é estrutural, pois a região $n$
de deriva precisa ser mais espessa e menos dopada para suportar o campo elétrico. A relação empírica
aproximada é

$$R_{DS(on)} \propto V_{BR}^{\,2{,}4\ \text{a}\ 2{,}6}$$

Duplicar a tensão de bloqueio quintuplica a resistência de canal. **É esta lei que criou o IGBT** e,
mais recentemente, os dispositivos de carbeto de silício, cujo campo crítico de ruptura dez vezes
maior desloca a curva inteira.

### 3.4 Exemplo 5. Chopper abaixador com IRFP460A

**Circuito.** Conversor abaixador (*buck*) alimentado em $V_{dd} = 200$ V, entregando corrente de
carga $I_D = 8$ A quase contínua (indutor grande), com $D = 0{,}5$ e $f_s = 50$ kHz. Carga
indutiva com diodo de roda livre.

**Componente.** IRFP460A / SiHFP460, de 500 V e 20 A a 25 °C (13 A a 100 °C),
$R_{DS(on)} \le 0{,}27$ Ω a $V_{GS} = 10$ V, $t_r = 55$ ns, $t_f = 39$ ns,
$R_{th,jc} = 0{,}45$ °C/W, $T_{j,max} = 150$ °C.

**Passo 1, formas de onda.** Corrente retangular de amplitude 8 A e razão cíclica 0,5.

**Passo 2, valores característicos.**

$$I_{D(rms)} = I_D\sqrt{D} = 8\sqrt{0{,}5} = 5{,}657\ \text{A}$$

**Passo 3, correção térmica.**

$$R_{DS(on)}(100\,^\circ\text{C}) = 0{,}27 \times [1 + 0{,}006(100-25)] = 0{,}27 \times 1{,}45
= 0{,}3915\ \Omega$$

**Passo 4, perda de condução.**

$$P_{cond} = 0{,}3915 \times 5{,}657^2 = 12{,}528\ \text{W}$$

**Passo 5, perda de comutação.** Carga indutiva grampeada, portanto vale o modelo dos slides:

$$P_{ec} = \tfrac{1}{2} \times 8 \times 200 \times (1{,}2 \times 55\ \text{ns}) \times 50\ \text{kHz}
= 2{,}640\ \text{W}$$
$$P_{bloq} = \tfrac{1}{2} \times 8 \times 200 \times (1{,}2 \times 39\ \text{ns}) \times 50\ \text{kHz}
= 1{,}872\ \text{W}$$
$$P_{com} = 4{,}512\ \text{W}$$

Para contraste, o modelo de carga resistiva do livro daria

$$P_{com} = \tfrac{1}{6} \times 200 \times 8 \times (55+39)\ \text{ns} \times 50\ \text{kHz}
= 1{,}253\ \text{W}$$

ou seja, **3,6 vezes menos**, exatamente a razão prevista no documento 01. Aplicar o modelo errado
aqui levaria a dimensionar o dissipador para 13,8 W em vez de 17,0 W, com erro de 23 % na
temperatura de junção.

**Passo 6, total.**

$$P_D = 12{,}528 + 4{,}512 = 17{,}040\ \text{W}
\qquad (\text{comutação} = 26{,}5\ \%)$$

**Varredura em frequência.** A separação entre as duas parcelas fica evidente:

| $f_s$ | $P_{cond}$ | $P_{com}$ | Total |
|---|---|---|---|
| 10 kHz | 12,53 W | 0,90 W | 13,43 W |
| 20 kHz | 12,53 W | 1,80 W | 14,33 W |
| 50 kHz | 12,53 W | 4,51 W | 17,04 W |
| 100 kHz | 12,53 W | 9,02 W | 21,55 W |
| 200 kHz | 12,53 W | 18,05 W | 30,58 W |

A perda de condução é constante; a de comutação dobra a cada duplicação da frequência. Elas se
igualam em torno de 140 kHz.

**Passo 7, circuito térmico.** Com $T_j = 125$ °C (margem de 25 °C sobre 150 °C), $T_a = 40$ °C,
$R_{th,jc} = 0{,}45$ °C/W e $R_{th,ch} = 0{,}5$ °C/W:

$$R_{th,da} = \frac{125-40}{17{,}04} - 0{,}45 - 0{,}5 = 4{,}99 - 0{,}95 = 4{,}04\ ^\circ\text{C/W}$$

**Leitura crítica do resultado.** Um dissipador de 4 °C/W para 17 W é perfeitamente viável, mas o
projeto merece uma objeção: 12,5 W de perda de condução para entregar 800 W ($200 \times 8 \times
0{,}5$) representa 1,6 %, e vem quase toda do fato de o IRFP460A ser um dispositivo de 500 V
operando com apenas 8 A. Duas alternativas melhorariam substancialmente o rendimento:

- **Paralelar dois IRFP460A**: a resistência equivalente cai à metade e a perda de condução para
  6,3 W, ao custo de dobrar a carga de porta;
- **Usar tecnologia de superjunção**: um SPW20N60C3 (CoolMOS de 650 V) tem $R_{DS(on)} = 0{,}19$ Ω
  que é 30 % menor, com tensão de bloqueio 30 % maior, e comuta cerca de dez vezes mais rápido.

Este é um resultado típico e vale generalizar: **quando a perda de condução domina, o caminho é
mais silício; quando a de comutação domina, o caminho é silício melhor.**

## 4. Síntese das perdas de comutação

$$\boxed{
\begin{aligned}
P_{ec} &= \tfrac{1}{2}\,V_{DS}\,I_D\,(1{,}2\,t_r)\,f_s\\[4pt]
P_{bloq} &= \tfrac{1}{2}\,V_{DS}\,I_D\,(1{,}2\,t_f)\,f_s\\[4pt]
P_{com} &= P_{ec} + P_{bloq} = 0{,}6\,V_{DS}\,I_D\,(t_r + t_f)\,f_s
\end{aligned}}$$

Três parcelas adicionais que o modelo não captura e que precisam ser lembradas:

**Perda capacitiva.** $P_{cap} = \tfrac{1}{2}C_{o(er)}V_{DS}^2 f_s$, com $C_{o(er)}$ a capacitância
equivalente de energia na tensão de operação, e não a $C_{oss}$ tabelada a 25 V. Em conversores de
alta tensão e baixa corrente, é a parcela dominante.

**Recuperação reversa do diodo complementar.** A carga $Q_{rr}$ do diodo que está bloqueando aparece
como um pico adicional de corrente no MOSFET que está ligando, e a energia correspondente
$Q_{rr}V_{DS}$ é dissipada **no MOSFET**, não no diodo. Em meia-ponte com o diodo de corpo atuando
como roda livre, essa parcela pode superar todas as demais somadas, e é a razão pela qual MOSFETs de
alta tensão em comutação dura exigem topologias com diodo externo rápido ou comutação suave.

**Perda de comando.** $P_{drive} = Q_g V_{GS} f_s$, dissipada no *driver* e no resistor de porta.
Para o IRFP460A ($Q_g = 105$ nC) a 100 kHz com $V_{GS} = 15$ V, resultam 158 mW por chave, valor
irrelevante para a térmica do MOSFET, mas dimensionante para a fonte auxiliar quando há muitas
chaves.

## 5. Parâmetros necessários da folha de dados

| Grandeza | Uso |
|---|---|
| $V_{DSS}$ | Verificação de margem de tensão (usar $\ge 1{,}3 \times$ a tensão do barramento) |
| $I_D$ a 25 °C e a 100 °C | Verificação de margem de corrente, usando sempre o valor a 100 °C |
| $R_{DS(on)}$ máx. e curva normalizada vs. $T_j$ | Perda de condução, corrigida a 100 °C |
| $t_r$, $t_f$ (com o $R_G$ do ensaio) | Perda de comutação |
| $C_{iss}$, $C_{oss}$, $C_{rss}$; $Q_g$, $Q_{gs}$, $Q_{gd}$ | Projeto do *driver* e parcela capacitiva |
| $V_{SD}$, $t_{rr}$, $Q_{rr}$ do diodo de corpo | Viabilidade do uso como roda livre |
| $R_{th,jc}$, $T_{j,max}$ | Circuito térmico |

**Recomendação dos slides, que vale repetir:** *abrir o catálogo para verificar detalhes.* Os
valores de comutação são medidos sob condições declaradas de $V_{DD}$, $I_D$, $R_G$ e $T_j$, e
extrapolá-los para outro ponto de operação sem crítica é fonte frequente de erro.

---

**Documento anterior:** [03. Tiristor e TRIAC](03-tiristor-e-triac.md)
**Próximo documento:** [05. IGBT de potência](05-igbt-de-potencia.md)
