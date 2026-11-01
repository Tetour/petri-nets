from pn import Net

net = Net("M/M/1, porucha zabere linku na dobu R, přerušená transakce se vrací do fronty")
net.params = {"A": 10, "B": 6, "E": 100, "R": 5}

# M/M/1 (rozmístění jako v úloze „Porucha vrací transakci do fronty“)
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="obsluha")
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("linka", (7.5, 1.6), tokens=1, label="Linka", label_pos="above left")
net.arc("linka", "obsaz", via=[(4.5, 1.6)])
net.arc("obsl", "linka")
net.place("konec", (9, 0), label="hotovo")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# oprava nad linkou: porucha zabere linku (p=1, přednost před obsazením transakcí) na dobu R
net.immediate("zabrani", (7.5, 3.2), p=1, param_pos="left")
net.arc("linka", "zabrani")
net.place("oprava", (9, 3.2), label="oprava")
net.timed("opr", (9, 1.6), "R", param_pos="right")
net.chain("zabrani", "oprava", "opr", "linka")

# poruchy: řada pod linkou, přerušení přímo pod místem obsluha
net.place("gen_p", (3, -3.2), tokens=1, label="vznik poruch", label_pos="left")
net.timed("vznik", (4.5, -3.2), "exp(E)")
net.loop("gen_p", "vznik")
net.place("porucha", (6, -3.2), label="porucha", label_pos="below")
net.arc("vznik", "porucha")
# obsazená linka: porucha převezme linku obsluhované transakce rovnou do opravy
net.immediate("preruseni", (6, -1.6))
net.arc("obsluha", "preruseni")
net.arc("porucha", "preruseni")
# přerušená transakce zpět do fronty (vlevo)
net.arc("preruseni", "fronta", via=[(3, -1.6)])
net.arc("preruseni", "oprava", via=[(11.5, -1.6), (11.5, 3.2)])
# volná linka: porucha ji zabere (hrana kolem přerušení a odchodu)
net.arc("porucha", "zabrani", via=[(12.2, -3.2), (12.2, 4.6), (7.5, 4.6)])

net.invariant({"linka": 1, "obsluha": 1, "oprava": 1}, 1)
