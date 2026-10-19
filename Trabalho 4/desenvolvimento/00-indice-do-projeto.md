# Trabalho 4 — índice e rastreabilidade

Projeto de um carregador de baterias de 15 A baseado no conversor Forward de duas chaves. UFC, Eletrônica Industrial. Professor: René Pastor Torrico-Bascopé. Discentes: Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962).

## Sequência de leitura

1. [Inventário, método e fontes](01-inventario-e-fontes.md)
2. [Auditoria do documento do professor](02-auditoria-do-documento.md)
3. [Retificador e barramento](03-retificador.md)
4. [Forward, filtro e esforços](04-forward-e-filtro.md)
5. [Transformador e indutor](05-magneticos.md)
6. [Modelagem e compensadores](06-controle.md)
7. [Guia de simulação PLECS](07-guia-plecs.md)
8. [Resultados e critérios de validação](08-resultados.md)
9. [Componentes, UC3525A e melhorias](09-componentes-e-melhorias.md)

`calculos.py` refaz cálculos e Bodes, sem simular a dinâmica do conversor. `calculos/parametros.json` é a fonte numérica para os modelos e o artigo. `../simulação PLECS/gerar_modelos.py` escreve os esquemas nativos. O executor e os dados brutos ficam em `../resultados PLECS`. O artigo e suas fontes ficam em `../artigo`.

## Classes de evidência

- **F:** dado ou gráfico fornecido pelo professor (PDF, página indicada).
- **A:** resultado analítico deste trabalho, com equação e script.
- **S:** resultado efetivamente retornado pelo PLECS, ligado a modelo, configuração, CSV e registro de execução.
- **H:** hipótese de engenharia ou proposta de componente; não equivale a medição ou validação de hardware.

As pastas `qa_fonte` e o arquivo `extracao_restrita.txt` são materiais de conferência local, sujeitos à mesma restrição de circulação do PDF original. Não publicá-los. Nenhum envio ao GitHub integra esta entrega.

## Estado final

Entrega concluída em 19/10/2026: cinco modelos principais, oito ensaios efetivamente executados, dados brutos, gráficos, artigo IEEE A4 de seis páginas em DOCX/PDF e verificação de integridade. Abrir `../LEIA-ME-ENTREGA.md` para instruções rápidas. Os valores medidos e ressalvas estão em 08-resultados.md; `verificacao_entrega.json` e o manifesto na raiz registram a conferência final.
