from pn import Net

net = Net("11–05", "Překladiště kontejnerů (půlsemestrálka 2021/22, varianta A)")

# příjezdy aut, jeřáb (transakce = auto)
net.place("gen", (0, 0), tokens=1, label="příjezdy aut", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(20 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta aut", label_pos="below")
net.place("jerab", (4.5, -1.8), tokens=1, label="jeřáb", label_pos="left")
net.immediate("obsaz_jerab", (4.5, 0))
net.place("auto", (6, 0), label="auto", label_pos="below right")
net.chain("prichod", "fronta", "obsaz_jerab", "auto")
net.arc("jerab", "obsaz_jerab")
net.place("kontejnery", (4.5, 1.8), label="kontejnery v autě", label_pos="left")
net.arc("obsaz_jerab", "kontejnery", w=3, w_pos="left")

# cyklus vykládky: dokud má auto kontejner (p=1), jinak uvolnění jeřábu
net.immediate("dalsi", (6, 1.8), p=1, label="další kontejner", label_pos="above",
              param_pos="below right")
net.arc("auto", "dalsi")
net.arc("kontejnery", "dalsi")
net.place("ceka", (7.5, 1.8), label="čeká na vlak", label_pos="below")
net.immediate("obsaz_vlak", (9, 1.8))
net.place("vykladka", (10.5, 1.8), label="vykládka", label_pos="below")
net.timed("vylozeni", (12, 1.8), "exp(8 min)", param_pos="below right")
net.chain("dalsi", "ceka", "obsaz_vlak", "vykladka", "vylozeni")
net.place("vlak", (9, 3.6), tokens=1, label="vlak u rampy", label_pos="below left")
net.arc("vlak", "obsaz_vlak")
net.arc("vylozeni", "vlak", out=90, into=0)
net.arc("vylozeni", "auto", via=[(12, 0)])

# vyložené auto uvolní jeřáb a odjíždí
net.immediate("uvolneni", (6, -1.8), label="uvolnění", label_pos="right")
net.arc("auto", "uvolneni")
net.arc("uvolneni", "jerab")
net.place("prazdne", (6, -3.6), label="prázdné auto", label_pos="left")
net.immediate("odjezd_auta", (7.5, -3.6), exit=True, label="odjezd auta", label_pos="right")
net.chain("uvolneni", "prazdne", "odjezd_auta")

# chování vlaku: po 20 kontejnerech odjíždí (p=1), za hodinu se vrací prázdný
net.place("nalozeno", (14, 1.8), label="naloženo", label_pos="above")
net.arc("vylozeni", "nalozeno")
net.immediate("odjezd_vlaku", (15.75, 1.8), p=1, label="odjezd vlaku", label_pos="below",
              param_pos="above right")
net.arc("nalozeno", "odjezd_vlaku", w=20, w_pos="below")
net.arc("vlak", "odjezd_vlaku", via=[(9, 5.4), (15.75, 5.4)])
net.place("cesta", (17.5, 1.8), label="vlak na cestě", label_pos="above")
net.timed("navrat", (19.25, 1.8), "1 h", param_pos="below")
net.chain("odjezd_vlaku", "cesta", "navrat")
net.arc("navrat", "vlak", via=[(19.25, 7), (8.25, 7), (8.25, 3.6)])

net.invariant({"jerab": 1, "auto": 1, "ceka": 1, "vykladka": 1}, 1)
net.invariant({"vlak": 1, "vykladka": 1, "cesta": 1}, 1)
net.bound("kontejnery", 3)
net.bound("nalozeno", 20)
# 3 × exp(8 min) = 24 min vykládky na auto > 20 min mezi auty: fronta aut roste bez omezení
# (přetížení je dané zadáním, ne chybou modelu)
net.unbounded_ok = {"fronta"}
