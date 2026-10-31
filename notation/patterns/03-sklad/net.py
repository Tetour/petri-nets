from pn import Net

net = Net("P03", "Sklad (Store) s kapacitou N a obsazení více jednotek najednou")
net.closed = True
net.simulate = False
# sklad mezi oběma řádky; každá hrana má vlastní stranu skladu
net.place("store", (1.5, -1.5), tokens=3, label="Sklad (kapacita 3)", label_pos="below left")
net.place("q", (0, 0), tokens=2, label="Fronta", label_pos="above")
net.immediate("enter", (1.5, 0), label="Enter", label_pos="above")
net.place("s", (3, 0))
net.timed("obsl", (4.5, 0), "exp(10)")
net.place("o", (6, 0))
net.chain("q", "enter", "s", "obsl", "o")
net.arc("store", "enter")
# návrat z horního řádku obchází frontu a vchází do skladu zleva
net.arc("obsl", "store", via=[(4.5, 1.1), (-0.8, 1.1), (-0.8, -1.5)])
# transakce, která potřebuje 2 jednotky naráz
net.place("q2", (0, -3), tokens=1, label="Fronta 2", label_pos="below")
net.immediate("enter2", (1.5, -3), label="Enter(2)", label_pos="below")
net.place("s2", (3, -3))
net.timed("obsl2", (4.5, -3), "exp(20)")
net.place("o2", (6, -3))
net.chain("q2", "enter2", "s2", "obsl2", "o2")
net.arc("store", "enter2", w=2, w_pos="right=2pt")
net.arc("obsl2", "store", w=2, via=[(4.5, -1.5)], w_pos="right")
