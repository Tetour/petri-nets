from pn import Net

net = Net("Psí salon (půlsemestrálka 2025/26, varianta A – zadání rekonstruované)")

# fronta se dělí: nahoru obsluha, rovně vyprázdnění fronty; obě větve končí v místě „ven“
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above left")
net.arc("prichod", "fronta")

# obsluha (horní řada)
net.place("linka", (4.5, 3.4), tokens=1, label="Linka obsluhy", label_pos="left")
net.immediate("obsaz", (4.5, 1.8))
net.place("strihani", (6, 1.8))
net.timed("obsluha", (7.5, 1.8), "exp(15 min)", param_pos="below")
net.arc("fronta", "obsaz", via=[(3, 1.8)], corner=20)
net.chain("obsaz", "strihani", "obsluha")
net.arc("linka", "obsaz")
net.arc("obsluha", "linka", out=90, into=0)
net.place("konec", (9, 0), label="ven", label_pos="above right")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.arc("obsluha", "konec", via=[(9, 1.8)], corner=20)
net.arc("konec", "odchod")

# všichni čekající odcházejí (p=1, smyčka s místem „poplach“)
net.immediate("vyprazdni", (4.5, 0), p=1, param_pos="above")
net.arc("fronta", "vyprazdni")
net.arc("vyprazdni", "konec")

# proces vyhlížení: někdo čeká ve frontě 1 h
net.place("vyhl", (1.5, -2.0), tokens=1, label="vyhlížení", label_pos="above")
net.timed("cekani", (3, -2.0), "1 h", param_pos="below")
net.place("poplach", (4.5, -2.0), label="poplach", label_pos="right")
net.arc("vyhl", "cekani")
net.arc("fronta", "cekani")
net.arc("cekani", "poplach")
net.loop("poplach", "vyprazdni", bend=25)

# deaktivace procesu příchodů na 3 h (řada běží zprava doleva zpět ke generátoru)
net.immediate("deaktivace", (4.5, -3.8), label="deaktivace příchodů", label_pos="below right")
net.arc("poplach", "deaktivace")
net.arc("gen", "deaktivace", via=[(-0.9, 0), (-0.9, -5.2), (4.5, -5.2)])
net.arc("deaktivace", "konec", via=[(9, -3.8)])
net.place("pauza", (3, -3.8))
net.timed("pauza_3h", (1.5, -3.8), "3 h", param_pos="below")
net.chain("deaktivace", "pauza", "pauza_3h")
net.arc("pauza_3h", "vyhl")
net.arc("pauza_3h", "gen", via=[(0, -3.8)])

net.invariant({"linka": 1, "strihani": 1}, 1)
net.invariant({"gen": 1, "pauza": 1}, 1)
net.invariant({"vyhl": 1, "poplach": 1, "pauza": 1}, 1)
net.sim_events = 50000
