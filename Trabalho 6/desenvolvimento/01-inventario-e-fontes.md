# 01. Inventário, método e fontes

Este arquivo descreve o que existe no material de partida, como cada parte foi usada e quais regras de evidência valem para o restante do memorial. Ele vem logo depois do [índice](00-indice-do-projeto.md) e prepara a [auditoria do documento](02-auditoria-do-documento.md).

## 1. Ambiente de trabalho

A checagem de ambiente foi feita em 09/11/2026, antes de qualquer cálculo. Os resultados ficam registrados aqui porque condicionam a forma de executar a simulação.

| Item | Situação encontrada |
|---|---|
| Shell | Linux em VM (Ubuntu 22.04, kernel 6.8) com as pastas Trabalho 4, Trabalho 6 e a instalação do PLECS montadas; não há PowerShell nem Word |
| Python | 3.10.12; numpy 2.2.6, matplotlib 3.10.9, lxml 6.1.3, python-docx disponível; scipy 1.15.3 instalado na sessão |
| Arquivo-base do PLECS | `simulação PLECS/arquivo_exemplo.plecs`, campo `Version "5.0"`, CRLF, SHA-256 13c61562…2f9a; permanece intacto |
| Versão do PLECS | PLECS Standalone 5.0 de 64 bits, pasta `Documents/Plexim/PLECS 5.0 (64 bit)`; o Trabalho 4 registrou 5.0.6 na mesma instalação |
| RPC do PLECS | inacessível a partir da VM: a porta 1080 da VM responde HTTP 407 do proxy do sandbox, não o PLECS do Windows |
| Template para PDF | LibreOffice 24.2 converte o template OOXML Strict em três páginas A4 com aparência equivalente à renderização do Word registrada no Trabalho 4 |
| Compilador C | gcc 11.4 na VM, usado só para conferir a sintaxe do C-Script antes da execução |

Como a shell não alcança o PLECS, valeu a regra de contingência da especificação. Os modelos, o executor e o analisador foram preparados aqui, e a execução dos ensaios foi pedida ao usuário no PowerShell, com o PLECS aberto. Enquanto não houver CSV registrado, todo resultado de simulação aparece como pendente.

A sintaxe dos blocos foi tirada da própria instalação. O script `inspecionar_biblioteca.py` extrai das demos e de `components.plecs` um exemplo literal de cada tipo usado e grava `blocos_biblioteca.json`. A documentação interna do PLECS (`onlinehelp/plecshelp.qch`) confirmou a ordem de execução de `ModelVars` (aplicados depois dos comandos de inicialização e antes da avaliação dos parâmetros dos componentes), a numeração dos enrolamentos do bloco Transformer e o significado dos códigos dos operadores. A conferência do terminal de cada bloco foi feita pelas conexões de demos reais, como a do conversor Forward com transformador de três enrolamentos.

## 2. Inventário do PDF do professor

`documento explicativo/Planilha_Nobreak04_2026.pdf` é uma planilha Mathcad impressa pelo Microsoft Print to PDF em 16/10/2026, com 18 páginas A4. A extração de texto perde raízes, expoentes, ômega e barras de módulo, por isso cada fórmula foi conferida na imagem rasterizada da página. As imagens de conferência ficam em `desenvolvimento/qa_fonte` e a extração em `extracao_restrita.txt`, ambas fora de qualquer entrega pública.

| Página | Conteúdo | Uso neste trabalho |
|---|---|---|
| 1 | Capa: título, disciplina TH0263, professor e dois discentes genéricos, Fortaleza, outubro de 2026 | Identificação |
| 2 | Seção 1 (introdução) e Figura 1, diagrama de blocos com conversor CA-CC unidirecional, CC-CC unidirecional e inversor; seção 2 com as especificações | Classe F das especificações; Figura 1 redesenhada no artigo |
| 3 | Seção 3.1 (Prec = 2250 W pelo rendimento de 0,933), 3.2 (ondulação de 37,33 V), 3.3 e Figura 2 (ponte D1 a D4 com C1) | Base do retificador; auditoria da ondulação |
| 4 | Figura 3 (formas de onda idealizadas de vC, iD1, iD2 e iC), VC1max, VC1min e θC1 | Hipótese de pulso retangular |
| 5 | Seção 3.5: C1, tC1, VC1medio, Ioeq, Roeq, Ichg, IC1ef; escolha de 4 × 470 µF/450 V EPCOS B43501 e Rse = 0,05 Ω | Recalculado; banco de 1880 µF adotado nos modelos |
| 6 | Seção 3.6: ID1med, ID1ef, ID1pk = 2·Ichg, VDrrevpk; ponte de diodos lentos Vishay; Vimin_cc e Vimax_cc | Recalculado e comparado com o PLECS |
| 7 | Seção 4.1 (Vimax_cc = 373 V e Vimin_cc = 223 V), 4.2 (Vopk, Ioef, Iopk, ΔILo, fs, Mmax, Mmin) | Auditoria do barramento mínimo e de M |
| 8 | Seções 4.3 (Lo, citando Rashid), 4.4 (Co) e 4.5 (Ro) | Recalculado; dedução de Lo revista |
| 9 | Segunda seção 4.5: Figura 4 (malha de tensão), Vref = 4 V, Hv, Gv(s), Vd = 5 V, Fm | Modelo da planta e do modulador |
| 10 | Passo 1 e Figura 5 (Bode de FTLAscv) | Bode refeito em vários pontos |
| 11 | Passos 2 a 8: fcv = 2fs/6, P, Av, MF = 60°, α, escolha do Tipo 3, função α(K) | Auditoria do texto de 33,23 dB |
| 12 | Figura 6 (α em função de K), K = 47, passo 9 (zeros, polos e Gv) | Recalculado; K exato registrado |
| 13 | Equações de R2, R3, C1, C2, C3; Figura 7 (compensador Tipo 3 com amplificador operacional); Cv(s) | Implementado no C-Script |
| 14 | Figura 8 (Bode de Cv) e passo 10 | Bode refeito |
| 15 | Figura 9 (Bode de FTLAccv), margem de fase 60,516° e margem de ganho declarada infinita | Margens revistas em vários pontos |
| 16 | Seção 5: Vib de 42 a 56 V, Vob = 210 V, Pob = 2250 W, Dbmax = 0,7, fsb = 20 kHz, Iibmax, ΔIibmax, Lb, VC1 = 140 V, VNp = 70 V | Base do CC-CC |
| 17 | VSec = 70 V e a = 1; seção 6 com os títulos dos ensaios (6.1, 6.2, 6.3); seção 7 vazia ("ESCREVER") | Matriz de ensaios; interpretação no guia |
| 18 | Referências vazias ("PADRONIZAR", dois livros nos slides, pesquisar artigos, dissertações e teses); Anexo 01, circuito PSIM completo | Topologia do CC-CC, falta de rede, carga não linear e compensador comercial |

A numeração do PDF tem dois pequenos defeitos sem efeito técnico: não existe seção 3.4 e há duas seções 4.5. Este memorial preserva a numeração do professor quando cita o PDF.

### Leitura do Anexo 01

O circuito PSIM da página 18 traz informações que o texto não explica e que orientaram os modelos.

- A rede é uma fonte de 373 V de pico e 60 Hz ligada por uma chave bidirecional SS2, comandada por uma fonte quadrada VSQ3 de 2 Hz e razão cíclica 0,5. A rede fica, portanto, 250 ms conectada e 250 ms desconectada, e é assim que o professor emula a falta.
- Entre a chave e a ponte existe um transformador T1 de 100:100 espiras, com resistências de 1 mΩ, dispersões de 1 µH e magnetização de 1 H. Sua função é isolar galvanicamente a fonte aterrada do lado CC, cuja referência é a saída do inversor (o PSIM exige essa separação para não curto-circuitar a ponte). A relação 1:1 e as impedâncias desprezíveis indicam que ele não altera a tensão.
- Um resistor R2 de 0,1 Ω liga a ponte BD11 ao barramento, onde está C4 = 1880 µF.
- O CC-CC usa duas chaves comandadas por VSQ1 e VSQ2 a 20 kHz, razão cíclica 0,7 e fases 180° e 0°. As chaves estão permanentemente comandadas durante a simulação do professor.
- O transformador T_32 tem três enrolamentos de 100 espiras, resistências de 1 mΩ, dispersões de 1 µH e magnetização de 10 mH. Os dois primeiros formam o autotransformador da célula de três estados; o indutor L1 de 39,2 µH vem da bateria VDC3 de 42 V e entra na derivação central.
- Os diodos D17 e D18 levam a energia dos primários ao capacitor C8 de 10 µF, e o terceiro enrolamento alimenta a ponte D13 a D16, que carrega o capacitor C7 de 10 µF empilhado sobre C8. O conjunto C7 + C8 fica em paralelo com C4.
- O inversor tem quatro MOSFETs, filtro L2 = 365,6 µH e C1 = 60 µF com 5 mΩ. O sensor é um divisor de 1000 kΩ e 25,22 kΩ seguido de um seguidor de tensão.
- O compensador usa OP_AMP14 com RF = 33 kΩ, CFV2 = 5,6 nF, C9 = 120 pF, RIZ = 10 kΩ, RIP = 220 Ω e CI = 18 nF; a referência V1 de 4 V de pico a 60 Hz entra na entrada não inversora.
- O modulador compara a saída do compensador com duas portadoras triangulares de 10 V pico a pico (±5 V) e 20 kHz, defasadas de 180°, e gera os sinais complementares de cada braço com inversores lógicos. É a modulação unipolar.
- A carga não linear é uma ponte de diodos com 0,2 Ω em série, 1880 µF com 0,05 Ω de ESR e 9,5 Ω.

## 3. Outras fontes

- `README.txt` do Trabalho 6, que prevalece sobre qualquer suposição.
- `documentos de referência/template-a4.docx`, template IEEE A4 em OOXML Strict (SHA-256 9d0153f7…04d3, o mesmo do Trabalho 4).
- Pasta do Trabalho 4, usada apenas como modelo de método e de infraestrutura (gerador de modelos, executor, analisador, montagem do artigo e verificação). Nenhum valor, ensaio, figura ou conclusão do Trabalho 4 foi importado. As lições aproveitadas foram manter o arquivo `.plecs` em ASCII (a gravação pelo PLECS reinterpretou acentos), preservar o hash do modelo executado, exportar só por terminais de saída de nível superior e fixar a forma do PDF antes de investir no artigo.
- Documentação da instalação do PLECS 5.0 e blocos de exemplo, já descritos.
- Literatura pesquisada para as referências do artigo (listada em [09](09-componentes-e-melhorias.md) e no artigo). Só entram fontes cuja existência e metadados foram conferidos.

Os dois livros mencionados nos slides da disciplina não estão disponíveis. A planilha cita [Rashid] na dedução de Lo, o que é uma pista e não confirma qual livro é. Fica como pendência para o usuário informar os títulos.

## 4. Classes de evidência

- **F** para dado ou gráfico do professor, sempre com a página do PDF.
- **A** para resultado analítico deste trabalho, ligado a uma equação e a `calculos.py`.
- **S** para resultado efetivamente retornado pelo PLECS, ligado ao modelo, ao hash, às opções do solver, ao CSV e ao registro `_execucao.json`.
- **H** para hipótese de engenharia, como resistências de condução, quedas de diodos e seleção preliminar de componentes.

Nenhuma curva ou tabela de simulação é digitalizada do PDF ou produzida por integração em Python. O Python calcula expressões analíticas, gera arquivos e pós-processa CSVs do PLECS.

Próximo arquivo: [02. Auditoria do documento](02-auditoria-do-documento.md).
