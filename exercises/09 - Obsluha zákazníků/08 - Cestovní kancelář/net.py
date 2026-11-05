from pn import Net

net = Net("Cestovní kancelář (půlsemestrálka 2022/23, varianta D)")

# hlavní řada: příchody a obsluha u 3 (dočasně 5) přepážek
net.place("gen", (0, 0), tokens=1, label="příchody klientů", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.immediate("obsaz", (6, 0))
net.place("obsluha", (7.5, 0))
net.timed("obsl", (9, 0), "exp(8 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha", "obsl")
net.place("konec", (11.5, 0), label="hotovo", label_pos="above")
net.immediate("odchod", (13, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# přepážky pod hlavní řadou; návrat oblouk ze spodní strany přechodu
net.place("prepazky", (6, -2.2), tokens=3, label="Přepážky", label_pos="above left")
net.arc("prepazky", "obsaz")
net.arc("obsl", "prepazky", out=270, into=0)

# fronta >= 5: otevřít 2 přepážky na 1 h
net.place("nepridano", (0, -2.2), tokens=1, label="nepřidáno", label_pos="left")
net.immediate("otevri", (3, -2.2), label="otevři", label_pos="below left")
net.arc("fronta", "otevri", w=5, bend=-25, w_pos="left")
net.arc("otevri", "fronta", w=5, bend=-25, w_pos="right")
net.arc("nepridano", "otevri")
net.arc("otevri", "prepazky", w=2, w_pos="above")
net.place("pridano", (4.5, -4.2), label="přidáno", label_pos="below")
net.arc("otevri", "pridano", via=[(3, -4.2)])
net.timed("hodina", (6, -4.2), "1 h", param_pos="below")
net.place("zavirani", (7.5, -4.2), label="chci 2 zpět", label_pos="below")
net.arc("pridano", "hodina")
net.arc("hodina", "zavirani", w=2, w_pos="above")

# po hodině: každou uvolněnou přepážku (p=1) zavřít, po dvou obnovit stav
net.immediate("zavri", (10, -4.2), p=1, label="zavři", label_pos="below",
              param_pos="above right")
net.arc("zavirani", "zavri")
net.arc("prepazky", "zavri", via=[(6, -3.2), (10, -3.2)])
net.place("zavreno", (11.5, -4.2), label="zavřeno", label_pos="below")
net.immediate("obnov", (13, -4.2), label="obnov stav", label_pos="above")
net.arc("zavri", "zavreno")
net.arc("zavreno", "obnov", w=2, w_pos="above")
net.arc("obnov", "nepridano", via=[(13, -5.6), (0, -5.6)])

# 3 základní + 2 dočasné přepážky: zavřená dočasná je v „zavřeno“, obě nepřidané v „nepřidáno“
net.invariant({"prepazky": 1, "obsluha": 1, "nepridano": 2, "zavreno": 1}, 5)
# řízení je vždy v jednom stavu (zavírání a zavřeno počítají po polovinách)
net.invariant({"nepridano": 2, "pridano": 2, "zavirani": 1, "zavreno": 1}, 2)
# fronta 5 je při vytížení 27 % vzácná: delší běh, aby se přepážky otevřely víckrát
net.sim_events = 100000
