from pn import Net

net = Net("Výrobní hala (půlsemestrálky 2014–19, Z24)")

# příchody požadavků a montovna
net.place("gen", (0, 0), tokens=1, label="příchody požadavků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(30 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("montovna", (4.5, 1.6), tokens=1, label="Montovna", label_pos="above right")
net.immediate("obsaz_m", (4.5, 0))
net.place("montuje", (6, 0))
net.timed("montaz", (7.5, 0), "10–15 min")
net.chain("prichod", "fronta", "obsaz_m", "montuje", "montaz")
net.arc("montovna", "obsaz_m")
net.arc("montaz", "montovna", out=90, into=0)  # návrat montovny: oblouk z horní strany přechodu

# lakovna
net.place("fronta_l", (9, 0), label="fronta lakovny", label_pos="below right")
net.place("lakovna", (14, 1.6), tokens=1, label="Lakovna", label_pos="below left")
net.immediate("obsaz_l", (14, 0), p=1, param_pos="below")
net.place("lakuje", (15.5, 0))
net.timed("lakovani", (17, 0), "15–20 min")
net.chain("montaz", "fronta_l", "obsaz_l", "lakuje", "lakovani")
net.arc("lakovna", "obsaz_l")
net.arc("lakovani", "lakovna", out=90, into=0)
net.place("hotovo", (18.5, 0), label="hotovo", label_pos="above")
net.immediate("odchod", (20, 0), exit=True, label="odchod", label_pos="above")
net.chain("lakovani", "hotovo", "odchod")

# odstavení nad frontou lakovny: fronta ≥ 3 (test hranami s váhou 3), volná montovna → Odstaveno
net.immediate("odstav", (9, 1.6), p=1, label="odstavení", label_pos="above left", param_pos="left")
net.loop("fronta_l", "odstav", w=3)
net.arc("montovna", "odstav", via=[(4.5, 3.2), (9, 3.2)])
net.place("odstaveno", (12, 1.6), label="Odstaveno", label_pos="above left")
net.arc("odstav", "odstaveno")

# vyhození pod frontou lakovny: fronta ≥ 3 a rozpracovaná montáž → požadavek zpět do fronty,
# značka montovny rovnou do Odstaveno
net.immediate("vyhozeni", (9, -1.6), label="vyhození montáže", label_pos="below right")
net.loop("fronta_l", "vyhozeni", w=3)
net.arc("montuje", "vyhozeni", via=[(6, -1.6)])
net.arc("vyhozeni", "fronta", via=[(9, -3), (3, -3)])
net.arc("vyhozeni", "odstaveno", via=[(12, -1.6)])

# obnovení: lakovna volná a fronta lakovny prázdná (p=0 < obsazení lakovny p=1)
net.immediate("obnoveni", (14, 3.2), label="obnovení", label_pos="right")
net.arc("odstaveno", "obnoveni", via=[(12, 3.2)])
net.loop("lakovna", "obnoveni")
net.arc("obnoveni", "montovna", via=[(14, 4.6), (3, 4.6), (3, 1.6)])

net.invariant({"montovna": 1, "montuje": 1, "odstaveno": 1}, 1)
net.invariant({"lakovna": 1, "lakuje": 1}, 1)
net.bound("fronta_l", 3)
# vyhození montáže se v této síti neprovede: fronta lakovny roste jen dokončením montáže,
# takže montovna je v okamžiku dosažení 3 vždy volná a odstavení (p=1) ji zabere dřív,
# než ji obsadí další požadavek (viz poznámka).
net.may_not_fire = {"vyhozeni"}
