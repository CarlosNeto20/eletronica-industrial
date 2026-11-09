# 08. Resultados de simulação

**Situação: pendente de execução no PLECS.** Os modelos, o executor e o analisador estão prontos, mas nenhum CSV do PLECS foi gravado ainda em `resultados PLECS`. Enquanto isso não ocorrer, nenhum resultado de simulação (classe S) é apresentado neste memorial nem no artigo.

Para executar, abrir o PLECS com a interface RPC habilitada na porta 1080 e rodar, na pasta Trabalho 6:

```powershell
& $taskPython 'resultados PLECS\executar_ensaios.py' --teste
& $taskPython 'resultados PLECS\executar_ensaios.py' --todos
& $taskPython 'resultados PLECS\analisar_resultados.py'
```

Depois da execução, este arquivo passa a trazer, para cada ensaio, as janelas usadas, médias, eficazes e picos, a comparação com os valores analíticos, os critérios atendidos e não atendidos e as limitações.

Próximo arquivo: [09. Componentes e melhorias](09-componentes-e-melhorias.md).
