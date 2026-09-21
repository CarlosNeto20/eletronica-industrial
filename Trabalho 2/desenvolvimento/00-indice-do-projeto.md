# Trabalho 2. Conversores CC-CC Isolados e Comparação com os Equivalentes

**Disciplina:** Eletrônica Industrial (UFC, Prof. Dr. René Pastor Torrico-Bascopé)
**Autores:** Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962)
**Enunciado:** `documento explicativo/Trabalho02_Conversores_Isolados_2026b.pdf`, convertido em
[`Trabalho02.md`](../documento%20explicativo/Trabalho02.md)
**Simulador:** PLECS Standalone 5.0 (Plexim), no lugar do PSIM usado pelo professor; modelos
prontos em `simulação PLECS/`
**Entregáveis:** memorial de desenvolvimento (esta pasta), modelos `.plecs`, resultados exportados e
artigo final no formato IEEE A4, nas versões `.docx` e `.pdf` (pasta `artigo`)

## O que este material é

O enunciado pede, para quatro conversores isolados, a mesma sequência: análise qualitativa
(topologia, formas de onda teóricas e etapas de operação), exemplo de projeto e uma simulação que
compara o conversor isolado com o seu equivalente não isolado durante degraus de carga de 20 % para
100 % e de volta. O Forward de uma chave vem inteiramente resolvido e serve de modelo. Os outros
três trazem o projeto numérico pronto, os esquemáticos PSIM e as formas de onda do professor, mas o
texto está marcado como **ESCREVER**.

O fio condutor do trabalho é uma única ideia. Um conversor isolado, visto do secundário, é um
conversor básico (Buck, Boost ou Buck-Boost) com a tensão de entrada, a indutância e às vezes a
frequência e a razão cíclica transformadas pela relação de espiras e pela forma como a ponte ou o
push-pull combinam os semiciclos. Se essa equivalência vale também no regime transitório, então o
modelo médio e as funções de transferência do conversor básico servem para projetar o controle do
conversor isolado. A simulação de degrau de carga é o teste que confirma isso.

## Organização do material

| Documento | Conteúdo | Estado |
|-----------|----------|--------|
| [00. Índice do projeto](00-indice-do-projeto.md) | Este arquivo: visão geral, parâmetros consolidados, convenções | pronto |
| [07. Guia de simulação no PLECS](07-guia-simulacao-plecs.md) | Passo a passo dos oito circuitos (4 isolados + 4 equivalentes), parâmetros, conexões, ensaios e exportação | pronto |
| `../simulação PLECS/*.plecs` | Os quatro modelos prontos (isolado + equivalente, Scope e gravação CSV), gerados por `gerador/gerar_modelos.py` | validados no PLECS 5.0; todas as simulações feitas |
| `calculos/parametros_projeto.py` | Script que confere todas as contas do enunciado e deriva os parâmetros dos equivalentes | pronto |
| [01. Fundamentos de conversores isolados](01-fundamentos-conversores-isolados.md) | Transformador de AF (modelo ideal + $L_m$ + dispersão), relação de espiras, reflexão de impedâncias, desmagnetização, dedução geral dos equivalentes referidos ao secundário | pronto |
| [02. Forward de uma chave](02-forward.md) | Revisão do exemplo resolvido pelo professor, equivalência com o Buck e resultados no PLECS | pronto |
| [03. Ponte completa (*full-bridge*)](03-full-bridge.md) | Introdução, topologia, formas de onda (Fig. 7), 4 etapas de operação, projeto, equivalente Buck (67,5 V, 40 kHz, D = 0,8) | pronto |
| [04. Push-pull alimentado em corrente](04-push-pull-alimentado-em-corrente.md) | Introdução, topologia, formas de onda (Fig. 11), 4 etapas, projeto, equivalente Boost (240 V, 2,88 mH, 40 kHz, D = 0,4) | pronto |
| [05. Flyback de uma chave](05-flyback.md) | Introdução, topologia, formas de onda (Fig. 16), 3 etapas em MCD (e 2 em MCC), projeto, equivalente Buck-Boost, MCD × MCC | pronto |
| [06. Metodologia de validação](06-metodologia-de-validacao.md) | Ensaios, grandezas medidas, critérios quantitativos de equivalência (valor final, pico, tempo de acomodação, erro RMS) | pronto |
| 08. Análise de resultados | Incorporada aos docs 02 a 05 e a `resultados PLECS/metricas_degraus.md` | dispensado |
| [09. Conclusões e referências](09-conclusoes-e-referencias.md) | Conclusões gerais e bibliografia | pronto |
| Artigo | `../artigo/artigo-conversores-isolados-equivalentes.docx` e `.pdf`, gerados por `../artigo/fonte/` | pronto (em revisão) |

O guia do PLECS recebeu o número 07 para manter a mesma posição que o guia do PSIM ocupava no
projeto `controle-main/Modelos de Conversores FT`, que é a base metodológica deste trabalho. Ele foi
escrito primeiro porque é o único documento que depende de uma ferramenta que ainda precisa ser
validada na máquina da equipe.

## Parâmetros consolidados dos quatro projetos

Todos os valores abaixo foram recalculados por `calculos/parametros_projeto.py` e coincidem com o
enunciado (as poucas divergências estão na seção seguinte).

### Especificações e componentes do conversor isolado

| Grandeza | Forward | Full-bridge | Push-pull (corrente) | Flyback |
|---|---|---|---|---|
| Potência de saída $P_o$ | 500 W | 5000 W | 1000 W | 200 W |
| Tensão de entrada $V_i$ | 200 V | 400 V | 54 V | 200 V |
| Tensão de saída $V_o$ | 54 V | 54 V | 400 V | 54 V |
| Frequência de comutação $f_s$ | 20 kHz | 20 kHz | 20 kHz | 20 kHz |
| Razão cíclica $D$ | 0,4 | 0,4 (por diagonal) | 0,7 (por chave, com sobreposição) | 0,4 |
| Ganho estático | $V_o/V_i = nD$ | $V_o/V_i = 2aD$ | $V_o/V_i = a/[2(1-D)]$ | $V_o/V_i = aD/(1-D)$ (MCC) |
| Relação de espiras | $n = N_s/N_p = 0{,}675$ | $a = 0{,}16875$ | $a = 4{,}444$ (secundário / cada meio primário) | $a = 0{,}405$ |
| Espiras usadas na simulação | 100 : 68 : 100 (p : s : t) | 100 : 17 | 22,5 + 22,5 : 100 | 100 : 40,5 |
| Corrente de saída nominal $I_o$ | 9,259 A | 92,593 A | 2,5 A | 3,704 A |
| Ondulação especificada | $\Delta I_{Lo}$ = 1,5 A; $\Delta V_{Co}$ = 0,27 V | $\Delta I_{Lo}$ = 18,52 A; $\Delta V_{Co}$ = 0,27 V | $\Delta I_{Li}$ = 3,7 A; $\Delta V_{Co}$ = 4 V | $\Delta V_{Co}$ = 0,54 V |
| Indutor de filtro | $L_o$ = 1,08 mH | $L_o$ = 14,58 µH | $L_i$ = 145,9 µH (sim.: 146 µH) | (é o próprio $L_m$) |
| Capacitor de saída | $C_o$ = 34,72 µF | $C_o$ = 214,4 µF | $C_o$ = 6,25 µF | $C_o$ = 137,2 µF |
| RSE do capacitor | 0,18 Ω | 0,015 Ω | 0,873 Ω | 0,044 Ω |
| Carga nominal $R_o$ | 5,832 Ω | 0,5832 Ω | 160 Ω | 14,58 Ω |
| Indutância magnetizante | calc. 12,7 mH; sim. 13 mH | calc. 2,546 mH; sim. 2,6 mH | calc. 3,867 mH; sim. 200 mH | MCD 720 µH; MCC 7200 µH |

### Ensaio de degrau de carga

A carga é formada por um resistor fixo que sozinho consome 20 % da potência nominal, $R_{20} = 5R_o$,
em paralelo com um resistor chaveado $R_{80} = 1{,}25R_o$. Com a chave fechada, $R_{20} \parallel
R_{80} = R_o$ (100 %). A chave é comandada por uma onda quadrada de razão cíclica 0,5, que começa
em nível alto, de modo que o primeiro degrau é de 100 % para 20 % e o segundo de 20 % para 100 %.

| Grandeza | Forward | Full-bridge | Push-pull | Flyback |
|---|---|---|---|---|
| $R_{20}$ (fixo) | 29,16 Ω | 2,916 Ω | 800 Ω | 72,9 Ω |
| $R_{80}$ (chaveado) | 7,29 Ω | 0,729 Ω | 200 Ω | 18,225 Ω (PSIM: 18,2 Ω) |
| Frequência do chaveamento de carga | 10 Hz | 5 Hz | 2 Hz | 2 Hz |
| Instante 100 % → 20 % mostrado | 0,05 s | 0,3 s | 1,25 s | 0,75 s |
| Instante 20 % → 100 % mostrado | 0,10 s | 0,2 s | 1,00 s | 0,50 s |

### Conversor equivalente não isolado (referido ao secundário)

| Grandeza | Forward → Buck | Full-bridge → Buck | Push-pull → Boost | Flyback → Buck-Boost |
|---|---|---|---|---|
| Tensão de entrada equivalente | $nV_i$ = 135 V | $aV_i$ = 67,5 V (PSIM: 67,6 V) | $aV_i$ = 240 V | $aV_i$ = 81 V |
| Indutor equivalente | $L_o$ = 1,08 mH | $L_o$ = 14,58 µH | $a^2L_i$ = 2,883 mH (PSIM: 2,88 mH) | $a^2L_m$ = 118,1 µH (MCD) / 1181 µH (MCC) |
| Razão cíclica equivalente | $D$ = 0,4 | $2D$ = 0,8 | $2D-1$ = 0,4 | $D$ = 0,4 |
| Frequência equivalente | $f_s$ = 20 kHz | $2f_s$ = 40 kHz | $2f_s$ = 40 kHz | $f_s$ = 20 kHz |
| Capacitor, RSE e cargas | iguais ao isolado | iguais ao isolado | iguais ao isolado | iguais ao isolado |
| Verificação: $V_o$ do equivalente | 135 × 0,4 = 54 V | 67,5 × 0,8 = 54 V | 240 / 0,6 = 400 V | 81 × 0,4/0,6 = 54 V |

As três regras que geram essa tabela são as mesmas para qualquer conversor isolado e serão
deduzidas no documento 01. A tensão de entrada é refletida pela relação de espiras. Uma indutância
do primário é refletida pelo quadrado da relação de espiras. E, nos conversores que usam os dois
semiciclos do transformador (ponte completa e push-pull), o secundário vê dois pulsos por período,
de modo que o equivalente opera no dobro da frequência, com a razão cíclica efetiva $2D$ (ponte) ou
$2D-1$ (push-pull com sobreposição).

### Resultados esperados (lidos nas figuras do professor)

Servem de gabarito para conferir as simulações no PLECS. Os valores de pico são leituras
aproximadas dos gráficos do PSIM.

| Grandeza | Forward | Full-bridge | Push-pull | Flyback MCD | Flyback MCC |
|---|---|---|---|---|---|
| $V_o$ em regime a 100 % | 54 V | 54 V | 400 V | ≈ 56,9 V | 54 V |
| $V_o$ em regime a 20 % | 54 V | 54 V | 400 V | ≈ 127 V | 54 V |
| $I_o$ a 100 % / 20 % | 9,26 / 1,85 A | 92,6 / 18,5 A | 2,5 / 0,5 A | ≈ 3,9 / 1,75 A | 3,70 / 0,74 A |
| Vale de $V_o$ no degrau 20 → 100 % | ≈ 31 V | ≈ 40 V | ≈ 338 V | sem oscilação (1ª ordem) | ≈ 43 V |
| Pico de $V_o$ no degrau 100 → 20 % | ≈ 90 V | ≈ 71 V | ≈ 465 V | sem oscilação (1ª ordem) | ≈ 67 V |

No Flyback em MCD a tensão de saída em malha aberta depende da carga,
$V_o = V_i D\sqrt{R/(2L_mf_s)}$, o que explica os 127 V a 20 % e os 57 V a 100 %, e a resposta é de
primeira ordem porque o indutor deixa de ser uma variável de estado. Em MCC reaparece o par de polos
LC e a resposta oscila, como nos demais conversores.

## Divergências encontradas no enunciado

Registradas aqui para que o texto final as trate de forma consciente, e não as reproduza.

1. **Full-bridge, corrente magnetizante.** A expressão $I_m = 0{,}02\,(n I_o)$ dá 1,25 A somente
   com $n = 0{,}675$, que é a relação do Forward. Com a relação deste conversor, $a = 0{,}169$,
   resulta $I_m = 0{,}3125$ A e $L_m = 10{,}2$ mH. A simulação do professor usa 2,6 mH, coerente com
   o valor do enunciado. Como $L_m$ quase não afeta a dinâmica de saída, a sugestão é **manter
   2,6 mH na simulação**, para comparar com as figuras do professor, e **comentar no texto** que o
   valor coerente com o critério de 2 % seria 10,2 mH.
2. **Full-bridge, tensão do equivalente.** O enunciado arredonda $a$ para 0,169 e usa 67,6 V;
   o transformador simulado tem 100:17 ($a = 0{,}17$, 68 V). O valor exato é 67,5 V. Usar 67,5 V no
   equivalente e 100:16,875 no transformador, ou manter os valores do professor e justificar.
3. **Push-pull, corrente magnetizante.** O texto diz "entre 2 e 5 %", mas a conta usa 1 %
   ($I_{Lm} = 0{,}01\,I_i$). A simulação usa 200 mH, e o próprio enunciado autoriza um valor maior.
4. **Push-pull, defasagem das chaves.** Os geradores VSQ1 e VSQ2 aparecem apenas com 20 kHz e
   D = 0,7. A defasagem de 180° entre eles não está legível, mas é indispensável (Fig. 11).
5. **Flyback, numeração e legendas.** As subseções 4.3.2 a 4.3.5 estão numeradas como 3.3.x; as
   Figs. 19(a) e 19(b) são o mesmo gráfico (falta o degrau 100 → 20 % em MCD); a legenda da Fig. 21
   diz "MCD", mas o circuito é o de MCC (Fig. 20).
6. **Forward, referências cruzadas.** "Eq. (3)" e "Eq. (46)" não existem no documento. A introdução
   fala em "corrente através do indutor", mas os gráficos mostram a corrente de saída; o trabalho
   deve apresentar as duas.

## Convenções adotadas

**Relação de espiras.** Segue o enunciado: $n$ ou $a$ = $N_s/N_p$, secundário sobre primário, de
modo que $V_s = aV_p$ e $I_p = aI_s$. No push-pull, $N_p$ é o número de espiras de **cada metade**
do primário com derivação central.

**Equivalente referido ao secundário.** Todas as grandezas do equivalente são as do lado da carga.
Isso permite sobrepor diretamente, no mesmo gráfico, tensão e corrente de saída dos dois circuitos,
exatamente como nas figuras do professor.

**Componentes ideais.** Chaves e diodos ideais (queda e resistência nulas), transformador ideal
acrescido apenas da indutância magnetizante. As resistências série dos capacitores são mantidas,
porque fazem parte do projeto. O guia do PLECS explica por que a dispersão do transformador foi
retirada e como reintroduzi-la com segurança.

**Vírgula decimal.** Texto e tabelas usam vírgula decimal. Campos do PLECS e código usam ponto.

## Sequência de trabalho

```
   Enunciado (PDF convertido) e material de aula
                     |
   Conferência numérica dos quatro projetos (calculos/parametros_projeto.py)
                     |
   Guia do PLECS (doc 07) --> montagem dos 8 circuitos --> ensaios --> CSV em "resultados PLECS"
                     |
   Fundamentos de conversores isolados e dedução dos equivalentes (doc 01)
                     |
   Um documento por conversor (docs 02 a 05): texto "ESCREVER" + etapas desenhadas
                     |
   Metodologia e análise de resultados (docs 06 e 08) com os números do PLECS
                     |
   Conclusões e referências (doc 09), estrutura do artigo (doc 10)
                     |
              Artigo final no formato IEEE A4 (.docx e .pdf)
```

O estado corrente e a lista de tarefas pendentes ficam em `../PROXIMOS-PASSOS.md`.
