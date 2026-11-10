# 02. Auditoria do documento do professor

Antes de reproduzir qualquer número, toda a planilha foi reconstruída em `calculos.py`. Cada valor impresso foi comparado com o recalculado, e a decisão tomada para cada um está em `calculos/auditoria.csv` (50 itens, com local, valor impresso, valor recalculado, desvio, decisão e justificativa). Este arquivo resume a tabela e discute os pontos que exigiam verificação. A regra geral foi manter os valores centrais do professor e revisar só o que é inconsistente, sempre dizendo por quê.

## 1. Resultado global

Todos os valores numéricos impressos nas seções 3, 4 e 5 conferem com o recálculo dentro do arredondamento de impressão, com desvios inferiores a 0,05%. Os problemas encontrados são de texto, de rótulo ou de hipótese, e não de aritmética. Nenhum componente do professor precisou ser trocado. As revisões ficam no plano da análise (barramento mínimo, margens, ondulação real, potência da bateria) e da representação no PLECS (lógica de transferência e carga não linear).

| Local | Item | Impresso | Recalculado (A) | Decisão |
|---|---|---|---|---|
| p.3 | ΔVC (texto diz 10% do pico) | 37,33 V | 37,33 V = 15% de 248,90 V | Mantido; texto corrigido |
| p.4 e p.5 | VC1max, VC1min, θC1, C1 | 248,902 V; 211,572 V; 0,555 rad; 1,796 mF | idem | Mantido; banco de 1880 µF |
| p.5 e p.6 | Ichg, IC1ef, ID1med, ID1ef | 55,341; 21,103; 4,886; 16,444 A | idem | Mantido como aproximação de pulso retangular |
| p.6 | ID1pk = 2·Ichg | 110,681 A | idem | Estimativa a comparar com o PLECS |
| p.7 | Vimin_cc rotulado "tensão eficaz nominal" | 223 V | vale de 211,57 V | Análise feita em 211,57 V (rede) e 210 V (bateria) |
| p.7 | Mmax | 0,729 | 0,769 (211,57 V); 0,774 (210 V) | Ambos abaixo de 0,85 |
| p.8 | Lo | 365,6 µH | 365,55 µH | Mantido; dedução conservadora |
| p.8 | Co (texto cita fs/40) | 69,29 µF | 69,29 µF com fs/20 | Mantido 60 µF; texto corrigido |
| p.9 | Gv(s) com L1/Ro | L1/Ro | Lo/Ro | Erro de digitação |
| p.11 | Atenuação em fcv (texto 33,23 dB) | −26,223 dB | −26,225 dB | Texto corrigido |
| p.12 | K | 47 | exato 45,55 | Mantido; MF de 60,5° |
| p.12 | Gv = 10^(\|Av\|/20) | 20,472 | 20,475 | Mantido; vale porque Av < 0 |
| p.13 | R2, R3, C1, C2, C3 | 30,51 kΩ; 217,4 Ω; 5,364 nF; 116,6 pF; 16,02 nF | idem | Mantidos e implementados |
| p.15 | Margem de fase | 60,516° | 60,516° (373 V, 6,298 Ω) | Vale só nesse ponto |
| p.15 | Margem de ganho | infinita | cerca de 22 a 29 dB em 44 a 49 kHz | Corrigido |
| p.16 | Iibmax | 53,571 A | 53,571 A sem rendimento do CC-CC | Limite inferior; 56,4 A com η = 0,95 (H) |
| p.16 | Lb, VC1 (C8), VNp | 39,2 µH; 140 V; 70 V | idem | Mantidos |
| p.17 | a | 1 | 1 | Mantido; topologia identificada |
| p.18 | Compensador do PSIM | 33 kΩ; 5,6 nF; 120 pF; 18 nF; 220 Ω; 10 kΩ | difere dos calculados | Não usado como validação |

## 2. Ondulação do retificador (p.3)

O texto da seção 3.2 afirma que a ondulação é de 10% do pico na tensão mínima, mas escreve a expressão 0,15·(1,4142·176) e adota ΔVC = 37,33 V.

$$\Delta V_C = 0{,}15\cdot\sqrt{2}\cdot 176 = 0{,}15\cdot 248{,}90 = 37{,}33\ \text{V}$$

O número corresponde a 15%. Com 10% a ondulação seria 24,89 V, o vale seria 224,01 V, θC1 cairia para 0,451 rad e o capacitor subiria para 2,73 mF. Como todo o restante da planilha (C1, Ichg, ID1 e o barramento mínimo do inversor) foi calculado com 37,33 V, a decisão foi manter 15% e tratar a frase como erro de texto. Com o banco adotado de 1880 µF, a mesma hipótese de descarga a potência constante dá vale de 213,19 V a 176 V (ondulação de 14,3%). Com a tolerância de −20% do eletrolítico (1504 µF) o vale cai para 204,5 V, abaixo dos 210 V do CC-CC, o que é registrado como sensibilidade relevante para a transferência.

## 3. Barramento mínimo e índice de modulação (p.6 e p.7)

O barramento mínimo aparece com três valores. Na seção 3 ele é Vimin_cc = 211,572 V, isto é, o vale do retificador a 176 V e 2250 W. Na seção 4.1 o inversor usa 223 V, com o rótulo "tensão de entrada eficaz nominal", que não se aplica a uma grandeza CC; o valor não é deduzido em lugar algum e fica entre o vale (211,57 V) e a média (230,24 V). Na seção 5 o CC-CC entrega 210 V.

A interpretação adotada separa os dois modos de operação.

- Modo rede: o barramento oscila entre o vale e o pico. O pior caso para o inversor é o vale, 211,57 V na hipótese da planilha e 213,19 V com 1880 µF.
- Modo bateria: o barramento é imposto pelo CC-CC, 210 V nominais, menos as quedas reais do conversor em malha aberta.

O índice de modulação no pico da tensão de saída é M = Vopk/Vcc.

$$M_{rede} = \frac{162{,}635}{211{,}57} = 0{,}769 \qquad M_{bat} = \frac{162{,}635}{210} = 0{,}774$$

Os dois valores ficam abaixo de 0,85, o limite que a própria planilha adota para uma senoide de boa qualidade, então a escolha de 223 V não compromete o projeto. Ela apenas subestima o índice em cerca de 6%. A margem entre 210 V e 211,57 V é de só 1,57 V, e por isso a coerência entre retificador e CC-CC depende da lógica de transferência, discutida em [06](06-conversor-cc-cc-elevador.md).

## 4. Indutor e capacitor do filtro (p.8)

A expressão de Lo confere numericamente.

$$L_o = \frac{(373 - 162{,}635)\cdot 0{,}5\,(1+0{,}436)}{2\cdot 20\,000\cdot 10{,}33} = 365{,}6\ \mu\text{H}$$

A dedução, porém, usa um intervalo Δt = 0,5(1 + M)/(2fs). Na modulação unipolar, no pico da tensão de saída o braço A fica em nível alto durante (1 + M)/2 do período e o braço B durante (1 − M)/2, de modo que vAB = Vcc dura M·Ts, repartido em dois pulsos de M/(2fs). A ondulação real é, portanto,

$$\Delta I_{Lo} = \frac{(V_{cc} - v_o)\, v_o}{2 f_s L_o V_{cc}} = \frac{(373 - 162{,}6)\cdot 0{,}436}{2\cdot 20\,000\cdot 365{,}6\cdot 10^{-6}} = 6{,}27\ \text{A}$$

ou 24% de Iopk, e não os 40% de projeto. O indutor é conservador e foi mantido. A dedução completa está em [04](04-inversor-e-filtro.md).

Para Co, o texto diz que a frequência de corte do filtro é um décimo da frequência de cruzamento fc = 2fs/4 e escreve em seguida fs/40. A conta usa (20/(2πfs))²/Lo, isto é, um corte em fs/20 = 1 kHz, que é o que resulta de 2fs/4 dividido por 10. A linha com fs/40 é erro de texto; com ela o capacitor seria de 277 µF. O valor calculado (69,29 µF) e o adotado (60 µF) foram mantidos. Com 60 µF a ressonância fica em 1074,6 Hz.

## 5. Potência de 2100 W frente a 3 kVA (p.7 e p.18)

O inversor é dimensionado com carga resistiva de 2100 W (Ioef = 18,26 A), enquanto a especificação é de 3000 VA e o Anexo 01 traz carga não linear. A tabela abaixo compara os esforços; os detalhes ficam em [04](04-inversor-e-filtro.md). A ponte conduz a corrente do indutor, que soma a corrente da carga, a do capacitor Co (2,60 A a 60 Hz) e a ondulação. Em ponte completa unipolar a corrente eficaz de cada interruptor (MOSFET com seu diodo) é ILo/√2, qualquer que seja o índice de modulação, e o pico inclui metade da ondulação de 6,28 A.

| Carga | Io eficaz (A) | Io pico (A) | Fator de crista | Chave eficaz (A) | Chave pico (A) |
|---|---|---|---|---|---|
| Resistiva 2100 W | 18,26 | 25,82 | 1,41 | 13,08 | 29,22 |
| Linear 3 kVA, FP 0,7 indutivo | 26,09 | 36,89 | 1,41 | 17,21 | 37,50 |
| Não linear 3 kVA (FC 3, referência) | 26,09 | 78,26 | 3,00 | 18,57 | 81,40 |

O fator de crista 3 é uma referência usual para cargas com retificador capacitivo e não uma medida; a carga do Anexo 01 é avaliada no PLECS. Os parâmetros dessa carga (0,2 Ω e 9,5 Ω) são próximos dos da carga não linear de referência da IEC 62040-3 para 3 kVA e 115 V (Rs = 0,176 Ω e R1 = 9,94 Ω, que dissipa 66% de S). O capacitor de 1880 µF, porém, é cerca de sete vezes menor que o da referência (R1·C = 7,5/f resulta em 12,6 mF para 5% de ondulação), o que aumenta a ondulação na carga e reduz a potência ativa. Essa observação não altera a carga de ensaio, que é a do professor.

## 6. Malha de tensão (p.9 a p.15)

O passo 4 diz que o sistema apresenta atenuação de 33,23 dB em fcv, mas a própria planilha calcula Av = −26,223 dB e usa esse valor. O recálculo dá −26,225 dB e confirma Gv = 20,47. A expressão Gv = 10^(|Av|/20) é correta neste caso porque a planta atenua em fcv (Av < 0); se a planta tivesse ganho positivo na frequência de cruzamento, o módulo inverteria o sentido do ganho necessário.

O avanço de fase exigido é α = 146,29°. A função α(K) = 4·atan(√K) − 180° dá K = 45,55 para esse avanço; a planilha adota K = 47, que fornece α = 146,80° e eleva a margem de fase para 60,52°. Os componentes do Tipo 3 conferem.

A planta é avaliada em um único ponto, 373 V e 6,298 Ω. Como o ganho da planta é proporcional a Vcc, o laço muda com o barramento, e a carga muda o amortecimento do LC. A análise em [05](05-malha-de-tensao-do-inversor.md) mostra que existe um único cruzamento por 0 dB em todos os pontos verificados, com margem de fase entre 53,6° (210 V, vazio) e 62,9° (373 V, 4,41 Ω) e cruzamento entre 4,1 kHz e 6,7 kHz. A margem de ganho não é infinita: a fase cruza −180° perto de 48 kHz (44 kHz sem a ESR de Co), com margem entre 22 e 29 dB. Esse cruzamento ocorre acima da frequência de ondulação da modulação unipolar (40 kHz), onde o modelo médio deixa de valer, e por isso a margem deve ser lida com cautela. O polo duplo do compensador em 45,7 kHz fica acima de fs e muito perto de 2fs, de modo que quase não atenua a ondulação de 40 kHz realimentada; o ganho do compensador nessa frequência é 69,6 (36,9 dB).

## 7. Componentes do compensador no PSIM (p.18)

Os componentes do circuito PSIM (RF = 33 kΩ, CFV2 = 5,6 nF, C9 = 120 pF, CI = 18 nF, RIP = 220 Ω, RIZ = 10 kΩ) correspondem a R2, C1, C2, C3, R3 e R1 arredondados para valores comerciais. Os zeros vão para 861 Hz e 865 Hz, os polos para 40,2 kHz e 41,1 kHz e o cruzamento a 373 V sobe para 7,85 kHz, com margem de fase de 59,6°. A diferença é pequena, mas a simulação do professor não valida exatamente a função publicada. Os modelos deste trabalho usam os valores calculados. Além disso, o circuito PSIM aplica a referência na entrada não inversora do amplificador, o que acrescenta à saída um termo proporcional a Vref (vc = Vref + Cv·e). Esse termo não altera o laço, mas muda a resposta à referência; os modelos seguem o diagrama de blocos da Figura 4 (vc = Cv·e).

## 8. Conversor CC-CC (p.16 e p.17)

A potência Pob = 2250 W é a de saída do CC-CC, e Iibmax = 53,57 A não inclui o rendimento do próprio conversor. Com η = 0,95 (hipótese H) a bateria fornece 56,4 A a 42 V. A razão cíclica a 56 V não é calculada; com o ganho identificado ela é 0,60, ainda na região de sobreposição (D > 0,5).

A topologia foi identificada pelo texto e pela figura do Anexo 01. É um conversor elevador com célula de comutação de três estados: L1 vem da bateria e entra na derivação central de um autotransformador de dois enrolamentos (os primários), cujas extremidades vão às chaves S1 e S2 e, pelos diodos D17 e D18, ao capacitor inferior C8. Um terceiro enrolamento, de relação a = 1 com cada primário, alimenta a ponte D13 a D16, que carrega C7. C7 fica empilhado sobre C8, e o barramento é a soma das duas tensões.

$$V_{C8} = \frac{V_{ib}}{1-D} = \frac{42}{0{,}3} = 140\ \text{V} \qquad V_{C7} = a\,\frac{V_{C8}}{2} = 70\ \text{V} \qquad V_{ob} = 210\ \text{V}$$

Essa é a topologia de [Araújo et al., 2010], com o enrolamento adicional no autotransformador. A soma 140 V + 70 V = 210 V confirma a hipótese de empilhamento. A dedução completa está em [06](06-conversor-cc-cc-elevador.md).

## 9. Esforços do retificador e impedância de rede (p.5, p.6 e p.18)

Ichg = 55,34 A vem do pulso retangular sem impedância, e ID1pk = 2·Ichg = 110,7 A é uma regra prática para o formato real do pulso. O Anexo 01 inclui 0,1 Ω entre a ponte e o barramento, o que achata o pulso e reduz o pico. A comparação com o PLECS é feita nos ensaios `ret_176_planilha` (condições ideais da seção 3) e `ret_176_anexo` (1880 µF, ESR, 0,1 Ω e diodos com queda).

## 10. Falta de rede e operação do CC-CC no Anexo 01

No circuito PSIM o CC-CC fica permanentemente comandado com D = 0,7. Com a rede presente o barramento é maior que 210 V e o conversor, em malha aberta, não para de transferir energia: ele passa a operar em condução descontínua e a bateria continua fornecendo uma parcela de potência. Um no-break de dupla conversão real mantém a bateria em espera e só habilita o elevador quando a rede falta (ou regula o elevador em malha fechada, o que o faria ficar parado enquanto o barramento estivesse acima da referência). Os ensaios principais deste trabalho usam a lógica de espera com detecção ideal (hipótese H), e um ensaio adicional (`nb_176_nl_anexo`) reproduz o comando permanente do PSIM para quantificar a corrente de bateria com a rede presente.

## 11. Pontos do documento que permanecem em aberto

- As seções 6 e 7 e as referências estão vazias; foram completadas por este trabalho.
- Os dois livros dos slides não foram identificados.
- A planilha não trata partida, pré-carga do barramento, carregador de baterias, chave estática de bypass, proteções nem perdas. Esses temas aparecem como limitações ou como melhorias em [09](09-componentes-e-melhorias.md).

Próximo arquivo: [03. Retificador e barramento](03-retificador-e-barramento.md).
