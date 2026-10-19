# Entrega do Trabalho 4

**Nota para a cópia do GitHub:** os CSVs brutos e os retornos RPC compactados foram mantidos apenas na pasta local original por causa do tamanho. O repositório contém métricas, gráficos em `artigo/figuras`, registros dos ensaios, modelos e scripts. Após clonar, execute os ensaios para regenerar os dados brutos antes de rodar a verificação integral.

Projeto de carregador Forward de duas chaves, UFC — Eletrônica Industrial. Entrega local de 19/10/2026, com modelos realmente executados no PLECS Standalone 5.0.6.

## Documentos principais

- [Artigo IEEE A4 em PDF](artigo/Trabalho4_Forward_15A.pdf): seis páginas, dez figuras próprias, dez equações e três tabelas.
- [Artigo editável em DOCX](artigo/Trabalho4_Forward_15A.docx): derivado do template fornecido; equações nativas editáveis. O PDF foi exportado desta mesma versão no Microsoft Word.
- [Índice do memorial](desenvolvimento/00-indice-do-projeto.md): auditoria, cálculos, magnéticos, controle, guia, resultados e melhorias opcionais.
- [Resultados interpretados](desenvolvimento/08-resultados.md): janelas, médias, picos, critérios e limitações.
- [Métricas detalhadas](resultados%20PLECS/metricas.md) e [JSON](resultados%20PLECS/metricas.json): valores calculados dos CSVs com hash conferido.

## Modelos e evidências

| Arquivo em `simulação PLECS` | Uso |
|---|---|
| `forward_degrau.plecs` | 20% ↔ 100%, redes de 176, 220 e 264 V; refinamento numérico |
| `forward_curto.plecs` | Curto de 1 mΩ e recuperação |
| `forward_bateria.plecs` | Emulação acelerada de recarga, 20 V + 400 mF + 10 mΩ |
| `forward_barramento_cc.plecs` | Banco revisado em 373 Vcc, ripple e cinco períodos PWM |
| `forward_capacitor_original.plecs` | Comparação de 2200 µF/110 mΩ com o controlador revisado |

O exemplo fornecido permanece intacto. A gravação posterior pelo PLECS normalizou a formatação dos modelos; a conferência confirmou componentes, parâmetros e conexões iguais. As versões normalizadas foram preservadas em `simulação PLECS/versoes_formatadas_plecs`, e os arquivos principais foram restaurados à versão de hash exato registrado nos ensaios. O relatório está em `desenvolvimento/comparacao_serializacao_plecs.json`. Os modelos usam blocos nativos e C-Script para controle; as conexões e parâmetros estão no arquivo texto. A extração automática usa terminais de saída no nível superior, sem depender de Scopes. O [guia PLECS](desenvolvimento/07-guia-plecs.md) descreve a montagem e a medição.

Cada um dos oito ensaios em `resultados PLECS` possui CSV, retorno nativo `_rpc.json.gz` e registro `_execucao.json`. Os gráficos PNG/PDF estão em `resultados PLECS/graficos`; os Bodes analíticos em `desenvolvimento/calculos` e `artigo/figuras`. Curvas temporais vieram do solver PLECS, não de um simulador Python alternativo.

## Reprodução neste computador

Abrir o PLECS com interface XML-RPC local na porta 1080 habilitada. Executar os comandos abaixo no PowerShell, a partir da pasta Trabalho 4. Não é necessário controlar o mouse. Salvar alterações manuais nos modelos antes de repetir um ensaio: o executor recarrega o arquivo de mesmo nome.

```powershell
$taskPython = 'C:\Users\Carlos Neto\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $taskPython 'desenvolvimento\calculos.py'
& $taskPython 'simulação PLECS\gerar_modelos.py'
& $taskPython 'resultados PLECS\executar_ensaios.py' --todos
& $taskPython 'resultados PLECS\analisar_resultados.py'
```

`--todos` preserva execuções concluídas com o mesmo modelo e duração. Para repetir um caso, usar, por exemplo, `--ensaio curto_220`. O teste rápido `--teste` executa 2 ms e substitui temporariamente o registro nominal; executar novamente o caso completo antes de produzir a análise. Em outra máquina, usar Python com numpy, scipy, matplotlib, lxml e pymupdf, ajustando o caminho. O circuito precisa de PLECS licenciado; não precisa de MATLAB ou PSIM.

Para reconstruir o artigo após revisar conteúdo e resultados:

```powershell
& $taskPython 'artigo\fonte\gerar_figura_arquitetura.py'
& $taskPython 'artigo\fonte\gerar_artigo.py'
& '.\artigo\fonte\exportar_pdf.ps1'
& $taskPython 'desenvolvimento\verificar_entrega.py'
```

A exportação PDF requer Microsoft Word instalado. `conteudo.py` contém o texto autoral; a atualização dos ensaios exige revisar as afirmações numéricas nele, não apenas regenerar as figuras. O código de montagem conserva os estilos e demais partes não afetadas do template. A renderização empacotada foi tentada, mas não dispunha de suporte funcional a OOXML Strict/LibreOffice; a alternativa Word → PDF foi renderizada e todas as seis páginas foram inspecionadas.

## Principais conclusões e limites

O banco revisado reduziu a ondulação de 0,321 para 0,166 Vpp. As malhas foram reprojetadas para cruzamentos de 2,5/5 kHz após auditar os valores publicados. O duty máximo foi ampliado de 0,4 para 0,45, preservando reset no modelo. A variação de rede e os degraus foram executados, assim como o curto e a recarga.

O desvio de tensão de −1,0073% no ensaio em 373 Vcc ultrapassa marginalmente o critério de ±1%. No curto, a média do indutor é 15 A, mas há pico de 20,991 A no indutor e cerca de 492 A no ramo de curto pela descarga capacitiva. Essas limitações estão no artigo; não foram omitidas para declarar aprovação integral. A bateria de 400 mF é um emulador acelerado e não prevê tempo real de recarga. Magnéticos, perdas, térmica, proteção e PCB permanecem projetos preliminares, não hardware ensaiado.

`verificacao_entrega.json` registra a conferência de execução, hashes, figuras, equações, formato A4 e preservação do template. `manifesto_entrega.json` permite verificar a integridade dos arquivos. Não houve publicação nem envio ao GitHub. O PDF didático, sua extração e imagens de conferência são restritos e foram excluídos do manifesto de entrega e sinalizados no `.gitignore`.
