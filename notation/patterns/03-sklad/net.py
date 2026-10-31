from pn import Net

net = Net("P03", "Sklad (Store) s kapacitou N a obsazení více jednotek najednou")
net.closed = True
net.simulate = False
net.place("q", (0, 0), tokens=2, label="Fronta", label_pos="below")
net.place("store", (1.5, 1.7), tokens=3, label="Sklad (kapacita 3)", label_pos="above")
net.immediate("enter", (1.5, 0), label="Enter", label_pos="below")
net.place("s", (3, 0))
net.timed("obsl", (4.5, 0), "exp(10)")
net.place("o", (6, 0))
net.chain("q", "enter", "s", "obsl", "o")
net.arc("store", "enter")
net.arc("obsl", "store", bend=-25)
# transakce, která potřebuje 2 jednotky naráz
net.place("q2", (0, -2.6), tokens=1, label="Fronta 2", label_pos="below")
net.immediate("enter2", (1.5, -2.6), label="Enter(2)", label_pos="below")
net.place("s2", (3, -2.6))
net.timed("obsl2", (4.5, -2.6), "exp(20)")
net.place("o2", (6, -2.6))
net.chain("q2", "enter2", "s2", "obsl2", "o2")
net.arc("store", "enter2", w=2, via=[(0.9, 0.9), (0.9, -1.6)], w_pos="left")
net.arc("obsl2", "store", w=2, via=[(4.5, -1.3), (2.6, -1.3)], w_pos="above")
