from pn import Net

net = Net("07–04", "M/M/1 se dvěma proudy příchodů, prioritní mají vyšší prioritu obsluhy")
net.params = {"A": 10, "P": 30, "B": 6}

# horní řada prioritní proud (P), dolní normální (N); linka je mezi řadami
for row, y, time in (("p", 2, "exp(P)"), ("n", -2, "exp(A)")):
    up = y > 0
    side = "above" if up else "below"
    net.place(f"gen_{row}", (0, y), tokens=1, label=f"příchody {row.upper()}", label_pos=side)
    net.timed(f"prichod_{row}", (1.5, y), time, param_pos=side)
    net.loop(f"gen_{row}", f"prichod_{row}")
    net.place(f"fronta_{row}", (3, y), label=f"fronta {row.upper()}", label_pos=side)
    net.place(f"obsluha_{row}", (6.5, y))
    net.timed(f"obsl_{row}", (8, y), "exp(B)", param_pos=side)
    net.arc(f"prichod_{row}", f"fronta_{row}")
    net.chain(f"obsaz_{row}", f"obsluha_{row}", f"obsl_{row}")

# jedna linka pro oba proudy; prioritní ji obsadí přednostně (p=1)
net.place("linka", (5, 0), tokens=1, label="linka", label_pos="above left")
net.immediate("obsaz_p", (5, 2), p=1, param_pos="above")
net.immediate("obsaz_n", (5, -2))
net.arc("fronta_p", "obsaz_p")
net.arc("fronta_n", "obsaz_n")
net.arc("linka", "obsaz_p")
net.arc("linka", "obsaz_n")
net.arc("obsl_p", "linka", out=270, into=25)
net.arc("obsl_n", "linka", out=90, into=-25)

# priorita obsluhy: čekající prioritní vyhodí normální transakci z obsluhy;
# hrana z obsluhy N obchází zdola a zleva proud N (jinak by křížila linku)
net.immediate("preruseni", (3, 0), label="přerušení", label_pos="below right")
net.loop("fronta_p", "preruseni", bend=20)
net.arc("obsluha_n", "preruseni", via=[(6.5, -3.4), (-1.2, -3.4), (-1.2, 0)])
net.arc("preruseni", "fronta_n")
net.arc("preruseni", "linka")

net.place("konec", (9.5, 0), label="obslouženo", label_pos="left")
net.immediate("odchod", (11, 0), exit=True, label="odchod")
net.arc("obsl_p", "konec", via=[(9.5, 2)], corner=20)
net.arc("obsl_n", "konec", via=[(9.5, -2)], corner=20)
net.arc("konec", "odchod")

net.invariant({"linka": 1, "obsluha_p": 1, "obsluha_n": 1}, 1)
