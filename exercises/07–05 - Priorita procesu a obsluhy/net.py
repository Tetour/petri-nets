from pn import Net

net = Net("07–05", "Ukázky: a) priorita procesu (pořadí ve frontě), b) priorita obsluhy (přerušení)")
net.params = {"A": 10, "P": 30, "B": 6}


def mm1(k, y0, preemptive):
    """M/M/1 s prioritními (P, nahoře) a normálními (N, dole) transakcemi; k = předpona."""
    def n(name):
        return f"{k}_{name}"

    yp, yn, ym = y0 + 4, y0, y0 + 2
    net.place(n("gen_p"), (0, yp), tokens=1, label="generátor P", label_pos="above")
    net.timed(n("prichod_p"), (1.5, yp), "exp(P)")
    net.loop(n("gen_p"), n("prichod_p"))
    net.place(n("fronta_p"), (3, yp), label="Fronta P")
    net.immediate(n("obsaz_p"), (4.5, yp), p=1, param_pos="above")
    net.place(n("obsluha_p"), (6.3, yp))
    net.timed(n("obsl_p"), (7.8, yp), "exp(B)", param_pos="above")
    net.chain(n("prichod_p"), n("fronta_p"), n("obsaz_p"), n("obsluha_p"), n("obsl_p"))

    net.place(n("gen_n"), (0, yn), tokens=1, label="generátor N", label_pos="below")
    net.timed(n("prichod_n"), (1.5, yn), "exp(A)")
    net.loop(n("gen_n"), n("prichod_n"))
    net.place(n("fronta_n"), (3, yn), label="Fronta N", label_pos="below")
    net.immediate(n("obsaz_n"), (4.5, yn))
    net.place(n("obsluha_n"), (6.3, yn))
    net.timed(n("obsl_n"), (7.8, yn), "exp(B)")
    net.chain(n("prichod_n"), n("fronta_n"), n("obsaz_n"), n("obsluha_n"), n("obsl_n"))

    net.place(n("linka"), (5.4, ym), tokens=1, label="Linka", label_pos="above right")
    net.arc(n("linka"), n("obsaz_p"))
    net.arc(n("linka"), n("obsaz_n"))
    net.arc(n("obsl_p"), n("linka"), bend=40)
    net.arc(n("obsl_n"), n("linka"), bend=-40)

    if preemptive:
        net.immediate(n("preruseni"), (3, ym), label="přerušení", label_pos="left")
        net.loop(n("fronta_p"), n("preruseni"), bend=20)
        net.arc(n("obsluha_n"), n("preruseni"))
        net.arc(n("preruseni"), n("fronta_n"))
        net.arc(n("preruseni"), n("linka"))

    net.place(n("konec"), (9.3, ym))
    net.immediate(n("odchod"), (10.8, ym), exit=True, label="odchod")
    net.arc(n("obsl_p"), n("konec"))
    net.arc(n("obsl_n"), n("konec"))
    net.arc(n("konec"), n("odchod"))

    net.invariant({n("linka"): 1, n("obsluha_p"): 1, n("obsluha_n"): 1}, 1)


net.notes.append(((-0.6, 5.5), "a) priorita procesu"))
mm1("a", 0, preemptive=False)
net.notes.append(((-0.6, -2.0), "b) priorita obsluhy"))
mm1("b", -8, preemptive=True)
