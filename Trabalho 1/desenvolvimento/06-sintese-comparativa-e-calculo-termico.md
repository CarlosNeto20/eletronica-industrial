# 06. Síntese Comparativa e Cálculo Térmico

Este documento fecha a Parte 1 reunindo as expressões dos quatro dispositivos em uma única grade,
desenvolvendo o cálculo térmico que transforma perda em dissipador, e respondendo
quantitativamente à pergunta que o projetista faz na prática: **qual dispositivo escolher?**

## 1. Grade unificada das expressões

### 1.1 Perdas de condução

| Dispositivo | Modelo do estado ligado | Expressão | Correntes necessárias |
|---|---|---|---|
| **Diodo** | Fonte de tensão + resistência | $V_{TO}I_{F(av)} + r_T I_{F(rms)}^2$ | média e eficaz |
| **Tiristor / TRIAC** | Fonte de tensão + resistência | $V_{TO}I_{T(av)} + r_T I_{T(rms)}^2$ | média (de $\|i\|$) e eficaz |
| **MOSFET** | Resistência pura | $R_{DS(on)}(T_j)\,I_{D(rms)}^2$ | apenas eficaz |
| **IGBT** | Fonte de tensão pura | $V_{CE(sat)}I_{C(av)}$ | apenas média |

A coluna da direita é a que mais confunde na hora de calcular, e resume uma diferença física real:
onde há junção $p$–$n$ polarizada diretamente, existe tensão de limiar e a corrente média importa;
onde a condução é por canal resistivo, importa apenas o valor eficaz.

### 1.2 Perdas de comutação

| Dispositivo | Entrada em condução | Bloqueio | Observação |
|---|---|---|---|
| **Diodo** | $\approx 0$ | $\tfrac{1}{2}Q_{rr}V_R f_s$ | Limite conservador: $Q_{rr}V_R f_s$ |
| **Tiristor / TRIAC** | $\tfrac{1}{2}V_{AK}I_T t_{on}f_s$ | $\tfrac{1}{2}Q_{rr}V_R f_s$ | Ambas desprezíveis em 60 Hz |
| **MOSFET** | $\tfrac{1}{2}V_{DS}I_D(1{,}2t_r)f_s$ | $\tfrac{1}{2}V_{DS}I_D(1{,}2t_f)f_s$ | Somar $\tfrac{1}{2}C_{o(er)}V^2 f_s$ |
| **IGBT** | $\tfrac{1}{2}V_{CE}I_C(1{,}2t_r)f_s$ | $\tfrac{1}{2}V_{CE}I_C(1{,}2t_f)f_s$ | Preferir $(E_{on}+E_{off})f_s$; o modelo linear subestima ~40 % |

### 1.3 O que cada dispositivo viola da chave ideal

Retomando a grade de leitura do documento 01:

| Característica ideal | Diodo | Tiristor / TRIAC | MOSFET | IGBT |
|---|---|---|---|---|
| Queda de condução nula | $V_{TO} + r_T i$ | $V_{TO} + r_T i$ | $R_{DS(on)}i$ | $V_{CE(sat)}$ |
| Bloqueio perfeito | fuga µA | fuga µA | fuga µA | fuga µA |
| Bidirecional em corrente | não | SCR não / TRIAC sim | não (diodo de corpo conduz) | não |
| Bloqueio bidirecional em tensão | sim | SCR sim / TRIAC sim | não (diodo de corpo) | sim |
| Comutação instantânea | $t_{rr}$ | $t_q$ | $t_r$, $t_f$ | $t_r$, $t_f$ + cauda |
| Controle das duas transições | nenhuma | só entrada em condução | ambas | ambas |
| Comando sem potência | não requer | $I_{GT}$ (corrente) | $Q_g$ (carga) | $Q_g$ (carga) |
| Faixa de frequência prática | até GHz (Schottky) | $< 1$ kHz | $10$ kHz – $1$ MHz | $2$ – $20$ kHz |

## 2. Cálculo térmico

### 2.1 A analogia e o circuito

O calor gerado na junção precisa escoar até o ambiente através de uma sequência de resistências
térmicas. A analogia com o circuito elétrico é exata:

| Grandeza térmica | Análogo elétrico | Unidade |
|---|---|---|
| Potência dissipada $P$ | Corrente | W |
| Temperatura $T$ | Tensão | °C |
| Resistência térmica $R_{th}$ | Resistência | °C/W |
| Capacitância térmica $C_{th}$ | Capacitância | J/°C |

O circuito em regime permanente, conforme os slides, é uma cadeia série:

```
  P_av
   |
   v
  [Tj] --Rth,jc--> [Tc] --Rth,cd--> [Td] --Rth,da--> [Ta]
 junção            cápsula          dissipador       ambiente
```

com as quatro grandezas assim caracterizadas:

| Símbolo | Significado | Origem |
|---|---|---|
| $R_{th,jc}$ | junção–cápsula | Catálogo do semicondutor |
| $R_{th,cd}$ | cápsula–dissipador | Catálogo do isolante (mica ou silicone); adotar 0,5 °C/W |
| $R_{th,da}$ | dissipador–ambiente | **Incógnita do projeto** |
| $T_j$ | temperatura de junção | Escolhida pelo projetista entre 100 °C e 120 °C |
| $T_a$ | temperatura ambiente | Escolhida entre 25 °C e 70 °C conforme o local |

### 2.2 O procedimento

Percorrendo a cadeia a partir da junção, conforme as expressões dos slides:

$$T_c = T_j - P_{av}\,R_{th,jc}$$
$$T_d = T_c - P_{av}\,R_{th,cd}$$
$$R_{th,da} = \frac{T_d - T_a}{P_{av}}$$

Duas observações sobre as escolhas de $T_j$ e $T_a$:

**$T_j$ entre 100 °C e 120 °C** é uma margem deliberada. O catálogo permite 150 °C (175 °C em
alguns diodos), mas projetar no limite significa nenhuma tolerância para envelhecimento do
dissipador, obstrução do fluxo de ar, sobrecarga temporária ou dispersão de fabricação. A regra
prática, que o projeto do retificador monofásico da mesma disciplina adotou, é usar 80 % do limite
de catálogo.

**$T_a$ é a temperatura dentro do gabinete**, não a da sala. Um equipamento fechado operando em
ambiente de 25 °C tem facilmente 50 a 60 °C internos. Usar 25 °C é o erro mais comum, e o mais
caro, do cálculo térmico.

### 2.3 Vários dispositivos no mesmo dissipador

É a situação normal em conversores. Os slides apresentam o procedimento correto:

1. Calcular, para **cada** dispositivo $k$, a temperatura de dissipador que ele exige:
$$T_{d,k} = T_{j,k} - P_{k}\left(R_{th,jc,k} + R_{th,cd,k}\right)$$
2. Tomar **o menor** valor entre todos: $T_d = \min\{T_{d,1}, \ldots, T_{d,n}\}$;
3. Dividir pela **soma** de todas as potências:
$$\boxed{\;R_{th,da} = \frac{T_d - T_a}{P_1 + P_2 + \cdots + P_n}\;}$$

A lógica é direta: o dissipador é um só e tem uma única temperatura; ela precisa ser baixa o
bastante para o dispositivo mais exigente, e precisa escoar o calor de todos.

O erro clássico aqui é dividir a resistência pelo número de dispositivos ($R_{th,da}/n$), o que só
é válido no caso particular em que todos dissipam a mesma potência e têm as mesmas resistências
térmicas.

### 2.4 Exemplo 7. Dissipador de uma ponte retificadora mista

Considere um retificador semicontrolado, do tipo apresentado nos slides, com dois tiristores
TYN1225 e dois diodos SKKD 46, alimentando a mesma carga do Exemplo 3 ($I_o = 15$ A contínuos), com
$T_a = 40$ °C.

**Perdas.** Recalculando para $I_o = 15$ A:

- Tiristores: $I_{T(av)} = 7{,}50$ A, $I_{T(rms)} = 10{,}607$ A →
  $P_{Th} = 0{,}77(7{,}50) + 0{,}014(10{,}607)^2 = 7{,}350$ W cada;
- Diodos: $I_{F(av)} = 7{,}50$ A, $I_{F(rms)} = 10{,}607$ A →
  $P_{D} = 0{,}85(7{,}50) + 0{,}005(10{,}607)^2 = 6{,}375 + 0{,}563 = 6{,}938$ W cada.

**Temperaturas de dissipador exigidas.** Com $T_{j} = 110$ °C para ambos (limite do TYN1225 é
125 °C; do SKKD 46, 125 °C) e $R_{th,cd} = 0{,}5$ °C/W:

$$T_{d,Th} = 110 - 7{,}350\,(2{,}0 + 0{,}5) = 110 - 18{,}4 = 91{,}6\ ^\circ\text{C}$$
$$T_{d,D} = 110 - 6{,}938\,(0{,}6 + 0{,}5) = 110 - 7{,}6 = 102{,}4\ ^\circ\text{C}$$

**O tiristor é o dispositivo dimensionante**, apesar de dissipar apenas 6 % a mais que o diodo,
porque a sua resistência térmica junção-cápsula é mais de três vezes maior. Adota-se
$T_d = 91{,}6$ °C.

**Resistência do dissipador.**

$$P_{total} = 2 \times 7{,}350 + 2 \times 6{,}938 = 28{,}58\ \text{W}$$
$$R_{th,da} = \frac{91{,}6 - 40}{28{,}58} = 1{,}81\ ^\circ\text{C/W}$$

**Verificação.** Com o dissipador escolhido, a temperatura real de cada junção é

$$T_d = 40 + 28{,}58 \times 1{,}81 = 91{,}7\ ^\circ\text{C}$$
$$T_{j,Th} = 91{,}7 + 7{,}350 \times 2{,}5 = 110{,}1\ ^\circ\text{C} \quad\checkmark$$
$$T_{j,D} = 91{,}7 + 6{,}938 \times 1{,}1 = 99{,}3\ ^\circ\text{C} \quad\checkmark$$

Ambas abaixo do limite de projeto, com o tiristor no valor de dimensionamento e o diodo com folga
de 11 °C. Resultado coerente.

### 2.5 O que o modelo em regime permanente não captura

O circuito de resistências puras vale para dissipação constante. Duas situações exigem mais:

**Transitórios.** Sob sobrecarga breve ou pulso de partida, a capacitância térmica do sistema
limita a elevação. O parâmetro adequado é a **impedância térmica transitória** $Z_{th(t)}$,
fornecida em curva pelos fabricantes, que tende a $R_{th}$ para tempos longos e é muito menor para
pulsos curtos. É por isso que um diodo com $I_{F(AV)} = 45$ A suporta $I_{FSM} = 700$ A por 10 ms.

**Coordenação com fusível.** O parâmetro $I^2t$ do semicondutor precisa ser **maior** que o do
fusível de proteção, para que o fusível atue antes de a junção fundir. Para o SKKD 46,
$I^2t = 2450$ A²s a 10 ms; qualquer fusível ultrarrápido escolhido para esse ramo precisa ter
$I^2t$ inferior a esse valor.

## 3. A fronteira MOSFET × IGBT

### 3.1 O critério

Este é o cálculo que decide o projeto na prática. Igualando as perdas totais dos dois dispositivos
no mesmo ponto de operação, com $D$ a razão cíclica, $V$ a tensão de barramento, $I$ a corrente
comutada e $f_s$ a frequência:

$$\underbrace{R_{DS(on)}D\,I^2 + 0{,}6\,V(t_r+t_f)f_s\,I}_{\text{MOSFET}}
\;=\;
\underbrace{V_{CE(sat)}D\,I + e_{sw}f_s\,I}_{\text{IGBT}}$$

onde $e_{sw} = (E_{on}+E_{off})/I^{cat}$ é a energia de comutação por ampère. Dividindo tudo por
$I$, já que as parcelas do IGBT são todas lineares em $I$ e a de condução do MOSFET é quadrática:

$$\boxed{\;I_{cruz} = \frac{V_{CE(sat)}D + e_{sw}f_s - 0{,}6\,V(t_r+t_f)f_s}{R_{DS(on)}\,D}\;}$$

**Abaixo de $I_{cruz}$ o MOSFET vence; acima, o IGBT.**

### 3.2 Aplicação numérica

Comparando o **SPW20N60C3** (CoolMOS 650 V; $R_{DS(on)} = 0{,}285$ Ω a 100 °C; $t_r = 5$ ns,
$t_f = 4{,}5$ ns) com o **IRG4PC40UD** (IGBT 600 V; $V_{CE(sat)} = 1{,}72$ V;
$e_{sw} = 1{,}06\ \text{mJ}/20\ \text{A} = 53$ µJ/A), em $V = 400$ V e $D = 0{,}5$:

| $f_s$ | $I_{cruz}$ | Perda no cruzamento |
|---|---|---|
| 2 kHz | 6,75 A | 6,5 W |
| 5 kHz | 7,81 A | 8,8 W |
| 10 kHz | 9,59 A | 13,3 W |
| 20 kHz | 13,15 A | 25,3 W |
| 50 kHz | 23,83 A | 83,7 W |
| 100 kHz | 41,63 A | 256,4 W |

E a varredura em corrente a 20 kHz:

| $I$ | $P_{MOSFET}$ | $P_{IGBT}$ | Vencedor |
|---|---|---|---|
| 2 A | 0,66 W | 3,84 W | MOSFET |
| 5 A | 3,79 W | 9,60 W | MOSFET |
| 8 A | 9,48 W | 15,36 W | MOSFET |
| 10 A | 14,71 W | 19,20 W | MOSFET |
| 13 A | 24,68 W | 24,96 W | **empate** |
| 15 A | 32,75 W | 28,80 W | IGBT |
| 20 A | 57,91 W | 38,40 W | IGBT |
| 30 A | 129,62 W | 57,60 W | IGBT |

### 3.3 Leitura do resultado

Três conclusões, e a terceira é contra-intuitiva:

**Em corrente baixa o MOSFET é imbatível.** A 2 A ele dissipa seis vezes menos que o IGBT, porque
$R_{DS(on)}I^2$ cai com o quadrado enquanto $V_{CE(sat)}I$ cai apenas linearmente. A tensão de
limiar do IGBT é um custo fixo que não desaparece em carga leve, motivo pelo qual o IGBT tem
rendimento ruim a carga parcial.

**Em corrente alta o IGBT é imbatível.** A 30 A o MOSFET dissiparia 130 W, contra 58 W do IGBT. É
a lei $R_{DS(on)} \propto V_{BR}^{2{,}4}$ cobrando o seu preço.

**A fronteira se desloca para cima com a frequência.** A 2 kHz o MOSFET só vence até 6,75 A; a
100 kHz ele vence até 41,6 A. Isso parece invertido à primeira vista, já que a alta frequência é
tida como território do MOSFET. E é justamente o que a tabela diz: quanto maior a frequência, **mais
severamente a energia de comutação do IGBT o penaliza**, e maior é a faixa de corrente em que o
MOSFET compensa a sua pior condução com a sua comutação muito mais rápida. O que a tabela também
mostra, na coluna da direita, é que a partir de 50 kHz a perda no ponto de cruzamento já é tão alta
(84 W, 256 W) que **nenhum dos dois é utilizável nessa corrente**, de modo que a comparação perde
sentido prático, e a resposta correta passa a ser mudar de topologia (comutação suave) ou de
tecnologia (SiC, GaN).

### 3.4 Regra prática consolidada

| Faixa | Escolha natural | Razão dominante |
|---|---|---|
| $< 1$ kHz, qualquer corrente | Tiristor / TRIAC | Menor queda em condução, menor custo por ampère |
| 2 a 20 kHz, $I > 15$ A, $V > 400$ V | IGBT | Condução por portadores minoritários |
| 10 a 200 kHz, $I < 15$ A | MOSFET | Comutação rápida, sem cauda |
| $V < 200$ V, qualquer corrente | MOSFET | $R_{DS(on)}$ baixa nessa classe de tensão |
| $> 100$ kHz com $V > 400$ V | MOSFET de superjunção, SiC ou GaN | $Q_{rr}$ nulo e $R_{DS(on)}$ deslocada |

## 4. Consolidação dos exemplos numéricos da Parte 1

| # | Dispositivo | Aplicação | $f_s$ | $P_{cond}$ | $P_{com}$ | Total | Comutação |
|---|---|---|---|---|---|---|---|
| 1 | SKKD 46/16 (diodo) | Ponte 60 Hz, 30 A | 60 Hz | 15,00 W | ~0 | 15,00 W | ~0 % |
| 2 | DSEI2×31-06C (FRED) | Boost 1 kW | 50 kHz | 2,85 W | 7,44 W | 10,29 W | 72 % |
| 3 | TYN1225 (SCR) | Retificador controlado 15 A | 60 Hz | 7,35 W | 1,05 W | 8,40 W | 12,5 % |
| 4 | BTA41-600B (TRIAC) | Controlador CA 2,4 kW | 60 Hz | 12,32 W | ~0 | 12,32 W | ~0 % |
| 5 | IRFP460A (MOSFET) | Buck 200 V / 8 A | 50 kHz | 12,53 W | 4,51 W | 17,04 W | 26 % |
| 6 | IRG4PC40UD (IGBT) | Braço de inversor 400 V / 20 A | 10 kHz | 17,20 W | 10,60 W | 27,80 W | 38 % |

A coluna da direita conta a história inteira da Parte 1: **a fração de comutação cresce
monotonicamente com a frequência**, de zero em 60 Hz a mais de 70 % em 50 kHz. Ela é a variável de
projeto que separa as famílias de dispositivos, e é o que justifica dedicar tanto esforço a
modelar corretamente uma perda que dura nanossegundos.

## 5. Roteiro de dimensionamento consolidado

1. Definir topologia e ponto de operação; **desenhar as formas de onda** de $v$ e $i$ no
   dispositivo.
2. Calcular $I_{(av)}$ e $I_{(rms)}$ **sobre o período completo**.
3. Escolher a família de dispositivo pela frequência e pela corrente (Seção 3.4).
4. Verificar as margens de catálogo: $V_{max} \ge 1{,}3\,PIV$; $I$ nominal **a 100 °C**.
5. Extrair os parâmetros de condução **corrigidos para $T_j$ de operação** e calcular $P_{cond}$.
6. Extrair os parâmetros dinâmicos e calcular $P_{com}$ com o modelo adequado à carga; para IGBT,
   preferir as energias de catálogo.
7. Somar e obter $P_{total}$ por dispositivo.
8. Fechar o circuito térmico; se houver vários dispositivos no mesmo dissipador, aplicar o critério
   do menor $T_d$.
9. Escolher o perfil comercial com $R_{th,da}$ igual ou inferior ao calculado e **recalcular
   $T_j$ real** para verificação.
10. Verificar $I_{FSM}$, $I^2t$, $di/dt$ e $dv/dt$, restrições que não são perdas mas podem
    inviabilizar a escolha.

---

**Documento anterior:** [05. IGBT de potência](05-igbt-de-potencia.md)
**Próximo documento:** [07. Fundamentos de magnéticos em alta frequência](07-fundamentos-de-magneticos-em-alta-frequencia.md)
