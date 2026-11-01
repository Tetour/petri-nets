from pn import Net

net = Net("M/M/1 s netrpělivými požadavky (čekání nejvýš 10)")
net.params = {"A": 10, "B": 8}

# M/M/1
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("linka", (4.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(B)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("linka", "obsaz")
# návrat linky: oblouk z horní strany přechodu
net.arc("obsl", "linka", out=90, into=0)
net.place("konec", (9, 0), label="konec", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# netrpělivost: časovaný přechod přímo na frontě, každý čekající má vlastní odpočet
net.timed("netrp", (6, -1.8), "10", label="netrpělivost", label_pos="below",
          param_pos="above")
net.arc("fronta", "netrp", via=[(3, -1.8)], corner=20)
net.arc("netrp", "konec", via=[(9, -1.8)], corner=20)

net.invariant({"linka": 1, "obsluha": 1}, 1)
