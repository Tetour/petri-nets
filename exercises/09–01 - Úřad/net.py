from pn import Net

net = Net("09–01", "Úřad (půlsemestrálka 2025/26, varianta D – zadání rekonstruované)")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (6, 0))
net.place("linka", (6, -1.7), tokens=1, label="Úředníci", label_pos="left")
net.place("obsluha", (7.5, 0))
net.timed("vyrizeni", (9, 0), "exp(10 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "vyrizeni")
net.arc("linka", "obsaz")
net.arc("vyrizeni", "linka", bend=25)
net.place("konec", (10.5, 0), label="konec")
net.immediate("odchod", (12, 0), exit=True, label="odchod")
net.chain("vyrizeni", "konec", "odchod")

# proces rozšíření kapacity: ve frontě aspoň 5 → 2 další úředníci na 1 h
net.place("proces", (1.5, -3.6), tokens=1, label="proces rozšíření", label_pos="above")
net.immediate("rozsireni", (3, -3.6), label="rozšíření", label_pos="below")
net.arc("fronta", "rozsireni", w=5, bend=-12, w_pos="left")
net.arc("rozsireni", "fronta", w=5, bend=-12, w_pos="right")
net.arc("proces", "rozsireni")
net.arc("rozsireni", "linka", w=2, w_pos="above left")
net.place("rozsireno", (4.5, -3.6))
net.timed("hodina", (6, -3.6), "1 h", param_pos="below")
net.place("chci", (7.5, -3.6), label="chci 2 zpátky", label_pos="below")
net.chain("rozsireni", "rozsireno", "hodina")
net.arc("hodina", "chci", w=2, w_pos="above")

# úředníci se vrací po jednom, až dokončí rozpracovaného klienta
net.immediate("beru", (9.8, -3.6), p=1, label="beru si je zpět", label_pos="below", param_pos="above right")
net.chain("chci", "beru")
net.arc("linka", "beru")
net.place("vraceno", (11.3, -3.6))
net.immediate("mam", (12.8, -3.6), label="mám je", label_pos="above")
net.arc("beru", "vraceno")
net.arc("vraceno", "mam", w=2, w_pos="above")
net.arc("mam", "proces", via=[(12.8, -5.3), (1.5, -5.3)])

net.invariant({"linka": 1, "obsluha": 1, "rozsireno": -2, "chci": -1}, 1, name="Linka + obsluha = 1 + zapůjčení")
net.invariant({"proces": 2, "rozsireno": 2, "chci": 1, "vraceno": 1}, 2)
