from pn import Net

net = Net("09–20", "Pražírna kávy (půlsemestrálka 2010/11)")

# příchody a fronta; netrpělivý je jen první čekající (místo „první“ má doplněk)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 h)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("volno", (4.5, -1.6), tokens=1, label="1. místo volné", label_pos="left")
net.immediate("postup", (4.5, 0))
net.place("prvni", (6, 0), label="První", label_pos="above")
net.chain("prichod", "fronta", "postup", "prvni")
net.arc("volno", "postup")
net.timed("netrp", (6, -1.6), "1 min", horizontal=True, label="netrpělivost",
          label_pos="below right", param_pos="above right")
net.arc("prvni", "netrp")
net.arc("netrp", "volno")

# prodavač: obsluha, nebo po 10 min bez zákazníka pražení v dílně
net.place("prodavac", (9, 1.6), tokens=1, label="Prodavač v prodejně",
          label_pos="below right")
net.immediate("zacatek", (9, 0))
net.place("obsluhovan", (10.5, 0), label="Nakupuje", label_pos="above right")
net.chain("prvni", "zacatek", "obsluhovan")
net.arc("prodavac", "zacatek")
net.arc("zacatek", "volno")
net.timed("necinnost", (7.5, 1.6), "10 min", param_pos="left")
net.place("dilna", (7.5, 3.0), label="V dílně", label_pos="left")
net.timed("prazeni", (9, 3.0), "exp(1 h)", horizontal=True, label="pražení",
          label_pos="above", param_pos="right")
net.chain("prodavac", "necinnost", "dilna", "prazeni", "prodavac")

# 5 iterací nákupu, v každé koupí balíček s pravděpodobností 50 %
net.place("zbyva", (9, -1.6), label="Zbývá výběrů", label_pos="below")
net.arc("zacatek", "zbyva", w=5, w_pos="right")
net.immediate("vyber", (10.5, -1.6), p=1, horizontal=True, param_pos="right")
net.arc("obsluhovan", "vyber")
net.arc("zbyva", "vyber")
net.place("rozhoduje", (10.5, -3.2))
net.arc("vyber", "rozhoduje")
net.immediate("kupuje", (12, -3.2), prob=50, label="koupí", label_pos="below",
              param_pos="above right")
net.immediate("nekupuje", (12, -1.6), prob=50, label="nekoupí", label_pos="right",
              param_pos="below right")
net.arc("rozhoduje", "kupuje")
net.arc("rozhoduje", "nekupuje")
net.arc("nekupuje", "obsluhovan")
net.place("balicek", (14.25, -3.2), label="vybírá balíček", label_pos="below")
net.timed("nakup", (14.25, -1.6), "exp(1 min)", horizontal=True, param_pos="right")
net.chain("kupuje", "balicek", "nakup", "obsluhovan")

# konec nákupu (p=0: až po všech 5 výběrech), prodavač se vrací
net.immediate("konec_nakupu", (14.25, 0), label="konec nákupu", label_pos="below left")
net.arc("obsluhovan", "konec_nakupu")
net.arc("konec_nakupu", "prodavac", via=[(14.25, 1.6)])

# odchod ze systému (obsloužení i netrpěliví)
net.place("konec", (15.75, 0), label="konec", label_pos="above")
net.immediate("odchod", (17.25, 0), exit=True, label="odchod", label_pos="above")
net.chain("konec_nakupu", "konec", "odchod")
net.arc("netrp", "konec", via=[(6, -4.4), (15.75, -4.4)])

net.invariant({"volno": 1, "prvni": 1}, 1)
net.invariant({"prodavac": 1, "dilna": 1, "obsluhovan": 1, "rozhoduje": 1, "balicek": 1}, 1)
net.bound("zbyva", 5)
net.sim_events = 50000
