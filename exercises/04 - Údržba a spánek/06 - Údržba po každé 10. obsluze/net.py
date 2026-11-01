from pn import Net

net = Net("M/M/1 – transakce po každé 10. dokončené obsluze zařadí údržbu linky trvající C")
net.params = {"A": 10, "B": 6, "C": 20}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below left")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat linky
net.place("konec", (9, 0), label="obslouženo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# čítač obsluh: každá dokončená obsluha přidá značku (hrana oklikou kolem konce řady)
net.place("pocet", (7.5, 3.2), label="počet obsluh", label_pos="above")
net.arc("obsl", "pocet", via=[(7.5, -1.2), (12, -1.2), (12, 3.2)])

# po 10. obsluze vezme údržba volnou linku dřív než další transakce (p=1)
net.immediate("do_udrzby", (4.5, 3.2), p=1, label="do údržby", label_pos="above",
              param_pos="below right")
net.arc("pocet", "do_udrzby", w=10, w_pos="above")
net.arc("linka", "do_udrzby")
net.place("udrzba", (3, 3.2), label="údržba", label_pos="above")
net.arc("do_udrzby", "udrzba")
net.timed("konec_udrzby", (3, 1.6), "C", param_pos="left")
net.arc("udrzba", "konec_udrzby")
net.arc("konec_udrzby", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, nebo je v údržbě")
net.bound("pocet", 10)
