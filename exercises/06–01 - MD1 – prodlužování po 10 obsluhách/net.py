from pn import Net

net = Net("06–01", "M/D/1, obsluha 3 a po každých 10 obsluhách o 3 delší (obsluha = k fází po 3)")
net.params = {"A": 10}

net.place("gen", (0, 0), tokens=1, label="příchody transakcí", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="above")
net.place("linka", (4.5, 1.7), tokens=1, label="Linka", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="v obsluze", label_pos="above right")
net.chain("prichod", "fronta", "obsaz", "obsluha")
net.arc("linka", "obsaz")

# smyčka fází v řadě obsluhy: další fáze (p=1) bere značku z úrovně, po 3 vrací transakci
net.immediate("faze", (9, 0), p=1, label="další fáze", label_pos="above", param_pos="below left")
net.place("ve_fazi", (10.75, 0))
net.timed("faze_t", (12.5, 0), "3", param_pos="right")
net.chain("obsluha", "faze", "ve_fazi", "faze_t")
net.arc("faze_t", "obsluha", via=[(12.5, 1.4), (6, 1.4)])

# úroveň (počet fází) a odsloužené fáze pod řadou obsluhy
net.place("uroven", (9, -1.6), tokens=1, label="úroveň", label_pos="below")
net.arc("uroven", "faze")
net.place("pouzito", (12.5, -1.6), label="odsloužené fáze", label_pos="below right")
net.arc("faze_t", "pouzito")
net.immediate("vraceni", (10.5, -1.6), p=1, label="vrácení", label_pos="above right",
              param_pos="above left")
net.arc("pouzito", "vraceni")
net.arc("vraceni", "uroven")

# fáze došly (p=0): transakce odchází spodní řadou; nejdřív se vrátí odsloužené fáze, pak linka
net.immediate("dosly", (7.6, -4.8), label="fáze došly", label_pos="below")
net.arc("obsluha", "dosly", via=[(6, -4.8)], corner=20)
net.place("hotovo", (10.5, -4.8), label="hotovo", label_pos="below")
net.arc("dosly", "hotovo")
net.arc("hotovo", "vraceni", bend=20)
net.arc("vraceni", "hotovo", bend=20)
net.immediate("uvolneni", (14, -4.8), label="uvolnění", label_pos="below")
net.arc("hotovo", "uvolneni")
net.arc("uvolneni", "linka", via=[(14, 2.7), (4.5, 2.7)])

# čítač obsluh: po každých 10 skončených obsluhách přibude jedna fáze
net.place("citac", (7.6, -3.2), label="čítač", label_pos="right")
net.arc("dosly", "citac")
net.immediate("navyseni", (7.6, -1.6), p=1, label="+3 č. j.", label_pos="left",
              param_pos="above")
net.arc("citac", "navyseni", w=10, w_pos="right")
net.arc("navyseni", "uroven")

net.place("konec", (15.5, -4.8), label="konec", label_pos="below")
net.immediate("odchod", (17, -4.8), exit=True, label="odchod")
net.chain("uvolneni", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1, "ve_fazi": 1, "hotovo": 1}, 1)
net.bound("citac", 9)
# doba obsluhy roste bez omezení, takže fronta nakonec vždy neomezeně roste
net.unbounded_ok = {"fronta"}
