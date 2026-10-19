# 01. Fundamentos de Conversores CC-CC Isolados

Todo conversor deste trabalho é um conversor básico (Buck, Boost ou Buck-Boost) em que se
intercalou um transformador de alta frequência. O transformador faz três coisas ao mesmo tempo:
isola galvanicamente a carga da fonte, ajusta o nível de tensão pela relação de espiras e, em
alguns casos, armazena energia. Este documento reúne o que é comum aos quatro conversores, isto é,
o modelo do transformador, a condição de desmagnetização e, principalmente, a regra geral que
transforma cada conversor isolado no seu equivalente não isolado. Os documentos 02 a 05 aplicam
esse raciocínio a cada topologia.

## 1. Por que isolar

A isolação galvânica é exigida por norma sempre que a entrada está ligada à rede ou a um
barramento perigoso e a saída é acessível ao usuário, como em fontes de telecomunicações (54 V),
carregadores e equipamentos médicos. Mas ela também é uma ferramenta de projeto. Num Buck que
precisa baixar 400 V para 54 V a razão cíclica seria 0,135, com pulsos estreitos, correntes de pico
altas e chaves dimensionadas para 400 V e 93 A ao mesmo tempo. O transformador desloca o problema:
o primário trabalha com tensão alta e corrente baixa, o secundário com tensão baixa e corrente alta,
e a razão cíclica volta para uma faixa confortável (0,4 nos exemplos do enunciado). Por isso os
conversores isolados dominam as fontes chaveadas acima de algumas dezenas de watts.

O preço é um componente magnético a mais, com perdas, indutância de dispersão e a obrigação de
**desmagnetizar o núcleo a cada período**, tema da seção 3.

## 2. O transformador de alta frequência

### 2.1 Transformador ideal

O enunciado define a relação de transformação como secundário sobre primário:

$$n = a = \frac{N_s}{N_p} = \frac{V_s}{V_p} = \frac{I_p}{I_s}$$

de modo que $V_s = a\,V_p$ e $I_p = a\,I_s$. Num transformador ideal a tensão por espira é a mesma
em todos os enrolamentos e os ampères-espiras se anulam:

$$\frac{v_1}{N_1} = \frac{v_2}{N_2} = \frac{v_3}{N_3}, \qquad N_1 i_1 + N_2 i_2 + N_3 i_3 = 0$$

com as correntes tomadas como positivas quando entram pelo terminal marcado com o ponto. É essa
convenção de pontos que distingue, por exemplo, um Forward de um Flyback com o mesmo núcleo: no
Forward os pontos do primário e do secundário estão do mesmo lado e a energia passa à carga
enquanto a chave conduz; no Flyback estão em lados opostos e a energia só passa quando a chave abre.

### 2.2 Modelo com indutância magnetizante

Um núcleo real tem permeabilidade finita, e para estabelecer o fluxo é preciso uma corrente que não
é transferida à carga: a **corrente magnetizante** $i_{Lm}$. O modelo mais simples que a representa é
o transformador ideal com uma indutância $L_m$ em paralelo com o primário:

```
        o-------+--------(•)  ideal  (•)--------o
                |          )        (
    primário   Lm          )  Np:Ns (      secundário
                |          )        (
        o-------+-----------         ---------o
```

Com esse modelo a corrente do primário é a soma de duas parcelas, a refletida da carga e a
magnetizante:

$$i_{pri} = a\,i_{sec} + i_{Lm}, \qquad L_m\frac{di_{Lm}}{dt} = v_{pri}$$

Nos conversores Forward, ponte completa e push-pull, $L_m$ é um efeito parasita, que se quer grande
para que $i_{Lm}$ seja pequena (o enunciado adota 1 a 2 % da corrente de pico do primário). No
Flyback é o contrário: $L_m$ é o próprio elemento armazenador de energia e é dimensionada como o
indutor de um Buck-Boost.

Os modelos no PLECS usam exatamente esse circuito (ver `simulação PLECS/LEIA-ME.md`).

### 2.3 Indutância de dispersão

Parte do fluxo de cada enrolamento não enlaça o outro. Esse fluxo disperso é representado por
indutâncias $L_{d}$ em série com cada enrolamento. Elas não armazenam energia útil e, quando a chave
abre, a energia $\tfrac{1}{2}L_d i^2$ precisa de um caminho: é ela que produz os picos de tensão
sobre as chaves e exige grampeadores (o RCD do Flyback do professor) ou circuitos de comutação
suave. Neste trabalho a dispersão foi desprezada, porque não altera a equivalência dinâmica que se
quer verificar e, com chaves ideais, só acrescentaria picos numéricos sem significado físico.

## 3. Desmagnetização: o balanço volt-segundo

Em regime permanente o fluxo no núcleo precisa voltar ao mesmo valor ao fim de cada período, caso
contrário ele cresce ciclo a ciclo até a saturação. Como $v = N\,d\phi/dt$, isso equivale a exigir
que a tensão média sobre qualquer enrolamento seja nula:

$$\int_0^T v_{pri}\,dt = 0 \qquad\Longleftrightarrow\qquad \text{área } A^+ = \text{área } A^-$$

São as áreas $A^+$ e $A^-$ desenhadas nas formas de onda do enunciado (Figs. 2, 7, 11 e 16). Cada
topologia cumpre essa condição de um jeito diferente, e isso é o que mais distingue uma da outra:

| Conversor | Como o núcleo é desmagnetizado | Consequência |
|---|---|---|
| Forward | enrolamento terciário devolve a energia magnetizante à fonte, aplicando $-V_i\,N_p/N_t$ | com $N_t = N_p$, $D \le 0{,}5$; a chave suporta $2V_i$ |
| Ponte completa | o primário recebe $+V_i$ e $-V_i$ alternadamente, com o mesmo tempo | desmagnetização natural; $D < 0{,}5$ por diagonal |
| Push-pull alimentado em corrente | cada metade do primário recebe tensões opostas em semiciclos alternados | desmagnetização natural; exige $D > 0{,}5$ (sobreposição) |
| Flyback | a energia de $L_m$ é entregue à carga pelo secundário com a chave aberta | $L_m$ é o indutor do conversor; MCD ou MCC |

As topologias em que o primário é excitado nos dois sentidos (ponte, meia-ponte, push-pull) usam o
núcleo nos dois quadrantes do laço B-H, e por isso aproveitam melhor o ferrite do que as de uma
chave (Forward, Flyback), que só o excitam num sentido. É uma das razões pelas quais a ponte
completa aparece no exemplo de maior potência (5 kW).

## 4. O conversor equivalente referido ao secundário

### 4.1 A ideia

Olhando da carga para trás, o filtro de saída e a carga de um conversor isolado não sabem que
existe um transformador. Tudo o que eles enxergam é uma certa forma de onda de tensão (ou de
corrente) aplicada na entrada do filtro. Se um conversor básico, sem transformador, produzir
**exatamente a mesma forma de onda** nesse ponto, o filtro e a carga se comportam de modo idêntico,
em regime e em transitório. Esse conversor básico é o **equivalente referido ao secundário**.

A verificação desse fato por simulação, com degraus de carga, é o objetivo central do enunciado:
se a equivalência vale no transitório, o modelo médio e as funções de transferência do conversor
básico (deduzidos no projeto `controle-main/Modelos de Conversores FT`) podem ser usados para
projetar a malha de controle do conversor isolado.

### 4.2 As três regras de reflexão

Para levar um elemento do primário ao secundário basta preservar tensão por espira e potência:

| Grandeza do primário | Equivalente no secundário | Por quê |
|---|---|---|
| Fonte de tensão $V_i$ | $a\,V_i$ | a tensão por espira é a mesma |
| Corrente $i$ | $i/a$ | ampères-espiras se conservam |
| Indutância $L$ | $a^2L$ | energia $\tfrac12 L i^2 = \tfrac12 (a^2L)(i/a)^2$ se conserva |
| Resistência ou impedância $Z$ | $a^2Z$ | idem, $v/i$ escala com $a^2$ |

A quarta regra é específica das topologias simétricas. Na ponte completa e no push-pull o
retificador de onda completa entrega ao filtro **dois pulsos por período de comutação**, um em cada
semiciclo do transformador. O equivalente precisa então comutar no **dobro da frequência**,
$f_{eq} = 2f_s$, e a sua razão cíclica é a fração de cada meio período ocupada pelo pulso.

### 4.3 Aplicação aos quatro conversores

**Forward → Buck.** Com $S_1$ fechada o secundário aplica $nV_i$ ao filtro através de $D_1$; com
$S_1$ aberta a corrente de $L_o$ circula por $D_2$ e a entrada do filtro fica em zero. É a forma de
onda do nó de comutação de um Buck alimentado por $nV_i$:

$$V_{i,eq} = nV_i, \quad D_{eq} = D, \quad f_{eq} = f_s, \quad V_o = nDV_i$$

**Ponte completa → Buck.** A entrada do filtro recebe $aV_i$ durante $DT$ em cada meio período e
zero no restante (roda livre pelos quatro diodos). É um Buck de frequência dobrada:

$$V_{i,eq} = aV_i, \quad D_{eq} = \frac{DT}{T/2} = 2D, \quad f_{eq} = 2f_s, \quad V_o = 2aDV_i$$

**Push-pull alimentado em corrente → Boost.** Aqui o elemento armazenador está no primário. Nos
intervalos de sobreposição, em que as duas chaves conduzem, o primário fica em curto e $L_i$ recebe
$V_i$; nos intervalos com uma só chave, $L_i$ recebe $V_i - V_o/a$ e entrega energia à saída.
Multiplicando as tensões por $a$ e referindo $L_i$ ao secundário:

| Intervalo | Tensão em $L_i$ | Referida ao secundário | Boost equivalente |
|---|---|---|---|
| Sobreposição, duração $(2D-1)T/2$, duas vezes por período | $V_i$ | $aV_i$ | chave fechada |
| Uma chave, duração $(1-D)T$, duas vezes por período | $V_i - V_o/a$ | $aV_i - V_o$ | chave aberta |

$$V_{i,eq} = aV_i, \quad L_{eq} = a^2L_i, \quad D_{eq} = 2D - 1, \quad f_{eq} = 2f_s, \quad
V_o = \frac{aV_i}{1 - D_{eq}} = \frac{aV_i}{2(1-D)}$$

**Flyback → Buck-Boost.** Com $S_1$ fechada, $L_m$ recebe $V_i$; com $S_1$ aberta, a corrente
magnetizante passa ao secundário e $L_m$, visto do secundário, recebe $-V_o$. Referindo $L_m$ ao
secundário obtém-se um Buck-Boost, cuja saída é invertida (o transformador desfaz a inversão, o
equivalente não):

$$V_{i,eq} = aV_i, \quad L_{eq} = a^2L_m, \quad D_{eq} = D, \quad f_{eq} = f_s, \quad
V_o = aV_i\frac{D}{1-D}\ \text{(MCC)}$$

### 4.4 Valores numéricos dos quatro exemplos

| | Forward | Ponte completa | Push-pull | Flyback |
|---|---|---|---|---|
| Relação de espiras | $n = 0{,}675$ (sim.: 0,68) | $a = 0{,}16875$ | $a = 4{,}444$ | $a = 0{,}405$ |
| $V_{i,eq}$ | 135 V (sim.: 136 V) | 67,5 V | 240 V | 81 V |
| $L_{eq}$ | $L_o$ = 1,08 mH | $L_o$ = 14,58 µH | $a^2L_i$ = 2,883 mH | $a^2L_m$ = 118 µH (MCD) / 1,18 mH (MCC) |
| $D_{eq}$ / $f_{eq}$ | 0,4 / 20 kHz | 0,8 / 40 kHz | 0,4 / 40 kHz | 0,4 / 20 kHz |
| $V_o$ | 54 V (sim.: 54,4 V) | 54 V | 400 V | 54 V (MCC) |

O Forward simulado tem 54,4 V porque o professor usou 100:68 espiras (0,68) em vez de 0,675; o
equivalente foi alimentado com os mesmos 136 V, e os dois circuitos coincidem.

### 4.5 O que o equivalente não representa

A equivalência é exata para a tensão e a corrente de saída, mas deixa de fora tudo o que existe só
do lado do primário:

- **a corrente magnetizante** (exceto no Flyback, onde ela é a corrente do indutor);
- **o reset do núcleo** e as restrições de razão cíclica que ele impõe ($D \le 0{,}5$ no Forward,
  $D < 0{,}5$ na ponte, $D > 0{,}5$ no push-pull);
- **os esforços nas chaves do primário** ($2V_i$ no Forward, $2V_o/a$ no push-pull);
- **a dispersão**, que atrasa a subida da corrente no secundário e reduz a razão cíclica efetiva
  (perda de razão cíclica), um efeito que em conversores reais pode ser apreciável.

Por isso o equivalente serve para a **modelagem dinâmica e o projeto do controle**, mas não para o
dimensionamento dos semicondutores e do transformador, que continua sendo feito no circuito
isolado.

### 4.6 O que a simulação mostrou

Com componentes ideais, as duas simulações de cada conversor coincidem dentro da precisão numérica
(tabela completa em `resultados PLECS/metricas_degraus.md`):

| Conversor | Maior diferença isolado × equivalente em $V_o$ e $I_o$ |
|---|---|
| Forward | 0,000 % (idênticos) |
| Ponte completa | 0,088 % RMS; 0,78 % no pior instante (degrau 100 → 20 %) |
| Push-pull | 0,064 % RMS; 0,34 % no pior instante (degrau 100 → 20 %) |
| Flyback, MCD e MCC | 0,000 % (idênticos) |

As pequenas diferenças da ponte e do push-pull vêm justamente da seção 4.5: nos dois circuitos
isolados a corrente magnetizante é modelada ($L_m$ = 2,6 mH e 200 mH) e circula pelo retificador,
algo que o equivalente não tem. No Forward e no Flyback essa corrente não passa pelo filtro de
saída (no Forward é devolvida à fonte pelo terciário; no Flyback ela é a própria corrente do
indutor equivalente), e por isso os circuitos coincidem exatamente.

## 5. Modos de condução

Todos os exemplos, exceto o Flyback de projeto, operam em **modo de condução contínua (MCC)** em
toda a faixa de 20 % a 100 % de carga, porque a ondulação de corrente especificada ($\Delta I$ ≈ 20 %
da corrente nominal) é menor que o dobro da corrente mínima. A verificação está em
`calculos/parametros_projeto.py`:

| Conversor | Corrente mínima no indutor a 20 % de carga |
|---|---|
| Forward | 1,10 A |
| Ponte completa | 9,26 A |
| Push-pull | 1,85 A (lado primário) |

O Flyback é projetado com $L_m = 0{,}9\,L_{crit}$, isto é, em **modo de condução descontínua
(MCD)** já a plena carga. Em MCD o indutor esvazia a cada período, deixa de ser uma variável de
estado e o ganho passa a depender da carga,

$$V_o = V_i D\sqrt{\frac{R_o}{2L_mf_s}},$$

o que muda qualitativamente a dinâmica (documento 05). A nota do professor sobre multiplicar $L_m$
por dez existe exatamente para mostrar também o caso em MCC.

## Referências deste documento

- Enunciado do Trabalho 2 (Prof. R. P. Torrico-Bascopé), seções 1 a 4.
- R. W. Erickson e D. Maksimović, *Fundamentals of Power Electronics*, 3. ed., Springer, 2020,
  cap. 6 (conversores isolados) e cap. 13 (magnéticos).
- N. Mohan, T. M. Undeland e W. P. Robbins, *Power Electronics: Converters, Applications and
  Design*, 3. ed., Wiley, 2003, cap. 10.
- I. Barbi, *Projetos de Fontes Chaveadas*, 3. ed., edição do autor, Florianópolis, 2015.

Próximo arquivo: `02-forward.md`.
