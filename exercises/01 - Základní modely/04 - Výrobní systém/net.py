from pn import Net

net = Net("Výrobní systém (poznámky MSI, P/T sítě, příklad 1)")
# Zadání neuvádí časy; symboly A, S, V, K mají hodnoty jen pro simulaci.
net.params = {"A": 10, "S": 6, "V": 15, "K": 5}

# příchody a soustruh
net.place("gen", (0, 0), tokens=1, label="příchody výrobků", label_pos="below")
net.timed("prichod", (1.5, 0), "A", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta_S", (3, 0), label="fronta", label_pos="below")
net.place("soustruh", (4.5, 1.6), tokens=1, label="Soustruh", label_pos="above")
net.immediate("obsaz_S", (4.5, 0))
net.place("na_S", (6, 0))
net.timed("soustruzeni", (7.5, 0), "S", param_pos="below")
net.chain("prichod", "fronta_S", "obsaz_S", "na_S", "soustruzeni")
net.arc("soustruh", "obsaz_S")
net.arc("soustruzeni", "soustruh", out=90, into=0)

# dvě stejné vrtačky = sklad se dvěma značkami (store s kapacitou 2)
net.place("fronta_V", (9, 0), label="fronta", label_pos="below")
net.arc("soustruzeni", "fronta_V")
net.place("vrtacky", (10.5, 1.6), tokens=2, label="Vrtačky", label_pos="above")
net.immediate("obsaz_V", (10.5, 0))
net.place("na_V", (12, 0))
net.timed("vrtani", (13.5, 0), "V", param_pos="below")
net.chain("fronta_V", "obsaz_V", "na_V", "vrtani")
net.arc("vrtacky", "obsaz_V")
net.arc("vrtani", "vrtacky", out=90, into=0)

# kontrola, pak dobrý výrobek nebo zmetek
net.place("fronta_K", (15, 0), label="fronta", label_pos="below")
net.arc("vrtani", "fronta_K")
net.place("kontrola", (16.5, 1.6), tokens=1, label="Kontrola", label_pos="above")
net.immediate("obsaz_K", (16.5, 0))
net.place("na_K", (18, 0))
net.timed("kontrolovani", (19.5, 0), "K", param_pos="below")
net.chain("fronta_K", "obsaz_K", "na_K", "kontrolovani")
net.arc("kontrola", "obsaz_K")
net.arc("kontrolovani", "kontrola", out=90, into=0)
net.place("zkontrolovano", (21, 0))
net.arc("kontrolovani", "zkontrolovano")
net.immediate("dobry", (22.5, 0), exit=True, label="dobrý výrobek", label_pos="above")
net.immediate("zmetek", (22.5, -1.6), exit=True, label="zmetek", label_pos="below")
net.arc("zkontrolovano", "dobry")
net.arc("zkontrolovano", "zmetek", via=[(21, -1.6)], corner=20)

net.invariant({"soustruh": 1, "na_S": 1}, 1)
net.invariant({"vrtacky": 1, "na_V": 1}, 2)
net.invariant({"kontrola": 1, "na_K": 1}, 1)
