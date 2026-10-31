from pn import Net

net = Net("04–05", "M/M/1 – trvala-li obsluha C a déle, následuje údržba D")
net.params = {"A": 10, "B": 6, "C": 10, "D": 5}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka", label_pos="below left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below left")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)  # návrat linky
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# s obsazením linky se spustí časovač C, který běží souběžně s obsluhou
# (hrana z obsazení vede oklikou kolem konce řady)
net.place("casovac", (7.5, 4.8), label="časovač", label_pos="above")
net.arc("obsaz", "casovac", via=[(4.5, -1.2), (12, -1.2), (12, 4.8)])
net.timed("t_c", (6, 4.8), "C", param_pos="above")
net.arc("casovac", "t_c")
net.place("uplynulo", (4.5, 4.8), label="uplynulo C", label_pos="above")
net.arc("t_c", "uplynulo")

# obsluha skončila dřív: vrácená linka (testovací hrany) zruší běžící časovač
net.immediate("kratka", (6, 3.2), p=1, label="kratší než C", label_pos="above",
              param_pos="below right")
net.arc("casovac", "kratka", via=[(7.5, 3.2)])
net.loop("linka", "kratka", bend=20)

# obsluha trvala aspoň C: vrácenou linku si vezme údržba dřív než další transakce
net.immediate("dlouha", (4.5, 3.2), p=1, param_pos="right")
net.arc("uplynulo", "dlouha")
net.arc("linka", "dlouha")
net.place("udrzba", (3, 3.2), label="údržba", label_pos="above")
net.arc("dlouha", "udrzba")
net.timed("t_d", (3, 1.6), "D", param_pos="left")
net.arc("udrzba", "t_d")
net.arc("t_d", "linka")

net.invariant({"linka": 1, "obsluha": 1, "udrzba": 1}, 1,
              name="linka je volná, obsluhuje, nebo je v údržbě")
net.invariant({"obsluha": 1, "casovac": -1, "uplynulo": -1}, 0,
              name="časovač běží (nebo uplynul) právě během obsluhy")
