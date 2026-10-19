"""Mini-biblioteca para escrever arquivos .plecs (PLECS Standalone) em texto.

O formato foi levantado a partir de modelos públicos (PLECS 4.6 a 5.0) e do
manual do PLECS. Os componentes são descritos por tipo, posição e parâmetros;
as ligações elétricas são descritas por redes (listas de terminais) e as de
sinal, sempre que possível, por pares Goto/From, o que dispensa fios longos.

Convenções de terminais (Flipped off), no referencial "up":
  bipolos (R, L, C, D, fonte CC, voltímetro, amperímetro, chave):
      terminal 1 em cima, terminal 2 embaixo.
      Diodo: 1 = anodo, 2 = catodo.  Fonte CC: 1 = positivo.
  MOSFET: 1 = dreno (cima), 2 = fonte (baixo), 3 = gatilho (à esquerda).
  Voltímetro/Amperímetro: 3 = saída de sinal (à direita no referencial up).
  Direction gira o componente: up -> 1 em cima; right -> 1 à direita;
  down -> 1 embaixo; left -> 1 à esquerda.
  Transformer (usado sempre com Direction right, Flipped on):
      1/2 = enrolamento 1 (esquerda, cima/baixo), 3/4 = enrolamento 2
      (direita, cima/baixo); 1 e 3 têm a mesma polaridade quando os números
      de espiras têm o mesmo sinal.
"""

# ---------------------------------------------------------------- geometria
# (dx, dy, direção de saída) no referencial "up"
_BIPOLO = {1: (0, -20, "up"), 2: (0, 20, "down")}
_TERM_UP = {
    "Resistor": _BIPOLO, "Inductor": _BIPOLO, "Capacitor": _BIPOLO,
    "Diode": _BIPOLO, "DCVoltageSource": _BIPOLO, "ACVoltageSource": _BIPOLO,
    "Label": {1: (0, 10, "down")},
    "Switch": {1: (0, -20, "up"), 2: (0, 20, "down"), 3: (-20, 0, "left")},
    "Mosfet": {1: (0, -20, "up"), 2: (0, 20, "down"), 3: (-35, 0, "down")},
    "MosfetWithDiode": {1: (0, -20, "up"), 2: (0, 20, "down"), 3: (-20, 0, "left")},
    "Voltmeter": {1: (0, -20, "up"), 2: (0, 20, "down"), 3: (20, 0, "right")},
    "Ammeter": {1: (0, -20, "up"), 2: (0, 20, "down"), 3: (20, 0, "right")},
    "Ground": {1: (0, -10, "up")},
}
# blocos de sinal: coordenadas já no referencial em que são usados
_TERM_SIG = {
    "PulseGenerator": {1: (20, 0, "right")},
    "Constant": {1: (15, 0, "right")},
    "From": {1: (15, 0, "right")},
    "Goto": {1: (-15, 0, "left")},
    "Gain": {1: (-15, 0, "left"), 2: (15, 0, "right")},
    "LogicalOperator": {1: (15, 0, "right"), 2: (-15, 0, "left")},
    "ToFile": {1: (-15, 0, "left")},
    "PlecsProbe": {1: (15, 0, "right")},
    "Comparator": {1: (-15, -5, "left"), 2: (-15, 5, "left"), 3: (15, 0, "right")},
    "TriangleGenerator": {1: (20, 0, "right")},
    "Output": {1: (-15, 0, "left")},
}
_VEC = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
_ROT = {  # rotação do referencial "up" para a Direction pedida (y para baixo)
    "up": lambda x, y: (x, y),
    "right": lambda x, y: (-y, x),
    "down": lambda x, y: (-x, -y),
    "left": lambda x, y: (y, -x),
}
_DIR_ROT = {  # idem para as direções de saída
    "up": {"up": "up", "down": "down", "left": "left", "right": "right"},
    "right": {"up": "right", "down": "left", "left": "up", "right": "down"},
    "down": {"up": "down", "down": "up", "left": "right", "right": "left"},
    "left": {"up": "left", "down": "right", "left": "down", "right": "up"},
}

# listas de parâmetros (nome, valor padrão) por tipo, na ordem do PLECS
_PARAMS = {
    "Resistor": [("R", "1")],
    "Inductor": [("L", "1e-3"), ("i_init", "0")],
    "Capacitor": [("C", "1e-6"), ("v_init", "0")],
    "DCVoltageSource": [("V", "1")],
    "ACVoltageSource": [("V", "1"), ("w", "2*pi*50"), ("phi", "0")],
    "Label": [("Tag", "x"), ("Visibility", "1")],
    "Comparator": [],
    "TriangleGenerator": [("Min", "0"), ("Max", "1"), ("f", "1"), ("DutyCycle", "0.5"),
                          ("Delay", "0")],
    "Output": [("Index", "1"), ("Width", "-1")],
    "Diode": [("Vf", "0"), ("Ron", "0"), ("thermal", ""), ("Rth", "0"), ("Np", "1"),
              ("T_init", ""), ("SwitchModel", "1"), ("f_grid", "0")],
    "MosfetWithDiode": [("Ron", "0"), ("s_init", "0"), ("thermal", ""), ("Rth", "0"),
                        ("T_init", "")],
    "Switch": [("s_init", "0"), ("SwitchModel", "1"), ("f_grid", "0")],
    "Transformer": [("Windings", "[1 1]"), ("n", "[1 1]"), ("Polarity", "+"),
                    ("Lm", "inf"), ("im0", "0")],
    "PulseGenerator": [("Hi", "1"), ("Lo", "0"), ("f", "1"), ("DutyCycle", "0.5"),
                       ("Delay", "0"), ("DataType", "10")],
    "Constant": [("Value", "1"), ("DataType", "10")],
    "LogicalOperator": [("Operator", "6"), ("Inputs", "1")],  # 6 = NOT
    "Gain": [("K", "1"), ("Multiplication", "1"), ("OutputDataType", "11"),
             ("DataTypeOverflowMode", "1"), ("GainDataType", "11")],
    "SignalMux": [("Width", "2")],
    "Goto": [("Tag", "tag"), ("Visibility", "1"), ("NoMatchingCounterpartAction", "2")],
    "From": [("Tag", "tag"), ("Visibility", "1"), ("NoMatchingCounterpartAction", "1")],
    "ToFile": [("Filename", "dados"), ("FileType", "1"), ("WriteSignalNames", "2"),
               ("SampleTime", "-1")],
}
_EVAL = {("ToFile", "Filename"): "on"}  # nome do arquivo avaliado como expressão


def _ascii(s):
    """Remove acentos: o arquivo .plecs é gravado só com caracteres ASCII."""
    import unicodedata
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii")


def _q(s):
    s = _ascii(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


class Model:
    def __init__(self, name, time_span, max_step, rel_tol="1e-4", init_cmds=""):
        self.name, self.time_span, self.max_step = name, time_span, max_step
        self.rel_tol, self.init_cmds = rel_tol, init_cmds
        self.comps, self.conns, self._n = {}, [], 0

    # ------------------------------------------------------------ componentes
    def add(self, typ, name, x, y, direction="up", flipped="off", show=True,
            label=None, **params):
        if name in self.comps:
            raise ValueError("nome repetido: " + name)
        self.comps[name] = dict(type=typ, name=name, x=x, y=y, dir=direction,
                                flip=flipped, show=show, label=label, params=params,
                                extra=None)
        return name

    def add_ref(self, name, src, x, y, terminals, frame, params, direction="up",
                show=True, label=None):
        """Componente de biblioteca (Type Reference), p. ex. amp-op e zener.

        terminals: lista de (dx, dy, direcao) no referencial "up", na ordem das
        portas da biblioteca; params: lista de (variavel, valor)."""
        self.add("Reference", name, x, y, direction, show=show, label=label)
        self.comps[name]["extra"] = dict(src=src, terminals=list(terminals), frame=frame,
                                         params=list(params))
        return name

    def probe(self, name, x, y, component, signals=None, show=False):
        """Probe de um componente (component, signals) ou de varios: component
        = lista de (componente, [sinais])."""
        self.add("PlecsProbe", name, x, y, "right", show=show)
        itens = component if signals is None else [(component, signals)]
        self.comps[name]["extra"] = list(itens)
        return name

    def scope(self, name, x, y, axes_names):
        self.add("Scope", name, x, y, "up")
        self.comps[name]["extra"] = list(axes_names)
        return name

    def mux(self, name, x, y, width):
        return self.add("SignalMux", name, x, y, "right", show=False, Width=str(width))

    # ------------------------------------------------------------ geometria
    def term(self, name, t):
        c = self.comps[name]
        typ = c["type"]
        if typ == "Transformer":
            dx, dy, d = {1: (-10, -20, "left"), 2: (-10, 20, "left"),
                         3: (10, -20, "right"), 4: (10, 20, "right")}[t]
            return (c["x"] + dx, c["y"] + dy), d
        if typ == "SignalMux":
            w = int(c["params"]["Width"])
            if t == 1:
                return (c["x"] + 10, c["y"]), "right"
            k = t - 1
            return (c["x"] - 10, c["y"] + (k - (w + 1) / 2) * 10), "left"
        if typ == "Scope":
            n = len(c["extra"])
            return (c["x"] - 20, c["y"] + (t - (n + 1) / 2) * 10), "left"
        if typ in _TERM_SIG:
            dx, dy, d = _TERM_SIG[typ][t]
            return (c["x"] + dx, c["y"] + dy), d
        if typ == "Reference":
            dx, dy, d = c["extra"]["terminals"][t - 1]
            rx, ry = _ROT[c["dir"]](dx, dy)
            return (c["x"] + rx, c["y"] + ry), _DIR_ROT[c["dir"]][d]
        dx, dy, d = _TERM_UP[typ][t]
        rx, ry = _ROT[c["dir"]](dx, dy)
        return (c["x"] + rx, c["y"] + ry), _DIR_ROT[c["dir"]][d]

    def _stub(self, name, t, length=None):
        (x, y), d = self.term(name, t)
        typ = self.comps[name]["type"]
        if length is None:
            length = 15 if typ in _TERM_SIG or typ in ("SignalMux", "Scope") else 20
        vx, vy = _VEC[d]
        return (x + vx * length, y + vy * length), d

    # ------------------------------------------------------------ ligações
    @staticmethod
    def _route(p, q, q_dir):
        """Pontos de p até q, ortogonal, chegando em q pelo eixo de q_dir."""
        if p == q:
            return [q]
        if q_dir in ("up", "down"):      # último trecho vertical
            mid = (q[0], p[1])
        else:                            # último trecho horizontal
            mid = (p[0], q[1])
        return [m for m in (mid, q) if m != p]

    def wire(self, a, b, via=None, kind="Wire"):
        """Liga dois terminais a=(comp, term) e b=(comp, term)."""
        sa, da = self._stub(*a)
        sb, db = self._stub(*b)
        pts = [sa]
        for v in (via or []):
            pts += self._route(pts[-1], v, "up" if v[0] == pts[-1][0] else "left")
        pts += self._route(pts[-1], sb, db)
        self.conns.append(dict(kind=kind, src=a, pts=_clean(pts), branches=[], dst=b))

    def net(self, endpoints, rail=None, axis="h", kind="Wire"):
        """Rede com vários terminais.

        rail: coordenada do barramento (y se axis='h', x se axis='v'). Cada
        terminal desce (ou vai) até o barramento pela sua própria reta.
        """
        if len(endpoints) == 2 and rail is None:
            return self.wire(endpoints[0], endpoints[1], kind=kind)
        stubs = [self._stub(*e) for e in endpoints]
        if rail is None:
            ys = [s[0][1] for s in stubs] if axis == "h" else [s[0][0] for s in stubs]
            rail = sum(ys) / len(ys)

        def on_rail(s):
            (x, y), d = s
            return (x, rail) if axis == "h" else (rail, y)

        def to_rail(s):
            # do ponto de saída do terminal até o barramento, em linha reta
            return [s[0], on_rail(s)]

        src = endpoints[0]
        src_pts = to_rail(stubs[0])
        branches = []
        for e, s in zip(endpoints[1:], stubs[1:]):
            path = list(reversed(to_rail(s)))
            branches.append(dict(pts=_clean(path), dst=e))
        self.conns.append(dict(kind=kind, src=src, pts=_clean(src_pts),
                               branches=branches, dst=None))

    def signal(self, a, b, via=None):
        self.wire(a, b, via=via, kind="Signal")

    def direct(self, a, b, pts=None, kind="Wire"):
        """Liga a e b passando exatamente pelos pontos dados (sem trechos automaticos)."""
        self.conns.append(dict(kind=kind, src=a, pts=_clean(pts or []), branches=[], dst=b))

    def star(self, src, trunk, branches, kind="Wire"):
        """No com geometria explicita: src -> pontos do tronco -> ramos.

        branches: lista de (pontos, terminal); cada ramo parte do fim do tronco."""
        self.conns.append(dict(kind=kind, src=src, pts=_clean(trunk), dst=None,
                               branches=[dict(pts=_clean(p), dst=d) for p, d in branches]))

    # ------------------------------------------------------------ atalhos
    def goto(self, name, x, y, tag, src):
        """Goto posicionado à direita de src=(comp, term) e ligado a ele."""
        self.add("Goto", name, x, y, "right", show=False, Tag=tag, Visibility="1",
                 NoMatchingCounterpartAction="2")
        self.signal(src, (name, 1))

    def from_(self, name, x, y, tag, dst=None):
        self.add("From", name, x, y, "right", show=False, Tag=tag, Visibility="1",
                 NoMatchingCounterpartAction="1")
        if dst is not None:
            self.signal((name, 1), dst)

    # ------------------------------------------------------------ escrita
    def write(self, path, header_path):
        head = open(header_path, encoding="utf-8").read()
        head = head.split("  Schematic {")[0]
        repl = {"Name": _q(self.name), "TimeSpan": _q(self.time_span),
                "MaxStep": _q(self.max_step), "RelTol": _q(self.rel_tol),
                "InitializationCommands": _q(self.init_cmds)}
        lines = []
        for ln in head.splitlines():
            key = ln.strip().split(" ")[0] if ln.strip() else ""
            if ln.startswith("  ") and not ln.startswith("   ") and key in repl:
                lines.append("  %-13s %s" % (key, repl[key]))
            else:
                lines.append(ln)
        # portas de saída do nível superior são declaradas como terminais do modelo
        # (sem isso o comando "simulate" do RPC devolve Time e Values vazios)
        for c in self.comps.values():
            if c["type"] == "Output":
                lines += ["  Terminal {", "    Type          Output",
                          '    Index         "%s"' % c["params"].get("Index", "1"), "  }"]
        out = lines + ["  Schematic {",
                       "    Location      [0, 26; 1600, 900]",
                       "    ZoomFactor    1",
                       "    SliderPosition [0, 0]",
                       "    ShowBrowser   off",
                       "    BrowserWidth  100"]
        for c in self.comps.values():
            out += self._comp_lines(c)
        for k in self.conns:
            out += self._conn_lines(k)
        out += ["  }", "}", ""]
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(out))

    def _comp_lines(self, c):
        i = "    "
        L = [i + "Component {",
             i + "  Type          " + c["type"],
             i + "  Name          " + _q(c["name"]),
             i + "  Show          " + ("on" if c["show"] else "off"),
             i + "  Position      [%d, %d]" % (c["x"], c["y"]),
             i + "  Direction     " + c["dir"],
             i + "  Flipped       " + c["flip"]]
        if c["label"]:
            L.append(i + "  LabelPosition " + c["label"])
        typ = c["type"]
        if typ == "SignalMux":
            h = 5 * int(c["params"]["Width"])
            L.append(i + "  Frame         [-2, -%d; 7, %d]" % (h, h))
        if typ == "Scope":
            axes = c["extra"]
            h = 5 * len(axes) + 5
            L += [i + "  Frame         [-15, -%d; 15, %d]" % (h, h),
                  i + "  Location      [0, 26; 1200, 800]",
                  i + '  Axes          "%d"' % len(axes),
                  i + '  TimeRange     "0"', i + '  ScrollingMode "1"',
                  i + '  SingleTimeAxis "1"', i + '  Open          "0"',
                  i + '  Ts            "-1"', i + '  SampleLimit   "0"',
                  i + '  XAxisLabel    "Tempo / s"', i + '  ShowLegend    "1"']
            for a in axes:
                L += [i + "  Axis {", i + "    Name          " + _q(a),
                      i + "    AutoScale     1", i + "    MinValue      0",
                      i + "    MaxValue      1", i + "    Signals       {}",
                      i + "    SignalTypes   [ ]", i + "    Untangle      0",
                      i + "    KeepBaseline  off", i + "    BaselineValue 0", i + "  }"]
            L += [i + "  Fourier {", i + "    SingleXAxis       on",
                  i + '    AxisLabel         "Frequency / Hz"', i + "    Scaling           0",
                  i + "    PhaseDisplay      0", i + "    ShowFourierLegend off"]
            for _ in axes:
                L += [i + "    Axis {", i + '      Name          ""',
                      i + "      AutoScale     1", i + "      MinValue      0",
                      i + "      MaxValue      1", i + "      Signals       {}",
                      i + "      Untangle      0", i + "      KeepBaseline  off",
                      i + "      BaselineValue 0", i + "    }"]
            L += [i + "  }"]
        elif typ == "PlecsProbe":
            for comp, sigs in c["extra"]:
                L += [i + "  Probe {", i + "    Component     " + _q(comp),
                      i + '    Path          ""',
                      i + "    Signals       {" + ", ".join(_q(s) for s in sigs) + "}",
                      i + "  }"]
        elif typ == "Reference":
            e = c["extra"]
            L.insert(2, i + "  SrcComponent  " + _q(e["src"]))
            (x0, y0), (x1, y1) = e["frame"]
            L.append(i + "  Frame         [%d, %d; %d, %d]" % (x0, y0, x1, y1))
            for var, val in e["params"]:
                L += [i + "  Parameter {", i + "    Variable      " + _q(var),
                      i + "    Value         " + _q(val), i + "    Show          off",
                      i + "  }"]
            for dx, dy, d in e["terminals"]:
                L += [i + "  Terminal {", i + "    Type          Port",
                      i + "    Position      [%d, %d]" % (dx, dy),
                      i + "    Direction     " + d, i + "  }"]
        elif typ in ("Voltmeter", "Ammeter", "Ground"):
            pass
        else:
            given = dict(c["params"])
            for var, default in _PARAMS[typ]:
                val = given.pop(var, default)
                L += [i + "  Parameter {", i + "    Variable      " + _q(var),
                      i + "    Value         " + _q(val),
                      i + "    Show          off"]
                if (typ, var) in _EVAL:
                    L.append(i + "    Evaluate      " + _EVAL[(typ, var)])
                L.append(i + "  }")
            if given:
                raise ValueError("parâmetros desconhecidos em %s: %s" % (c["name"], given))
        L.append(i + "}")
        return L

    def _conn_lines(self, k):
        i = "    "
        L = [i + "Connection {", i + "  Type          " + k["kind"],
             i + "  SrcComponent  " + _q(k["src"][0]),
             i + "  SrcTerminal   %d" % k["src"][1]]
        if k["pts"]:
            L.append(i + "  Points        " + _pts(k["pts"]))
        if k["dst"] is not None:
            L += [i + "  DstComponent  " + _q(k["dst"][0]),
                  i + "  DstTerminal   %d" % k["dst"][1]]
        for b in k["branches"]:
            L.append(i + "  Branch {")
            if b["pts"]:
                L.append(i + "    Points        " + _pts(b["pts"]))
            L += [i + "    DstComponent  " + _q(b["dst"][0]),
                  i + "    DstTerminal   %d" % b["dst"][1], i + "  }"]
        L.append(i + "}")
        return L

    # ------------------------------------------------------------ conferência
    def check(self):
        """Confere que todo terminal elétrico está ligado exatamente uma vez."""
        used = {}
        for k in self.conns:
            ends = [k["src"]] + ([k["dst"]] if k["dst"] else []) + [b["dst"] for b in k["branches"]]
            for e in ends:
                if e[0] not in self.comps:
                    raise ValueError("componente inexistente: %s" % (e,))
                used[e] = used.get(e, 0) + 1
        problems = []
        for name, c in self.comps.items():
            typ = c["type"]
            if typ in _TERM_UP:
                terms = list(_TERM_UP[typ].keys())
            elif typ == "Transformer":
                terms = [1, 2, 3, 4]
            elif typ == "Reference":
                terms = list(range(1, len(c["extra"]["terminals"]) + 1))
            elif typ in _TERM_SIG:
                terms = list(_TERM_SIG[typ].keys())
            elif typ == "SignalMux":
                terms = list(range(1, int(c["params"]["Width"]) + 2))
            elif typ == "Scope":
                terms = list(range(1, len(c["extra"]) + 1))
            else:
                terms = []
            for t in terms:
                n = used.get((name, t), 0)
                if n != 1:
                    problems.append("%s terminal %d ligado %d vezes" % (name, t, n))
        return problems


def _clean(pts):
    out = []
    for p in pts:
        p = (int(round(p[0])), int(round(p[1])))
        if not out or out[-1] != p:
            out.append(p)
    # remove pontos colineares intermediários
    res = []
    for p in out:
        while len(res) >= 2 and ((res[-2][0] == res[-1][0] == p[0]) or (res[-2][1] == res[-1][1] == p[1])):
            res.pop()
        res.append(p)
    return res


def _pts(pts):
    return "[" + "; ".join("%d, %d" % p for p in pts) + "]"
