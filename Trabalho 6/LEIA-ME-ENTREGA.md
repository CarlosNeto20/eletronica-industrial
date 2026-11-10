# Entrega do Trabalho 6

Projeto de um no-break de dupla conversão monofásico de 3 kVA. UFC, Eletrônica Industrial (TH0263). Discentes: Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962).

**Situação em 09/11/2026: entrega completa.** O memorial 01 a 09, os cálculos, a auditoria, os cinco modelos PLECS, a matriz de ensaios, a análise, o artigo em `.docx` e `.pdf` e a conferência final estão prontos. Dos 71 ensaios da matriz, 70 foram executados no PLECS e 1 falhou por limite de tempo, o `diag_cc_sem_20ms`, cuja falha é o próprio resultado procurado no grupo de diagnóstico. `verificar_entrega.py` fecha sem nenhuma falha.

## Documentos principais

- [Índice do memorial](desenvolvimento/00-indice-do-projeto.md), com a sequência 01 a 09.
- [Auditoria da planilha](desenvolvimento/02-auditoria-do-documento.md) e `desenvolvimento/calculos/auditoria.csv` (50 itens).
- [Guia de simulação PLECS](desenvolvimento/07-guia-plecs.md), com modelos, layout, ensaios, solver, grandezas e critérios.
- [Resultados de simulação](desenvolvimento/08-resultados.md), com as janelas, as comparações entre cálculo e simulação e o que atende ou não atende.
- `desenvolvimento/calculos/parametros.json`, fonte numérica única para modelos e artigo.
- `artigo/Trabalho6_NoBreak_3kVA.docx` e `.pdf`, sete páginas A4 no modelo IEEE, com 11 figuras, 8 tabelas e 7 equações editáveis.

## Modelos e ensaios

| Modelo em `simulação PLECS` | Uso | Ensaios |
|---|---|---|
| `retificador_barramento.plecs` | Seção 3 da planilha | `ret_176_planilha`, `ret_176_anexo`, `ret_264_anexo` |
| `elevador_bateria.plecs` | CC-CC de alto ganho | `elev_42`, `elev_56` e os diagnósticos com amortecedores |
| `elevador_sem_amortecedor.plecs` | Diagnóstico numérico | `diag_cc_sem_*` |
| `inversor_malha_fechada.plecs` | Inversor e malha com barramento ideal | `inv_373_res`, `inv_2116_res`, `inv_373_vazio`, `inv_2116_vazio`, `inv_2116_nl`, `inv_degrau_2116` |
| `nobreak_completo.plecs` | Seção 6 e regulação | `nb_*` (falta de rede a 176, 220 e 264 V, cargas linear, não linear e RL de 3 kVA, retorno da rede, comando do PSIM), `conv_176_nl`, `reg_*` (44 pontos) |

O arquivo-base `arquivo_exemplo.plecs` permanece intacto. Os modelos são texto ASCII gerado por `gerar_modelos.py`, com os fios roteados por `roteador.py`, e conferidos por `conferir_modelos.py` e `conferir_conexoes.py`.

## Layout dos esquemas

Os cinco modelos foram redesenhados em novembro de 2026. Os blocos ficam em grade de 10, por grupos funcionais e com o fluxo de potência da esquerda para a direita; cada conexão traz os seus pontos de passagem, de modo que todo fio é horizontal ou vertical e nenhum passa sobre um bloco. A geometria dos terminais foi medida na própria instalação do PLECS e está em `desenvolvimento/blocos_biblioteca.json`. Os arquivos anteriores à reorganização ficam em `simulação PLECS/layout_anterior/`, fora do manifesto, só como referência de conferência. `conferir_conexoes.py` compara os dois e confirma que componentes, parâmetros, nós elétricos, nós de sinal e terminais de saída são idênticos, com zero segmentos em diagonal e zero segmentos sobre blocos.

## Como executar

Abrir o PLECS e habilitar File, PLECS Preferences, General, RPC interface na porta 1080. No PowerShell, na pasta Trabalho 6:

```powershell
python 'resultados PLECS\executar_ensaios.py' --teste
python 'resultados PLECS\executar_ensaios.py' --todos
```

Para refazer tudo do zero, a ordem completa é `desenvolvimento\inspecionar_biblioteca.py`, `desenvolvimento\calculos.py`, `simulação PLECS\gerar_modelos.py`, `simulação PLECS\conferir_modelos.py`, `simulação PLECS\conferir_conexoes.py`, o executor, `resultados PLECS\analisar_resultados.py`, `artigo\fonte\gerar_figuras_artigo.py`, `artigo\fonte\gerar_artigo.py`, `artigo\fonte\exportar_pdf.ps1` (Word) ou `exportar_pdf.py` (LibreOffice com o componente Math) e `desenvolvimento\verificar_entrega.py`. O executor usa só a biblioteca padrão; as análises usam numpy, scipy, matplotlib, lxml, schemdraw, python-docx e PyMuPDF.

## Resultados em uma linha

A saída fica entre 114,60 V e 114,89 V eficazes em todos os ensaios, com distorção de 0,13% a 0,27% com carga linear e de 0,72% a 1,19% com carga não linear. O coeficiente de regulação fica abaixo de 0,08% em módulo nas quatro famílias levantadas. A transferência de rede para bateria derruba o valor eficaz por semiciclo em no máximo 0,18%. Dois critérios não são atendidos: o valor instantâneo do barramento em modo bateria cai abaixo de 210 V menos 5% por causa da ondulação de 120 Hz, e o índice de modulação efetivo chega a 0,873 em modo bateria, acima do limite de 0,85 adotado. Os detalhes, com as janelas e as comparações, estão em [08](desenvolvimento/08-resultados.md).

## Limitações conhecidas

Modelos sem perdas de comutação e sem tempo morto, indutores lineares, transformadores sem saturação, bateria ideal, sem modelo térmico e sem EMI. A lógica de transferência é ideal, com detecção instantânea. As condições iniciais evitam a partida e não a certificam. A seleção de componentes é preliminar (classe H). Os rendimentos medidos contam apenas perdas de condução e quedas de diodos, e por isso são limites superiores.

## Pendências

- Os dois livros citados nos slides da disciplina ficaram fora das referências, por decisão de entrega. Os títulos não foram informados e não seriam inventados; as onze referências do artigo são todas de fontes efetivamente consultadas. Se os títulos vierem depois, basta acrescentá-los à lista `REFERENCIAS` em `artigo/fonte/conteudo.py` e regerar o `.docx` e o `.pdf`.
- Qual obra de Rashid a planilha usa na dedução de L_o.
- O código do fabricante do MOSFET de 200 V do CC-CC, depois da correção da tensão de bloqueio descrita em [08](desenvolvimento/08-resultados.md).

O PDF do professor, a extração de texto e as imagens de conferência são material restrito, listados no `.gitignore` e fora do manifesto.
