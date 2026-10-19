# Auditoria e decisões justificadas

| Local | Original (F) | Verificação (A) e decisão |
|---|---|---|
| p. 2 | FP menor que 0,5 | Não é consequência universal da ponte capacitiva. Medir P/(Vrms Irms) com impedância de rede explicitada. |
| p. 4 | η=0,9 chamado rendimento do retificador | 405/0,9=450 W é orçamento conservador de entrada. Não atribuir 45 W de perda somente à ponte; não confundir com rendimento simulado. |
| p. 5 | C1=940 em µF | Nos arquivos usar 940e-6 F, preservando a unidade. A corrente de 4,648 A foi calculada para 545,7 µF e pulsos ideais, não automaticamente para 940 µF. |
| p. 6 | Vmín=225 V, Dmáx=0,4, n=0,3 | Relação ideal coerente. Não há margem para diodos, cobre ou shunt a 225 V. Limite implementado 0,45, mantendo reset abaixo de 0,5. |
| p. 7 | C mínimo=27,78 µF; texto menciona 47 µF | 47 µF é arredondamento comercial implícito, não novo resultado da equação. |
| p. 7 | ESRmáx=0,09 Ω, selecionada 0,11 Ω | A própria escolha excede o limite. Ondulação conservadora ≈0,3334 Vpp. Banco revisado: dois 2200 µF em paralelo, C=4400 µF e ESR nominal equivalente=0,055 Ω; ≈0,1667 Vpp. |
| p. 9/15 | fo=290,358 Hz | É frequência ideal sem o fator (1+r/R); frequência natural do denominador é menor. Na malha de corrente o zero é 1/[2πC(R+r)], não o zero ESR da tensão. |
| p. 11 | Gv=10^(abs(Av_dB)/20) | A imagem confirma as barras de módulo. Correto para atenuação; usar genericamente G=1/abs(planta no cruzamento), evitando inversão de ganho quando a planta amplifica. |
| p. 14/21 | MF escrita como módulo de −180−fase; MG infinita | MF deve ser avaliada no cruzamento real de 0 dB e fase contínua. O módulo pode esconder margem negativa. O laço de tensão original cruza −180° em baixa frequência; listar todos os cruzamentos e confirmar polos fechados. |
| p. 16–18 | fci=12,5 kHz; ganho compensador=2,076 | A expressão da p. 17 usa fcv=5 kHz, onde o ganho da planta é +6,341 dB. Em 12,5 kHz é −1,638 dB, requerendo ganho 1,2075, e não 2,076. Os RC listados resultam em fc≈19,995 kHz a 373 V. |
| p. 16 | fase −89,2° e avanço 59,446° | Cálculo da planta dá −89,446° em 12,5 kHz; texto arredondado inconsistente. |
| p. 21, fig. 14 | Barramento C1=470 µF; texto 940 µF | Adotar 940 µF no modelo final e registrar a diferença. Fonte marcada 248 V deve ser entendida como pico para 176 Vrms, não 248 Vrms. |
| p. 21 | Tensão RC: 82 kΩ, 1,5 nF, 100 pF; corrente: 18 kΩ, 2,7 nF, 220 pF | Não são os RC calculados. Não declarar que essas simulações validam exatamente as funções publicadas. |
| p. 21 | Divisor 100 kΩ/10,20 kΩ | Hv=0,09256: referência 2,5 V leva a 27,0098 V. Modelo usa 2,5/27 exato. |
| p. 21 | Shunt 10 mΩ, ganho 16,7 | Hi=0,167 V/A, limitação nominal 14,97 A; usa-se 1/6 V/A exato. |
| p. 21–22 | Cbat=400 mF, 20 V e 10 mΩ; gráfico alcança 27 V perto de 0,37 s | A estimativa CC ideal é 0,4×7/15=0,1867 s. A figura não identifica todos os parâmetros efetivos; não forçar o modelo para copiar o tempo da figura. |
| p. 22 | Corrente do indutor como corrente de recarga | Só coincidem em média estacionária quando a corrente do capacitor é desprezível. Medir também corrente no ramo da bateria. |
| p. 23 | Conclusões “ESCREVER” | Substituir por conclusões autorais apoiadas em cálculos e ensaios efetivamente executados. |

## Critério de projeto revisado

Mantêm-se tensão, corrente, frequência, relação de espiras e indutância de saída centrais. Revisam-se banco capacitivo, compensadores, margem de duty, rastreamento anti-windup e definição dos ensaios. Os modelos são equivalentes de engenharia com dispositivos por trechos lineares, não modelos completos de fabricante. Não há validação de placa, perdas de comutação, EMI, isolação ou envelhecimento da bateria.
