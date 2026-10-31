from pn import Net

net = Net("11–11", "Výletní loď na jezeře (půlsemestrálky 2014–19, Z1)")

# cestující: po provozní době hned odchází (p=1), jinak do fronty na molu
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("prichozi", (3, 0))
net.immediate("do_fronty", (4.5, 0))
net.place("fronta", (6, 0), label="Fronta", label_pos="above left")
net.chain("prichod", "prichozi", "do_fronty", "fronta")
net.immediate("pozde", (3, -1.6), p=1, horizontal=True, label="pozdě", label_pos="above right",
              param_pos="below right")
net.arc("prichozi", "pozde")

# provozní doba 10 h (jeden den); konec provozu nastaví dva příznaky
net.place("provoz", (-1.5, -3.0), tokens=1, label="provozní doba", label_pos="below")
net.timed("t10", (0, -3.0), "10 h", param_pos="above")
net.place("po_provozu", (1.5, -1.6), label="po provozní době", label_pos="above left")
net.chain("provoz", "t10", "po_provozu")
net.loop("po_provozu", "pozde", bend=20)

# nástup po jednom (loď u mola = zařízení), exp(30 s)
net.place("lod", (7.5, 1.8), tokens=1, label="Loď u mola", label_pos="below left")
net.immediate("zacatek", (7.5, 0))
net.place("nastupuje", (9, 0))
net.timed("nastup", (10.5, 0), "exp(30 s)", param_pos="below")
net.place("paluba", (12, 0), label="Na palubě", label_pos="below")
net.chain("fronta", "zacatek", "nastupuje", "nastup", "paluba")
net.arc("lod", "zacatek")
net.arc("nastup", "lod", bend=-25)

# odjezd: (1) loď je plná (p=1), (2) 2 min od posledního nástupu a někdo je na palubě
net.timed("cekani", (12.75, 2.2), "2 min", param_pos="above left")
net.arc("lod", "cekani")
net.loop("paluba", "cekani", bend=20)
net.immediate("plna", (14.25, 2.2), p=1, label="plná", label_pos="right", param_pos="below right")
net.arc("lod", "plna", via=[(7.5, 3.4), (14.25, 3.4)])
net.loop("paluba", "plna", bend=12, w=50)
net.place("plavba", (13.5, 4.4), label="Plavba", label_pos="above")
net.arc("plna", "plavba")
net.arc("cekani", "plavba")
net.timed("vylet", (15.75, 4.4), "1 h", param_pos="above")
net.place("navrat", (17.25, 2.2), label="návrat k molu", label_pos="above left")
net.chain("plavba", "vylet", "navrat")

# po návratu všichni vystoupí (p=2); pak k molu, nebo po provozní době do depa (p=1)
net.immediate("vystoupeni", (15.75, 0), p=2, label="vystoupení", label_pos="above left",
              param_pos="below left")
net.arc("paluba", "vystoupeni")
net.loop("navrat", "vystoupeni", bend=15)
net.place("vystoupili", (15.75, -1.5), label="vystoupili", label_pos="left")
net.immediate("odchod", (17.25, -1.5), exit=True, label="odchod", label_pos="right")
net.chain("vystoupeni", "vystoupili", "odchod")
net.immediate("k_molu", (18.75, 3.4), label="k molu", label_pos="right")
net.arc("navrat", "k_molu")
net.arc("k_molu", "lod", via=[(18.75, 5.4), (6.6, 5.4), (6.6, 1.8)])
net.immediate("do_depa", (18.75, 1.0), p=1, label="do depa", label_pos="left",
              param_pos="below left")
net.arc("navrat", "do_depa")
net.place("po_provozu_lod", (20.25, 1.0), label="po provozní době", label_pos="above")
net.arc("t10", "po_provozu_lod", via=[(0, -4.6), (20.25, -4.6)])
net.loop("po_provozu_lod", "do_depa", bend=25)

# loď v depu: cestující, kteří zůstali na molu, odcházejí
net.place("depo", (7.5, -1.6), label="Depo", label_pos="right")
net.arc("do_depa", "depo", via=[(18.75, -2.8), (7.5, -2.8)])
net.immediate("rozchod", (6, -1.6), label="rozchod", label_pos="left")
net.arc("fronta", "rozchod")
net.loop("depo", "rozchod", bend=25)
net.place("odmitnuti", (4.5, -3.0), label="odchází", label_pos="left")
net.immediate("odchod_molo", (4.5, -4.2), horizontal=True, exit=True, label="odchod",
              label_pos="right")
net.arc("pozde", "odmitnuti")
net.arc("rozchod", "odmitnuti")
net.arc("odmitnuti", "odchod_molo")

net.invariant({"lod": 1, "nastupuje": 1, "plavba": 1, "navrat": 1, "depo": 1}, 1,
              name="loď je u mola, nabírá, pluje, nebo v depu")
net.invariant({"provoz": 1, "po_provozu": 1}, 1)
net.invariant({"po_provozu": 1, "po_provozu_lod": -1}, 0)
net.bound("paluba", 50)
# S příchody exp(5 min) se loď za jeden den nenaplní (na jízdu nastoupí typicky
# 10–20 cestujících), takže „plná“ se v simulaci neprovede. Větev je ověřená
# zvlášť se zrychlenými příchody (viz poznámka).
net.may_not_fire = {"plna"}
