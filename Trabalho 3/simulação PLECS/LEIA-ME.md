# Modelo PLECS do Trabalho 3

`carregador.plecs` (PLECS Standalone 5.0) contém o carregador completo: retificador em ponte com
filtro capacitivo, Forward de duas chaves e controle analógico com amplificadores operacionais.
Ele reproduz a Fig. 14 do professor (PSIM) com os mesmos designadores e é gerado por
`gerador/gerar_carregador.py`.

## Como usar

**Pela interface.** Abrir `carregador.plecs`. Em *Simulation › Simulation Parameters ›
Initialization*, as duas primeiras variáveis definem o ensaio:

| Variável | Valores |
|---|---|
| `Vrede` | 176 (mínima), 220 (nominal) ou 264 (máxima), em volts eficazes |
| `ensaio` | 0 = regime a 100 %; 1 = degrau de carga 100 % ↔ 20 % (3 Hz); 2 = curto-circuito de 1 mΩ (3 Hz); 3 = recarga da bateria |

*Simulation › Start*. Há três osciloscópios: **Saida** (Vbat e corrente em L2, como nas figuras do
professor), **Controle** (tensão de controle, portadora e PWM) e **Retificador** (tensão em C1,
tensão e corrente da rede). Um segundo de simulação leva cerca de 30 s.

**Por script.** `resultados PLECS/rodar_ensaios.py` roda todos os ensaios pela interface RPC do
PLECS e grava os CSV. Requer o PLECS aberto e a opção *File › PLECS Preferences › General ›
RPC interface* habilitada na porta 1080 (habilitada nesta máquina em 11/10/2026).

```bash
python "resultados PLECS/rodar_ensaios.py"
```

```bash
python "resultados PLECS/analisar_ensaios.py"
```

## Estrutura do modelo

- **Em cima**, da esquerda para a direita: fonte V1, ponte D11 a D14, capacitor C1, Forward de
  duas chaves (MOS3, MOS1, D3, D4, Lm, T1, Lk), secundário (D2, D1, L2, R8 + C4, Rsh), diodo de
  bloqueio D15, cargas (R9; R10 com a chave MOS6; modelo da bateria S_bat, R22, C2, VDC1) e o
  divisor R11, R12 com o seguidor OP_AMP3.
- **No meio**, o amplificador diferencial do shunt (OP_AMP2) e o compensador de corrente
  (OP_AMP14), com a referência VDC3 = `Vrefi`.
- **Embaixo**, o compensador de tensão (OP_AMP1, referência VDC2), o nó da tensão de controle
  (R7, D6, R17, grampo DZ, voltímetro V9) e o modulador (COMP3 e a portadora VTRI1).
- **À direita**, os comandos da carga (VSQ3 e `hab_bat`), o bloco **Medidas**, que leva 28 sinais à
  porta de saída **Out** (lida pelo RPC), e os osciloscópios.
- A saída do seguidor chega ao compensador de tensão pelo rótulo elétrico **Hv**, e o PWM chega às
  chaves pelo rótulo de sinal **pwm**.

## Decisões de modelagem (e por quê)

| Ponto | Como foi feito | Motivo |
|---|---|---|
| Dispersão do transformador | indutor `Lk` = 0,109 µH em série com o secundário | o PSIM do professor tem 0,1 µH por enrolamento; sem ela o PLECS acusa "state/source dependence" na comutação D1/D2 |
| Diodos da ponte | `Ron` = 5 mΩ | o PLECS não aceita fonte ideal em paralelo com C1 por chaves ideais |
| Magnetizante | indutor explícito `Lm` em paralelo com o primário | acesso direto à corrente magnetizante |
| Amplificadores operacionais | *Lim. Op-Amp* da biblioteca, ganho 1e5, saída de 0 a 5 V | iguais aos do PSIM (5 / 0); a saturação é essencial para o comportamento das malhas |
| Grampo de vc | *Zener Diode* de 1,95 V (`Dmax` = 0,48) | valor ilegível no esquemático do professor |
| C1 | 940 µF | valor adotado na planilha (o esquemático mostra 470 µF) |
| C2 (bateria) | 0,8 F | reproduz o tempo de recarga da Fig. 17 (o esquemático mostra 400 mF) |
| Medidores | *Probes* no lugar dos voltímetros e amperímetros do PSIM | menos fios; só V11, Vbat e V9 são voltímetros |

## O que foi aprendido sobre o formato .plecs (complementa o Trabalho 2)

- Componentes de biblioteca entram como `Type Reference` com `SrcComponent
  "Components/Electrical/Electronics/Lim. Op-Amp"` (portas: 1 = +, 2 = −, 3 = saída, 4 = terra) e
  `".../Power Semiconductors/Z1"` (zener: 1 = catodo, 2 = anodo), repetindo os blocos `Terminal`.
- Porta de saída de nível superior (`Type Output`) precisa também de um bloco `Terminal { Type
  Output; Index "1" }` no cabeçalho do modelo; sem ele `plecs.simulate` devolve listas vazias.
- Num `PlecsProbe`, cada componente aparece uma única vez, e a ordem dos sinais é a do PLECS
  (diodo e capacitor: tensão, corrente; indutor: corrente, tensão), não a escrita no arquivo.
- `Comparator`: 1 = entrada +, 2 = entrada −, 3 = saída. `TriangleGenerator`: `Min`, `Max`, `f`,
  `DutyCycle`, `Delay`. `ACVoltageSource`: `V`, `w`, `phi`. Rótulo elétrico: `Type Label`, `Tag`.
- Pelo RPC, `ModelVars` substitui as variáveis depois dos comandos de inicialização: variáveis
  derivadas (`Vpk`, `R9` ...) precisam ser enviadas já calculadas (ver `variaveis()` em
  `rodar_ensaios.py`). `OutputTimes` com `OutputTimesOption = "range"` devolve todos os passos do
  integrador numa janela.
- A biblioteca do próprio PLECS (`components.plecs`) e os demos da instalação são a referência
  para tipos e parâmetros.

## Regenerar o modelo

```bash
python "simulação PLECS/gerador/gerar_carregador.py" --previa
```

Regenerar **sobrescreve** `carregador.plecs`. Se o desenho for arrumado à mão para a captura,
salve com outro nome (por exemplo `carregador-arrumado.plecs`). `--previa` grava
`gerador/previa_carregador.png`, um rascunho do roteamento.

## Captura do esquemático

O PLECS só exporta o esquemático pela interface: *File › Export › PNG*. A captura usada no artigo
(Fig. 15) é `simulacao-circuitos/plecs-circ-carregador.png`, feita pelo usuário em 11/10/2026 sobre
o desenho gerado pelo script. Para trocá-la, exportar de novo com o mesmo nome e regenerar o artigo
(`artigo/fonte/montar_figuras.py` troca o fundo amarelo por branco).
