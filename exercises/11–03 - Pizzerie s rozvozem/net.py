from pn import Net

net = Net("11–03", "Pizzerie s rozvozem (půlsemestrálka 2022/23, varianta C)")

# objednávky: 3 pracovníci, vyřízení exp(10 min)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("volani", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "volani")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("prac", (4.5, 1.7), tokens=3, label="Pracovníci")
net.immediate("obsaz", (4.5, 0))
net.place("vyrizuje", (6, 0))
net.timed("vyrizeni", (7.5, 0), "exp(10 min)", param_pos="below right")
net.chain("volani", "fronta", "obsaz", "vyrizuje", "vyrizeni")
net.arc("prac", "obsaz")
net.arc("vyrizeni", "prac", bend=-25)

# objednávka opouští systém, hotová pizza čeká na rozvoz
net.place("vyrizeno", (7.5, -1.7), label="vyřízeno", label_pos="left")
net.immediate("odchod", (7.5, -3.3), horizontal=True, exit=True, label="odchod", label_pos="below")
net.chain("vyrizeni", "vyrizeno", "odchod")
net.place("hotove", (9.4, 0), label="Hotové", label_pos="above")
net.arc("vyrizeni", "hotove")

# rozvozník: A) aspoň 10 hotových
net.place("rozvoznik", (10.9, 1.7), tokens=1, label="Rozvozník", label_pos="above left")
net.immediate("deset", (10.9, 0), label="A", label_pos="below")
net.arc("hotove", "deset", w=10, w_pos="above")
net.arc("rozvoznik", "deset")
net.place("naklada", (12.4, 0), label="nakládá", label_pos="above right")
net.arc("deset", "naklada")

# B) čeká už 15 min a je hotová aspoň jedna
net.timed("cekani", (10.9, 3.3), "15 min", horizontal=True, param_pos="above")
net.arc("rozvoznik", "cekani")
net.place("cekal", (12.4, 3.3), label="čekal 15 min", label_pos="above")
net.arc("cekani", "cekal")
net.immediate("po15", (12.4, 1.7), horizontal=True, label="B", label_pos="right")
net.arc("cekal", "po15")
net.arc("hotove", "po15")
net.arc("po15", "naklada")

# naloží všechny hotové (p=1), pak vyráží
net.immediate("dober", (12.4, -1.7), p=1, horizontal=True, label="dobere hotové",
              label_pos="below", param_pos="right")
net.arc("hotove", "dober", via=[(9.4, -1.7)])
net.arc("naklada", "dober", bend=-30)
net.arc("dober", "naklada", bend=-30)
net.immediate("vyrazi", (14.2, 0), label="vyráží", label_pos="below")
net.place("na_ceste", (15.7, 0), label="na cestě", label_pos="below")
net.timed("rozvoz", (17.2, 0), "30–50 min", param_pos="below")
net.chain("naklada", "vyrazi", "na_ceste", "rozvoz")
net.arc("rozvoz", "rozvoznik", via=[(17.2, 4.8), (9.4, 4.8), (9.4, 1.7)])

net.invariant({"prac": 1, "vyrizuje": 1}, 3)
net.invariant({"rozvoznik": 1, "cekal": 1, "naklada": 1, "na_ceste": 1}, 1)
