from pn import Net

net = Net("03–10", "M/M/1, porucha Exp(50) prodlouží probíhající obsluhu o 5")
net.params = {"A": 10, "B": 6}

# M/M/1 (rozmístění jako v 03–02)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# poruchy
net.place("gen_p", (10.8, -1.8), tokens=1, label="generátor poruch", label_pos="above")
net.timed("vznik", (9.3, -1.8), "Exp(50)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("porucha", (7.8, -1.8), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
# obsluha se pozastaví na 5 j. a pak pokračuje (exp(B) je bez paměti)
net.immediate("preruseni", (5.4, -1.8), p=1, horizontal=True, param_pos="below")
net.arc("obsluha", "preruseni")
net.arc("porucha", "preruseni")
net.place("prodl", (3.6, -2.7), label="prodloužení", label_pos="below")
net.arc("preruseni", "prodl")
net.timed("pet", (3.6, -1.35), "5", param_pos="left")
net.arc("prodl", "pet")
net.arc("pet", "obsluha")
# volná linka: porucha nemá účinek (test linky, linka zůstává)
net.immediate("zanik", (8.55, 3.2), horizontal=True, label="porucha bez účinku", label_pos="right",
              param_pos="above")
net.arc("porucha", "zanik", via=[(8.55, -0.9)])
net.loop("linka", "zanik", bend=12)

net.invariant({"linka": 1, "obsluha": 1, "prodl": 1}, 1)
