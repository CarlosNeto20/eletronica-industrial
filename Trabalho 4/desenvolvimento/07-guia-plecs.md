# Guia reproduzível de simulação PLECS

## Ambiente e ordem

Versão identificada: PLECS Standalone 5.0.6 de 64 bits, formato 5.0 do exemplo fornecido. Não requer MATLAB/PSIM. O Python apenas gera arquivos, chama o solver PLECS por XML-RPC e analisa os sinais retornados. Nunca trata uma integração Python como resultado PLECS.

1. Executar `desenvolvimento/calculos.py` na raiz do Trabalho 4.
2. Executar `simulação PLECS/gerar_modelos.py`; o exemplo original permanece intacto.
3. Abrir o PLECS. Em File > PLECS Preferences > General, ativar RPC interface port 1080. A conexão é local, `http://localhost:1080`. Se a configuração for alterada enquanto o programa está aberto, confirmar a ativação ou reiniciar após salvar modelos próprios.
4. Rodar `resultados PLECS/executar_ensaios.py --teste` para carregar e simular 2 ms. O executor registra falhas, não cria resultados fictícios.
5. Rodar `--todos` para a matriz principal; `--ensaio degrau_176` permite repetição individual. O executor fecha apenas o modelo de mesmo nome que irá carregar; salve eventuais modificações manuais nesse modelo antes de executar.
6. Rodar o script de análise dos CSVs para regenerar métricas e figuras. Toda atualização numérica no texto do artigo deve ser conferida contra metricas.json e parametros.json antes da reconstrução.

Runtime usado para reprodução neste computador: `C:/Users/Carlos Neto/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`. Dependências de análise: numpy, scipy, matplotlib, lxml, pymupdf. A API XML-RPC integra a biblioteca padrão. Em outro computador, qualquer Python compatível com essas bibliotecas pode ser usado, ajustando apenas o caminho do executável.

## Modelos e ensaios

| Modelo | Finalidade | Condições |
|---|---|---|
| forward_degrau.plecs | 20%→100%→20% | Rbase=9 Ω, paralelo com 2,25 Ω entre 0,12 e 0,24 s, equivalente 1,8 Ω; 0–0,36 s |
| forward_curto.plecs | Curto e recuperação | Rbase=1,8 Ω, ramo de 1 mΩ ligado de 0,12 a 0,24 s; 0–0,36 s |
| forward_bateria.plecs | Transição CC/CV | Ebat=20 V, Cbat=0,4 F inicialmente a 0 V, Rbat=10 mΩ; 0–0,6 s |
| forward_barramento_cc.plecs | Ondulação/PWM isolados da rede | Fonte CC=373 V e banco revisado; degrau em 0,12 s |
| forward_capacitor_original.plecs | Comparação da ESR original | Mesma topologia e controle da revisão, C=2200 µF/r=0,11 Ω; não é réplica integral do controle PSIM |

Rede principal: 176, 220 e 264 Vrms, 60 Hz. Fonte V=√2Vrms, fase π/2, R=0,5 Ω e L=100 µH. Barramento: 940 µF, pré-carregado a √2Vrms−1,4 V. Isto evita inrush; o ensaio não certifica partida do retificador. Saída: C inicial 27 V nos ensaios resistivos e 20 V na bateria, IL inicial zero. Transformador: Np:Ns=60:18, Lm=19,08 mH, magnetizante inicial zero. Rcu agregado=20 mΩ; shunt=10 mΩ. As perdas reais dos magnéticos podem ser maiores, conforme memorial.

## Bibliotecas e conexões

Os tipos nativos são: ACVoltageSource/DCVoltageSource (Electrical/Sources), Diode e Mosfet (Electrical/Power Semiconductors), Transformer, Inductor, Capacitor e Resistor (Electrical/Passive Components), Switch, Voltmeter e Ammeter; no controle, CScript (Control/Functions & Tables), TriangleGenerator, Comparator, Goto/From, Output e PlecsProbe; Ground fixa o retorno de saída. O arquivo texto define todos os parâmetros, sem dependência de blocos externos.

Ponte: os catodos dos dois diodos superiores formam bus+, os anodos inferiores bus−; os dois nós CA ligam a rede. Cbus fica entre bus+ e bus−. Q1 liga bus+ ao topo do primário; Q2 liga a base do primário a bus−. ResetSuperior tem anodo na base do primário e catodo em bus+; ResetInferior tem anodo em bus− e catodo no topo do primário. Secundário em fase alimenta Dforward, Lo, RLo, IL e Dbloqueio; o diodo de roda livre liga o retorno secundário ao nó após Dforward. Co possui ESR em série até o retorno de saída. Rsh liga o retorno secundário ao retorno de saída. O ramo de carga ou de bateria fica em paralelo com o banco capacitivo.

Desenho: o fluxo vai da esquerda para a direita (entrada, ponte assimétrica do Forward, transformador, retificador e filtro de saída, carga) com o controle numa faixa abaixo. Todos os fios são ortogonais e o único cruzamento é o de pri+ sobre a perna B da ponte, inevitável porque o primário do transformador liga as duas pernas. Os sinais de controle não atravessam a potência: Vo e IL chegam ao C-Script pelas etiquetas `Vo_fb` e `IL_fb`, o PWM chega a Q1 e Q2 pela etiqueta `pwm` e o comando do degrau/curto chega a Scarga por `sel_carga`. As etiquetas só mudam o desenho; as conexões elétricas e a ordem das saídas 1 a 11 são as mesmas dos ensaios.

O C-Script recebe Vo e IL e contém quatro estados contínuos dos compensadores. Suas duas primeiras saídas são o comando limitado e o comando da chave de carga. As demais são uv/ui. O comparador compara o comando à portadora triangular de 0–2,1 V, 50 kHz, e aciona ambos os MOSFETs simultaneamente. A referência de corrente de 15 A sobe em 5 ms. O seletor mínimo implementa CC/CV e o rastreamento anti-windup usa 30000 s⁻¹.

## Solver e exportação

Solver implícito Radau, passo máximo inicial 2 µs, tolerância relativa 1e−6, absoluta 1e−8, detecção de eventos a 1 ns. O passo máximo corresponde a Ts/10; os eventos de comutação não se restringem a essa grade. O arquivo de ensaio detalha as opções efetivamente enviadas. Curto usa limite/saída de 1 µs; janela detalhada PWM usa 0,2 µs. O teste de convergência usa 1 µs e tolerância relativa 1e−7. Saídas em grade uniforme especificada permitem comparação direta, preservando também o retorno RPC compactado.

Cada execução válida gera `.csv`, `_rpc.json.gz` e `_execucao.json`. O registro informa data, versão identificada, hash do modelo, parâmetros, solver, duração real, número de amostras, colunas e hash do CSV. Uma falha registra status `falhou`; não habilita a seção de resultados medidos.

## Grandezas e critérios

Vo, IL, Vbus, comando, portadora, PWM, uv/ui, esforços de Q1, magnetização, Irede e Ibat quando aplicável. Unidades constam dos cabeçalhos. Calcular médias integrais, valores de pico, RMS, ripple em cinco períodos, duty médio e recuperação. No curto distinguir corrente limitada do indutor da descarga do banco; na recarga distinguir Ibat de IL. A janela inicial de soft-start é excluída das estatísticas de regime.

Esperado analítico: 27 V e 3/15 A nas cargas; corrente de recarga próxima de 15 A antes da transição CV; bateria chega à região de 27 V em ordem de 0,19 s com Cbat=0,4 F, não em horas. PWM de cinco períodos dura 100 µs. Os valores esperados não substituem a medição. Critérios: regulação média ±1%, limite de corrente média ±2%, ripple nominal ≤0,27 Vpp, reset por ciclo e ausência de crescimento sustentado de oscilação nos ensaios.

## Complementos confirmados na execução

O transformador nativo é ideal (magnetização interna infinita); o indutor `Lmag` de 19,08 mH está em paralelo com o primário. Essa separação permite medir diretamente a corrente magnetizante. Não são dois ramos magnetizantes em paralelo.

Os ensaios de ripple integram até 0,20 s, mas exportam somente 0,18–0,20 s em 0,2 µs, total de 100001 amostras. O executor preserva ensaios já concluídos com o mesmo hash de modelo; `--ensaio nome` força repetição individual. Os gráficos exportados ficam em `resultados PLECS/graficos` e são copiados para `artigo/figuras`. A interpretação dos desvios e dos critérios está em `08-resultados.md`.
