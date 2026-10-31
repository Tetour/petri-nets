from pn import Net

net = Net("P06", "Netrpělivost (timeout) ve frontě")
net.closed = True
net.simulate = False
net.place("q", (0, 0), tokens=2, label="Fronta", label_pos="above left")
net.place("f", (1.5, 1.7), tokens=0, label="Linka", label_pos="above")
net.immediate("seize", (1.5, 0))
net.place("s", (3, 0), tokens=1)
net.timed("obsl", (4.5, 0), "exp(10)")
net.place("o", (6, 0), label="konec", label_pos="above")
net.chain("q", "seize", "s", "obsl", "o")
net.arc("f", "seize")
net.arc("obsl", "f", via=[(4.5, 1.7)])
net.timed("timeout", (1.5, -1.6), "10", label="netrpělivost", param_pos="above",
          label_pos="below")
net.arc("q", "timeout", via=[(0, -1.6)])
net.arc("timeout", "o", via=[(6, -1.6)])
