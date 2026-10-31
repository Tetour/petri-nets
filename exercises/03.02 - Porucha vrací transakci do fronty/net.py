from pn import Net

net = Net("03.02", "M/M/1, porucha přeruší obsluhu a transakce se vrací do fronty")
net.params = {"A": 10, "B": 6, "X": 50}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka")
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
net.timed("vznik", (9.3, -1.8), "exp(X)", param_pos="below")
net.loop("gen_p", "vznik")
net.place("porucha", (7.8, -1.8), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.immediate("preruseni", (5.4, -1.8), p=1, horizontal=True, param_pos="below")
net.arc("obsluha", "preruseni")
net.arc("porucha", "preruseni")
net.arc("preruseni", "fronta", via=[(3, -1.8)])
net.arc("preruseni", "linka")
net.immediate("zanik", (7.8, -3.4), horizontal=True, label="porucha bez účinku",
              label_pos="right", param_pos="right")
net.arc("porucha", "zanik")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.bound("porucha", 1)
