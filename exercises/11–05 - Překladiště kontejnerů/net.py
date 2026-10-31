from pn import Net

net = Net("11–05", "Překladiště kontejnerů (půlsemestrálka 2021/22, varianta A)")

# příchody aut, jeřáb (transakce = auto)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(20 min)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta aut")
net.place("jerab", (4.5, -1.8), tokens=1, label="Jeřáb", label_pos="below")
net.immediate("obsaz_jerab", (4.5, 0))
net.place("auto", (6, 0), label="auto", label_pos="below left")
net.chain("prichod", "fronta", "obsaz_jerab", "auto")
net.arc("jerab", "obsaz_jerab")
net.place("kontejnery", (6, 1.8), label="kontejnery v autě", label_pos="above")
net.arc("obsaz_jerab", "kontejnery", w=3, w_pos="above left")

# cyklus vykládky: dokud má auto kontejner (p=1), jinak uvolnění jeřábu
net.immediate("dalsi", (7.5, 0), p=1, label="další kontejner", label_pos="below",
              param_pos="above right")
net.arc("auto", "dalsi")
net.arc("kontejnery", "dalsi")
net.place("ceka", (9.3, 0), label="čeká na vlak", label_pos="above")
net.immediate("obsaz_vlak", (10.8, 0))
net.place("vykladka", (12.3, 0), label="vykládka", label_pos="below")
net.timed("vylozeni", (13.8, 0), "exp(8 min)", param_pos="below right")
net.chain("dalsi", "ceka", "obsaz_vlak", "vykladka", "vylozeni")
net.place("vlak", (12.3, 1.8), tokens=1, label="Vlak (u rampy)", label_pos="left")
net.arc("vlak", "obsaz_vlak")
net.arc("vylozeni", "vlak")
net.arc("vylozeni", "auto", via=[(13.8, -1.3), (6.6, -1.3)])

net.immediate("uvolneni", (6, -1.8), label="uvolnění", label_pos="right")
net.arc("auto", "uvolneni")
net.arc("uvolneni", "jerab")
net.place("prazdne", (6, -3.4), label="prázdné auto", label_pos="left")
net.immediate("odjezd_auta", (7.5, -3.4), exit=True, label="odjezd auta", label_pos="right")
net.chain("uvolneni", "prazdne", "odjezd_auta")

# chování vlaku
net.place("nalozeno", (15.3, 0), label="Naloženo", label_pos="above")
net.arc("vylozeni", "nalozeno")
net.immediate("odjezd_vlaku", (17, 0), p=1, label="odjezd vlaku", label_pos="below",
              param_pos="above left")
net.arc("nalozeno", "odjezd_vlaku", w=20, w_pos="below")
net.arc("vlak", "odjezd_vlaku", via=[(17, 1.8)])
net.place("cesta", (18.7, 0), label="vlak na cestě", label_pos="above")
net.timed("navrat", (20.4, 0), "1 h", param_pos="below")
net.chain("odjezd_vlaku", "cesta", "navrat")
net.arc("navrat", "vlak", via=[(20.4, 3.2), (12.3, 3.2)])

net.invariant({"jerab": 1, "auto": 1, "ceka": 1, "vykladka": 1}, 1)
net.invariant({"vlak": 1, "vykladka": 1, "cesta": 1}, 1)
net.bound("kontejnery", 3)
net.bound("nalozeno", 20)
# 3 × exp(8 min) = 24 min vykládky na auto > 20 min mezi auty: fronta aut roste bez omezení
# (přetížení je dané zadáním, ne chybou modelu)
net.unbounded_ok = {"fronta"}
