from pn import Net

net = Net("M/M/1, příchody se při frontě 5 přeruší na 10 č. j.")
net.params = {"A": 5, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta dosáhne 5: přerušení vezme značku příchodů (zespodu), test přímo pod Frontou
net.immediate("preruseni", (3, -1.6), p=1, label="přerušení", label_pos="below left",
              param_pos="below right")
net.arc("fronta", "preruseni", w=5, bend=25, w_pos="right")
net.arc("preruseni", "fronta", w=5, bend=25, w_pos="left")
net.arc("gen", "preruseni", via=[(0, -1.6)])
net.place("preruseno", (4.5, -1.6), label="přerušeno", label_pos="below")
net.timed("trvani", (6, -1.6), "10", param_pos="above")
net.chain("preruseni", "preruseno", "trvani")

# po 10 č. j. se značka vrací do příchodů zleva
net.arc("trvani", "gen", via=[(6, -2.7), (-1.2, -2.7), (-1.2, 0)])

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "preruseno": 1}, 1, name="příchody běží, nebo jsou přerušené")
net.bound("fronta", 5)
