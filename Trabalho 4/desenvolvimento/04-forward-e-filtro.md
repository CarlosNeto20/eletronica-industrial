# Forward de duas chaves e filtro

## Estados de operação

Q1 e Q2 ligam simultaneamente, aplicando Vbus ao primário. Dforward conduz e o indutor recebe nVbus−Vo, desprezadas perdas. No desligamento, os dois diodos de reset devolvem a energia magnetizante ao barramento e aplicam aproximadamente −Vbus ao primário; Dlivre mantém a corrente do indutor. Após desmagnetização, a tensão ideal do primário é zero. Não acionar as duas chaves em oposição de fase.

Pelo balanço volt-segundo no indutor em CCM:

\[
n=N_s/N_p=\frac{27}{225\times0,4}=0,3,\qquad D=\frac{V_o}{nV_{bus}}.
\]

D(225 V)=0,4 e D(373 V)=0,241287. A 20 V, D varia de 0,29630 a 0,17873. Como reset e excitação têm amplitudes iguais, tr≈ton e 2D<1. A versão final admite D≤0,45 para compensar perdas, reservando ao menos 10% do período sem excitação/reset, no modelo ideal. Esse limite é uma revisão do D=0,4 de projeto, não uma demonstração de que 0,4 atende a todas as perdas.

Com o diodo adicional de bloqueio, Rcu=20 mΩ, shunt=10 mΩ e Ron=5 mΩ por diodo de saída, estimativa em 15 A: tensão requerida ≈27+2×0,7+15×(0,02+0,01+0,005+0,005)=29,0 V. A 225 V, D≈29/(0,3×225)=0,4296, antes da pequena queda primária. Com limite 0,4, a especificação não seria atingida nesse ponto.

## Ondulação e capacitância

Para 27 V e pior tensão alta:

\[
L_o=\frac{V_o(1-D_{min})}{f_s\Delta I_L}
=\frac{27(1-0,241287)}{50000\times3}=136,568\ \mu H.
\]

Adota-se 136,6 µH no PLECS, como no esquema-base. A corrente de pico ideal é 16,5 A e eficaz √(15²+3²/12)=15,025 A. Em 20% de carga, Io=3 A>ΔIL/2≈1,5 A, mantendo CCM ideal. Na cauda de recarga há DCM; as funções de transferência CCM deixam de descrevê-la.

Cmin=ΔIL/(8fsΔVo)=3/(8×50000×0,27)=27,778 µF. Uma cota conservadora, somando parcelas capacitiva e resistiva, é ΔVo≤ΔIL[ESR+1/(8fsC)]. Os máximos das parcelas não precisam ser simultâneos; a soma é critério conservador de seleção, não identidade exata da forma de onda.

Com 2200 µF/0,11 Ω: ΔVo≤0,33341 Vpp, maior que 0,27 V. Com 2×2200 µF/50 V em paralelo: C=4400 µF, ESR=0,055 Ω e ΔVo≤0,16670 Vpp. A capacitância de 4400 µF foi escolhida principalmente para reduzir a ESR em paralelo e sustentar transientes. A energia armazenada a 27 V é 0,5CVo²=1,6038 J.

O catálogo B41821F6228M*** informa ESR máxima a 120 Hz, 20 °C. O valor constante em 50 kHz é hipótese conservadora de modelo, não uma curva de impedância medida. A corrente triangular eficaz no banco é ΔIL/(2√3)=0,8660 A, ≈0,4330 A por capacitor, inferior ao valor nominal de catálogo de 1,98 A por unidade a 120 Hz/85 °C. Transientes de carga e curto exigem análise separada.

## Esforços de primeira ordem

Cada MOSFET bloqueia aproximadamente Vbus, ou até 373,35 V, sem sobretensão parasita. Corrente de condução ≈nIL+Im; valor de pico da carga ≈4,95 A mais magnetização. Corrente eficaz de cada MOSFET ≈n√[D(Io²+ΔIL²/12)], cerca de 2,85 A a D=0,4. A potência I²Ron é estimativa de condução; não inclui Eon/Eoff e capacitâncias.

Dforward: corrente média D Io (3,62–6 A no ideal), eficaz √[D(Io²+ΔIL²/12)]. Dlivre: média (1−D)Io (9–11,38 A) e eficaz √[(1−D)(Io²+ΔIL²/12)]. Tensão reversa ideal de ambos até nVbus≈112 V. Classe sugerida ≥200 V, corrente ≥25–30 A e dissipação dimensionada. Dbloqueio conduz toda a corrente média e dissipa pelo menos 0,7×15=10,5 W com o Vf simplificado. Ele impede descarga da bateria de volta ao estágio; não impede a descarga do capacitor de saída num curto.

Um curto de 1 mΩ com o banco inicialmente a 27 V pode produzir corrente inicial aproximadamente 27/(0,055+0,001)=482 A, limitada pela ESR idealizada e impedâncias da malha. A limitação de 15 A refere-se ao indutor/conversor; não elimina o pulso do capacitor. Medir e discutir esse pulso separadamente. O circuito funcional não é uma especificação de interrupção segura de curto em hardware.
