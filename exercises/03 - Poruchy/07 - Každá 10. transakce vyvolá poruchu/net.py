from pn import Net

net = Net("M/M/1, každá 10. obsloužená transakce vyvolá poruchu linky na dobu C")
net.params = {"A": 10, "B": 6, "C": 5}

# M/M/1 (rozmístění jako v úloze „Porucha vrací transakci do fronty“)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)", param_pos="below left")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka", label_pos="above left")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# porucha nad linkou (jako oprava v úloze „Porucha s opravou, návrat do fronty“): zabere linku (p=1, přednost před obsazením) na dobu C
net.immediate("porucha", (7.5, 3.2), p=1, param_pos="left")
net.arc("linka", "porucha")
net.place("oprava", (9, 3.2), label="porucha linky", label_pos="right")
net.timed("opr", (9, 1.6), "C", param_pos="right")
net.chain("porucha", "oprava", "opr", "linka")

# čítač dokončených obsluh pod obsluhou; hrana s váhou 10 vede kolem odchodu k poruše
net.place("citac", (7.5, -1.6), label="čítač", label_pos="below")
net.arc("obsl", "citac")
net.arc("citac", "porucha", w=10, w_pos="below", via=[(11.5, -1.6), (11.5, 4.6), (7.5, 4.6)])

net.invariant({"linka": 1, "obsluha": 1, "oprava": 1}, 1)
net.bound("citac", 10)
