# Próximos passos — Trabalho 2 (Conversores CC-CC isolados)

Este arquivo registra o estado do trabalho ao fim de cada sessão e a lista de tarefas pendentes,
para que qualquer sessão futura (humana ou do Claude) retome exatamente do ponto em que parou.
**Atualize-o ao final de cada sessão.**

## Estado em 21/09/2026 (sessão 1)

### Concluído

- [x] PDF do professor movido para `documento explicativo/` e convertido fielmente em
      `documento explicativo/Trabalho02.md`, com equações em LaTeX, tabelas de especificações e
      notas de conversão com os parâmetros legíveis dos esquemáticos PSIM.
- [x] 35 figuras recortadas do PDF a 220 dpi em `documento explicativo/imagens/`
      (`fig00` a `fig21`, com sufixos a/b/c para subfiguras). Os nomes descrevem conversor e conteúdo.
- [x] Estrutura de pastas criada, espelhando o Trabalho 1 e o projeto `controle-main`:
      `desenvolvimento/` (+ `figuras/`, `calculos/`), `simulação PLECS/`, `resultados PLECS/`,
      `artigo/`, `documentos de referência/` (com o `template-a4.docx` copiado do Trabalho 1).
- [x] `README.txt` com o contexto do trabalho.
- [x] `desenvolvimento/calculos/parametros_projeto.py`: reproduz todas as contas do enunciado e
      deriva os equivalentes e as cargas do degrau. Todos os valores conferem com o enunciado.
- [x] `desenvolvimento/00-indice-do-projeto.md`: plano dos documentos, tabelas consolidadas de
      parâmetros (isolados, equivalentes, degrau de carga, resultados esperados) e a lista de
      **6 divergências** encontradas no enunciado.
- [x] `desenvolvimento/07-guia-simulacao-plecs.md`: guia completo do PLECS para os 8 circuitos
      (4 isolados + 4 equivalentes), com scripts de inicialização, tabelas de conexão, contagem de
      terminais, comando das chaves, resultados esperados, ensaio de formas de onda, diagnóstico.

### Decisões tomadas (e por quê)

- **PLECS no lugar do PSIM**: o usuário não tem acesso ao PSIM. Guia escrito para PLECS
  Standalone 4.x, com notas para o Blockset. Não há PLECS instalado nesta máquina (só MATLAB
  R2024a, sem toolboxes detectadas), então o guia **ainda não foi validado** numa instalação real.
- **Transformador ideal + $L_m$ explícito, sem dispersão**: evita erros de interrupção de corrente
  com chaves ideais, dispensa o grampeador RCD do Flyback e dá acesso direto a $i_{Lm}$.
- **Full-bridge com duas variantes de comando**: B (a do professor, braços complementares) para o
  degrau; A (diagonais, Fig. 7) para conferir as formas de onda teóricas.
- **Um arquivo `.plecs` por conversor**, com isolado e equivalente juntos, gerador de degrau de
  carga único (Goto/From) e Scope com as curvas sobrepostas, como nas figuras do professor.
- Numeração dos documentos: o guia do PLECS é o 07, mesma posição do guia do PSIM no projeto base.

## Estado em 21/09/2026 (sessão 2)

### Respostas do usuário (decididas)
- **PLECS Standalone 5.0** (arquivo de exemplo `simulação PLECS/arquivo-qualquer.plecs`).
- **Entrega no mesmo formato do Trabalho 1**: artigo IEEE A4, .docx + .pdf, seguindo as seções do
  enunciado.
- **Autores:** Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962).
  Já registrados no `README.txt` e no doc 00.

### Concluído nesta sessão
- [x] **Modelos `.plecs` gerados** em `simulação PLECS/`: `forward`, `fullbridge`, `pushpull`,
      `flyback` (isolado + equivalente, geradores de pulso via Goto/From, degrau de carga, Scope
      com 3 gráficos sobrepostos, *To File* gravando CSV em `resultados PLECS/`).
- [x] Gerador reprodutível: `simulação PLECS/gerador/plecs_lib.py` (escreve o formato .plecs) e
      `gerar_modelos.py` (descreve os 4 circuitos). O gerador confere que todo terminal está ligado
      exatamente uma vez. Cabeçalho 5.0 copiado do arquivo do usuário (`cabecalho_plecs50.txt`).
- [x] `simulação PLECS/LEIA-ME.md`: organização dos modelos, decisões de modelagem e checklist da
      primeira abertura. Guia 07 atualizado com uma nota sobre os modelos prontos.

### Como o formato .plecs foi levantado (para futuras correções)
Não há PLECS nesta máquina. O formato veio de ~20 modelos públicos no GitHub (versões 4.6 a 5.0,
incluindo um Forward ideal e dois Flybacks) e do manual do PLECS (baixado; páginas: Ideal
Transformer p. 714-715, Ammeter p. 541, Logical Operator p. 763, Pulse Generator p. 861,
To File p. 996). Fatos confirmados:
- tipos: `DCVoltageSource`, `MosfetWithDiode` (1 dreno, 2 fonte, 3 gatilho), `Diode` (1 anodo,
  2 catodo), `Inductor` (`L`, `i_init`), `Capacitor` (`C`, `v_init`), `Resistor`, `Switch`,
  `Transformer` (`Windings`, `n`, `Polarity`, `Lm`, `im0`; terminais 1/2 = enrolamento 1,
  3/4 = enrolamento 2, 1 e 3 com a mesma polaridade), `Voltmeter`/`Ammeter` (3 = saída),
  `Ground`, `PulseGenerator` (`Hi`, `Lo`, `f`, `DutyCycle`, `Delay` em s), `LogicalOperator`
  (`Operator` 6 = NOT), `Goto`/`From` (`Tag`), `SignalMux` (1 = saída), `Scope`, `PlecsProbe`
  (sinal "Inductor current"), `ToFile` (`FileType` 1 = CSV), `Gain` (`K`).
- espiras negativas invertem a polaridade de um enrolamento (manual + flybacks de referência).
- Incertos (a confirmar na 1ª abertura): posição exata de alguns terminais (só estética), sentido
  positivo do amperímetro, se o *Scope* sem os campos `State`/`HeaderState` abre sem aviso.

### Pontos em aberto que dependem do usuário
1. **Abrir os quatro modelos no PLECS 5.0 e relatar** qualquer erro de carregamento ou de
   simulação (mensagem exata), seguindo o checklist de `simulação PLECS/LEIA-ME.md`.
2. Divergência 1 (Full-bridge, $L_m$): plano atual é simular com 2,6 mH e comentar no texto.

## Estado em 21/09/2026 (sessão 3)

- Usuário abriu e simulou os modelos **sem erros**; sentido dos amperímetros e desenho OK.
  O formato .plecs gerado está validado no PLECS 5.0.
- CSVs recebidos: `forward`, `fullbridge`, `pushpull`, `flyback_mcd`. **Falta `flyback_mcc`**
  (rodar `flyback.plecs` com `kL = 10`).
- **Problema no Forward:** o CSV mostra razão cíclica efetiva 0,50 (Vo = 68 V = 136 × 0,5) nos
  dois circuitos, embora o arquivo tenha `D = 0.4`. Full-bridge, push-pull e flyback conferem
  (0,80 / 0,40 / 0,40). Hipótese: `D` alterado na sessão do PLECS antes de simular. **Refazer a
  simulação do Forward** conferindo `D = 0.4` nos comandos de inicialização.
- [x] `resultados PLECS/analisar_degraus.py`: lê os CSV, gera as figuras no estilo do professor em
  `desenvolvimento/figuras/plecs-<caso>-degrau-<de>-<para>.png` (300 dpi) e as métricas em
  `metricas_degraus.csv` / `.md` (antes, final, vale/pico, instante, acomodação 2 %, erro RMS e
  máximo isolado × equivalente). Rodar de novo após refazer o Forward e o Flyback MCC.
- Resultados já confirmados: Full-bridge vale 40,8 V / pico 70,7 V (prof.: ≈ 40 / ≈ 71);
  push-pull 340,0 / 466,3 V (≈ 338 / ≈ 465); Flyback MCD 127,1 V a 20 % e 56,8 V a 100 %
  (previsto 127,3 / 56,9), sem sobressinal. Erro isolado × equivalente: ≤ 0,09 % RMS e ≤ 0,8 %
  máximo (maior no Full-bridge 100→20 %, efeito da corrente magnetizante de 2,6 mH).
- Observação para o texto: no push-pull a 100 % o Vo médio é 398,5 V (não 400 V) nos dois
  circuitos: perda na RSE de 0,873 Ω com a corrente pulsada do diodo.

## Estado em 21/09/2026 (sessão 4)

- Forward refeito com `D = 0.4` (Vo = 54,4 V por causa das espiras 100:68) e Flyback MCC simulado.
  **Todas as simulações concluídas**; 10 figuras de degrau e `metricas_degraus.md` completos.
- [x] Figuras das etapas de operação: `desenvolvimento/figuras/etapas-fullbridge-{1..4}.png` e
      `etapas-pushpull-{1..4}.png` (400 dpi), geradas por `desenvolvimento/figuras/fonte/
      etapas_operacao.py` + `esquema.py` (primitivas matplotlib, caminho de corrente em traço
      grosso vinho, no estilo das Figs. 3 e 17 do professor).
- [x] Memorial escrito: `01-fundamentos-conversores-isolados.md` (reflexão, equivalentes, reset,
      modos de condução, resumo dos resultados), `02-forward.md`, `03-full-bridge.md`,
      `04-push-pull-alimentado-em-corrente.md`, `05-flyback.md`. Os textos "ESCREVER" do enunciado
      estão todos redigidos (introdução, topologia, formas de onda, etapas) e os resultados do
      PLECS incorporados com comparação às figuras do professor.
- Pendentes do memorial: `06-metodologia-de-validacao.md` (curto; a métrica está no script),
  `09-conclusoes-e-referencias.md` (seção 5 "Conclusões gerais" e seção 6 "Referências" do
  enunciado), `10-estrutura-do-artigo.md`. Opcional: figuras das 2 etapas do Flyback em MCC.

## Estado em 21/09/2026 (sessão 4, fim) — ARTIGO GERADO

- [x] `06-metodologia-de-validacao.md` e `09-conclusoes-e-referencias.md` escritos.
- [x] Usuário forneceu capturas dos esquemáticos arrumados no PLECS em
      `simulação PLECS/simulacao-circuitos/plecs-circ-*.png`; entraram no artigo (Figs. 4, 9, 14, 19).
- [x] **Artigo IEEE A4 gerado**: `artigo/artigo-conversores-isolados-equivalentes.docx` e `.pdf`
      (13 páginas, 21 figuras, 9 equações, 2 tabelas, 9 referências). Pipeline em `artigo/fonte/`
      (ver `artigo/fonte/LEIA-ME.txt`): `montar_figuras.py` → `omml_gen.py` (sem pandoc:
      latex2mathml + MML2OMML.XSL do Office) → `build_docx.py` → `exportar_pdf.ps1` (Word COM).
- Pendências menores / revisão do usuário:
  1. Ler o artigo e pedir ajustes de texto (edita-se `artigo/fonte/conteudo.py` e regenera).
  2. Páginas 6 e 9 têm espaço em branco abaixo das figuras de circuito de largura total
     (equilíbrio de colunas do Word). Ajustável à mão no Word ou reordenando figuras.
  3. Conferir as referências bibliográficas (edições disponíveis à equipe) e a forma de citar o
     material do professor.
  4. Opcional: `10-estrutura-do-artigo.md` (o artigo já existe; o mapeamento está implícito em
     `conteudo.py`), figuras das 2 etapas do Flyback em MCC.

## Próximas tarefas, em ordem (histórico do planejamento)

### Etapa 1 — Simulações (usuário, com os modelos prontos)
1. Abrir `forward.plecs`, simular e comparar com a Fig. 5 do professor (valida o fluxo inteiro).
2. Simular `fullbridge.plecs`, `pushpull.plecs` e `flyback.plecs` (este com `kL = 1` e depois
   `kL = 10` nos comandos de inicialização).
3. Conferir que os CSV `*_degrau.csv` apareceram em `resultados PLECS/`.
4. Salvar capturas dos esquemáticos em `desenvolvimento/figuras/plecs-*.png` (arrumar o desenho
   à mão antes, se quiser; nesse caso salvar o .plecs com outro nome, porque regenerar sobrescreve).
5. Ensaio de formas de onda em regime (guia, seção 10): acrescentar *Probes* e gravar
   `*_regime.csv`. *Opcional (Claude):* incluir esse ensaio no gerador.
6. Se algo falhar: Claude corrige `plecs_lib.py`/`gerar_modelos.py` e regenera.

### Etapa 2 — Scripts de pós-processamento (Claude)
6. `resultados PLECS/plotar_degraus.py`: lê os CSV (tempo + 6 colunas na ordem da seção 3 do guia),
   gera figuras no estilo das Figs. 5/9/14/19/21 (vermelho = isolado, azul = equivalente, dois
   painéis: $V_o$ e $I_o$; opcional terceiro painel $I_L$), nas janelas de tempo da seção 8 do guia,
   a 400 dpi, em `desenvolvimento/figuras/`.
7. `resultados PLECS/metricas_degrau.py`: valor antes/depois, extremo e instante, tempo de
   acomodação (2 %), erro RMS isolado × equivalente — alimenta os docs 06 e 08.
   (Base de referência: `controle-main/.../simulação MatLab/metricas_degrau.m`.)
   Dependências já disponíveis: Python 3.14, numpy, matplotlib 3.10, pymupdf.

### Etapa 3 — Memorial teórico (Claude), no estilo do Trabalho 1
8. `01-fundamentos-conversores-isolados.md`: transformador de AF (ideal + $L_m$ + dispersão),
   relação de espiras, reflexão de fontes e impedâncias, desmagnetização/reset, dedução geral dos
   equivalentes (regras: $V_{i,eq} = aV_i$; $L_{eq} = a^2L$; frequência e razão cíclica efetivas).
9. `02-forward.md`: revisão do exemplo resolvido + equivalência Buck + resultados PLECS.
10. `03-full-bridge.md`: preencher todos os ESCREVER (introdução, topologia, formas de onda da
    Fig. 7, as 4 etapas de operação), projeto (com a nota da divergência 1), equivalente Buck.
11. `04-push-pull-alimentado-em-corrente.md`: idem, com as 4 etapas (2 de armazenamento em $L_i$,
    2 de transferência) e o equivalente Boost.
12. `05-flyback.md`: idem, 3 etapas em MCD (e as 2 de MCC), fronteira MCD/MCC, $V_o$ em MCD
    dependente da carga, equivalente Buck-Boost, gráfico faltante 100→20 % em MCD.
13. **Figuras das etapas de operação** (pedido explícito do professor: "colocar 4 conversores e
    marcar em negrito por onde percorre a corrente"): Full-bridge (4 etapas) e Push-pull (4 etapas)
    são obrigatórias; Flyback já tem as 3 do professor (Fig. 17). Estilo a imitar: Figs. 3 e 17
    (caminho de corrente em traço grosso vinho, componentes inativos finos). Ferramenta sugerida:
    Python (matplotlib ou `schemdraw`, a instalar) ou reportlab, como no projeto `controle-main`
    (`artigo/fonte/gerar_figuras_vetoriais.py`). Salvar em `desenvolvimento/figuras/` a 400 dpi.
14. `06-metodologia-de-validacao.md`, `08-analise-de-resultados.md`,
    `09-conclusoes-e-referencias.md`, `10-estrutura-do-artigo.md`.

### Etapa 4 — Artigo (Claude)
15. Reaproveitar o pipeline do Trabalho 1 (`Trabalho 1/artigo/fonte/`: `conteudo.py`,
    `omml_gen.py`, `build_docx.py`, `check_pdf.py`) — ler o `LEIA-ME.txt` de lá, incluindo as
    armadilhas do template OOXML *strict*.
16. Gerar `artigo/artigo-conversores-isolados.docx` e o `.pdf` (exportado pelo Word).

## Referências úteis já localizadas

- Guia PSIM de origem: `C:\Users\josem\Downloads\Pasta Pessoal do Jonatas\controle-main\controle-main\Modelos de Conversores FT\desenvolvimento\07-guia-simulacao-psim.md`
- Projeto base (FT de conversores): mesma pasta `Modelos de Conversores FT` (scripts MATLAB, artigo LaTeX/DOCX).
- Trabalho 1 (estilo do memorial e pipeline do artigo): `..\Trabalho 1\`.
- Recorte das figuras do PDF: `documento explicativo/recortar_figuras.py`
  (uso: `python recortar_figuras.py <pdf> <pasta_saida>`; PyMuPDF, 220 dpi, coordenadas medidas numa
  renderização a 110 dpi).
