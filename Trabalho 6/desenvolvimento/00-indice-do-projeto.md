# Trabalho 6. Índice e rastreabilidade

Projeto de um no-break de dupla conversão monofásico de 3 kVA. UFC, Eletrônica Industrial (TH0263). Professor: René Pastor Torrico-Bascopé. Discentes: Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962).

## Sequência de leitura

1. [Inventário, ambiente e fontes](01-inventario-e-fontes.md)
2. [Auditoria do documento do professor](02-auditoria-do-documento.md)
3. [Retificador e barramento](03-retificador-e-barramento.md)
4. [Inversor, modulação unipolar e filtro](04-inversor-e-filtro.md)
5. [Malha de tensão do inversor](05-malha-de-tensao-do-inversor.md)
6. [Conversor CC-CC elevador de alto ganho](06-conversor-cc-cc-elevador.md)
7. [Guia de simulação no PLECS](07-guia-plecs.md)
8. [Resultados de simulação](08-resultados.md)
9. [Componentes, melhorias e referências](09-componentes-e-melhorias.md)

Cada arquivo termina apontando o seguinte.

## Scripts e dados

| Arquivo | Papel |
|---|---|
| `calculos.py` | Refaz toda a planilha, a auditoria e os Bodes, sem simular a dinâmica dos conversores |
| `calculos/parametros.json` | Fonte numérica única para os modelos e o artigo |
| `calculos/auditoria.csv` e `.json` | 49 itens auditados (local, impresso, recalculado, decisão, justificativa) |
| `calculos/figuras/` | Bodes da planta, do compensador e do laço; α(K); ondulação de Lo; ganho do CC-CC |
| `inspecionar_biblioteca.py`, `blocos_biblioteca.json` | Sintaxe literal dos blocos do PLECS 5.0 instalado |
| `../simulação PLECS/gerar_modelos.py` | Escreve os quatro modelos `.plecs`, `modelos.json` e `ensaios.json` |
| `../simulação PLECS/conferir_modelos.py` | Conferência estrutural dos modelos e do C-Script, sem PLECS |
| `../resultados PLECS/executar_ensaios.py` | Executor por XML-RPC, só biblioteca padrão |
| `../resultados PLECS/analisar_resultados.py` | Métricas, comparação com os valores analíticos e gráficos |
| `verificar_entrega.py` | Conferência final de hashes, figuras, formato do artigo e números |

## Classes de evidência

- **F:** dado ou gráfico do professor, com a página do PDF.
- **A:** resultado analítico deste trabalho, com equação e script.
- **S:** resultado efetivamente retornado pelo PLECS, ligado a modelo, hash, opções do solver, CSV e registro de execução.
- **H:** hipótese de engenharia ou escolha preliminar de componente.

O PDF do professor, a extração `extracao_restrita.txt` e as imagens de `qa_fonte` são material de conferência local e não devem ser publicados (ver `.gitignore`).

## Estado da entrega

O estado atualizado da entrega, com o que foi executado no PLECS e o que ficou pendente, está em `../LEIA-ME-ENTREGA.md` e em `verificacao_entrega.json`.

Próximo arquivo: [01. Inventário, ambiente e fontes](01-inventario-e-fontes.md).
