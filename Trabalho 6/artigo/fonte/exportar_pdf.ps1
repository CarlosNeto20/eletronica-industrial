param([string]$Arquivo = (Join-Path $PSScriptRoot '..\Trabalho6_NoBreak_3kVA.docx'))
# Alternativa ao exportar_pdf.py: exporta o DOCX para PDF pelo Microsoft Word, sem regravar o DOCX.
$taskInput = (Resolve-Path -LiteralPath $Arquivo).Path
$taskOutput = [System.IO.Path]::ChangeExtension($taskInput, '.pdf')
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
try {
  $taskDocument = $taskWord.Documents.Open($taskInput, $false, $true)
  $taskDocument.ExportAsFixedFormat($taskOutput, 17)
  $taskDocument.Close(0)
  Write-Output $taskOutput
} finally { $taskWord.Quit() }
