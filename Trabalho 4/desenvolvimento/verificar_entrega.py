"""Confere rastreabilidade dos ensaios e integridade dos documentos entregues."""
from pathlib import Path
import json,hashlib,re,zipfile
from lxml import etree
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['degrau_176','degrau_220','degrau_264','curto_220','bateria_220','ripple_original','ripple_revisado','convergencia']
records=[]
for name in names:
    log=json.loads((ROOT/'resultados PLECS'/f'{name}_execucao.json').read_text(encoding='utf8'))
    assert log['status']=='executado',name
    assert log['sha256_csv']==sha(ROOT/'resultados PLECS'/f'{name}.csv'),name
    assert log['sha256_modelo']==sha(ROOT/'simulação PLECS'/f'{log["modelo"]}.plecs'),name
    assert log['tempo_final_s']==log['opcoes']['SolverOpts']['TimeSpan'],name
    csv=ROOT/'resultados PLECS'/f'{name}.csv'
    assert log['amostras']==csv.read_bytes().count(b'\n')-1,name
    if 'grade_saida' in log:
        assert log['amostras']==round((log['grade_saida']['fim_s']-log['grade_saida']['inicio_s'])/log['grade_saida']['passo_s'])+1,name
    assert (ROOT/'resultados PLECS'/f'{name}_rpc.json.gz').stat().st_size>0
    records.append(dict(ensaio=name,amostras=log['amostras'],modelo=log['modelo'],status='hashes e duração conferidos'))
params=json.loads((ROOT/'desenvolvimento/calculos/parametros.json').read_text(encoding='utf8'))
for key in ['final_v','final_i']:
    assert params['controle'][key]['estavel_continuo']
    assert all(c['estavel_continuo'] for c in params['controle'][key]['cantos'])
tpl=ROOT/'documentos de referência/template-a4.docx';docx=ROOT/'artigo/Trabalho4_Forward_15A.docx';pdf=docx.with_suffix('.pdf')
assert sha(tpl)=='9d0153f7121508f585eff77c6fc112234a9d289c0390bf54a5296d15d01b04d3'
with zipfile.ZipFile(tpl) as a, zipfile.ZipFile(docx) as b:
    for n in ['word/styles.xml','word/numbering.xml','word/theme/theme1.xml']:assert a.read(n)==b.read(n),n
    root=etree.fromstring(b.read('word/document.xml'))
    text=' '.join(root.xpath('//*[local-name()="t"]/text()'))
    assert 'Jonatas Manoel Assunção Felix' in text and 'Jose Carlos Moreira de Brito Neto' in text
    assert len(root.xpath('//*[local-name()="oMath"]'))==10
    assert len(root.xpath('//*[local-name()="drawing"]'))==13
    assert not any(t in text.lower() for t in ['paper title','first author','insert here','xxx-x-xxxx'])
d=pymupdf.open(pdf);pt='\n'.join(p.get_text() for p in d)
assert len(d)==7
for i in range(1,14):assert re.search(r'Fig\.\s*'+str(i)+r'\.',pt),i
assert all(abs(p.rect.width-595.3)<2 and abs(p.rect.height-841.9)<2 for p in d)
report=dict(ensaios=records,artigo=dict(paginas=len(d),equacoes_editaveis=10,figuras=13,docx_sha256=sha(docx),pdf_sha256=sha(pdf)),template_preservado=True,polos_revisados_estaveis_nos_seis_pontos=True,nota='Verificação automática de integridade; a revisão visual foi registrada separadamente. Não certifica hardware.')
(ROOT/'desenvolvimento/verificacao_entrega.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
manifest={}
for folder in ['desenvolvimento','simulação PLECS','resultados PLECS','artigo']:
    for p in (ROOT/folder).rglob('*'):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(x in p.parts for x in ['qa','qa_fonte','qa_template','qa_modelos','__pycache__']):continue
        if p.name in ['extracao_restrita.txt','manifesto_entrega.json']:continue
        manifest[str(rel).replace('\\','/')]=dict(bytes=p.stat().st_size,sha256=sha(p))
(ROOT/'manifesto_entrega.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
print(f'OK: {len(records)} ensaios, {len(d)} páginas, 13 figuras, 10 equações; {len(manifest)} arquivos no manifesto.')
