Contexto: Trabalho acadêmico para a disciplina de Eletrônica Industrial (UFC, Prof. René Torrico-Bascopé)

Trabalho 2: ANÁLISE DE CONVERSORES CC-CC ISOLADOS E COMPARAÇÃO COM OS EQUIVALENTES

Autores (discentes):
	Jonatas Manoel Assunção Felix - 539729
	Jose Carlos Moreira de Brito Neto - 536962
Professor: Prof. Dr. René Pastor Torrico-Bascopé

Formato de entrega: o mesmo do Trabalho 1, isto é, artigo no modelo IEEE A4
(documentos de referência/template-a4.docx), em .docx e .pdf, seguindo a estrutura de seções do
enunciado do professor (Forward, Full-bridge, Push-pull, Flyback, Conclusões, Referências).

O trabalho estuda quatro conversores CC-CC isolados e, para cada um, verifica por simulação que o
conversor isolado e o seu equivalente não isolado (referido ao secundário) têm o mesmo
comportamento dinâmico diante de degraus de carga de 20% para 100% e de 100% para 20%. Essa
equivalência é o que autoriza, depois, levantar as funções de transferência sobre o conversor não
isolado, que é muito mais simples de modelar.

	1. Forward de uma chave           -> equivalente Buck        (JÁ RESOLVIDO pelo professor, serve de exemplo)
	2. Ponte completa (full-bridge)   -> equivalente Buck        (a desenvolver)
	3. Push-pull alimentado em corrente -> equivalente Boost     (a desenvolver)
	4. Flyback de uma chave (MCD e MCC) -> equivalente Buck-Boost (a desenvolver)

Para cada conversor devem ser escritos: introdução, topologia, formas de onda teóricas, etapas de
operação (desenhar os circuitos de cada etapa destacando o caminho da corrente), exemplo de projeto
(já dado pelo professor) e resultados de simulação (circuitos e formas de onda dos degraus de
carga). Ao final, conclusões gerais e referências. Assim como no Trabalho 1, o conversor Forward já
desenvolvido é o GUIA de profundidade e formato para as demais seções.

DIFERENÇA IMPORTANTE EM RELAÇÃO AO MATERIAL DO PROFESSOR: as simulações do professor foram feitas no
PSIM. Não temos acesso ao PSIM, então TODAS as simulações deste trabalho são feitas no PLECS
(Plexim). O guia de simulação (desenvolvimento/07-guia-simulacao-plecs.md) adapta o passo a passo do
projeto "controle-main/Modelos de Conversores FT" (que usava PSIM) para o PLECS, com todos os
parâmetros, tabelas de conexão e resultados esperados de cada circuito.

Organização das pastas
	documento explicativo/    PDF do professor e a sua conversão fiel para Markdown (Trabalho02.md),
	                          com todas as figuras recortadas em "imagens/".
	documentos de referência/ Template IEEE A4 (template-a4.docx), o mesmo do Trabalho 1.
	desenvolvimento/          Memorial de desenvolvimento (arquivos .md numerados), guia do PLECS,
	                          subpasta "figuras" e subpasta "calculos" (script que confere todos os
	                          parâmetros de projeto).
	simulação PLECS/          Arquivos .plecs montados a partir do guia.
	resultados PLECS/         Exportações CSV das simulações e scripts de plotagem.
	artigo/                   Artigo final no formato IEEE A4, em .docx e .pdf (mesmo fluxo do Trabalho 1).

Por onde começar: desenvolvimento/00-indice-do-projeto.md. O estado atual e as próximas tarefas estão
sempre em PROXIMOS-PASSOS.md, na raiz desta pasta.

No final, é necessário apresentar o artigo disponível tanto em formato .docx quanto em formato .pdf.
