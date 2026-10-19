# Componentes de controle e melhorias opcionais

## Lista para reprodução funcional

| Elemento | Valor do modelo | Realização preliminar |
|---|---|---|
| Sensor de tensão | Hv=2,5/27 | Divisor 98 kΩ/10 kΩ; resistores de precisão, filtro a dimensionar |
| Sensor de corrente | 10 mΩ e ganho 16,6667 | Shunt ≥5 W, conexão Kelvin; 2,25 W CC em 15 A |
| Amplificador diferencial | 16,6667 | Pares 10 kΩ/166,667 kΩ, rede casada; verificar modo comum |
| Referência de tensão | 2,5 V | Referência de precisão e buffer; não usar saída de 5,1 V como 2,5 V diretamente |
| Referência de corrente | 0–2,5 V | Ajuste Iref=6Vrefi, com soft-start |
| Compensador de tensão | 10 kΩ; 79,2299 kΩ; 7,55294 nF; 86,4589 pF | Candidatos comerciais 10 kΩ; 78,7 kΩ; 7,5 nF; 82 pF: revalidar margem após arredondar |
| Compensador de corrente | 10 kΩ; 5,09002 kΩ; 27,3992 nF; 1,50577 nF | Candidatos 10 kΩ; 5,11 kΩ; 27 nF; 1,5 nF: revalidar |
| Seletor mínimo | min(uv,ui) com rastreamento | Diodos/op-amps ou lógica equivalente; quedas e saturação não são automaticamente iguais ao C-Script |
| PWM | Triangular 0–2,1 V/50 kHz | Modelo funcional; não é macromodelo do UC3525A |
| Chaves | 2 MOSFETs, Ron=0,15 Ω | Classe ≥600 V e ≥10 A; escolher por perdas e SOA, não somente corrente de catálogo |
| Diodos de saída | Vf=0,7 V/Ron=5 mΩ | Classe ≥200 V e ≥25–30 A, dissipação e recuperação a validar |
| Banco de saída | 2×2200 µF/50 V | B41821F6228M*** como referência documentada; ESR total assumida 55 mΩ |

A lista distingue valor simulado de sugestão de compra. Nenhum componente físico ou placa foi ensaiado. Alimentações auxiliares, driver isolado de gate, proteção de pico ciclo a ciclo e isolação da realimentação precisam integrar o circuito executivo.

## UC3525A

O catálogo TI SLUS191D informa duas saídas alternadas e oscilador com fosc≈1/[CT(0,7RT+3RD)]. Para usar uma saída alternada a 50 kHz, o oscilador trabalha em 100 kHz. Com CT=1 nF e RD=100 Ω, RT≈13,857 kΩ. Os dois MOSFETs do Forward devem receber o mesmo pulso via drivers adequados: as saídas A e B do CI não podem alimentar Q1 e Q2 diretamente em alternância. Também não se deve colocar saídas totem-pole em paralelo diretamente.

Uma arquitetura viável usa uma das saídas a 50 kHz, fan-out para dois canais isolados, supervisão de duty/reset e alimentação flutuante do canal superior. Outra utiliza lógica combinadora e limitação de duty compatível, mas precisa ser redesenhada para a frequência correta. O datasheet fornece faixa de rampa, limiares, atrasos e máximo duty que não são representados pelo simples ganho 1/2,1. O amplificador interno também não é ideal. Por isso o modelo funcional não é apresentado como esquema UC3525A pronto para placa.

## Avaliação das cinco sugestões

1. **Outro conversor isolado:** não incorporado ao núcleo da entrega, pois mudaria topologia, ganho, magnetização e validação. Como extensão, meia ponte ideal tem Vo≈(Ns/Np)(Vbus/2)D quando D representa a soma dos dois pulsos e cada primário recebe Vbus/2; documentar a convenção de duty antes de reutilizar equações.
2. **Retificador de quatro diodos:** incorporado nos três modelos principais. O dimensionamento e o teste em três tensões de rede evitam tratá-lo como barramento CC fixo.
3. **Circuito com UC3525A para PCB:** avaliação de arquitetura e temporização fornecida; esquema executivo e PCB ficam futuros. Não há validação de driver, fontes auxiliares ou proteção que justifique declarar a placa pronta.
4. **Lista de componentes de controle:** incorporada, separando valores exatos da simulação e valores comerciais que exigem revalidação.
5. **Cinco períodos de PWM:** extração realizada de 100 µs dos dados efetivamente executados, junto a comando, portadora e gate. Cinco períodos revelam o comportamento local do modulador, mas não demonstram isoladamente estabilidade de baixa frequência.

## Bateria e alcance

O modelo E=20 V em série com Rbat=10 mΩ e Cbat=0,4 F é uma emulação acelerada, não uma bateria eletroquímica calibrada. O equivalente coulômbico para 150 Ah sobre 7 V seria C=150×3600/7=77142,86 F, cerca de 192857 vezes maior. A escala temporal comprimida não representa tempo real, SOC, eficiência coulômbica ou envelhecimento. Corrente a 0,1C: 0,7 A para 7 Ah e 15 A para 150 Ah. A referência deve ser ajustada à bateria conectada. 27 V corresponde a 2,25 V/célula num banco de 12 células; não universalizar o valor como tensão de equalização. A configuração correta depende do fabricante, temperatura e uso cíclico/flutuação.
