# Resultados executados e avaliação crítica

## Evidência e método

Foram concluídos oito ensaios no solver PLECS Standalone 5.0.6: três redes no degrau de carga, curto, bateria, comparação dos dois bancos capacitivos e refinamento numérico. Os CSVs preservam as saídas uniformemente amostradas; os retornos RPC compactados preservam a resposta original. Cada `_execucao.json` contém opções, data, hashes, duração e número de amostras. `metricas.json` é gerado após conferir o hash de cada CSV. Nenhuma curva do professor foi tratada como medição nova.

Médias e RMS usam integração trapezoidal. Regime resistivo: 0,08–0,10 s (20%), 0,18–0,20 s (100%) e 0,28–0,30 s (20%). FP usa 0,18–0,213333333 s, dois períodos completos de rede, com interpolação no extremo final. Ripple de comutação usa 0,1900–0,1901 s, cinco períodos, barramento CC de 373 V e resolução 0,2 µs. Os extremos são valores amostrados, não limites matemáticos de pico. Os gráficos globais usam redução de pontos para visualização; as métricas usam todos os pontos da janela.

## Degrau de carga e variação de rede

| Rede (Vrms) | Vo médio plena (V) | IL médio (A) | Vo pp em 20 ms (V) | Vbus mínimo (V) | Pentrada (W) | Irede RMS (A) | FP |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 176 | 26,7810 | 14,8820 | 0,1537 | 231,885 | 445,5 | 4,8500 | 0,5219 |
| 220 | 26,7510 | 14,8621 | 0,1480 | 296,466 | 440,0 | 4,0947 | 0,4884 |
| 264 | 26,7316 | 14,8525 | 0,1421 | 360,220 | 436,6 | 3,5706 | 0,4632 |

A saída leve nominal é 26,9999 V e 2,9999 A. Em plena carga há pequeno deslocamento para baixo na fronteira CC/CV. O seletor mínimo recebe sinais com ripple; o rastreamento integral do regulador momentaneamente inativo pode produzir erro médio diferente de zero, mesmo com integradores. Os Bodes de cada malha isolada não modelam essa alternância. A observação não deve ser atribuída apenas à precisão do solver: o refinamento mantém o deslocamento. Filtragem do sensor, histerese de modo ou anti-windup revisto precisam de nova validação se for exigida regulação mais estrita.

Na rede de 220 V, a aplicação da carga produz mínimo amostrado de 26,3064 V (−2,57% de 27 V); a retirada produz máximo de 27,4526 V (+1,68%). Em 176 V, os respectivos extremos são 26,2763 V e 27,4808 V. As janelas de 40 ms após cada evento não mostram crescimento sustentado de oscilação. A regra de acomodação em `metricas.json` usa média móvel de 100 µs e faixa de 1% em torno do valor final, não em torno de 27 V. Valores nulos significam que essa média já ficou dentro da faixa, e não resposta instantânea ou ausência de pico. Por isso o artigo privilegia os extremos e a curva completa.

A tensão média atende ±1% nas três redes simuladas, por margem pequena na rede alta; não se demonstrou robustez a tolerâncias. A ondulação em 20 ms mistura comutação e modulação pela rede. O duty de comando médio é 0,4019 na rede mínima e 0,3124 na nominal. A necessidade de ultrapassar 0,4 confirma a revisão para limite 0,45. A média de comando/2,1 não é exatamente a fração ligada porque o comando varia dentro do período. Uma média de PWM amostrado também sofre quantização de bordas; não confundir as duas medidas.

A corrente de rede é pulsada, apesar da tensão senoidal. FP=0,5219 em 176 V mostra que a afirmação FP<0,5 não é universal. Os valores dependem da carga, do capacitor e da impedância de rede assumida. Pentrada não comprova rendimento físico de 90%: os semicondutores têm perdas de condução simplificadas e não há perdas de comutação, núcleo ou EMI completas.

## Curto e recuperação

O ramo de 1 mΩ é conectado em 0,12 s e retirado em 0,24 s, em paralelo com 1,8 Ω. Em regime de curto, IL médio=15,00001 A; Vo médio=14,99168 mV; corrente do ramo=14,99168 A. A diferença é a pequena corrente no resistor de 1,8 Ω. O conversor limita a corrente média, mas há pico de IL=20,9910 A na aplicação do curto. Não há proteção instantânea de pico neste controlador.

A corrente do ramo de curto, calculada por Vo/1 mΩ, atinge 491,97 A na grade de 1 µs. É descarga do banco de saída, coerente com sua energia inicial próxima de 1,6 J e a ESR de 55 mΩ. O valor inicial de primeira ordem inclui também a corrente que já circulava no indutor. Não interpretar 15 A como limite desse pulso nem 492 A como previsão exata de hardware: ESL, indutância de cabos, chave, contatos e saturação não foram modelados. O pico amostrado é dependente desses elementos e da resolução.

Após a abertura do curto, o banco recarrega e a saída retorna à região de 26,75 V. O ensaio demonstra recuperação funcional do modelo, sem certificar SOA, dissipação, proteção da bateria ou segurança de interrupção física. No indutor proposto, o pico de 20,991 A implica B≈0,1468 T nominal ou 0,1615 T com L +10%, usando área mínima 529 mm² e 37 espiras. É abaixo do critério de 0,2 T adotado, mas a simulação usa L linear e não confirma saturação real.

## Recarga emulada

Modelo Ebat=20 V, Rbat=10 mΩ e Cbat=400 mF, em série. Na janela 0,04–0,06 s, IL médio=15,0007 A e Ibat médio=14,8373 A. A diferença de 0,1634 A carrega o banco de saída de 4,4 mF: não é erro no sensor. Aproximadamente Co·dVo/dt=0,0044×37≈0,163 A. A tensão chega a 26,9 V em 0,185084 s. O cálculo CC ideal Cbat·7/15=0,186667 s prevê corretamente a ordem temporal. A figura do professor próxima de 0,37 s não se reproduz automaticamente com os parâmetros escritos; não se alterou o capacitor para forçar concordância visual.

Na janela 0,5–0,55 s, Vo≈27,02484 V e corrente praticamente nula. A cauda entra em DCM, interrompe os pulsos e retém cerca de 25 mV de sobre-elevação porque o modelo não possui autodescarga ou caminho de potência reversa. Não representa flutuação perfeita em 27,000 V. A carga integrada em 0,6 s é 2,81003 C e a energia terminal integrada 66,4791 J; são grandezas do emulador, não capacidade de uma bateria de 150 Ah.

Para 150 Ah e excursão de 7 V, o equivalente coulômbico seria 77142,86 F. A razão para 0,4 F é 192857; não converter o tempo medido em um tempo real de carga por simples proporcionalidade sem modelo eletroquímico. O ajuste 0–15 A está implementado por Iref=6Vrefi; os ensaios centrais testam 15 A. Não se executou uma campanha em todos os ajustes intermediários, nem compensação por temperatura, SOC ou diferentes químicas.

## Ripple e cinco períodos PWM

| Caso em 373 Vcc | Co | ESR | Vo médio | Ripple medido | IL pp |
|---|---:|---:|---:|---:|---:|
| Capacitor original | 2200 µF | 110 mΩ | 26,9822 V | 0,321095 V | 3,09778 A |
| Banco revisado | 4400 µF | 55 mΩ | 26,7280 V | 0,165516 V | 3,10080 A |

A redução de ripple é 48,45%. O original viola 0,27 Vpp; a revisão atende. A previsão conservadora de 0,16670 V usa ΔIL=3 A, enquanto a medição tem 3,10 A por incluir quedas e condições reais do modelo. A soma conservadora recalculada com 3,10 A é cerca de 0,1723 V, acima da medição. A comparação troca somente C/ESR: mantém o controlador revisado, portanto não é reprodução integral da configuração PSIM original.

A revisão apresenta Vo=26,7280 V, erro −1,0073%, ultrapassando marginalmente o critério de ±1% no ensaio CC de 373 V. Esse ponto deve constar como ressalva da validação. Há atendimento do ripple e da limitação média; não há atendimento perfeito de todos os critérios em todos os pontos.

Cinco períodos duram 100 µs. O gráfico mostra portadora, comando, gate comum, tensão do primário e VDS de Q1. A magnetização retorna aproximadamente a zero a cada ciclo (mínimo numérico −0,12 mA), pico 99,03 mA. Q1 atinge 373,701 V e 4,99585 A, sem parasitas. Excitação e reset aparecem com sinais opostos no primário. Integrar sinais uniformemente amostrados em bordas pode gerar pequeno erro de volt-segundo; o retorno da corrente magnetizante é a evidência prática de reset neste modelo.

## Convergência e alcance

O ensaio nominal repetido com passo máximo 1 µs e RelTol=1e−7, contra 2 µs/1e−6, apresentou diferenças nas médias de plena carga de 0,011465% em Vo, 0,001625% em IL e 0,000480% em Vbus. Isto sustenta as médias reportadas, não a exatidão de cada pico submicrossegundo. O curto e a bateria não tiveram uma campanha independente completa de convergência.

Conclusão: o modelo executado cobre a faixa de rede, os degraus, o curto, a recarga emulada, a correção do ripple e a desmagnetização. As limitações relevantes são o deslocamento na transição CC/CV, picos de curto, aproximações das perdas, condição inicial pré-carregada, modelo linear dos magnéticos e ausência de bateria eletroquímica. Os Bodes são cálculos analíticos; as curvas temporais e métricas citadas aqui são resultados PLECS.
