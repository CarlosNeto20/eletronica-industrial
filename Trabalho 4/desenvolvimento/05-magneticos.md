# Transformador e indutor de saída

O documento fornece n=0,3 e a figura 14 indica Lm=20 mH, mas não dimensiona o núcleo. Completa-se aqui o projeto eletromagnético preliminar, com verificação de fluxo, janela e cobre. Perdas AC, dispersão, isolação e temperatura precisam de validação física.

## Transformador

Seleção fundamentada em catálogo: ETD59/31/22 N87, duas metades B66397G0000X187, carretel B66398W1024T001 e duas presilhas B66398A2000X000. TDK: Ae=Amin=368 mm²; AL=5300 nH (+30/−20%); janela AN=365,6 mm²; comprimento médio de espira 106,1 mm. Fonte: <https://www.tdk-electronics.tdk.com/inf/80/db/fer/etd_59_31_22.pdf>, outubro de 2024.

Para suportar o transiente extremo Vbus=373 V e Dlim=0,45 com ΔB≤0,18 T:

Np,min = 373×0,45/(50000×368e−6×0,18) = 50,68 espiras.

Adotam-se Np=60 e Ns=18, n=0,3000 exato. ΔBtrans=0,15204 T. Em regime ideal VbusD=Vo/n=90 V, ΔB=0,08152 T. O reset por dois diodos dispensa enrolamento adicional; seu tempo aproximado é ton e há margem de 10% do período no limite de duty.

Lm=AL Np²=5300e−9×60²=19,08 mH, próxima dos 20 mH do esquema-base. A faixa de tolerância é 15,264–24,804 mH. No pior limite, ΔIm=373×0,45/(50000×15,264e−3)=0,2199 A. O modelo usa Lm nominal e magnetização linear. Não incorpora histerese, dispersão ou remanência; ausência de saturação na simulação linear não comprova o projeto. A verificação do fluxo é analítica.

Correntes eficazes conservadoras a D=0,45: Ip,carga≈0,3×15,025×√0,45=3,024 A; Is≈15,025√0,45=10,079 A. Reserva-se seção do primário ≥0,80 mm² para a magnetização. Proposta: primário 10 fios de diâmetro 0,32 mm em paralelo, Ap=0,8042 mm²; secundário 33 fios de 0,32 mm, As=2,6541 mm². Densidades de corrente aproximadas 3,8 e 3,8 A/mm². São feixes em paralelo a transpor; não supor que paralelismo simples elimine proximidade.

A profundidade pelicular no cobre, δ=√[ρ/(πfµ0)], com ρ=1,724e−8 Ωm e f=50 kHz, é 0,296 mm a 20 °C; o raio do fio é 0,16 mm. A ocupação geométrica de cobre é 60Ap+18As=96,02 mm², 26,26% da janela. Critério ku≤0,35 deixa cerca de 32 mm² adicionais dentro do orçamento para dispersão geométrica; isolação, margens laterais e espessuras reais do esmalte precisam ser desenhadas e medidas. Recomenda-se 30 espiras primárias, isolação, 18 secundárias, isolação, 30 primárias em série, com polaridades e barreira dielétrica definidas no desenho físico.

Rp,20≈ρ(60×0,1061)/Ap=0,1365 Ω; Rs,20≈ρ(18×0,1061)/As=0,01241 Ω. Perda CC estimada no pior duty ≈Ip²Rp+Is²Rs≈2,51 W, sem magnetizante, terminais e perdas AC. A 100 °C, o fator resistivo aproximado 1+0,00393×80=1,314 aumenta essa parcela para ≈3,30 W. O catálogo fornece perdas de núcleo em pontos específicos; não se extrapola a indicação a 100 kHz/100 mT como resultado em 50 kHz com fluxo unipolar. Deve-se obter a curva de material e integrar perdas adequadas à forma de onda, ou medir calorimetricamente.

## Indutor

Energia ideal: W=LIpk²/2=136,6e−6×16,5²/2=18,595 mJ. Seleção preliminar: E65/32/27DG N87 AL=100 nH ±10%, conjunto B66387Q0100K187 com carretel B66388B1000T001. Fonte: <https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_65_32_27_dg.pdf>. Ae=535 mm², Amin=529 mm², janela=426 mm² e comprimento médio de espira=188 mm. O carretel B66388B requer um conjunto; a alternativa A2000 requer dois e não é a escolhida.

N=√(136,6 µH/100 nH)=36,96, adotar 37 espiras, Lnom=136,9 µH. Para correspondência com o documento, a simulação usa 136,6 µH; diferença nominal de 0,22%, muito menor que a tolerância. Em 20 A, B≈LI/(NAmin)=0,1399 T. Considerando L +10%, B≈0,1539 T, ainda abaixo do critério de 0,20 T. A curva AL versus polarização e temperatura deve confirmar a retenção de indutância; o cálculo linear não substitui essa curva.

Usar 48 fios de 0,32 mm em paralelo: Acu=3,8604 mm², J≈3,89 A/mm² a 15,025 A. Ocupação N Acu/426=33,53%, abaixo de ku=0,35, mas com margem estreita para o método de enrolamento; conferir desenho e isolação. Rdc,20≈ρ×37×0,188/Acu=31,06 mΩ, maior que os 20 mΩ simplificados do circuito. A perda CC estimada é 7,01 W a 20 °C, ≈9,22 W a 100 °C. Portanto o modelo funcional não deve sustentar uma afirmação térmica baseada em Rcu=20 mΩ. Deve-se aumentar cobre/janela ou aceitar e dissipar essa perda no protótipo. O entreferro distribuído reduz concentração de fluxo em um único gap; não foi substituído por um gap arbitrário no núcleo sem entreferro.

## Estado do projeto magnético

Há escolha de núcleos, espiras, condutores, fluxo, tolerância e verificação de ocupação. A simulação usa transformador ideal com Lm e indutor linear, com perdas agregadas assumidas. O projeto eletromagnético preliminar é reproduzível; a aprovação de fabricação continua dependente de bobinagem, isolamento, perdas AC, curva de polarização e ensaio térmico, que não fazem parte das medições de simulação apresentadas.


O ensaio de curto efetivamente executado atingiu IL=20,991 A. Recalculando com 136,9 µH, 37 espiras e Amin=529 mm²: B≈0,1468 T nominal e 0,1615 T com L +10%. Essa extensão supera o ponto inicial de 20 A e preserva o critério analítico de 0,20 T; continua sem representar ensaio de saturação.
