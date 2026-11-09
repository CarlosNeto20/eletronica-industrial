# 03. Retificador com filtro capacitivo e barramento CC

O retificador em ponte com filtro capacitivo alimenta o barramento do inversor enquanto a rede está presente. Este arquivo refaz a seção 3 da planilha passo a passo, acrescenta a sensibilidade ao banco realmente adotado e define os valores de barramento usados no inversor. Os números vêm de `calculos.py` (classe A) e estão em `calculos/parametros.json`, chave `retificador`.

## 1. Hipóteses

A planilha trata o inversor como uma carga de potência constante Prec ligada ao barramento. Essa potência é obtida do rendimento do inversor, usado aqui apenas como orçamento.

$$P_{rec} = \frac{P_o}{\eta_{inv}} = \frac{2100}{0{,}933} = 2250{,}8\ \text{W} \approx 2250\ \text{W}$$

O valor de 0,933 não é uma eficiência medida nem calculada; serve para dimensionar o retificador com alguma folga sobre os 2100 W de saída. Os diodos são ideais, a rede não tem impedância e o projeto é feito na tensão mínima de entrada (176 V), que é o pior caso para o vale do barramento. A ondulação total é ΔVC = 37,33 V, isto é, 15% do pico, conforme a auditoria em [02](02-auditoria-do-documento.md).

## 2. Tensões no capacitor

O pico do barramento é o pico da rede mínima.

$$V_{C1max} = \sqrt{2}\cdot V_{imin} = \sqrt{2}\cdot 176 = 248{,}90\ \text{V}$$

O vale é o pico menos a ondulação.

$$V_{C1min} = V_{C1max} - \Delta V_C = 248{,}90 - 37{,}33 = 211{,}57\ \text{V}$$

O valor médio, usado para definir a corrente equivalente, é a média aritmética entre pico e vale.

$$V_{C1med} = \frac{248{,}90 + 211{,}57}{2} = 230{,}24\ \text{V}$$

## 3. Ângulo de condução

A ponte conduz do instante em que a tensão retificada alcança o vale até o pico. Medido a partir do pico para trás, o ângulo é

$$\theta_{C1} = \frac{\pi}{2} - \arcsin\!\left(\frac{V_{C1min}}{V_{C1max}}\right) = \frac{\pi}{2} - \arcsin(0{,}85) = 0{,}5548\ \text{rad}$$

o que equivale a 31,8° e a um tempo de condução de

$$t_{C1} = \frac{\theta_{C1}}{2\pi f_r} = \frac{0{,}5548}{2\pi\cdot 60} = 1{,}472\ \text{ms}$$

em cada semiciclo de 8,33 ms.

## 4. Capacitância

Durante a descarga, que dura (π − θC1)/(2πfr), o capacitor fornece sozinho a energia da carga. Igualando essa energia à variação da energia armazenada,

$$P_{rec}\,\frac{\pi-\theta_{C1}}{2\pi f_r} = \frac{1}{2}\,C_1\,(V_{C1max}^2 - V_{C1min}^2)$$

e isolando C1,

$$C_1 = \frac{P_{rec}\,(\pi-\theta_{C1})}{\pi f_r\,(V_{C1max}^2 - V_{C1min}^2)} = \frac{2250\cdot(3{,}1416-0{,}5548)}{\pi\cdot 60\cdot(248{,}90^2-211{,}57^2)} = 1{,}796\ \text{mF}$$

As unidades fecham em W·s/V², que é farad. A planilha adota quatro eletrolíticos de 470 µF/450 V em paralelo, 1880 µF, com resistência série equivalente de 0,05 Ω para o banco. O banco supera o mínimo calculado em 4,7%.

Essa folga é pequena diante da tolerância usual de eletrolíticos. Resolvendo a mesma equação para o vale, com C1 conhecido, obtêm-se os valores abaixo para 2250 W.

| Rede (V) | Pico (V) | Vale com 1880 µF (V) | Ondulação (%) |
|---|---|---|---|
| 176 | 248,90 | 213,19 | 14,3 |
| 220 | 311,13 | 282,16 | 9,3 |
| 264 | 373,35 | 348,93 | 6,5 |

Com C = 1504 µF (−20%), o vale a 176 V cai para 204,5 V. Esse número fica abaixo dos 210 V do CC-CC e mostra que a coerência entre retificador e elevador não é robusta à tolerância do banco, ponto retomado em [06](06-conversor-cc-cc-elevador.md).

## 5. Correntes

A corrente média drenada pela carga equivalente é

$$I_{oeq} = \frac{P_{rec}}{V_{C1med}} = \frac{2250}{230{,}24} = 9{,}773\ \text{A}$$

e a resistência equivalente que dissipa Prec na tensão média é

$$R_{oeq} = \frac{V_{C1med}^2}{P_{rec}} = \frac{230{,}24^2}{2250} = 23{,}56\ \Omega$$

Na aproximação de pulso retangular da Figura 3 da planilha, a carga reposta em cada semiciclo durante θC1 é igual à carga retirada pela carga em π. O balanço dá a corrente de pico do pulso,

$$I_{chg}\,\theta_{C1} = I_{oeq}\,\pi \quad\Rightarrow\quad I_{chg} = \frac{9{,}773\cdot\pi}{0{,}5548} = 55{,}34\ \text{A}$$

No capacitor circula Ichg − Ioeq durante a condução e −Ioeq no restante do semiciclo, o que leva ao valor eficaz

$$I_{C1ef} = \sqrt{\frac{1}{\pi}\left[(I_{chg}-I_{oeq})^2\,\theta_{C1} + I_{oeq}^2\,(\pi-\theta_{C1})\right]} = \sqrt{\frac{45{,}57^2\cdot 0{,}5548 + 9{,}773^2\cdot 2{,}587}{\pi}} = 21{,}10\ \text{A}$$

Cada diodo conduz um pulso por período da rede. Seus valores médio e eficaz são

$$I_{D1med} = \frac{I_{chg}\,\theta_{C1}}{2\pi} = 4{,}886\ \text{A} \qquad I_{D1ef} = I_{chg}\sqrt{\frac{\theta_{C1}}{2\pi}} = 16{,}44\ \text{A}$$

O pico real do pulso é maior que Ichg, porque a corrente acompanha a derivada da senoide e não é plana. A planilha adota a regra prática ID1pk = 2·Ichg = 110,7 A. Esse número é uma estimativa conservadora; o pico efetivo depende da impedância entre a rede e o capacitor e é medido no PLECS.

## 6. Tensão reversa

Na ponte cada diodo bloqueia, no semiciclo em que não conduz, a tensão do capacitor carregado no pico da rede máxima.

$$V_{Drrevpk} = \sqrt{2}\cdot 264 = 373{,}35\ \text{V}$$

A planilha indica uma ponte de diodos lentos da Vishay. A escolha preliminar, com folga para surtos, está em [09](09-componentes-e-melhorias.md).

## 7. Barramento visto pelo inversor

O inversor recebe do retificador uma tensão entre o vale na rede mínima e o pico na rede máxima.

$$V_{imin\_cc} = 211{,}57\ \text{V} \qquad V_{imax\_cc} = 373{,}35\ \text{V}$$

Em modo bateria o barramento é imposto pelo CC-CC, com 210 V nominais. O valor de 223 V usado na seção 4.1 da planilha não é deduzido; a análise do inversor usa 211,57 V em rede e 210 V em bateria, como discutido na auditoria.

## 8. Elementos do Anexo 01 e o que eles mudam

O circuito PSIM acrescenta dois elementos que a seção 3 não considera.

O resistor de 0,1 Ω entre a ponte e o barramento representa, de forma concentrada, a impedância da rede e da fiação. Ele limita a derivada da corrente de carga e achata o pulso, de modo que o pico real tende a ser menor que 2·Ichg e o tempo de condução maior que tC1. Também reduz levemente a tensão média do barramento.

O transformador T1 de relação 1:1 tem a função de isolar a fonte da rede, aterrada no PSIM, do lado CC, que é referido à saída do inversor. Com dispersões de 1 µH e magnetização de 1 H, ele praticamente não altera a tensão. No PLECS o mesmo papel é cumprido por um transformador ideal 1:1 (sem dispersão e sem magnetização) com 2 mΩ de resistência série, o que permite abrir a chave SS2 em qualquer instante sem interromper corrente em indutância. A reatância de 2 µH a 60 Hz (0,75 mΩ) e a corrente magnetizante de 1 H (0,66 A de pico a 176 V) são desprezíveis diante dos 0,1 Ω e das correntes de carga.

## 9. Verificação no PLECS

Os ensaios `ret_176_planilha`, `ret_176_anexo` e `ret_264_anexo` do modelo `retificador_barramento` comparam estes valores com o solver. O primeiro reproduz as condições da seção 3 (C1 = 1,796 mF, diodos ideais, sem resistência série), o segundo usa o banco de 1880 µF com 0,05 Ω, 0,1 Ω no barramento e diodos com queda de 0,8 V, e o terceiro repete o segundo na rede máxima para verificar a tensão reversa. A carga é a resistência equivalente que dissipa 2250 W na tensão média de cada caso. As grandezas comparadas são a ondulação do barramento, o pulso de corrente (pico, duração, médio e eficaz por diodo) e a corrente eficaz no capacitor. Os resultados estão em [08](08-resultados.md).

Próximo arquivo: [04. Inversor e filtro](04-inversor-e-filtro.md).
