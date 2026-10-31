from pn import Net

net = Net("12–05", "Spalovna se třemi vozy (půlsemestrálky 2014–19, Z20)")

# 3 svozové vozy: každý má vlastní odpočet exp(1 h) (slajd 138); příjezd = vyložení balíku
net.place("vozy", (0, 0), tokens=3, label="Vozy na trase", label_pos="left")
net.timed("prijezd", (1.5, 0), "exp(1 h)", param_pos="above")
net.arc("vozy", "prijezd")
net.place("fronta", (3.5, 0), label="Fronta", label_pos="above")
net.arc("prijezd", "fronta")
# vůz po vyložení: dolů do „vyloženo“ a přes odjezd zpět na trasu
net.place("vylozeno", (1.5, -1.6), label="vyloženo", label_pos="below")
net.arc("prijezd", "vylozeno")
net.immediate("odjezd", (0, -1.6), label="odjezd", label_pos="left")
net.arc("vylozeno", "odjezd")
net.arc("odjezd", "vozy")

# spalovací komora s kapacitou 5 balíků (volná místa pod řadou), každý hoří exp(2 h)
net.place("volne", (7, -1.6), tokens=5, label="Volná místa", label_pos="above left")
net.immediate("vlozeni", (7, 0), p=2, param_pos="above")
net.place("komora", (8.5, 0), label="v komoře", label_pos="above")
net.timed("spalovani", (10, 0), "exp(2 h)", param_pos="above")
net.chain("fronta", "vlozeni", "komora", "spalovani")
net.arc("volne", "vlozeni")
net.arc("spalovani", "volne", out=270, into=0)  # návrat místa: oblouk ze spodní strany přechodu
net.place("spaleno", (11.5, 0), label="spáleno", label_pos="above")
net.immediate("odchod", (13, 0), exit=True, label="odchod", label_pos="above")
net.chain("spalovani", "spaleno", "odchod")

# režim: normální / výjimečný (pod řadou)
net.place("normalni", (0, -3.2), tokens=1, label="Normální stav", label_pos="left")
net.loop("normalni", "odjezd")
net.immediate("prepnuti", (3.5, -1.6), p=1, label="přepnutí", label_pos="below right",
              param_pos="left")
net.arc("normalni", "prepnuti", via=[(3.5, -3.2)])
net.loop("fronta", "prepnuti")
net.place("vyjimecny", (5.5, -3.2), label="Výjimečný stav", label_pos="below")
net.arc("prepnuti", "vyjimecny", via=[(5.5, -1.6)])
net.immediate("odvolani", (7, -3.2), label="odvolání", label_pos="right")
net.arc("vyjimecny", "odvolani")
net.loop("volne", "odvolani", w=5)
net.arc("odvolani", "normalni", via=[(7, -4.6), (0, -4.6)])

net.invariant({"vozy": 1, "vylozeno": 1}, 3)
net.invariant({"volne": 1, "komora": 1}, 5)
net.invariant({"normalni": 1, "vyjimecny": 1}, 1)
net.bound("fronta", 3)
