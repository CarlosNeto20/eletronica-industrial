# -*- coding: utf-8 -*-
"""Atualiza as figuras do artigo no DOCX sem reconstruir o restante do documento."""
import argparse
import html
import importlib.util
import os
import re
import struct
import tempfile
import zipfile


SRC = os.path.dirname(os.path.abspath(__file__))
ARTIGO = os.path.dirname(SRC)
FIGURAS = os.path.join(ARTIGO, "figuras")
DOCX_PADRAO = os.path.join(ARTIGO, "artigo-perdas-semicondutores-trafo-af.docx")


def carregar_conteudo():
    caminho = os.path.join(SRC, "conteudo.py")
    spec = importlib.util.spec_from_file_location("conteudo", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def dimensoes_png(caminho):
    with open(caminho, "rb") as arquivo:
        cabecalho = arquivo.read(24)
    if cabecalho[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("arquivo PNG invalido: %s" % caminho)
    return struct.unpack(">II", cabecalho[16:24])


def atributo_acessivel(bloco, tag, descricao):
    padrao = re.compile(r"(<%s\b[^>]*?)(\s*/?>)" % re.escape(tag))

    def substituir(casamento):
        inicio, fim = casamento.group(1), casamento.group(2)
        if re.search(r'\bdescr="[^"]*"', inicio):
            inicio = re.sub(r'\bdescr="[^"]*"', 'descr="%s"' % descricao, inicio)
        else:
            inicio += ' descr="%s"' % descricao
        return inicio + fim

    return padrao.sub(substituir, bloco, count=1)


def atualizar_xml(documento_xml, relacionamentos_xml, figuras):
    relacoes = dict(re.findall(r'<Relationship\b[^>]*\bId="([^"]+)"[^>]*\bTarget="([^"]+)"',
                               relacionamentos_xml))
    midias = {}

    for nome, legenda in figuras:
        png = os.path.join(FIGURAS, nome + ".png")
        largura_px, altura_px = dimensoes_png(png)
        marcador = 'name="%s.png"' % nome
        inicio_marcador = documento_xml.find(marcador)
        if inicio_marcador < 0:
            raise RuntimeError("figura nao localizada no DOCX: %s" % nome)
        inicio = documento_xml.rfind("<wp:inline", 0, inicio_marcador)
        fim = documento_xml.find("</wp:inline>", inicio_marcador)
        if inicio < 0 or fim < 0:
            raise RuntimeError("bloco inline invalido para: %s" % nome)
        fim += len("</wp:inline>")
        bloco = documento_xml[inicio:fim]

        id_rel = re.search(r'\br:embed="([^"]+)"', bloco)
        extensao = re.search(r'<wp:extent\b[^>]*\bcx="(\d+)"[^>]*\bcy="(\d+)"', bloco)
        if not id_rel or not extensao:
            raise RuntimeError("relacao ou dimensoes ausentes para: %s" % nome)
        alvo = relacoes.get(id_rel.group(1))
        if not alvo:
            raise RuntimeError("midia nao localizada para: %s" % nome)

        cx = int(extensao.group(1))
        cy = int(round(cx * altura_px / largura_px))
        bloco = re.sub(
            r'(<wp:extent\b[^>]*\bcx="%d"[^>]*\bcy=")\d+("/?>)' % cx,
            lambda m: m.group(1) + str(cy) + m.group(2), bloco, count=1)
        bloco = re.sub(
            r'(<a:ext\b[^>]*\bcx=")\d+("[^>]*\bcy=")\d+("/?>)',
            lambda m: m.group(1) + str(cx) + m.group(2) + str(cy) + m.group(3),
            bloco, count=1)
        descricao = html.escape(legenda, quote=True)
        bloco = atributo_acessivel(bloco, "wp:docPr", descricao)
        bloco = atributo_acessivel(bloco, "pic:cNvPr", descricao)
        documento_xml = documento_xml[:inicio] + bloco + documento_xml[fim:]
        midias["word/" + alvo.replace("\\", "/")] = png

    return documento_xml, midias


def atualizar_docx(entrada, saida):
    conteudo = carregar_conteudo()
    figuras = [(item[1], item[2]) for item in conteudo.C if item[0] == "fig"]
    pasta_saida = os.path.dirname(os.path.abspath(saida))
    os.makedirs(pasta_saida, exist_ok=True)
    fd, temporario = tempfile.mkstemp(prefix="artigo_figuras_", suffix=".docx",
                                      dir=pasta_saida)
    os.close(fd)
    try:
        with zipfile.ZipFile(entrada, "r") as origem:
            documento_xml = origem.read("word/document.xml").decode("utf-8")
            relacionamentos_xml = origem.read("word/_rels/document.xml.rels").decode("utf-8")
            documento_xml, midias = atualizar_xml(
                documento_xml, relacionamentos_xml, figuras)
            with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED) as destino:
                for item in origem.infolist():
                    if item.filename == "word/document.xml":
                        dados = documento_xml.encode("utf-8")
                    elif item.filename in midias:
                        with open(midias[item.filename], "rb") as arquivo:
                            dados = arquivo.read()
                    else:
                        dados = origem.read(item.filename)
                    destino.writestr(item, dados)
        os.replace(temporario, saida)
    finally:
        if os.path.exists(temporario):
            os.remove(temporario)
    print("atualizado:", saida)
    print("figuras substituidas:", len(figuras))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DOCX_PADRAO)
    parser.add_argument("--output", default=DOCX_PADRAO)
    args = parser.parse_args()
    atualizar_docx(os.path.abspath(args.input), os.path.abspath(args.output))


if __name__ == "__main__":
    main()
