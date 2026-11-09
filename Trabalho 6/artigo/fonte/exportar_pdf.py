"""Exporta o artigo .docx para PDF com o LibreOffice (soffice) e renderiza as paginas para revisao.

O LibreOffice precisa do componente Math (pacote libreoffice-math no Linux; incluido no
instalador do Windows) para desenhar as equacoes OMML. Alternativa com Microsoft Word:
artigo/fonte/exportar_pdf.ps1. As imagens de revisao vao para artigo/qa/ (fora da entrega publica).
Uso: python artigo/fonte/exportar_pdf.py [--soffice caminho]
"""
from pathlib import Path
import argparse, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import conteudo as C

a = argparse.ArgumentParser()
a.add_argument('--soffice', default=shutil.which('soffice') or shutil.which('libreoffice') or r'C:\Program Files\LibreOffice\program\soffice.exe')
a.add_argument('--dpi', type=int, default=110)
args = a.parse_args()
docx = ROOT / 'artigo' / (C.ARQUIVO + '.docx')
pdf = docx.with_suffix('.pdf')
with tempfile.TemporaryDirectory() as tmp:
    perfil = Path(tmp) / 'perfil'
    cmd = [args.soffice, f'-env:UserInstallation=file:///{perfil.as_posix().lstrip("/")}', '--headless',
           '--convert-to', 'pdf', '--outdir', tmp, str(docx)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    gerado = Path(tmp) / pdf.name
    if not gerado.exists():
        sys.exit('falha na conversao: ' + r.stdout + r.stderr)
    shutil.copy2(gerado, pdf)
print(pdf)
qa = ROOT / 'artigo' / 'qa'
qa.mkdir(exist_ok=True)
pdftoppm = shutil.which('pdftoppm')
if pdftoppm:
    for antigo in qa.glob('pagina-*.png'):
        antigo.unlink()
    subprocess.run([pdftoppm, '-r', str(args.dpi), '-png', str(pdf), str(qa / 'pagina')], check=True)
    print('paginas renderizadas em', qa)
else:
    try:
        import fitz
        d = fitz.open(pdf)
        for i, pg in enumerate(d, 1):
            pg.get_pixmap(dpi=args.dpi).save(qa / f'pagina-{i:02d}.png')
        print('paginas renderizadas em', qa)
    except ImportError:
        print('pdftoppm e PyMuPDF ausentes; renderize as paginas manualmente para a revisao visual')
