# Próximos passos — Trabalho 3 (Carregador de baterias, Forward de duas chaves)

Este arquivo registra o estado do trabalho ao fim de cada sessão e a lista de pendências, para que
qualquer sessão futura (humana ou do Claude) retome do ponto em que parou.
**Atualize-o ao final de cada sessão.**

## Estado em 11/10/2026 (sessão 1)

### Pendente do usuário (rápido)

1. **Ler o artigo** (`artigo/artigo-carregador-forward-duas-chaves.pdf`, 14 páginas) e pedir
   ajustes de texto (edita-se `artigo/fonte/conteudo.py` e regenera).
2. Conferir as referências bibliográficas (edições disponíveis à equipe) e os e-mails dos autores.

Para regenerar o artigo depois de qualquer ajuste, na pasta `artigo/fonte`:
`python montar_figuras.py; python omml_gen.py; python build_docx.py;`
`powershell -ExecutionPolicy Bypass -File exportar_pdf.ps1; python exportar_markdown.py`
e copiar `build/artigo-*.docx` e `.pdf` para `artigo/`.

### Print do circuito no PLECS (feito)

O usuário exportou `simulação PLECS/simulacao-circuitos/plecs-circ-carregador.png` (desenho gerado
pelo script, sem retoques) e o artigo foi regenerado: a captura é a Fig. 15, logo abaixo do
esquemático do professor (Fig. 14). Se o desenho for arrumado e a captura refeita com o mesmo
nome, basta regenerar.

### Revisão das figuras pedida pelo usuário (feita)

- **Fig. 21** (aplicação de carga): a legenda ficava sobre as curvas; foi para o canto inferior
  direito do primeiro gráfico. Pelo mesmo motivo, as legendas dos diagramas de Bode (Figs. 11 e 12),
  do retificador (Fig. 16) e do Forward em regime (Fig. 17) foram para cima do gráfico.
- **Fig. 2** (formas de onda do retificador): o recorte da planilha ficava com letras ilegíveis na
  largura de uma coluna; foi redesenhada (`desenvolvimento/figuras/fonte/retificador_formas.py`).
- **Fig. 5** (etapas do Forward): setas de corrente maiores, em vermelho vivo com contorno branco e
  em vários pontos de cada caminho; rótulos com o dobro do tamanho (`esquema.ESC = 2`).
- Pelo mesmo critério, as Figs. 4 e 6 e os Bode foram refeitos já na largura de uma coluna.

Regra para as próximas figuras: desenhar no tamanho final (3,5 pol para uma coluna), com letra de
7 a 9 pt, legenda fora da área das curvas e setas de corrente bem visíveis. Depois de mudar a
altura de qualquer figura, conferir o PDF página a página (as ilhas de largura total deixam vazios
quando não cabem).

### Concluído nesta sessão

- [x] `README.txt` reescrito (objetivo, entrega, o que falta, quem faz o quê, critério de pronto).
- [x] Estrutura de pastas espelhando o Trabalho 2; `simulação plecs` renomeada para
      `simulação PLECS`.
- [x] Planilha convertida em `documento explicativo/Trabalho03.md`; 12 figuras recortadas em
      `documento explicativo/imagens/` (`recortar_figuras.py`).
- [x] `desenvolvimento/calculos/parametros_projeto.py`: reproduz todos os números da planilha
      (erros ≤ 0,1 %) e calcula as extensões: retificador em 176/220/264 V com 545,7, 940 e 470 µF,
      esforços nos semicondutores, laços com os componentes comerciais. Gera os Bode.
- [x] Modelo `simulação PLECS/carregador.plecs` gerado por `gerador/gerar_carregador.py`
      (retificador + Forward de duas chaves + controle analógico com amp-ops saturados, mesmos
      designadores da Fig. 14 do professor). Carrega e simula sem erros no PLECS 5.0.6.
- [x] Simulações rodadas por script (`resultados PLECS/rodar_ensaios.py`, interface RPC): regime
      (176, 220, 264 V), degrau de carga, degrau com folga no limite de corrente, curto-circuito e
      recarga, em 176 V e 264 V. 23 CSV em `resultados PLECS/`.
- [x] `resultados PLECS/analisar_ensaios.py`: 15 figuras `plecs-*.png` e `metricas_ensaios.md`.
- [x] Figuras do Forward de duas chaves: topologia, 3 etapas e formas de onda teóricas
      (`desenvolvimento/figuras/fonte/forward_duas_chaves.py`).
- [x] Datasheets baixados em `documentos de referência/datasheets/` (GBU8J, IRFP460, UF4005,
      VS-MUR3020WT, B41821, UC3525A) e tabelas recortadas (`recortar_datasheets.py`).
- [x] **Artigo IEEE A4 gerado:** `artigo/artigo-carregador-forward-duas-chaves.docx` e `.pdf`
      (14 páginas, 24 figuras, 20 equações, 7 tabelas, 13 referências), já com a captura do
      esquemático do PLECS.
- [x] Memorial `desenvolvimento/00` a `05` (01 a 05 gerados do texto do artigo) e guia do modelo
      em `simulação PLECS/LEIA-ME.md`.

### Decisões tomadas (e por quê)

- **Simulações por RPC.** O PLECS 5.0.6 está instalado nesta máquina
  (`C:\Users\ingri\OneDrive\Documentos\Plexim\PLECS 5.0 (64 bit)`). O usuário autorizou habilitar a
  interface RPC (registro `HKCU\Software\Plexim\PLECS5.0`, `XmlRpcEnabled = true`, porta 1080), e
  ela ficou habilitada. Com o PLECS aberto, `rodar_ensaios.py` refaz tudo em cerca de 6 min.
- **Controle analógico fiel ao do professor**, com *Lim. Op-Amp* (0 a 5 V), e não blocos de
  função de transferência: a saturação dos compensadores é o que define o comportamento nas
  trocas de malha.
- **Valores do esquemático do professor** para os compensadores e a portadora (18 kΩ, 2,7 nF,
  220 pF; 2,4 V pico a pico), e não os da planilha, porque são os que geraram as figuras dele.
- **C1 = 940 µF** (adotado na planilha) e **C2 = 0,8 F** (reproduz a Fig. 17), embora o
  esquemático mostre 470 µF e 400 mF. Ver as 9 divergências no doc 00.
- **Figuras de resultados em uma coluna**, com 176 V e 264 V sobrepostas, para evitar os vazios
  que as figuras de largura total deixam no Word.
- **Semicondutores:** IRFP460 (500 V) para as chaves, porque a topologia grampeia a tensão em
  373 V; UF4005 para a desmagnetização; um VS-MUR3020WT duplo para o secundário; GBU8J na ponte.

### Achados que valem destaque na apresentação

1. Ganho do compensador de corrente da planilha lido em 5 kHz em vez de 12,5 kHz: o laço cruza em
   20 kHz (margem de 57,4°).
2. A carga nominal coincide com o limite de corrente (15,006 A pedidos contra 14,97 A): o
   compensador de tensão satura e o pico na retirada de carga sobe de 28,4 V para 29,3 V. Uma
   folga de 4 % (Vrefi = 2,6 V) resolve, e o resultado passa a coincidir com o do professor.
3. Fator de potência de 0,405 (176 V) e 0,335 (264 V); corrente de pico da rede de 30,8 A, quase
   o dobro da do modelo de pulso retangular.
4. Surto de 256 A no diodo de bloqueio D15 quando a saída é curto-circuitada.
5. Sem partida suave, a corrente do indutor chega a 25 A na energização.

## Opcionais (se sobrar tempo)

- Redesenhar o circuito de controle com o UC3525A já com os valores deste projeto (hoje o artigo
  usa o circuito do anexo do professor, mais a lista de adaptações e a Tabela V).
- Projeto físico do transformador e do indutor (metodologia do Trabalho 1).
- Sugestão 1 do professor: adaptar o projeto a outro isolado da família Buck (meia ponte).
- Ensaio com o compensador de corrente corrigido (13,05 kΩ; 3,57 nF; 288 pF) para comparar.
- Partida suave e limitador da corrente de energização no modelo.

## Referências úteis

- Trabalho 2 (organização e pipeline do artigo): `..\Trabalho 2\`.
- Ajuda do PLECS: `onlinehelp/plecshelp.qch` na pasta de instalação (SQLite; as páginas saem com
  `zlib.decompress(dados[4:])`). Biblioteca de componentes: `components.plecs`. Demos úteis:
  `demos/operational_amplifier_circuits`, `demos/buck_converter_with_parameter_sweep` (RPC).
