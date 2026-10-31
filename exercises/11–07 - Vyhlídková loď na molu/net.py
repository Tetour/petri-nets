from pn import Net

net = Net("11–07", "Vyhlídková loď na molu (půlsemestrálky 2014–19, Z18)")

# příchody; každý čekající po 30 min odchází (vlastní odpočet pro každou značku)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")
net.timed("netrpelivost", (3, -1.75), "30 min", horizontal=True, param_pos="below")
net.arc("fronta", "netrpelivost")
net.place("odesel", (1.5, -1.75))
net.immediate("odchod_f", (0, -1.75), exit=True, label="odchod", label_pos="below")
net.chain("netrpelivost", "odesel", "odchod_f")

# nástup po jednom: loď u mola je prázdná, nebo už někdo nastoupil
net.place("lod0", (4.5, 2.4), tokens=1, label="Loď u mola (prázdná)", label_pos="above")
net.place("lod1", (4.5, -2.4), label="Loď u mola (s cestujícími)", label_pos="below left")
net.immediate("zac0", (4.5, 0.9))
net.immediate("zac1", (4.5, -0.9))
net.place("nastupuje", (6, 0))
net.timed("nastup", (7.5, 0), "1 min", param_pos="above")
net.place("paluba", (9, 0), label="Na palubě", label_pos="above")
net.arc("fronta", "zac0")
net.arc("fronta", "zac1")
net.arc("lod0", "zac0")
net.arc("lod1", "zac1")
net.arc("zac0", "nastupuje")
net.arc("zac1", "nastupuje")
net.chain("nastupuje", "nastup", "paluba")
net.arc("nastup", "lod1")

# vyplutí: 20 na palubě (p=1, před dalším nástupem), nebo 3 min bez dalšího nástupu
net.immediate("plna", (9, -1.8), p=1, horizontal=True, label="plná loď", label_pos="right",
              param_pos="below right")
net.loop("paluba", "plna", bend=20, w=20)
net.arc("lod1", "plna")
net.timed("cekani", (6, -3.6), "3 min", param_pos="below")
net.arc("lod1", "cekani")
net.place("plavba", (9, -3.6), label="Plavba", label_pos="below")
net.arc("plna", "plavba")
net.arc("cekani", "plavba")
net.timed("t_plavba", (10.5, -3.6), "1 h", param_pos="below")
net.place("navrat", (12, -3.6), label="návrat", label_pos="below")
net.chain("plavba", "t_plavba", "navrat")

# po návratu vystoupí všichni (smyčka p=1), pak je loď opět prázdná u mola
net.immediate("vystup", (12, -1.8), p=1, horizontal=True, label="výstup", label_pos="right",
              param_pos="below right")
net.loop("navrat", "vystup", bend=20)
net.arc("paluba", "vystup")
net.place("konec", (12, 0), label="konec", label_pos="above")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod", label_pos="above")
net.arc("vystup", "konec")
net.arc("konec", "odchod")
net.immediate("pristavena", (13.5, -3.6), label="přistavení", label_pos="below")
net.arc("navrat", "pristavena")
net.arc("pristavena", "lod0", via=[(14.7, -3.6), (14.7, 2.4)])

net.invariant({"lod0": 1, "lod1": 1, "nastupuje": 1, "plavba": 1, "navrat": 1}, 1)
net.bound("paluba", 20)
