# 11. Resumo Consolidado e Referências

Este documento fecha o trabalho. A Seção 2 é a que dá unidade às duas partes: as expressões de
perda levantadas na Parte 1 são aplicadas ao conversor cujo transformador foi projetado na Parte 2,
e o rendimento resultante é confrontado com a hipótese que abriu o dimensionamento.

## 1. Consolidação da Parte 1

### 1.1 As expressões

$$\begin{array}{l|l|l}
\textbf{Dispositivo} & \textbf{Condução} & \textbf{Comutação}\\ \hline
\text{Diodo} & V_{TO}I_{F(av)} + r_TI_{F(rms)}^2 &
P_{ec}\approx 0;\ P_{bloq}=\tfrac12 Q_{rr}V_Rf_s\\[2pt]
\text{Tiristor / TRIAC} & V_{TO}I_{T(av)} + r_TI_{T(rms)}^2 &
\text{desprezível para } f_s<1\ \text{kHz}\\[2pt]
\text{MOSFET} & R_{DS(on)}(T_j)\,I_{D(rms)}^2 &
0{,}6\,V_{DS}I_D(t_r+t_f)f_s + \tfrac12 C_{o(er)}V_{DS}^2f_s\\[2pt]
\text{IGBT} & V_{CE(sat)}I_{C(av)} &
(E_{on}+E_{off})f_s
\end{array}$$

### 1.2 Os sete exemplos numéricos

| # | Componente | Aplicação | $f_s$ | $P_{cond}$ | $P_{com}$ | $P_{total}$ | $R_{th,da}$ exigida |
|---|---|---|---|---|---|---|---|
| 1 | SKKD 46/16 | Ponte 60 Hz, 30 A | 60 Hz | 15,00 W | ~0 | 15,00 W | 0,97 °C/W (4 diodos) |
| 2 | DSEI2×31-06C | Boost 1 kW | 50 kHz | 2,85 W | 7,44 W | 10,29 W | 6,56 °C/W |
| 3 | TYN1225 | Retificador controlado 15 A | 60 Hz | 7,35 W | 1,05 W | 8,40 W | 1,46 °C/W (4 SCR) |
| 4 | BTA41-600B | Controlador CA 2,4 kW ($\alpha = 90°$) | 60 Hz | 12,32 W | ~0 | 12,32 W | 4,28 °C/W |
| 5 | IRFP460A | Buck 200 V / 8 A | 50 kHz | 12,53 W | 4,51 W | 17,04 W | 4,04 °C/W |
| 6 | IRG4PC40UD | Braço de inversor 400 V / 20 A | 10 kHz | 17,20 W | 10,60 W | 27,80 W | 2,05 °C/W |
| 7 | TYN1225 + SKKD 46 | Ponte mista 15 A | 60 Hz | 28,58 W | ~0 | 28,58 W | 1,81 °C/W |

O Exemplo 4 é apresentado no ângulo de disparo de 90°; o caso dimensionante do dissipador é
$\alpha = 0°$, com 24,64 W e $R_{th,da} \le 1{,}44$ °C/W (documento 03, Seção 3.4).

### 1.3 As três conclusões da Parte 1

**A frequência é a variável organizadora.** A fração de comutação na perda total cresce de zero em
60 Hz para mais de 70 % em 50 kHz. É essa progressão que separa as famílias de dispositivos e que
define o nicho de cada uma.

**O tipo de carga muda o resultado por um fator 3,6.** O modelo de carga resistiva do livro-texto,
com fator $1/6$, e o modelo de carga indutiva grampeada dos slides, com fator $\tfrac12$ e margem
de 20 %, descrevem situações físicas distintas. Aplicar o primeiro num conversor com diodo de roda
livre subestima grosseiramente a perda de comutação.

**A correção térmica dos parâmetros não é refinamento, é requisito.** A $R_{DS(on)}$ de um MOSFET
de 500 V cresce 45 % entre 25 °C e 100 °C; a resistividade do cobre, 31 % entre 20 °C e 100 °C. Os
dois erros apontam no mesmo sentido, o de subestimar a perda, e se realimentam com a temperatura.

## 2. Aplicação integrada: as perdas do conversor da Parte 2

O transformador projetado na Parte 2 pertence a um conversor em ponte completa de 500 W. As
expressões da Parte 1 permitem calcular as perdas dos semicondutores desse conversor e, com elas,
o rendimento, fechando o círculo do trabalho.

### 2.1 Topologia e componentes

| Bloco | Componente | Quantidade | Justificativa |
|---|---|---|---|
| Chaves do primário | SPW20N60C3 (CoolMOS, 650 V / 20,7 A) | 4 | 650 V sobre barramento de 400 V: margem de 63 % |
| Transformador | Thornton NEE-42/21/20, 60:10 | 1 | Projeto da Parte 2 |
| Retificador do secundário | MBR20200CT (Schottky, 200 V / 2×10 A) | 2 (4 diodos) | PIV de 66,7 V com margem de 3 vezes |

### 2.2 Perdas nas chaves do primário

Cada chave conduz durante $D_{req} = 0{,}4103$ do período, com o patamar de corrente
$I_{p,patamar} = 1{,}5546$ A.

$$I_{sw(rms)} = I_{p,patamar}\sqrt{D_{req}} = 1{,}5546\sqrt{0{,}4103} = 0{,}9957\ \text{A}$$

**Condução.** Corrigindo $R_{DS(on)}$ para 100 °C com o fator 1,5 da curva normalizada:

$$R_{DS(on)}(100\,^\circ\text{C}) = 0{,}19 \times 1{,}5 = 0{,}285\ \Omega$$
$$P_{cond} = 0{,}285 \times 0{,}9957^2 = 0{,}2826\ \text{W}$$

**Comutação (cruzamento de $v$ e $i$).** Com $t_r = 5$ ns e $t_f = 4{,}5$ ns:

$$P_{ec} = \tfrac12 \times 1{,}5546 \times 400 \times (1{,}2 \times 5\ \text{ns}) \times 10^5
= 0{,}1865\ \text{W}$$
$$P_{bloq} = \tfrac12 \times 1{,}5546 \times 400 \times (1{,}2 \times 4{,}5\ \text{ns}) \times 10^5
= 0{,}1679\ \text{W}$$

**Comutação (parcela capacitiva).** Aqui a advertência do documento 04, Seção 4, cobra o seu preço.
A $C_{oss}$ de catálogo, 780 pF, é medida a $V_{DS} = 25$ V; em 400 V a capacitância equivalente de
energia $C_{o(er)}$ é muito menor. A sensibilidade:

| $C_{o(er)}$ | $P_{cap} = \tfrac12 C_{o(er)}V^2f_s$ |
|---|---|
| 50 pF | 0,400 W |
| 100 pF | 0,800 W |
| 150 pF | 1,200 W |

Adotando a estimativa central de 50 pF, característica de dispositivos de superjunção em 400 V:

$$P_{cap} = 0{,}400\ \text{W}$$

**Total por chave e no conjunto:**

$$P_{sw} = 0{,}2826 + 0{,}1865 + 0{,}1679 + 0{,}400 = 1{,}0370\ \text{W}$$
$$\boxed{P_{primário} = 4 \times 1{,}0370 = 4{,}148\ \text{W}}$$

**Observação central.** A parcela capacitiva, 0,400 W, responde sozinha por **39 %** da perda de
cada chave, mais que a condução (27 %) e mais que o cruzamento de tensão e corrente (34 %). Este é
o regime de alta tensão, baixa corrente e alta frequência em que o modelo linear de comutação, por
si só, dá uma resposta incompleta. Vale registrar também que a incerteza sobre $C_{o(er)}$ é a
maior de todo o balanço: entre 50 e 150 pF, a perda total das quatro chaves varia de 4,15 W a
7,35 W.

### 2.3 Perdas no retificador do secundário

Da folha de dados do MBR20200CT, $V_F = 0{,}66$ V típico a $I_F = 10$ A e $T_j = 125$ °C. Com o
retificador em ponte, dois diodos conduzem simultaneamente:

$$P_{retif} = 2\,V_F\,I_o = 2 \times 0{,}66 \times 9{,}259 = 12{,}222\ \text{W}$$

Se a configuração fosse de derivação central, com apenas um diodo em série:

$$P_{retif} = V_F\,I_o = 6{,}111\ \text{W}$$

### 2.4 Balanço e rendimento

| Bloco | Perda | Fração |
|---|---|---|
| 4 × SPW20N60C3 (primário) | 4,148 W | 22,0 % |
| Retificador de saída (ponte, 4 Schottky) | 12,222 W | 64,7 % |
| Transformador (cobre + núcleo) | 2,514 W | 13,3 % |
| **Total** | **18,884 W** | 100 % |

$$\eta_{conversor} = \frac{500}{500 + 18{,}884} = 96{,}36\ \%$$

Com secundário em derivação central (que exigiria o núcleo NEE-55/28/21, conforme o documento 09,
Seção 10):

| Bloco | Perda | Fração |
|---|---|---|
| 4 × SPW20N60C3 | 4,148 W | 32,5 % |
| Retificador de saída (derivação central, 2 Schottky) | 6,111 W | 47,8 % |
| Transformador | 2,514 W | 19,7 % |
| **Total** | **12,773 W** | 100 % |

$$\eta_{conversor} = \frac{500}{512{,}77} = 97{,}51\ \%$$

*(O balanço não inclui o indutor de saída, os capacitores, o circuito de comando e o controlador,
que somariam cerca de 1 % adicional em um conversor completo.)*

### 2.5 As três leituras deste balanço

**Primeira leitura, o retificador de saída domina.** Com 12,2 W, o retificador responde por quase dois
terços da perda dos semicondutores, e por 2,4 % da potência de saída. A causa é estrutural: a saída
é de baixa tensão (54 V) e alta corrente (9,26 A), e a queda de 0,66 V de cada Schottky representa
1,2 % dessa tensão. **Em fontes de baixa tensão, o retificador de saída é sempre o gargalo de
rendimento**, e é por isso que fontes comerciais acima de algumas centenas de watts usam
**retificação síncrona**, com MOSFETs de baixa $R_{DS(on)}$ no lugar dos diodos. Com
$R_{DS(on)} = 5$ mΩ, a queda a 9,26 A seria de 46 mV em vez de 660 mV, e a perda cairia de 12,2 W
para 0,86 W.

**Segunda leitura, a escolha do documento 09 tem custo mensurável.** Adotar a ponte no secundário para
caber no núcleo menor custa 6,1 W, ou 1,15 ponto percentual de rendimento. Em troca, economiza 106 g
de ferrite. **O projeto magnético e o projeto do retificador estão acoplados**, e a decisão correta
depende de qual restrição pesa mais na aplicação, o volume ou o rendimento.

**Terceira leitura, a hipótese de rendimento do passo 1 é confirmada.** O
$\eta = 98$ % adotado no dimensionamento é o **rendimento do transformador**, e o projeto entregou
99,50 %, o que confirma que a hipótese era conservadora e portanto segura. O rendimento do
**conversor**, 96,4 %, é uma
grandeza distinta e não deve ser confundida com aquela. Essa distinção é a fonte de erro mais
comum na aplicação do método de McLyman: usar o rendimento do conversor completo no cálculo de
$P_t$ superdimensionaria o núcleo sem necessidade.

## 3. Consolidação da Parte 2

### 3.1 Especificações e projeto fechado

| Grandeza | Símbolo | Valor |
|---|---|---|
| **Especificações** | | |
| Tensão de entrada | $V_{in}$ | 400 V |
| Tensão de saída | $V_o$ | 54 V |
| Potência de saída | $P_o$ | 500 W |
| Frequência de comutação | $f_s$ | 100 kHz |
| Razão cíclica nominal | $D$ | 0,40 |
| **Escolhas de projeto** | | |
| Densidade de fluxo (amplitude) | $B_{ac}$ | 0,07 T |
| Densidade de corrente | $J$ | 400 A/cm² |
| Fator de utilização da janela | $K_u$ | 0,40 |
| Fator de forma de onda | $K_f$ | 4,00 |
| Rendimento admitido | $\eta$ | 98 % |
| **Núcleo** | | |
| Modelo | | Thornton NEE-42/21/20 |
| Material | | IP12R (Mn-Zn) |
| Produto de áreas requerido / disponível | $A_p$ / $A_eA_w$ | 2,255 / 3,768 cm⁴ |
| Seção efetiva | $A_e$ | 2,40 cm² |
| Janela do carretel | $A_w$ | 1,57 cm² |
| Comprimento médio da espira | $l_t$ | 10,5 cm |
| Volume efetivo | $V_e$ | 23,30 cm³ |
| Massa | $m$ | 112 g |
| **Enrolamentos** | | |
| Espiras primário / secundário | $N_p$ / $N_s$ | 60 / 10 (6:1) |
| Condutor | | 26 AWG |
| Fios em paralelo, primário / secundário | $n_p$ / $n_s$ | 3 / 17 |
| Resistência primário / secundário (100 °C) | $R_p$ / $R_s$ | 369,75 / 10,87 mΩ |
| **Verificações** | | |
| Excursão de fluxo, operação / pior caso | $\Delta B$ | 0,1140 / 0,1389 T |
| Margem de saturação (pior caso, a 100 °C) | | 4,7 × |
| Razão cíclica requerida | $D_{req}$ | 0,4103 |
| Margem de razão cíclica até $D_{max} = 0{,}45$ | | 8,8 % |
| Corrente eficaz primário / secundário | $I_p$ / $I_s$ | 1,4081 / 8,3872 A |
| Densidade de corrente realizada, prim. / sec. | $J_p$ / $J_s$ | 364,7 / 383,3 A/cm² |
| Ocupação da janela | $K_u$ | 0,3574 (89 % do útil) |
| Perda no cobre | $P_{cu}$ | 1,4981 W |
| Perda no núcleo | $P_{fe}$ | 1,0154 W |
| Perda total | $P_\Sigma$ | 2,5135 W |
| Densidade de perdas no núcleo | | 43,6 mW/cm³ |
| Resistência térmica | $R_t$ | 14,08 °C/W |
| Elevação de temperatura | $\Delta T$ | 35,4 °C |
| Temperatura do núcleo | $T$ | 75,4 °C |
| Rendimento do transformador | $\eta_{trafo}$ | 99,50 % |
| Regulação | $\alpha$ | 0,30 % |
| Indutância de magnetização | $L_m$ | 23,51 mH |
| Corrente de magnetização (pico) | $I_{mag}$ | 69,8 mA (4,5 %) |

### 3.2 Verificação dos critérios de aceitação

| Critério | Limite | Obtido | Situação |
|---|---|---|---|
| Produto de áreas | $A_eA_w \ge A_p$ | 3,768 ≥ 2,255 cm⁴ | ✓ folga de 67 % |
| Ocupação da janela | $K_u \le 0{,}40$ | 0,3574 | ✓ folga de 11 % |
| Densidade de perdas no núcleo | ≤ 100 mW/cm³ | 43,6 (70,1 no pior caso) | ✓ |
| Elevação de temperatura | ≤ 40 °C | 35,4 °C | ✓ folga de 4,6 °C |
| Margem de saturação | ≥ 2 × | 4,7 × | ✓ |
| Diâmetro do fio | ≤ $2\varepsilon$ = 0,419 mm | 0,405 mm | ✓ |
| Margem de razão cíclica | ≥ 5 % | 8,8 % | ✓ |
| Corrente de magnetização | ≤ 10 % | 4,5 % | ✓ |
| Regulação | ≤ 0,5 % | 0,30 % | ✓ |

**Todos os nove critérios são atendidos.** O mais apertado é a ocupação da janela, com 89 % do
espaço útil consumido, consequência direta da opção por adotar o menor núcleo viável.

### 3.3 As três conclusões da Parte 2

**O critério do produto de áreas é necessário, não suficiente.** Ele fixa o produto $A_eA_w$, mas
não a repartição entre seção e janela. A primeira tentativa deste projeto satisfez $A_p$ com 19 %
de folga e mesmo assim exigiria 125 % da janela disponível. A verificação de $K_u$ precisa ser
tratada como restrição durante o dimensionamento, e não como constatação posterior.

**Em alta frequência, quem limita a densidade de fluxo é a perda, não a saturação.** O IP12R satura
em torno de 0,33 T a quente; o projeto opera com pico de 0,069 T, quase cinco vezes menos. O limite
efetivo veio do critério de 100 mW/cm³, que em 100 kHz corresponde a $\Delta B \le 0{,}161$ T.

**O ótimo é o equilíbrio entre cobre e núcleo, restrito pela execução.** A varredura de $B_{ac}$
mostrou o mínimo de perda total em 0,06 T, inatingível por falta de janela; o valor adotado, 0,07 T,
fica 3,5 % acima do mínimo teórico e é o menor $B_{ac}$ fisicamente executável. As perdas
resultantes se repartem em 59,6 % de cobre e 40,4 % de núcleo, próximo do 50/50 previsto pela
teoria.

## 4. Limitações do trabalho

Registradas explicitamente, para que o leitor saiba o que não foi feito:

1. **A resistência CA dos enrolamentos não foi calculada.** O efeito de proximidade foi tratado por
   recomendação construtiva (intercalamento) e quantificado apenas como cenário de sensibilidade
   ($F_R = 1{,}4$). Um cálculo rigoroso exigiria o método de Dowell.
2. **A indutância de dispersão não foi calculada**, apenas especificada como critério de ensaio
   ($\le 1$ % de $L_m$). Ela afeta a sobretensão nas chaves e a razão cíclica efetiva.
3. **A capacitância equivalente de energia $C_{o(er)}$** do MOSFET foi estimada, não extraída de
   catálogo. É a maior fonte de incerteza do balanço da Seção 2.
4. **Não houve verificação experimental nem por simulação.** Todos os resultados são analíticos, a
   partir de dados de catálogo.
5. **O modelo térmico do transformador é de resistência única**, com temperatura uniforme. O ponto
   quente real fica no interior do enrolamento e é mais alto que o valor calculado.
6. **A carga de recuperação $Q_{rr}$** dos diodos foi estimada pela aproximação triangular
   $Q_{rr} = \tfrac12 t_{rr}I_{rr}$, com dispersão de até cinco vezes entre 25 °C e 100 °C, o que
   torna o Exemplo 2 o de maior incerteza da Parte 1.

## 5. Referências

### 5.1 Material da disciplina

[1] TORRICO BASCOPÉ, R. P. **Eletrônica Industrial, Unidade I: Dispositivos de Eletrônica de
Potência.** Notas de aula. Fortaleza, 2025.

[2] TORRICO BASCOPÉ, R. P. **Transformadores e Indutores de Baixa e Alta Frequência.**
Apostila 01 de Magnéticos. Fortaleza, 2015.

[3] UMANAND, L. **Power Electronics: Essentials and Applications.** Capítulo 1: *Power
Semiconductor Switches*. Wiley India.

### 5.2 Bibliografia de projeto

[4] McLYMAN, C. W. T. **Transformer and Inductor Design Handbook.** 3. ed. Marcel Dekker.
*(Base das expressões de produto de áreas, coeficiente de geometria e elevação de temperatura
adotadas na Parte 2.)*

[5] BARBI, I. **Projeto de Fontes Chaveadas.** Florianópolis: edição do autor.
*(Base da expressão de perdas no núcleo de ferrite e da resistência térmica em função de
$A_eA_w$.)*

[6] BOYLESTAD, R. L.; NASHELSKY, L. **Dispositivos Eletrônicos e Teoria de Circuitos.**
*(Modelo linear por partes do diodo.)*

[7] PETRY, C. A. **Especificação de Semicondutores e Cálculo Térmico.** Capítulo 4 de Eletrônica de
Potência. Florianópolis, 2013, revisado em 2020.

[8] KAZIMIERCZUK, M. K. **High-Frequency Magnetic Components.** Wiley.
*(Referência para efeito pelicular, efeito de proximidade e método de Dowell.)*

### 5.3 Catálogos e folhas de dados

**Núcleos magnéticos**

[9] THORNTON ELETRÔNICA LTDA. **Catálogo de Ferrite.**
https://www.thornton.com.br/pdf/CATALOGO%20THORNTON.pdf

[10] THORNTON ELETRÔNICA LTDA. **Product Catalog** (edição em inglês, com $A_w$ e MLT).
https://www.thornton.com.br/pdf/CATALOG%20THORNTON_ing.pdf

**Semicondutores**

[11] SEMIKRON. **SEMIPACK 1 Rectifier Diode Modules, SKKD 46 e SKKD 81.**
https://media.distrelec.com/Web/Downloads/ta/_e/riSKKx81_Data_E.pdf

[12] LITTELFUSE / IXYS. **DSEI2x31-06C, Fast Recovery Epitaxial Diode.**
https://www.littelfuse.com/assetdocs/littelfuse-power-semiconductors-dsei2x31-06c-datasheet

[13] STMICROELECTRONICS. **TN2540, TXN625, TYN625, TYN825, TYN1225, SCRs.**
https://www.st.com/resource/en/datasheet/tn2540.pdf

[14] STMICROELECTRONICS / WeEn. **BTA41-600B, 4Q Triac.**
https://www.mouser.com/datasheet/2/848/BTA41-600B-1382474.pdf

[15] VISHAY SILICONIX. **IRFP460A / SiHFP460, Power MOSFET.**
https://www.vishay.com/docs/91234/sihfp460.pdf

[16] INFINEON TECHNOLOGIES. **SPW20N60C3, CoolMOS Power Transistor.**
https://www.gloriouselectronics.com/wp-content/uploads/2025/01/SPW20N60C3.pdf

[17] INTERNATIONAL RECTIFIER. **IRG4PC40UD, Insulated Gate Bipolar Transistor with Ultrafast Soft
Recovery Diode.** https://www.farnell.com/datasheets/68574.pdf

[18] ON SEMICONDUCTOR. **MBR20200CT, Switch-mode Power Rectifier.**
https://www.onsemi.com/download/data-sheet/pdf/mbr20200ct-d.pdf

[19] ON SEMICONDUCTOR / FAIRCHILD. **MUR1540 e MUR1560, Ultrafast Rectifiers.**
https://eletrodex.org/eletrodex/Loja_Tray/Datasheets/Semicondutores/Diodos/Rapidos/MUR1560.pdf

### 5.4 Trabalho correlato da mesma linha

[20] NETO, C. **Projeto e Verificação Térmica de um Retificador Monofásico em Ponte com Filtro
Capacitivo.** Trabalho de Eletrônica de Potência (Fontes Chaveadas), 2026.
*(Fonte da metodologia de cálculo térmico e do padrão de organização deste memorial.)*

---

## Índice de figuras sugeridas para o artigo

Para orientar a montagem do artigo IEEE, as figuras que a exposição pede:

| Fig. | Conteúdo | Documento de origem |
|---|---|---|
| 1 | Estrutura e símbolo do diodo; curva característica com as três regiões | 02, Seção 1 |
| 2 | Modelo linear por partes e extração de $V_{TO}$ e $r_T$ | 02, Seção 3 |
| 3 | Formas de onda da recuperação reversa, com $t_{rr}$, $I_{rr}$ e $Q_{rr}$ | 02, Seção 4.2 |
| 4 | Curva característica do SCR com $I_G$ como parâmetro; modelo de dois transistores | 03, Seções 1.2 e 1.3 |
| 5 | Característica de saída do MOSFET com as regiões ôhmica e ativa | 04, Seção 1.3 |
| 6 | Os seis intervalos de comutação do MOSFET | 04, Seção 2 |
| 7 | Estrutura do IGBT e circuitos equivalentes; corrente de cauda | 05, Seções 1.1 e 1.5 |
| 8 | Circuito térmico equivalente com vários dispositivos | 06, Seção 2 |
| 9 | Fronteira MOSFET × IGBT: perda total × corrente, a 20 kHz | 06, Seção 3.2 |
| 10 | Laço B-H: processamento simétrico × assimétrico | 07, Seção 2.4 |
| 11 | Efeito pelicular: distribuição de corrente e $\varepsilon$ × frequência | 07, Seção 5 |
| 12 | Topologia do conversor em ponte completa com formas de onda de $v_p$ e $B$ | 08 e 09 |
| 13 | Varredura de $B_{ac}$: $P_{cu}$, $P_{núcleo}$, $P_{total}$ e $K_u$ | 08, Seção 4.1 |
| 14 | Corte do carretel com a sequência de bobinagem intercalada | 10, Seção 7 |
| 15 | Repartição das perdas do conversor completo | 11, Seção 2.4 |

---

**Documento anterior:** [10. Verificação: perdas e térmica](10-verificacao-perdas-e-termica.md)
**Voltar ao início:** [00. Índice do projeto](00-indice-do-projeto.md)
