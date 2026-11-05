from pn import Net

net = Net("Centrum M/M/1 s rychlým režimem (půlsemestrálka 2024/25, varianta D)")

# hlavní řada: příchody a obsazení linky
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above left")
net.place("linka", (4.5, 1.8), tokens=1, label="Linka", label_pos="above right")
net.immediate("seize", (4.5, 0), p=1, param_pos="below right")
net.place("vybrano", (6.5, 0))
net.chain("prichod", "fronta", "seize", "vybrano")
net.arc("linka", "seize")

# doba obsluhy podle režimu (rozhoduje se při zahájení obsluhy): běžně nahoru, rychle dolů
net.immediate("normal", (8, 1.5), p=0, label="běžně", label_pos="above", param_pos="below")
net.place("obsl_n", (9.5, 1.5))
net.timed("exp7", (11, 1.5), "exp(7 min)", param_pos="below")
net.immediate("rychle", (8, -1.5), p=1, label="rychle", label_pos="above left", param_pos="above right")
net.place("obsl_r", (9.5, -1.5))
net.timed("exp3", (11, -1.5), "exp(3 min)", param_pos="above")
net.arc("vybrano", "normal", via=[(6.5, 1.5)])
net.arc("vybrano", "rychle", via=[(6.5, -1.5)])
net.chain("normal", "obsl_n", "exp7")
net.chain("rychle", "obsl_r", "exp3")

# uvolnění linky a odchod
net.place("hotovo", (12.5, 0), label="hotovo", label_pos="left")
net.arc("exp7", "hotovo", via=[(12.5, 1.5)])
net.arc("exp3", "hotovo", via=[(12.5, -1.5)])
net.immediate("release", (14, 0), label="uvolnění", label_pos="below")
net.arc("hotovo", "release")
net.arc("release", "linka", via=[(14, 3.0), (4.5, 3.0)])
net.place("konec", (15.5, 0))
net.immediate("odchod", (17, 0), exit=True, label="odchod", label_pos="above")
net.chain("release", "konec", "odchod")

# režimy centra (pod hlavní řadou)
net.place("normalni", (1.5, -1.8), tokens=1, label="běžný režim", label_pos="below")
net.immediate("zrychleni", (3, -1.8), label="zrychlení", label_pos="right")
net.place("rychly", (8, -3.2), label="zrychlený režim", label_pos="below")
net.arc("normalni", "zrychleni")
net.arc("zrychleni", "rychly", via=[(3, -3.2)])
net.loop("fronta", "zrychleni", bend=25, w=5)
net.loop("rychly", "rychle", bend=25)

# návrat do běžného režimu: linka volná a nikdo ve frontě (obsazení má p=1);
# obnovení je u linky, hrany z/do režimů obchází síť zprava a zleva
net.immediate("obnoveni", (3, 1.8), p=0, label="obnovení", label_pos="below",
              param_pos="above left")
net.loop("obnoveni", "linka", bend=25)
net.arc("rychly", "obnoveni", via=[(18, -3.2), (18, 4.2), (3, 4.2)])
net.arc("obnoveni", "normalni", via=[(-1.8, 1.8), (-1.8, -1.8)])

net.invariant({"linka": 1, "vybrano": 1, "obsl_n": 1, "obsl_r": 1, "hotovo": 1}, 1)
net.invariant({"normalni": 1, "rychly": 1}, 1)
