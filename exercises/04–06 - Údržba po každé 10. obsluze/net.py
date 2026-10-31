from pn import Net

net = Net("04–06", "M/M/1 – transakce po každé 10. dokončené obsluze zařadí údržbu linky trvající C")
net.params = {"A": 10, "B": 6, "C": 20}

# M/M/1; transakce drží linku i po obsluze, dokud se nerozhodne o údržbě
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.place("hotovo", (9.3, 0), label="obslouženo", label_pos="above")
net.immediate("uvolneni", (10.8, 0), label="uvolnění", label_pos="above right")
net.chain("obsl", "hotovo", "uvolneni")
net.arc("uvolneni", "linka", via=[(10.8, 1.7)])
net.place("konec", (12.6, 0))
net.immediate("odchod", (14.1, 0), exit=True, label="odchod")
net.chain("uvolneni", "konec", "odchod")

# čítač dokončených obsluh; 10. transakce před uvolněním linky provede údržbu (p=1)
net.place("pocet", (7.8, -1.7), label="počet obsluh", label_pos="left")
net.arc("obsl", "pocet")
net.immediate("desata", (9.3, -1.7), p=1, label="10. obsluha", label_pos="below",
              param_pos="above left")
net.arc("pocet", "desata", w=10, w_pos="below")
net.arc("hotovo", "desata")
net.place("udrzba", (10.8, -1.7), label="údržba", label_pos="below")
net.arc("desata", "udrzba")
net.timed("t_udrzba", (12.3, -1.7), "C", param_pos="below")
net.arc("udrzba", "t_udrzba")
net.arc("t_udrzba", "hotovo", via=[(12.3, -0.9), (9.9, -0.9)])

net.invariant({"linka": 1, "obsluha": 1, "hotovo": 1, "udrzba": 1}, 1,
              name="linka je volná, nebo ji drží transakce (v obsluze, po ní, v údržbě)")
net.bound("pocet", 10)
