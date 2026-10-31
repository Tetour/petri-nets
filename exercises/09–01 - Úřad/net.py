from pn import Net

net = Net("09–01", "Úřad (půlsemestrálka 2025/26, varianta D – zadání rekonstruované)")

# hlavní řada: příchody a obsluha klientů
net.place("gen", (0, 0), tokens=1, label="příchody klientů", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.immediate("obsaz", (6, 0))
net.place("obsluha", (7.5, 0))
net.timed("vyrizeni", (9, 0), "exp(10 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "vyrizeni")
net.place("konec", (11.5, 0), label="konec", label_pos="above")
net.immediate("odchod", (13, 0), exit=True, label="odchod")
net.chain("vyrizeni", "konec", "odchod")

# úředníci pod hlavní řadou; návrat oblouk ze spodní strany přechodu
net.place("linka", (6, -2.2), tokens=1, label="Úředníci", label_pos="above left")
net.arc("linka", "obsaz")
net.arc("vyrizeni", "linka", out=270, into=0)

# proces rozšíření: ve frontě aspoň 5 → 2 další úředníci na 1 h
net.place("proces", (0, -2.2), tokens=1, label="proces rozšíření", label_pos="left")
net.immediate("rozsireni", (3, -2.2), label="rozšíření", label_pos="below left")
net.arc("fronta", "rozsireni", w=5, bend=-25, w_pos="left")
net.arc("rozsireni", "fronta", w=5, bend=-25, w_pos="right")
net.arc("proces", "rozsireni")
net.arc("rozsireni", "linka", w=2, w_pos="above")
net.place("rozsireno", (4.5, -4.2))
net.arc("rozsireni", "rozsireno", via=[(3, -4.2)], corner=20)
net.timed("hodina", (6, -4.2), "1 h", param_pos="below")
net.place("chci", (7.5, -4.2), label="chci 2 zpátky", label_pos="below")
net.arc("rozsireno", "hodina")
net.arc("hodina", "chci", w=2, w_pos="above")

# úředníci se vrací po jednom, až dokončí rozpracovaného klienta
net.immediate("beru", (10, -4.2), p=1, label="beru si je zpět", label_pos="below",
              param_pos="above right")
net.arc("chci", "beru")
net.arc("linka", "beru", via=[(6, -3.2), (10, -3.2)])
net.place("vraceno", (11.5, -4.2))
net.immediate("mam", (13, -4.2), label="mám je", label_pos="above")
net.arc("beru", "vraceno")
net.arc("vraceno", "mam", w=2, w_pos="above")
net.arc("mam", "proces", via=[(13, -5.6), (0, -5.6)])

net.invariant({"linka": 1, "obsluha": 1, "rozsireno": -2, "chci": -1}, 1, name="Linka + obsluha = 1 + zapůjčení")
net.invariant({"proces": 2, "rozsireno": 2, "chci": 1, "vraceno": 1}, 2)
