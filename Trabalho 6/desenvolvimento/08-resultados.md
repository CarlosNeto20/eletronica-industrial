# 08. Resultados de simulação

Execução no PLECS Standalone 5.0.3 de 64 bits, em 9 de novembro de 2026, pela interface XML-RPC na porta 1080. Dos 71 ensaios da matriz, 70 terminaram e 1 falhou por limite de tempo de relógio. A única falha é o `diag_cc_sem_20ms`, que faz parte do grupo de diagnóstico e cuja falha é o próprio resultado procurado, como a seção 2 explica. Nenhum resultado foi criado para ensaio que não terminou.

Todos os números deste arquivo são de classe S, isto é, vieram do solver do PLECS. Cada um está ligado ao arquivo do modelo, às opções do solver, ao CSV e ao registro `*_execucao.json` por resumo criptográfico, de modo que `analisar_resultados.py` recusa qualquer CSV cujo hash não bata com o registro ou cujo modelo tenha mudado depois da execução. As comparações marcadas como cálculo são de classe A e vêm de `calculos/parametros.json`. As métricas completas estão em `metricas.json` e em `metricas.md`, e os gráficos em `resultados PLECS/graficos`.

As janelas de regime têm número inteiro de ciclos de 60 Hz e as integrais são trapezoidais sobre a grade de saída, que não é uniforme. Em modo rede a janela vai de 4/60 s a 6/60 s e em modo bateria de 10/60 s a 12/60 s. Nas curvas de regulação a janela é de 0,1 s a 0,2 s, seis ciclos completos.

## 1. Tempos de execução

| Grupo | Ensaios | Tempo por ensaio |
|---|---|---|
| Diagnóstico do CC-CC | 5 | 0,16 s a 2,8 s, exceto a falha de 90 s |
| Retificador | 3 | cerca de 0,6 s |
| Elevador | 2 | 11 s |
| Inversor | 6 | 1,7 s a 9,7 s |
| No-break, seção 6 e verificação | 11 | 48 s a 103 s |
| Regulação, quatro famílias de 11 pontos | 44 | 25 s por lote de 11 em rede e 404 s em bateria |

O modelo completo é cerca de cinquenta vezes mais lento que o do retificador, o que era de esperar: ele tem 115 componentes, seis interruptores comandados a 20 kHz e duas pontes de diodos. Os ensaios de regulação em bateria são os mais caros porque o CC-CC comuta durante os 0,2 s inteiros.

## 2. Diagnóstico numérico do conversor CC-CC

Na primeira rodada o ensaio `elev_42` ficou mais de cinco minutos sem terminar, embora os mesmos 2 ms do teste de carga tivessem levado 0,125 s. A hipótese era que, quando a corrente de um ramo se anula com a chave e o diodo abertos, o nó correspondente fica sem caminho para a corrente e sem capacitância, o que leva o solver a um sistema mal condicionado. O grupo de diagnóstico mede isso diretamente.

| Ensaio | Amortecedores RC | Duração simulada | Tempo de relógio |
|---|---|---|---|
| `diag_cc_sem_5ms` | não | 5 ms | 0,16 s |
| `diag_cc_sem_partida_5ms` | não, partindo de corrente nula | 5 ms | 0,21 s |
| `diag_cc_sem_20ms` | não | 20 ms | falhou em 90 s |
| `diag_cc_amort_20ms` | sim | 20 ms | 2,8 s |
| `diag_cc_amort_partida_5ms` | sim, partindo de corrente nula | 5 ms | 0,63 s |

O resultado é claro. Sem os ramos RC, 5 ms terminam em 0,16 s mas 20 ms não terminam em 90 s, o que mostra que o problema não é o tamanho do intervalo e sim um estado que o circuito alcança depois de alguns milissegundos. Com ramos RC de 33 Ω e 1 nF em paralelo com S1, com S2 e com o secundário de T_32, os mesmos 20 ms terminam em 2,8 s, trinta vezes mais rápido que o limite, e a tensão média do barramento é a mesma dos ensaios curtos sem amortecedor, 202,9 V contra 200,9 V. Os amortecedores representam a capacitância de saída das chaves, da ordem de 1 nF para MOSFETs dessa classe, e por isso não são um artifício numérico, e sim um elemento físico que faltava. A perda neles é da ordem de 0,4 W cada, cerca de 1 W nos três, desprezível diante de 2250 W.

A falha do `diag_cc_sem_20ms` fica registrada como falha, com a mensagem do PLECS, e não é usada como resultado em nenhuma outra parte do trabalho.

## 3. Retificador e barramento

Janela de regime de 0,10 s a 0,15 s, nos ensaios do modelo `retificador_barramento`.

| Grandeza | Cálculo (A) | `ret_176_planilha` (S) | `ret_176_anexo` (S) | `ret_264_anexo` (S) |
|---|---|---|---|---|
| Tensão média do barramento (V) | 230,2 | 231,28 | 227,99 | 357,30 |
| Vale do barramento (V) | 211,57 | 212,02 | 210,67 | 345,42 |
| Ondulação (Vpp) | 37,33 | 36,86 | 33,79 | 23,42 |
| Pico em D1 (A) | 110,68 | 96,02 | 66,28 | 58,41 |
| Corrente média em D1 (A) | 4,886 | 4,907 | 4,839 | 3,082 |
| Corrente eficaz em D1 (A) | 16,44 | 17,98 | 15,82 | 11,91 |
| Corrente eficaz em C4 (A) | 21,10 | 23,46 | 20,12 | 15,65 |
| Duração do pulso (ms) | 1,472 | 1,615 | 1,919 | 1,363 |
| Fator de potência de entrada | não previsto | 0,509 | 0,586 | 0,508 |

O que confere. Nas condições idealizadas da seção 3, com 1,796 mF, diodos ideais e sem resistência série, o vale medido é 212,02 V contra 211,57 V calculados, uma diferença de 0,2%. O dimensionamento de C1 e o ângulo de condução, portanto, estão corretos. A corrente média no diodo bate em menos de 0,5%, o que era esperado, porque a média depende apenas da carga transferida por ciclo e não do formato do pulso.

O que não confere, e por quê. O pico de corrente previsto pela aproximação de pulso retangular, 2·I_chg = 110,68 A, superestima em 15% o valor simulado nas mesmas condições, 96,02 A, porque o pulso real não é retangular e sim aproximadamente senoidal recortado. Com os 0,1 Ω entre a ponte e o barramento, que o Anexo 01 inclui e a planilha não, o pico cai para 66,28 A, 40% abaixo da previsão. O mesmo elemento alarga o pulso de 1,6 ms para 1,9 ms e reduz a corrente eficaz no capacitor de 23,46 A para 20,12 A. A conclusão prática é que o pico de corrente no diodo e no capacitor depende fortemente da impedância do laço de recarga, que não entra no dimensionamento da planilha. Para especificar o diodo e o capacitor, o valor relevante é o do circuito com a impedância real, e não o da fórmula.

Com os 1880 µF adotados, maiores que os 1796 µF calculados, a ondulação cai de 37,33 V para 33,79 V e o vale sobe para 210,67 V, acima do mínimo de 210 V exigido pelo CC-CC, mas com margem de apenas 0,67 V. A tolerância de −20% dos eletrolíticos, discutida em [09](09-componentes-e-melhorias.md), consome essa margem inteira, o que reforça a recomendação de usar seis capacitores em vez de quatro.

A 264 V o vale fica em 345,42 V contra 348,93 V previstos pela mesma conta com 1880 µF, diferença de 1%, e o fator de potência de entrada permanece em torno de 0,51, valor típico de retificador com filtro capacitivo sem correção.

![Retificador a 176 V](../resultados%20PLECS/graficos/retificador_176.png)

## 4. Conversor CC-CC elevador

Janela de regime de 0,08 s a 0,10 s e janela de detalhe nos 2 ms finais, com carga resistiva de 19,6 Ω, equivalente a 2250 W em 210 V.

| Grandeza | 42 V cálc. | 42 V sim. | 56 V cálc. | 56 V sim. |
|---|---|---|---|---|
| Barramento (V) | 210,0 | 202,91 | 210,0 | 205,94 |
| Tensão em C8 (V) | 140,0 | 136,19 | 140,0 | 137,78 |
| Tensão em C7 (V) | 70,0 | 66,72 | 70,0 | 68,16 |
| Corrente média da bateria (A) | 53,57 | 51,13 | 40,18 | 39,33 |
| Ondulação ΔILb (App) | 10,71 | 10,51 | 7,14 | 7,03 |
| Tensão de bloqueio de S1 (V) | 140,0 | 142,03 | 140,0 | 142,79 |
| Razão cíclica medida | 0,700 | 0,702 | 0,600 | 0,603 |
| Corrente eficaz em S1 (A) | não prevista | 24,86 | não prevista | 18,99 |
| Corrente eficaz em D17 (A) | não prevista | 10,35 | não prevista | 9,06 |
| Corrente eficaz no secundário (A) | não prevista | 16,56 | não prevista | 14,62 |
| Ondulação do barramento (Vpp) | não prevista | 1,04 | não prevista | 0,80 |

O ganho se confirma com erro de 3,4% a 42 V e 1,9% a 56 V. A diferença é sempre para menos e cresce com a corrente, o que identifica a causa: as quedas nos diodos rápidos, a resistência de condução das chaves e as resistências dos enrolamentos, nenhuma delas presente no balanço de volt-segundo ideal. A repartição entre C8 e C7 segue a prevista, dois terços e um terço, e a ondulação em L_b bate em 2%, o que confirma tanto o valor de L_b quanto o fato de o indutor ver o dobro da frequência de comutação.

Uma correção importante saiu deste ensaio. A tabela de [06](06-conversor-cc-cc-elevador.md) dizia que S1 e S2 bloqueiam VC8/2 = 70 V. O PLECS mede 142 V de pico sobre S1, praticamente a tensão de C8. A dedução das etapas de operação, no mesmo arquivo, já dizia que o dreno da chave aberta sobe até VC8 pelo seu próprio diodo, de modo que o erro estava na tabela e no texto, não na dedução: os 70 V são a tensão sobre cada enrolamento do primário, que é outra grandeza. O item foi acrescentado à auditoria, que passou a ter 50 linhas, e a seleção de componentes em [09](09-componentes-e-melhorias.md) foi revista, porque um MOSFET de 150 V ficaria com menos de 6% de margem sobre o valor medido. A vantagem da célula de três estados continua, mas é de dois terços do barramento e não de um terço.

O rendimento do modelo é 97,8% a 42 V e 98,2% a 56 V. Ele conta apenas as quedas de condução e dos diodos, porque não há perdas de comutação no modelo, e por isso não deve ser usado como previsão de rendimento real.

![CC-CC a 42 V](../resultados%20PLECS/graficos/elevador_42.png)

## 5. Inversor com barramento ideal

Janela de regime de 0,05 s a 0,10 s, com fonte de tensão contínua ideal no lugar do barramento.

| Ensaio | Vo eficaz (V) | DHT de vo (%) | M efetivo | M previsto | ΔILo no pico (App) | Fator de crista |
|---|---|---|---|---|---|---|
| `inv_373_res` | 114,87 | 0,13 | 0,491 | 0,436 | 6,28 | 1,415 |
| `inv_2116_res` | 114,75 | 0,13 | 0,813 | 0,769 | 2,96 | 1,415 |
| `inv_373_vazio` | 114,85 | 0,13 | 0,483 | 0,436 | 6,26 | sem carga |
| `inv_2116_vazio` | 114,71 | 0,13 | 0,801 | 0,769 | 2,97 | sem carga |
| `inv_2116_nl` | 114,78 | 1,19 | 0,866 | 0,769 | 3,65 | 2,754 |

A malha regula a saída em 114,7 V a 114,9 V eficazes em todos os casos, dentro de 0,3% dos 115 V de referência, e a distorção da tensão fica em 0,13% com carga linear. Com a carga não linear do Anexo 01 a corrente tem fator de crista 2,75, próximo do valor de referência 3, e a distorção da tensão sobe para 1,19%, ainda muito abaixo do limite de 8% adotado para esse tipo de carga. O pico de corrente no indutor chega a 79,1 A nesse ensaio, contra 27,3 A com carga resistiva, o que é o dado relevante para o projeto do magnético e para a escolha dos interruptores.

A ondulação do indutor a 373 V, 6,28 A, bate com o cálculo de 6,28 A com quatro algarismos, o que valida a expressão usada e o valor de Lo. A 211,57 V o cálculo prevê 3,62 A e a simulação dá 2,96 A, 18% abaixo; a diferença vem de a expressão analítica usar o pulso máximo em vez do pulso efetivo no pico com o índice de modulação medido.

O índice de modulação efetivo é sistematicamente maior que o previsto, 0,813 contra 0,769 no caso de 211,57 V com carga resistiva, porque o modulante precisa compensar as quedas nos interruptores e no indutor, que a previsão não inclui. Com a carga não linear ele chega a 0,866 e ultrapassa o limite de 0,85 adotado. Esse é o primeiro critério que não é atendido, e ele reaparece no modelo completo em modo bateria.

No degrau de vazio para 2100 W aplicado no pico da tensão, o erro instantâneo fica entre −25,36 V e +7,37 V nos 4 ms seguintes, e o valor eficaz passa de 114,71 V para 114,75 V em dois ciclos, sem oscilação sustentada. É a verificação temporal da margem de fase calculada em [05](05-malha-de-tensao-do-inversor.md).

![Inversor a 211,6 V](../resultados%20PLECS/graficos/inversor_2116.png)

## 6. No-break completo, grupos da seção 6

A seção 6 da planilha pede três grupos de formas de onda. O grupo (a) é a tensão da fonte e a corrente de entrada através de SS2, o grupo (b) é a tensão do barramento e a corrente da bateria e o grupo (c) é a tensão e a corrente de saída. A falta da rede ocorre em 0,1 s, no cruzamento por zero, e o CC-CC é habilitado no mesmo instante.

### Grupo (a), entrada, em modo rede

| Ensaio | Vin eficaz (V) | Iin eficaz (A) | Pico de Iin (A) | Pin (W) | Fator de potência | DHT de iin (%) | Ieficaz em C4 (A) |
|---|---|---|---|---|---|---|---|
| `nb_176_nl` | 176,0 | 24,62 | 82,8 | 2401 | 0,554 | 146,1 | 19,69 |
| `nb_176_lin` | 176,0 | 21,87 | 67,8 | 2251 | 0,585 | 134,4 | 17,47 |
| `nb_220_lin` | 220,0 | 18,24 | 64,8 | 2151 | 0,536 | 154,0 | 17,07 |
| `nb_220_nl` | 220,0 | 19,66 | 75,7 | 2243 | 0,519 | 160,3 | 18,74 |
| `nb_264_lin` | 264,0 | 16,31 | 62,4 | 2169 | 0,504 | 168,5 | 15,92 |
| `nb_264_nl` | 264,0 | 17,45 | 71,4 | 2268 | 0,492 | 172,5 | 18,46 |
| `nb_220_rl3k` | 220,0 | 18,23 | 62,9 | 2182 | 0,544 | 150,7 | 19,38 |

O fator de potência de entrada fica entre 0,49 e 0,59 e piora com a tensão de rede, como é característico de retificador com filtro capacitivo: quanto maior a tensão, mais curto o pulso de condução e maior a distorção da corrente, que vai de 134% a 173%. A corrente eficaz de entrada cai de 24,6 A a 176 V para 16,3 A a 264 V, mantida a mesma potência de saída, mas o pico se mantém entre 62 A e 83 A em todos os casos. A corrente eficaz no banco do barramento fica entre 15,9 A e 19,7 A, próxima dos 21,1 A calculados para o pior caso, o que sustenta a discussão de dimensionamento do banco em [09](09-componentes-e-melhorias.md).

### Grupos (b) e (c), barramento, bateria e saída

| Ensaio | Modo | Vbus médio (V) | Vbus mínimo (V) | Ondulação (Vpp) | Ibat médio (A) | Vo eficaz (V) | DHT (%) | M efetivo | Rendimento |
|---|---|---|---|---|---|---|---|---|---|
| `nb_176_nl` | rede | 240,8 | 223,8 | 20,1 | 0,00 | 114,82 | 1,04 | 0,780 | 0,893 |
| `nb_176_nl` | bateria | 207,1 | 180,5 | 39,4 | 55,34 | 114,73 | 1,01 | 0,870 | 0,917 |
| `nb_176_lin` | rede | 230,8 | 218,0 | 26,3 | 0,00 | 114,80 | 0,25 | 0,735 | 0,930 |
| `nb_176_lin` | bateria | 203,9 | 190,6 | 24,6 | 52,26 | 114,69 | 0,27 | 0,873 | 0,952 |
| `nb_220_lin` | rede | 295,2 | 283,7 | 22,8 | 0,00 | 114,85 | 0,18 | 0,598 | 0,974 |
| `nb_220_nl` | rede | 303,3 | 286,6 | 19,6 | 0,00 | 114,86 | 0,86 | 0,634 | 0,954 |
| `nb_264_lin` | rede | 358,9 | 348,5 | 20,2 | 0,00 | 114,88 | 0,15 | 0,503 | 0,966 |
| `nb_264_nl` | rede | 365,6 | 349,8 | 18,6 | 0,00 | 114,89 | 0,72 | 0,533 | 0,943 |
| `nb_264_nl` | bateria | 207,1 | 180,3 | 40,0 | 55,19 | 114,73 | 1,01 | 0,870 | 0,920 |
| `nb_220_rl3k` | rede | 289,9 | 282,3 | 24,2 | 0,00 | 114,81 | 0,17 | 0,608 | 0,959 |
| `nb_220_rl3k` | bateria | 205,0 | 187,9 | 30,5 | 53,03 | 114,60 | 0,26 | 0,851 | 0,936 |

Três leituras saem desta tabela.

A primeira é que a saída permanece regulada em 114,6 V a 114,9 V eficazes nos onze casos, com a rede presente ou ausente, com carga linear, não linear ou RL de 3 kVA. A distorção da tensão de saída fica entre 0,15% e 0,27% com carga linear e entre 0,72% e 1,04% com carga não linear, bem dentro dos limites de 5% e 8% adotados. O objetivo central do no-break, manter a tensão da carga, é cumprido.

A segunda é que em modo bateria o barramento médio fica entre 203,9 V e 207,1 V, dentro da faixa de 210 V ± 5%, mas o valor instantâneo mínimo cai a 180 V a 191 V por causa da ondulação de 120 Hz. A ondulação medida, de 24,6 Vpp com carga linear e até 40 Vpp com carga não linear, é bem maior que os 15,1 Vpp previstos pela conta que supõe que só C4 absorve a componente alternada. O CC-CC não sustenta o barramento dentro de um ciclo de 60 Hz, porque opera em malha aberta com razão cíclica fixa; é o capacitor que faz esse trabalho, e C7 e C8, de 10 µF cada, pouco ajudam.

A terceira decorre da segunda. Com o barramento mais baixo, o índice de modulação efetivo em modo bateria sobe para 0,851 a 0,873 e ultrapassa o limite de 0,85 adotado. Não houve perda de regulação nem distorção perceptível nesses ensaios, porque a margem até a saturação do modulante ainda existe, mas a folga é pequena. Esse é o segundo critério não atendido e tem solução conhecida: regular o CC-CC em malha fechada em vez de usar razão cíclica fixa, ou aumentar a capacitância do barramento.

O rendimento medido vai de 0,885 a 0,98 em modo rede e de 0,917 a 0,952 em modo bateria. Ele conta apenas perdas de condução e quedas de diodos, e por isso é um limite superior, não uma previsão.

![No-break a 176 V com carga não linear](../resultados%20PLECS/graficos/nb_176_nl.png)

## 7. Transferência de rede para bateria

A continuidade foi medida pelo valor eficaz da tensão de saída em cada semiciclo de 60 Hz, de três semiciclos antes a doze semiciclos depois da falta.

| Ensaio | Instante da falta | Menor eficaz por semiciclo (V) | Maior (V) | Queda | Vbus mínimo após a falta (V) | Pico de Ibat (A) |
|---|---|---|---|---|---|---|
| `nb_176_nl` | cruzamento por zero | 114,68 | 114,82 | 0,12% | 174,2 | 198,9 |
| `nb_176_nl_pico` | pico positivo | 114,68 | 114,82 | 0,12% | 175,3 | 191,5 |
| `nb_176_lin` | cruzamento por zero | 114,66 | 114,80 | 0,12% | 190,4 | 123,5 |
| `nb_264_nl` | cruzamento por zero | 114,68 | 114,89 | 0,18% | 173,9 | 201,0 |
| `nb_220_rl3k` | cruzamento por zero | 114,60 | 114,81 | 0,18% | 187,4 | 136,4 |

A queda máxima no valor eficaz por semiciclo é de 0,18%, muito abaixo do critério de 10% adotado, e o instante da falta quase não importa: abrir SS2 no pico da tensão, quando a ponte conduz, dá o mesmo resultado de abrir no cruzamento por zero. A razão é que o capacitor do barramento sustenta a tensão durante a transição, e aqui a detecção é ideal, sem atraso. Com um tempo de detecção real, de alguns milissegundos, o barramento cairia mais antes de o CC-CC assumir, e esse é o ponto que a simulação não cobre.

O barramento desce a 174 V a 191 V logo após a falta, abaixo do valor de regime em bateria, e o pico de corrente da bateria chega a 199 A a 201 A com carga não linear, quase quatro vezes a corrente média de regime. Esse pico define o cabeamento, o fusível e a capacidade de pico do banco, e não aparece em nenhuma conta da planilha.

![Transferência a 176 V](../resultados%20PLECS/graficos/transferencia_176_nl.png)

O ensaio `nb_220_retorno` acrescenta o retorno da rede em 0,2 s, também no cruzamento por zero. O pico de corrente de entrada chega a 134,1 A, limitado apenas pelos 0,1 Ω entre a ponte e o barramento, porque o barramento está em 208 V e a rede volta com pico de 311 V. Esse é um resultado do modelo adotado e indica que um no-break construído assim precisa de limitação da corrente de recarga, por termistor com relé de bypass ou por pré-carga comandada. O assunto não aparece no projeto de partida e entra como recomendação em [09](09-componentes-e-melhorias.md).

### Comparação com o comando permanente do Anexo 01

No circuito PSIM do professor as chaves do CC-CC ficam comandadas o tempo todo com D = 0,7. O ensaio `nb_176_nl_anexo` repete o caso de 176 V com esse comando. Com a rede presente, a bateria entrega 4,54 A em média, contra zero no ensaio com o CC-CC em espera, o que confirma por medida o que [06](06-conversor-cc-cc-elevador.md) previa: um elevador em malha aberta não fica parado quando o barramento está acima da sua tensão natural, ele passa a operar em condução descontínua e continua drenando potência da bateria. Em modo bateria os dois ensaios dão exatamente o mesmo resultado, como deveriam. A lógica de habilitação na falta, adotada nos ensaios principais, é portanto parte do projeto e não um detalhe de simulação.

![CC-CC em espera e sempre comandado](../resultados%20PLECS/graficos/cc_espera_vs_anexo.png)

## 8. Curvas de regulação Vo = f(Po)

Onze pontos por família, de 0 a 2100 W em passos de 210 W, com carga resistiva nominal R = 115²/P. Janela de regime de 0,1 s a 0,2 s.

| Família | Vo em vazio (V) | Vo a 2100 W (V) | RV | DHT a 2100 W (%) | M efetivo a 2100 W |
|---|---|---|---|---|---|
| Rede de 176 V | 114,755 | 114,800 | −0,039% | 0,25 | 0,734 |
| Rede de 220 V | 114,812 | 114,846 | −0,029% | 0,18 | 0,596 |
| Rede de 264 V | 114,850 | 114,876 | −0,022% | 0,15 | 0,498 |
| Bateria de 42 V | 114,780 | 114,693 | 0,077% | 0,27 | 0,873 |

O coeficiente de regulação, definido como a variação relativa entre vazio e plena carga, fica em módulo abaixo de 0,08% nas quatro famílias, muito abaixo do limite de 2% adotado. Nas três famílias com rede o sinal é negativo, isto é, a tensão de saída é ligeiramente maior em plena carga que em vazio. Isso não é um erro: com o amortecimento do filtro LC variando com a carga, o ganho do laço em 60 Hz muda um pouco e o erro de regime, que é pequeno mas não nulo, muda de sinal. A amplitude total do efeito é de 45 mV em 115 V.

A escala vertical do gráfico cobre apenas 0,2 V, de modo que as retas parecem inclinadas sem que isso signifique variação relevante. O ponto de vazio da família em bateria destoa dos demais porque, sem carga, o CC-CC em malha aberta deixa o barramento subir até 253 V em vez dos cerca de 208 V dos demais pontos; é a mesma ausência de malha fechada discutida na seção 6.

![Curvas de regulação](../resultados%20PLECS/graficos/regulacao.png)

## 9. Verificação numérica

O ensaio `conv_176_nl` repete o `nb_176_nl` com passo máximo de 1 µs, cinco vezes menor, e tolerância relativa de 10⁻⁷, dez vezes menor.

| Grandeza | Base | Refinado | Diferença relativa |
|---|---|---|---|
| Vo eficaz em rede (V) | 114,82 | 114,82 | 4·10⁻⁹ |
| DHT de vo em rede (%) | 1,0401 | 1,0401 | 9·10⁻⁶ |
| Vbus médio em rede (V) | 240,84 | 240,84 | 7·10⁻⁸ |
| Vo eficaz em bateria (V) | 114,73 | 114,73 | 6·10⁻⁹ |
| Ibat médio em bateria (A) | 55,335 | 55,335 | 6·10⁻⁸ |

As diferenças são da ordem de 10⁻⁶ por cento, isto é, nenhuma conclusão deste arquivo depende da escolha do passo ou da tolerância. A localização dos eventos de comutação pelo solver, independente da grade de saída, é o que garante isso.

Uma correção foi feita depois da primeira análise. A janela `depois` do ensaio `inv_degrau_2116` terminava em 121 ms, além dos 100 ms simulados, o que fazia o valor eficaz incluir uma extrapolação constante e dava 70,6 V em vez do valor real. A janela foi corrigida para dois ciclos inteiros terminando no fim do ensaio, o ensaio foi reexecutado e o resultado correto, 114,75 V, está na seção 5. Uma verificação automática passou a conferir que toda janela declarada cabe dentro do tempo simulado de cada ensaio.

## 10. O que atende e o que não atende

| Critério | Limite | Resultado | Situação |
|---|---|---|---|
| Tensão eficaz de saída em regime | 115 V ± 2% | 114,60 V a 114,89 V em todos os ensaios | Atende |
| Coeficiente de regulação RV | ≤ 2% | ≤ 0,08% em módulo nas quatro famílias | Atende |
| DHT da tensão de saída, carga linear | ≤ 5% | 0,13% a 0,27% | Atende |
| DHT da tensão de saída, carga não linear | ≤ 8% | 0,72% a 1,19% | Atende |
| Ondulação ΔILo no pico | ≤ 10,33 A | 2,96 A a 6,28 A | Atende |
| Vale do barramento a 176 V com rede | ≥ 210 V | 218,0 V com carga linear e 223,8 V com não linear | Atende, com margem pequena nas condições da planilha |
| Barramento em bateria, valor médio | 210 V ± 5% | 203,9 V a 207,1 V | Atende |
| Barramento em bateria, valor instantâneo | 210 V ± 5% | mínimo de 180,3 V a 190,6 V | Não atende |
| Índice de modulação efetivo em regime | < 0,85 | 0,48 a 0,78 em modo rede | Atende em modo rede |
| Índice de modulação efetivo em regime | < 0,85 | 0,851 a 0,873 em modo bateria e 0,866 no inversor com carga não linear | Não atende |
| Estabilidade | sem oscilação sustentada fora de 60 Hz e 2fs | nenhuma observada em 71 ensaios | Atende |
| Continuidade na transferência | queda ≤ 10% no eficaz por semiciclo | 0,12% a 0,18% | Atende |

Os dois critérios não atendidos têm a mesma origem e a mesma solução. O barramento em modo bateria é baixo e ondula muito porque o CC-CC opera em malha aberta com razão cíclica fixa e porque a capacitância do barramento foi dimensionada para o modo rede. Regular o CC-CC em malha fechada, com referência acima do vale do retificador, ou aumentar o banco do barramento resolve os dois ao mesmo tempo. A recomendação já estava em [09](09-componentes-e-melhorias.md) por outros motivos e agora tem medida que a sustenta.

## 11. Limitações destes resultados

Valem para todos os números deste arquivo. Os modelos não têm tempo morto nem perdas de comutação, de modo que os rendimentos citados são limites superiores e as formas de onda não mostram os efeitos de recuperação reversa. Os indutores são lineares e o transformador não satura, o que importa principalmente no pico de 79 A do indutor de saída com carga não linear e nos picos de 199 A da bateria na transferência. A bateria é uma fonte de tensão ideal, sem resistência interna nem queda com a descarga. Não há modelo térmico nem de interferência eletromagnética. A lógica de transferência é ideal, com detecção instantânea da falta, o que torna a continuidade medida otimista. As condições iniciais evitam o transitório de partida e portanto não certificam a partida real, que exigiria pré-carga do barramento e partida suave do inversor. A seleção de componentes de [09](09-componentes-e-melhorias.md) continua preliminar, de classe H, e nenhum ensaio de bancada foi feito.

Próximo arquivo: [09. Componentes e melhorias](09-componentes-e-melhorias.md).
