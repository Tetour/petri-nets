from pn import Net

net = Net("09–08", "Cestovní kancelář (půlsemestrálka 2022/23, varianta D)")

# příchody a obsluha u 3 (dočasně 5) přepážek
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(10 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("prepazky", (4.5, 1.7), tokens=3, label="Přepážky", label_pos="above right")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0))
net.timed("obsl", (7.5, 0), "exp(8 min)")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.arc("prepazky", "obsaz")
net.arc("obsl", "prepazky", bend=-15)
net.place("konec", (9, 0), label="hotovo", label_pos="below")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# fronta >= 5: otevřít 2 přepážky na 1 h
net.place("nepridano", (1.5, 3.4), tokens=1, label="nepřidáno", label_pos="left")
net.immediate("otevri", (3, 3.4), label="otevři", label_pos="above")
net.arc("nepridano", "otevri")
net.arc("fronta", "otevri", w=5, bend=-15, w_pos="right")
net.arc("otevri", "fronta", w=5, bend=-15, w_pos="left")
net.arc("otevri", "prepazky", w=2, w_pos="above right")
net.place("pridano", (4.5, 3.4), label="přidáno", label_pos="above")
net.timed("hodina", (6, 3.4), "1 h")
net.place("zavirani", (7.5, 3.4), label="chci 2 zpět", label_pos="above")
net.chain("otevri", "pridano", "hodina")
net.arc("hodina", "zavirani", w=2, w_pos="above")

# po hodině: každou uvolněnou přepážku (p=1) zavřít, po dvou obnovit stav
net.immediate("zavri", (7.5, 1.7), p=1, horizontal=True, param_pos="above left")
net.arc("zavirani", "zavri")
net.arc("prepazky", "zavri")
net.place("zavreno", (9, 1.7), label="zavřeno", label_pos="below right")
net.arc("zavri", "zavreno")
net.immediate("obnov", (9, 3.4), horizontal=True, label="obnov stav", label_pos="right")
net.arc("zavreno", "obnov", w=2, w_pos="right")
net.arc("obnov", "nepridano", via=[(9, 4.9), (1.5, 4.9)])

# 3 základní + 2 dočasné přepážky: zavřená dočasná je v „zavřeno“, obě nepřidané v „nepřidáno“
net.invariant({"prepazky": 1, "obsluha": 1, "nepridano": 2, "zavreno": 1}, 5)
# řízení je vždy v jednom stavu (zavírání a zavřeno počítají po polovinách)
net.invariant({"nepridano": 2, "pridano": 2, "zavirani": 1, "zavreno": 1}, 2)
# fronta 5 je při vytížení 27 % vzácná: delší běh, aby se přepážky otevřely víckrát
net.sim_events = 100000
