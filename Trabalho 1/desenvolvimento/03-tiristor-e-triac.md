# 03. Tiristor e TRIAC de Potência

O tiristor introduz uma categoria que não existia no diodo: o dispositivo **semicontrolado**. É
possível decidir quando ele entra em condução, mas não quando ele sai, porque o bloqueio depende
do circuito. Essa assimetria explica tanto o domínio histórico do tiristor em conversores de grande
porte quanto a sua limitação a frequências abaixo de 1 kHz.

## 1. Características básicas

### 1.1 Estrutura e a família tiristor

O termo *tiristor* designa genericamente um semicondutor de quatro ou mais camadas com estrutura
$p$–$n$–$p$–$n$. A taxonomia do livro-texto organiza a família pelos terminais de controle:

| Conexões ôhmicas | Denominação | Exemplo |
|---|---|---|
| Apenas às camadas externas | Tiristor diodo | DIAC |
| Mais uma camada intermediária | Tiristor tríodo | SCR, TRIAC, GTO |
| Às duas camadas intermediárias | Tiristor tetrodo | SCS |

E pela característica reversa:

| Característica reversa | Dispositivos |
|---|---|
| Bloqueante (como um diodo) | SCR simétrico |
| Condutora | SCR assimétrico, GTO |
| Imagem espelhada da direta | DIAC, TRIAC (bidirecionais) |

O membro mais simples e mais comum é o **retificador controlado de silício** (SCR), um tiristor
tríodo com bloqueio reverso, de três terminais: anodo (A), catodo (K) e porta ou *gate* (G). O mais
complexo dos de uso corrente é o **TRIAC**, tiristor tríodo bidirecional.

### 1.2 Curva característica do SCR

O SCR tem quatro junções de interesse ($J_1$, $J_2$, $J_3$) e três estados:

**Bloqueio reverso.** Com o anodo negativo, $J_1$ e $J_3$ ficam reversamente polarizadas e $J_2$
diretamente. O dispositivo sustenta a tensão reversa como um diodo.

**Bloqueio direto.** Com o anodo positivo e a porta aberta, $J_1$ e $J_3$ ficam diretamente
polarizadas e **$J_2$ reversamente**. O dispositivo sustenta a tensão direta. *Essa é a
propriedade que define a família tiristor*, pois nenhum outro dispositivo de potência bloqueia
tensão direta com polarização direta aplicada.

**Condução.** Elevando a tensão direta até $V_{BO}$ (tensão de *breakover*), $J_2$ rompe e o
dispositivo conduz como um diodo. Na prática, jamais se dispara um SCR por *breakover*: injeta-se
corrente de porta, o que reduz $V_{BO}$ progressivamente até que o disparo ocorra na tensão de
operação.

### 1.3 O modelo de dois transistores e o travamento

O comportamento do SCR é elegantemente explicado pelo modelo de dois transistores acoplados: um
PNP ($Q_1$) e um NPN ($Q_2$), com o coletor de cada um alimentando a base do outro. Com a porta
aberta, ambos estão cortados e circula apenas a corrente de fuga. Um pulso positivo de corrente na
porta torna-se corrente de base de $Q_2$; o coletor de $Q_2$ fornece corrente de base a $Q_1$;
o coletor de $Q_1$ realimenta a base de $Q_2$, e assim por diante. **A realimentação positiva
sustenta a condução mesmo depois que o sinal de porta é retirado**, e o dispositivo "travou".

Daí decorrem as três consequências práticas que governam o projeto:

1. **A porta perde o controle após o disparo.** O único modo de bloquear é levar a corrente de
   anodo abaixo da **corrente de manutenção** $I_H$.
2. **O pulso de porta pode ser curto**, desde que a corrente de anodo ultrapasse a **corrente de
   travamento** $I_L$ antes de o pulso terminar. Com carga indutiva, em que a corrente sobe
   lentamente, o pulso precisa ser longo ou repetitivo (trem de pulsos).
3. **O disparo é sempre por corrente**, nunca por tensão. Os slides são explícitos: pré-requisitos
   do disparo são $V_{AK} > 0{,}7$ V *e* corrente de porta $I_{GT}$ recomendada pelo fabricante.

### 1.4 TRIAC

O TRIAC é bidirecional em corrente e em tensão, funcionalmente equivalente a dois SCR em
antiparalelo com porta comum. Por não haver anodo e catodo definidos, seus terminais principais
chamam-se MT1 e MT2. A curva característica é a imagem espelhada de si mesma nos dois quadrantes.

Os slides listam as suas características de uso:

- É bidirecional em corrente e tensão;
- Opera em baixa frequência ($< 1$ kHz);
- É controlado por corrente de porta $I_{GT}$;
- **Necessita de disparo a cada semiciclo**, com $V_{MT2-MT1} > 0{,}7$ V e $I_{GT}$;
- O bloqueio ocorre naturalmente na passagem por zero da corrente; **não é possível bloquear pela
  porta**.

Os dois métodos de acionamento têm consequências opostas em qualidade de energia:

| Método | Como funciona | Consequência |
|---|---|---|
| **Controle de fase** | Ângulos de disparo de 0° a 180° no semiciclo positivo e de 180° a 360° no negativo | Controle contínuo da potência, mas **elevado conteúdo harmônico** na corrente de entrada |
| **Comutação no cruzamento por zero** | O disparo sempre ocorre no cruzamento por zero da tensão; o controle é feito pelo número de ciclos completos entregues | **Injeção de harmônicas muito reduzida**, mas o controle é discreto e produz cintilação em cargas rápidas |

Há circuitos integrados dedicados para ambos: MOC3020/3021/3022/3023 e TCA 785 para controle de
fase; MOC3063 e similares, com detecção interna de cruzamento por zero, para o segundo método.

### 1.5 Por que a frequência é limitada

Os slides classificam SCR e TRIAC como dispositivos de "baixa frequência ($< 1$ kHz)". A razão é
quantitativa e está no **tempo de recuperação comutada** $t_q$, que é o intervalo, medido a partir
do cruzamento por zero da corrente, de que o dispositivo precisa para recuperar a capacidade de
bloqueio direto. O livro-texto classifica:

- SCR de rede (*converter grade*): $t_q > 50$ µs;
- SCR de inversor (*inverter grade*): $t_q < 20$ µs.

Em 60 Hz o semiperíodo é de 8,33 ms, e um $t_q$ de 50 µs consome 0,6 % dele, o que é irrelevante. A
1 kHz o semiperíodo cai para 500 µs e o mesmo $t_q$ já consome 10 %. Acima disso, o dispositivo
simplesmente não recupera a tempo, e uma tensão direta reaplicada com $dv/dt$ elevado o redispara.

Esse é também o mecanismo do **efeito $dv/dt$**: a corrente de fuga através da capacitância da
junção $J_2$ vale $i = C\,dv/dt$; se ela superar a corrente de travamento, o SCR dispara sozinho,
sem corrente de porta. Os limites típicos são de 200 a 500 V/µs para SCR e chegam a 750 V/µs para
o TRIAC BTA41-600B a 125 °C. Circuitos *snubber* RC em paralelo com o dispositivo servem
precisamente para limitar esse $dv/dt$, e são obrigatórios em TRIAC com carga indutiva, na qual a
tensão reaparece abruptamente no bloqueio.

## 2. Princípio de polarização

**Entrada em condução do SCR.** Pré-requisitos simultâneos: (i) tensão anodo-catodo positiva,
maior que 0,7 V; (ii) corrente de porta igual ou superior a $I_{GT}$ de catálogo, mantida até que
a corrente de anodo ultrapasse $I_L$. Após o travamento, o pulso pode ser retirado.

**Bloqueio do SCR.** Ocorre **naturalmente** quando a corrente de anodo cai abaixo da corrente de
manutenção $I_H$, o que em conversores ligados à rede acontece na passagem natural por zero. Não é
possível bloquear pela porta. Em conversores alimentados por fonte contínua é preciso um circuito
de **comutação forçada**, que impõe artificialmente a inversão da corrente. Essa foi uma solução
historicamente importante, hoje abandonada em favor de GTO, IGCT e IGBT.

**TRIAC.** O mesmo, com a diferença de que o processo se repete a cada semiciclo e que a corrente
de porta é sempre positiva, independentemente do sentido da corrente principal (no modo de disparo
mais comum, referido a MT1).

## 3. Perdas de condução

### 3.1 A expressão

Em condução o tiristor comporta-se como um diodo: junção $p$–$n$ diretamente polarizada, com
tensão de limiar e resistência dinâmica. O livro-texto é explícito ao afirmar que "a potência
dissipada em um tiristor é calculada da mesma forma que a do diodo", acrescentando apenas a perda
de porta. Portanto:

$$\boxed{\;P_{cond} = V_{TO}\,I_{T(av)} + r_T\,I_{T(rms)}^2\;}$$

com $V_{TO}$ e $r_T$ tomados na temperatura de junção quente. Para o TRIAC, cuja corrente é
bidirecional, $I_{T(av)}$ deve ser entendido como o **valor médio do módulo** da corrente, já que
a queda $V_{TO}$ se opõe à circulação nos dois sentidos:

$$I_{T(av)} = \frac{1}{T}\int_0^T |i_T(t)|\,dt$$

Essa é uma sutileza que passa despercebida com frequência: o valor médio da corrente de um TRIAC
em controle de fase simétrico é *zero*, e usá-lo levaria à conclusão absurda de que a parcela de
limiar não dissipa.

### 3.2 Extração dos parâmetros

Ao contrário do que ocorre com muitos diodos, as folhas de dados de tiristores e TRIAC costumam
fornecer $V_{TO}$ e $r_T$ diretamente, porque o cálculo térmico é parte do fluxo normal de projeto
desses dispositivos. Os dois componentes usados neste trabalho:

| Componente | $V_{TO}$ | $r_T$ | Condição | $R_{th,jc}$ | $T_{j,max}$ |
|---|---|---|---|---|---|
| **TYN1225** (SCR, 1200 V / 25 A) | 0,77 V | 14 mΩ | $T_j = 125$ °C | 2,0 °C/W | 125 °C |
| **BTA41-600B** (TRIAC, 600 V / 40 A) | 1,063 V | 7,4 mΩ | curva da Fig. 10 | 0,9 K/W | 150 °C |

Note que o TRIAC tem tensão de limiar **maior** e resistência dinâmica **menor** que o SCR de
corrente comparável. A tensão de limiar maior é o preço estrutural da bidirecionalidade: a corrente
atravessa mais junções.

### 3.3 Exemplo 3. Retificador monofásico controlado com TYN1225

**Circuito.** Ponte monofásica totalmente controlada, 220 V / 60 Hz, alimentando carga fortemente
indutiva que drena $I_o = 15$ A contínuos. Cada tiristor conduz 180° por período,
independentemente do ângulo de disparo $\alpha$.

**Passos 1 e 2, formas de onda e valores característicos.**

$$I_{T(av)} = \frac{I_o}{2} = 7{,}50\ \text{A}, \qquad
I_{T(rms)} = \frac{I_o}{\sqrt{2}} = 10{,}607\ \text{A}$$

**Passos 3 e 4, perda de condução.**

$$P_{cond} = 0{,}77 \times 7{,}50 + 0{,}014 \times 10{,}607^2 = 5{,}775 + 1{,}575 = 7{,}350\ \text{W}$$

Aqui a repartição é de 79 % para o limiar e 21 % para a parcela resistiva, porque a resistência
dinâmica do TYN1225 (14 mΩ) é quase três vezes a do SKKD 46 (5 mΩ), o que faz o termo quadrático
pesar mais.

**Passo 5, perda de comando.** Com $V_{GT} = 1{,}3$ V, $I_{GT} = 40$ mA de catálogo e pulso de
200 µs a cada ciclo de 60 Hz:

$$P_G = V_{GT}\,I_{GT}\,(t_g f) = 1{,}3 \times 0{,}040 \times (200\ \mu\text{s} \times 60)
= 0{,}62\ \text{mW}$$

Absolutamente desprezível, como antecipado no documento 01.

**Passo 6, perdas de comutação.** As duas parcelas merecem tratamento separado.

*Entrada em condução.* No instante do disparo, a tensão anodo-catodo é a tensão da rede naquele
ângulo: para $\alpha = 60°$, $V_{AK} = \sqrt{2}\times 220 \times \sin 60° = 269{,}4$ V. Admitindo
tempo de espalhamento da condução $t_{on} \approx 2$ µs, que é a ordem de grandeza típica de SCR de
rede e não um valor de catálogo do TYN1225, e modelo de carga indutiva:

$$P_{ec} = \tfrac{1}{2}\,V_{AK}\,I_o\,t_{on}\,f
= \tfrac{1}{2} \times 269{,}4 \times 15 \times 2\ \mu\text{s} \times 60 = 0{,}24\ \text{W}$$

*Bloqueio.* Ocorre na passagem natural da corrente por zero, quando a corrente já é pequena. O
catálogo do TYN1225 não fornece $Q_{rr}$, o que é comum em SCR de rede, para os quais o parâmetro
relevante é $t_q$. Estimando por limite superior generoso, com $Q_{rr} = 100$ µC:

$$P_{bloq} = \tfrac{1}{2}\,Q_{rr}\,V_R\,f
= \tfrac{1}{2} \times 100\ \mu\text{C} \times 269{,}4 \times 60 = 0{,}81\ \text{W}$$

**Passo 7, total e leitura.**

$$P_T \approx 7{,}35 + 0{,}24 + 0{,}81 + 0{,}0006 = 8{,}40\ \text{W}$$

com a condução respondendo por **87,5 %** do total. Confirma-se a regra: em 60 Hz, dimensiona-se
tiristor pela condução.

Vale registrar o comportamento com o ângulo de disparo. Como a corrente do tiristor é retangular de
180° qualquer que seja $\alpha$, **a perda de condução não depende de $\alpha$**, mas a potência
entregue à carga depende:

| $\alpha$ | $V_o = \frac{2\sqrt2 V}{\pi}\cos\alpha$ | $P_o$ | Perda na ponte (4 × 7,35 W) |
|---|---|---|---|
| 0° | 198,07 V | 2971 W | 0,99 % |
| 15° | 191,32 V | 2870 W | 1,02 % |
| 30° | 171,53 V | 2573 W | 1,14 % |
| 45° | 140,06 V | 2101 W | 1,40 % |
| 60° | 99,03 V | 1486 W | 1,98 % |
| 75° | 51,26 V | 769 W | 3,82 % |

O rendimento do conversor **degrada-se conforme se afasta do disparo pleno**, ainda que a perda
absoluta seja constante. É a mesma razão pela qual o fator de potência cai com $\alpha$: o
conversor de fase controlada é eficiente apenas próximo do seu ponto de projeto.

**Circuito térmico.** Com $T_j = 110$ °C, $T_a = 40$ °C, $R_{th,jc} = 2{,}0$ °C/W e
$R_{th,ch} = 0{,}5$ °C/W (isolador), por tiristor:

$$R_{th,da} = \frac{110 - 40}{8{,}40} - 2{,}0 - 0{,}5 = 8{,}33 - 2{,}50 = 5{,}83\ ^\circ\text{C/W}$$

Se os quatro tiristores forem montados em um único dissipador, o critério dos slides manda calcular
$T_d$ para cada um, tomar o menor e dividir pela soma:

$$T_d = 110 - 8{,}40 \times (2{,}0 + 0{,}5) = 89{,}0\ ^\circ\text{C}
\;\Rightarrow\;
R_{th,da} = \frac{89{,}0 - 40}{4 \times 8{,}40} = 1{,}46\ ^\circ\text{C/W}$$

### 3.4 Exemplo 4. Controlador CA com TRIAC BTA41-600B

**Circuito.** Controlador de tensão alternada por controle de fase, 220 V / 60 Hz, carga resistiva
de 10 Ω, ângulo de disparo $\alpha = 90°$.

**Passo 1, formas de onda.** A corrente é senoidal truncada, nula de 0 a $\alpha$ e
$\frac{\sqrt2 V}{R}\sin\theta$ de $\alpha$ a $\pi$, repetindo-se com sinal invertido no semiciclo
negativo. A corrente de pico vale $\sqrt2 \times 220/10 = 31{,}11$ A.

**Passo 2, valores característicos.**

$$I_{T(rms)} = \frac{V}{R}\sqrt{\frac{1}{\pi}\left[(\pi - \alpha) + \frac{\sin 2\alpha}{2}\right]}
= 15{,}556\ \text{A}$$

$$I_{T(av)}\big|_{|i|} = \frac{\sqrt2\,V}{\pi R}\,(1 + \cos\alpha) = 9{,}904\ \text{A}$$

**Passos 3 e 4, perda de condução.**

$$P_{cond} = 1{,}063 \times 9{,}904 + 0{,}0074 \times 15{,}556^2 = 10{,}527 + 1{,}791 = 12{,}318\ \text{W}$$

A potência entregue à carga é $R\,I_{rms}^2 = 2420$ W, de modo que a perda no TRIAC representa
**0,51 %**, desempenho excelente e típico de controladores de fase com carga de alguns quilowatts.

**Varredura no ângulo de disparo.** Diferentemente do retificador controlado do exemplo anterior,
aqui a corrente eficaz *depende* de $\alpha$, e portanto a perda também:

| $\alpha$ | $I_{T(rms)}$ | $I_{T(av)}$ | $P_{cond}$ | $P_{carga}$ | Perda relativa |
|---|---|---|---|---|---|
| 0° | 22,00 A | 19,81 A | 24,64 W | 4840 W | 0,51 % |
| 30° | 21,68 A | 18,48 A | 23,12 W | 4700 W | 0,49 % |
| 60° | 19,73 A | 14,86 A | 18,67 W | 3894 W | 0,48 % |
| 90° | 15,56 A | 9,90 A | 12,32 W | 2420 W | 0,51 % |
| 120° | 9,73 A | 4,95 A | 5,96 W | 946 W | 0,63 % |
| 150° | 3,74 A | 1,33 A | 1,51 W | 140 W | 1,08 % |

O caso dimensionante do dissipador é $\alpha = 0°$, com 24,64 W. Com $T_j = 110$ °C, $T_a = 40$ °C,
$R_{th,j\text{-}mb} = 0{,}9$ °C/W e isolador de 0,5 °C/W:

$$R_{th,da} = \frac{110 - 40}{24{,}64} - 0{,}9 - 0{,}5 = 2{,}84 - 1{,}40 = 1{,}44\ ^\circ\text{C/W}$$

**Nota de projeto.** A tabela mostra que a perda relativa é praticamente constante e baixa em toda
a faixa útil, o que faz do controle de fase uma solução muito eficiente do ponto de vista térmico.
O seu problema não é rendimento, e sim **qualidade de energia**: a corrente truncada tem conteúdo
harmônico elevado e fator de potência de deslocamento degradado, exatamente como advertem os
slides. É por isso que o acionamento por cruzamento de zero, apesar do controle mais grosseiro, é
preferido sempre que a carga tolera (aquecimento resistivo, fornos).

## 4. Perdas de comutação

Consolidando o que os exemplos mostraram:

$$P_{ec} = \tfrac{1}{2}\,V_{AK}\,I_T\,t_{on}\,f_s
\qquad\text{(carga indutiva; use } \tfrac{1}{6} \text{ para carga resistiva)}$$

$$P_{bloq} = \tfrac{1}{2}\,Q_{rr}\,V_R\,f_s$$

Em 60 Hz, ambas são desprezíveis frente à condução, e no Exemplo 3 elas somaram 12,5 % do total, com
hipóteses conservadoras. **A comutação não é o que limita o tiristor: o que o limita é o $t_q$.**

Há, porém, duas restrições de comutação que não aparecem como perda média e que são igualmente
determinantes:

**Limite de $di/dt$.** No instante do disparo, a condução começa concentrada numa pequena área ao
redor da região de porta e leva alguns microssegundos para se espalhar por toda a pastilha. Se a
corrente cresce rápido demais, a densidade de corrente nessa área inicial produz aquecimento
localizado capaz de destruir o dispositivo. O TYN1225 admite 50 A/µs; o BTA41-600B, 150 A/µs com
$I_G = 150$ mA. Circuitos com barramento capacitivo de baixa impedância exigem **indutor de
$di/dt$** em série.

**Limite de $dv/dt$.** Já discutido na Seção 1.5. Exige *snubber* RC, sobretudo com carga indutiva.

## 5. Nota sobre o GTO

Vale registrar o dispositivo que resolve a limitação central do SCR. O **GTO** (*gate turn-off
thyristor*) é um tiristor de quatro camadas com geometria de porta e catodo interdigitada, que pode
ser bloqueado por um pulso **negativo** de corrente de porta. As diferenças de projeto, segundo o
livro-texto:

| Aspecto | SCR | GTO |
|---|---|---|
| Queda em condução | 1,5 a 2 V | 3 a 4 V |
| Correntes $I_L$ / $I_H$ | 150 / 300 mA (110 A) | 600 / 900 mA (18 A) |
| Bloqueio reverso | Pleno | Muito baixo (~20 V) |
| $dv/dt$ admissível | 200–500 V/µs | ~1000 V/µs |
| Frequência de operação | < 1 kHz | 1 a 4 kHz |
| Ganho de bloqueio | não se aplica | 1 a 5 |

O ganho de bloqueio entre 1 e 5 significa que desligar 100 A exige um pulso de porta de 20 a 100 A e
isso exige um circuito de comando pesado e caro. Somado à queda em condução quase duas vezes maior,
isso explica por que o GTO foi deslocado pelo IGBT em praticamente todas as faixas de potência
abaixo de alguns megawatts.

## 6. Síntese das expressões do tiristor e do TRIAC

$$\boxed{
\begin{aligned}
P_{cond} &= V_{TO}\,I_{T(av)} + r_T\,I_{T(rms)}^2
\qquad \big(I_{T(av)} = \text{média de } |i_T| \text{ no TRIAC}\big)\\[4pt]
P_{G} &= V_{GT}\,I_{GT}\,\delta_G \qquad (\text{desprezível em 60 Hz})\\[4pt]
P_{ec} &= \tfrac{1}{2}\,V_{AK}\,I_T\,t_{on}\,f_s \qquad (\text{desprezível em 60 Hz})\\[4pt]
P_{bloq} &= \tfrac{1}{2}\,Q_{rr}\,V_R\,f_s \qquad (\text{desprezível em 60 Hz})\\[4pt]
P_{T} &\approx P_{cond} \quad\text{para } f_s \le 1\ \text{kHz}
\end{aligned}}$$

**Parâmetros necessários da folha de dados:** $V_{TO}$ e $r_T$ a $T_j$ de operação; $I_{T(RMS)}$ e
$I_{T(AV)}$; $I_{TSM}$ e $I^2t$ para coordenação com fusível; $V_{DRM}/V_{RRM}$; $I_{GT}$, $V_{GT}$,
$I_H$, $I_L$; limites de $di/dt$ e $dv/dt$; $t_q$; $R_{th,jc}$.

**Restrições que não são perdas mas dimensionam o projeto:** $di/dt$ (indutor série), $dv/dt$
(*snubber* RC), $t_q$ (frequência máxima), $I_L$ (duração do pulso de porta com carga indutiva).

---

**Documento anterior:** [02. Diodo de potência](02-diodo-de-potencia.md)
**Próximo documento:** [04. MOSFET de potência](04-mosfet-de-potencia.md)
