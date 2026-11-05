"""TikZ output in the course notation (Hrubý, IMS slides 128–164).

Places are circles with dots (or a number/symbol inside), immediate transitions
are thin white bars, timed transitions are grey bars with the time under them,
priority and probability are written next to the transition.
"""

PREAMBLE = r"""\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{tikz}
\usetikzlibrary{petri,arrows.meta,backgrounds}
\pagestyle{empty}
\begin{document}
"""

STYLE = r"""[
  show background rectangle,inner frame sep=8pt,
  background rectangle/.style={fill=white,draw=none},
  >={Stealth[length=2.6mm,width=1.8mm]},
  every place/.style={draw,thick,minimum size=7.5mm,inner sep=0pt},
  imm/.style={draw,thick,fill=white,rectangle,inner sep=0pt,minimum width=2.4mm,minimum height=9mm},
  imm h/.style={imm,minimum width=9mm,minimum height=2.4mm},
  tim/.style={imm,fill=black!45},
  tim h/.style={imm h,fill=black!45},
  arc/.style={->,thick},
  inh/.style={-{Circle[open,length=2mm]},thick},
  lbl/.style={font=\small},
  par/.style={font=\footnotesize},
  wgt/.style={font=\footnotesize,inner sep=1.5pt},
  note/.style={font=\footnotesize\itshape,align=left,text=black!70},
]
"""

_OPPOSITE = {"above": "below", "below": "above", "left": "right", "right": "left"}

CORNER = 20          # default corner radius of orthogonal arcs, pt
PT = 1 / 28.4527     # pt in cm (TikZ unit)
# half sizes in cm of the node shapes in STYLE, with half a thick line
_PLACE_R = 0.375 + 0.4 * PT
_BAR = (0.12 + 0.4 * PT, 0.45 + 0.4 * PT)
_TIP = 0.3           # straight end the arrow tip needs (2.6 mm Stealth and a margin), cm


def _tex(s):
    return (str(s).replace("\\", r"\textbackslash{}").replace("%", r"\%")
            .replace("&", r"\&").replace("#", r"\#").replace("_", r"\_")
            .replace("\u202f", r"\,").replace("≥", r"$\geq$").replace("≤", r"$\leq$")
            .replace("→", r"$\rightarrow$").replace("×", r"$\times$").replace("∧", r"$\land$"))


def _xy(at):
    return f"({at[0]:g},{at[1]:g})"


def _place(p):
    opts = ["place"]
    text = ""
    if isinstance(p.tokens, str):
        text = _tex(p.tokens)
    elif p.tokens > 4:
        text = str(p.tokens)
    elif p.tokens > 0:
        opts.append(f"tokens={p.tokens}")
    # a number or symbol written inside the place must fit the circle
    if len(text) >= 4:
        opts.append("font=\\scriptsize")
    elif len(text) == 3:
        opts.append("font=\\footnotesize")
    if p.label:
        opts.append(f"label={{[lbl]{p.label_pos}:{{{_tex(p.label)}}}}}")
    return f"\\node[{','.join(opts)}] ({p.id}) at {_xy(p.at)} {{{text}}};"


def _transition(t):
    style = ("tim" if t.kind == "timed" else "imm") + (" h" if t.horizontal else "")
    opts = [style]
    if t.label:
        opts.append(f"label={{[lbl]{t.label_pos}:{{{_tex(t.label)}}}}}")
    param = t.param
    if t.capacity:
        param = f"{param}, kap.\\ {t.capacity}" if param else f"kap.\\ {t.capacity}"
    if param:
        pos = t.param_pos or ("below" if t.label_pos == "above" else "above")
        if t.horizontal and not t.param_pos:
            pos = "right"
        opts.append(f"label={{[par]{pos}:{{{_tex(param)}}}}}")
    return f"\\node[{','.join(opts)}] ({t.id}) at {_xy(t.at)} {{}};"


def _border(net, nid, toward):
    """Distance in cm from the centre of node `nid` to its border in the direction of `toward`."""
    node = net.places.get(nid) or net.transitions[nid]
    dx, dy = toward[0] - node.at[0], toward[1] - node.at[1]
    length = (dx * dx + dy * dy) ** 0.5
    if nid in net.places or not length:
        return _PLACE_R
    w, h = _BAR[::-1] if node.horizontal else _BAR
    return length * min(w / abs(dx) if dx else float("inf"), h / abs(dy) if dy else float("inf"))


def _corners(net, a):
    """Radius in pt of each via corner: `a.corner` (default CORNER), reduced where a neighbouring
    segment is too short for it. A segment between two corners is shared by both; a segment
    ending at a node belongs to its one corner, minus the straight end for the arrow tip.
    Without this TikZ draws loops, and arrow tips inside the target."""
    full = CORNER if a.corner is None else a.corner
    src, dst = net.places.get(a.src) or net.transitions[a.src], net.places.get(a.dst) or net.transitions[a.dst]
    pts = [src.at] + [tuple(v) for v in a.via] + [dst.at]
    # real corners only: a via on a straight line has nothing to round
    turn = [i for i in range(1, len(pts) - 1)
            if (pts[i][0] - pts[i - 1][0]) * (pts[i + 1][1] - pts[i][1])
            != (pts[i][1] - pts[i - 1][1]) * (pts[i + 1][0] - pts[i][0])]
    radius = {i: full for i in range(1, len(pts) - 1)}
    ends = [0] + turn + [len(pts) - 1]
    for k, i in enumerate(turn):
        room = []
        for j, other in ((ends[k], ends[k]), (ends[k + 2], ends[k + 2])):
            length = ((pts[j][0] - pts[i][0]) ** 2 + (pts[j][1] - pts[i][1]) ** 2) ** 0.5
            if j == 0:
                length -= _border(net, a.src, pts[1])
            elif j == len(pts) - 1:
                length -= _border(net, a.dst, pts[-2]) + _TIP
            else:
                length /= 2
            room.append(length / PT)
        radius[i] = max(0, min([full] + room))
    return [radius[i] for i in range(1, len(pts) - 1)]


def _rc(r):
    return f"rounded corners={r:.1f}pt" if r >= 0.5 else "sharp corners"


def _arc(a, net):
    style = "inh" if a.inhibitor else "arc"
    if a.corner is not None:
        style += f",rounded corners={a.corner:g}pt"
    w = f" node[wgt,{a.w_pos},pos=0.5] {{{a.w}}}" if a.w != 1 else ""
    if a.out is not None or a.into is not None:
        opts = ",".join(o for o in (f"out={a.out:g}" if a.out is not None else "",
                                    f"in={a.into:g}" if a.into is not None else "",
                                    f"looseness={a.looseness:g}" if a.looseness is not None else "") if o)
        return f"\\draw[{style}] ({a.src}) to[{opts}]{w} ({a.dst});"
    if a.via:
        # each corner's radius goes right before the segment that ends in it
        r = _corners(net, a)
        pts = "".join(f" [{_rc(r[k + 1])}] -- {_xy(v)}" for k, v in enumerate(a.via[1:]))
        # weight label on the first segment
        return (f"\\draw[{style}] ({a.src}) [{_rc(r[0])}] --{w} {_xy(a.via[0])}{pts}"
                f" -- ({a.dst});")
    if a.bend:
        side = "left" if a.bend > 0 else "right"
        return f"\\draw[{style}] ({a.src}) to[bend {side}={abs(a.bend):g}]{w} ({a.dst});"
    return f"\\draw[{style}] ({a.src}) --{w} ({a.dst});"


def picture(net):
    lines = [r"\begin{tikzpicture}" + STYLE]
    lines += [_place(p) for p in net.places.values()]
    lines += [_transition(t) for t in net.transitions.values()]
    lines += [_arc(a, net) for a in net.arcs]
    for at, text in net.notes:
        lines.append(f"\\node[note,anchor=north west] at {_xy(at)} {{{_tex(text)}}};")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def document(net):
    """A standalone document whose page is cropped to the picture."""
    return (PREAMBLE
            + "\\setbox0\\hbox{%\n" + picture(net) + "%\n}\n"
            + r"""\pdfpagewidth=\wd0
\pdfpageheight=\dimexpr\ht0+\dp0\relax
\pdfhorigin=0pt \pdfvorigin=0pt
\shipout\vbox{\box0}
\end{document}
""")
