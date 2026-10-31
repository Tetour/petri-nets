from pn import Net

net = Net("11–14", "Přehrada s vyhlídkovou lodí (půlsemestrálka, rok neznámý)")

# příchody návštěvníků a nástup po jednom (loď v přístavu = zařízení pro nástup)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta v přístavu", label_pos="above")
net.place("lod", (4.5, 1.6), tokens=1, label="Loď v přístavu", label_pos="left")
net.immediate("zacatek", (4.5, 0))
net.place("nastupuje", (6, 0))
net.timed("nastup", (7.5, 0), "exp(10 s)", param_pos="below left")
net.chain("prichod", "fronta", "zacatek", "nastupuje", "nastup")
net.arc("lod", "zacatek")
net.arc("nastup", "lod", via=[(7.5, 1.6)])
net.place("paluba", (9.5, 0), label="Na palubě", label_pos="below left")
net.arc("nastup", "paluba")

# kotvení: odjezd po 100. návštěvníkovi (p=1), nebo po 15 min
net.place("kotvi", (11, -1.6), tokens=1, label="Kotví", label_pos="left")
net.immediate("plna", (11, 0), p=1, label="plná", label_pos="above",
              param_pos="below right")
net.loop("paluba", "plna", w=100, bend=30)
net.arc("kotvi", "plna")
net.timed("limit", (12.5, -1.6), "15 min", param_pos="below")
net.arc("kotvi", "limit")
net.place("odjizdi", (12.5, 0), label="Odjíždí", label_pos="above right")
net.arc("plna", "odjizdi")
net.arc("limit", "odjizdi")

# s odjezdem odplouvají všichni na palubě (smyčka p=2), pak vyplutí (p=1)
net.immediate("odplouvaji", (11, 1.6), p=2, horizontal=True, label="cestující odplouvají",
              label_pos="above left", param_pos="right")
net.arc("paluba", "odplouvaji")
net.loop("odjizdi", "odplouvaji", bend=20)
net.place("konec", (11, 3.0), label="konec", label_pos="left")
net.arc("odplouvaji", "konec")
net.immediate("odchod", (12.5, 3.0), exit=True, label="odchod", label_pos="right")
net.arc("konec", "odchod")

net.immediate("vypluti", (14, 0), p=1, label="vyplutí", label_pos="below",
              param_pos="below left")
net.arc("odjizdi", "vypluti")
net.arc("lod", "vypluti", via=[(5.4, 3.8), (14.9, 3.8), (14.9, 0.9)])
net.place("plavba", (15.5, 0), label="Plavba", label_pos="below")
net.timed("navrat", (17, 0), "50–60 min", label="návrat", label_pos="above",
          param_pos="below right")
net.chain("vypluti", "plavba", "navrat")
net.arc("navrat", "lod", via=[(17, 4.4), (4.5, 4.4)])
net.arc("navrat", "kotvi", via=[(17, -2.6), (11, -2.6)])

net.invariant({"lod": 1, "nastupuje": 1, "plavba": 1}, 1)
net.invariant({"kotvi": 1, "odjizdi": 1, "plavba": 1}, 1)
net.bound("paluba", 100)
# plná loď je vzácná (za 15 min nastoupí nejvýš asi 90 lidí), potřebuje dlouhý běh
net.sim_events = 300000
