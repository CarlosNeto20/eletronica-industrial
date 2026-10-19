# Trabalho 3. Carregador de Baterias de 15 A Baseado no Conversor Forward de Duas Chaves

**Disciplina:** Eletrônica Industrial (UFC, Prof. Dr. René Pastor Torrico-Bascopé)
**Autores:** Jonatas Manoel Assunção Felix (539729) e Jose Carlos Moreira de Brito Neto (536962)
**Enunciado:** `documento explicativo/Forward_Carregador_Planilha_2026.pdf` (a "planilha"), convertido em
[`Trabalho03.md`](../documento%20explicativo/Trabalho03.md), e `Controle_Basico_Parte04_Anexo.pdf`
**Simulador:** PLECS Standalone 5.0.6 (Plexim), no lugar do PSIM usado pelo professor
**Entregáveis:** artigo IEEE A4 em `.docx` e `.pdf` (pasta `artigo`), modelo `.plecs`, resultados
exportados e este memorial

## O que este material é

A planilha do professor já traz o projeto resolvido: capacitor do barramento, relação de espiras,
filtro de saída, as duas malhas de controle pelo fator K e três ensaios no PSIM com a rede em 176 V.
O trabalho consiste em conferir tudo isso, desenvolver o que falta e reproduzir as simulações no
PLECS, também em 264 V. O que foi acrescentado à planilha:

- topologia, etapas de operação e formas de onda teóricas do Forward de duas chaves;
- esforços e escolha dos diodos da ponte e dos semicondutores do Forward, com os datasheets;
- análise dos laços com os componentes comerciais realmente usados na simulação;
- circuito de controle com o UC3525A adaptado para 50 kHz e lista de componentes;
- os três ensaios em 176 V e em 264 V, o regime permanente (retificador, fator de potência,
  esforços) e os cinco períodos de portadora e moduladora;
- conclusão.

## Organização do material

| Documento | Conteúdo |
|---|---|
| [00. Índice do projeto](00-indice-do-projeto.md) | Este arquivo: visão geral, parâmetros, divergências, fluxo de trabalho |
| [01. Especificações e retificador](01-especificacoes-e-retificador.md) | Seções I a IV do artigo: bateria, rede e retificador com filtro capacitivo |
| [02. Forward de duas chaves](02-forward-de-duas-chaves.md) | Seção V: topologia, etapas, projeto, esforços e componentes comerciais |
| [03. Circuito de controle](03-circuito-de-controle.md) | Seção VI: fator K, as duas malhas, UC3525A e lista de componentes |
| [04. Resultados de simulação](04-resultados-de-simulacao.md) | Seção VII: modelo, regime, degrau, curto, recarga e comparação com o professor |
| [05. Conclusões e referências](05-conclusoes-e-referencias.md) | Seção VIII e bibliografia |
| `calculos/parametros_projeto.py` | Confere todos os números da planilha e calcula as extensões (176 V e 264 V) |
| `figuras/` | Figuras desenhadas (`fwd2-*`), Bode (`calc-*`), datasheets (`ds-*`) e resultados (`plecs-*`) |
| `../simulação PLECS/LEIA-ME.md` | Guia do modelo PLECS: ensaios, decisões de modelagem, formato do arquivo |
| `../resultados PLECS/metricas_ensaios.md` | Todas as métricas medidas nas simulações |

Os documentos 01 a 05 são gerados por `artigo/fonte/exportar_markdown.py` a partir do texto do
artigo (`artigo/fonte/conteudo.py`), para que memorial e artigo nunca divirjam.

## Parâmetros consolidados

| Grupo | Grandeza | Valor |
|---|---|---|
| Bateria | Capacidade; tensão | 150 Ah; 20 V a 27 V |
| | Corrente de recarga; potência | 15 A (0,1 C); 405 W |
| Rede | Tensão; frequência | 220 V (176 V a 264 V); 60 Hz |
| Retificador | Ondulação de projeto; ângulo de condução | 10 % (24,89 V); 0,451 rad |
| | C1 calculado / adotado | 545,7 µF / 940 µF (2 × 470 µF, TDK B43658) |
| | Ponte | GBU8J (600 V, 8 A) |
| Forward | Barramento; saída | 225 V a 373 V; 27 V, 15 A |
| | fs; Dmax; Dmin | 50 kHz; 0,4; 0,241 |
| | n = Ns/Np; Lm (simulação) | 0,3 (100 : 30); 20 mH |
| | Lo; Co; Rse | 136,6 µH; 2200 µF (EPCOS B41821); 0,11 Ω |
| | Chaves; desmagnetização; secundário | IRFP460; UF4005; VS-MUR3020WT |
| Controle | Vrefv; Vrefi; Rsh; ganho diferencial | 2,5 V; 0 a 2,5 V; 10 mΩ; 16,7 |
| | Divisor de tensão | 100 kΩ + 10,2 kΩ (27,01 V) |
| | Compensador de tensão | R13 = 10 kΩ; R14 = 82 kΩ; C5 = 1,5 nF; C6 = 100 pF |
| | Compensador de corrente | R16 = 10 kΩ; R18 = 18 kΩ; C7 = 2,7 nF; C8 = 220 pF |
| | Portadora | triangular, 0,8 V a 3,2 V, 50 kHz |

## Resultados principais (PLECS)

| Grandeza | 176 V | 264 V | Professor (PSIM, 176 V) |
|---|---|---|---|
| Fator de potência | 0,405 | 0,335 | "menor que 0,5" |
| Ondulação em C1 | 14,0 V | 9,6 V | — |
| Razão cíclica | 0,396 | 0,259 | — |
| Vale de tensão, 20 → 100 % | 25,62 V | 25,62 V | ≈ 25,7 V |
| Pico de tensão, 100 → 20 % | 29,33 V | 29,47 V | ≈ 28,3 V |
| Idem, com folga de 4 % no limite | 28,42 V | 28,44 V | — |
| Corrente em curto-circuito | 14,97 A | 14,97 A | ≈ 15 A |
| Fim da recarga em corrente constante | 0,378 s | 0,379 s | ≈ 0,375 s |

## Divergências encontradas no material do professor

Registradas para que o texto as trate de forma consciente, e não as reproduza.

1. **Ganho do compensador de corrente lido na frequência errada.** A planilha calcula
   `Ai_dB = 20 log|FTLAsci(fcv·2π)| = 6,343 dB`, isto é, em 5 kHz, e o texto fala em "atenuação
   de −6,34 dB". Na frequência de cruzamento pretendida, fci = 12,5 kHz, o laço sem compensador
   tem −1,64 dB. Com os valores da planilha o laço cruza em 20,0 kHz, com margem de fase de 57,4°
   (a planilha informa 60,3°, que é a fase em 12,5 kHz). Valores corretos: R2 = 13,05 kΩ,
   C1 = 3,57 nF, C2 = 288 pF.
2. **Componentes do compensador de corrente.** A planilha calcula 22,39 kΩ, 2,104 nF e 165,8 pF;
   o esquemático usa 18 kΩ, 2,7 nF e 220 pF (os comerciais mais próximos seriam 22 kΩ, 2,2 nF e
   180 pF). A simulação segue o esquemático.
3. **Amplitude da portadora.** A planilha usa VD = 2,1 V; o esquemático usa uma triangular de
   2,4 V pico a pico (0,8 V a 3,2 V). A simulação segue o esquemático; o ganho dos laços cai 12,5 %.
4. **Capacitor do barramento.** A planilha adota 940 µF (2 × 470 µF); o esquemático mostra
   C1 = 470 µF. A simulação usa 940 µF.
5. **Capacitor do modelo da bateria.** O esquemático mostra C2 = 400 mF, mas a Fig. 17 (recarga em
   0,375 s) só é reproduzida com 0,8 F. A simulação usa 0,8 F.
6. **Fonte de entrada.** O esquemático usa 248 V de pico; o valor exato para 176 V é 248,9 V. A
   simulação usa √2·Vrede.
7. **Carga nominal igual ao limite de corrente.** Com 1,8 Ω a malha de tensão pede 15,006 A e o
   limite é 14,97 A (ganho 16,7 em vez de 16,667). No PLECS a malha de corrente assume e o
   compensador de tensão satura, o que eleva o pico na retirada de carga para 29,3 V. A figura do
   professor mostra ≈ 28,3 V, compatível com a malha de tensão no comando. Com Vrefi = 2,6 V o
   PLECS reproduz 28,4 V.
8. **Zener da tensão de controle.** O valor não é legível no esquemático. Adotado 1,95 V
   (Dmax = 0,48).
9. **Numeração.** Há duas "Fig. 8" e dois "Passo No8" na seção 6.1, e "Fig. 13" tem a legenda
   "FTLAccv" no lugar de "FTLAcci".

## Convenções

**Relação de espiras:** n = Ns/Np, secundário sobre primário. **Designadores:** os da Fig. 14 do
professor no modelo e nos resultados; nas figuras de topologia do Forward usam-se S1, S2 (chaves),
D1, D2 (desmagnetização), D3 (retificador) e D4 (roda livre), que no modelo são MOS3, MOS1, D4,
D3, D2 e D1. **Vírgula decimal** no texto e nas tabelas; ponto no código e no PLECS.

## Fluxo de trabalho

```
 planilha do professor (PDF) --> calculos/parametros_projeto.py  (conferência e extensões)
                                        |
 simulação PLECS/gerador/gerar_carregador.py --> carregador.plecs
                                        |
 resultados PLECS/rodar_ensaios.py (RPC) --> CSV --> analisar_ensaios.py --> figuras e métricas
                                        |
 artigo/fonte: montar_figuras.py -> omml_gen.py -> build_docx.py -> exportar_pdf.ps1
                                        |
 artigo/fonte/exportar_markdown.py --> desenvolvimento/01 a 05
```

O estado corrente e as pendências ficam em `../PROXIMOS-PASSOS.md`.
