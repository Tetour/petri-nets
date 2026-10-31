from pn import Net

net = Net("P02", "Zařízení (Facility): obsazení, obsluha, uvolnění")
net.closed = True
net.simulate = False
# a) jako na slajdu 154: Seize – obsluha – Release
net.place("q", (0, 0), tokens=1, label="Fronta", label_pos="below")
net.place("f", (1.5, 1.6), tokens=1, label="Linka", label_pos="above")
net.immediate("seize", (1.5, 0), label="Seize", label_pos="below")
net.place("s", (3, 0))
net.timed("obsl", (4.5, 0), "exp(10)")
net.place("r", (6, 0))
net.immediate("release", (7.5, 0), label="Release", label_pos="below")
net.place("o", (9, 0))
net.chain("q", "seize", "s", "obsl", "r", "release", "o")
net.arc("f", "seize")
net.arc("release", "f", via=[(7.5, 1.6)])
# b) zkrácený zápis: uvolnění sloučené s časovaným přechodem (slajd 164)
net.place("q2", (0, -3.8), tokens=1, label="Fronta", label_pos="below")
net.place("f2", (1.5, -2.2), tokens=1, label="Linka", label_pos="above")
net.immediate("seize2", (1.5, -3.8))
net.place("s2", (3, -3.8))
net.timed("obsl2", (4.5, -3.8), "exp(10)")
net.place("o2", (6, -3.8))
net.chain("q2", "seize2", "s2", "obsl2", "o2")
net.arc("f2", "seize2")
net.arc("obsl2", "f2", bend=-25)
