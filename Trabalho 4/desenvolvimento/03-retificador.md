# Ponte retificadora e filtro capacitivo

## Especificações e energia

Pout=27 V×15 A=405 W. Orçamento Pin=Pout/0,90=450 W. Rede 220 Vrms nominal, 176–264 Vrms e 60 Hz. A ondulação de linha é a 120 Hz.

Na menor rede, Vp=√2×176=248,9016 V. O professor reserva ΔV=0,1Vp=24,8902 V, resultando Vmin=224,0114 V, sem quedas da ponte. θ=acos(Vmin/Vp)=acos(0,9)=0,451027 rad. O intervalo de reposição aproximado é tc=θ/(2π60)=1,19639 ms.

Durante descarga com potência constante, d(Cv²/2)/dt=−P. Logo:

\[
C_{in}=\frac{P(\pi-\theta)}{\pi f_r(V_p^2-V_{min}^2)}
=\frac{450(\pi-0,451027)}{\pi\,60(248,9016^2-224,0114^2)}
=545,69\ \mu F.
\]

Dimensão: W/[Hz V²]=J/V²=F. Seleção F: dois 470 µF/450 V em paralelo, 940 µF. Uma tolerância −20% fornece 752 µF, ainda acima do mínimo ideal. A tensão máxima da rede é √2×264=373,35 V; 450 V é classe de tensão, não proteção contra surtos.

## Esforços aproximados

Vmed=(248,9016+224,0114)/2=236,4565 V; Io=450/236,4565=1,90310 A; Req=Vmed²/450=124,248 Ω. Aproximando corrente de recarga por pulso retangular, Ipk=Ioπ/θ=13,2559 A. Cada diodo conduz um pulso por período de rede:

\[
I_{D,av}=I_o/2=0,95155 A,\quad I_{D,rms}=I_{pk}\sqrt{\theta/(2\pi)}=3,55157 A.
\]

\[
I_{C,rms}=\sqrt{I_o(I_{pk}-I_o)}=4,64817 A.
\]

Esses números são do modelo retangular no ponto de projeto original; não representam os picos de carga inicial e não se transferem sem revisão ao banco de 940 µF. Capacitância maior estreita a condução em certas condições e pode elevar o esforço eficaz. Exigir que a soma das capacidades de corrente dos dois capacitores cubra a corrente efetivamente medida, com temperatura e frequência corretas. A especificação nominal mínima derivada é 2,324 A por capacitor se houver compartilhamento ideal; a seleção de código comercial de 450 V depende da confirmação de catálogo e do ensaio. Não declarar aprovados quaisquer capacitores de 470 µF apenas por sua capacitância.

## Modelo PLECS e fator de potência

A ponte usa quatro diodos com Vf=0,7 V e Ron=10 mΩ. Impedância explícita de rede H: Rline=0,5 Ω e Lline=100 µH. Não é uma medição da instalação. Capacitor do barramento pré-carregado a √2Vrms−1,4 V, senoide iniciada no pico, para separar o ensaio de regulação do inrush. Não se valida partida a frio do retificador com essa condição inicial.

O capacitor entrega potência variável ao Forward comutado. Extraem-se Vbus, Irede e sinais de entrada. Em um número inteiro de períodos de rede, calcular P=integral(v i)/T, S=Vrms Irms, FP=P/S; não usar somente cos φ. O professor afirma FP<0,5 sem detalhar a impedância da fonte; a comparação efetivamente executada está em 08-resultados.md, sem impor tal valor.

Ponte proposta: classe ≥800 V, corrente média de saída ≥10 A, com verificação de IFSM, I²t e dissipação em projeto físico. Prever fusível, limitação de inrush, descarga do barramento e filtro EMI em implementação posterior. Esses elementos não são contabilizados como simulados no modelo funcional.
