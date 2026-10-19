# Modelos PLECS do Trabalho 2

Quatro modelos prontos para abrir no **PLECS 5.0** (Standalone), gerados pelo script
`gerador/gerar_modelos.py` a partir do guia `desenvolvimento/07-guia-simulacao-plecs.md`.

| Arquivo | Conteúdo | Tempo simulado | CSV gravado em `resultados PLECS/` |
|---|---|---|---|
| `forward.plecs` | Forward de uma chave + Buck equivalente | 0,11 s | `forward_degrau.csv` |
| `fullbridge.plecs` | Ponte completa + Buck equivalente (40 kHz, D = 0,8) | 0,31 s | `fullbridge_degrau.csv` |
| `pushpull.plecs` | Push-pull alimentado em corrente + Boost equivalente (40 kHz, D = 0,4) | 1,3 s | `pushpull_degrau.csv` |
| `flyback.plecs` | Flyback + Buck-Boost equivalente; `kL = 1` → MCD, `kL = 10` → MCC | 0,8 s | `flyback_mcd_degrau.csv` / `flyback_mcc_degrau.csv` |

`arquivo-qualquer.plecs` é o arquivo de exemplo usado para copiar o cabeçalho da versão 5.0 e
pode ser apagado.

## Organização de cada modelo

- **Em cima**, o conversor isolado; **embaixo**, o equivalente não isolado referido ao secundário.
- **À direita, no alto**, os geradores de pulso (`PG_*`), que distribuem os comandos por blocos
  *Goto*/*From* (`g_S1`, `g_eq`, `carga` ...). Não há fios longos de comando atravessando o circuito.
- **À direita, embaixo**, o painel de medidas: um *Scope* com três gráficos (tensão de saída,
  corrente de saída e corrente no indutor, isolado × equivalente sobrepostos) e um bloco *To File*
  que grava tempo + `Vo_iso, Vo_eq, Io_iso, Io_eq, IL_iso, IL_eq` em CSV.
- **Todos os valores** estão em *Simulation › Simulation Parameters › Initialization*. Para mudar
  um valor, mude lá, e não no componente.

## Decisões de modelagem (e por quê)

| Ponto | Como foi feito |
|---|---|
| Transformador | bloco *Transformer* ideal. No Forward e no Flyback, $L_m$ é um indutor explícito em paralelo com o primário (dá acesso direto a $i_{Lm}$); na ponte e no push-pull, $L_m$ é o parâmetro do próprio bloco. |
| Terciário do Forward | segundo transformador ideal com o primário em paralelo (equivale a um transformador de 3 enrolamentos). Espiras negativas (`[Np -Nt]`) invertem a polaridade do terciário. |
| Primário com derivação central (push-pull) | dois transformadores ideais, um por metade do primário, com os secundários em paralelo. |
| Flyback | espiras negativas no secundário (`[Np -Ns]`), recurso previsto no manual do PLECS e usado em modelos de flyback publicados. |
| Ponte completa | comando da **variante B** do guia (a do professor): braços complementares, com `NOT` para as chaves inferiores. |
| Buck-Boost equivalente | saída negativa em relação ao terra; o estágio de saída usa o terra como barramento positivo e o voltímetro lê +54 V. |
| Dispersão e grampeador RCD | omitidos (ver guia, seções 7.2 e 12). |
| Forward, equivalente | `Vi_eq = Vi·Ns/Np` = 136 V, coerente com as espiras 100:68 do professor. Com 100:67,5 dá 135 V. |

## Primeira abertura: o que conferir

1. **O arquivo abre sem erro.** Se o PLECS reclamar de algum parâmetro ou componente, anote a
   mensagem exata: o formato foi montado sem acesso a uma instalação do PLECS, a partir de modelos
   públicos e do manual, e qualquer ajuste vira uma correção no gerador.
2. **Simulation › Start.** O *Scope* abre com os três gráficos.
3. **Regime a 100 % (antes do primeiro degrau):** $V_o$ ≈ 54 V (400 V no push-pull, ≈ 57 V no
   Flyback em MCD), com as curvas do isolado e do equivalente sobrepostas.
4. **Sinal das correntes.** Se $I_o$ aparecer negativo, o amperímetro está com o sentido invertido
   em relação ao que o gerador supôs: gire o amperímetro 180° no esquemático ou avise para
   corrigir no gerador.
5. **Janela de observação dos degraus:** use a lupa do *Scope* nas janelas indicadas na seção 8 do
   guia. O CSV é gravado automaticamente a cada simulação.

## Regenerar os modelos

```bash
cd "simulação PLECS/gerador"
python gerar_modelos.py
```

O script também confere que todo terminal está ligado exatamente uma vez. Regenerar
**sobrescreve** os `.plecs`; se alguém arrumar o desenho à mão no PLECS, salve com outro nome.
