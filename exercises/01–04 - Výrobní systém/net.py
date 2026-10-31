from pn import Net

net = Net("01–04", "Výrobní systém (poznámky MSI, P/T sítě, příklad 1)")
# P/T síť bez času: všechny přechody kromě generátoru jsou okamžité (jen událost, bez trvání).
# Generátor musí být časovaný, jinak by zdroj výrobků vyráběl nekonečně mnoho v nulovém čase.
# Interval T zadání neuvádí; hodnota je jen pro simulaci.
net.params = {"T": 10}

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("novy_mat", (1.5, 0), "T", label="nový materiál", label_pos="above", param_pos="below")
net.loop("gen", "novy_mat")
net.place("P1", (3, 0), label="P1", label_pos="below")

# soustruh: start, soustružení, stop
net.place("P3", (4.5, 1.6), tokens=1, label="P3 soustruh volný", label_pos="above")
net.immediate("soustr_start", (4.5, 0), label="start", label_pos="below")
net.place("P2", (6, 0), label="P2", label_pos="below")
net.immediate("soustr_stop", (7.5, 0), label="stop", label_pos="below")
net.place("P4", (9, 0), label="P4", label_pos="below left")
net.chain("novy_mat", "P1", "soustr_start", "P2", "soustr_stop", "P4")
net.arc("P3", "soustr_start")
net.arc("soustr_stop", "P3", bend=-25)

# dvě vrtačky
net.place("P9", (15.5, 0), label="P9", label_pos="below right")
for n, y in ((1, 1.6), (2, -1.6)):
    up = y > 0
    free = f"P{6 if n == 1 else 8}"
    busy = f"P{5 if n == 1 else 7}"
    net.place(free, (12, y + (1.6 if up else -1.6)), tokens=1,
              label=f"{free} vrtačka {n} volná", label_pos="above" if up else "below")
    net.immediate(f"vrt{n}_start", (10.5, y), label="start", label_pos="above" if up else "below")
    net.place(busy, (12, y), label=busy, label_pos="below" if up else "above")
    net.immediate(f"vrt{n}_stop", (13.5, y), label="stop", label_pos="above" if up else "below")
    net.chain("P4", f"vrt{n}_start", busy, f"vrt{n}_stop", "P9")
    net.arc(free, f"vrt{n}_start")
    net.arc(f"vrt{n}_stop", free)

# kontrola: start, pak úspěch nebo neúspěch
net.place("P11", (17.5, 1.6), tokens=1, label="P11 kontrola volná", label_pos="above left")
net.immediate("kontr_start", (17.5, 0), label="start", label_pos="below")
net.place("P10", (19, 0), label="P10", label_pos="below left")
net.chain("P9", "kontr_start", "P10")
net.arc("P11", "kontr_start")
net.immediate("kontr_uspech", (20.5, 0), label="úspěch", label_pos="below")
net.immediate("kontr_neuspech", (20.5, -1.8), label="neúspěch", label_pos="left")
net.place("P12", (22, 0), label="P12", label_pos="below")
net.place("P13", (22, -1.8), label="P13", label_pos="below")
net.immediate("vyrobek", (23.5, 0), exit=True, label="dobrý výrobek", label_pos="above")
net.immediate("zmetek", (23.5, -1.8), exit=True, label="zmetek", label_pos="below")
net.chain("P10", "kontr_uspech", "P12", "vyrobek")
net.chain("P10", "kontr_neuspech", "P13", "zmetek")
net.arc("kontr_uspech", "P11", bend=-25)
net.arc("kontr_neuspech", "P11", via=[(20.5, -3.1), (25, -3.1), (25, 2.6), (18.2, 2.6)])

net.invariant({"P3": 1, "P2": 1}, 1)
net.invariant({"P6": 1, "P5": 1}, 1)
net.invariant({"P8": 1, "P7": 1}, 1)
net.invariant({"P11": 1, "P10": 1}, 1)
