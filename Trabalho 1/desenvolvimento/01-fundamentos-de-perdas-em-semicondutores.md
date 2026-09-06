# 01. Fundamentos de Perdas em Semicondutores de Potência

Este documento estabelece o ferramental comum a todos os dispositivos tratados na Parte 1. Nenhum
componente específico é dimensionado aqui; o objetivo é fixar o vocabulário, o modelo geral de
perdas e, sobretudo, a razão física de cada termo, para que as expressões dos documentos
seguintes não apareçam como fórmulas a decorar.

## 1. A chave ideal como referência

Toda a eletrônica de potência se apoia numa ideia simples: processar energia comutando, não
dissipando. Um regulador linear que abaixa 12 V para 5 V a 1 A joga 7 W fora em calor porque o
transistor opera na região ativa, sustentando 7 V enquanto conduz 1 A. Um conversor chaveado
resolve o mesmo problema alternando entre dois estados nos quais, idealmente, ou a tensão sobre o
dispositivo é zero, ou a corrente através dele é zero. Em ambos os casos o produto $v \cdot i$ se
anula, e a potência dissipada é nula.

O livro-texto adotado na disciplina lista as características de uma chave ideal do tipo SPST
(*single pole, single throw*):

1. Resistência de condução nula (queda direta zero);
2. Resistência de bloqueio infinita (corrente reversa zero);
3. Conduz corrente infinita nos dois sentidos quando ligada;
4. Suporta tensões direta e reversa infinitas quando desligada;
5. Comuta instantaneamente entre os dois estados;
6. Não dissipa potência, nem em condução nem nas transições;
7. As transições são plenamente controláveis;
8. Não consome potência de comando.

Nenhuma chave semicondutora real reúne todas essas características, e a lista serve exatamente
como grade de leitura: **cada perda que este trabalho quantifica é a violação de um desses itens.**

| Item violado | Perda resultante | Onde é tratada |
|---|---|---|
| 1. Resistência de condução nula | perda de condução | Seção 3 deste documento |
| 2. Bloqueio perfeito | perda de bloqueio (corrente de fuga) | Seção 6 |
| 5. Comutação instantânea | perda de comutação | Seção 4 |
| 8. Comando sem potência | perda de porta ou de gatilho | Seção 5 |

A parcela 3 (condução unidirecional) e a 4 (limites de tensão) não geram perda, mas geram
**restrições de escolha**, pois são elas que determinam se um dado dispositivo pode ou não ser
usado numa topologia. A parcela 7 é o que separa dispositivos não controlados (diodo),
semicontrolados (tiristor, TRIAC) e plenamente controlados (MOSFET, IGBT).

## 2. Decomposição da potência dissipada

A potência total dissipada em qualquer dispositivo semicondutor de potência decompõe-se em três
parcelas, seguindo a Eq. (1.5) do capítulo de referência:

$$P_D = P_{on} + P_{off} + P_{sw}$$

onde $P_{on}$ é a perda no estado conduzindo, $P_{off}$ a perda no estado bloqueado e $P_{sw}$ a
perda associada às transições entre os dois estados. Adotando a notação dos slides de aula, que é
a que será usada daqui em diante:

$$P_{total} = P_{cond} + P_{com}, \qquad P_{com} = P_{ec} + P_{bloq}$$

com $P_{ec}$ a perda na entrada em condução (*turn-on*) e $P_{bloq}$ a perda no bloqueio
(*turn-off*). A perda de estado bloqueado foi absorvida por ser desprezível na quase totalidade
dos casos práticos, e a justificativa está na Seção 6.

A distinção fundamental entre as duas parcelas é o **comportamento com a frequência**:

$$P_{cond} \;\text{é independente de } f_s, \qquad P_{com} \propto f_s$$

Esse é o fato mais importante de toda a Parte 1. A perda de condução depende apenas das correntes
médias e eficazes que o circuito impõe; a perda de comutação é energia perdida *por evento* de
chaveamento, multiplicada pelo número de eventos por segundo. Toda a escolha de dispositivo em
eletrônica de potência decorre dessa assimetria: em baixa frequência vence quem tem menor queda
de condução (tiristor, IGBT); em alta frequência vence quem comuta mais rápido (MOSFET).

## 3. Perda de condução

### 3.1 Por que duas correntes, e não uma

Em condução, a característica $v$–$i$ de um dispositivo bipolar (diodo, tiristor, IGBT) não é
uma reta pela origem. A junção $p$–$n$ impõe uma barreira de potencial, de modo que existe uma
tensão de limiar abaixo da qual praticamente não há corrente, e acima da qual a queda cresce de
forma quase linear. O modelo linear por partes captura esse comportamento com dois parâmetros:

$$v(t) = V_{TO} + r_T \, i(t)$$

onde $V_{TO}$ é a **tensão de limiar**, ou seja, a interseção da reta ajustada com o eixo de tensão,
e $r_T$ a **resistência dinâmica**, a inclinação dessa reta. A Figura 2 do enunciado, reproduzida da
literatura, mostra exatamente essa construção: $r_T = 1/\tan\alpha$.

A potência instantânea é $p(t) = v(t)\,i(t)$, e a potência média em um período $T$ vale

$$P_{cond} = \frac{1}{T}\int_0^T v(t)\,i(t)\,dt
           = \frac{1}{T}\int_0^T V_{TO}\,i(t)\,dt + \frac{1}{T}\int_0^T r_T\,i^2(t)\,dt$$

O primeiro integrando é linear em $i$ e o segundo é quadrático. Reconhecendo as definições de
valor médio e valor eficaz,

$$\boxed{\;P_{cond} = V_{TO}\,I_{(av)} + r_T\,I_{(rms)}^2\;}$$

**É por isso que são necessários dois valores de corrente, e não um.** A parcela de limiar
"enxerga" quanta carga passou pelo dispositivo, que é uma informação de valor médio. A parcela
resistiva "enxerga" o aquecimento por efeito Joule, que é uma informação de valor eficaz. Um
projetista que use apenas a corrente média subestima a perda; um que use apenas a eficaz
superestima.

### 3.2 A forma alternativa com fator de forma

Quando a folha de dados ou o roteiro de projeto fornece apenas a corrente média, é comum escrever
a mesma expressão em função do **fator de forma**

$$a = \frac{I_{(rms)}}{I_{(av)}}$$

de onde resulta a forma usada na figura de referência do enunciado:

$$P_{cond} = V_{TO}\,I_{(av)} + r_T\,a^2\,I_{(av)}^2$$

As duas formas são idênticas, e a segunda apenas explicita que a razão entre eficaz e média é uma
propriedade da forma de onda, não do dispositivo. Alguns valores úteis:

| Forma de onda da corrente no dispositivo | $a = I_{rms}/I_{av}$ |
|---|---|
| Contínua (retangular, ciclo completo) | 1,00 |
| Retangular de razão cíclica $D$ | $1/\sqrt{D}$ |
| Semi-onda senoidal (condução de 180°) | $\pi/2 \approx 1{,}571$ |
| Retangular de 180° (carga muito indutiva) | $\sqrt{2} \approx 1{,}414$ |
| Triangular de razão cíclica $D$ | $2/\sqrt{3D}$ |

O fator de forma explica por que um retificador com filtro capacitivo castiga muito mais os diodos
do que um retificador com filtro indutivo, ainda que ambos entreguem a mesma corrente média: os
pulsos estreitos do primeiro elevam $a$ para valores acima de 3, e a parcela resistiva cresce com
o quadrado.

### 3.3 O caso do MOSFET

O MOSFET é a exceção ao modelo de dois parâmetros. Na região ôhmica ele se comporta como um
resistor puro, sem tensão de limiar, porque a condução se dá por portadores majoritários através
de um canal induzido, pois não há junção p-n polarizada diretamente no caminho da corrente. Com
$V_{TO} = 0$, a expressão colapsa em

$$P_{cond} = R_{DS(on)}\,I_{D(rms)}^2$$

e passa a depender **exclusivamente** do valor eficaz. Essa é uma diferença conceitual, não apenas
numérica: em correntes baixas o MOSFET dissipa muito menos que um IGBT de mesma classe de tensão,
porque a queda cai linearmente com a corrente em vez de estacionar em $V_{CE(sat)}$; em correntes
altas a situação se inverte, porque a perda cresce com $I^2$ em vez de $I$. O documento 06
quantifica essa fronteira.

## 4. Perda de comutação

### 4.1 A origem: sobreposição de tensão e corrente

Durante uma transição, o dispositivo não está nem plenamente ligado nem plenamente desligado. Por
um intervalo de dezenas ou centenas de nanossegundos, tensão e corrente são simultaneamente não
nulas, e o produto $v \cdot i$ atinge valores que podem superar em ordens de grandeza a potência
dissipada em condução. A energia perdida em uma transição é

$$E_{sw} = \int_{transição} v(t)\,i(t)\,dt$$

e a potência média resultante é essa energia multiplicada pelo número de transições por segundo:

$$P_{com} = E_{sw}\,f_s$$

Toda a modelagem de perdas de comutação consiste em estimar essa integral sem conhecer as formas
de onda exatas. E aqui entra o ponto que mais confunde: **o resultado depende do tipo de carga.**

### 4.2 Carga resistiva: o fator 1/6

Com carga resistiva, tensão e corrente variam *simultaneamente* durante a transição. Admitindo
variação linear, na entrada em condução tem-se, conforme as Eqs. (1.22) e (1.23) do livro-texto,

$$v(t) = V_{cc}\left(1 - \frac{t}{t_r}\right), \qquad i(t) = I_c\,\frac{t}{t_r}$$

de modo que

$$E_{ec} = \int_0^{t_r} V_{cc}\left(1-\frac{t}{t_r}\right) I_c \frac{t}{t_r}\,dt
        = V_{cc}I_c\,t_r\left(\frac{1}{2}-\frac{1}{3}\right) = \frac{V_{cc}I_c\,t_r}{6}$$

e, somando o bloqueio, resulta a Eq. (1.36) do livro:

$$P_{com} = \frac{1}{6}\,V_{DS}\,I_D\,(t_r + t_f)\,f_s \qquad \text{(carga resistiva)}$$

O fator $1/6$ vem da integral do produto de duas rampas de sentidos opostos. Não há nada de
arbitrário nele, mas ele **só vale para carga resistiva**, situação rara em eletrônica de
potência.

### 4.3 Carga indutiva grampeada: o modelo dos slides

Na esmagadora maioria dos conversores, como choppers, inversores e conversores CC-CC isolados, a
carga vista pela chave é indutiva e existe um diodo de roda livre grampeando o nó. Nesse caso a
sequência é outra:

- **Na entrada em condução**, a corrente na chave sobe de zero até $I_D$ *enquanto a tensão
  permanece em $V_{DS}$*, porque o diodo de roda livre só bloqueia depois que toda a corrente da
  indutância migrou para a chave. Só então a tensão cai.
- **No bloqueio**, a tensão sobe de $V_{DS(on)}$ até $V_{DS}$ *enquanto a corrente permanece em
  $I_D$*, porque a indutância impõe corrente constante até que o diodo de roda livre entre em
  condução. Só então a corrente cai.

Em ambos os casos a área sob $v \cdot i$ é a de um triângulo de altura $V_{DS}I_D$ e base igual ao
tempo de transição, ou seja, $E = \tfrac{1}{2}V_{DS}I_D\,t$, três vezes maior que no caso
resistivo. É esse o modelo dos slides de aula, com um acréscimo de 20 % nos tempos para cobrir os
atrasos de propagação e a dispersão entre amostras:

$$\boxed{\;P_{ec} = \frac{1}{2}\,V_{DS}\,I_D\,(1{,}2\,t_r)\,f_s, \qquad
P_{bloq} = \frac{1}{2}\,V_{DS}\,I_D\,(1{,}2\,t_f)\,f_s\;}$$

A razão entre os dois modelos, para os mesmos $t_r$ e $t_f$, é

$$\frac{P_{com}^{\text{indutiva}}}{P_{com}^{\text{resistiva}}}
= \frac{\tfrac{1}{2}(1{,}2)}{\tfrac{1}{6}} = 3{,}6$$

Um fator de 3,6 é a diferença entre um dissipador e um incêndio. **Sempre que houver diodo de roda
livre, o modelo dos slides é o correto.** O modelo de $1/6$ do livro fica reservado a cargas
efetivamente resistivas, e mesmo aí como limite inferior.

### 4.4 A parcela capacitiva, muitas vezes esquecida

Há uma terceira contribuição que nenhum dos dois modelos captura. A capacitância de saída do
dispositivo, $C_{oss}$ no MOSFET, armazena energia enquanto ele está bloqueado. Ao ligar, essa
energia é dissipada internamente no canal:

$$P_{cap} = \tfrac{1}{2}\,C_{o(er)}\,V_{DS}^2\,f_s$$

onde $C_{o(er)}$ é a capacitância **equivalente de energia**, e não o valor de $C_{oss}$ tabelado
a 25 V. A distinção é essencial: $C_{oss}$ é fortemente não linear e cai por uma ordem de grandeza
entre 25 V e 400 V. Em conversores de alta tensão, baixa corrente e frequência elevada, que é
exatamente o caso do primário da Parte 2, essa parcela pode superar a perda de cruzamento. Ela é
quantificada no documento 11.

## 5. Perda de comando

O item 8 da chave ideal é violado de duas maneiras distintas:

**Dispositivos controlados por corrente** (tiristor, TRIAC, transistor bipolar) exigem que o
circuito de comando injete corrente pelo terminal de controle. No tiristor, a perda de porta é

$$P_G = V_{GT}\,I_{GT}\,\delta_G$$

com $\delta_G$ a razão cíclica do pulso de disparo. Para os valores típicos de catálogo em 60 Hz,
essa parcela é da ordem de miliwatts e sempre desprezível frente à condução. O custo real do
comando por corrente está no *driver*, não no dispositivo.

**Dispositivos controlados por tensão** (MOSFET, IGBT) não drenam corrente contínua de porta, mas
exigem que a carga de porta $Q_g$ seja movida a cada comutação. A potência que o *driver* fornece é

$$P_{drive} = Q_g\,V_{GS}\,f_s$$

e é dissipada nas resistências de porta e na saída do *driver*, **não no dispositivo**. Ela conta
para o rendimento do conversor e para o dimensionamento da fonte auxiliar, mas não entra no
cálculo térmico do semicondutor de potência. Para o IRFP460A ($Q_g = 105$ nC) comutando a 100 kHz
com $V_{GS} = 15$ V, resultam $P_{drive} = 158$ mW por chave.

## 6. Perda de estado bloqueado

Bloqueado, o dispositivo sustenta a tensão do circuito enquanto conduz apenas a corrente de fuga
$I_R$ da junção reversamente polarizada. A perda é $P_{off} = V_R\,I_R\,(1-D)$.

Para o diodo MBR20200CT, por exemplo, a folha de dados especifica $I_R \le 1{,}0$ mA a 25 °C sob
200 V, o que dá 0,2 W, valor já perceptível. A 125 °C, porém, o limite sobe para 50 mA, e a perda
nominal saltaria para 10 W. Esse crescimento exponencial da fuga com a temperatura é o mecanismo
da **fuga térmica** (*thermal runaway*) que limita o uso de diodos Schottky de alta tensão em
temperatura elevada.

Na prática, os valores *típicos* são três ordens de grandeza menores que os máximos de catálogo
(0,2 µA e 0,4 mA, respectivamente, para o mesmo dispositivo), e para dispositivos de silício com
junção $p$–$n$ a fuga é ainda menor. **Adota-se neste trabalho $P_{off} \approx 0$**, com a
ressalva explícita de que a hipótese deve ser revista em projetos com Schottky de alta tensão
operando acima de 100 °C.

## 7. Da perda ao calor: o encadeamento térmico

Calcular a perda não é um fim em si. O objetivo é responder a duas perguntas: *o dispositivo
sobrevive?* e *que dissipador é necessário?* O caminho é o circuito térmico equivalente
apresentado nos slides, no qual a potência dissipada faz o papel da corrente, a temperatura o da
tensão, e as resistências térmicas o das resistências elétricas:

$$T_j \;\xrightarrow{\;R_{th,jc}\;}\; T_c \;\xrightarrow{\;R_{th,cd}\;}\; T_d
\;\xrightarrow{\;R_{th,da}\;}\; T_a$$

Percorrendo o circuito a partir da junção:

$$T_c = T_j - P_{av}R_{th,jc}, \qquad T_d = T_c - P_{av}R_{th,cd}, \qquad
T_a = T_d - P_{av}R_{th,da}$$

de onde se extrai a incógnita de projeto, a resistência térmica do dissipador:

$$R_{th,da} = \frac{T_d - T_a}{P_{av}}$$

Os slides fixam as convenções de projeto: $R_{th,jc}$ vem do catálogo do semicondutor,
$R_{th,cd} \approx 0{,}5$ °C/W para isolador de mica ou silicone, $T_j$ escolhida entre 100 °C e
120 °C, bem abaixo do limite de catálogo, como margem, e $T_a$ entre 25 °C e 70 °C conforme o
ambiente. Quando vários dispositivos compartilham o mesmo dissipador, calcula-se $T_d$ para cada
um e adota-se **o menor valor**, dividindo-o pela soma de todas as potências:

$$R_{th,da} = \frac{T_{d,\min} - T_a}{P_1 + P_2 + \cdots + P_n}$$

O documento 06 desenvolve esse cálculo em detalhe e o aplica aos exemplos de cada dispositivo.

## 8. Roteiro geral de cálculo

Consolidando, o procedimento que será repetido nos documentos 02 a 05 tem sempre os mesmos sete
passos:

1. **Identificar a forma de onda** de tensão e de corrente no dispositivo, a partir da topologia e
   do ponto de operação, e não da folha de dados.
2. **Calcular $I_{(av)}$ e $I_{(rms)}$** sobre o período completo de operação.
3. **Extrair os parâmetros de condução** ($V_{TO}$ e $r_T$, ou $R_{DS(on)}$, ou $V_{CE(sat)}$) da
   folha de dados, **corrigidos para a temperatura de junção de operação**.
4. **Calcular $P_{cond}$**.
5. **Extrair os parâmetros dinâmicos** ($t_r$, $t_f$, $Q_{rr}$, $E_{on}$, $E_{off}$) e calcular
   $P_{com}$ com o modelo adequado ao tipo de carga.
6. **Somar** e verificar contra as classificações de catálogo.
7. **Fechar o circuito térmico** e dimensionar o dissipador.

O passo 3 merece ênfase. Os slides são explícitos ao exigir que $R_{DS(on)}$ seja corrigida para
100 °C usando a curva normalizada do catálogo, e que $V_{TO}$ e $r_T$ sejam tomados a 125 °C.
Usar valores de 25 °C é o erro mais comum e o mais caro: para um MOSFET de 500 V, a resistência de
canal a 100 °C é cerca de 45 % maior que a de 25 °C, e a perda de condução cresce na mesma
proporção. O projeto que ignora isso dimensiona um dissipador insuficiente e descobre o problema
apenas no ensaio térmico.

---

**Próximo documento:** [02. Diodo de potência](02-diodo-de-potencia.md)
