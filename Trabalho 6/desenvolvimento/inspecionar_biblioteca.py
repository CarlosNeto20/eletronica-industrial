"""Extrai da instalacao do PLECS 5.0 um exemplo literal de cada tipo de bloco usado nos modelos.

Fonte: demos e components.plecs da pasta de instalacao. O resultado (blocos_biblioteca.json)
serve de referencia de sintaxe para gerar_modelos.py e conferir_modelos.py.
Uso: python desenvolvimento/inspecionar_biblioteca.py [caminho_da_instalacao]
"""
from pathlib import Path
import re, json, sys

PADRAO = Path(r'C:\Users\Carlos Neto\Documents\Plexim\PLECS 5.0 (64 bit)')
INSTALL = Path(sys.argv[1]) if len(sys.argv) > 1 else PADRAO
TIPOS = ['ACVoltageSource', 'DCVoltageSource', 'Switch', 'Ammeter', 'Voltmeter', 'Resistor', 'Inductor', 'Capacitor',
         'Diode', 'MosfetWithDiode', 'Transformer', 'Ground', 'TriangleGenerator', 'Comparator', 'Constant', 'CScript', 'Output']


def blocos(texto, tipo='Component'):
    for m in re.finditer(r'\b' + tipo + r'\s*\{', texto):
        i, nivel, aspas, esc = m.end(), 1, False, False
        while nivel and i < len(texto):
            c = texto[i]
            if aspas:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == '"':
                    aspas = False
            elif c == '"':
                aspas = True
            elif c == '{':
                nivel += 1
            elif c == '}':
                nivel -= 1
            i += 1
        yield texto[m.start():i]


if __name__ == '__main__':
    achados = {}
    for p in [*sorted((INSTALL / 'demos').rglob('*.plecs')), INSTALL / 'components.plecs']:
        for b in blocos(p.read_text(encoding='utf-8', errors='replace')):
            m = re.match(r'Component\s*\{\s*Type\s+(\S+)', b)
            if m and m[1] in TIPOS and m[1] not in achados and len(b) < 30000:
                achados[m[1]] = dict(fonte=str(p.relative_to(INSTALL)).replace('\\', '/'),
                                     parametros=re.findall(r'Variable\s+"([^"]+)"', b), bloco=b)
        if len(achados) == len(TIPOS):
            break
    saida = Path(__file__).parent / 'blocos_biblioteca.json'
    saida.write_text(json.dumps(achados, indent=1, ensure_ascii=False), encoding='utf-8')
    for t in TIPOS:
        print(t, achados.get(t, {}).get('fonte', 'NAO ENCONTRADO'), achados.get(t, {}).get('parametros'))
