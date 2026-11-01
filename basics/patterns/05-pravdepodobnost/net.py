from pn import Net

net = Net("Pravděpodobnostní větvení")
net.closed = True
net.simulate = False
net.place("t", (0, 0), tokens=1, label="transakce", label_pos="left")
net.immediate("a", (1.5, 1), prob=30)
net.immediate("b", (1.5, -1), prob=70, param_pos="below")
net.place("pa", (3, 1), label="akce 1", label_pos="right")
net.place("pb", (3, -1), label="akce 2", label_pos="right")
net.arc("t", "a", via=[(0, 1)])
net.arc("t", "b", via=[(0, -1)])
net.arc("a", "pa")
net.arc("b", "pb")
