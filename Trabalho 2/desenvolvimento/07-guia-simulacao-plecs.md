# 07. Guia passo a passo da simulação no PLECS

Este arquivo é um roteiro operacional, escrito para ser seguido com o PLECS aberto ao lado, do
primeiro componente colocado na tela até o arquivo CSV salvo na pasta `resultados PLECS`. Ele
adapta ao PLECS o guia do PSIM do projeto `controle-main/Modelos de Conversores FT` e reproduz, no
PLECS, os circuitos que o professor montou no PSIM (Figs. 4, 8, 13, 18 e 20 do enunciado).

Cada circuito é apresentado pela representação esquemática em texto, pela tabela de conexões, por
uma conferência de contagem de terminais, pelo script de inicialização com todos os parâmetros e,
por fim, pelo resultado esperado. Os valores numéricos vêm de `calculos/parametros_projeto.py` e do
documento 00.

> **Modelos prontos.** A equipe usa o **PLECS Standalone 5.0**. Os quatro circuitos deste guia já
> estão montados em `simulação PLECS/` (`forward.plecs`, `fullbridge.plecs`, `pushpull.plecs` e
> `flyback.plecs`), gerados por `simulação PLECS/gerador/gerar_modelos.py`; o `LEIA-ME.md` daquela
> pasta explica a organização de cada modelo e o que conferir na primeira abertura. Este guia
> continua valendo como explicação de cada circuito, como roteiro para montá-lo à mão e como
> referência dos resultados esperados.
>
> **Diferenças entre os modelos prontos e o texto abaixo.** O bloco de transformador ideal do PLECS
> tem o tipo `Transformer` no arquivo (*Ideal Transformer* na biblioteca). Nos modelos prontos, os
> transformadores de três enrolamentos (Forward com terciário, push-pull com derivação central)
> foram feitos com **dois transformadores de dois enrolamentos** ligados em paralelo pelo lado
> comum, o que é eletricamente equivalente; a inversão de polaridade (terciário do Forward,
> secundário do Flyback) foi feita com **número de espiras negativo**, recurso previsto no manual.
> Na ponte e no push-pull, $L_m$ é o parâmetro *Magnetizing inductance* do próprio bloco, referido
> ao primeiro enrolamento.
>
> **Sobre nomes de menus e campos.** Os nomes dos componentes e dos campos das caixas de diálogo
> são os da biblioteca padrão, mas podem variar levemente entre versões. Se algum não aparecer no
> caminho indicado, digite o nome em inglês no campo de busca do *Library Browser*. No **PLECS
> Blockset** (dentro do Simulink) os circuitos são idênticos; muda apenas onde ficam o *solver* e
> as variáveis, como explicado na seção 2.4.

## 1. Convenções e preparação

### 1.1 O que muda do PSIM para o PLECS

Quem vem do guia do PSIM precisa desaprender quatro hábitos. Eles são a fonte de quase todos os
erros na primeira montagem.

| Assunto | PSIM | PLECS |
|---|---|---|
| Valores numéricos | aceita sufixos: `1080u`, `13m`, `20k` | **não aceita sufixos**; os campos são expressões: `1080e-6`, `13e-3`, `20e3`, ou nomes de variáveis |
| Comando da chave | exige o bloco *On-Off Controller* entre o sinal e o gatilho | o gatilho recebe o sinal de controle **diretamente**: valor diferente de zero liga, zero desliga |
| Gerador de pulsos | fonte quadrada VSQ (amplitude, frequência, razão cíclica, fase em graus) | bloco *Pulse Generator* (níveis alto/baixo, frequência, razão cíclica, **atraso em segundos**) |
| Medidas | sondas de tensão e amperímetros com saída para o SIMVIEW | *Voltmeter* e *Ammeter* geram sinais; o bloco *Probe* lê grandezas internas de qualquer componente sem inserir medidor |
| Transformador | bloco `T_31`/`T2` com resistências, dispersões, $L_m$ e espiras num só diálogo | *Ideal Transformer* + indutor $L_m$ explícito (recomendado neste guia); *Linear Transformer* como alternativa |
| Passo de simulação | passo fixo (`Time Step`) | *solver* de passo variável; os instantes de comutação são localizados exatamente, e limita-se só o passo máximo |
| Visualização | SIMVIEW | bloco *Scope* dentro do próprio modelo |
| Exportação | Arquivo, Salvar como, CSV | bloco *To File* (CSV) ou, na janela do *Scope*, exportação dos dados em CSV |

### 1.2 Arquivos e nomes

Dentro da pasta `simulação PLECS` crie um arquivo por conversor. Em cada arquivo ficam **os dois
circuitos**, o isolado e o equivalente, lado a lado, compartilhando o mesmo gerador de degrau de
carga e o mesmo *Scope*, exatamente como nas figuras do professor. Assim os dois recebem o degrau no
mesmo instante e as curvas saem sobrepostas.

| Arquivo | Circuitos | Figuras do enunciado |
|---|---|---|
| `forward.plecs` | Forward de uma chave + Buck equivalente | Figs. 4 e 5 |
| `fullbridge.plecs` | Ponte completa + Buck equivalente | Figs. 8 e 9 |
| `pushpull.plecs` | Push-pull alimentado em corrente + Boost equivalente | Figs. 13 e 14 |
| `flyback.plecs` | Flyback + Buck-Boost equivalente, MCD ou MCC por uma variável | Figs. 18 a 21 |

### 1.3 Elementos usados e onde encontrá-los

| Elemento | Caminho no *Library Browser* | Uso |
|---|---|---|
| *DC Voltage Source* | Electrical › Sources | fontes de entrada |
| *Resistor*, *Inductor*, *Capacitor* | Electrical › Passive Components | filtros, cargas, RSE, $L_m$ |
| *MOSFET with Diode* | Electrical › Power Semiconductors | chaves principais (o diodo em antiparalelo faz o papel do diodo de corpo do PSIM) |
| *Diode* | Electrical › Power Semiconductors | retificadores, roda livre, desmagnetização |
| *Switch* | Electrical › Switches | chave ideal que conecta a carga extra no degrau |
| *Ideal Transformer* | Electrical › Transformers | transformador de 2 ou 3 enrolamentos |
| *Voltmeter*, *Ammeter* | Electrical › Meters | medidas que vão ao *Scope* |
| *Ground* | Electrical › Connectors (ou Electrical) | referência |
| *Electrical Label* | System | liga dois pontos pelo nome, sem desenhar o fio |
| *Pulse Generator* | Control › Sources | comando das chaves e do degrau de carga |
| *Logical Operator* (NOT) | Control › Logical | sinal complementar no braço da ponte |
| *Goto* / *From* | System | leva um sinal de controle por nome |
| *Signal Multiplexer* | System | junta isolado e equivalente num mesmo gráfico |
| *Probe* | System | lê corrente/tensão interna de componentes |
| *Scope* | System | visualização |
| *To File* | System (ou Control › Sinks, conforme a versão) | grava o CSV durante a simulação |

### 1.4 Convenção de desenho deste guia

Nos esquemas em texto, existe conexão elétrica apenas onde aparece `+` ou `o`. Os nós têm nomes em
minúsculas (`pin`, `d`, `sw`, `vo` ...). Os nós do lado do primário terminam em `_p` quando for
preciso distingui-los; os do conversor equivalente terminam em `_e`. O ponto de polaridade do
transformador é indicado por `(•)` ao lado do terminal.

**Terra nos circuitos isolados.** O enunciado deixa o primário flutuando e aterra só o secundário.
No PLECS é mais seguro colocar um *Ground* também no primário: todos os blocos *Ground* são o mesmo
nó, mas como o transformador ideal não oferece caminho de corrente entre os lados, nenhuma corrente
circula por essa ligação e o isolamento funcional é preservado. Isso elimina qualquer aviso de nó
flutuante.

## 2. Ajustes comuns do simulador

### 2.1 Parâmetros de simulação (Simulation › Simulation Parameters)

| Campo | Valor | Justificativa |
|---|---|---|
| Solver type | Variable-step | o PLECS localiza cada comutação exatamente; não há passo fixo a escolher |
| Solver | DOPRI (non-stiff) | padrão; troque para RADAU (stiff) se aparecer aviso de rigidez (ver seção 11) |
| Max step size | `1e-6` (Forward e Flyback), `5e-7` (Full-bridge e Push-pull) | pelo menos 50 pontos por período da maior frequência presente |
| Initial step size | auto | |
| Relative tolerance | `1e-4` | |
| Absolute tolerance | auto | |
| Refine factor | 1 | |
| Stop time | ver cada circuito | cobre os dois degraus de carga do professor |

### 2.2 Script de inicialização

Todos os valores entram por variáveis. Em **Simulation › Simulation Parameters › Initialization**
(campo *Model initialization commands*) cole o script de cada circuito dado nas seções 4 a 7. Nos
campos dos componentes escreva o **nome da variável** (por exemplo `Lo`), nunca o número. Isso
garante que os dois circuitos usem exatamente os mesmos valores e que um ajuste feito uma vez valha
para os dois.

A sintaxe do script é a do Octave/MATLAB: `nome = valor;`, com `%` para comentários.

### 2.3 Gerador de degrau de carga, comum aos quatro arquivos

Este bloco é idêntico nos quatro modelos. Monte-o uma vez e replique.

```
  Pulse Generator  "PG_carga"  --->  Goto [carga]

  ... em cada circuito (isolado e equivalente):

        vl o----+-----------+
                |           |
               [ ] R20     [ ] R80
                |           |
                |           o x
                |           |
                |         [SW] Switch  <---  From [carga]
                |           |
       gnd  o---+-----------+
```

| Campo do *Pulse Generator* `PG_carga` | Valor |
|---|---|
| High-state output | `1` |
| Low-state output | `0` |
| Frequency | `f_carga` |
| Duty cycle | `0.5` |
| Phase delay | `0` |

O gerador começa em nível alto. A carga extra $R_{80}$ fica conectada na primeira metade do período
(100 %) e desconectada na segunda (20 %), de modo que o primeiro degrau é 100 % → 20 % e o segundo é
20 % → 100 %, reproduzindo os instantes das figuras do professor (tabela da seção 8).

Usar **um único** gerador, distribuído por *Goto*/*From* às duas chaves de carga, garante que o
isolado e o equivalente sofram o degrau no mesmo instante.

### 2.4 Diferenças no PLECS Blockset

No Blockset, cada circuito fica dentro de um bloco PLECS Circuit no Simulink. O *solver* é o do
Simulink (Model Settings › Solver: variable-step, `ode23tb` ou `ode45`, com *Max step size* igual
ao da tabela 2.1), o script de inicialização vai em Model Properties › Callbacks › InitFcn, e o
*Scope* e o *To File* podem ser os do Simulink. Os geradores de pulso podem ser o *Pulse Generator*
do Simulink, lembrando que nele o atraso de fase também é em segundos e o período substitui a
frequência.

## 3. Grandezas medidas e montagem do Scope

O professor compara, para cada conversor, **tensão de saída** e **corrente de saída** do isolado e
do equivalente. Este trabalho mede também a corrente no indutor de armazenamento, citada na
introdução do enunciado.

| Sinal | Como medir | Nome do sinal (Goto) |
|---|---|---|
| Tensão de saída do isolado | *Voltmeter* entre `vo` e `gnd` do secundário | `Vo_iso` |
| Tensão de saída do equivalente | *Voltmeter* entre `vo_e` e `gnd` (ver nota do Flyback, seção 7) | `Vo_eq` |
| Corrente de saída do isolado | *Ammeter* entre `vo` e `vl` (entrada da carga) | `Io_iso` |
| Corrente de saída do equivalente | *Ammeter* entre `vo_e` e `vl_e` | `Io_eq` |
| Corrente no indutor, isolado | *Probe* no indutor ($L_o$, $L_i$ ou $L_m$) | `IL_iso` |
| Corrente no indutor, equivalente | *Probe* no indutor do equivalente | `IL_eq` |

O *Scope* recebe três entradas (Scope Parameters › Number of plots = 3). Cada entrada vem de um
*Signal Multiplexer* de duas vias, com o sinal do isolado na primeira e o do equivalente na
segunda, de modo que as duas curvas fiquem no mesmo gráfico, como no PSIM: vermelho para o
isolado, azul para o equivalente.

| Gráfico | Via 1 (isolado) | Via 2 (equivalente) |
|---|---|---|
| 1 | `Vo_iso` | `Vo_eq` |
| 2 | `Io_iso` | `Io_eq` |
| 3 | `IL_iso` referida ao secundário (ver cada circuito) | `IL_eq` |

Para o *To File*, junte os seis sinais num *Signal Multiplexer* de seis vias, na ordem da tabela
acima, e configure:

| Campo do *To File* | Valor |
|---|---|
| Filename | `../resultados PLECS/<conversor>_degrau.csv` |
| File type | CSV |
| Sample time | `2e-6` (Forward, Flyback) ou `1e-6` (Full-bridge, Push-pull) |

O arquivo sai com uma coluna de tempo seguida das seis colunas, nessa ordem. Se a sua versão não
tiver o *To File*, abra a janela do *Scope* depois da simulação e exporte os dados em CSV pelo menu
File (o item aparece como *Export* ou *Save data*, conforme a versão), com os mesmos nomes.

## 4. Circuito 1, Forward de uma chave e Buck equivalente (`forward.plecs`)

Este é o circuito que o professor já resolveu. Montá-lo primeiro serve para validar o fluxo inteiro
no PLECS contra um resultado conhecido (Fig. 5) antes de partir para os conversores novos.

### 4.1 Script de inicialização

```matlab
% ---- Forward de uma chave: especificações e projeto (enunciado, seção 1.3)
Po = 500;  Vi = 200;  Vo = 54;  fs = 20e3;  D = 0.4;
n  = Vo/(Vi*D);            % 0.675 = Ns/Np
Np = 100;  Ns = 68;  Nt = 100;   % espiras usadas pelo professor (Ns/Np = 0.68)
Lo  = 1080e-6;             % indutor de filtro
Co  = 34.72e-6;  Rse = 0.18;
Lm  = 13e-3;               % indutância magnetizante, referida ao primário
Ro  = Vo^2/Po;             % 5.832
R20 = 5*Ro;  R80 = 1.25*Ro;       % 29.16 e 7.29
f_carga = 10;              % degraus em 0.05 s (100->20 %) e 0.10 s (20->100 %)
% ---- Buck equivalente, referido ao secundário
Vi_eq = n*Vi;              % 135 V
fs_eq = fs;  D_eq = D;
% ---- condições iniciais (regime a 100 %)
IL0 = Po/Vo;  VC0 = Vo;
```

### 4.2 Forward isolado

```
  pin_p o-------+-----------------+---------------------+
                |                 |                     |
               (•) Np      Lm   UUUU                   Nt  (terminal sem ponto)
               UUUU              |                     UUUU
                |                 |                    (•)
                +--------+--------+                     o t
                         o d                            |
                      [MOSFET] S1 <--- PG_S1           _|_  Dt  (catodo em t)
                         |                             /_\
 (+) Vi                  |                              |
  gnd_p o----------------+------------------------------+

  secundário:
      (•) Ns ---o s ----->|----o sw ---UUUU(Lo)---o vo --[A]--o vl --> carga (seção 2.3)
          UUUU      D1         |                  |
           |                  _|_ D2             [ ] Rse
           |                  /_\ (catodo em sw)  |
           |                   |                 === Co
  gnd    o-+-------------------+------------------+----------------- gnd
```

O transformador é um *Ideal Transformer* com três enrolamentos (um de cada lado mais o terciário;
na caixa de diálogo, *Number of windings* `[1 2]` e *Number of turns* `[Np Ns Nt]`). A indutância
magnetizante é um *Inductor* $L_m$ ligado em paralelo com o primário.

A orientação do terciário é o ponto que exige mais atenção. O terminal **sem ponto** do terciário
vai ao positivo da fonte, e o terminal **com ponto** vai ao catodo de $D_t$, cujo anodo está no
negativo da fonte. Com $S_1$ conduzindo, o terminal com ponto do terciário fica em $2V_i$ e $D_t$
bloqueia. Quando $S_1$ abre, a corrente magnetizante força a inversão das tensões, o terminal com
ponto desce a zero, $D_t$ conduz e devolve a energia magnetizante à fonte, enquanto $S_1$ suporta
$2V_i = 400$ V, como na Fig. 2 do enunciado.

#### Tabela de conexões

| Elemento | Terminal | Nó |
|---|---|---|
| Vi (*DC Voltage Source*, `Vi`) | positivo / negativo | `pin_p` / `gnd_p` |
| Transformador, primário | com ponto / sem ponto | `pin_p` / `d` |
| $L_m$ (*Inductor*, `Lm`) | 1 / 2 | `pin_p` / `d` |
| Transformador, terciário | sem ponto / com ponto | `pin_p` / `t` |
| $D_t$ (*Diode*) | anodo / catodo | `gnd_p` / `t` |
| $S_1$ (*MOSFET with Diode*) | dreno / fonte / gatilho | `d` / `gnd_p` / `PG_S1` |
| Transformador, secundário | com ponto / sem ponto | `s` / `gnd` |
| $D_1$ | anodo / catodo | `s` / `sw` |
| $D_2$ | anodo / catodo | `gnd` / `sw` |
| $L_o$ (`Lo`, corrente inicial `IL0`) | 1 / 2 | `sw` / `vo` |
| $R_{se}$ (`Rse`) | 1 / 2 | `vo` / `c` |
| $C_o$ (`Co`, tensão inicial `VC0`) | positivo / negativo | `c` / `gnd` |
| Ammeter `Io_iso` | + / − | `vo` / `vl` |
| $R_{20}$, $R_{80}$ + *Switch* | seção 2.3 | `vl` / `gnd` |
| Voltmeter `Vo_iso` | + / − | `vo` / `gnd` |
| *Ground* | — | `gnd_p` e `gnd` |

#### Conferência por contagem de terminais

| Nó | Terminais que deve reunir | Total |
|---|---|---|
| `pin_p` | Vi+, primário (ponto), $L_m$, terciário (sem ponto) | 4 |
| `d` | primário (sem ponto), $L_m$, dreno de $S_1$ | 3 |
| `t` | terciário (ponto), catodo de $D_t$ | 2 |
| `gnd_p` | Vi−, anodo de $D_t$, fonte de $S_1$, *Ground* | 4 |
| `s` | secundário (ponto), anodo de $D_1$ | 2 |
| `sw` | catodo de $D_1$, catodo de $D_2$, $L_o$ | 3 |
| `vo` | $L_o$, $R_{se}$, Ammeter +, Voltmeter + | 4 |

#### Comando da chave

| Campo do *Pulse Generator* `PG_S1` | Valor |
|---|---|
| High-state output / Low-state output | `1` / `0` |
| Frequency | `fs` |
| Duty cycle | `D` |
| Phase delay | `0` |

Com o transformador desmagnetizado por um terciário de mesmo número de espiras do primário, a razão
cíclica não pode passar de 0,5. Com D = 0,4 sobra folga de 0,1·T para a desmagnetização completa,
que é o intervalo "Transf. Desmagnetizado" da Fig. 2.

### 4.3 Buck equivalente

```
  pin_e o---[MOSFET] S1e---o sw_e ---UUUU(Lo)---o vo_e --[A]--o vl_e --> carga
   (+)        ^ PG_S1e      |                   |
   Vi_eq                   _|_ D2e             [ ] Rse
   |                       /_\                  |
   |                        |                  === Co
  gnd o---------------------+-------------------+----------------- gnd
```

| Elemento | Terminal | Nó | Valor |
|---|---|---|---|
| Vi_eq | + / − | `pin_e` / `gnd` | `Vi_eq` (135 V) |
| $S_{1e}$ (*MOSFET with Diode*) | dreno / fonte / gatilho | `pin_e` / `sw_e` / `PG_S1e` | — |
| $D_{2e}$ | anodo / catodo | `gnd` / `sw_e` | — |
| $L_{oe}$ | 1 / 2 | `sw_e` / `vo_e` | `Lo`, inicial `IL0` |
| $R_{se}$ + $C_o$ | série | `vo_e` → `gnd` | `Rse`, `Co`, inicial `VC0` |
| Ammeter `Io_eq`, Voltmeter `Vo_eq`, cargas | como no isolado | `vo_e`, `vl_e`, `gnd` | `R20`, `R80` |

O gerador `PG_S1e` tem `Frequency = fs_eq`, `Duty cycle = D_eq`, atraso `0`. No PLECS a chave do
lado alto não precisa de fonte flutuante de gatilho, porque o comando é um sinal ideal.

### 4.4 Simulação e resultado esperado

| Parâmetro | Valor |
|---|---|
| Stop time | `0.11` |
| Max step size | `1e-6` |
| Janelas de observação (como na Fig. 5) | 0,0475 a 0,061 s (100 → 20 %) e 0,0975 a 0,105 s (20 → 100 %) |

| Grandeza | Previsto | Simulado isolado | Simulado equivalente |
|---|---|---|---|
| $V_o$ médio, 100 % e 20 % | 54,0 V | | |
| $I_o$ médio, 100 % / 20 % | 9,26 A / 1,85 A | | |
| Ondulação de $i_{Lo}$ | 1,5 A | | |
| Pico de $i_{Lm}$ | $V_iDT/L_m$ = 0,31 A | | — |
| Tensão máxima em $S_1$ | $2V_i$ = 400 V | | — |
| Vale de $V_o$ no degrau 20 → 100 % | ≈ 31 V (Fig. 5a) | | |
| Pico de $V_o$ no degrau 100 → 20 % | ≈ 90 V (Fig. 5b) | | |

Se $V_o$ médio não bater com 54 V em regime, pare e corrija antes de seguir: quase sempre é a
polaridade de algum enrolamento (ver seção 11). Para o gráfico 3 do *Scope*, a corrente $i_{Lo}$ já
está no secundário e é comparada diretamente com a do equivalente.

## 5. Circuito 2, Ponte completa e Buck equivalente (`fullbridge.plecs`)

### 5.1 Script de inicialização

```matlab
% ---- Ponte completa: especificações e projeto (enunciado, seção 2.3)
Po = 5000;  Vi = 400;  Vo = 54;  fs = 20e3;  D = 0.4;
a  = Vo/(Vi*2*D);          % 0.16875 = Ns/Np
Np = 100;  Ns = Np*a;      % 16.875 (o professor usou 17)
Lo  = 14.58e-6;
Co  = 214.4e-6;  Rc = 0.015;
Lm  = 2.6e-3;              % valor do enunciado (ver divergência 1 do doc 00)
Ro  = Vo^2/Po;             % 0.5832
R20 = 5*Ro;  R80 = 1.25*Ro;       % 2.916 e 0.729
f_carga = 5;               % degraus em 0.1/0.3 s (100->20 %) e 0.2 s (20->100 %)
Rbal = 100e3;              % resistores de equilíbrio (só na variante A, seção 5.3)
% ---- Buck equivalente
Vi_eq = a*Vi;              % 67.5 V (o professor usou 67.6)
fs_eq = 2*fs;  D_eq = 2*D; % 40 kHz, 0.8
% ---- condições iniciais (regime a 100 %)
IL0 = Po/Vo;  VC0 = Vo;
```

### 5.2 Ponte completa isolada

Os nomes das chaves seguem a Fig. 6 do enunciado: $S_1$ e $S_4$ no braço esquerdo (superior e
inferior), $S_3$ e $S_2$ no braço direito (superior e inferior). A diagonal $S_1$–$S_2$ aplica
$+V_i$ ao primário; a diagonal $S_3$–$S_4$ aplica $-V_i$.

```
  pin_p o-----+-------------------+
              |                   |
          S1 [M]              S3 [M]
              |                   |
            a o---(•)UUUU----+----o b          secundário:   (•)UUUU
              |    primário  |    |                           |    |
              +----UUUU(Lm)--+    |                         p o    o q
              |                   |
          S4 [M]              S2 [M]           p --+-- D1 -->|-- r --UUUU(Lo)-- vo --[A]-- vl --> carga
              |                   |                +-- D4 --|<-- gnd (anodo em gnd)
  gnd_p o-----+-------------------+            q --+-- D3 -->|-- r
   (Vi entre pin_p e gnd_p)                        +-- D2 --|<-- gnd (anodo em gnd)
                                                vo --[Rc]--[Co]-- gnd
```

#### Tabela de conexões

| Elemento | Terminal | Nó |
|---|---|---|
| Vi (`Vi`) | + / − | `pin_p` / `gnd_p` |
| $S_1$ | dreno / fonte | `pin_p` / `a` |
| $S_4$ | dreno / fonte | `a` / `gnd_p` |
| $S_3$ | dreno / fonte | `pin_p` / `b` |
| $S_2$ | dreno / fonte | `b` / `gnd_p` |
| Transformador (*Ideal Transformer*, `[1 1]`, espiras `[Np Ns]`), primário | ponto / sem ponto | `a` / `b` |
| $L_m$ (`Lm`) | 1 / 2 | `a` / `b` |
| Transformador, secundário | ponto / sem ponto | `p` / `q` |
| $D_1$ | anodo / catodo | `p` / `r` |
| $D_4$ | anodo / catodo | `gnd` / `p` |
| $D_3$ | anodo / catodo | `q` / `r` |
| $D_2$ | anodo / catodo | `gnd` / `q` |
| $L_o$ (`Lo`, inicial `IL0`) | 1 / 2 | `r` / `vo` |
| $R_c$ + $C_o$ (`Rc`, `Co`, inicial `VC0`) | série | `vo` → `gnd` |
| Ammeter `Io_iso`, Voltmeter `Vo_iso`, cargas | seção 3 e 2.3 | `vo`, `vl`, `gnd` |

#### Conferência por contagem de terminais

| Nó | Terminais | Total |
|---|---|---|
| `pin_p` | Vi+, dreno $S_1$, dreno $S_3$ | 3 |
| `a` | fonte $S_1$, dreno $S_4$, primário (ponto), $L_m$ | 4 |
| `b` | fonte $S_3$, dreno $S_2$, primário (sem ponto), $L_m$ | 4 |
| `gnd_p` | Vi−, fonte $S_4$, fonte $S_2$, *Ground* | 4 |
| `p` | secundário (ponto), anodo $D_1$, catodo $D_4$ | 3 |
| `q` | secundário (sem ponto), anodo $D_3$, catodo $D_2$ | 3 |
| `r` | catodo $D_1$, catodo $D_3$, $L_o$ | 3 |

### 5.3 Comando das chaves, duas variantes

Existem duas formas de comandar a ponte, e elas servem a propósitos diferentes.

**Variante B, a do professor (Fig. 8), para o ensaio de degrau de carga.** Cada braço é comandado
de forma complementar. O braço esquerdo recebe um pulso de razão cíclica $D$; o direito, o mesmo
pulso atrasado de meio período. As chaves inferiores recebem o complemento lógico (*Logical
Operator* NOT).

| Chave | Sinal de gatilho |
|---|---|
| $S_1$ | `PG_A`: Frequency `fs`, Duty `D`, Phase delay `0` |
| $S_4$ | NOT(`PG_A`) |
| $S_3$ | `PG_B`: Frequency `fs`, Duty `D`, Phase delay `1/(2*fs)` |
| $S_2$ | NOT(`PG_B`) |

De $0$ a $DT$ conduzem $S_1$ e $S_2$ e o primário recebe $+V_i$. De $T/2$ a $T/2+DT$ conduzem $S_3$
e $S_4$ e o primário recebe $-V_i$. Nos intervalos restantes conduzem $S_4$ e $S_2$, o primário fica
em curto por baixo, a tensão do transformador é nula e a corrente magnetizante circula pelas
chaves inferiores. Não há nó flutuante em nenhum instante, o que torna esta variante a mais robusta
para as simulações longas do degrau.

**Variante A, a da teoria (Fig. 7), para conferir as formas de onda teóricas.** As diagonais são
comandadas juntas e, na roda livre, as quatro chaves ficam abertas.

| Chave | Sinal de gatilho |
|---|---|
| $S_1$ e $S_2$ | `PG_A` (Duty `D`, atraso `0`) |
| $S_3$ e $S_4$ | `PG_B` (Duty `D`, atraso `1/(2*fs)`) |

Nesta variante, na roda livre os pontos `a` e `b` ficam presos apenas por chaves abertas. Coloque
um resistor `Rbal` (100 kΩ) em paralelo com cada uma das quatro chaves: eles fixam os pontos médios
em $V_i/2$, exatamente o patamar $V_i/2$ que a Fig. 7 mostra em $v_{S1}$, e dissipam no máximo
3,2 W no total, desprezível diante de 5 kW.

Para as duas variantes, o resultado na saída é o mesmo, porque o secundário enxerga a mesma
sequência $+V_i$, $0$, $-V_i$, $0$ refletida pela relação de espiras.

### 5.4 Buck equivalente

Idêntico ao da seção 4.3, com `Vi_eq` = 67,5 V, `Lo`, `Co`, `Rc`, gerador `PG_S1e` com
`Frequency = fs_eq` (40 kHz) e `Duty cycle = D_eq` (0,8), e as mesmas cargas.

O retificador de onda completa entrega ao filtro dois pulsos de amplitude $aV_i$ por período de
comutação, cada um com duração $DT$. Um Buck que comuta no dobro da frequência com razão cíclica
$2D$ produz exatamente a mesma forma de onda na entrada do filtro, e por isso é o equivalente.

### 5.5 Simulação e resultado esperado

| Parâmetro | Valor |
|---|---|
| Stop time | `0.31` |
| Max step size | `5e-7` |
| Janelas (como na Fig. 9) | 0,1995 a 0,2025 s (20 → 100 %) e 0,2995 a 0,305 s (100 → 20 %) |

| Grandeza | Previsto | Simulado isolado | Simulado equivalente |
|---|---|---|---|
| $V_o$ médio | 54,0 V | | |
| $I_o$ médio, 100 % / 20 % | 92,6 A / 18,5 A | | |
| Ondulação de $i_{Lo}$ (a 40 kHz) | 18,5 A | | |
| $i_{Lm}$ de pico | $V_iDT/(2L_m)$ = ±1,54 A | | — |
| Vale de $V_o$ no degrau 20 → 100 % | ≈ 40 V (Fig. 9a) | | |
| Pico de $V_o$ no degrau 100 → 20 % | ≈ 71 V (Fig. 9b) | | |

## 6. Circuito 3, Push-pull alimentado em corrente e Boost equivalente (`pushpull.plecs`)

### 6.1 Script de inicialização

```matlab
% ---- Push-pull alimentado em corrente (enunciado, seção 3.3)
Po = 1000;  Vi = 54;  Vo = 400;  fs = 20e3;  D = 0.7;
a  = Vo/Vi*2*(1-D);        % 4.444 = Ns/Np (Np = cada metade do primário)
Np = 22.5;  Ns = 100;
Li  = 146e-6;              % indutor de entrada (calculado 145.9e-6)
Co  = 6.25e-6;  Rc = 0.873;
Lm  = 200e-3;              % referida ao secundário (100 espiras), como no PSIM
Ro  = Vo^2/Po;             % 160
R20 = 5*Ro;  R80 = 1.25*Ro;       % 800 e 200
f_carga = 2;               % degraus em 0.75/1.25 s (100->20 %) e 1.0 s (20->100 %)
% ---- Boost equivalente
Vi_eq = a*Vi;              % 240 V
L_eq  = a^2*Li;            % 2.883e-3 (o professor usou 2.88e-3)
fs_eq = 2*fs;  D_eq = 2*D-1;      % 40 kHz, 0.4
% ---- condições iniciais (regime a 100 %)
ILi0 = Po/Vi;  IL_eq0 = ILi0/a;  VC0 = Vo;
```

### 6.2 Push-pull isolado

```
                 (•) N_p1              S2 [M] dreno em x1, fonte em gnd_p
      x1 o-------UUUU------+
                           o ct  <---UUUU(Li)---- pin_p (+) Vi
      x2 o-------UUUU------+
                 N_p2 (•) no lado de ct         S1 [M] dreno em x2, fonte em gnd_p

  secundário (100 espiras): (•) p , q  -> ponte D1..D4 -> r (+) / gnd (-)
         r --+--[Rc]--[Co]-- gnd      r --[A]-- vl --> carga
         Lm em paralelo com o secundário (p–q)
```

O transformador é um *Ideal Transformer* com três enrolamentos: dois à esquerda (as duas metades do
primário, 22,5 espiras cada) e um à direita (secundário, 100 espiras); *Number of windings* `[2 1]`,
*Number of turns* `[Np Np Ns]`. As duas metades estão em série aditiva: a metade superior tem o
ponto no terminal externo `x1`, e a metade inferior tem o ponto no terminal da derivação central
`ct`, como na Fig. 10.

#### Tabela de conexões

| Elemento | Terminal | Nó |
|---|---|---|
| Vi (`Vi`) | + / − | `pin_p` / `gnd_p` |
| $L_i$ (`Li`, inicial `ILi0`) | 1 / 2 | `pin_p` / `ct` |
| Metade superior do primário | ponto / sem ponto | `x1` / `ct` |
| Metade inferior do primário | ponto / sem ponto | `ct` / `x2` |
| $S_2$ | dreno / fonte / gatilho | `x1` / `gnd_p` / `PG_S2` |
| $S_1$ | dreno / fonte / gatilho | `x2` / `gnd_p` / `PG_S1` |
| Secundário | ponto / sem ponto | `p` / `q` |
| $L_m$ (`Lm`) | 1 / 2 | `p` / `q` |
| $D_1$, $D_3$ | anodo / catodo | `p`, `q` / `r` |
| $D_4$, $D_2$ | anodo / catodo | `gnd` / `p`, `q` |
| $R_c$ + $C_o$ (inicial `VC0`) | série | `r` → `gnd` |
| Ammeter `Io_iso`, Voltmeter `Vo_iso`, cargas | seções 3 e 2.3 | `r`, `vl`, `gnd` |

#### Conferência por contagem de terminais

| Nó | Terminais | Total |
|---|---|---|
| `ct` | $L_i$, primário superior (sem ponto), primário inferior (ponto) | 3 |
| `x1` | primário superior (ponto), dreno $S_2$ | 2 |
| `x2` | primário inferior (sem ponto), dreno $S_1$ | 2 |
| `gnd_p` | Vi−, fontes de $S_1$ e $S_2$, *Ground* | 4 |
| `r` | catodos de $D_1$ e $D_3$, $R_c$, Ammeter +, Voltmeter + | 5 |

#### Comando das chaves

| Chave | *Pulse Generator* |
|---|---|
| $S_1$ | `PG_S1`: Frequency `fs`, Duty `D` (0,7), Phase delay `0` |
| $S_2$ | `PG_S2`: Frequency `fs`, Duty `D` (0,7), Phase delay `1/(2*fs)` |

Com $D > 0{,}5$ e defasagem de meio período, sempre há ao menos uma chave conduzindo. Nos
intervalos em que as duas conduzem, o primário fica em curto (as duas metades se cancelam), a
tensão do transformador é nula e $L_i$ armazena energia com $V_i$ aplicada. Quando só uma conduz, a
energia de $L_i$ e da fonte passa ao secundário. **Nunca** deixe as duas chaves abertas ao mesmo
tempo: isso interromperia a corrente de $L_i$, o que no circuito real destrói as chaves e no PLECS
gera um erro de descontinuidade. A verificação do comando (seção 9.1) é obrigatória antes da
primeira simulação deste circuito.

### 6.3 Boost equivalente

```
  pin_e o---UUUU(L_eq)---o sw_e ---->|---o vo_e --[A]--o vl_e --> carga
   (+)                    |      D_e      |
   Vi_eq              S_e [M] <--- PG_Se [ ] Rc
   |                      |               === Co
  gnd o-------------------+---------------+------------------ gnd
```

| Elemento | Terminal | Nó | Valor |
|---|---|---|---|
| Vi_eq | + / − | `pin_e` / `gnd` | `Vi_eq` (240 V) |
| $L_{eq}$ | 1 / 2 | `pin_e` / `sw_e` | `L_eq`, inicial `IL_eq0` |
| $S_e$ | dreno / fonte / gatilho | `sw_e` / `gnd` / `PG_Se` | `fs_eq`, `D_eq` (40 kHz; 0,4) |
| $D_e$ | anodo / catodo | `sw_e` / `vo_e` | — |
| $R_c$ + $C_o$ | série | `vo_e` → `gnd` | `Rc`, `Co`, inicial `VC0` |

O intervalo de sobreposição do push-pull, que ocorre duas vezes por período e dura
$(2D-1)T/2$ cada vez, é o intervalo de "chave fechada" do Boost; daí a frequência dobrada e a razão
cíclica $2D-1 = 0{,}4$. O indutor $L_i$ refletido ao secundário vale $a^2L_i$.

Para o gráfico 3 do *Scope*, a corrente $i_{Li}$ do isolado deve ser dividida por $a$ (bloco *Gain*
com `1/a`) antes de entrar no *Multiplexer*, para ficar referida ao secundário e comparável com a
do equivalente.

### 6.4 Simulação e resultado esperado

| Parâmetro | Valor |
|---|---|
| Stop time | `1.3` |
| Max step size | `5e-7` |
| Janelas (como na Fig. 14) | 0,991 a 1,02 s (20 → 100 %) e 1,231 a 1,281 s (100 → 20 %) |

Com as condições iniciais do script o regime é atingido muito antes de 1 s. Se quiser uma
simulação mais curta, use `f_carga = 10` (degraus em 0,05 e 0,10 s) e `Stop time = 0.12`; o tempo de
acomodação deste circuito é da ordem de 8 ms, então cabe folgadamente.

| Grandeza | Previsto | Simulado isolado | Simulado equivalente |
|---|---|---|---|
| $V_o$ médio | 400 V | | |
| $I_o$ médio, 100 % / 20 % | 2,5 A / 0,5 A | | |
| $I_{Li}$ médio a 100 % (primário) | 18,52 A | | 4,167 A (= 18,52/a) |
| Ondulação de $i_{Li}$ (primário) | 3,7 A | | 0,833 A (secundário) |
| Tensão máxima nas chaves | $2V_o/a$ = 180 V | | — |
| Vale de $V_o$ no degrau 20 → 100 % | ≈ 338 V (Fig. 14a) | | |
| Pico de $V_o$ no degrau 100 → 20 % | ≈ 465 V (Fig. 14b) | | |

## 7. Circuito 4, Flyback e Buck-Boost equivalente (`flyback.plecs`)

### 7.1 Script de inicialização

```matlab
% ---- Flyback de uma chave (enunciado, seção 4.3)
Po = 200;  Vi = 200;  Vo = 54;  fs = 20e3;  D = 0.4;
a  = Vo/Vi*(1-D)/D;        % 0.405 = Ns/Np
Np = 100;  Ns = 40.5;
Lcrit = Vi^2*D^2/(2*fs*Po);       % 800e-6, fronteira MCD/MCC
kL = 1;                    % 1 -> MCD (Lm = 720 uH); 10 -> MCC (Lm = 7200 uH)
Lm  = 0.9*Lcrit*kL;        % referida ao primário
Co  = 137.2e-6;  Rse = 0.044;
Ro  = Vo^2/Po;             % 14.58
R20 = 5*Ro;  R80 = 1.25*Ro;       % 72.9 e 18.225
f_carga = 2;               % degraus em 0.75 s (100->20 %) e 0.5 s (20->100 %)
% ---- Buck-Boost equivalente
Vi_eq = a*Vi;              % 81 V
L_eq  = a^2*Lm;            % 118.1e-6 (MCD) ou 1.181e-3 (MCC)
fs_eq = fs;  D_eq = D;
% ---- condições iniciais
VC0 = Vo;
ILm0   = (kL>1) * a*(Po/Vo)/(1-D);   % MCC: 2.5 A no primário; MCD: 0
IL_eq0 = ILm0/a;                     % MCC: 6.17 A no secundário
```

Rode o arquivo duas vezes, com `kL = 1` (MCD, Figs. 18 e 19) e com `kL = 10` (MCC, Figs. 20 e
21), salvando cada resultado com um nome próprio (seção 10).

### 7.2 Flyback isolado

```
  pin_p o-----(•)UUUU-----+          secundário:   q o---UUUU(•)---o gnd   (ponto no lado do terra)
               primário   |                        |
         +----UUUU(Lm)----+                        +---->|----o vo --[A]-- vl --> carga
         |                o d                          D1     |
                       S1 [M] <--- PG_S1                     [ ] Rse
                          |                                  === Co
  gnd_p o-----------------+                          gnd o----+
```

O ponto de polaridade do secundário fica no terminal **ligado ao terra**, o oposto do Forward. É
essa inversão que faz o Flyback armazenar energia em $L_m$ com a chave fechada ($D_1$ bloqueado) e
entregá-la à carga com a chave aberta.

| Elemento | Terminal | Nó |
|---|---|---|
| Vi (`Vi`) | + / − | `pin_p` / `gnd_p` |
| Transformador (`[1 1]`, espiras `[Np Ns]`), primário | ponto / sem ponto | `pin_p` / `d` |
| $L_m$ (`Lm`, inicial `ILm0`) | 1 / 2 | `pin_p` / `d` |
| $S_1$ | dreno / fonte / gatilho | `d` / `gnd_p` / `PG_S1` |
| Secundário | ponto / sem ponto | `gnd` / `q` |
| $D_1$ | anodo / catodo | `q` / `vo` |
| $R_{se}$ + $C_o$ (inicial `VC0`) | série | `vo` → `gnd` |
| Ammeter `Io_iso`, Voltmeter `Vo_iso`, cargas | seções 3 e 2.3 | `vo`, `vl`, `gnd` |

`PG_S1`: Frequency `fs`, Duty `D`, atraso `0`.

O professor incluiu no primário um grampeador RCD ($D_2$, $C_2$ = 100 nF, $R_3$ = 10 kΩ) porque
modelou a dispersão do transformador (0,1 µH). Com o transformador ideal deste guia não há energia
de dispersão a grampear, e o grampeador **deve ser omitido**: se for mantido, ele passa a conduzir
parte da corrente magnetizante a cada ciclo para repor os ≈ 1,8 W dissipados em $R_3$
($V_{grampo} \approx V_o/a = 133$ V), o que desvia o isolado do equivalente sem nenhum motivo
físico. A seção 12 mostra como reintroduzir a dispersão junto com o grampeador.

### 7.3 Buck-Boost equivalente

```
  pin_e o---[M] S_e---o sw_e ---|<----o vn_e      (D_e: catodo em sw_e, anodo em vn_e)
   (+)        ^PG_Se   |       D_e     |
   Vi_eq              UUUU L_eq       [ ] Rse
   |                   |              === Co
  gnd o----------------+---------------+------ gnd         carga entre gnd (+) e vn_e (−)
```

O Buck-Boost clássico entrega tensão **negativa** em relação ao terra. O professor contornou isso
colocando o terra no nó superior da saída (Figs. 18b e 20b). No PLECS basta medir ao contrário:

| Elemento | Terminal | Nó | Valor |
|---|---|---|---|
| Vi_eq | + / − | `pin_e` / `gnd` | `Vi_eq` (81 V) |
| $S_e$ | dreno / fonte / gatilho | `pin_e` / `sw_e` / `PG_Se` | `fs_eq`, `D_eq` |
| $L_{eq}$ | 1 / 2 | `sw_e` / `gnd` | `L_eq`, inicial `IL_eq0` (sentido `sw_e` → `gnd`) |
| $D_e$ | anodo / catodo | `vn_e` / `sw_e` | — |
| $R_{se}$ + $C_o$ | série | `gnd` → `vn_e` (positivo do capacitor em `gnd`) | `Rse`, `Co`, inicial `VC0` |
| Voltmeter `Vo_eq` | + / − | `gnd` / `vn_e` | lê +54 V |
| Ammeter `Io_eq` | + / − | `gnd` / `vl_e` | corrente positiva entrando na carga |
| Cargas | seção 2.3 | entre `vl_e` e `vn_e` | `R20`, `R80` |

### 7.4 Simulação e resultado esperado

| Parâmetro | Valor |
|---|---|
| Stop time | `0.8` |
| Max step size | `1e-6` |
| Janelas MCD (Fig. 19) | 0,477 a 0,541 s (20 → 100 %) e 0,727 a 0,791 s (100 → 20 %) |
| Janelas MCC (Fig. 21) | 0,488 a 0,536 s (20 → 100 %) e 0,74 a 0,813 s (100 → 20 %) |

| Grandeza | MCD previsto | MCC previsto | Isolado | Equivalente |
|---|---|---|---|---|
| $V_o$ a 100 % | $V_iD\sqrt{R_o/(2L_mf_s)}$ ≈ 56,9 V | 54,0 V | | |
| $V_o$ a 20 % | ≈ 127 V | 54,0 V | | |
| $I_o$, 100 % / 20 % | ≈ 3,90 / 1,75 A | 3,70 / 0,74 A | | |
| Pico de $i_{Lm}$ (primário) | $V_iDT/L_m$ = 5,56 A | ≈ 2,78 A | | |
| Pico da corrente no secundário | 13,7 A | ≈ 6,9 A | | |
| Tensão máxima em $S_1$ | $V_i + V_o/a$ ≈ 333 V (a 100 %) | 333 V | | — |
| Forma do transitório | exponencial, sem oscilação | oscilatório, vale ≈ 43 V e pico ≈ 67 V | | |

Em MCD a tensão de saída depende da carga porque, em malha aberta, o Flyback entrega a cada
período uma energia fixa $\tfrac{1}{2}L_mI_p^2$, independentemente de quanto a carga consome. Isso
explica a subida para 127 V a 20 % e também por que a resposta ao degrau não oscila: o indutor
esvazia a cada período e deixa de ser uma variável de estado, sobrando só o polo do capacitor com a
carga.

Para o gráfico 3 do *Scope*, use o *Probe* do indutor $L_m$ dividido por $a$ (bloco *Gain* com
`1/a`) e compare com $i_{L,eq}$. Não use a corrente do primário nem a do secundário: cada uma delas
existe só em parte do período (primário com $S_1$ fechado, secundário com $D_1$ conduzindo). A
grandeza contínua, que corresponde ao indutor do Buck-Boost, é a corrente em $L_m$, e como $L_m$ está
explícito no circuito o *Probe* a entrega diretamente em todos os intervalos.

## 8. Resumo dos ensaios de degrau de carga

| Arquivo | `f_carga` | 100 → 20 % | 20 → 100 % | Stop time | Max step | CSV |
|---|---|---|---|---|---|---|
| `forward.plecs` | 10 Hz | 0,05 s | 0,10 s | 0,11 s | 1e-6 | `forward_degrau.csv` |
| `fullbridge.plecs` | 5 Hz | 0,1 e 0,3 s | 0,2 s | 0,31 s | 5e-7 | `fullbridge_degrau.csv` |
| `pushpull.plecs` | 2 Hz | 0,75 e 1,25 s | 1,0 s | 1,3 s | 5e-7 | `pushpull_degrau.csv` |
| `flyback.plecs` (`kL = 1`) | 2 Hz | 0,25 e 0,75 s | 0,5 s | 0,8 s | 1e-6 | `flyback_mcd_degrau.csv` |
| `flyback.plecs` (`kL = 10`) | 2 Hz | 0,25 e 0,75 s | 0,5 s | 0,8 s | 1e-6 | `flyback_mcc_degrau.csv` |

## 9. Verificações obrigatórias antes dos ensaios

### 9.1 Verificação do comando

Antes de montar a parte de potência, ligue ao *Scope* os sinais de gatilho de cada arquivo e rode
por 0,2 ms (quatro períodos a 20 kHz). O que precisa aparecer:

| Arquivo | O que conferir |
|---|---|
| Forward | pulso de 20 µs a cada 50 µs |
| Full-bridge, variante B | `PG_A` alto de 0 a 20 µs, `PG_B` alto de 25 a 45 µs; as chaves inferiores exatamente complementares |
| Full-bridge, variante A | as duas diagonais nunca altas ao mesmo tempo |
| Push-pull | sobreposição de 10 µs duas vezes por período e **nunca** as duas em nível baixo |
| Flyback | pulso de 20 µs a cada 50 µs |
| Equivalentes | Full-bridge: 20 µs alto a cada 25 µs; Push-pull: 10 µs alto a cada 25 µs |

Se o atraso de meio período estiver errado, o sintoma no Full-bridge é saída com metade da tensão
e transformador saturando (corrente magnetizante crescendo sem parar); no Push-pull é erro de
simulação por interrupção da corrente de $L_i$.

### 9.2 Verificação do regime permanente

Com o *Switch* de carga forçado fechado (troque temporariamente o *From* por uma *Constant* igual a
1), rode cada circuito e confira a primeira linha da tabela de resultado esperado de cada seção
($V_o$ e $I_o$ a 100 %). Se o isolado e o equivalente não baterem com o previsto em regime, não
adianta partir para o degrau.

## 10. Ensaio A, formas de onda em regime (apoio às seções "Formas de onda teóricas")

O enunciado pede, para cada conversor, um texto sobre as formas de onda teóricas (Figs. 2, 7, 11 e
16). O PLECS permite conferir cada uma delas, e as curvas simuladas podem entrar no artigo como
validação da análise qualitativa. Rode cada isolado com a carga a 100 % e observe dois ou três
períodos depois do regime (por exemplo, de 0,0499 a 0,05 s), com *Max step size* de `1e-7`.

| Conversor | Sinais a observar (use *Probe*) | Figura a comparar |
|---|---|---|
| Forward | gatilho, $v_{Lo}$, $i_{Lo}$, $i_{Lm}$, $i_{D1}$, $v_{D1}$, $i_{D2}$, $v_{D2}$, $i_{S1}$, $v_{S1}$, $i_{Co}$ | Fig. 2 |
| Full-bridge (variante A) | gatilhos de $S_1$ e $S_3$, $i_{Lo}$, $v_{Lo}$, $i_{Lm}$, $i_{D1}$, $v_{D1}$, $i_{S1}$, $v_{S1}$, $i_{Co}$ | Fig. 7 |
| Push-pull | gatilhos de $S_1$ e $S_2$, $i_{Li}$, $v_{Li}$, $i_{Lm}$, $i_{S1}$, $v_{S1}$, $i_{D1}$, $v_{D1}$, $i_{Co}$ | Fig. 11 |
| Flyback (MCD) | gatilho, $i_{Lm}$, $v_{pri}$, corrente e tensão do secundário, $i_{S1}$, $v_{S1}$, $i_{D1}$, $v_{D1}$, $i_{Co}$ | Fig. 16 |

Salve como `<conversor>_regime.csv` na pasta `resultados PLECS`. Esses dados alimentam também as
figuras das etapas de operação, porque mostram, intervalo a intervalo, quais componentes conduzem.

## 11. Diagnóstico de problemas

| Sintoma | Causa provável | Correção |
|---|---|---|
| Erro de sintaxe ao rodar ("undefined" ou "invalid expression") | sufixo do PSIM num campo (`1080u`, `20k`) | escrever `1080e-6`, `20e3` ou o nome da variável |
| Variável indefinida | script de inicialização não colado, ou nome diferente no campo | conferir a seção 2.2 |
| Forward: erro de simulação ao abrir $S_1$ (corrente de indutor interrompida) ou tensão absurda em $S_1$ | terciário invertido: a corrente magnetizante não tem caminho quando $S_1$ abre | inverter o terciário (ponto em `t`, seção 4.2) |
| $V_o$ do Forward nula | secundário invertido ($D_1$ bloqueia quando $S_1$ conduz) | inverter os terminais do secundário |
| Flyback: $V_o$ errada e erro ao abrir $S_1$ | secundário com o ponto no lado errado: o circuito vira um Forward sem desmagnetização | ponto do secundário no terra (seção 7.2) |
| Corrente magnetizante do Full-bridge crescendo sem limite | atraso de meio período ausente, ou diagonais com razões cíclicas diferentes | seção 9.1 |
| Erro de descontinuidade de corrente em indutor no Push-pull | as duas chaves abertas ao mesmo tempo | conferir $D > 0{,}5$ e o atraso de `1/(2*fs)` |
| Aviso de nó flutuante / tensão indefinida | primário sem *Ground*, ou ponte na variante A sem `Rbal` | seção 1.4 e seção 5.3 |
| Aviso de rigidez ou simulação muito lenta | constantes de tempo muito diferentes ($L_m$ grande, RSE pequena) | *Solver* RADAU (stiff) |
| Isolado e equivalente com valores finais diferentes | relação de espiras arredondada diferente nos dois (17 × 16,875; 67,6 × 67,5 V) | usar as variáveis do script nos dois circuitos |
| Flyback: isolado com tensão de saída um pouco abaixo da do equivalente | grampeador RCD mantido no isolado sem dispersão | remover o grampeador (seção 7.2) |
| Curvas serrilhadas no *Scope* | passo máximo grande demais | reduzir *Max step size* |
| CSV enorme | *Sample time* do *To File* pequeno demais | 1e-6 a 2e-6 é suficiente para os degraus |
| Equivalente do Flyback com tensão negativa no gráfico | voltímetro na ordem convencional | inverter o voltímetro (seção 7.3) |

## 12. Reintroduzindo as não idealidades (opcional)

Os circuitos do professor incluem resistências de enrolamento (0,1 a 1 mΩ) e dispersões (10 a
100 nH). Elas não mudam a equivalência, mas podem entrar numa seção de discussão.

- **Resistências de enrolamento**: acrescente resistores em série com cada enrolamento. Não há
  qualquer cuidado especial.
- **Dispersão**: acrescente um indutor em série com o primário. Com chaves ideais, abrir $S_1$
  interrompe a corrente dessa indutância, e o PLECS precisa de um caminho para ela: no Forward e no
  Flyback, um grampeador RCD (como o do professor) ou um *snubber* RC em paralelo com $S_1$; na
  ponte e no push-pull, os diodos em antiparalelo das chaves já oferecem o caminho. Use o *Solver*
  RADAU nesse caso.
- **Alternativa**: o *Linear Transformer* (Electrical › Transformers) agrega num só bloco espiras,
  dispersões, resistências e indutância magnetizante, como o bloco `T_31` do PSIM. É útil para
  reproduzir exatamente os valores do professor, mas esconde $L_m$ dentro do bloco e torna menos
  direta a observação de $i_{Lm}$.

## 13. Depois da simulação

1. Confira que os cinco arquivos `*_degrau.csv` estão em `resultados PLECS`.
2. Gere os gráficos no estilo das Figs. 5, 9, 14, 19 e 21 com o script de plotagem (a ser criado em
   `resultados PLECS/plotar_degraus.py`, ver `PROXIMOS-PASSOS.md`).
3. Preencha as colunas "Simulado" das tabelas das seções 4 a 7 e leve os números para o documento
   de análise de resultados.
4. Salve uma captura de tela de cada esquemático do PLECS em `desenvolvimento/figuras`, com nomes
   `plecs-forward.png`, `plecs-fullbridge.png`, `plecs-pushpull.png` e `plecs-flyback.png`. Elas
   substituem, no artigo, os esquemáticos do PSIM das Figs. 4, 8, 13, 18 e 20.

Próximo arquivo a ser escrito: `01-fundamentos-conversores-isolados.md`.
