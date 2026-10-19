# Modelagem, compensadores e estabilidade

## Planta média em CCM

Sejam L=136,6 µH, C a capacitância, r a ESR e R a carga resistiva. Pelo balanço de corrente no nó de saída, impedância Z(s)=R(1+sCr)/[1+sC(R+r)]. Da tensão média aplicada ao indutor, Gi(s)=nVbus/[sL+Z(s)] e Gv(s)=Gi(s)Z(s). Portanto:

\[
D_p(s)=LC(1+r/R)s^2+(L/R+Cr)s+1,
\]
\[
G_v(s)=nV_{bus}\frac{1+sCr}{D_p(s)},\qquad
G_i(s)=\frac{nV_{bus}}R\frac{1+sC(R+r)}{D_p(s)}.
\]

Gv tem unidades V/duty; Gi, A/duty. O denominador é adimensional. DCR, shunt e quedas de diodo são desprezados nesta reconstrução para comparabilidade com o professor; estão explicitados no modelo comutado. A equação de Gi deixa de corresponder à carga quando a saída é ligada à bateria de baixa impedância; por isso as margens resistivas não provam estabilidade de recarga ou curto.

Para C=2200 µF, r=0,11 Ω e R=1,8 Ω: fLC≈290,32 Hz (diferença de arredondamento frente a 290,358 do PDF), fn=1/[2π√(LC(1+r/R))]≈281,8 Hz; zero de tensão fzv=1/(2πCr)=657,665 Hz; zero de corrente fzi=1/[2πC(R+r)]≈37,88 Hz. A expressão da página 15 repete o zero de tensão, mas Gi tem outro zero.

Sensores: Hv=2,5/27=0,0925926 V/V; Hi=Rsh Kdif=0,01×16,6666667=1/6 V/A. A referência de corrente Vrefi=Iref/6 varia de 0 a 2,5 V. Ganho do PWM Fm=1/2,1 V⁻¹. Laços: Tv=CvFmHvGv e Ti=CiFmHiGi. São malhas seletoras CC/CV, não duas malhas em cascata nem reguladores simultaneamente dominantes.

## Síntese tipo II

\[
C_x(s)=\frac{1+sR_2C_1}{R_1s(C_1+C_2+sR_2C_1C_2)}
=\frac{K_i(1+s/\omega_z)}{s(1+s/\omega_p)}.
\]

No cruzamento desejado fc, calcula-se p=arg(GFmH), G=1/|GFmH|, avanço α=MF−p−90°. Se 0<α<90°, K=tan[(α+90°)/2], fz=fc/K e fp=fcK. Com R1=10 kΩ, C2=1/(2πfcGKR1), C1=C2(K²−1), R2=K/(2πfcC1). Não aplicar valor absoluto ao ganho em dB indiscriminadamente: a função inversa precisa atenuar se a planta tiver ganho maior que um.

## Reconstrução dos valores publicados

Tensão: R1=10 kΩ, R2=86,88 kΩ, C1=1,722 nF, C2=81,65 pF. Com os valores arredondados e Vbus=373 V, fc≈4999 Hz e MF≈60,306°. A análise mostra cruzamentos de fase −180° em baixa frequência, com módulos acima de um. Assim, a afirmação genérica MG=infinito não é correta para esse laço: todas as interseções e os polos fechados estão no JSON. Margens de ganho negativas nesses cruzamentos descrevem estabilidade condicional à redução de ganho; não se deve inferir instabilidade apenas por uma margem escalar sem analisar o polinômio fechado.

Corrente: R1=10 kΩ, R2=22,39 kΩ, C1=2,104 nF, C2=165,8 pF. Na planta original, |GFmHi| em 5 kHz é +6,34067 dB, enquanto em 12,5 kHz é −1,63786 dB. Portanto G em 12,5 kHz deveria ser 10^(1,63786/20)≈1,2075. Os componentes publicados cruzam em ≈19995 Hz, com MF≈57,376°. A margem calculada em 12,5 kHz não é a margem real, pois nessa frequência o módulo não é unitário.

## Projeto revisado

Com o banco C=4400 µF/r=0,055 Ω, preserva-se Cr, mas muda o denominador. Adotam-se fc,v=2500 Hz e fc,i=5000 Hz com MF contínua alvo de 65°. Os componentes exatos, usados para evitar ambiguidade de arredondamento, são:

| Malha | R1 | R2 | C1 | C2 | Ki | Kp | wp |
|---|---:|---:|---:|---:|---:|---:|---:|
| Tensão | 10 kΩ | 79,2299 kΩ | 7,55294 nF | 86,4589 pF | 13090,039 s⁻¹ | 7,74466 | 147653,789 rad/s |
| Corrente | 10 kΩ | 5,09002 kΩ | 27,3992 nF | 1,50577 nF | 3459,617 s⁻¹ | 0,457352 | 137643,762 rad/s |

Aqui Ki=1/[R1(C1+C2)] e Kp=Ki(1/wz−1/wp). Realização por estados: xdot=Ki e; zdot=wp(e−z); u=x+Kp z. Seu ganho é exatamente o tipo II acima. As constantes do modelo são geradas do JSON, não copiadas manualmente desta tabela.

## Seletor e anti-windup

O modulador recebe u=sat(min(uv,ui),0,2,1Dlim), com Dlim=0,45. Acrescenta-se aos estados integrais 30000(u−ux) s⁻¹, permitindo rastreamento do controlador inativo e da saturação. Tal termo é nulo no regulador dominante não saturado; não altera sua função linear nominal. Ele modifica a transição entre malhas e deve ser verificado no circuito comutado. A referência de corrente sobe linearmente em 5 ms para evitar degrau integral na partida funcional. O bloco C-Script implementa só o controle; as leis de circuito e os estados de potência são resolvidos pelo PLECS.

## Margens e validade

O script varre 225, 310 e 373 V e R=1,8/9 Ω. Para a revisão, os cruzamentos variam aproximadamente de 1,61–2,56 kHz na tensão e 3,18–5,00 kHz na corrente. MF nominal é 65° em ambas. Uma análise de sensibilidade com atraso hipotético Ts/2 subtrai 180fc/fs graus: 9° na tensão e 18° na corrente, resultando 56° e 47°. Isto não é uma margem medida no PWM natural: é uma verificação de sensibilidade. O original de corrente perderia cerca de 72° em 20 kHz sob a mesma hipótese.

`calculos.py` salva Bodes com frequência, ganho e fase de planta, compensador e laço, encontra todas as passagens 0 dB/−180° e calcula os polos do denominador fechado. Polos com parte real negativa validam somente o modelo linear resistivo. A estabilidade com saturação, DCM, bateria, curto e comutação deve ser observada nos ensaios, sem confundir ausência de oscilação em uma janela com prova universal.
