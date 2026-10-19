# 06. Metodologia de Validação da Equivalência

Este documento fixa como a equivalência entre cada conversor isolado e o seu equivalente não isolado
foi verificada, para que o resultado possa ser reproduzido e julgado.

## 1. Ensaio

Para cada conversor, o circuito isolado e o equivalente são simulados **no mesmo modelo PLECS**,
com os mesmos componentes de saída ($C_o$, RSE e cargas) e com o degrau de carga comandado por um
único gerador, o que garante que os dois sofrem a perturbação no mesmo instante. A carga é formada
por $R_{20} = 5R_o$ fixo em paralelo com $R_{80} = 1{,}25R_o$ chaveado por uma onda quadrada de
razão cíclica 0,5. Os dois circuitos partem do regime a 100 % de carga (condições iniciais no
script de inicialização) e passam por degraus de 100 % → 20 % e de 20 % → 100 %.

Os conversores operam em **malha aberta**, com razão cíclica fixa. Isso é intencional: o objetivo é
comparar as plantas, e qualquer controlador mascararia diferenças entre elas.

Componentes ideais: chaves e diodos sem queda nem resistência, transformador ideal com indutância
magnetizante e sem dispersão. As RSE dos capacitores são mantidas porque fazem parte do projeto.

## 2. Grandezas registradas

O bloco *To File* grava, a cada 1 ou 2 µs: tensão de saída, corrente de saída e corrente no
indutor de armazenamento, do isolado e do equivalente. A corrente no indutor do isolado é referida
ao secundário (dividida por $a$ no push-pull e no Flyback, em que o indutor está no primário).

## 3. Métricas (script `resultados PLECS/analisar_degraus.py`)

Todas as métricas usam o sinal filtrado por uma média móvel de um período de comutação, que remove
a ondulação e deixa só a dinâmica média, que é o que um modelo médio descreve.

| Métrica | Definição |
|---|---|
| Valor antes / final | média nos 2 ms anteriores ao degrau / nos últimos 5 ms (ou 1/4 do intervalo) antes do próximo evento |
| Extremo | vale de $V_o$ (pico de $I_o$) no degrau 20 → 100 %; pico de $V_o$ (vale de $I_o$) no degrau 100 → 20 % |
| Instante do extremo | medido a partir do degrau |
| Tempo de acomodação | último instante em que o sinal está fora de ±2 % do valor final |
| Erro RMS e máximo | diferença instantânea (sem filtro) isolado − equivalente, em % do valor final |

## 4. Critério de aceitação

A equivalência é considerada verificada quando, simultaneamente:

1. os valores de regime do isolado e do equivalente coincidem entre si **e** com a previsão
   analítica (ganho estático do documento 01);
2. o erro RMS isolado − equivalente é menor que 1 % em $V_o$ e $I_o$;
3. extremos e tempos de acomodação diferem em menos de 2 %.

A primeira condição é indispensável: dois circuitos podem concordar entre si e estar ambos
errados, como aconteceu na primeira execução do Forward (documento 02, seção 4).

## 5. Resultado

Os quatro conversores, e o Flyback nos dois modos de condução, cumprem os três critérios com folga
(tabela completa em `resultados PLECS/metricas_degraus.md`; resumo no documento 01, seção 4.6). O
maior erro, 0,78 % no pior instante e 0,09 % em RMS, ocorre na ponte completa e é explicado pela
corrente magnetizante.

Próximo arquivo: `07-guia-simulacao-plecs.md`.
