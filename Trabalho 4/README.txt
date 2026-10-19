TRABALHO 4 — ELETRÔNICA INDUSTRIAL
Projeto de um carregador de baterias de 15 A baseado no conversor Forward de duas chaves

Disciplina: Eletrônica Industrial (UFC)
Professor: Prof. Dr. René Pastor Torrico-Bascopé
Discentes:
  Jonatas Manoel Assunção Felix — 539729
  Jose Carlos Moreira de Brito Neto — 536962

1. OBJETIVO

Completar, verificar e documentar o projeto de um carregador de baterias estacionárias de até 15 A, alimentado por retificador em ponte com filtro capacitivo e baseado no conversor CC-CC Forward de duas chaves. O projeto deve incluir os cálculos, o circuito de controle, a simulação no PLECS, a análise dos resultados e um artigo final no formato IEEE A4.

2. FONTES E CRITÉRIOS

- Documento principal do professor: "documento explicativo/Forward_Carregador_Planilha_2026.pdf". Ele apresenta o desenvolvimento parcial, os valores de projeto, as figuras e os resultados de referência. Conferir equações, unidades, hipóteses e coerência dos valores antes de reproduzi-los. Registrar e justificar qualquer correção ou adaptação.
- Modelo do artigo: "documentos de referência/template-a4.docx".
- Arquivo-base do PLECS: será fornecido posteriormente para identificar a versão e orientar a edição dos modelos. Sua ausência atual não deve ser tratada como simulação concluída.
- Trabalhos anteriores: consultar os repositórios GitHub acessíveis para identificar e aprimorar o padrão de organização, documentação, figuras e entrega, sem importar resultados técnicos indevidos para este projeto.
- O PDF do professor contém aviso de circulação restrita. Não publicar nem repassar o arquivo ou reproduções extensas sem autorização.

3. ESCOPO TÉCNICO

O documento do professor parte de uma bateria estacionária de 20 a 27 V, corrente de recarga ajustável de 0 a 15 A e referência de corrente de 0 a 2,5 V. Considera rede de 220 V, 60 Hz, com faixa de 176 a 264 V. Desenvolver e verificar, na sequência do material:

  1) especificações e retificador em ponte com filtro capacitivo;
  2) dimensionamento do conversor Forward de duas chaves e dos componentes de saída;
  3) modelagem e projeto das malhas de tensão e de corrente, incluindo compensadores e diagramas de Bode;
  4) modelo completo no PLECS e ensaios de degrau de carga (20% ↔ 100%), curto circuito e recarga com modelo de bateria;
  5) análise crítica dos cálculos e das formas de onda, conclusões e referências.

As sugestões finais do professor (outro conversor isolado, retificador adicional, esquemático com UC-3525A, lista de componentes e cinco períodos dos sinais PWM) são oportunidades de melhoria. Avaliar viabilidade e relevância, sem confundi-las com os resultados centrais já descritos no documento.

4. SIMULAÇÃO E RESULTADOS

O material do professor usa PSIM, ao qual não temos acesso. Todas as simulações deste trabalho devem ser feitas no PLECS (Plexim). Criar em "desenvolvimento" um guia .md reproduzível para montagem, parametrização, medições e execução de cada ensaio. Salvar os modelos em "simulação PLECS" e exportar os sinais em .csv para "resultados PLECS". A partir dos dados exportados, conferir grandezas e produzir gráficos legíveis para o artigo. Distinguir claramente valores calculados, resultados do PDF e resultados realmente obtidos no PLECS; nunca apresentar estes últimos sem execução e evidência.

5. ORGANIZAÇÃO E ENTREGÁVEIS

  documento explicativo/     PDF-base do professor.
  documentos de referência/  Template IEEE A4 em .docx.
  desenvolvimento/           Memorial em .md com cálculos, decisões, verificações e guia do PLECS.
  simulação PLECS/           Modelos e arquivos necessários para reproduzir os ensaios.
  resultados PLECS/          CSVs, scripts de análise e gráficos provenientes das simulações.
  artigo/                    Artigo final IEEE A4 em .docx e .pdf.

O artigo deve seguir a estrutura técnica do documento do professor, com texto e figuras próprios, resultados rastreáveis, conclusões completas e referências conferidas. Entregar as versões .docx e .pdf visualmente revisadas e consistentes entre si.
