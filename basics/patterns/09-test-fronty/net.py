from pn import Net

net = Net("Test délky fronty: alespoň k transakcí (k = 5)")
net.closed = True
net.simulate = False
net.place("q", (0, 0), tokens=5, label="Fronta", label_pos="below")
net.place("rezim", (1.6, 1.6), tokens=1, label="režim normální", label_pos="above")
net.immediate("prepni", (1.6, 0), p=1, param_pos="below")
net.place("novy", (3.2, 0), label="režim zrychlený", label_pos="above")
net.arc("q", "prepni", w=5, bend=25, w_pos="above")
net.arc("prepni", "q", w=5, bend=25, w_pos="below")
net.arc("rezim", "prepni")
net.arc("prepni", "novy")
