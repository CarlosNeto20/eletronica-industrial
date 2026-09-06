# Trabalho 1. Perdas em Semicondutores e Transformador de Alta Frequência

**Disciplina:** Eletrônica Industrial, Unidade I, Dispositivos de Eletrônica de Potência
**Partes:** (1) expressões de perdas em semicondutores de potência; (2) projeto de transformador de
alta frequência com núcleo de ferrite Thornton
**Entregáveis:** memorial de desenvolvimento (esta pasta) e artigo final no formato IEEE A4,
nas versões `.docx` e `.pdf` (pasta `artigo`)

## O que este material é

O enunciado pede duas coisas que, à primeira vista, não se conversam: um levantamento de
expressões de perdas em semicondutores e um projeto de transformador. A escolha feita aqui foi
tratá-las como as duas metades de um mesmo problema, o de saber quanta energia um conversor
desperdiça e onde, e fechar o trabalho com um exemplo em que as duas partes se encontram. O
conversor CC-CC em ponte completa da Parte 2 tem suas perdas de semicondutor calculadas com as
expressões da Parte 1.

Cada documento fecha uma etapa e entrega os números que alimentam a seguinte, de modo que a
leitura na ordem reproduz a sequência real do raciocínio.

## Organização do material

### Parte 1. Expressões de perdas em semicondutores de potência

| Documento | Conteúdo |
|-----------|----------|
| [01. Fundamentos de perdas](01-fundamentos-de-perdas-em-semicondutores.md) | A chave ideal como referência, as três parcelas de perda, por que a perda de condução depende de dois valores de corrente, e a origem física dos modelos de comutação |
| [02. Diodo de potência](02-diodo-de-potencia.md) | Características, polarização, modelo linear por partes, recuperação reversa e dois exemplos numéricos (60 Hz e 50 kHz) |
| [03. Tiristor e TRIAC](03-tiristor-e-triac.md) | SCR e TRIAC: disparo, bloqueio natural, perdas de condução, perda de porta, e por que a frequência é limitada a 1 kHz |
| [04. MOSFET de potência](04-mosfet-de-potencia.md) | Região ôhmica, $R_{DS(on)}$ e sua deriva térmica, capacitâncias parasitas, os seis intervalos de comutação |
| [05. IGBT de potência](05-igbt-de-potencia.md) | Estrutura híbrida, $V_{CE(sat)}$, corrente de cauda, e por que o modelo linear subestima a perda |
| [06. Síntese comparativa e cálculo térmico](06-sintese-comparativa-e-calculo-termico.md) | Tabela unificada das expressões, circuito térmico, dimensionamento de dissipador e a fronteira quantitativa MOSFET × IGBT |

### Parte 2. Transformador de alta frequência com ferrite Thornton

| Documento | Conteúdo |
|-----------|----------|
| [07. Fundamentos de magnéticos em AF](07-fundamentos-de-magneticos-em-alta-frequencia.md) | Lei de Faraday na forma de tensão-segundo, laço B-H, perdas no núcleo, efeito pelicular e a dedução do produto de áreas |
| [08. Especificações e metodologia](08-especificacoes-e-metodologia-do-transformador.md) | Especificações fechadas, hipóteses, escolha de $\Delta B$, $J$ e $K_u$, e o roteiro de cálculo |
| [09. Dimensionamento passo a passo](09-dimensionamento-passo-a-passo.md) | Os quinze passos do projeto, da potência total ao enrolamento executável, com a iteração de núcleo |
| [10. Verificação: perdas e térmica](10-verificacao-perdas-e-termica.md) | Perdas no cobre e no núcleo, elevação de temperatura, ocupação de janela e indutância de magnetização |

### Fechamento

| Documento | Conteúdo |
|-----------|----------|
| [11. Resumo consolidado e referências](11-resumo-consolidado-e-referencias.md) | Aplicação integrada das duas partes, tabelas de resultados e bibliografia |

## Especificações do projeto da Parte 2

| Parâmetro | Símbolo | Valor |
|-----------|---------|-------|
| Topologia | | Conversor CC-CC em ponte completa (*full-bridge*) |
| Tensão de entrada | $V_{in}$ | 400 V |
| Tensão de saída | $V_o$ | 54 V |
| Potência de saída | $P_o$ | 500 W |
| Frequência de comutação | $f_s$ | 100 kHz |
| Razão cíclica nominal por diagonal | $D$ | 0,40 |
| Rendimento admitido do transformador | $\eta$ | 98 % |
| Material do núcleo | | Ferrite Thornton IP12R |

As quatro primeiras linhas reproduzem o exemplo de projeto resolvido na Apostila 01 do professor
(Seção 1.6.5), deliberadamente, para que o resultado obtido aqui, com núcleo Thornton no lugar
do núcleo Magnetics, possa ser confrontado com o material de referência. As demais são definições
de projeto justificadas no documento 08.

## Síntese dos resultados

### Parte 1. Expressões consolidadas

| Dispositivo | Perda de condução | Perda de comutação |
|---|---|---|
| Diodo | $V_{TO}I_{F(av)} + r_T I_{F(rms)}^2$ | $\tfrac{1}{2}Q_{rr}V_R f_s$ (entrada em condução $\approx 0$) |
| Tiristor / TRIAC | $V_{TO}I_{T(av)} + r_T I_{T(rms)}^2$ | desprezível em 60 Hz; limita $f_s < 1$ kHz |
| MOSFET | $R_{DS(on)}(T_j)\,I_{D(rms)}^2$ | $\tfrac{1}{2}V_{DS}I_D(1{,}2\,t_r)f_s + \tfrac{1}{2}V_{DS}I_D(1{,}2\,t_f)f_s$ |
| IGBT | $V_{CE(sat)}I_{C(av)}$ | idem, ou $(E_{on}+E_{off})f_s$ pelo catálogo |

### Parte 2. Projeto fechado

| Grandeza | Valor |
|-----------|-------|
| Núcleo adotado | Thornton **NEE-42/21/20**, material IP12R |
| Produto de áreas requerido / disponível | 2,255 cm⁴ / 3,768 cm⁴ |
| Espiras primário / secundário | 60 / 10 (relação 6:1) |
| Excursão de fluxo em operação / pior caso | 0,114 T / 0,139 T |
| Condutor | 26 AWG, 3 fios em paralelo (primário) e 17 fios (secundário) |
| Ocupação da janela | $K_u = 0{,}357$ (limite 0,40) |
| Perdas no cobre / no núcleo / totais | 1,498 W / 1,015 W / 2,514 W |
| Elevação de temperatura | 35,4 °C (44,1 °C no pior caso) |
| Rendimento do transformador | 99,50 % |

## Sequência de trabalho

```
   Enunciado, slides de aula e capítulo do livro
                     |
   Parte 1: levantamento e dedução das expressões (docs 01 a 05)
                     |
   Exemplos numéricos com componentes reais de catálogo
                     |
   Síntese comparativa e cálculo térmico (doc 06)
                     |
   Parte 2: fundamentos de magnéticos em AF (doc 07)
                     |
   Especificações, metodologia e dimensionamento (docs 08 e 09)
                     |
   Verificação de perdas, janela e temperatura (doc 10)
                     |
   Aplicação integrada: perdas do full-bridge (doc 11)
                     |
              Artigo final no formato IEEE A4
```

## Convenções adotadas

**Notação de correntes.** Ao longo de todo o trabalho, $I_{(av)}$ designa o **valor médio** e
$I_{(rms)}$ o **valor eficaz** da corrente no dispositivo, ambos tomados sobre o período completo de
operação do circuito, e não sobre o intervalo de condução. Essa distinção é a fonte de erro mais
comum no cálculo de perdas e é discutida em detalhe no documento 01.

**Vírgula decimal.** Todos os resultados numéricos usam vírgula decimal, conforme a norma
brasileira. Nas expressões em modo matemático o separador é o ponto, por limitação do formato.

**Temperaturas de referência.** Salvo indicação contrária, os parâmetros de catálogo são tomados
na temperatura de junção quente do dispositivo, ou seja, 125 °C para diodos e tiristores e 100 °C
para MOSFETs, conforme a recomendação dos slides de aula. É nessa condição que o dispositivo opera
em regime, e não a 25 °C.

**Dados de catálogo.** Todos os componentes usados nos exemplos numéricos são comerciais e seus
parâmetros foram extraídos das respectivas folhas de dados, citadas no documento 11. Nenhum valor
foi arbitrado.
