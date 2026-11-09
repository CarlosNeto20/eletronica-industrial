# 05. Malha de tensão do inversor

Este arquivo refaz os passos 1 a 10 da seção 4.5 da planilha, verifica o laço em vários pontos de operação e descreve como o compensador foi implementado no PLECS. Os números estão em `calculos/parametros.json`, chave `malha`, e os Bodes em `calculos/figuras` e `calculos/bode_laco_pontos.csv`.

## 1. Elementos do laço

O sensor reduz o pico de 162,63 V da saída ao pico de 4 V da referência.

$$H_v = \frac{V_{ref}}{\sqrt{2}\,V_{oef}} = \frac{4}{\sqrt{2}\cdot 115} = 0{,}024595$$

O divisor do Anexo 01 (25,22 kΩ sobre 1025,22 kΩ) dá 0,024600, diferença de 0,02%.

A planta relaciona a razão cíclica média com a tensão de saída. Para o filtro LC carregado por Ro,

$$G_v(s) = \frac{v_o(s)}{d(s)} = V_{cc}\,\frac{1}{L_oC_o s^2 + \dfrac{L_o}{R_o}s + 1}$$

em que o termo de amortecimento é Lo/Ro (a forma em s da planilha traz L1/Ro por erro de digitação). O ganho estático é Vcc, por isso a planta muda com o barramento. A ESR de 5 mΩ de Co acrescenta um zero em 530 kHz e foi incluída na verificação dos pontos de operação, mas não no projeto, para reproduzir a planilha.

O modulador tem ganho Fm = 1/Vd = 1/5, já que a portadora vai de −5 V a +5 V. O laço sem compensador é FTLAscv = Gv·Fm·Hv, com ganho estático 373·0,2·0,024595 = 1,835 (5,27 dB) em 373 V.

## 2. Passos 1 a 4: frequência de cruzamento e ganho necessário

A planilha escolhe a frequência de cruzamento abaixo de 2fs/4.

$$f_{cv} = \frac{2 f_s}{6} = \frac{40\,000}{6} = 6{,}667\ \text{kHz}$$

Nessa frequência, com 373 V e 6,298 Ω, ω²LoCo = 38,49 e ωLo/Ro = 2,432, de modo que

$$|FTLA_{scv}(j\omega_{cv})| = \frac{1{,}835}{\sqrt{(1-38{,}49)^2 + 2{,}432^2}} = 0{,}0488 \;\Rightarrow\; A_v = -26{,}22\ \text{dB}$$

$$P = -180^\circ + \arctan\frac{2{,}432}{37{,}49} = -176{,}29^\circ$$

O texto do passo 4 fala em 33,23 dB, mas o cálculo da própria planilha dá −26,22 dB, valor usado em seguida. O compensador precisa fornecer

$$G_v = 10^{|A_v|/20} = 10^{26{,}22/20} = 20{,}47$$

na frequência de cruzamento. A expressão com módulo vale porque Av < 0.

## 3. Passos 5 a 8: avanço de fase e fator K

Com margem de fase desejada de 60°, o avanço exigido é

$$\alpha = MF - P - 90^\circ = 60 + 176{,}29 - 90 = 146{,}29^\circ$$

Como α > 90°, é preciso um Tipo 3, com dois zeros e dois polos além do integrador. Pelo método do fator K, os zeros ficam em fcv/√K e os polos em fcv·√K, e o avanço no cruzamento é

$$\alpha(K) = 4\arctan\sqrt{K} - 180^\circ$$

O K exato para 146,29° é 45,55. A planilha adota K = 47, que fornece α = 146,80° e margem de fase de 60,52°. A curva está em `avanco_fase_K.png`.

## 4. Passo 9: componentes do Tipo 3

Com R1 = 10 kΩ,

$$F_{z1} = F_{z2} = \frac{f_{cv}}{\sqrt{K}} = 972{,}4\ \text{Hz} \qquad F_{p2} = F_{p3} = f_{cv}\sqrt{K} = 45{,}70\ \text{kHz}$$

$$R_2 = \frac{\sqrt{K}}{K-1}\,G_v R_1 = 30{,}52\ \text{k}\Omega \qquad R_3 = \frac{R_1}{K-1} = 217{,}4\ \Omega$$

$$C_1 = \frac{K-1}{2\pi f_{cv} G_v R_1} = 5{,}363\ \text{nF} \qquad C_2 = \frac{1}{2\pi f_{cv} G_v R_1} = 116{,}6\ \text{pF} \qquad C_3 = \frac{K-1}{\sqrt{K}}\,\frac{1}{2\pi f_{cv} R_1} = 16{,}02\ \text{nF}$$

e a função de transferência do circuito da Figura 7 da planilha é

$$C_v(s) = \frac{(R_1+R_3)\left(s+\frac{1}{R_2C_1}\right)\left(s+\frac{1}{(R_1+R_3)C_3}\right)}{R_1R_3C_2\,s\left(s+\frac{1}{R_3C_3}\right)\left(s+\frac{C_1+C_2}{R_2C_1C_2}\right)} = K_c\,\frac{(s+\omega_{z1})(s+\omega_{z2})}{s\,(s+\omega_{p1})(s+\omega_{p2})}$$

com Kc = 4,031·10⁷ s⁻¹, ωz1 = ωz2 = 6110 rad/s e ωp1 = ωp2 = 2,872·10⁵ rad/s. Os zeros reais caem exatamente em 972,4 Hz e os polos em 45,70 kHz. No cruzamento o compensador fornece ganho de 20,47 e fase de +56,8°, o que leva a fase do laço a −119,5° e a margem a 60,52°, como na planilha.

## 5. Passo 10 e verificação em vários pontos de operação

O laço compensado foi avaliado de 1 Hz a 1 MHz em nove pontos, combinando barramentos de 210 V a 373 V e cargas de vazio a 4,41 Ω (3 kVA resistivos). Para cada ponto foram procurados todos os cruzamentos por 0 dB e todas as passagens da fase por −180°, e a estabilidade em malha fechada foi conferida pelas raízes do polinômio característico.

| Ponto | Cruzamentos por 0 dB | MF no cruzamento | Fase −180° em | MG | Estável |
|---|---|---|---|---|---|
| 373 V, 2100 W | 6,66 kHz | 61,3° | 48,5 kHz | 24,0 dB | sim |
| 373 V, vazio | 6,68 kHz | 57,5° | 48,0 kHz | 23,8 dB | sim |
| 248,9 V, 2100 W | 4,70 kHz | 60,8° | 48,5 kHz | 27,5 dB | sim |
| 211,57 V, 2100 W | 4,12 kHz | 59,9° | 48,5 kHz | 28,9 dB | sim |
| 211,57 V, vazio | 4,14 kHz | 53,7° | 48,0 kHz | 28,7 dB | sim |
| 210 V, 2100 W | 4,09 kHz | 59,8° | 48,5 kHz | 29,0 dB | sim |
| 210 V, vazio | 4,12 kHz | 53,6° | 48,0 kHz | 28,8 dB | sim |
| 373 V, 4,41 Ω | 6,65 kHz | 62,9° | 48,7 kHz | 24,1 dB | sim |
| 210 V, 4,41 Ω | 4,07 kHz | 62,4° | 48,7 kHz | 29,0 dB | sim |

Valores com a ESR de Co; sem ela, o ponto de projeto reproduz exatamente os 60,52° da planilha e a fase cruza −180° em 44 kHz com MG de 22,3 dB.

Os resultados confirmam que há um único cruzamento por 0 dB em todos os pontos e que o laço é estável em todos eles. Três observações completam a leitura do Bode da planilha.

- O cruzamento real só fica em 6,67 kHz no barramento máximo. Como o ganho da planta é proporcional a Vcc, em 211,57 V o laço perde 4,9 dB e cruza em 4,1 kHz. A margem de fase muda pouco, porque a fase do compensador é larga entre os zeros e os polos.
- Em vazio a ressonância do filtro em 1,07 kHz fica praticamente sem amortecimento (Q ≈ 494). O pico de ressonância aparece no Bode do laço logo acima dos zeros duplos de 972 Hz, mas o ganho ali é muito maior que 1 e a fase do laço, embora se aproxime de −180° logo acima de f0 (a fase do compensador é só de +3,0° em 1,07 kHz), não cruza esse valor. Não há cruzamento adicional por 0 dB e a malha fechada é estável. A margem nessa região é pequena em termos de fase, o que torna a resposta em vazio sensível a atrasos não modelados.
- A margem de ganho não é infinita. Os polos duplos em 45,7 kHz levam a fase a −180° perto de 48 kHz. Essa frequência está acima de 2fs = 40 kHz, onde o modelo médio da modulação já não descreve o conversor, de modo que a margem de ganho calculada tem valor apenas indicativo.

A Figura `bode_laco.png` mostra o laço em quatro desses pontos, com os cruzamentos marcados, e `bode_planta.png` mostra a planta em 373 V (plena e vazio) e em 211,6 V.

## 6. Interação com a modulação

Os polos do compensador ficam acima de fs e muito perto da frequência de ondulação unipolar (40 kHz). Nessa frequência o ganho do compensador é 69,6 (36,9 dB). A ondulação de 0,33 V pico a pico na saída, vista pelo sensor, vira cerca de 0,56 V pico a pico em vc. A inclinação dessa ondulação é cerca de 18% da inclinação da portadora (10 V em 25 µs), o que mantém um único cruzamento por meio período, mas não deixa folga ampla. Uma alternativa seria colocar um dos polos abaixo de fs, ao custo de alguns graus de margem.

O modelo médio também ignora o atraso efetivo do modulador. Como sensibilidade (hipótese H), um atraso puro de 1/(4fs) = 12,5 µs reduziria a margem de fase em 373 V para 31,3° e moveria o cruzamento da fase por −180° para 12,1 kHz, com margem de ganho de 5,9 dB. Na modulação analógica com amostragem natural esse atraso é menor, mas o número mostra que a escolha de fcv = fs/3 é agressiva e que a simulação chaveada é o teste decisivo.

## 7. Erro em regime a 60 Hz

O compensador não tem ressonância em 60 Hz; o seguimento da referência senoidal depende do ganho elevado do integrador. A 60 Hz o laço tem módulo de 89,4 em 373 V e de 50,3 em 210 V, com fase próxima de −84°. A relação entre a saída e a referência escalonada é L/(1 + L), o que prevê

| Barramento | |L(j2π60)| | Vo previsto (V) | Defasagem |
|---|---|---|---|
| 373 V, 2100 W | 89,4 | 114,87 | −0,64° |
| 248,9 V, 2100 W | 59,7 | 114,80 | −0,95° |
| 211,57 V, 2100 W | 50,7 | 114,76 | −1,12° |
| 210 V, vazio | 50,3 | 114,70 | −1,13° |

O erro estático previsto pelo modelo linear é de 0,1% a 0,3%, abaixo de qualquer critério usual de regulação. O resultado chaveado, que inclui quedas nos MOSFETs, a não linearidade da carga e eventuais saturações do modulador, é comparado com esses valores nas curvas de regulação.

## 8. Compensador com os componentes do PSIM

O Anexo 01 usa valores comerciais. Com RF = 33 kΩ, CFV2 = 5,6 nF, C9 = 120 pF, RIZ = 10 kΩ, RIP = 220 Ω e CI = 18 nF, os zeros vão para 861 Hz e 865 Hz e os polos para 40,2 kHz e 41,1 kHz. A 373 V e plena carga o cruzamento sobe para 7,85 kHz com margem de 59,6° e margem de ganho de 21,1 dB; a 211,57 V cruza em 4,79 kHz com 62,0°. A resposta é parecida, mas não igual, e por isso a simulação do professor não valida a função publicada. A Figura `bode_compensador.png` compara as duas versões.

## 9. Implementação no PLECS

O compensador foi escrito em um bloco C-Script com três estados contínuos, em uma realização em série de integrador e dois avanços.

$$x_0' = K_c\,e \qquad x_1' = \omega_{p1}(x_0 - x_1) \qquad x_2' = \omega_{p2}(y_2 - x_2)$$

$$y_2 = x_0 + \left(\frac{\omega_{z1}}{\omega_{p1}} - 1\right)x_1 \qquad v_c = y_2 + \left(\frac{\omega_{z2}}{\omega_{p2}} - 1\right)x_2$$

com e = vref − Hv·vo e vref = 4 sen(2π60t). Cada estado fica em volts, o que mantém as tolerâncias absolutas do solver significativas. A resposta em frequência dessa realização foi conferida contra Cv(s) da planilha pelo script `conferir_modelos.py`, com erro relativo máximo de 8·10⁻¹³. A saída é limitada a ±5 V, como o amplificador operacional do Anexo 01, e o integrador para de integrar quando a saída está saturada e o erro tende a aumentá-la (anti-windup por integração condicional). O C-Script também gera os comandos da chave SS2, a habilitação do CC-CC e a ligação das cargas, todos por tempo e com sinais de cruzamento por zero para que o solver localize os eventos.

O laço segue o diagrama de blocos da Figura 4 da planilha (vc = Cv·e). No circuito PSIM a referência entra na porta não inversora do amplificador, e a saída vale vc = Vref + Cv·e. O termo adicional age como alimentação direta da referência; ele não altera o laço, mas altera a resposta à referência. Essa diferença fica registrada para a comparação qualitativa com a simulação do professor.

Próximo arquivo: [06. Conversor CC-CC elevador](06-conversor-cc-cc-elevador.md).
