# Exporta o .docx gerado por build_docx.py para PDF usando o Microsoft Word (automação COM).
# Uso (a partir de artigo/fonte):  powershell -ExecutionPolicy Bypass -File exportar_pdf.ps1
$base = Join-Path (Split-Path -Parent $PSScriptRoot) "build"
$nome = "artigo-carregador-forward-duas-chaves"
$docx = Join-Path $base "$nome.docx"
$pdf  = Join-Path $base "$nome.pdf"
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($docx, $false, $true)
    $d.ExportAsFixedFormat([string]$pdf, 17)
    "PDF: $pdf  ($($d.ComputeStatistics(2)) páginas)"
    $d.Close([ref]0)
} finally {
    $w.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($w)
}
