# 09. Conclusões Gerais e Referências

Este documento preenche as seções 5 (**ESCREVER**) e 6 (**LISTAR**) do enunciado.

## 1. Conclusões gerais (enunciado, seção 5)

Foram analisados quatro conversores CC-CC isolados, o Forward de uma chave, a ponte completa, o
push-pull alimentado em corrente e o Flyback de uma chave, e cada um foi comparado com o conversor
não isolado equivalente, referido ao secundário do transformador, por meio de degraus de carga de
20 % para 100 % e de 100 % para 20 %, simulados no PLECS.

**A equivalência dinâmica foi verificada nos quatro casos.** As tensões e correntes de saída do
conversor isolado e do equivalente coincidem em regime e durante todo o transitório, com erro RMS
máximo de 0,09 % e erro instantâneo máximo de 0,78 %. No Forward e no Flyback, nos modos contínuo e
descontínuo, as respostas são idênticas; na ponte completa e no push-pull a pequena diferença
existente se deve à corrente magnetizante do transformador, que circula pelo retificador do circuito
isolado e não tem correspondente no equivalente. Os valores de vale e pico de tensão obtidos
reproduzem os resultados do professor no PSIM com diferença de 1 a 2 V.

**Os equivalentes seguem três regras gerais.** A fonte é refletida pela relação de espiras
($V_{i,eq} = aV_i$), uma indutância do primário pelo seu quadrado ($L_{eq} = a^2L$), e as topologias
que excitam o transformador nos dois semiciclos (ponte completa e push-pull) têm equivalentes que
comutam no dobro da frequência, com razão cíclica efetiva $2D$ e $2D-1$, respectivamente. O Forward
e a ponte completa são equivalentes ao Buck, o push-pull alimentado em corrente ao Boost e o Flyback
ao Buck-Boost.

**Consequência para o controle.** Como a planta vista da saída é a mesma, os modelos médios e as
funções de transferência dos conversores básicos podem ser usados diretamente no projeto dos
controladores dos conversores isolados, bastando substituir $V_i$, $L$, $D$ e $f_s$ pelos valores
equivalentes. Isso justifica a proposta do enunciado de levantar as funções de transferência sobre
o conversor não isolado.

**Limites da equivalência.** O equivalente não representa o que existe apenas do lado do primário:
a corrente magnetizante e o reset do núcleo, as restrições de razão cíclica que eles impõem
($D \le 0{,}5$ no Forward, $D < 0{,}5$ na ponte, $D > 0{,}5$ no push-pull), os esforços de tensão
nas chaves ($2V_i$ no Forward, $2V_o/a$ no push-pull, $V_i + V_o/a$ no Flyback) e os efeitos da
dispersão, como a perda de razão cíclica e os picos de tensão que exigem grampeadores. O
dimensionamento de semicondutores e magnéticos continua exigindo o circuito isolado.

**Modo de condução.** O Flyback mostrou a diferença qualitativa entre os modos. Em MCD a tensão
depende da carga (127 V a 20 % contra 57 V a 100 %, em malha aberta), a resposta é de primeira
ordem, sem sobressinal, com constante de tempo próxima de $R_oC_o/2$, e a tensão sobre a chave chega
a 514 V com carga leve. Em MCC a tensão é independente da carga e a resposta é oscilatória, como nos
demais conversores. Nos dois modos, porém, a equivalência com o Buck-Boost é exata.

**Comparação entre as topologias.** Para a mesma função, as topologias trocam simplicidade por
aproveitamento do transformador e dos semicondutores: o Flyback usa um único semicondutor comandado
e nenhum indutor de filtro, mas processa toda a energia no núcleo e se limita a potências baixas; o
Forward acrescenta o filtro LC e o enrolamento de desmagnetização e suporta $2V_i$ na chave; a ponte
completa usa quatro chaves submetidas apenas a $V_i$ e excita o núcleo nos dois sentidos, o que a
torna adequada a potências elevadas; e o push-pull alimentado em corrente eleva a tensão com
corrente de entrada contínua, ao custo de chaves com o triplo da tensão de entrada e da necessidade
de sobreposição dos comandos.

**Sobre a ferramenta.** Todas as simulações, que no material de referência foram feitas no PSIM,
foram refeitas no PLECS, com resultados concordantes. Os modelos foram gerados por um script que
descreve os circuitos e confere suas ligações, o que torna o trabalho reprodutível e facilita
variações de parâmetros.

## 2. Referências (enunciado, seção 6)

Formato IEEE, na ordem sugerida para citação no artigo.

[1] R. P. Torrico-Bascopé, "Análise de conversores CC-CC isolados e comparação com os
equivalentes (Trabalho 2)", notas da disciplina Eletrônica Industrial, Departamento de Engenharia
Elétrica, Universidade Federal do Ceará, Fortaleza, set. 2026.

[2] R. W. Erickson e D. Maksimović, *Fundamentals of Power Electronics*, 3. ed. Cham, Suíça:
Springer, 2020.

[3] N. Mohan, T. M. Undeland e W. P. Robbins, *Power Electronics: Converters, Applications, and
Design*, 3. ed. Hoboken, NJ, EUA: Wiley, 2003.

[4] I. Barbi, *Projetos de Fontes Chaveadas*, 3. ed. Florianópolis: Edição do Autor, 2015.

[5] I. Barbi e D. C. Martins, *Conversores CC-CC Básicos Não Isolados*, 4. ed. Florianópolis:
Edição dos Autores, 2011.

[6] M. H. Rashid, *Power Electronics: Devices, Circuits, and Applications*, 4. ed. Harlow, Reino
Unido: Pearson, 2014.

[7] A. I. Pressman, K. Billings e T. Morey, *Switching Power Supply Design*, 3. ed. Nova York, NY,
EUA: McGraw-Hill, 2009.

[8] Plexim GmbH, *PLECS User Manual*, versão 5.0. Zurique, Suíça, 2025. [Online]. Disponível em:
https://www.plexim.com/sites/default/files/plecsmanual.pdf

[9] R. D. Middlebrook e S. Ćuk, "A general unified approach to modelling switching-converter power
stages," em *Proc. IEEE Power Electronics Specialists Conference (PESC)*, 1976, pp. 18–34.

> Verificar, antes da entrega, edição e ano dos livros efetivamente disponíveis para a equipe e a
> versão exata do manual do PLECS usada. O item [1] deve seguir a forma que o professor preferir
> para citar o próprio material.

Próximo arquivo: `10-estrutura-do-artigo.md`.
