from pn import Net

net = Net("03–02", "M/M/1, porucha přeruší obsluhu a transakce se vrací do fronty")
net.params = {"A": 10, "B": 6, "X": 50}

# M/M/1; Linka je nad obsluhou, aby k ní vedla hrana z přerušení zprava kolem odchodu
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# poruchy: řada pod linkou, přerušení přímo pod místem obsluha
net.place("gen_p", (3, -3.2), tokens=1, label="vznik poruch", label_pos="left")
net.timed("vznik", (4.5, -3.2), "exp(X)")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -3.2), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
net.immediate("preruseni", (6, -1.6), p=1, param_pos="above left")
net.arc("obsluha", "preruseni")
net.arc("porucha", "preruseni")
# přerušená transakce zpět do fronty (vlevo), linka zpět (vpravo kolem odchodu)
net.arc("preruseni", "fronta", via=[(3, -1.6)])
net.arc("preruseni", "linka", via=[(11.5, -1.6), (11.5, 1.6)])
net.immediate("zanik", (7.5, -3.2), label="porucha bez účinku", label_pos="right")
net.arc("porucha", "zanik")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.bound("porucha", 1)
