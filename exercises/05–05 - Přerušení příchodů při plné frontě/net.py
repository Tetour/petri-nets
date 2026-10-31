from pn import Net

net = Net("05–05", "M/M/1, příchody se při frontě 5 přeruší na 10 č. j.")
net.params = {"A": 5, "B": 6}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(A)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linka", (4.5, 1.7), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9, 0))
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta dosáhne 5: generátor přijde o značku na 10 č. j.
net.immediate("preruseni", (1.5, -2), p=1, label="přerušení", label_pos="right",
              param_pos="left")
net.arc("gen", "preruseni")
net.arc("fronta", "preruseni", w=5, bend=-20, w_pos="left")
net.arc("preruseni", "fronta", w=5, bend=-20, w_pos="below right")
net.place("preruseno", (1.5, -3.6), label="přerušeno", label_pos="right")
net.arc("preruseni", "preruseno")
net.timed("trvani", (0, -3.6), "10", param_pos="left")
net.arc("preruseno", "trvani")
net.arc("trvani", "gen")

net.invariant({"linka": 1, "obsluha": 1}, 1)
net.invariant({"gen": 1, "preruseno": 1}, 1, name="příchody běží, nebo jsou přerušené")
net.bound("fronta", 5)
