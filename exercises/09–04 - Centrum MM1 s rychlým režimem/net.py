from pn import Net

net = Net("09–04", "Centrum M/M/1 s rychlým režimem (půlsemestrálka 2024/25, varianta D)")

# příchody a obsazení linky
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above left")
net.place("linka", (4.5, 1.8), tokens=1, label="Linka", label_pos="right")
net.immediate("seize", (4.5, 0), p=1, param_pos="below right")
net.place("vybrano", (6, 0))
net.chain("prichod", "fronta", "seize", "vybrano")
net.arc("linka", "seize")

# doba obsluhy podle režimu (rozhoduje se při zahájení obsluhy)
net.immediate("normal", (7.5, 1.4), p=0, label="běžně", label_pos="above")
net.place("obsl_n", (9, 1.4))
net.timed("exp7", (10.5, 1.4), "exp(7 min)", param_pos="above")
net.immediate("rychle", (7.5, -1.4), p=1, label="rychle", label_pos="below right",
              param_pos="above")
net.place("obsl_r", (9, -1.4))
net.timed("exp3", (10.5, -1.4), "exp(3 min)")
net.arc("vybrano", "normal")
net.arc("vybrano", "rychle")
net.chain("normal", "obsl_n", "exp7")
net.chain("rychle", "obsl_r", "exp3")

# uvolnění linky a odchod
net.place("hotovo", (12, 0), label="hotovo", label_pos="above right")
net.arc("exp7", "hotovo")
net.arc("exp3", "hotovo")
net.immediate("release", (13.5, 0), label="uvolnění", label_pos="below")
net.arc("hotovo", "release")
net.arc("release", "linka", via=[(13.5, 3.0), (4.5, 3.0)])
net.place("konec", (15, 0))
net.immediate("odchod", (16.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("release", "konec", "odchod")

# režimy centra
net.place("normalni", (0.75, -1.8), tokens=1, label="běžný režim", label_pos="below")
net.immediate("zrychleni", (2.25, -1.8), label="zrychlení", label_pos="above left")
net.place("rychly", (3.75, -3.4), label="zrychlený režim", label_pos="below")
net.chain("normalni", "zrychleni", "rychly")
net.loop("fronta", "zrychleni", bend=15, w=5)
net.loop("rychly", "rychle", bend=8)

# návrat do běžného režimu: linka volná a nikdo ve frontě (obsazení má p=1)
net.immediate("obnoveni", (3.75, 2.6), p=0, horizontal=True, label="obnovení",
              label_pos="above", param_pos="below left")
net.arc("rychly", "obnoveni")
net.loop("linka", "obnoveni", bend=15)
net.arc("obnoveni", "normalni", via=[(-0.9, 2.6), (-0.9, -1.8)])

net.invariant({"linka": 1, "vybrano": 1, "obsl_n": 1, "obsl_r": 1, "hotovo": 1}, 1)
net.invariant({"normalni": 1, "rychly": 1}, 1)
