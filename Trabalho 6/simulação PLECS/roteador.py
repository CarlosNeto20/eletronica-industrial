"""Roteador ortogonal dos fios e sinais dos modelos PLECS do Trabalho 6.

O PLECS liga dois terminais por uma polilinha cujos vertices intermediarios ficam no
campo Points da conexao. Sem Points o programa desenha uma reta entre os terminais, que
em geral sai diagonal e atravessa blocos. Este modulo recebe a posicao e a direcao de
saida de cada terminal, mais a caixa ocupada por cada bloco, e devolve os Points de cada
conexao com todos os segmentos horizontais ou verticais e sem passar sobre bloco algum.

Como funciona:

1. Cada terminal ganha um trecho inicial fixo (o toco) no sentido em que ele aponta, com
   comprimento tal que o fim do toco caia na grade de roteamento. Isso garante que o fio
   sai do bloco pelo lado certo e nunca encosta no corpo.
2. O miolo do caminho e procurado numa grade de passo GRADE por A* com custo 1 por passo,
   CUSTO_CURVA por mudanca de direcao e CUSTO_PARALELO por andar junto de um fio de outra
   rede. Blocos sao obstaculos. O resultado e ortogonal por construcao.
3. Num no com mais de dois terminais, os terminais entram um a um: a busca parte de todos
   os pontos ja ligados ao no (custo zero), o que produz uma arvore com tronco comum em
   vez de uma estrela. Os caminhos ate cada destino sao depois fundidos por prefixo comum
   e viram a arvore Connection/Branch do arquivo .plecs.

A geometria dos terminais de cada tipo de bloco vem de desenvolvimento/blocos_biblioteca.json,
medida nos modelos que o proprio PLECS gravou (ver desenvolvimento/inspecionar_biblioteca.py).
"""
import heapq

GRADE = 10          # passo da grade de roteamento, em unidades do esquema
CUSTO_CURVA = 4     # penalidade por mudanca de direcao
CUSTO_PARALELO = 8  # penalidade por ocupar o mesmo trecho que um fio de outra rede
MARGEM = 5          # folga ao redor da caixa de cada bloco
JANELA = 240        # folga da janela de busca ao redor dos pontos a ligar
DIR = ((1, 0), (-1, 0), (0, 1), (0, -1))


def arredonda(v, passo=GRADE):
    return int(round(v / passo)) * passo


class Tela:
    """Grade de roteamento com os blocos como obstaculos."""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = arredonda(x0) - GRADE, arredonda(y0) - GRADE
        self.nx = (arredonda(x1) + GRADE - self.x0) // GRADE + 1
        self.ny = (arredonda(y1) + GRADE - self.y0) // GRADE + 1
        self.bloqueado = bytearray(self.nx * self.ny)
        self.ocupado = {}            # (celula, orientacao) -> rede que ja usa o trecho
        self.caixas = []

    # --- grade -------------------------------------------------------------
    def dentro(self, x, y):
        return self.x0 <= x < self.x0 + self.nx * GRADE and self.y0 <= y < self.y0 + self.ny * GRADE

    def celula(self, x, y):
        return ((y - self.y0) // GRADE) * self.nx + (x - self.x0) // GRADE

    def ponto(self, c):
        return (self.x0 + (c % self.nx) * GRADE, self.y0 + (c // self.nx) * GRADE)

    def obstaculo(self, caixa, nome=''):
        xa, ya, xb, yb = caixa
        self.caixas.append((xa, ya, xb, yb, nome))
        xa, ya, xb, yb = xa - MARGEM, ya - MARGEM, xb + MARGEM, yb + MARGEM
        x = arredonda(xa, GRADE)
        while x <= xb:
            if x >= xa:
                y = arredonda(ya, GRADE)
                while y <= yb:
                    if y >= ya and self.dentro(x, y):
                        self.bloqueado[self.celula(x, y)] = 1
                    y += GRADE
            x += GRADE

    def livre(self, x, y):
        return self.dentro(x, y) and not self.bloqueado[self.celula(x, y)]

    def liberar(self, pontos):
        """Desbloqueia pontos de acesso (o fim do toco pode cair na folga de um bloco)."""
        for x, y in pontos:
            if self.dentro(x, y):
                self.bloqueado[self.celula(x, y)] = 0

    # --- tocos -------------------------------------------------------------
    def toco(self, p, d, comprimento=20):
        """Pontos do trecho inicial, do terminal ate um ponto na grade, e o ponto de acesso.

        Primeiro anda no sentido do terminal ate que a coordenada ao longo caia na grade;
        depois, se a coordenada transversal nao estiver na grade, da um passo de 5 para o
        lado de fora do bloco. Devolve (pontos_intermediarios, ponto_de_acesso)."""
        x, y = p
        dx, dy = d
        if dx:
            n = comprimento if (x + dx * comprimento) % GRADE == 0 else comprimento + 5
            x1, y1 = x + dx * n, y
            pts = [(x1, y1)]
            if y1 % GRADE:
                y2 = y1 + (5 if y1 > arredonda(y1) else -5)
                pts.append((x1, y2))
                y1 = y2
        else:
            n = comprimento if (y + dy * comprimento) % GRADE == 0 else comprimento + 5
            x1, y1 = x, y + dy * n
            pts = [(x1, y1)]
            if x1 % GRADE:
                x2 = x1 + (5 if x1 > arredonda(x1) else -5)
                pts.append((x2, y1))
                x1 = x2
        return pts, (x1, y1)

    # --- busca -------------------------------------------------------------
    def caminho(self, origens, destino, rede):
        """A* de um conjunto de pontos de partida (custo zero) ate destino."""
        xd, yd = destino
        if not self.dentro(*destino):
            raise ValueError(f'{rede}: destino {destino} fora da tela')
        cd = self.celula(xd, yd)
        xa = min([x for x, _ in origens] + [xd]) - JANELA
        xb = max([x for x, _ in origens] + [xd]) + JANELA
        ya = min([y for _, y in origens] + [yd]) - JANELA
        yb = max([y for _, y in origens] + [yd]) + JANELA

        def h(c):
            x, y = self.ponto(c)
            return (abs(x - xd) + abs(y - yd)) // GRADE

        inicio = {self.celula(x, y) for x, y in origens}
        dist, anterior, fila = {}, {}, []
        for c in inicio:
            for k in range(4):
                dist[(c, k)] = 0
                heapq.heappush(fila, (h(c), 0, c, k))
        achou = None
        while fila:
            _, g, c, k = heapq.heappop(fila)
            if dist.get((c, k), 1 << 30) < g:
                continue
            if c == cd:
                achou = (c, k)
                break
            x, y = self.ponto(c)
            for nk, (dx, dy) in enumerate(DIR):
                nxp, nyp = x + dx * GRADE, y + dy * GRADE
                if not (xa <= nxp <= xb and ya <= nyp <= yb) or not self.livre(nxp, nyp):
                    continue
                nc = self.celula(nxp, nyp)
                orient = 0 if dx else 1
                custo = 1 + (0 if nk == k or c in inicio else CUSTO_CURVA)
                dono = self.ocupado.get((nc, orient))
                if dono is not None and dono != rede:
                    custo += CUSTO_PARALELO
                ng = g + custo
                if ng < dist.get((nc, nk), 1 << 30):
                    dist[(nc, nk)] = ng
                    anterior[(nc, nk)] = (c, k)
                    heapq.heappush(fila, (ng + h(nc), ng, nc, nk))
        if achou is None:
            raise RuntimeError(f'{rede}: sem caminho ortogonal livre ate {destino}')
        seq = []
        estado = achou
        while estado is not None:
            seq.append(self.ponto(estado[0]))
            estado = anterior.get(estado)
        seq.reverse()
        return seq

    def marcar(self, seq, rede):
        for (xa_, ya_), (xb_, yb_) in zip(seq, seq[1:]):
            orient = 0 if ya_ == yb_ else 1
            if orient == 0:
                for x in range(min(xa_, xb_), max(xa_, xb_) + GRADE, GRADE):
                    self.ocupado[(self.celula(x, ya_), 0)] = rede
            else:
                for y in range(min(ya_, yb_), max(ya_, yb_) + GRADE, GRADE):
                    self.ocupado[(self.celula(xa_, y), 1)] = rede


def simplificar(pontos):
    """Remove pontos repetidos e colineares."""
    saida = []
    for p in pontos:
        if saida and saida[-1] == p:
            continue
        saida.append(p)
    k = 1
    while k < len(saida) - 1:
        a, b, c = saida[k - 1], saida[k], saida[k + 1]
        if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]):
            del saida[k]
        else:
            k += 1
    return saida


def rotear(tela, rede, terminais):
    """Liga os terminais de uma rede e devolve (caminhos, arvore).

    terminais: lista de (componente, terminal, ponto, direcao). O primeiro e a origem.
    Devolve lista de (pontos_intermediarios, (componente, terminal)) para cada destino,
    com os pontos ja na ordem em que o PLECS os le, partindo da origem.
    """
    tocos, acessos = [], []
    for c, t, p, d in terminais:
        pts, ac = tela.toco(p, d)
        tocos.append(pts)
        acessos.append(ac)
    tela.liberar(acessos)
    for pts in tocos:
        tela.liberar(pts)
    ligados = [acessos[0]]
    trechos = {acessos[0]: []}          # ponto de acesso -> caminho desde a origem
    for i in range(1, len(terminais)):
        if acessos[i] in trechos:
            continue
        seq = tela.caminho(ligados, acessos[i], rede)
        tela.marcar(seq, rede)
        base = trechos[seq[0]]
        trechos[acessos[i]] = base + seq[1:]
        for p in seq:
            if p not in ligados:
                ligados.append(p)
            trechos.setdefault(p, base + seq[1:seq.index(p) + 1])
    caminhos = []
    for i in range(1, len(terminais)):
        pts = tocos[0] + trechos[acessos[i]] + list(reversed(tocos[i]))
        caminhos.append((simplificar(pts), (terminais[i][0], terminais[i][1])))
    return caminhos


def arvore(caminhos, q):
    """Funde os caminhos por prefixo comum e escreve o corpo Points/Branch do PLECS."""
    def pontos(ps):
        return 'Points [' + '; '.join(f'{x}, {y}' for x, y in ps) + '] ' if ps else ''

    def no(itens, k):
        """itens: lista de (pontos, destino). k: quantos pontos ja foram escritos."""
        if len(itens) == 1:
            ps, (c, t) = itens[0]
            return pontos(ps[k:]) + f'DstComponent {q(c)} DstTerminal {t}'
        comum = k
        while True:
            seguintes = {tuple(ps[comum:comum + 1]) for ps, _ in itens}
            if len(seguintes) != 1 or not next(iter(seguintes)):
                break
            comum += 1
        prefixo = pontos(itens[0][0][k:comum])
        folhas = [it for it in itens if len(it[0]) == comum]
        grupos = {}
        for it in itens:
            if len(it[0]) > comum:
                grupos.setdefault(it[0][comum], []).append(it)
        ramos = []
        for ps, (c, t) in folhas:
            ramos.append(f'Branch {{ DstComponent {q(c)} DstTerminal {t} }}')
        for _, itens2 in sorted(grupos.items()):
            ramos.append('Branch { ' + no(itens2, comum) + ' }')
        if len(ramos) == 1 and not folhas:
            interno = ramos[0][len('Branch { '):-2]
            return prefixo + interno
        return prefixo + ' '.join(ramos)

    return no(list(caminhos), 0)
