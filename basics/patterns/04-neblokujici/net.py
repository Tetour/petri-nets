from pn import Net

net = Net("Podmínka pomocí priority: neblokující obsazení (if–else)")
net.closed = True
net.simulate = False
net.place("t", (0, 0), tokens=1, label="transakce", label_pos="above")
net.place("f", (1.5, 1.7), tokens=1, label="Linka", label_pos="above")
net.immediate("seize", (1.5, 0), p=1, param_pos="below right")
net.place("s", (3, 0), label="obsluha", label_pos="above")
net.arc("t", "seize")
net.arc("f", "seize")
net.arc("seize", "s")
net.immediate("jinak", (1.5, -1.8), label="jinak (p=0): odchází", label_pos="right")
net.arc("t", "jinak", via=[(0, -1.8)])
