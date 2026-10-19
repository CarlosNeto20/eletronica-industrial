TRABALHO 3 - CARREGADOR DE BATERIAS DE 15 A BASEADO NO CONVERSOR FORWARD DE DUAS CHAVES
=========================================================================================

Disciplina: Eletrônica Industrial (UFC) - Prof. Dr. René Pastor Torrico-Bascopé
Autores (discentes):
	Jonatas Manoel Assunção Felix - 539729
	Jose Carlos Moreira de Brito Neto - 536962

Este arquivo é a instrução de trabalho. O estado atual e as pendências ficam sempre em
PROXIMOS-PASSOS.md (raiz desta pasta); o ponto de entrada técnico é
desenvolvimento/00-indice-do-projeto.md.


1. OBJETIVO DO TRABALHO
-----------------------
Projetar e simular um carregador de baterias estacionárias (7 Ah a 150 Ah, banco de 24 V: 20 V a
27 V) com corrente de recarga ajustável de 0 A a 15 A pela referência de corrente Vrefi (0 V a
2,5 V). A rede (220 V, de 176 V a 264 V eficazes, 60 Hz) alimenta um retificador a diodos com
filtro capacitivo, que alimenta um conversor CC-CC Forward de duas chaves (chaves de menor tensão,
faixa de potência adequada, saída em fonte de corrente). O controle tem duas malhas que NÃO
operam ao mesmo tempo: corrente (recarga em corrente constante) e tensão (flutuação/equalização).
Ponto negativo a comentar: o retificador com filtro capacitivo drena corrente pulsada e o fator
de potência fica abaixo de 0,5.


2. ENTREGA
----------
Artigo no modelo IEEE A4 (documentos de referência/template-a4.docx), em .docx E .pdf, no mesmo
formato e com o mesmo fluxo do Trabalho 2. Seções, na ordem do enunciado do professor:

	1. Introdução
	2. Especificações básicas da bateria estacionária
	3. Dados da rede elétrica
	4. Projeto do retificador a diodos com filtro capacitivo
	5. Projeto do conversor Forward de duas chaves
	6. Projeto do circuito de controle
	7. Resultados de simulação
	8. Conclusão
	   Referências


3. MATERIAL DO PROFESSOR (pasta "documento explicativo")
-------------------------------------------------------
	Forward_Carregador_Planilha_2026.pdf   A "planilha" (Mathcad) com o projeto resolvido:
	                                       bateria, rede, retificador (C1), Forward (n, Dmin, Lo,
	                                       Co), malhas de tensão e de corrente (fator K, tipo 2),
	                                       circuito de simulação no PSIM (Fig. 14) e três ensaios
	                                       (Figs. 15 a 17), todos com a rede em 176 V eficazes.
	Controle_Basico_Parte04_Anexo.pdf      Circuitos de controle com o CI UC3525A (malha aberta,
	                                       malha de tensão, tensão + corrente). Base do
	                                       esquemático de controle e da lista de componentes.

A planilha é o GUIA de profundidade e de formato: o que ela já resolve é conferido e reproduzido;
o que ela não traz é desenvolvido no mesmo nível.


4. O QUE PRECISA SER FEITO
--------------------------
Regra geral: desenvolver tudo o que falta na planilha, reproduzir as simulações do professor e
comparar com as dele, e escrever a conclusão.

4.1 Para cada conversor (retificador com filtro capacitivo e Forward de duas chaves):
	- introdução, topologia e formas de onda teóricas (e etapas de operação do Forward);
	- cálculo dos componentes, com o print do datasheet do componente comercial escolhido
	  sempre que houver escolha de componente (como o professor fez com o capacitor TDK);
	- resultados de simulação.

4.2 Melhorias mínimas pedidas sobre a planilha:
	- reproduzir os resultados de simulação do professor (degrau de carga 100 % <-> 20 %,
	  curto-circuito e recarga da bateria);
	- repetir os mesmos ensaios com a rede em 264 V eficazes (a planilha só tem 176 V);
	- escrever a conclusão (na planilha está "ESCREVER").

4.3 Sugestões do professor ao final da planilha (entram as que couberem):
	- projeto do retificador convencional de 4 diodos (esforços e escolha dos diodos);
	- esquemático do circuito de controle com o UC3525A e tabela de componentes;
	- 5 períodos da portadora triangular e da moduladora (noção de estabilidade);
	- (opcional, só se sobrar tempo) adaptar o projeto a outro isolado da família Buck.

4.4 Simulação: SEMPRE no PLECS (Plexim). O professor usou o PSIM, que não temos. Os resultados do
artigo saem dos CSV exportados pelo PLECS, plotados por script, e são comparados com as figuras
do professor. Divergências entre a planilha e o esquemático do professor são listadas no doc 00
e tratadas de forma consciente no texto, nunca copiadas sem comentário.


5. QUEM FAZ O QUÊ
-----------------
Claude: conferência numérica da planilha (script), modelos .plecs, pós-processamento dos CSV,
figuras, memorial, artigo (.docx e .pdf) e atualização do PROXIMOS-PASSOS.md.

Usuário (tarefas rápidas; o Claude deve PEDIR em vez de gastar tempo tentando contornar):
	- prints dos circuitos no PLECS -> simulação PLECS/simulacao-circuitos/plecs-circ-*.png
	  (o PLECS só exporta o esquemático pela interface: File > Export);
	- rodar as simulações e entregar os CSV, caso o Claude não tenha como rodá-las sozinho
	  (o PLECS 5.0.6 está instalado nesta máquina; com a interface RPC habilitada em
	  File > PLECS Preferences, o Claude roda tudo por script);
	- prints de datasheet que não possam ser obtidos de outra forma;
	- decisões e revisão final do texto.

Regra de ouro: se algo depende do usuário e ele resolve em um minuto, pedir de uma vez, em lista
objetiva (o que, com que nome de arquivo, em que pasta), e seguir com o que não depende dele.


6. ORGANIZAÇÃO DAS PASTAS (espelha o Trabalho 2)
------------------------------------------------
	documento explicativo/     PDFs do professor, a conversão da planilha para Markdown
	                           (Trabalho03.md) e as figuras recortadas em "imagens/".
	documentos de referência/  Template IEEE A4 (template-a4.docx) e datasheets usados.
	desenvolvimento/           Memorial (arquivos .md numerados), "figuras/" e "calculos/"
	                           (script que confere a planilha para 176 V e 264 V).
	simulação PLECS/           Modelo .plecs, o gerador que o escreve, o guia (LEIA-ME.md) e
	                           "simulacao-circuitos/" (prints dos esquemáticos).
	resultados PLECS/          CSV exportados, scripts de análise/plotagem e métricas.
	artigo/                    Artigo final (.docx e .pdf) e "fonte/" (pipeline do Trabalho 2).


7. ORDEM DE EXECUÇÃO
--------------------
	1. Conferir a planilha por script (176 V e 264 V) e registrar as divergências.
	2. Gerar os modelos PLECS (retificador + Forward de duas chaves + controle analógico).
	3. Simular: degrau de carga, curto-circuito, recarga e portadora x moduladora, em 176 V e
	   em 264 V; exportar CSV.
	4. Pós-processar: figuras no estilo do professor, métricas e comparação com as Figs. 15-17.
	5. Pedir ao usuário os prints dos circuitos (e o que mais estiver pendente).
	6. Escrever o memorial e montar o artigo; exportar .docx e .pdf.
	7. Atualizar PROXIMOS-PASSOS.md.


8. CRITÉRIO DE PRONTO
---------------------
	[ ] Todos os números da planilha reproduzidos pelo script, com as divergências explicadas.
	[ ] Retificador e Forward com topologia, formas de onda, cálculo e datasheets.
	[ ] Três ensaios do professor reproduzidos no PLECS em 176 V e em 264 V e comparados.
	[ ] Portadora x moduladora (5 períodos) e fator de potência medido.
	[ ] Conclusão escrita.
	[ ] Artigo IEEE A4 em .docx e .pdf na pasta "artigo".
