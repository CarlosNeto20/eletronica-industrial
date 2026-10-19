# Métricas dos ensaios do carregador (PLECS)

Geradas por `analisar_ensaios.py` a partir dos CSV desta pasta. Médias e valores eficazes calculados por integração trapezoidal; nos transitórios, "antes" e "final" são médias por período de comutação e os extremos são valores instantâneos.


## Regime permanente com carga nominal (1,8 Ω)

| Grandeza | 176 V | 220 V | 264 V |
|---|---|---|---|
| Tensão máxima em C1 (V) | 247,5 | 309,7 | 371,9 |
| Tensão mínima em C1 (V) | 233,5 | 298,4 | 362,4 |
| Tensão média em C1 (V) | 240,8 | 304,2 | 367,3 |
| Ondulação em C1 (V) | 13,99 | 11,35 | 9,55 |
| Corrente eficaz da rede (A) | 6,03 | 5,34 | 4,85 |
| Corrente de pico da rede (A) | 30,8 | 30,4 | 30,0 |
| Potência de entrada (W) | 429,7 | 429,1 | 428,7 |
| Potência aparente (VA) | 1061 | 1175 | 1280 |
| Fator de potência | 0,405 | 0,365 | 0,335 |
| DHT da corrente | 2,20 | 2,51 | 2,78 |
| Fator de deslocamento | 0,977 | 0,985 | 0,990 |
| Corrente eficaz em C1 (A) | 6,17 | 5,57 | 5,11 |
| Corrente média num diodo da ponte (A) | 0,886 | 0,702 | 0,581 |
| Corrente eficaz num diodo da ponte (A) | 4,26 | 3,78 | 3,43 |
| Corrente de pico num diodo da ponte (A) | 30,7 | 30,4 | 30,0 |
| Tensão reversa num diodo da ponte (V) | 248,2 | 310,4 | 372,6 |
| Tempo de condução por pulso (ms) | 0,946 | 0,754 | 0,629 |
| Razão cíclica média | 0,396 | 0,313 | 0,259 |
| Corrente média em Lo (A) | 14,97 | 14,97 | 14,97 |
| Corrente máxima em Lo (A) | 16,26 | 16,42 | 16,53 |
| Corrente mínima em Lo (A) | 13,69 | 13,53 | 13,42 |
| Tensão média na saída (V) | 26,95 | 26,95 | 26,95 |
| Ondulação da tensão de saída (V) | 0,268 | 0,301 | 0,323 |
| Tensão máxima nas chaves (V) | 248,2 | 310,4 | 372,6 |
| Corrente de pico nas chaves (A) | 4,97 | 5,02 | 5,05 |
| Corrente eficaz nas chaves (A) | 2,86 | 2,54 | 2,32 |
| Corrente média nas chaves (A) | 1,79 | 1,42 | 1,18 |
| Corrente magnetizante de pico (A) | 0,095 | 0,095 | 0,095 |
| Tensão reversa em D2 (V) | 74,0 | 92,6 | 111,3 |
| Corrente média em D2 (A) | 5,93 | 4,69 | 3,89 |
| Corrente eficaz em D2 (A) | 9,43 | 8,40 | 7,64 |
| Tensão reversa em D1 (V) | 73,5 | 92,2 | 110,8 |
| Corrente média em D1 (A) | 9,04 | 10,28 | 11,09 |
| Corrente eficaz em D1 (A) | 11,65 | 12,43 | 12,91 |
| Corrente eficaz em C4 (A) | 0,71 | 0,80 | 0,87 |
| Potência de saída (W) | 403,5 | 403,5 | 403,5 |
| Rendimento | 0,939 | 0,940 | 0,941 |
| Tensão de controle mínima (V) | 1,50 | 1,27 | 1,10 |
| Tensão de controle máxima (V) | 1,94 | 1,72 | 1,58 |
| Saída do compensador de tensão (V) | 5,00 | 5,00 | 4,99 |
| Saída do compensador de corrente (V) | 1,21 | 0,98 | 0,81 |

## Degrau de carga (valores nominais do projeto)

| Rede | Degrau | Vbat antes (V) | Vbat máx (V) | Vbat mín (V) | Vbat final (V) | IL antes / final (A) | IL máx (A) | Acomodação a ±1 % (ms) | vCv antes (V) |
|---|---|---|---|---|---|---|---|---|---|
| 176 V | 100 → 20 % | 26,95 | 29,33 | 26,32 | 27,01 | 14,97 / 3,00 | 16,22 | 1,62 | 5,00 |
| 176 V | 20 → 100 % | 27,01 | 27,49 | 25,62 | 26,93 | 3,00 / 14,97 | 22,59 | 0,38 | 1,74 |
| 264 V | 100 → 20 % | 26,95 | 29,47 | 26,33 | 27,01 | 14,97 / 3,00 | 16,57 | 1,62 | 5,00 |
| 264 V | 20 → 100 % | 27,01 | 27,53 | 25,62 | 27,01 | 3,00 / 15,01 | 20,79 | 0,20 | 1,41 |

## Degrau de carga com folga no limite de corrente (Vrefi = 2,6 V)

| Rede | Degrau | Vbat antes (V) | Vbat máx (V) | Vbat mín (V) | Vbat final (V) | IL antes / final (A) | IL máx (A) | Acomodação a ±1 % (ms) | vCv antes (V) |
|---|---|---|---|---|---|---|---|---|---|
| 176 V | 100 → 20 % | 27,01 | 28,42 | 26,65 | 27,01 | 15,01 / 3,00 | 15,88 | 0,07 | 1,76 |
| 176 V | 20 → 100 % | 27,01 | 27,59 | 25,62 | 27,01 | 3,00 / 15,00 | 23,21 | 0,39 | 1,74 |
| 264 V | 100 → 20 % | 27,01 | 28,44 | 26,66 | 27,01 | 15,01 / 3,00 | 16,08 | 0,06 | 1,42 |
| 264 V | 20 → 100 % | 27,01 | 27,53 | 25,62 | 27,01 | 3,00 / 15,01 | 20,79 | 0,20 | 1,41 |

## Curto-circuito na saída (1 mΩ)

| Rede | IL antes (A) | IL máx no curto (A) | IL em curto (A) | Pico em D15 (A) | Subida de Vbat até 90 % (ms) | Vbat final (V) | IL durante a subida (A) |
|---|---|---|---|---|---|---|---|
| 176 V | 14,97 | 17,63 | 14,97 | 256 | 9,4 | 26,93 | 14,96 |
| 264 V | 14,97 | 17,48 | 14,97 | 256 | 9,4 | 26,92 | 14,97 |

## Recarga da bateria (R22 = 10 mΩ, C2 = 0,8 F, VDC1 = 20 V)

| Rede | Corrente de recarga (A) | Vbat inicial (V) | Inclinação (V/s) | Fim da corrente constante (s) | Vbat final (V) | IL final (A) | Vbat máx (V) |
|---|---|---|---|---|---|---|---|
| 176 V | 14,97 | 20,28 | 18,7 | 0,378 | 27,02 | 0,000 | 27,16 |
| 264 V | 14,97 | 20,28 | 18,7 | 0,379 | 27,02 | 0,000 | 27,17 |
