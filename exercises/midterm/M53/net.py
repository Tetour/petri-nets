from pn import Net

net = Net("M53", "Psí salon (půlsemestrálka 2025/26, varianta A – zadání rekonstruované)")

# příchody a obsluha
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka obsluhy")
net.immediate("obsaz", (4.5, 0))
net.place("strihani", (6, 0))
net.timed("obsluha", (7.5, 0), "exp(15 min)")
net.chain("prichod", "fronta", "obsaz", "strihani", "obsluha")
net.arc("linka", "obsaz")
net.arc("obsluha", "linka", bend=-25)
net.place("konec", (9, 0), label="ven", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True)
net.chain("obsluha", "konec", "odchod")

# proces vyhlížení: někdo čeká ve frontě 1 h
net.place("vyhl", (1.5, -2.5), tokens=1, label="vyhlížení", label_pos="above")
net.timed("cekani", (3, -2.5), "1 h")
net.place("poplach", (4.5, -2.5), label="poplach", label_pos="above")
net.arc("vyhl", "cekani")
net.arc("fronta", "cekani")
net.arc("cekani", "poplach")

# všichni čekající odcházejí
net.immediate("vyprazdni", (6.2, -2.5), p=1, param_pos="below right")
net.loop("poplach", "vyprazdni", bend=25)
net.arc("fronta", "vyprazdni")
net.arc("vyprazdni", "konec", via=[(9, -2.5)])

# deaktivace procesu příchodů na 3 h
net.immediate("deaktivace", (6.2, -4.5), label="deaktivace příchodů", label_pos="below")
net.arc("poplach", "deaktivace")
net.arc("gen", "deaktivace", via=[(0, -4.5)])
net.arc("deaktivace", "konec")
net.place("pauza", (7.6, -4.5))
net.timed("pauza_3h", (9, -4.5), "3 h", param_pos="right")
net.chain("deaktivace", "pauza", "pauza_3h")
net.arc("pauza_3h", "vyhl", via=[(9, -5.6), (1.5, -5.6)])
net.arc("pauza_3h", "gen", via=[(9, -6.2), (-0.9, -6.2), (-0.9, 0)])

net.invariant({"linka": 1, "strihani": 1}, 1)
net.invariant({"gen": 1, "pauza": 1}, 1)
net.invariant({"vyhl": 1, "poplach": 1, "pauza": 1}, 1)
net.sim_events = 50000
