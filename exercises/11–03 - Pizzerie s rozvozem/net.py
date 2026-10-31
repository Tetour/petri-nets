from pn import Net

net = Net("11–03", "Pizzerie s rozvozem (půlsemestrálka 2022/23, varianta C)")

# objednávky: 3 pracovníci, vyřízení exp(10 min)
net.place("gen", (0, 0), tokens=1, label="volání zákazníků", label_pos="below")
net.timed("volani", (1.5, 0), "exp(5 min)", param_pos="above")
net.loop("gen", "volani")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("prac", (4.5, 1.8), tokens=3, label="pracovníci", label_pos="above")
net.immediate("obsaz", (4.5, 0))
net.place("vyrizuje", (6, 0), label="vyřizuje", label_pos="below")
net.timed("vyrizeni", (7.5, 0), "exp(10 min)", param_pos="above right")
net.chain("volani", "fronta", "obsaz", "vyrizuje", "vyrizeni")
net.arc("prac", "obsaz")
net.arc("vyrizeni", "prac", out=90, into=0)

# objednávka opouští systém, hotová pizza čeká na rozvoz
net.place("vyrizeno", (7.5, -1.8), label="vyřízeno", label_pos="left")
net.immediate("odchod", (7.5, -3.6), exit=True, label="odchod", label_pos="left")
net.chain("vyrizeni", "vyrizeno", "odchod")
net.place("hotove", (10, 0), label="hotové", label_pos="below left")
net.arc("vyrizeni", "hotove")

# rozvozník: A) aspoň 10 hotových
net.place("rozvoznik", (11.5, 1.8), tokens=1, label="rozvozník", label_pos="left")
net.immediate("deset", (11.5, 0), label="A", label_pos="below")
net.arc("hotove", "deset", w=10, w_pos="above")
net.arc("rozvoznik", "deset")
net.place("naklada", (14.5, 0), label="nakládá", label_pos="above left")
net.arc("deset", "naklada")

# B) čeká už 15 min a je hotová aspoň jedna
net.timed("cekani", (13, 1.8), "15 min", param_pos="below")
net.arc("rozvoznik", "cekani")
net.place("cekal", (13, 3.6), label="čekal 15 min", label_pos="left")
net.arc("cekani", "cekal")
net.immediate("po15", (14.5, 3.6), label="B", label_pos="right")
net.arc("cekal", "po15")
net.arc("hotove", "po15", via=[(10, 5.4), (14.5, 5.4)])
net.arc("po15", "naklada")

# naloží všechny hotové (p=1), pak vyráží
net.immediate("dober", (14.5, -1.8), p=1, label="dobere hotové", label_pos="below",
              param_pos="right")
net.arc("hotove", "dober", via=[(10, -1.8)])
net.loop("naklada", "dober", bend=20)
net.immediate("vyrazi", (16, 0), label="vyráží", label_pos="below")
net.place("na_ceste", (17.5, 0), label="na cestě", label_pos="below")
net.timed("rozvoz", (19, 0), "30–50 min", param_pos="below")
net.chain("naklada", "vyrazi", "na_ceste", "rozvoz")
net.arc("rozvoz", "rozvoznik", via=[(19, 7), (11.5, 7)])

net.invariant({"prac": 1, "vyrizuje": 1}, 3)
net.invariant({"rozvoznik": 1, "cekal": 1, "naklada": 1, "na_ceste": 1}, 1)
