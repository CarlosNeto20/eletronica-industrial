# Entrega do Trabalho 6

Projeto de um no-break de dupla conversão monofásico de 3 kVA. UFC, Eletrônica Industrial (TH0263). Discentes: Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962).

**Situação em 09/11/2026:** memorial teórico, cálculos, auditoria, modelos PLECS, executor, analisador e infraestrutura do artigo concluídos. **A simulação no PLECS ainda não foi executada**, porque a shell de trabalho (VM Linux) não alcança a interface RPC do PLECS no Windows. Nenhum resultado de simulação é apresentado como obtido até que os CSVs existam em `resultados PLECS`.

## Documentos principais

- [Índice do memorial](desenvolvimento/00-indice-do-projeto.md), com a sequência 01 a 09.
- [Auditoria da planilha](desenvolvimento/02-auditoria-do-documento.md) e `desenvolvimento/calculos/auditoria.csv` (49 itens).
- [Guia de simulação PLECS](desenvolvimento/07-guia-plecs.md), com modelos, ensaios, solver, grandezas e critérios.
- `desenvolvimento/calculos/parametros.json`, fonte numérica única para modelos e artigo.

## Modelos e ensaios

| Modelo em `simulação PLECS` | Uso | Ensaios |
|---|---|---|
| `retificador_barramento.plecs` | Seção 3 da planilha | `ret_176_planilha`, `ret_176_anexo`, `ret_264_anexo` |
| `elevador_bateria.plecs` | CC-CC de alto ganho | `elev_42`, `elev_56` |
| `inversor_malha_fechada.plecs` | Inversor e malha com barramento ideal | `inv_373_res`, `inv_2116_res`, `inv_373_vazio`, `inv_2116_vazio`, `inv_2116_nl`, `inv_degrau_2116` |
| `nobreak_completo.plecs` | Seção 6 e regulação | `nb_*` (falta de rede a 176, 220 e 264 V, cargas linear, não linear e RL de 3 kVA, retorno da rede, comando do PSIM), `conv_176_nl`, `reg_*` (44 pontos) |

O arquivo-base `arquivo_exemplo.plecs` permanece intacto. Os modelos são texto ASCII gerado por `gerar_modelos.py` e conferido por `conferir_modelos.py`.

## Como executar

Abrir o PLECS e habilitar File, PLECS Preferences, General, RPC interface na porta 1080. No PowerShell, na pasta Trabalho 6:

```powershell
$taskPython = 'C:\Users\Carlos Neto\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $taskPython 'resultados PLECS\executar_ensaios.py' --teste
& $taskPython 'resultados PLECS\executar_ensaios.py' --todos
```

O executor usa só a biblioteca padrão. Para refazer tudo do zero, a ordem completa é `desenvolvimento\calculos.py`, `simulação PLECS\gerar_modelos.py`, `simulação PLECS\conferir_modelos.py`, o executor, `resultados PLECS\analisar_resultados.py`, `artigo\fonte\gerar_figuras_artigo.py`, `artigo\fonte\gerar_artigo.py`, `artigo\fonte\exportar_pdf.py` (LibreOffice com o componente Math) ou `exportar_pdf.ps1` (Word) e `desenvolvimento\verificar_entrega.py`. As análises usam numpy, scipy, matplotlib, lxml e schemdraw.

## Limitações conhecidas

Modelos sem perdas de comutação e sem tempo morto, indutores lineares, transformadores sem saturação, bateria ideal, sem modelo térmico e sem EMI. A lógica de transferência é ideal (detecção instantânea). As condições iniciais evitam a partida e não a certificam. A seleção de componentes é preliminar (classe H).

O PDF do professor, a extração de texto e as imagens de conferência são material restrito, listados no `.gitignore` e fora do manifesto.
