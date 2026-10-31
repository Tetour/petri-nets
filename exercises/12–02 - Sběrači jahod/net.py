from pn import Net

net = Net("12–02", "Sběrači jahod (půlsemestrálka 2021/22, varianta B)")

# 5 sběračů: každá značka má vlastní odpočet exp(20 min) (slajd 138)
net.place("sberaci", (0, 0), tokens=5, label="Sběrači", label_pos="above")
net.timed("sber", (1.5, 0), "exp(20 min)")
net.loop("sberaci", "sber")
net.place("fronta", (3, 0), label="Fronta beden", label_pos="above")
net.arc("sber", "fronta")

# balicí linka
net.place("linka", (4.5, 1.6), tokens=1, label="Linka")
net.immediate("obsaz", (4.5, 0))
net.place("baleni", (6, 0))
net.timed("zabaleni", (7.5, 0), "5–7 min")
net.chain("fronta", "obsaz", "baleni", "zabaleni")
net.arc("linka", "obsaz")
net.arc("zabaleni", "linka", bend=-25)
net.place("zabaleno", (9, 0), label="zabaleno", label_pos="above")
net.immediate("odvoz", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("zabaleni", "zabaleno", "odvoz")

# siréna: test fronty ≥ 10, odvolá všech 5 sběračů (zruší jejich rozpracovaný sběr)
net.immediate("sirena", (3, -2.2), p=1, horizontal=True, label="siréna", label_pos="right",
              param_pos="below right")
net.arc("fronta", "sirena", w=10, bend=25, w_pos="right")
net.arc("sirena", "fronta", w=10, bend=25, w_pos="left")
net.arc("sberaci", "sirena", w=5, via=[(0, -2.2)], w_pos="left")
net.place("pauza", (3, -3.8), label="pauza", label_pos="right")
net.timed("konec_pauzy", (1.2, -3.8), "60 min", param_pos="below")
net.chain("sirena", "pauza", "konec_pauzy")
net.arc("konec_pauzy", "sberaci", w=5, via=[(-1.2, -3.8), (-1.2, 0)], w_pos="above")

net.invariant({"linka": 1, "baleni": 1}, 1)
net.invariant({"sberaci": 1, "pauza": 5}, 5)
net.bound("fronta", 10)
