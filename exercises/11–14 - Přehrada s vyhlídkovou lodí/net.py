from pn import Net

net = Net("11–14", "Přehrada s vyhlídkovou lodí (půlsemestrálka, rok neznámý)")

# příchody návštěvníků a nástup po jednom (loď v přístavu = zařízení pro nástup)
net.place("gen", (0, 0), tokens=1, label="příchody návštěvníků", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(1 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta v přístavu", label_pos="below")
net.place("lod", (4.5, 1.7), tokens=1, label="loď v přístavu", label_pos="below left")
net.immediate("zacatek", (4.5, 0))
net.place("nastupuje", (6, 0))
net.timed("nastup", (7.5, 0), "exp(10 s)", param_pos="below")
net.place("paluba", (9.5, 0), label="na palubě", label_pos="below")
net.chain("prichod", "fronta", "zacatek", "nastupuje", "nastup", "paluba")
net.arc("lod", "zacatek")
net.arc("nastup", "lod", out=90, into=0)

# s odjezdem odplouvají všichni na palubě (smyčka p=2)
net.immediate("odplouvaji", (11, 0), p=2, label="odplouvají", label_pos="below right",
              param_pos="above right")
net.place("konec", (13.5, 0), label="konec", label_pos="below")
net.immediate("odchod", (15, 0), exit=True, label="odchod", label_pos="below")
net.chain("paluba", "odplouvaji", "konec", "odchod")

# kotvení: odjezd po 100. návštěvníkovi (p=1), nebo po 15 min
net.place("kotvi", (9.5, 3.2), tokens=1, label="kotví", label_pos="left")
net.immediate("plna", (9.5, 1.7), p=1, label="plná", label_pos="left", param_pos="below left")
net.loop("paluba", "plna", w=100, bend=20)
net.arc("kotvi", "plna")
net.timed("limit", (11, 3.2), "15 min", param_pos="right")
net.arc("kotvi", "limit")
net.place("odjizdi", (11, 1.7), label="odjíždí", label_pos="below right")
net.arc("plna", "odjizdi")
net.arc("limit", "odjizdi")
net.loop("odjizdi", "odplouvaji", bend=20)

# vyplutí (p=1) bere loď v přístavu, takže nastupující smí dokončit nástup
net.immediate("vypluti", (13, 1.7), p=1, label="vyplutí", label_pos="below",
              param_pos="above left")
net.arc("odjizdi", "vypluti")
net.arc("lod", "vypluti", via=[(3, 1.7), (3, 6.2), (15.5, 6.2), (15.5, 1.7)])
net.place("plavba", (13, 3.2), label="plavba", label_pos="right")
net.arc("vypluti", "plavba")
net.timed("navrat", (9.5, 4.8), "50–60 min",
          param_pos="above")
net.arc("plavba", "navrat", via=[(13, 4.8)])
net.arc("navrat", "lod", via=[(4.5, 4.8)])
net.arc("navrat", "kotvi")

net.invariant({"lod": 1, "nastupuje": 1, "plavba": 1}, 1)
net.invariant({"kotvi": 1, "odjizdi": 1, "plavba": 1}, 1)
net.bound("paluba", 100)
# plná loď je vzácná (za 15 min nastoupí nejvýš asi 90 lidí), potřebuje dlouhý běh
net.sim_events = 300000
