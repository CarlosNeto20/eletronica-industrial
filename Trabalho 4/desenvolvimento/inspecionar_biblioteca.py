from pathlib import Path
import re, json
INSTALL=Path(r'C:\Users\Carlos Neto\Documents\Plexim\PLECS 5.0 (64 bit)')
def blocks(text, kind='Component'):
    pat=re.compile(r'\b'+kind+r'\s*\{')
    for m in pat.finditer(text):
        i=m.end(); depth=1; quote=False; escape=False
        while depth and i<len(text):
            c=text[i]
            if quote:
                if escape: escape=False
                elif c=='\\': escape=True
                elif c=='"': quote=False
            elif c=='"': quote=True
            elif c=='{': depth+=1
            elif c=='}': depth-=1
            i+=1
        yield text[m.start():i]
if __name__=='__main__':
    types={'Transformer','CScript','Output','SignalMux','Comparator','TriangleGenerator','SawtoothGenerator','VoltageSource','CurrentSource','ACVoltageSource','Switch','Ammeter','Ground'}
    found={}
    for p in [INSTALL/'components.plecs',*list((INSTALL/'demos').rglob('*.plecs'))]:
        for b in blocks(p.read_text(encoding='utf-8')):
            m=re.match(r'Component\s*\{\s*Type\s+(\S+)',b)
            if m and m[1] in types and m[1] not in found:
                found[m[1]]=b
        if len(found)==len(types): break
    out=Path(__file__).parent/'blocos_biblioteca.json'
    out.write_text(json.dumps(found,indent=2),encoding='utf-8')
    for t,b in found.items():
        print(t, re.findall(r'Variable\s+"([^"]+)"\s+Value\s+"([^"\n]*)"',b)[:25])
