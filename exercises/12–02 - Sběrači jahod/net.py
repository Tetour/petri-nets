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
net.arc("zabaleni", "linka", out=90, into=0)  # návrat linky: oblouk z horní strany přechodu
net.place("zabaleno", (9, 0), label="zabaleno", label_pos="above")
net.immediate("odvoz", (10.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("zabaleni", "zabaleno", "odvoz")

# siréna pod frontou: test fronty ≥ 10, odvolá všech 5 sběračů (zruší jejich rozpracovaný sběr)
net.immediate("sirena", (3, -1.8), p=1, label="siréna", label_pos="below", param_pos="below right")
net.loop("fronta", "sirena", w=10)
net.arc("sberaci", "sirena", w=5, via=[(0, -1.8)], w_pos="left")
net.place("pauza", (4.5, -1.8), label="pauza", label_pos="below")
net.timed("konec_pauzy", (6, -1.8), "60 min", param_pos="above")
net.chain("sirena", "pauza", "konec_pauzy")
# po pauze se všech 5 vrací oklikou zdola do Sběračů
net.arc("konec_pauzy", "sberaci", w=5, via=[(6, -3.2), (-1.2, -3.2), (-1.2, 0)], w_pos="right")

net.invariant({"linka": 1, "baleni": 1}, 1)
net.invariant({"sberaci": 1, "pauza": 5}, 5)
net.bound("fronta", 10)
