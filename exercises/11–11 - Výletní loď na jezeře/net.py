from pn import Net

net = Net("11–11", "Výletní loď na jezeře (půlsemestrálky 2014–19, Z1)")

# cestující: po provozní době hned odchází (p=1), jinak do fronty na molu
net.place("gen", (0, 0), tokens=1, label="příchody cestujících", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("prichozi", (3, 0))
net.immediate("do_fronty", (4.5, 0))
net.place("fronta", (6, 0), label="fronta", label_pos="above left")
net.chain("prichod", "prichozi", "do_fronty", "fronta")
net.immediate("pozde", (3, -1.5), p=1, label="pozdě", label_pos="below right",
              param_pos="above right")
net.arc("prichozi", "pozde")

# provozní doba 10 h (jeden den); konec provozu nastaví dva příznaky
net.place("po_provozu", (1.5, -1.5), label="po provozní době", label_pos="left")
net.loop("po_provozu", "pozde", bend=20)
net.place("provoz", (0, -3.0), tokens=1, label="provozní doba", label_pos="below")
net.timed("t10", (1.5, -3.0), "10 h", param_pos="right")
net.chain("provoz", "t10", "po_provozu")

# nástup po jednom: loď u mola je prázdná (dole), nebo už někdo nastoupil (nahoře)
net.place("lod0", (7.5, -1.5), tokens=1, label="loď u mola (prázdná)", label_pos="right")
net.place("lod1", (7.5, 3.0), label="loď u mola (s cestujícími)", label_pos="above right")
net.immediate("zac0", (7.5, 0))
net.immediate("zac1", (7.5, 1.5))
net.arc("fronta", "zac0")
net.arc("fronta", "zac1", via=[(6, 1.5)])
net.arc("lod0", "zac0")
net.arc("lod1", "zac1")
net.place("nastupuje", (9, 0))
net.arc("zac0", "nastupuje")
net.arc("zac1", "nastupuje", via=[(9, 1.5)])
net.timed("nastup", (10.5, 0), "exp(30 s)", param_pos="below")
net.place("paluba", (12, 0), label="na palubě", label_pos="below")
net.chain("nastupuje", "nastup", "paluba")
net.arc("nastup", "lod1", out=90, into=0)

# odjezd: (1) loď je plná (p=1, test 50 na palubě), (2) 2 min od posledního nástupu
net.timed("cekani", (6, 3.0), "2 min", param_pos="left")
net.arc("lod1", "cekani")
net.immediate("plna", (12, 1.6), p=1, label="plná", label_pos="above left",
              param_pos="left")
net.arc("lod1", "plna", via=[(7.5, 4.4), (12, 4.4)])
net.loop("paluba", "plna", bend=20, w=50)
net.place("plavba", (13.5, 1.6), label="plavba", label_pos="below")
net.arc("plna", "plavba")
net.arc("cekani", "plavba", via=[(6, 5.6), (13.5, 5.6)])
net.timed("vylet", (15, 1.6), "1 h", param_pos="below")
net.place("navrat", (16.8, 1.6), label="návrat", label_pos="above left")
net.chain("plavba", "vylet", "navrat")

# po návratu všichni vystoupí (p=2); pak k molu, nebo po provozní době do depa (p=1)
net.immediate("vystoupeni", (16.8, 0), p=2, label="vystoupení", label_pos="below",
              param_pos="above left")
net.arc("paluba", "vystoupeni")
net.loop("navrat", "vystoupeni", bend=20)
net.place("vystoupili", (18.3, 0), label="vystoupili", label_pos="above")
net.immediate("odchod", (19.8, 0), exit=True, label="odchod", label_pos="below")
net.chain("vystoupeni", "vystoupili", "odchod")
net.immediate("k_molu", (18.3, 1.6), label="k molu", label_pos="above")
net.arc("navrat", "k_molu")
net.arc("k_molu", "lod0", via=[(21, 1.6), (21, -3.0), (7.5, -3.0)])
net.immediate("do_depa", (16.8, 3.0), p=1, label="do depa", label_pos="left",
              param_pos="below right")
net.arc("navrat", "do_depa")
net.place("po_provozu_lod", (16.8, 4.4), label="po provozní době", label_pos="left")
net.loop("po_provozu_lod", "do_depa", bend=20)
net.arc("t10", "po_provozu_lod", via=[(1.5, -5.5), (23, -5.5), (23, 4.4)])

# loď v depu: cestující, kteří zůstali na molu, odcházejí
net.place("depo", (6, -3.0), label="depo", label_pos="left")
net.arc("do_depa", "depo", via=[(22, 3.0), (22, -4.5), (6, -4.5)])
net.immediate("rozchod", (6, -1.5), label="rozchod", label_pos="above right")
net.arc("fronta", "rozchod")
net.loop("depo", "rozchod", bend=20)
net.place("odmitnuti", (4.5, -1.5), label="odchází", label_pos="above")
net.immediate("odchod_molo", (4.5, -3.0), exit=True, label="odchod", label_pos="below")
net.arc("pozde", "odmitnuti")
net.arc("rozchod", "odmitnuti")
net.arc("odmitnuti", "odchod_molo")

net.invariant({"lod0": 1, "lod1": 1, "nastupuje": 1, "plavba": 1, "navrat": 1, "depo": 1}, 1,
              name="loď je u mola, nabírá, pluje, nebo v depu")
net.invariant({"provoz": 1, "po_provozu": 1}, 1)
net.invariant({"po_provozu": 1, "po_provozu_lod": -1}, 0)
net.bound("paluba", 50)
# S příchody exp(5 min) se loď za jeden den nenaplní (na jízdu nastoupí typicky
# 10–20 cestujících), takže „plná“ se v simulaci neprovede. Větev je ověřená
# zvlášť se zrychlenými příchody (viz poznámka).
net.may_not_fire = {"plna"}
