from pn import Net

net = Net("09–05", "Pizza stánek (půlsemestrálka 2024/25, varianta B – zadání z parafráze)")

# příchody
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")

# objednávka a příprava: pizzař + místo v peci
net.place("pizzar", (8.25, 2.2), tokens=1, label="Pizzař", label_pos="above")
net.place("pec", (4.5, -1.7), tokens=4, label="Pec (4 místa)", label_pos="below")
net.immediate("objednavka", (4.5, 0))
net.place("priprava", (6, 0), label="příprava", label_pos="below")
net.timed("pripr", (7.5, 0), "3–5 min")
net.chain("prichod", "fronta", "objednavka", "priprava", "pripr")
net.arc("pizzar", "objednavka")
net.arc("pec", "objednavka")
net.arc("pripr", "pizzar")

# pečení bez pizzaře
net.place("v_peci", (9, 0), label="v peci", label_pos="below")
net.timed("peceni", (10.5, 0), "4 min")
net.place("upeceno", (12, 0), label="upečeno", label_pos="below")
net.chain("pripr", "v_peci", "peceni", "upeceno")

# vyndání a předání pizzy má přednost před novým zákazníkem
net.immediate("vyndani", (13.5, 0), p=1, param_pos="below")
net.place("vyndavani", (15, 0), label="vyndávání", label_pos="below")
net.timed("predani", (16.5, 0), "1 min", param_pos="below right")
net.chain("upeceno", "vyndani", "vyndavani", "predani")
net.arc("pizzar", "vyndani")
net.arc("predani", "pizzar", via=[(16.5, 2.2)])
net.arc("predani", "pec", via=[(16.5, -1.7)])
net.place("konec", (18, 0), label="hotovo", label_pos="above")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("predani", "konec", "odchod")

net.invariant({"pizzar": 1, "priprava": 1, "vyndavani": 1}, 1)
net.invariant({"pec": 1, "priprava": 1, "v_peci": 1, "upeceno": 1, "vyndavani": 1}, 4)
