# 04. Inversor em ponte completa, modulação unipolar e filtro LC

O inversor converte o barramento CC em 115 V eficazes a 60 Hz. Este arquivo refaz as seções 4.1 a 4.5 da planilha, corrige a dedução da ondulação do indutor para a modulação unipolar e calcula os esforços para 2,1 kW, para 3 kVA e para a carga não linear. Os valores estão em `calculos/parametros.json`, chave `inversor`.

## 1. Estrutura e modulação

A ponte tem dois braços. O braço A (QA_sup e QA_inf) alimenta o indutor Lo, e o braço B (QB_sup e QB_inf) é o retorno, ligado ao lado inferior do capacitor Co e da carga. Na modulação unipolar com duas portadoras triangulares de amplitude Vd = 5 V e frequência fs = 20 kHz, defasadas de 180°, cada braço compara o mesmo sinal modulante vc com uma portadora diferente. Uma portadora triangular simétrica atrasada de meio período é igual à primeira com o sinal trocado, de modo que o arranjo equivale a comparar +vc e −vc com uma única portadora.

A consequência é que vAB assume os níveis +Vcc e 0 no semiciclo positivo e −Vcc e 0 no negativo, com frequência aparente de 2fs = 40 kHz. O valor médio de vAB em um período de comutação é linear em vc,

$$\langle v_{AB}\rangle = V_{cc}\,\frac{v_c}{V_d} = V_{cc}\,m$$

o que dá ao modulador o ganho Fm = 1/Vd usado na malha de controle.

## 2. Grandezas de saída

Para carga puramente resistiva de 2100 W,

$$V_{opk} = \sqrt{2}\cdot 115 = 162{,}63\ \text{V} \qquad I_{oef} = \frac{2100}{115} = 18{,}26\ \text{A} \qquad I_{opk} = \sqrt{2}\cdot 18{,}26 = 25{,}82\ \text{A}$$

e o resistor de carga é

$$R_o = \frac{115^2}{2100} = 6{,}298\ \Omega$$

## 3. Índices de modulação

No pico da tensão de saída o índice é m = Vopk/Vcc. A tabela reúne os valores nos barramentos relevantes.

| Barramento | Vcc (V) | m no pico |
|---|---|---|
| Pico na rede máxima | 373,35 | 0,436 |
| Valor da planilha (seção 4.1) | 223 | 0,729 |
| Média na rede mínima | 230,24 | 0,706 |
| Vale na rede mínima | 211,57 | 0,769 |
| Saída do CC-CC | 210 | 0,774 |

Todos ficam abaixo de 0,85, limite adotado na planilha para manter a modulação linear com folga. A folga entre o pico de vAB necessário e o barramento é o que permite ao inversor impor as variações rápidas de corrente pedidas pela carga não linear, assunto da seção 7.

## 4. Indutor de filtro

### 4.1 Ondulação na modulação unipolar

No semiciclo positivo, durante um período de comutação, o braço A fica em nível alto pela fração (1 + m)/2 e o braço B pela fração (1 − m)/2. Como as portadoras estão defasadas, vAB = +Vcc ocorre em dois pulsos de duração m/(2fs) cada. Durante um desses pulsos a tensão no indutor é Vcc − vo, e a ondulação pico a pico é

$$\Delta I_{Lo} = \frac{(V_{cc} - v_o)\,m}{2 f_s L_o} = \frac{(V_{cc} - v_o)\,v_o}{2 f_s L_o V_{cc}}$$

A expressão cresce com vo até vo = Vcc/2. Com Vcc = 373 V, Vcc/2 = 186,5 V é maior que Vopk, e o máximo ocorre no pico da senoide.

$$\Delta I_{Lo,max} = \frac{(373 - 162{,}63)\cdot 162{,}63}{2\cdot 20\,000\cdot 365{,}6\cdot10^{-6}\cdot 373} = 6{,}27\ \text{A}$$

Com barramento baixo (210 V ou 211,57 V), Vcc/2 fica abaixo de Vopk e o máximo ocorre antes do pico, em vo = Vcc/2, com valor Vcc/(8fsLo) = 3,59 A a 210 V.

### 4.2 Dedução da planilha

A planilha usa a tensão Vcc − Vopk e um intervalo Δt = 0,5(1 + m)/(2fs), o que, com ΔILo = 0,4·Iopk = 10,33 A, leva a

$$L_o = \frac{(373 - 162{,}63)\cdot 0{,}5\cdot(1+0{,}436)}{2\cdot 20\,000\cdot 10{,}33} = 365{,}6\ \mu\text{H}$$

O fator 0,5(1 + m) = 0,718 é maior que o fator m = 0,436 da modulação unipolar; ele corresponderia ao tempo em nível alto de um único braço. Por isso o indutor resulta 1,65 vez maior que o necessário para 10,33 A de ondulação, e a ondulação real é 6,27 A, 24% de Iopk. O indutor de 365,6 µH foi mantido, porque é conservador, reduz a ondulação na carga e é o valor do Anexo 01. A Figura `calculos/figuras/ondulacao_Lo.png` mostra ΔILo ao longo do semiciclo para três barramentos, junto com o critério de 10,33 A.

## 5. Capacitor de filtro

A planilha posiciona a frequência de corte do filtro em um décimo da frequência efetiva de cruzamento da modulação unipolar, fc = 2fs/4 = 10 kHz, isto é, em 1 kHz = fs/20.

$$\frac{f_s}{20} = \frac{1}{2\pi\sqrt{L_o C_o}} \quad\Rightarrow\quad C_o = \frac{1}{L_o}\left(\frac{20}{2\pi f_s}\right)^2 = \frac{1}{365{,}6\cdot10^{-6}}\left(\frac{20}{2\pi\cdot 20\,000}\right)^2 = 69{,}29\ \mu\text{F}$$

A linha "fs/40" do texto é erro de digitação, como registrado em [02](02-auditoria-do-documento.md). Adotam-se 60 µF (polipropileno metalizado, 250 Vca), com ESR de 5 mΩ no Anexo 01. A ressonância e a impedância característica ficam

$$f_0 = \frac{1}{2\pi\sqrt{365{,}6\cdot10^{-6}\cdot 60\cdot10^{-6}}} = 1074{,}6\ \text{Hz} \qquad Z_0 = \sqrt{\frac{L_o}{C_o}} = 2{,}468\ \Omega$$

O fator de qualidade em plena carga é Q = Ro/Z0 = 2,55. Em vazio, apenas a ESR amortece o filtro e Q = Z0/ESR ≈ 494, o que torna o laço de tensão responsável por todo o amortecimento nessa condição.

A ondulação de tensão na saída, com a ondulação máxima de corrente e a frequência aparente de 40 kHz, é

$$\Delta V_o \approx \frac{\Delta I_{Lo}}{8\cdot(2f_s)\cdot C_o} = \frac{6{,}27}{8\cdot 40\,000\cdot 60\cdot10^{-6}} = 0{,}33\ \text{V pico a pico}$$

somada a 6,27·0,005 = 0,03 V na ESR, ou cerca de 0,2% de Vopk. A 60 Hz o capacitor absorve uma corrente reativa de 115·2π·60·60·10⁻⁶ = 2,60 A, presente mesmo em vazio.

## 6. Cargas de ensaio

| Carga | Parâmetros | Observação |
|---|---|---|
| Resistiva | Ro = 6,298 Ω | 2100 W em 115 V |
| Linear de 3 kVA | R = 3,086 Ω em série com L = 8,351 mH | 3000 VA com FP 0,7 indutivo, 2100 W |
| Não linear do Anexo 01 | Rs = 0,2 Ω, ponte de diodos, 1880 µF com 0,05 Ω e 9,5 Ω | definida pelo professor |

A carga não linear do Anexo 01 se aproxima da carga não linear de referência da IEC 62040-3 para 3 kVA e 115 V. Nessa referência, Rs produz 4% de queda (0,176 Ω), R1 dissipa 66% da potência aparente com a tensão do capacitor em 1,22·U = 140,3 V (R1 = 9,94 Ω, 1980 W) e o capacitor dá 5% de ondulação, R1·C = 7,5/f, o que resulta em 12,6 mF. Com 9,5 Ω e 140,3 V a carga do professor dissiparia 2072 W, praticamente a potência ativa nominal. O capacitor de 1880 µF, porém, dá constante de tempo de 17,9 ms, frente aos 125 ms da referência; a ondulação na carga fica muito maior que 5%, a tensão média menor e o pulso de corrente mais largo. A potência e o fator de crista efetivos dessa carga são medidos no PLECS.

## 7. Esforços

A ponte conduz a corrente do indutor, iLo = io + iCo. Com fasores de 60 Hz, a corrente de Co (2,60 A, adiantada de 90°) soma-se à da carga. A esse valor soma-se a ondulação de alta frequência, cujo valor eficaz ao longo do semiciclo, a 373,35 V, é obtido integrando ΔILo²/12. Em ponte completa unipolar cada interruptor (MOSFET com o diodo em antiparalelo) conduz iLo em metade do tempo em média, qualquer que seja m, e por isso sua corrente eficaz é ILo/√2. A tensão de bloqueio é o barramento máximo.

| Carga | Io ef (A) | Io pico (A) | ILo ef (A) | ILo pico (A) | Chave ef (A) | Chave pico (A) | Bloqueio (V) |
|---|---|---|---|---|---|---|---|
| Resistiva 2100 W | 18,26 | 25,82 | 18,50 | 29,22 | 13,08 | 29,22 | 373,35 |
| Linear 3 kVA, FP 0,7 | 26,09 | 36,89 | 24,34 | 37,50 | 17,21 | 37,50 | 373,35 |
| Não linear 3 kVA, FC 3 | 26,09 | 78,26 | 26,26 | 81,40 | 18,57 | 81,40 | 373,35 |

Três conclusões saem dessa tabela. Dimensionar com 2100 W resistivos subestima a corrente eficaz dos interruptores em cerca de 30% frente a 3 kVA. A carga indutiva tem pico menor que o esperado porque o capacitor compensa parte da potência reativa. A carga não linear é a que define o pico, cerca de três vezes o da carga resistiva, e é ela que solicita o indutor quanto à saturação. O valor de 81 A usa fator de crista 3, uma referência usual para retificadores capacitivos, e será substituído pelo valor medido.

Há ainda um limite dinâmico. A taxa máxima de crescimento da corrente no indutor, no pico da tensão de saída, é (Vcc − Vopk)/Lo.

$$\left.\frac{di_{Lo}}{dt}\right|_{max} = \frac{210 - 162{,}63}{365{,}6\cdot10^{-6}} = 0{,}13\ \text{A}/\mu\text{s} \quad (\text{barramento de } 210\ \text{V})$$

A 373 V esse limite sobe para 0,58 A/µs. Uma carga com retificador capacitivo pede um pulso de dezenas de ampères em fração de milissegundo justamente perto do pico de vo, onde a folga de tensão é menor. Com barramento baixo a malha tende a saturar o modulador e a tensão de saída tende a achatar no pico. Esse efeito não aparece no modelo médio linear e é verificado no PLECS nos ensaios com carga não linear.

## 8. Verificação no PLECS

O modelo `inversor_malha_fechada` usa um barramento CC ideal e permite isolar o inversor do restante. Os ensaios `inv_373_res`, `inv_2116_res`, `inv_373_vazio`, `inv_2116_vazio`, `inv_2116_nl` e `inv_degrau_2116` verificam a tensão eficaz, o índice de modulação efetivo (pico de vc/Vd), a ondulação ΔILo no pico, a estabilidade em vazio, o efeito da carga não linear com barramento mínimo e a resposta a um degrau de carga. Os resultados estão em [08](08-resultados.md).

Próximo arquivo: [05. Malha de tensão do inversor](05-malha-de-tensao-do-inversor.md).
