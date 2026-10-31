from pn import Net

net = Net("12–05", "Spalovna se třemi vozy (půlsemestrálky 2014–19, Z20)")

# 3 svozové vozy: každý má vlastní odpočet exp(1 h) (slajd 138); příjezd = vyložení balíku
net.place("vozy", (0, 0), tokens=3, label="Vozy na trase", label_pos="left")
net.timed("prijezd", (1.5, 0), "exp(1 h)", param_pos="above")
net.arc("vozy", "prijezd")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prijezd", "fronta")
net.place("vylozeno", (1.5, -1.8), label="vyloženo", label_pos="right")
net.arc("prijezd", "vylozeno")
net.immediate("odjezd", (0, -1.8), label="odjezd", label_pos="left", param_pos="left")
net.arc("vylozeno", "odjezd")
net.arc("odjezd", "vozy")

# spalovací komora s kapacitou 5 balíků, každý hoří exp(2 h)
net.place("volne", (4.5, -1.7), tokens=5, label="Volná místa komory", label_pos="above right")
net.immediate("vlozeni", (4.5, 0), p=2, param_pos="above")
net.place("komora", (6, 0), label="v komoře", label_pos="above")
net.timed("spalovani", (7.5, 0), "exp(2 h)", param_pos="above")
net.chain("fronta", "vlozeni", "komora", "spalovani")
net.arc("volne", "vlozeni")
net.arc("spalovani", "volne", via=[(7.5, -1.7)])
net.place("spaleno", (9, 0), label="spáleno", label_pos="above")
net.immediate("odchod", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("spalovani", "spaleno", "odchod")

# režim: normální / výjimečný
net.place("normalni", (0, -3.6), tokens=1, label="Normální stav", label_pos="left")
net.loop("normalni", "odjezd", bend=25)
net.immediate("prepnuti", (3, -3.6), p=1, horizontal=True, label="přepnutí", label_pos="below left",
              param_pos="above right")
net.arc("normalni", "prepnuti")
net.loop("fronta", "prepnuti", bend=12)
net.place("vyjimecny", (4.5, -3.6), label="Výjimečný stav", label_pos="below")
net.arc("prepnuti", "vyjimecny")
net.immediate("odvolani", (6, -3.6), horizontal=True, label="odvolání", label_pos="below")
net.arc("vyjimecny", "odvolani")
net.arc("volne", "odvolani", w=5, bend=18, w_pos="left")
net.arc("odvolani", "volne", w=5, bend=18, w_pos="left")
net.arc("odvolani", "normalni", via=[(7.2, -3.6), (7.2, -5), (0, -5)])

net.invariant({"vozy": 1, "vylozeno": 1}, 3)
net.invariant({"volne": 1, "komora": 1}, 5)
net.invariant({"normalni": 1, "vyjimecny": 1}, 1)
net.bound("fronta", 3)
