from pn import Net

net = Net("09–09", "Trafika (půlsemestrálka 2022/23, varianta B)")

# příchody: zákazník vstoupí, jen když je prodavač u pultu
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("vstup", (3, 0), label="příchozí", label_pos="above")
net.place("pritomen", (4.5, 1.7), tokens=1, label="přítomen", label_pos="left")
net.immediate("zarad", (4.5, 0), p=1, param_pos="below")
net.loop("pritomen", "zarad", bend=25)
net.immediate("neni", (3, -1.7), horizontal=True, exit=True,
              label="není prodavač: odchází", label_pos="below")
net.arc("prichod", "vstup")
net.arc("vstup", "zarad")
net.arc("vstup", "neni")

# obsluha u pultu
net.place("fronta", (6, 0), label="Fronta", label_pos="below")
net.place("prodavac", (7.5, 1.7), tokens=1, label="prodavač", label_pos="left")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(2 min)")
net.chain("zarad", "fronta", "obsaz", "obsluha", "obsl")
net.arc("prodavac", "obsaz")
net.arc("obsl", "prodavac", bend=-25)
net.place("konec", (12, 0), label="obsloužen", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# 10 min bez zákazníka -> sklad na 10 min
net.timed("necinnost", (7.5, 3.4), "10 min", horizontal=True, param_pos="right")
net.arc("prodavac", "necinnost")
net.place("nikdo", (6, 3.4), label="nikdo nepřišel", label_pos="below")
net.arc("necinnost", "nikdo")
net.immediate("do_skladu", (4.5, 3.4), p=2, label="do skladu", label_pos="above",
              param_pos="below right")
net.arc("nikdo", "do_skladu")
net.arc("pritomen", "do_skladu")
net.place("sklad", (3, 3.4), label="ve skladu", label_pos="above")
net.arc("do_skladu", "sklad")
net.timed("navrat", (1.5, 3.4), "10 min", label="návrat", label_pos="left",
          param_pos="below")
net.arc("sklad", "navrat")
net.arc("navrat", "pritomen")
net.arc("navrat", "prodavac", via=[(1.5, 4.9), (9.7, 4.9), (9.7, 2.6)])

net.invariant({"prodavac": 1, "obsluha": 1, "nikdo": 1, "sklad": 1}, 1)
net.invariant({"pritomen": 1, "sklad": 1}, 1)
net.bound("nikdo", 1)
