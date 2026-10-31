from pn import Net

net = Net("03–09", "M/M/1, porucha prodlouží probíhající obsluhu o 2")
net.params = {"A": 10, "B": 6, "X": 20}

# M/M/1 (rozmístění jako v 03–02)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka", label_pos="above left")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# prodloužení pod obsluhou: přerušení vezme transakci, po 2 j. se vrátí do obsluhy
# (exp(B) začne znovu, je bez paměti); obě hrany místa obsluha vedou zespodu jako oblouky
net.immediate("preruseni", (5.1, -1.6), p=1, param_pos="left")
net.arc("obsluha", "preruseni", out=240, into=90)
net.place("prodl", (6, -2.8), label="prodloužení", label_pos="below")
net.arc("preruseni", "prodl", via=[(6, -1.6)])
net.timed("dva", (6.9, -1.6), "2", param_pos="right")
net.arc("prodl", "dva", via=[(6.9, -2.8)])
net.arc("dva", "obsluha", out=90, into=300)

# poruchy: řada pod prodloužením, porucha přímo pod přerušením
net.place("gen_p", (2.1, -4.4), tokens=1, label="vznik poruch", label_pos="left")
net.timed("vznik", (3.6, -4.4), "exp(X)")
net.loop("gen_p", "vznik")
net.place("porucha", (5.1, -4.4), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.arc("porucha", "preruseni")
# volná linka: porucha nemá účinek (test linky nad ní, hrana kolem odchodu)
net.immediate("zanik", (7.5, 3.2), label="porucha bez účinku", label_pos="right")
net.arc("linka", "zanik", bend=20)
net.arc("zanik", "linka", bend=20)
net.arc("porucha", "zanik", via=[(11.5, -4.4), (11.5, 4.6), (7.5, 4.6)])

net.invariant({"linka": 1, "obsluha": 1, "prodl": 1}, 1)
