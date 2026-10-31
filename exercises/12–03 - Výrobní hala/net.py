from pn import Net

net = Net("12–03", "Výrobní hala (půlsemestrálky 2014–19, Z24)")

# příchody požadavků a montovna
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(30 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above left")
net.place("montovna", (4.5, 1.7), tokens=1, label="Montovna", label_pos="left")
net.immediate("obsaz_m", (4.5, 0))
net.place("montuje", (6, 0))
net.timed("montaz", (7.5, 0), "10–15 min")
net.chain("prichod", "fronta", "obsaz_m", "montuje", "montaz")
net.arc("montovna", "obsaz_m")
net.arc("montaz", "montovna", bend=-25)

# lakovna
net.place("fronta_l", (9.5, 0), label="Fronta lakovny", label_pos="below right")
net.place("lakovna", (12.5, 1.7), tokens=1, label="Lakovna", label_pos="left")
net.immediate("obsaz_l", (12.5, 0), p=1, param_pos="above right")
net.place("lakuje", (14, 0))
net.timed("lakovani", (15.5, 0), "15–20 min")
net.chain("montaz", "fronta_l", "obsaz_l", "lakuje", "lakovani")
net.arc("lakovna", "obsaz_l")
net.arc("lakovani", "lakovna", bend=-25)
net.place("hotovo", (17, 0), label="hotovo", label_pos="above")
net.immediate("odchod", (18.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("lakovani", "hotovo", "odchod")

# odstavení: fronta lakovny ≥ 3 (test hranami s váhou 3 tam i zpět)
net.immediate("odstav", (6, 3.4), p=1, horizontal=True, label="odstavení", label_pos="above",
              param_pos="left")
net.arc("montovna", "odstav")
net.arc("fronta_l", "odstav", w=3, bend=12, w_pos="left")
net.arc("odstav", "fronta_l", w=3, bend=12, w_pos="left")
net.place("odstaveno", (9.25, 3.4), label="Odstaveno", label_pos="above")
net.arc("odstav", "odstaveno")

# rozpracovaná montáž se vyhodí: požadavek zpět do fronty, montovna se uvolní
# (a odstavení ji vzápětí zabere, fronta lakovny má pořád ≥ 3)
net.immediate("vyhozeni", (7.5, -2.0), horizontal=True, label="vyhození montáže",
              label_pos="below", param_pos="right")
net.arc("montuje", "vyhozeni")
net.arc("fronta_l", "vyhozeni", w=3, bend=-15, w_pos="right")
net.arc("vyhozeni", "fronta_l", w=3, bend=-15, w_pos="right")
net.arc("vyhozeni", "fronta", via=[(3, -2.0)])
net.arc("vyhozeni", "montovna", via=[(3.75, -1.2), (3.75, 1.1)])

# obnovení: lakovna volná a fronta lakovny prázdná (p=0 < obsazení lakovny p=1)
net.immediate("obnoveni", (12.5, 3.4), horizontal=True, label="obnovení", label_pos="above",
              param_pos="right")
net.arc("odstaveno", "obnoveni")
net.loop("lakovna", "obnoveni", bend=20)
net.arc("obnoveni", "montovna", via=[(12.5, 4.6), (4.5, 4.6)])

net.invariant({"montovna": 1, "montuje": 1, "odstaveno": 1}, 1)
net.invariant({"lakovna": 1, "lakuje": 1}, 1)
net.bound("fronta_l", 3)
# vyhození montáže se v této síti neprovede: fronta lakovny roste jen dokončením montáže,
# takže montovna je v okamžiku dosažení 3 vždy volná a odstavení (p=1) ji zabere dřív,
# než ji obsadí další požadavek (viz poznámka).
net.may_not_fire = {"vyhozeni"}
