from pn import Net

net = Net("07–05", "Ukázky: a) priorita procesu (pořadí ve frontě), b) priorita obsluhy (přerušení)")
net.params = {"A": 10, "P": 30, "B": 6}


def mm1(k, yc, preemptive):
    """M/M/1 s prioritními (P, nahoře) a normálními (N, dole) transakcemi; k = předpona."""
    def n(name):
        return f"{k}_{name}"

    for row, y, time in (("p", yc + 2, "exp(P)"), ("n", yc - 2, "exp(A)")):
        side = "above" if y > yc else "below"
        net.place(n(f"gen_{row}"), (0, y), tokens=1, label=f"příchody {row.upper()}", label_pos=side)
        net.timed(n(f"prichod_{row}"), (1.5, y), time, param_pos=side)
        net.loop(n(f"gen_{row}"), n(f"prichod_{row}"))
        net.place(n(f"fronta_{row}"), (3, y), label=f"fronta {row.upper()}", label_pos=side)
        net.place(n(f"obsluha_{row}"), (6.5, y))
        net.timed(n(f"obsl_{row}"), (8, y), "exp(B)", param_pos=side)
        net.arc(n(f"prichod_{row}"), n(f"fronta_{row}"))
        net.chain(n(f"obsaz_{row}"), n(f"obsluha_{row}"), n(f"obsl_{row}"))

    # jedna linka pro oba druhy; prioritní ji obsadí přednostně (p=1)
    net.place(n("linka"), (5, yc), tokens=1, label="linka", label_pos="above left")
    net.immediate(n("obsaz_p"), (5, yc + 2), p=1, param_pos="above")
    net.immediate(n("obsaz_n"), (5, yc - 2))
    net.arc(n("fronta_p"), n("obsaz_p"))
    net.arc(n("fronta_n"), n("obsaz_n"))
    net.arc(n("linka"), n("obsaz_p"))
    net.arc(n("linka"), n("obsaz_n"))
    net.arc(n("obsl_p"), n("linka"), out=270, into=25)
    net.arc(n("obsl_n"), n("linka"), out=90, into=-25)

    if preemptive:
        # hrana z obsluhy N obchází zdola a zleva proud N (jinak by křížila linku)
        net.immediate(n("preruseni"), (3, yc), label="přerušení", label_pos="below right")
        net.loop(n("fronta_p"), n("preruseni"), bend=20)
        net.arc(n("obsluha_n"), n("preruseni"), via=[(6.5, yc - 3.4), (-1.2, yc - 3.4), (-1.2, yc)])
        net.arc(n("preruseni"), n("fronta_n"))
        net.arc(n("preruseni"), n("linka"))

    net.place(n("konec"), (9.5, yc), label="obslouženo", label_pos="left")
    net.immediate(n("odchod"), (11, yc), exit=True, label="odchod")
    net.arc(n("obsl_p"), n("konec"), via=[(9.5, yc + 2)], corner=20)
    net.arc(n("obsl_n"), n("konec"), via=[(9.5, yc - 2)], corner=20)
    net.arc(n("konec"), n("odchod"))

    net.invariant({n("linka"): 1, n("obsluha_p"): 1, n("obsluha_n"): 1}, 1)


net.notes.append(((-1.6, 3.6), "a) priorita procesu"))
mm1("a", 0, preemptive=False)
net.notes.append(((-1.6, -3.6), "b) priorita obsluhy"))
mm1("b", -7.4, preemptive=True)
