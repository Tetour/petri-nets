from pn import Net

net = Net("09–20", "Pražírna kávy (půlsemestrálka 2010/11)")

# příchody a fronta; netrpělivý je jen první čekající (místo „první“ má doplněk)
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 h)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("volno", (4.5, 1.6), tokens=1, label="1. místo volné", label_pos="left")
net.immediate("postup", (4.5, 0))
net.place("prvni", (6, 0), label="první", label_pos="below")
net.chain("prichod", "fronta", "postup", "prvni")
net.arc("volno", "postup")
net.timed("netrp", (6, 1.6), "1 min", param_pos="right")
net.arc("prvni", "netrp")
net.arc("netrp", "volno")
net.place("odesel", (6, 2.7), label="neobsloužen", label_pos="left")
net.immediate("odchod_n", (6, 3.8), exit=True, label="odchod", label_pos="right")
net.chain("netrp", "odesel", "odchod_n")

# začátek obsluhy uvolní 1. místo (oblouk nad netrpělivostí) a vezme prodavače zdola
net.place("prodavac", (7.5, -1.6), tokens=1, label="Prodavač", label_pos="below left")
net.immediate("zacatek", (7.5, 0))
net.place("nakup_m", (9, 0), label="nákup", label_pos="below right")
net.chain("prvni", "zacatek", "nakup_m")
net.arc("prodavac", "zacatek")
net.arc("zacatek", "volno", via=[(7.5, 4.6), (4.5, 4.6)])

# prodavač po 10 min bez zákazníka odchází do dílny, po pražení exp(1 h) se vrací
net.timed("necinnost", (5.7, -1.6), "10 min", param_pos="below")
net.place("dilna", (4.2, -1.6), label="v dílně", label_pos="left")
net.timed("prazeni", (4.2, -3.2), "exp(1 h)", param_pos="left")
net.chain("prodavac", "necinnost", "dilna", "prazeni")
net.arc("prazeni", "prodavac", via=[(7.5, -3.2)])

# 5 iterací nákupu (čítač „výběry“), v každé koupí balíček s pravděpodobností 50 %
net.immediate("vyber", (10.5, 0), label="výběr", label_pos="above right")
net.place("rozhoduje", (12, 0), label="rozhoduje se", label_pos="below")
net.chain("nakup_m", "vyber", "rozhoduje")
net.immediate("nekupuje", (12, 1.6), prob=50, label="nekoupí", label_pos="above",
              param_pos="right")
net.arc("rozhoduje", "nekupuje")
net.immediate("kupuje", (13.5, 0), prob=50, label="koupí", label_pos="below", param_pos="right")
net.arc("rozhoduje", "kupuje")
net.place("balicek", (12, 3.2), label="vybírá balíček", label_pos="above")
net.arc("kupuje", "balicek", via=[(13.5, 3.2)])
net.timed("nakup", (10.5, 3.2), "exp(1 min)", param_pos="left")
net.arc("balicek", "nakup")
net.place("vybrano", (10.5, 1.6), label="vybráno", label_pos="above left")
net.arc("nakup", "vybrano")
net.arc("nekupuje", "vybrano")
net.immediate("dalsi", (9, 1.6))
net.chain("vybrano", "dalsi", "nakup_m")
net.place("vybery", (10.5, -1.6), label="provedené výběry", label_pos="right")
net.arc("vyber", "vybery")

# konec nákupu (p=1) po 5 výběrech: prodavač se vrací, zákazník odchází
net.immediate("konec_nakupu", (9, -1.6), p=1, label="konec", label_pos="below right",
              param_pos="above left")
net.arc("nakup_m", "konec_nakupu")
net.arc("vybery", "konec_nakupu", w=5, w_pos="above")
net.arc("konec_nakupu", "prodavac")
net.place("konec", (9, -3.2), label="obsloužen", label_pos="below")
net.immediate("odchod", (10.5, -3.2), exit=True, label="odchod", label_pos="right")
net.chain("konec_nakupu", "konec", "odchod")

net.invariant({"volno": 1, "prvni": 1}, 1)
net.invariant({"prodavac": 1, "dilna": 1, "nakup_m": 1, "rozhoduje": 1, "balicek": 1,
               "vybrano": 1}, 1)
net.bound("vybery", 5)
net.sim_events = 50000
