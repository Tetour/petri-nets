from pn import Net

net = Net("04–06", "M/M/1 – transakce po každé 10. dokončené obsluze zařadí údržbu linky trvající C")
net.params = {"A": 10, "B": 6, "C": 20}

# M/M/1; transakce drží linku i po obsluze, dokud se nerozhodne o údržbě
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.place("hotovo", (9, 0), label="obslouženo", label_pos="below right")
net.arc("obsl", "hotovo")

# uvolnění nad místem „obslouženo“: vrací linku a transakce pokračuje k odchodu
net.immediate("uvolneni", (9, 1.6), label="uvolnění", label_pos="above")
net.arc("hotovo", "uvolneni")
net.arc("uvolneni", "linka")
net.place("konec", (10.5, 1.6))
net.immediate("odchod", (12, 1.6), exit=True, label="odchod")
net.chain("uvolneni", "konec", "odchod")

# čítač dokončených obsluh; 10. transakce před uvolněním linky provede údržbu (p=1)
net.place("pocet", (7.5, -1.6), label="počet obsluh", label_pos="left")
net.arc("obsl", "pocet")
net.immediate("desata", (9, -1.6), p=1, label="10. obsluha", label_pos="below",
              param_pos="above right")
net.arc("pocet", "desata", w=10, w_pos="above")
net.arc("hotovo", "desata")
net.place("udrzba", (11.5, -1.6), label="údržba", label_pos="below")
net.arc("desata", "udrzba")
net.timed("t_udrzba", (11.5, 0), "C", param_pos="right")
net.arc("udrzba", "t_udrzba")
net.arc("t_udrzba", "hotovo")

net.invariant({"linka": 1, "obsluha": 1, "hotovo": 1, "udrzba": 1}, 1,
              name="linka je volná, nebo ji drží transakce (v obsluze, po ní, v údržbě)")
net.bound("pocet", 10)
