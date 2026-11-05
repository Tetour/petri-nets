from pn import Net

net = Net("Trafika (půlsemestrálka 2022/23, varianta B)")

# příchody: zákazník vstoupí, jen když je prodavač u pultu (test místa „přítomen“)
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("vstup", (3, 0), label="příchozí", label_pos="above")
net.arc("prichod", "vstup")
net.place("pritomen", (4.5, 1.6), tokens=1, label="přítomen", label_pos="left")
net.immediate("zarad", (4.5, 0), p=1, param_pos="below")
net.arc("vstup", "zarad")
net.loop("pritomen", "zarad", bend=25)
# prodavač chybí (p=0): zákazník hned odchází
net.immediate("neni", (4.5, -1.6), exit=True, label="odchod (prodavač chybí)", label_pos="right")
net.arc("vstup", "neni", via=[(3, -1.6)])

# obsluha u pultu
net.place("fronta", (6, 0), label="fronta", label_pos="below")
net.place("prodavac", (7.5, 1.6), tokens=1, label="prodavač", label_pos="above right")
net.immediate("obsaz", (7.5, 0))
net.place("obsluha", (9, 0))
net.timed("obsl", (10.5, 0), "exp(2 min)", param_pos="below")
net.chain("zarad", "fronta", "obsaz", "obsluha", "obsl")
net.arc("prodavac", "obsaz")
net.arc("obsl", "prodavac", out=90, into=0)
net.place("konec", (12, 0), label="obsloužen", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.chain("obsl", "konec", "odchod")

# 10 min bez zákazníka -> sklad na 10 min (cyklus nad prodavačem a přítomností)
net.timed("necinnost", (7.5, 3.2), "10 min", param_pos="right")
net.arc("prodavac", "necinnost")
net.place("nikdo", (7.5, 4.8), label="nikdo nepřišel", label_pos="right")
net.arc("necinnost", "nikdo")
net.immediate("do_skladu", (6.4, 4.8), p=2, label="do skladu", label_pos="above",
              param_pos="below left")
net.arc("nikdo", "do_skladu")
net.arc("pritomen", "do_skladu", via=[(4.5, 4.8)])
net.place("sklad", (6.4, 3.2), label="ve skladu", label_pos="left")
net.arc("do_skladu", "sklad")
net.timed("navrat", (6.4, 1.6), "10 min", label="návrat", label_pos="above left",
          param_pos="below")
net.arc("sklad", "navrat")
net.arc("navrat", "pritomen")
net.arc("navrat", "prodavac")

net.invariant({"prodavac": 1, "obsluha": 1, "nikdo": 1, "sklad": 1}, 1)
net.invariant({"pritomen": 1, "sklad": 1}, 1)
net.bound("nikdo", 1)
