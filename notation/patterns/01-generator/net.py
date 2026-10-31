from pn import Net

net = Net("P01", "Generátor transakcí a odchod ze systému")
net.closed = True
net.simulate = False
# a) místo se značkou ve smyčce (doporučené), b) zkrácený tvar bez místa
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(10)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="a)", label_pos="above")
net.arc("prichod", "fronta")
net.timed("prichod2", (1.5, -2), "exp(10)")
net.place("fronta2", (3, -2), label="b)", label_pos="above")
net.arc("prichod2", "fronta2")
# odchod: okamžitý přechod bez výstupu
net.place("konec", (5.5, -1), label="c)", label_pos="above")
net.immediate("odchod", (7, -1), exit=True, label="odchod")
net.arc("konec", "odchod")
