# Revisão visual do artigo

Cada página do PDF `artigo/Trabalho6_NoBreak_3kVA.pdf` foi renderizada em imagem a 120 dpi com PyMuPDF e conferida uma a uma. As imagens ficam em `artigo/qa/paginas/` e são regeneráveis com o trecho de código do fim deste arquivo. A pasta `artigo/qa/` tem circulação restrita, por conter também imagens de conferência do PDF do professor; só este arquivo de revisão é versionado.

Versão conferida: 7 páginas A4 (595,3 x 841,9 pt), 11 figuras, 8 tabelas e 7 equações editáveis, geradas em 9 de novembro de 2026 a partir de `metricas.json` com os 70 ensaios executados.

## O que foi conferido em cada página

| Página | Conteúdo | Situação |
|---|---|---|
| 1 | Título, autores com matrícula, afiliação, resumo, palavras-chave, Fig. 1, Tabela I, seções I a III, equação (1) | Correta |
| 2 | Equações (2) a (5), Tabelas II e III, Fig. 2 (Bode do laço), seções IV a VI, equação (6) | Correta |
| 3 | Fig. 3 (circuito do CC-CC), equação (7), início da seção VII, Tabela IV, Fig. 4, Tabela V | Correta |
| 4 | Fig. 5 (CC-CC em regime), Tabela VI, Fig. 6 (inversor), Fig. 7 (degrau), Tabela VII | Correta |
| 5 | Fig. 8 (no-break completo), Fig. 9 (transferência), Fig. 10 (retorno da rede) | Correta |
| 6 | Tabela VIII, Fig. 11 (regulação), verificação numérica, conclusões, início das referências | Correta |
| 7 | Referências [2] a [11] | Correta, com cerca de dois terços da página em branco |

## Defeitos encontrados e corrigidos

Todos os itens abaixo foram vistos nas imagens das páginas e corrigidos antes da versão final.

1. **Rótulos de painel sobre o eixo.** Na figura do no-break completo, as letras (a), (b) e (c) eram desenhadas com `ax.text` em coordenadas de eixo e caíam sobre o rótulo do eixo y do painel do barramento. Passaram a ser título à esquerda, fora do eixo, em `analisar_resultados.py`.
2. **Legenda sobre a curva.** Na figura do CC-CC em regime, a legenda do painel de corrente cobria o topo da curva de L_b. Foi acrescentada folga de 45% no limite superior do eixo.
3. **Legenda sobre as curvas de regulação.** As quatro curvas ocupam toda a área útil e a legenda em `loc='best'` caía sobre a de 176 V. Passou a ser uma linha horizontal acima do eixo.
4. **Identificador de código no texto.** O parágrafo de verificação numérica escrevia o nome da chave do JSON, `DHT_vo_pct`, no corpo do artigo, e a diferença aparecia como 0,00%. Passou a nomear a grandeza em português e a dar a ordem de grandeza da diferença.
5. **Concordância.** O mesmo parágrafo trazia "em a distorção"; corrigido para "na distorção".
6. **Afirmação desatualizada nas conclusões.** O texto dizia que as chaves do CC-CC veem "cerca de um terço do barramento", o que deixou de valer com a correção da tensão de bloqueio descrita em `desenvolvimento/08-resultados.md`. Passou a dizer dois terços, comparando com o barramento inteiro de um elevador simples.
7. **Última página quase vazia.** A primeira montagem terminava com uma página contendo apenas a referência [11]. Foram acrescentadas as figuras do degrau de carga e do retorno da rede, que já existiam e não estavam sendo usadas, o que equilibrou o corpo do artigo.

## Itens conferidos e aprovados

- Numeração das figuras contínua de 1 a 11, cada uma com legenda começando por `Fig. N.` e citada no texto da seção correspondente.
- Numeração das tabelas de I a VIII em algarismos romanos, com título em versalete acima da tabela e cabeçalho sombreado repetido em quebra de página.
- Sete equações numeradas e centralizadas, todas em OMML editável, não em imagem.
- Todos os eixos dos gráficos de resultado têm grandeza e unidade. Os eixos com valores fracionários usam vírgula decimal.
- As janelas ampliadas estão presentes onde importam: três períodos de comutação na figura do CC-CC, dois ciclos de 60 Hz nas figuras do inversor, 40 ms em torno da falta na figura da transferência e 50 ms em torno do retorno na figura do retorno da rede.
- Nenhuma figura ficou cortada na borda da coluna nem atravessou a divisão entre colunas.
- Nenhuma quebra de coluna separou um título de seção do primeiro parágrafo, nem a legenda da sua figura.
- Nenhum travessão no corpo do artigo, conferido por código em `verificar_entrega.py`.
- Autores e matrículas presentes; nenhum texto remanescente do modelo IEEE.
- Páginas em A4 com 595,3 x 841,9 pt, dentro da faixa de 6 a 8 páginas.

## Capturas dos esquemas do PLECS

As seis capturas de tela dos modelos, entregues em `resultados PLECS/circuitos-foto/`, foram recortadas e convertidas para fundo branco em `artigo/figuras/plecs_*.png`. Elas chegaram a ser montadas no corpo do artigo como duas figuras do modelo completo e a página foi conferida: a imagem de 2206 px de largura reduzida a uma coluna de 8,8 cm deixa os rótulos dos componentes ilegíveis. Foram retiradas do artigo, que passou a descrever o arranjo em texto, e ficaram em tamanho cheio em `desenvolvimento/07-guia-plecs.md`, que não tem limite de largura. O artigo voltou a ter 11 figuras e 7 páginas.

## Referências

A lista tem onze entradas, todas de fontes efetivamente consultadas e no mesmo estilo IEEE. As duas referências de livro citadas nos slides da disciplina não entraram, por decisão de entrega: os títulos não foram informados e não seriam inventados. Acrescentá-las depois é acrescentar duas linhas à lista `REFERENCIAS` de `artigo/fonte/conteudo.py` e regerar o `.docx` e o `.pdf`, sem mexer em mais nada. A dúvida sobre qual obra de Rashid a planilha usa na dedução de L_o continua registrada em `desenvolvimento/09-componentes-e-melhorias.md`.

## Como refazer as imagens

```powershell
python -c "import pymupdf; d=pymupdf.open('artigo/Trabalho6_NoBreak_3kVA.pdf'); [p.get_pixmap(dpi=120).save(f'artigo/qa/paginas/p{i+1:02d}.png') for i,p in enumerate(d)]"
```
