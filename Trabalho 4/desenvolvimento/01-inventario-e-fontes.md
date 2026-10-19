# Inventário, método e fontes

## Estado recebido

Foram encontrados quatro arquivos de entrada: README.txt; PDF do professor com 23 páginas; template-a4.docx; arquivo_exemplo.plecs. As pastas de desenvolvimento, resultados e artigo estavam vazias. O exemplo PLECS contém somente um resistor de 1 Ω, portanto demonstra o formato 5.0, mas não contém um carregador ou ensaios executados. O executável instalado é PLECS Standalone 5.0.6, em `C:/Users/Carlos Neto/Documents/Plexim/PLECS 5.0 (64 bit)`.

O repositório remoto identificado é <https://github.com/CarlosNeto20/eletronica-industrial>. A cópia local do Trabalho 1 e o histórico (ec40b34, 4037fcd, 7a12d30) foram examinados. Adota-se seu padrão de memorial numerado, figuras próprias, fontes do artigo e entrega DOCX/PDF. Acrescentam-se dados brutos, hashes, arquivos de configuração e distinção entre cálculos e simulação. Não se reutilizam números, conclusões ou figuras técnicas de outro projeto.

## Leitura integral do documento

| Páginas | Conteúdo e uso |
|---|---|
| 1–2 | Identificação, restrição de circulação, bateria de 150 Ah, 20–27 V, 15 A, 405 W e rede 176–264 V/60 Hz |
| 3–5 | Ponte, pulsos retangulares aproximados, capacitor mínimo, esforços e seleção de 2 × 470 µF |
| 6–7 | Forward, n=0,3, Dmáx=0,4 ideal, 50 kHz, L=136,6 µH, C=2200 µF e ESR=0,11 Ω |
| 8–14 | Sensores, planta de tensão, compensador tipo II, Bodes e margens declaradas |
| 15–20 | Planta de corrente, sensor shunt, compensador tipo II, Bodes e inconsistência de frequência |
| 21 | Margens, circuito PSIM e descrição dos ensaios |
| 22 | Figuras de degrau, curto e emulação de recarga; sem arquivos de dados associados |
| 23 | Conclusões pendentes, seis referências e cinco sugestões opcionais |

A extração foi confrontada com imagens das páginas, especialmente símbolos de valor absoluto, Ω, expoentes, compensadores e conexões da figura 14. A extração textual sozinha substituía Ω por W e omitia barras de módulo. As figuras PSIM são referências qualitativas, não CSVs nem medições deste trabalho. Não foram digitalizadas para gerar supostos dados do PLECS.

## Referências verificadas em 19/10/2026

1. R. P. Torrico-Bascopé. *Projeto de um carregador de baterias de 15 A baseado no conversor Forward de duas chaves*. UFC, setembro de 2026, 23 p. Material didático restrito, arquivo local.
2. Plexim. *PLECS 5.0 Documentation — Simulation Scripts*. <https://docs.plexim.com/plecs/latest/scripting/>. Interface RPC, opções do solver e exportação.
3. Texas Instruments. *How to Approach a Power-Supply Design — Part 7*. SLVAFW4. <https://www.ti.com/lit/pdf/slvafw4>. Topologia Forward de duas chaves, reset e formas de onda.
4. Texas Instruments. *UCx52xA Regulating Pulse Width Modulators*. SLUS191D, revisão julho de 2017. <https://www.ti.com/lit/ds/symlink/uc3525a.pdf>. Oscilador, duas saídas alternadas, ciclo máximo e limites do amplificador.
5. TDK/EPCOS. *Aluminum electrolytic capacitors — B41821/B43821*, catálogo de 2013. <https://www.tdk-electronics.tdk.com/inf/20/30/db/aec_2013/B41821_B43821.pdf>. B41821F6228M***: 2200 µF/50 V, ESR máxima 0,11 Ω a 120 Hz e 20 °C; corrente nominal 1,98 A a 120 Hz e 85 °C. Não constitui garantia de ESR em 50 kHz.
6. TDK. *ETD 49/25/16 — Core and accessories*, outubro de 2022. <https://www.tdk-electronics.tdk.com/inf/80/db/fer/etd_49_25_16.pdf>. Ae=211 mm², Amin=209 mm², AL nominal N87 sem entreferro=3800 nH, janela do carretel=269,4 mm², comprimento médio de espira=86 mm.
7. Yuasa. *Maximise Performance and Longevity: The Benefits of Correctly Charging VRLA Batteries*. <https://www.yuasa.com/uk/info-hub/Benefits-of-correctly-charging-VRLA-batteries>. Tensões dependem da família, temperatura e regime; 27 V não é tensão universal de equalização.

As seis referências citadas pelo professor foram identificadas, mas somente fontes efetivamente consultadas sustentam novas afirmações. A bibliografia final não atribui consulta a catálogos antigos indisponíveis. A documentação da Plexim e os exemplos locais servem ao formato e à API, não aos resultados do carregador.

## Template

O template usa OOXML Strict, Times New Roman 10 pt no corpo, título de 24 pt, resumo de 9 pt, legendas e referências de 8 pt, A4 e duas colunas separadas por 18 pt. O bloco de autores originalmente em três colunas foi adaptado a dois autores. Removem-se apenas conteúdo instrucional, autores fictícios, caixa de figura exemplo e copyright fictício. A renderização de referência tem três páginas. A conversão foi feita pelo Microsoft Word porque o renderizador empacotado não entende as seções Strict e não dispõe de LibreOffice. O original permanece preservado.

8. TDK. *ETD 59/31/22 — Core and accessories*, outubro de 2024. <https://www.tdk-electronics.tdk.com/inf/80/db/fer/etd_59_31_22.pdf>. Núcleo e carretel adotados no projeto final; Ae=368 mm², AL=5300 nH, janela=365,6 mm². ETD49 foi uma alternativa preliminar, não o componente final.
9. TDK. *E 65/32/27DG — Core and accessories*, outubro de 2022. <https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_65_32_27_dg.pdf>. Núcleo com entreferro distribuído, AL=100 nH, Ae=535 mm² e Amin=529 mm², adotado no indutor.
