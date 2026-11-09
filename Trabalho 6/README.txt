TRABALHO 6 DE ELETRÔNICA INDUSTRIAL
Projeto de um no-break de dupla conversão monofásico de 3 kVA

Disciplina: Eletrônica Industrial (UFC), código TH0263
Professor: Prof. Dr. René Pastor Torrico-Bascopé
Discentes:
  Jonatas Manoel Assunção Felix, matrícula 539729
  Jose Carlos Moreira de Brito Neto, matrícula 536962

1. OBJETIVO

Completar, verificar e documentar o projeto de um no-break de dupla conversão monofásico de 3 kVA e 2100 W, alimentado por rede de 220 V, 60 Hz (faixa de 176 a 264 V) e saída de 115 V, 60 Hz. O sistema é formado por três conversores: retificador a diodos de onda completa com filtro capacitivo, conversor CC-CC elevador de alto ganho ligado ao banco de baterias e inversor em ponte completa com modulação unipolar. O projeto deve incluir os cálculos, a malha de controle de tensão do inversor, a simulação no PLECS, a análise dos resultados e um artigo final no formato IEEE A4.

2. FONTES E CRITÉRIOS

- Documento principal do professor: "documento explicativo/Planilha_Nobreak04_2026.pdf". É uma planilha Mathcad impressa em PDF (18 páginas, outubro de 2026) com as especificações, os cálculos das seções 1 a 5 e o circuito PSIM do Anexo 01. As seções 6 (resultados de simulação) e 7 (conclusões) e as referências estão apenas indicadas, sem conteúdo. Conferir equações, unidades, hipóteses e coerência dos valores antes de reproduzi-los. Registrar e justificar qualquer correção ou adaptação. A extração de texto do PDF perde símbolos (raiz quadrada, ômega, expoentes e barras de módulo), por isso toda fórmula deve ser confrontada com a imagem da página.
- Modelo do artigo: "documentos de referência/template-a4.docx".
- Arquivo-base do PLECS: será fornecido posteriormente em "simulação PLECS" para identificar a versão e orientar a edição dos modelos. Sua ausência atual não deve ser tratada como simulação concluída.
- Trabalhos anteriores: consultar as pastas dos Trabalhos 3 e 4 (e o repositório GitHub, se acessível) para aproveitar e aprimorar o padrão de organização, documentação, geração de modelos PLECS, execução dos ensaios, análise, figuras e entrega. Reaproveitar método e infraestrutura, nunca valores, ensaios, figuras ou conclusões técnicas. O Trabalho 4 trata de um carregador Forward de 20 a 27 V e não tem relação numérica com este projeto.
- O PDF não traz aviso explícito de circulação restrita, mas é material didático do professor. Por prudência, aplicar a regra do Trabalho 4: não publicar nem repassar o arquivo, imagens de conferência ou reproduções extensas sem autorização, e mantê-los fora de qualquer repositório público.

3. ESCOPO TÉCNICO

O documento do professor parte de rede de 220 V (176 a 264 V), saída de 115 V, potência ativa de 2100 W e potência aparente de 3000 VA, banco de baterias de 42 a 56 V, rendimento de 0,933 adotado para o inversor, frequência de comutação de 20 kHz e barramento CC de 211 a 373 V. Desenvolver e verificar, na sequência do material:

  1) especificações e retificador em ponte com filtro capacitivo (seções 2 e 3);
  2) inversor monofásico em ponte completa com modulação unipolar, incluindo índices de modulação, indutor e capacitor de filtro e resistor de carga (seções 4.1 a 4.5);
  3) modelagem e projeto da malha de tensão do inversor, com compensador Tipo 3 e diagramas de Bode da planta, do compensador e do laço (seção 4.5);
  4) conversor CC-CC de alto ganho entre o banco de baterias e o barramento do inversor, com indutor Lb, tensões nos capacitores e relação de transformação (seção 5);
  5) modelo completo no PLECS e ensaios de simulação (seção 6): formas de onda em 176 V com carga não linear e em 264 V com carga linear e não linear, cada uma mostrando tensão e corrente de entrada, tensão do barramento e corrente da bateria, e tensão e corrente de saída; curvas de regulação Vo = f(Po) para 176, 220 e 264 V, com coeficiente de regulação RV;
  6) análise crítica dos cálculos e das formas de onda, conclusões e referências.

Pontos que o documento deixa em aberto ou que pedem conferência cuidadosa, a tratar como itens de auditoria e não como conclusões prévias:

  - O texto da seção 3.2 fala em ondulação de 10% do pico, mas o valor usado (37,33 V) corresponde a 15%.
  - A tensão mínima do barramento aparece como 211,6 V (retificador), 223 V (inversor) e 210 V (saída do CC-CC), e a saída do elevador precisa ser coerente com o mínimo do retificador para que a transferência rede/bateria funcione.
  - O texto do capacitor Co cita frequência de corte fs/40, enquanto a conta usa fs/20.
  - O inversor é dimensionado com 2100 W resistivos (18,26 A eficazes), mas a especificação é de 3000 VA e o circuito do Anexo 01 traz uma carga não linear, o que altera corrente eficaz, corrente de pico e esforços.
  - O texto do Passo 4 cita atenuação de 33,23 dB, enquanto o cálculo resulta em 26,22 dB.
  - A planta de tensão é avaliada com 373 V de barramento; é preciso verificar o laço no barramento mínimo e nas cargas extremas (vazio, plena carga resistiva e não linear).
  - O dimensionamento do CC-CC usa potência de 2250 W sem considerar o rendimento do próprio conversor, e a topologia (indutor, transformador, capacitores e diodos multiplicadores) deve ser identificada a partir do texto e da figura do Anexo 01, registrando a hipótese adotada.
  - Os componentes do compensador no circuito PSIM não são os valores calculados, portanto aquelas simulações não validam exatamente as funções publicadas.

As sugestões e pendências do professor (escrever as conclusões, padronizar as referências, aproveitar os dois livros dos slides da disciplina e pesquisar artigos, dissertações e teses sobre no-breaks de dupla conversão) fazem parte do trabalho. Outras melhorias, como estimativa de rendimento e perdas, distorção harmônica da tensão de saída, tempo de transferência rede/bateria, malha de corrente interna ou proteções, são oportunidades. Avaliar viabilidade e relevância, sem confundi-las com os resultados centrais já descritos no documento.

4. SIMULAÇÃO E RESULTADOS

O material do professor usa PSIM, ao qual não temos acesso. Todas as simulações deste trabalho devem ser feitas no PLECS (Plexim). Os modelos são montados e editados diretamente no arquivo de texto .plecs, a partir do arquivo-base fornecido, e executados por meio da interface RPC do PLECS Standalone (porta 1080), exportando os sinais por terminais de saída no nível superior do modelo. Não é necessário controlar mouse nem interface gráfica. Se o ambiente de trabalho não alcançar o PLECS, deixar os scripts prontos, indicar o comando exato para executá-los e manter os resultados como pendentes.

Criar em "desenvolvimento" um guia .md reproduzível para montagem, parametrização, medições e execução de cada ensaio. Salvar os modelos em "simulação PLECS" e exportar os sinais em .csv para "resultados PLECS", junto com o registro de cada execução (modelo, hash, parâmetros, solver, duração e amostras). A partir dos dados exportados, conferir grandezas e produzir gráficos legíveis para o artigo. Distinguir claramente valores calculados, resultados do PDF e resultados realmente obtidos no PLECS, e nunca apresentar estes últimos sem execução e evidência. As figuras de simulação do professor, quando existirem, são referências qualitativas e não dados.

Como a seção 6 do PDF define os ensaios apenas por título, registrar no guia a interpretação adotada para cada um, incluindo o instante e a forma de interrupção da rede para observar a corrente da bateria, a definição de carga não linear (ponte de diodos com capacitor e resistor, conforme o Anexo 01), a janela de regime usada nas médias e valores eficazes e os critérios de aceitação (por exemplo tensão de saída eficaz, índice de modulação, margem de fase e ondulação do barramento), informando com honestidade o que atende e o que não atende.

5. ORGANIZAÇÃO E ENTREGÁVEIS

  documento explicativo/     PDF-base do professor.
  documentos de referência/  Template IEEE A4 em .docx.
  desenvolvimento/           Memorial em arquivos .md numerados e encadeados (índice, inventário e fontes, auditoria do documento, retificador, inversor, malha de tensão, CC-CC elevador, guia do PLECS, resultados, componentes e melhorias), mais os scripts de cálculo e o arquivo de parâmetros que alimenta modelos e artigo.
  simulação PLECS/           Modelos e arquivos necessários para reproduzir os ensaios, incluindo o gerador dos modelos.
  resultados PLECS/          CSVs, executor dos ensaios, scripts de análise, métricas e gráficos provenientes das simulações.
  artigo/                    Artigo final IEEE A4 em .docx e .pdf, com fontes de geração e figuras.

O artigo deve seguir a estrutura técnica do documento do professor (introdução, especificações, retificador, inversor, malha de controle, conversor CC-CC, resultados de simulação, conclusões e referências), com texto e figuras próprios, resultados rastreáveis, conclusões completas e referências conferidas. Entregar as versões .docx e .pdf visualmente revisadas e consistentes entre si, acompanhadas de um LEIA-ME-ENTREGA.md na raiz com os comandos de reprodução e as limitações conhecidas.
