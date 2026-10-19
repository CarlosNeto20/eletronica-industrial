# Conclusões e referências

> Gerado por `artigo/fonte/exportar_markdown.py` a partir de `conteudo.py`. Para alterar o texto, edite `conteudo.py` e gere de novo. A numeração de seções, figuras, tabelas e equações é a do artigo.

## VIII. Conclusão

O carregador de 15 A baseado no Forward de duas chaves foi projetado, conferido e simulado. Todos os valores da planilha do professor foram reproduzidos, e as simulações no PLECS, com o controle analógico completo, repetem os três ensaios feitos por ele no PSIM: a tensão é regulada em 27 V diante de degraus de carga entre 20 % e 100 %, a corrente é limitada em 15 A mesmo com a saída em curto-circuito, e a recarga da bateria ocorre em corrente constante seguida de tensão constante. Os mesmos resultados foram obtidos com a rede em 264 V, o que mostra que o projeto atende a toda a faixa de tensão de entrada.

A topologia cumpre o que se esperava dela. A tensão sobre as chaves ficou grampeada na do barramento, 373 V no pior caso, o que permite usar MOSFETs de 500 V, e a desmagnetização do transformador se completa em um tempo igual ao de condução. Os esforços calculados concordam com os simulados dentro de 2 %, e os componentes comerciais escolhidos operam com folga. O retificador com filtro capacitivo confirmou a sua limitação: o fator de potência medido foi de 0,41 em 176 V e de 0,34 em 264 V, com corrente de pico de 30 A, quase o dobro da prevista pelo modelo de pulso retangular. A corrente eficaz no capacitor do barramento, de 6,2 A, justifica os dois capacitores em paralelo.

A conferência e a simulação trouxeram três observações que a planilha não registra. O ganho do compensador de corrente foi calculado com o valor do laço em 5 kHz, e não em 12,5 kHz, de modo que o cruzamento real fica acima do pretendido, embora com margem de fase adequada. A carga nominal coincide com o limite de corrente, o que deixa o carregador na fronteira entre as duas malhas e, por causa da saturação do compensador de tensão, eleva em um volt o pico de tensão na retirada de carga. Uma folga de 4 % no limite resolve o problema. Por fim, o diodo de bloqueio em série com a bateria sofre um surto de 256 A quando a saída é curto-circuitada, e deve ser dimensionado por essa corrente.

Como continuação, propõem-se o projeto físico do transformador e do indutor, a inclusão de partida suave e de um limitador da corrente de energização, e a substituição do retificador por um estágio com correção do fator de potência, que é a principal deficiência do carregador como está.

## Referências

[1] R. P. Torrico-Bascopé, Projeto de um Carregador de Baterias de 15 A Baseado no Conversor Forward de Duas Chaves. Planilha de projeto da disciplina de Eletrônica Industrial, Universidade Federal do Ceará, Fortaleza, 2026.

[2] R. P. Torrico-Bascopé, Mini-curso de Controle Básico para Conversores Estáticos, Parte IV, Anexo. Universidade Federal do Ceará, Fortaleza.

[3] Baterias Estacionárias Freedom, Catálogo Técnico.

[4] Y. S. Wong, W. G. Hurley e W. H. Wölfle, “Charge regimes for valve-regulated lead-acid batteries: Performance overview inclusive of temperature compensation,” Journal of Power Sources, 2008.

[5] M. H. Rashid, Power Electronics: Devices, Circuits, and Applications, 4th ed. Harlow: Pearson, 2014.

[6] I. Barbi, Projetos de Fontes Chaveadas, 3. ed. Florianópolis: Edição do Autor, 2015.

[7] R. W. Erickson e D. Maksimović, Fundamentals of Power Electronics, 3rd ed. Cham: Springer, 2020.

[8] H. D. Venable, “The K factor: A new mathematical tool for stability analysis and synthesis,” em Proc. Powercon 10, 1983.

[9] Texas Instruments, UC1525A, UC2525A, UC3525A Regulating Pulse Width Modulators. Folha de dados.

[10] Plexim GmbH, PLECS User Manual, versão 5.0. Zurique, 2025.

[11] TDK Electronics, Aluminum Electrolytic Capacitors: séries B43658 e B41821. Folhas de dados.

[12] Vishay Intertechnology, folhas de dados GBU8A a GBU8M, IRFP460, UF4001 a UF4007 e VS-MUR3020WT-N3.

[13] R. P. Torrico-Bascopé, Modelado y Control de Convertidores Estáticos. Notas de aula, Universidade Federal do Ceará, Fortaleza.
