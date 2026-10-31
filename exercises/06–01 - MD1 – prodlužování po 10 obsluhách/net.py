from pn import Net

net = Net("06–01", "M/D/1, obsluha 3 a po každých 10 obsluhách o 3 delší (obsluha = k fází po 3)")
net.params = {"A": 10}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(A)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.place("linka", (4.5, 1.8), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("obsluha", (6, 0), label="v obsluze", label_pos="above")
net.chain("prichod", "fronta", "obsaz", "obsluha")
net.arc("linka", "obsaz")

# obsluha = tolik fází po 3, kolik je značek v místě úroveň
net.place("uroven", (3.9, -1.4), tokens=1, label="úroveň", label_pos="above left")
net.immediate("faze", (5.3, -1.4), p=1, param_pos="below left")
net.place("ve_fazi", (6, -2.7))
net.timed("faze_t", (6.7, -1.4), "3", param_pos="above right")
net.chain("obsluha", "faze", "ve_fazi", "faze_t", "obsluha")
net.arc("uroven", "faze")
net.place("pouzito", (8.1, -1.4), label="odsloužené fáze", label_pos="below")
net.arc("faze_t", "pouzito")

# fáze došly (p=0): vrátit odsloužené fáze do úrovně, pak uvolnit linku
net.immediate("dosly", (7.7, 0), label="fáze došly", label_pos="above")
net.place("hotovo", (9.4, 0), label="hotovo", label_pos="above")
net.chain("obsluha", "dosly", "hotovo")
net.immediate("vraceni", (9.4, -1.4), p=1, label="vrácení", label_pos="right",
              param_pos="below right")
net.loop("hotovo", "vraceni", bend=25)
net.arc("pouzito", "vraceni")
net.arc("vraceni", "uroven", via=[(9.4, -3.6), (3.9, -3.6)])
net.immediate("uvolneni", (11.5, 0), label="uvolnění", label_pos="above left")
net.arc("hotovo", "uvolneni")
net.arc("uvolneni", "linka", via=[(11.5, 1.8)])

# po každých 10 obsluhách přibude jedna fáze
net.place("citac", (11.5, -1.4), label="čítač", label_pos="right")
net.arc("uvolneni", "citac")
net.immediate("navyseni", (11.5, -2.7), p=1, horizontal=True, label="+3 č. j.",
              label_pos="right", param_pos="below right")
net.arc("citac", "navyseni", w=10, w_pos="right")
net.arc("navyseni", "uroven", via=[(11.5, -4.2), (3.0, -4.2), (3.0, -1.4)])

net.place("konec", (13, 0), label="konec", label_pos="above")
net.immediate("odchod", (14.5, 0), exit=True, label="odchod")
net.chain("uvolneni", "konec", "odchod")

net.invariant({"linka": 1, "obsluha": 1, "ve_fazi": 1, "hotovo": 1}, 1)
net.bound("citac", 9)
# doba obsluhy roste bez omezení, takže fronta nakonec vždy neomezeně roste
net.unbounded_ok = {"fronta"}
