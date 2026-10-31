from pn import Net

net = Net("04–05", "M/M/1 – trvala-li obsluha C a déle, následuje údržba D")
net.params = {"A": 10, "B": 6, "C": 10, "D": 5}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("linka", (5.4, 1.7), tokens=1, label="Linka", label_pos="below right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6.3, 0))
net.timed("obsl", (7.8, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9.3, 0))
net.immediate("odchod", (10.8, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# s obsazením linky se spustí časovač C, který běží souběžně s obsluhou
net.place("casovac", (2.7, 3.4), label="časovač", label_pos="left")
net.arc("obsaz", "casovac")
net.timed("t_c", (2.7, 5.1), "C", horizontal=True, param_pos="left")
net.arc("casovac", "t_c")
net.place("uplynulo", (6.6, 5.1), label="uplynulo C", label_pos="right")
net.arc("t_c", "uplynulo")

# obsluha skončila dřív: vrácená linka (testovací hrany) zruší běžící časovač
net.immediate("kratka", (4.5, 3.4), p=1, label="kratší než C", label_pos="above",
              param_pos="below left")
net.arc("casovac", "kratka")
net.loop("linka", "kratka", bend=20)

# obsluha trvala aspoň C: vrácenou linku si vezme údržba dřív než další zákazník
net.immediate("dlouha", (6.6, 3.4), p=1, horizontal=True, param_pos="left")
net.arc("uplynulo", "dlouha")
net.arc("linka", "dlouha")
net.place("udrzba", (8.4, 3.4), label="údržba", label_pos="above")
net.arc("dlouha", "udrzba")
net.timed("t_d", (8.4, 1.7), "D", param_pos="right")
net.arc("udrzba", "t_d")
net.arc("t_d", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, nebo je v údržbě")
net.invariant({"obsluha": 1, "casovac": -1, "uplynulo": -1}, 0,
              name="časovač běží (nebo uplynul) právě během obsluhy")
