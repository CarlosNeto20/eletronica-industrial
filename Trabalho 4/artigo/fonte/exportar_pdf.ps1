param([string]$Arquivo = (Join-Path $PSScriptRoot '..\Trabalho4_Forward_15A.docx'))
$taskInput=(Resolve-Path -LiteralPath $Arquivo).Path
$taskOutput=[System.IO.Path]::ChangeExtension($taskInput,'.pdf')
$taskWord=New-Object -ComObject Word.Application
$taskWord.Visible=$false
try {
 $taskDocument=$taskWord.Documents.Open($taskInput,$false,$true)
 $taskDocument.ExportAsFixedFormat($taskOutput,17)
 $taskDocument.Close(0)
 Write-Output $taskOutput
} finally { $taskWord.Quit() }
