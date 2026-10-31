from pn import Net

net = Net("02–01", "M/M/1 s netrpělivými požadavky (čekání nejvýš 10)")
net.params = {"A": 10, "B": 8}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above left")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
net.arc("obsl", "linka", bend=-25)
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# netrpělivost: časovaný přechod přímo na Frontě, každý čekající má vlastní odpočet
net.timed("netrp", (6, -1.6), "10", horizontal=True, label="netrpělivost",
          label_pos="below", param_pos="above")
net.arc("fronta", "netrp", via=[(3, -1.6)])
net.arc("netrp", "konec", via=[(9, -1.6)])

net.invariant({"linka": 1, "obsluha": 1}, 1)
