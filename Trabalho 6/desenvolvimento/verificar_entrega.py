"""Conferencia final da entrega do Trabalho 6.

Verifica: execucao e hashes de cada ensaio PLECS (modelo, CSV, retorno nativo, duracao e amostras),
estabilidade do laco nos pontos calculados, preservacao do template, estrutura do DOCX (autores,
equacoes OMML, figuras, ausencia de texto do template), formato A4 e paginas do PDF, origem das
figuras de resultado (CSV registrado) e presenca, no texto do artigo, de numeros recalculados
diretamente de parametros.json e metricas.json. Grava verificacao_entrega.json e o manifesto.
Uso: python desenvolvimento/verificar_entrega.py
"""
from pathlib import Path
import json, hashlib, re, zipfile, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'resultados PLECS'
SIM = ROOT / 'simulação PLECS'
sys.path.insert(0, str(ROOT / 'artigo' / 'fonte'))
SHA_TPL = '9d0153f7121508f585eff77c6fc112234a9d289c0390bf54a5296d15d01b04d3'
SHA_BASE = '13c61562adcebe923f7799adee904e8f76fc7c3670352634d84cefb713cb2f9a'
falhas, avisos = [], []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def checa(cond, msg):
    if not cond:
        falhas.append(msg)
    return cond


def texto_pdf(pdf):
    try:
        import fitz
        d = fitz.open(pdf)
        return [p.get_text() for p in d], [(p.rect.width, p.rect.height) for p in d]
    except ImportError:
        pass
    exe = shutil.which('pdftotext')
    info = shutil.which('pdfinfo')
    if exe and info:
        out = subprocess.run([info, '-f', '1', '-l', '99', str(pdf)], capture_output=True, text=True).stdout
        tam = [tuple(float(x) for x in m) for m in re.findall(r'Page\s+\d+ size:\s+([\d.]+) x ([\d.]+)', out)]
        txt = subprocess.run([exe, '-layout', str(pdf), '-'], capture_output=True, text=True).stdout.split('\f')
        return [t for t in txt if t.strip()], tam
    raise RuntimeError('instale PyMuPDF ou poppler (pdftotext/pdfinfo)')


# 1. Ensaios -----------------------------------------------------------------
ENS = json.loads((SIM / 'ensaios.json').read_text(encoding='utf-8'))
ensaios, pendentes = [], []
for nome, e in ENS.items():
    log = RES / f'{nome}_execucao.json'
    if not log.exists():
        pendentes.append(nome)
        continue
    r = json.loads(log.read_text(encoding='utf-8'))
    if r.get('status') != 'executado':
        pendentes.append(nome)
        continue
    csv = RES / f'{nome}.csv'
    ok = checa(csv.exists() and r['sha256_csv'] == sha(csv), f'{nome}: hash do CSV')
    ok &= checa(r['sha256_modelo'] == sha(SIM / f"{e['modelo']}.plecs"), f'{nome}: hash do modelo difere do executado')
    ok &= checa(abs(r['tempo_final_s'] - e['TimeSpan']) < 1e-9, f'{nome}: duracao')
    ok &= checa(r['amostras'] == csv.read_bytes().count(b'\n') - 1, f'{nome}: amostras')
    ok &= checa((RES / f'{nome}_rpc.json.gz').exists(), f'{nome}: retorno nativo ausente')
    ensaios.append(dict(ensaio=nome, modelo=e['modelo'], amostras=r['amostras'], ok=bool(ok)))
checa(sha(SIM / 'arquivo_exemplo.plecs') == SHA_BASE, 'arquivo-base do PLECS alterado')

# 2. Calculos -----------------------------------------------------------------
P = json.loads((ROOT / 'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
for nome, pt in P['malha']['pontos'].items():
    checa(pt['estavel_malha_fechada'], f'laco instavel em {nome}')
    checa(len(pt['cruzamentos_0dB']) == 1, f'mais de um cruzamento por 0 dB em {nome}')

# 3. Artigo -------------------------------------------------------------------
import conteudo as C
tpl = ROOT / 'documentos de referência' / 'template-a4.docx'
docx = ROOT / 'artigo' / (C.ARQUIVO + '.docx')
pdf = docx.with_suffix('.pdf')
art = {}
checa(sha(tpl) == SHA_TPL, 'template alterado')
if checa(docx.exists() and pdf.exists(), 'artigo .docx/.pdf ausente'):
    from lxml import etree
    with zipfile.ZipFile(tpl) as a, zipfile.ZipFile(docx) as b:
        for n in ('word/styles.xml', 'word/numbering.xml', 'word/theme/theme1.xml', 'word/settings.xml', 'word/fontTable.xml'):
            checa(a.read(n) == b.read(n), f'parte do template alterada: {n}')
        raiz = etree.fromstring(b.read('word/document.xml'))
    txt = ''.join(raiz.xpath('//*[local-name()="t"]/text()'))
    n_eq = len(raiz.xpath('//*[local-name()="oMathPara"]'))
    n_fig = len(raiz.xpath('//*[local-name()="drawing"]'))
    checa('Jonatas Manoel Assunção Felix' in txt and 'Jose Carlos Moreira de Brito Neto' in txt, 'autores ausentes')
    checa('539729' in txt and '536962' in txt, 'matriculas ausentes')
    checa(not any(s in txt.lower() for s in ('paper title', 'given name', 'insert here', 'xxx-x-xxxx', 'name of organization')), 'texto do template remanescente')
    checa(n_eq >= 6, 'menos de seis equacoes editaveis')
    checa('—' not in txt, 'travessao no texto do artigo')
    paginas, tamanhos = texto_pdf(pdf)
    checa(6 <= len(paginas) <= 8, f'artigo com {len(paginas)} paginas (esperado 6 a 8)')
    checa(all(abs(w - 595.3) < 2 and abs(h - 841.9) < 2 for w, h in tamanhos), 'pagina fora do A4')
    tudo = '\n'.join(paginas)
    for i in range(1, n_fig + 1):
        checa(re.search(r'Fig\.\s*' + str(i) + r'\.', tudo) is not None, f'legenda da Fig. {i} ausente no PDF')
    # numeros recalculados diretamente dos JSON (independentes do texto)
    def fm(x, n):
        return f'{x:.{n}f}'.replace('.', ',').replace('-', '−')
    R = P['retificador']['planilha']
    esperados = {'Ichg': fm(R['Ichg'], 2), 'C1 mF': fm(R['C1_F'] * 1e3, 3), 'Lo': fm(P['inversor']['Lo'] * 1e6, 1),
                 'dILo': fm(P['inversor']['dILo_real_373'], 2), 'MF': fm(P['malha']['MF_projeto'], 1), 'Av': fm(abs(P['malha']['Av_dB']), 2),
                 'VC8': '140', 'f0': fm(P['inversor']['f0_LC'], 0)}
    mt = RES / 'metricas.json'
    if mt.exists():
        M = json.loads(mt.read_text(encoding='utf-8'))
        for V, ent in M.get('regulacao', {}).items():
            if 'RV_pct' in ent:
                esperados[f'RV {V}'] = fm(ent['RV_pct'], 2)
        figs_res = set(M.get('_figuras', []))
        usadas = {Path(b[1]).stem for b in C.blocos() if b[0] == 'fig'}
        for fnome in usadas - {'arquitetura', 'circuito_cc', 'bode_laco', 'bode_planta', 'bode_compensador'}:
            checa(fnome in figs_res, f'figura {fnome} sem origem registrada em metricas.json')
    for k, v in esperados.items():
        checa(v in txt, f'numero {k} = {v} ausente do texto do artigo')
    art = dict(paginas=len(paginas), equacoes_editaveis=n_eq, figuras=n_fig, docx_sha256=sha(docx), pdf_sha256=sha(pdf),
               numeros_conferidos=esperados)

rel = dict(ensaios_executados=len([e for e in ensaios if e['ok']]), ensaios_pendentes=pendentes, ensaios=ensaios,
           artigo=art, falhas=falhas, avisos=avisos,
           nota='Conferencia automatica de rastreabilidade e integridade; a revisao visual fica em artigo/qa/revisao_visual.md. Nao certifica hardware.')
(ROOT / 'desenvolvimento' / 'verificacao_entrega.json').write_text(json.dumps(rel, indent=1, ensure_ascii=False), encoding='utf-8')

# 4. Manifesto ----------------------------------------------------------------
# 'layout_anterior' guarda os .plecs antes da reorganizacao do desenho, so como referencia
# de conferencia; 'qa' e 'qa_fonte' tem material restrito, do qual so a revisao visual entra.
restritos = {'qa', 'qa_fonte', '__pycache__', 'testes', 'layout_anterior'}
manifesto = {}
for pasta in ('desenvolvimento', 'simulação PLECS', 'resultados PLECS', 'artigo'):
    for p in sorted((ROOT / pasta).rglob('*')):
        if not p.is_file() or p.name in ('extracao_restrita.txt',):
            continue
        if restritos & set(p.parts) and p.name != 'revisao_visual.md':
            continue
        manifesto[str(p.relative_to(ROOT)).replace('\\', '/')] = dict(bytes=p.stat().st_size, sha256=sha(p))
for extra in ('LEIA-ME-ENTREGA.md', 'README.txt', '.gitignore'):
    if (ROOT / extra).exists():
        manifesto[extra] = dict(bytes=(ROOT / extra).stat().st_size, sha256=sha(ROOT / extra))
(ROOT / 'manifesto_entrega.json').write_text(json.dumps(manifesto, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'{rel["ensaios_executados"]} ensaios conferidos, {len(pendentes)} pendentes, {len(falhas)} falhas; {len(manifesto)} arquivos no manifesto.')
for x in falhas:
    print('FALHA:', x)
sys.exit(1 if falhas else 0)
