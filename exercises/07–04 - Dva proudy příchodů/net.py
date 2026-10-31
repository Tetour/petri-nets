from pn import Net

net = Net("07–04", "M/M/1 se dvěma proudy příchodů, prioritní mají vyšší prioritu obsluhy")
net.params = {"A": 10, "P": 30, "B": 6}

# prioritní proud (nahoře)
net.place("gen_p", (0, 4), tokens=1, label="generátor P", label_pos="above")
net.timed("prichod_p", (1.5, 4), "exp(P)")
net.loop("gen_p", "prichod_p")
net.place("fronta_p", (3, 4), label="Fronta P")
net.immediate("obsaz_p", (4.5, 4), p=1, param_pos="above")
net.place("obsluha_p", (6.3, 4))
net.timed("obsl_p", (7.8, 4), "exp(B)", param_pos="above")
net.chain("prichod_p", "fronta_p", "obsaz_p", "obsluha_p", "obsl_p")

# normální proud (dole)
net.place("gen_n", (0, 0), tokens=1, label="generátor N", label_pos="below")
net.timed("prichod_n", (1.5, 0), "exp(A)")
net.loop("gen_n", "prichod_n")
net.place("fronta_n", (3, 0), label="Fronta N", label_pos="below")
net.immediate("obsaz_n", (4.5, 0))
net.place("obsluha_n", (6.3, 0))
net.timed("obsl_n", (7.8, 0), "exp(B)")
net.chain("prichod_n", "fronta_n", "obsaz_n", "obsluha_n", "obsl_n")

# jedna linka pro oba proudy
net.place("linka", (5.4, 2), tokens=1, label="Linka", label_pos="above right")
net.arc("linka", "obsaz_p")
net.arc("linka", "obsaz_n")
net.arc("obsl_p", "linka", bend=40)
net.arc("obsl_n", "linka", bend=-40)

# priorita obsluhy: čekající prioritní vyhodí normální transakci z obsluhy
net.immediate("preruseni", (3, 2), label="přerušení", label_pos="left")
net.loop("fronta_p", "preruseni", bend=20)
net.arc("obsluha_n", "preruseni")
net.arc("preruseni", "fronta_n")
net.arc("preruseni", "linka")

net.place("konec", (9.3, 2))
net.immediate("odchod", (10.8, 2), exit=True, label="odchod")
net.arc("obsl_p", "konec")
net.arc("obsl_n", "konec")
net.arc("konec", "odchod")

net.invariant({"linka": 1, "obsluha_p": 1, "obsluha_n": 1}, 1)
