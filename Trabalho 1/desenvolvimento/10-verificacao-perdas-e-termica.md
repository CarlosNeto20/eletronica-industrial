# 10. Verificação: Perdas, Térmica e Magnetização

Os passos 12 a 15 do roteiro. Aqui o projeto deixa de ser dimensionamento e passa a ser
verificação: o transformador da tabela final do documento 09 é submetido às três provas que decidem
se ele é executável: perdas, temperatura e comportamento magnético.

## 1. Perdas no cobre (passo 12)

### 1.1 Resistividade na temperatura de operação

A resistividade tabelada é a 20 °C. Corrigindo para a temperatura de operação estimada dos
enrolamentos, 100 °C:

$$\rho(100\,^\circ\text{C}) = \rho_{20}\left[1 + \alpha(100 - 20)\right]
= 1{,}724\times10^{-6}\left[1 + 0{,}00393 \times 80\right]$$
$$= 1{,}724\times10^{-6} \times 1{,}3144 = 2{,}266\times10^{-6}\ \Omega\cdot\text{cm}$$

Um acréscimo de **31,4 %** sobre o valor a 20 °C. Fazer o cálculo a 20 °C subestimaria a perda no
cobre em quase um terço.

### 1.2 Comprimento dos condutores

Com $l_t = 10{,}5$ cm por espira (MLT do carretel do NEE-42/21/20):

$$l_{cu,p} = l_t\,N_p = 10{,}5 \times 60 = 630\ \text{cm} = 6{,}30\ \text{m}$$
$$l_{cu,s} = l_t\,N_s = 10{,}5 \times 10 = 105\ \text{cm} = 1{,}05\ \text{m}$$

Multiplicando pelo número de fios em paralelo, o comprimento total de fio 26 AWG a ser enrolado é
$3 \times 6{,}30 + 17 \times 1{,}05 = 18{,}9 + 17{,}9 = 36{,}8$ m.

### 1.3 Resistências

$$R = \frac{\rho\,l_t\,N}{n\,S_{cu}}$$

**Primário:**
$$R_p = \frac{2{,}266\times10^{-6} \times 630}{3 \times 0{,}001287}
= \frac{1{,}4276\times10^{-3}}{3{,}861\times10^{-3}} = 0{,}3697\ \Omega = 369{,}75\ \text{m}\Omega$$

**Secundário:**
$$R_s = \frac{2{,}266\times10^{-6} \times 105}{17 \times 0{,}001287}
= \frac{2{,}3793\times10^{-4}}{2{,}1879\times10^{-2}} = 0{,}01087\ \Omega = 10{,}87\ \text{m}\Omega$$

A razão entre as duas, $R_p/R_s = 34{,}0$, é próxima do quadrado da relação de transformação
($6^2 = 36$), como deve ser em um transformador com enrolamentos igualmente bem projetados. A
pequena diferença vem do arredondamento do número de fios em paralelo.

### 1.4 Perdas

$$P_{cu,p} = R_p\,I_{p(rms)}^2 = 0{,}3697 \times 1{,}4081^2 = 0{,}7332\ \text{W}$$
$$P_{cu,s} = R_s\,I_{s(rms)}^2 = 0{,}01087 \times 8{,}3872^2 = 0{,}7650\ \text{W}$$

$$\boxed{P_{cu} = 0{,}7332 + 0{,}7650 = 1{,}4981\ \text{W}}$$

**As duas perdas são praticamente iguais**, 0,733 W contra 0,765 W, uma diferença de 4 %. Não é
coincidência: é a assinatura do método do produto de áreas, que distribui a janela
proporcionalmente às correntes e às tensões de cada enrolamento e, com isso, iguala automaticamente
as densidades de corrente e as perdas específicas.

### 1.5 A ressalva sobre resistência em corrente alternada

O cálculo acima usa a resistência em corrente contínua. Em 100 kHz, dois efeitos a elevam:

**Efeito pelicular residual.** Foi controlado pela escolha do 26 AWG, cujo diâmetro (0,405 mm)
é ligeiramente inferior a $2\varepsilon$ (0,419 mm). Nessa condição $R_{ac}/R_{cc}$ fica próximo de
1,05 a 1,1 por filamento, valor pequeno mas não nulo.

**Efeito de proximidade.** É o dominante e não foi calculado. Os 17 fios do secundário, dispostos
em camadas dentro da janela, veem campos magnéticos muito diferentes conforme a posição, e as
camadas mais próximas do entreferro magnético entre primário e secundário conduzem
desproporcionalmente. Sem intercalamento, $F_R = R_{ac}/R_{cc}$ pode alcançar 2 a 3 em enrolamentos
de muitas camadas.

**Recomendações construtivas** que reduzem o efeito, e que devem constar da folha de execução do
transformador:

1. **Intercalar os enrolamentos** na sequência ½ primário – secundário – ½ primário. Esse arranjo
   reduz pela metade a força magnetomotriz máxima na janela e, com ela, aproximadamente pela
   metade o fator $F_R$;
2. **Torcer levemente** os fios em paralelo de cada enrolamento, aproximando o comportamento do fio
   Litz e forçando cada filamento a ocupar posições equivalentes;
3. **Limitar o número de camadas**, preferindo bobinar em camadas largas e rasas;
4. **Manter o intercalamento simétrico**, para não introduzir assimetria de dispersão entre as duas
   metades do primário.

Com essas medidas, um $F_R$ da ordem de 1,3 a 1,5 é realista, elevando $P_{cu}$ para
aproximadamente 2,0 a 2,2 W. Esse valor é usado como cenário pessimista na Seção 3.

## 2. Perdas no núcleo (passo 13)

### 2.1 Cálculo

$$P_{n\acute{u}cleo} = \Delta B^{2{,}4}\left(K_H f_s + K_E f_s^2\right)V_e$$

Com $f_s = 100$ kHz:
$$K_H f_s = 4\times10^{-5} \times 10^5 = 4{,}00, \qquad
K_E f_s^2 = 4\times10^{-10} \times 10^{10} = 4{,}00$$

**Na razão cíclica de operação** ($\Delta B = 0{,}1140$ T):

$$P_{n\acute{u}cleo} = (0{,}1140)^{2{,}4} \times 8{,}00 \times 23{,}30
= 5{,}448\times10^{-3} \times 186{,}4 = 1{,}0154\ \text{W}$$

**No pior caso** ($\Delta B = 0{,}1389$ T):

$$P_{n\acute{u}cleo,max} = (0{,}1389)^{2{,}4} \times 8{,}00 \times 23{,}30 = 1{,}6325\ \text{W}$$

### 2.2 Verificação contra o critério de densidade de perdas

$$\frac{P_{n\acute{u}cleo}}{V_e} = \frac{1{,}0154}{23{,}30} = 0{,}0436\ \text{W/cm}^3
= 43{,}6\ \text{mW/cm}^3 \;\le\; 100\ \text{mW/cm}^3 \quad\checkmark$$

$$\frac{P_{n\acute{u}cleo,max}}{V_e} = 70{,}1\ \text{mW/cm}^3 \;\le\; 100\ \text{mW/cm}^3 \quad\checkmark$$

**Mesmo no pior caso de razão cíclica, a densidade de perdas fica 30 % abaixo do critério de
McLyman.** Em massa, $1{,}0154/112 = 9{,}07$ mW/g, valor consistente com o patamar de 20 mW/g que o
catálogo Thornton indica para o IP12R.

### 2.3 Repartição entre os dois mecanismos

Como observado no documento 07, Seção 4.3, em 100 kHz os dois coeficientes se igualam:

| Mecanismo | Parcela | Valor |
|---|---|---|
| Histerese | $\Delta B^{2{,}4}K_Hf_sV_e$ | 0,5081 W (50 %) |
| Correntes parasitas | $\Delta B^{2{,}4}K_Ef_s^2V_e$ | 0,5081 W (50 %) |

Se a frequência fosse dobrada para 200 kHz, mantendo $\Delta B$, a histerese dobraria e as
correntes parasitas quadruplicariam, e a perda total no núcleo saltaria de 1,02 W para 5,08 W, um
fator de cinco. **É essa lei que estabelece o teto prático do ferrite Mn-Zn**, e ela deve ser
lembrada sempre que se cogitar elevar a frequência para reduzir o volume.

## 3. Balanço térmico (passo 14)

### 3.1 Perdas totais e rendimento

$$P_\Sigma = P_{cu} + P_{n\acute{u}cleo} = 1{,}4981 + 1{,}0154 = 2{,}5135\ \text{W}$$

$$\eta_{trafo} = \frac{P_o}{P_o + P_\Sigma} = \frac{500}{502{,}51} = 0{,}99500
\;\Longrightarrow\; \boxed{99{,}50\ \%}$$

A repartição é 59,6 % no cobre e 40,4 % no núcleo, próxima do ótimo teórico de 50/50, o que
confirma a escolha de $B_{ac}$ feita no documento 08.

**O rendimento medido de 99,50 % supera a hipótese de 98 % adotada no passo 1.** Essa é a direção
segura do erro: a hipótese conservadora superdimensionou $P_t$ em 1,5 %, e portanto o núcleo, o que
apenas acrescenta margem. Se o rendimento real tivesse ficado abaixo da hipótese, o núcleo estaria
subdimensionado e o cálculo precisaria ser refeito com o novo valor.

### 3.2 Resistência térmica e elevação de temperatura

$$R_t = 23\,(A_eA_w)^{-0{,}37} = 23 \times (3{,}768)^{-0{,}37}$$

$$(3{,}768)^{0{,}37} = e^{0{,}37\ln 3{,}768} = e^{0{,}37 \times 1{,}3266} = e^{0{,}4908} = 1{,}6335$$

$$R_t = \frac{23}{1{,}6335} = 14{,}08\ ^\circ\text{C/W}$$

$$\Delta T = R_t\,P_\Sigma = 14{,}08 \times 2{,}5135 = 35{,}4\ ^\circ\text{C}$$

$$T_{n\acute{u}cleo} = T_a + \Delta T = 40 + 35{,}4 = 75{,}4\ ^\circ\text{C}$$

$$\boxed{\Delta T = 35{,}4\ ^\circ\text{C} \le 40\ ^\circ\text{C} \quad\checkmark}$$

### 3.3 Cenários de verificação

| Cenário | $P_{cu}$ | $P_{núcleo}$ | $P_\Sigma$ | $\Delta T$ | $T_{núcleo}$ | Situação |
|---|---|---|---|---|---|---|
| **Nominal** ($D = 0{,}4103$, $F_R = 1$) | 1,498 W | 1,015 W | 2,514 W | 35,4 °C | 75,4 °C | ✓ |
| Pior caso de fluxo ($D = 0{,}5$) | 1,498 W | 1,633 W | 3,131 W | 44,1 °C | 84,1 °C | limite |
| Com efeito de proximidade ($F_R = 1{,}4$) | 2,097 W | 1,015 W | 3,112 W | 43,8 °C | 83,8 °C | limite |
| Combinado (pior caso + $F_R = 1{,}4$) | 2,097 W | 1,633 W | 3,730 W | 52,5 °C | 92,5 °C | requer ventilação |

**Leitura.** O projeto nominal tem 4,6 °C de folga sobre o critério. Cada um dos dois cenários
adversos, isoladamente, leva a temperatura a cerca de 84 °C, ainda perfeitamente seguro para o
IP12R, cuja temperatura de Curie é superior a 210 °C, e próximo do ponto de mínima perda do
material, que fica em torno de 90 °C para ferrites tipo R. Somente a combinação dos dois exigiria
ventilação forçada.

Vale a observação: os 92,5 °C do cenário combinado são a temperatura de um componente, não uma
falha. O isolamento do fio esmaltado classe 155 suporta 155 °C continuamente, e o carretel de
poliamida, mais. **O critério de 40 °C de elevação é uma diretriz de projeto, não um limite
físico**, e é bom saber a distância entre os dois.

### 3.4 Verificação da regulação

O documento 07, Seção 7, registrou o critério alternativo de McLyman, baseado na regulação:

$$\alpha \approx \frac{P_{cu}}{P_o}\times 100 = \frac{1{,}4981}{500}\times 100 = 0{,}30\ \%$$

A especificação do exemplo da apostila para o mesmo ponto de operação é $\alpha = 0{,}5$ %. **O
projeto atende com folga**, o que era esperado: com $J = 400$ A/cm² e perdas equilibradas, a queda
resistiva total é pequena.

## 4. Verificação final da ocupação da janela

Retomando o resultado do documento 09, passo 11, e detalhando as parcelas:

| Enrolamento | Espiras | Fios | Área isolada total | $K_u$ parcial |
|---|---|---|---|---|
| Primário | 60 | 3 × 26 AWG | 0,28854 cm² | 0,1838 |
| Secundário | 10 | 17 × 26 AWG | 0,27251 cm² | 0,1736 |
| **Total** | | | **0,56105 cm²** | **0,3574** |

Área da janela do carretel: $A_w = 1{,}57$ cm². Ocupação de cobre isolado: 35,7 %; espaço útil
consumido (referido a $K_u^{max} = 0{,}40$): **89,3 %**.

**Estimativa de camadas.** Um passo prático de verificação, ainda que aproximado: a largura útil de
bobinagem do carretel do NEE-42/21 é de aproximadamente 29 mm. Com fio 26 AWG isolado
($d \approx 0{,}45$ mm com esmalte), cabem cerca de 64 fios por camada.

- **Primário:** 60 espiras × 3 fios = 180 fios → 3 camadas;
- **Secundário:** 10 espiras × 17 fios = 170 fios → 3 camadas.

Seis camadas no total, mais isolação entre elas. Com o intercalamento recomendado
(1,5 camadas de primário / 3 de secundário / 1,5 de primário), a construção é perfeitamente
exequível dentro da altura de janela disponível.

## 5. Indutância e corrente de magnetização (passo 15)

Este passo verifica a hipótese H2 do documento 08.

### 5.1 Indutância de magnetização

O catálogo Thornton fornece $\Sigma l/A$ para cada núcleo, de onde

$$A_L = \frac{\mu_0\,\mu_i}{\sum l/A} = \frac{\mu_0\,\mu_i\,A_e}{l_e}$$

Para o NEE-42/21/20, com $\mu_i = 2100$, $A_e = 2{,}40$ cm² e $l_e = 9{,}70$ cm:

$$A_L = \frac{4\pi\times10^{-7} \times 2100 \times 2{,}40\times10^{-4}}{9{,}70\times10^{-2}}
= 6{,}53\times10^{-6}\ \text{H/esp}^2 = 6529\ \text{nH/esp}^2$$

$$L_m = A_L\,N_p^2 = 6{,}53\times10^{-6} \times 60^2 = 23{,}51\ \text{mH}$$

Conferência do método: aplicado ao NEE-42/21/15, para o qual o catálogo declara
$\Sigma l/A = 0{,}54$ mm⁻¹, a expressão dá $A_L = \mu_0\mu_i/(540) = 4887$ nH/esp², contra os
4100 nH/esp² máximos do catálogo, com concordância dentro da tolerância de ±25 % de $\mu_i$.

### 5.2 Corrente de magnetização

$$I_{mag,pico} = \frac{V_{in}\,D\,T}{L_m}
= \frac{400 \times 0{,}4103 \times 10\times10^{-6}}{23{,}51\times10^{-3}}
= \frac{1{,}6412\times10^{-3}}{2{,}351\times10^{-2}} = 0{,}0698\ \text{A} = 69{,}8\ \text{mA}$$

Comparando com o patamar de corrente refletida da carga:

$$\frac{I_{mag,pico}}{I_{p,patamar}} = \frac{0{,}0698}{1{,}5546} = 4{,}5\ \%$$

$$\boxed{\text{Hipótese H2 verificada: } I_{mag} = 4{,}5\ \% \text{ de } I_{carga}}$$

Abaixo de 5 %, a corrente de magnetização é seguramente desprezível no cálculo de perdas e de
correntes eficazes. Ela **não** é desprezível, porém, para dois outros efeitos:

**Perdas de comutação nas chaves.** No bloqueio, as chaves interrompem
$I_{p,patamar} + I_{mag,pico} = 1{,}62$ A, e não 1,55 A, o que representa 4,5 % a mais de energia
de comutação.

**Comutação suave.** A energia armazenada na indutância de magnetização,

$$E = \tfrac{1}{2}L_mI_{mag}^2 = \tfrac{1}{2} \times 23{,}51\times10^{-3} \times 0{,}0698^2
= 57{,}3\ \mu\text{J}$$

é a energia disponível para descarregar as capacitâncias de saída das chaves numa topologia de
comutação suave por deslocamento de fase (*phase-shift full-bridge*). Para referência, a energia
armazenada nas capacitâncias de um braço em 400 V é da ordem de
$\tfrac{1}{2}C_{o(er)}V^2 = \tfrac{1}{2} \times 100\ \text{pF} \times 400^2 = 8\ \mu$J, menor que
os 57,3 µJ disponíveis, o que indica que a comutação suave seria viável nesta topologia. É uma
observação de projeto, não um requisito deste trabalho.

### 5.3 Verificação do campo magnético associado

$$B_{mag,pico} = \frac{\mu_0\,\mu_i\,N_p\,I_{mag}}{l_e}
= \frac{4\pi\times10^{-7} \times 2100 \times 60 \times 0{,}0698}{9{,}70\times10^{-2}} = 0{,}114\ \text{T}$$

Este valor coincide, como deve, com o $\Delta B$ calculado por Faraday no passo 5, já que as duas
rotas descrevem o mesmo fenômeno, uma pela tensão aplicada e outra pela corrente que essa tensão
produz.
A coincidência é uma boa verificação cruzada de todo o encadeamento de cálculo.

## 6. Comparação com o exemplo de referência da apostila

Confrontando o resultado deste trabalho com o exemplo da Seção 1.6.5 da Apostila 01, que resolve o
**mesmo** ponto de operação com núcleo Magnetics:

| Grandeza | Apostila (Magnetics EE-75) | Este trabalho (Thornton NEE-42/21/20) |
|---|---|---|
| $B_{ac}$ adotado | 0,05 T | 0,07 T |
| $J$ adotado | 250 A/cm² | 400 A/cm² |
| $A_p$ requerido | 5,05 cm⁴ | 2,255 cm⁴ |
| $A_eA_w$ do núcleo | 9,49 cm⁴ | 3,768 cm⁴ |
| $A_e$ | 3,39 cm² | 2,40 cm² |
| $A_w$ | 2,80 cm² | 1,57 cm² |
| $N_p$ | 59 | 60 |
| $N_s$ | 10 | 10 |
| Fio | 26 AWG | 26 AWG |
| Fios em paralelo (prim./sec.) | 4 / 26 | 3 / 17 |
| $K_u$ final | 0,24 | 0,357 |
| Massa do núcleo | 179 g (uma peça) | 112 g (par) |

**Os números de espiras coincidem quase exatamente**, com 59 contra 60 no primário e 10 no
secundário, o que valida o encadeamento de cálculo: os dois projetos partem da mesma tensão e da
mesma frequência, e o produto $B_{ac} \cdot A_e$ resulta praticamente igual nos dois casos:
$0{,}05 \times 3{,}39 = 0{,}170$ contra $0{,}07 \times 2{,}40 = 0{,}168$.

A diferença está no aproveitamento. A apostila termina com $K_u = 0{,}24$ e ela própria observa que
"é possível usar um núcleo menor ao escolhido". Este trabalho, ao tratar $K_u$ como restrição e não
como constatação, chega a 0,357, **próximo do limite prático de 0,40 e com um núcleo de menos da
metade da massa.** É a diferença entre verificar depois e restringir durante.

## 7. Folha de execução do transformador

| Item | Especificação |
|---|---|
| **Núcleo** | Thornton NEE-42/21/20, material IP12R, par de peças, sem entreferro |
| **Carretel** | Correspondente ao NEE-42/21, $A_w = 1{,}57$ cm², $l_t = 10{,}5$ cm |
| **Primário** | 60 espiras, 3 fios 26 AWG em paralelo, levemente torcidos |
| **Secundário** | 10 espiras, 17 fios 26 AWG em paralelo, levemente torcidos |
| **Sequência de bobinagem** | ½ primário (30 esp.) – secundário (10 esp.) – ½ primário (30 esp.) |
| **Isolação** | Fita de poliéster entre enrolamentos e a cada camada; mínimo 3 voltas nas interfaces primário-secundário |
| **Fixação** | Fita de poliéster envolvendo o conjunto; verniz de impregnação opcional |
| **Terminais** | Primário nos pinos 1–2 do carretel; secundário nos pinos 5–6 |
| **Ensaio de recebimento** | $L_m$ (primário, secundário aberto) ≈ 23,5 mH ±25 %; $L_{disp}$ (primário, secundário em curto) ≤ 1 % de $L_m$; relação de espiras 6,00 ±1 % |

O ensaio de indutância de dispersão é o mais importante para verificar a qualidade da execução: um
valor acima de 1 % de $L_m$ indica intercalamento mal feito e resultará em sobretensões nas chaves
e perda de razão cíclica efetiva.

---

**Documento anterior:** [09. Dimensionamento passo a passo](09-dimensionamento-passo-a-passo.md)
**Próximo documento:** [11. Resumo consolidado e referências](11-resumo-consolidado-e-referencias.md)
