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
  arc/.style={->,thick,rounded corners=5pt},
  inh/.style={-{Circle[open,length=2mm]},thick,rounded corners=5pt},
  lbl/.style={font=\small},
  par/.style={font=\footnotesize},
  wgt/.style={font=\footnotesize,inner sep=1.5pt},
  note/.style={font=\footnotesize\itshape,align=left,text=black!70},
]
"""

_OPPOSITE = {"above": "below", "below": "above", "left": "right", "right": "left"}


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


def _arc(a):
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
        pts = " -- ".join(_xy(v) for v in a.via)
        # weight label on the first segment
        return f"\\draw[{style}] ({a.src}) --{w} {pts} -- ({a.dst});"
    if a.bend:
        side = "left" if a.bend > 0 else "right"
        return f"\\draw[{style}] ({a.src}) to[bend {side}={abs(a.bend):g}]{w} ({a.dst});"
    return f"\\draw[{style}] ({a.src}) --{w} ({a.dst});"


def picture(net):
    lines = [r"\begin{tikzpicture}" + STYLE]
    lines += [_place(p) for p in net.places.values()]
    lines += [_transition(t) for t in net.transitions.values()]
    lines += [_arc(a) for a in net.arcs]
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
