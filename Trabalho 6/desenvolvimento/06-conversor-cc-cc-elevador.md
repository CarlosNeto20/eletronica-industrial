# 06. Conversor CC-CC elevador de alto ganho

O conversor CC-CC eleva os 42 a 56 V do banco de baterias para os 210 V do barramento do inversor quando a rede falta. Este arquivo identifica a topologia a partir do texto e do Anexo 01, deduz o ganho e os esforços e discute a coerência com o retificador. Os valores estão em `calculos/parametros.json`, chave `cc_cc`.

## 1. Topologia adotada

A seção 5 da planilha fala em um capacitor inferior "que fica entre os dois enrolamentos primários", em uma tensão sobre cada enrolamento igual à metade da tensão desse capacitor e em um retificador em ponte no secundário com relação a = 1. O circuito do Anexo 01 confirma a leitura. O indutor L1 de 39,2 µH sai do positivo da bateria e entra na derivação central de um autotransformador de dois enrolamentos iguais. As extremidades desses enrolamentos vão aos drenos das chaves S1 e S2, cujas fontes estão no negativo comum, e também, pelos diodos D17 e D18, ao capacitor inferior C8. Um terceiro enrolamento, acoplado ao mesmo núcleo, alimenta a ponte D13 a D16, que carrega o capacitor superior C7. C7 fica ligado entre o barramento positivo e o ponto comum com C8, de modo que o barramento é a soma VC8 + VC7, e esse conjunto fica em paralelo com o capacitor C4 do retificador.

Trata-se do elevador baseado na célula de comutação de três estados com um enrolamento adicional no autotransformador, proposto por Araújo, Torrico-Bascopé e Torrico-Bascopé para fontes de baixa tensão e alto ganho. A célula divide a corrente de entrada entre as duas chaves, faz o indutor operar no dobro da frequência de comutação e, com o enrolamento adicional, eleva o ganho sem aumentar a tensão nas chaves. Esta é a hipótese adotada e implementada no PLECS.

## 2. Etapas de operação com D > 0,5

As chaves recebem o mesmo comando, com razão cíclica D e defasagem de 180°. Com D > 0,5 há sobreposição, e cada meio período de comutação Te = 1/(2fsb) tem duas etapas.

Na primeira etapa as duas chaves conduzem, durante (2D − 1)Te. As duas extremidades do autotransformador estão no negativo; como os enrolamentos têm o mesmo número de espiras e estão em série aditiva, a única solução compatível com o acoplamento ideal é a derivação central também em zero. O indutor recebe a tensão da bateria, os enrolamentos não têm tensão, o secundário não conduz, e C7 e C8 alimentam a carga.

Na segunda etapa apenas uma chave conduz, durante 2(1 − D)Te. A extremidade da chave aberta sobe até VC8 pelo diodo correspondente, os dois enrolamentos em série ficam submetidos a VC8 e cada um a VC8/2. A derivação central fica em VC8/2, e o indutor recebe Vib − VC8/2. O secundário, com a mesma tensão por espira, carrega C7 através da ponte.

## 3. Ganho estático

O balanço de volt-segundo no indutor ao longo de Te dá

$$V_{ib}\,(2D-1) + \left(V_{ib} - \frac{V_{C8}}{2}\right) 2(1-D) = 0 \quad\Rightarrow\quad V_{C8} = \frac{V_{ib}}{1-D}$$

Com 42 V e D = 0,7,

$$V_{C8} = \frac{42}{1-0{,}7} = 140\ \text{V} \qquad V_{N_p} = \frac{V_{C8}}{2} = 70\ \text{V}$$

O secundário, com relação a = Ns/Np, carrega C7 com a tensão de um enrolamento primário refletida.

$$V_{C7} = a\,\frac{V_{C8}}{2} = 1\cdot 70 = 70\ \text{V}$$

e o barramento é

$$V_{ob} = V_{C8} + V_{C7} = \frac{V_{ib}}{1-D}\left(1 + \frac{a}{2}\right) = \frac{42}{0{,}3}\cdot 1{,}5 = 210\ \text{V}$$

A soma 140 V + 70 V reproduz os 210 V da planilha, o que confirma o empilhamento de C7 sobre C8. O ganho é 1,5/(1 − D), isto é, 1,5 vez o ganho 1/(1 − D) da célula de três estados sem o enrolamento adicional, obtido sem aumentar a tensão nas chaves.

A razão cíclica necessária para 210 V em cada extremo da bateria é

$$D = 1 - \frac{(1 + a/2)\,V_{ib}}{V_{ob}} \quad\Rightarrow\quad D_{42} = 0{,}70 \qquad D_{56} = 1 - \frac{1{,}5\cdot 56}{210} = 0{,}60$$

Os dois valores ficam acima de 0,5, então o conversor opera sempre na região de sobreposição, como pressupõe a dedução. A planilha não calcula o caso de 56 V. A Figura `calculos/figuras/ganho_cc.png` mostra Vob em função de D para as duas tensões de bateria.

## 4. Indutor

O indutor vê ondulação em 2fsb. A variação de corrente ocorre na etapa de sobreposição, com Vib aplicada durante (2D − 1)/(2fsb).

$$\Delta I_{Lb} = \frac{V_{ib}\,(2D-1)}{2 f_{sb} L_b}$$

A planilha fixa ΔI = 0,2·Iibmax, com Iibmax = Pob/Vibmin.

$$I_{ibmax} = \frac{2250}{42} = 53{,}57\ \text{A} \qquad \Delta I_{ibmax} = 10{,}71\ \text{A}$$

$$L_b = \frac{42\cdot(2\cdot 0{,}7 - 1)}{2\cdot 20\,000\cdot 10{,}71} = 39{,}2\ \mu\text{H}$$

A 56 V, com D = 0,6, a ondulação cai para 7,14 A e a corrente média para 40,18 A.

A potência de 2250 W é a de saída do CC-CC e Iibmax não inclui as perdas do próprio conversor. Com rendimento de 0,95 (hipótese H, para um conversor com MOSFETs de baixa tensão e diodos rápidos) a bateria fornece 56,4 A a 42 V, e o pico no indutor chega a cerca de 61,7 A. Esse acréscimo de 5% interessa ao dimensionamento do indutor, das chaves e dos cabos da bateria.

## 5. Esforços nos semicondutores e capacitores

| Grandeza | 42 V, D = 0,70 | 56 V, D = 0,60 |
|---|---|---|
| VC8 e tensão reversa de D17 e D18 (V) | 140 | 140 |
| VC7 e tensão reversa dos diodos D13 a D16 (V) | 70 | 70 |
| Tensão de bloqueio de S1 e S2, VC8/2 (V) | 70 | 70 |
| Corrente média na bateria, sem η (A) | 53,57 | 40,18 |
| Corrente média com η = 0,95 (A) | 56,39 | 42,29 |
| Ondulação ΔILb (A) | 10,71 | 7,14 |
| Pico em Lb, sem η (A) | 58,93 | 43,75 |
| Corrente média por chave, sem η (A) | 26,79 | 20,09 |

A tensão nas chaves é só um terço do barramento, o que permite MOSFETs de 100 V a 150 V com baixa resistência de condução. As correntes eficazes nas chaves e nos diodos dependem da distribuição entre primários e secundário durante cada etapa e da dispersão do transformador; elas são medidas no PLECS em vez de estimadas por fórmulas simplificadas.

## 6. Barramento em modo bateria

O inversor monofásico drena potência pulsante em 120 Hz. Se toda a componente alternada fosse absorvida pelo capacitor C4 de 1880 µF, a ondulação seria

$$\Delta V_{bus} \approx \frac{P}{2\pi f_o C_4 V_{bus}} = \frac{2250}{2\pi\cdot 60\cdot 1880\cdot10^{-6}\cdot 210} = 15{,}1\ \text{V pico a pico}$$

Em malha aberta o CC-CC se comporta como uma fonte com impedância de saída finita e absorve parte dessa ondulação, que então aparece como componente de 120 Hz na corrente da bateria. Nenhum dos dois efeitos é tratado pela planilha; ambos são medidos no PLECS.

## 7. Coerência com o retificador e lógica de transferência

O retificador entrega um barramento com vale de 211,57 V na rede mínima (213,2 V com 1880 µF), e o CC-CC entrega 210 V. A ideia é que, com a rede presente, o barramento fique sempre acima da saída natural do elevador, e que a bateria assuma quando a rede falta. A margem, porém, é de só 1,6 V a 3,2 V e desaparece com a tolerância do banco eletrolítico ou com a queda de tensão da rede abaixo de 176 V.

Há também uma questão de controle. No circuito PSIM do Anexo 01 as chaves do CC-CC ficam comandadas o tempo todo com D = 0,7. Um elevador em malha aberta não "espera" com o barramento acima da sua tensão natural: durante a sobreposição o indutor sempre armazena energia da bateria e a entrega na etapa seguinte. Com o barramento acima de 210 V o conversor passa a operar em condução descontínua e continua drenando uma parcela de potência da bateria enquanto a rede está presente. Um no-break de dupla conversão mantém a bateria em repouso nesse modo, seja desabilitando o elevador, seja regulando-o em malha fechada para uma referência abaixo do vale do retificador, caso em que ele permaneceria praticamente parado.

Na simulação deste trabalho a lógica de transferência foi representada da forma mais simples que preserva esse comportamento (hipótese H). As chaves do CC-CC ficam bloqueadas enquanto a rede está presente e são habilitadas, com D fixo, no mesmo instante em que a chave SS2 abre (detecção ideal, sem atraso). Os ensaios da seção 6 usam essa lógica. O ensaio `nb_176_nl_anexo` repete o caso de 176 V com o comando permanente do PSIM, para medir a corrente de bateria com a rede presente e comparar as duas interpretações.

## 8. Elementos de simulação

O transformador do Anexo 01 (T_32) tem três enrolamentos de 100 espiras, 1 mΩ e 1 µH de dispersão em cada um e 10 mH de magnetização. No PLECS ele é um Transformer com enrolamentos [2 1], relação [1 1 1] e magnetização de 10 mH referida ao primeiro enrolamento, com indutores de 1 µH e resistores de 1 mΩ em série com cada enrolamento. Os pontos dos enrolamentos primários foram ligados em série aditiva (ponto do primeiro do lado de S1 e ponto do segundo na derivação central). As correntes iniciais dos indutores de dispersão são metade da corrente inicial de Lb em cada primário, para que o corte indutivo formado por Lb e pelas duas dispersões comece coerente.

Os ensaios `elev_42` e `elev_56` do modelo `elevador_bateria` alimentam uma carga resistiva de 19,6 Ω (2250 W em 210 V) a partir do barramento com C4, C7 e C8, e medem a tensão do barramento, as tensões de C7 e C8, a corrente e a ondulação em Lb, as correntes nas chaves, no diodo D17 e no secundário e a tensão de bloqueio de S1. Os resultados estão em [08](08-resultados.md).

Próximo arquivo: [07. Guia de simulação no PLECS](07-guia-plecs.md).
