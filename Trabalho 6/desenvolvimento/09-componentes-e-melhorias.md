# 09. Seleção preliminar de componentes e melhorias

Este arquivo reúne uma seleção preliminar de componentes e a avaliação das melhorias opcionais citadas no README. Toda a seleção é classe H: os componentes foram escolhidos pelos esforços calculados em [03](03-retificador-e-barramento.md), [04](04-inversor-e-filtro.md) e [06](06-conversor-cc-cc-elevador.md) e pelos valores medidos no PLECS em [08](08-resultados.md), e os dados de catálogo citados foram conferidos em páginas de distribuidores ou fabricantes em 09/11/2026. Nenhum deles foi ensaiado. Perdas, temperatura e montagem precisam de projeto térmico próprio antes de qualquer protótipo.

## 1. Retificador e barramento

**Ponte de entrada.** A planilha pede uma ponte de diodos lentos da Vishay. A família GBPC35 de 35 A atende com folga: a GBPC3510 tem 1000 V de tensão reversa repetitiva, 35 A médios, 400 A de surto não repetitivo e queda máxima de 1,1 V a 17,5 A. A tensão reversa de 373 V fica com fator de segurança de 2,7, adequado para absorver surtos da rede junto com um varistor na entrada. A corrente média total da ponte (cerca de 9,8 A) é pequena para o encapsulamento, mas os pulsos repetitivos e, principalmente, a corrente de recarga quando a rede retorna exigem dissipador e limitação de partida.

**Banco do barramento.** A planilha escolhe quatro EPCOS (TDK) B43501 de 470 µF/450 V. O código B43501A5477M tem ESR típica de 280 mΩ a 100 Hz e corrente de ondulação nominal de 2,7 A a 100 Hz e 85 °C, com fator 1,03 para 120 Hz e fator de temperatura 2,0 a 55 °C segundo a folha de dados da série. Quatro unidades suportam, portanto, cerca de 11 A a 85 °C ou 22 A a 55 °C. A corrente eficaz calculada no capacitor é de 21,1 A no pior caso (176 V, 2250 W), o que exige temperatura ambiente próxima de 55 °C ou um quinto e um sexto capacitor. Duas consequências se somam: a ESR do banco é cerca de 70 mΩ, e não os 50 mΩ adotados, e a tolerância de −20% reduz o vale para 204,5 V, abaixo dos 210 V do CC-CC. A recomendação preliminar é usar seis unidades (2820 µF), o que eleva o vale a 176 V, reduz a corrente por unidade para 3,5 A e devolve a margem para a transferência.

## 2. Inversor

**Interruptores.** A tensão de bloqueio é 373 V em regime e a corrente de pico chega a cerca de 81 A com fator de crista 3 (ou ao valor medido no PLECS com a carga do Anexo 01). Um MOSFET de superjunção de 650 V é a escolha natural. O IPW65R041CFD7 (Infineon CoolMOS CFD7, TO-247) tem 41 mΩ máximos a 10 V, 50 A contínuos a 25 °C e diodo intrínseco rápido, o que é importante em ponte completa com comutação dura. A resistência adotada na simulação (50 mΩ) corresponde a esse dispositivo aquecido. Com 13 A a 19 A eficazes por chave, as perdas de condução ficam entre 9 W e 18 W por chave a quente; as de comutação, não modeladas, exigem cálculo próprio com a energia de comutação da folha de dados. Para 3 kVA contínuos com carga não linear, a versão de 29 mΩ da mesma família dá mais folga.

**Filtro.** O capacitor de 60 µF em polipropileno metalizado de 250 Vca segue a planilha; ele precisa suportar 2,6 A a 60 Hz e a ondulação de 40 kHz (cerca de 1,5 A eficazes a 373 V). O indutor de 365,6 µH deve ser projetado para o pico da carga não linear sem saturar, o que leva a um núcleo de pó de ferro ou de ferrite com entreferro dimensionado para cerca de 80 A de pico e 26 A eficazes; o projeto do magnético não faz parte desta etapa.

## 3. Conversor CC-CC

**Chaves.** As chaves bloqueiam 70 V e conduzem, em média, metade da corrente da bateria (27 A a 28 A, com picos de cerca de 60 A). Um MOSFET de 150 V com resistência de alguns miliohms é adequado. O IRFP4568 (150 V, 5,9 mΩ máximos, 171 A, TO-247AC) atende eletricamente, mas consta como produto em fim de vida em distribuidores; um equivalente atual da mesma classe deve ser escolhido no momento da compra.

**Diodos D17 e D18.** Bloqueiam 140 V e entregam a corrente da etapa de uma chave aberta. O STTH6002CW (ST, dois diodos ultrarrápidos de 30 A e 200 V com catodo comum em TO-247, trr típico de 22 ns) encaixa diretamente na célula, porque D17 e D18 têm catodo comum no ponto médio entre C7 e C8.

**Ponte do secundário (D13 a D16).** Bloqueiam 70 V; diodos ultrarrápidos ou Schottky de 100 V a 150 V e corrente compatível com a corrente medida no secundário.

**Indutor e transformador.** Lb precisa de 39,2 µH com pico de cerca de 62 A e ondulação em 40 kHz; T_32 é um transformador de alta frequência de três enrolamentos com relação 1:1:1 e dispersão baixa, cujo projeto segue o método usado no Trabalho 1 da disciplina. Ambos ficam como pendência.

**Capacitores C7 e C8.** Os 10 µF do Anexo 01 só funcionam porque C4 está em paralelo com a pilha. Capacitores de filme de 100 V (C7) e 200 V (C8) com baixa ESR são adequados para a corrente pulsada de alta frequência.

## 4. Melhorias avaliadas

A tabela resume as melhorias citadas no README e outras que a auditoria e a simulação mostraram relevantes. Nenhuma delas foi implementada nos modelos principais, para não confundir com os resultados centrais do documento.

| Melhoria | Viabilidade neste trabalho | Relevância | Situação |
|---|---|---|---|
| Lógica de transferência com o CC-CC em espera | Implementada como hipótese ideal | Alta: evita drenar a bateria com a rede presente | Usada nos ensaios principais; o caso do PSIM é comparado |
| CC-CC em malha fechada com referência abaixo do vale do retificador | Média (controle de tensão do barramento e limitação de corrente da bateria) | Alta: elimina a dependência de D fixo e da tensão da bateria | Recomendada |
| Banco de seis capacitores no barramento | Trivial | Alta: margem de vale e corrente eficaz | Recomendada |
| Limitação da corrente de recarga no retorno da rede (NTC com relé de bypass ou pré-carga) | Simples | Alta, pelo pico medido no retorno | Recomendada |
| Controlador ressonante em 60 Hz (P + R) ou malha interna de corrente no indutor | Média | Média: reduz o erro de fase em regime e limita a corrente na carga não linear e em curto | Recomendada para versão futura |
| Polo do compensador abaixo de fs | Simples | Média: atenua a ondulação de 40 kHz no sinal modulante | Avaliada em [05](05-malha-de-tensao-do-inversor.md) |
| Estimativa de rendimento e perdas | Possível de forma preliminar com as folhas de dados | Média | O PLECS mede apenas perdas de condução e quedas dos diodos; o rendimento medido não inclui comutação |
| DHT da tensão de saída | Já calculada a partir dos CSVs | Alta | Em [08](08-resultados.md) |
| Tempo de transferência | Medido como continuidade da tensão eficaz por semiciclo | Alta | Em [08](08-resultados.md); detecção real não modelada |
| Chave estática de bypass, carregador de baterias, proteções | Fora do escopo do documento | Alta em produto real | Pendência |

## 5. Referências consultadas

As referências usadas no artigo foram conferidas quanto à existência, aos autores, ao veículo, ao ano e ao DOI ou repositório. Quando só os metadados foram consultados, isso é dito.

- S. B. Bekiarov e A. Emadi, Uninterruptible power supplies: classification, operation, dynamics, and control, APEC 2002, v. 1, p. 597-604, DOI 10.1109/APEC.2002.989305 (metadados e resumo).
- A. Emadi, A. Nasiri e S. B. Bekiarov, Uninterruptible Power Supplies and Active Filters, CRC Press, 2005 (folha de rosto e prefácio).
- IEC 62040-3:2011, Uninterruptible power systems, Part 3, com o anexo E normativo sobre a carga não linear de referência; a relação R1·C = 7,5/f para 5% de ondulação foi conferida no texto do projeto de norma de 2010 (sumário e notas).
- S. V. Araújo, R. P. Torrico-Bascopé e G. V. Torrico-Bascopé, Highly efficient high step-up converter for fuel-cell power processing based on three-state commutation cell, IEEE Trans. Ind. Electron., v. 57, n. 6, p. 1987-1997, 2010, DOI 10.1109/TIE.2009.2029521 (metadados e resumo).
- Y. J. A. Alcazar, D. S. Oliveira, F. L. Tofoli e R. P. Torrico-Bascopé, DC-DC nonisolated boost converter based on the three-state switching cell and voltage multiplier cells, IEEE Trans. Ind. Electron., v. 60, n. 10, p. 4438-4449, 2013 (metadados e resumo).
- C. G. C. Branco, R. P. Torrico-Bascopé, F. L. Tofoli e C. M. T. Cruz, Three-state switching cell (3SSC)-based non-isolated dc-dc boost-type converter with balanced output voltage and wide voltage conversion range, IET Power Electron., v. 11, n. 7, p. 1217-1223, 2018, DOI 10.1049/iet-pel.2017.0551 (repositório da UFC).
- C. E. A. Silva, R. P. T. Bascopé e D. S. Oliveira Jr., Proposal of a new high step-up converter for UPS applications, ISIE 2006, p. 1288-1292, DOI 10.1109/ISIE.2006.295658 (metadados e resumo).
- R. P. Torrico-Bascopé, D. S. Oliveira Jr., C. G. C. Branco e F. L. M. Antunes, A high frequency transformer isolation UPS system with 110V/220V input voltage, Eletrônica de Potência, v. 11, n. 3, 2006, DOI 10.18618/REP.2006.3.239247 (metadados e resumo).
- F. M. A. Linard, Sistema ininterrupto de energia de dupla conversão com integração do retificador e do inversor, dissertação de mestrado, UFC, 2009 (registro da BDTD e resumo; UPS de 3 kVA, 220 V de entrada e 110 V de saída).
- M. F. Apolinário, Nobreak dupla conversão monofásico isolado em alta frequência com tensão de entrada bivolt e potência de 1 kVA, baseado no conceito de circuito multi-portas, dissertação de mestrado, UFC, 2017 (repositório da UFC e resumo).
- Plexim, documentação do PLECS 5.0 instalada com o programa (consultada para sintaxe de blocos, ModelVars e interface RPC).

Pendências para o usuário: informar os dois livros citados nos slides da disciplina, para que sejam incluídos no artigo, e confirmar qual obra de Rashid a planilha usa na dedução de Lo.

Próximo arquivo: volta ao [índice](00-indice-do-projeto.md).
