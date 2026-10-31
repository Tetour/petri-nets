from pn import Net

net = Net("09–14", "Pekárna (půlsemestrálky 2014–19, Z14)")

# příchody a obsluha u pultu
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(20 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("pekar", (4.5, 1.7), tokens=1, label="Pekař u pultu", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("zacatek", (6, 0), label="začátek obsluhy", label_pos="above")
net.immediate("prodej", (7.5, 0), p=1, param_pos="above right")
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "1–2 min", param_pos="below right")
net.chain("prichod", "fronta", "obsaz", "zacatek", "prodej", "obsluha", "obsl")
net.arc("pekar", "obsaz")
net.arc("obsl", "pekar", via=[(10.5, 1.7)])
net.place("chleba", (9, -1.75), tokens=20, label="Chléb na pultě", label_pos="right")
net.arc("chleba", "prodej")
net.place("konec", (12, 0), label="s chlebem", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("obsl", "konec", "odchod")

# na začátku obsluhy došel chléb (p=0): zákazník odchází, pekař jde péct
net.immediate("doslo", (6, -1.75), horizontal=True, label="došel chléb", label_pos="right")
net.arc("zacatek", "doslo")
net.place("bez", (6, -3.5))
net.immediate("odchod_b", (6, -5), horizontal=True, exit=True, label="odchod", label_pos="right")
net.chain("doslo", "bez", "odchod_b")
net.place("pece", (7.5, -3.5))
net.timed("peceni", (9, -3.5), "2 h", param_pos="below")
net.place("upeceno", (10.5, -3.5), label="upečeno", label_pos="below")
net.immediate("navrat", (12, -3.5), label="návrat k pultu", label_pos="below right")
net.chain("doslo", "pece", "peceni", "upeceno", "navrat")
net.arc("peceni", "chleba", w=20, w_pos="left")
net.arc("navrat", "pekar", via=[(14.4, -3.5), (14.4, 2.6), (4.5, 2.6)])

# během pečení odcházejí čekající i nově příchozí
net.place("peceS", (4.5, -3.5), label="Pekař peče", label_pos="below left")
net.arc("doslo", "peceS")
net.arc("peceS", "navrat", via=[(4.5, -5.8), (12, -5.8)])
net.immediate("vyprazdni", (3, -1.75), horizontal=True, label="vyprázdnění fronty",
              label_pos="above left")
net.arc("fronta", "vyprazdni")
net.loop("peceS", "vyprazdni", bend=20)
net.place("pryc", (1.5, -3.5), label="bez chleba", label_pos="below")
net.immediate("odchod_f", (0, -3.5), exit=True, label="odchod", label_pos="above")
net.chain("vyprazdni", "pryc", "odchod_f")

net.invariant({"pekar": 1, "zacatek": 1, "obsluha": 1, "pece": 1, "upeceno": 1}, 1)
net.invariant({"peceS": 1, "pece": -1, "upeceno": -1}, 0, name="Pekař peče = pece + upečeno")
net.bound("chleba", 20)
