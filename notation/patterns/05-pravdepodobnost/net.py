from pn import Net

net = Net("P05", "Pravděpodobnostní větvení")
net.closed = True
net.simulate = False
net.place("t", (0, 0), tokens=1, label="transakce", label_pos="below")
net.immediate("a", (1.5, 1), prob=30)
net.immediate("b", (1.5, -1), prob=70, param_pos="below")
net.place("pa", (3, 1), label="akce 1", label_pos="right")
net.place("pb", (3, -1), label="akce 2", label_pos="right")
net.chain("t", "a", "pa")
net.chain("t", "b", "pb")
