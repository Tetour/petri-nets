from pn import Net

net = Net("Dočasné zastavení příchodů (odebrání značky generátoru)")
net.closed = True
net.simulate = False
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="left")
net.timed("prichod", (1.5, 0), "exp(10)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")
# generátor zůstává vlevo: zastavení bere jeho značku zespodu, návrat ji vrací shora
net.immediate("stop", (0, -1.8), label="zastav", label_pos="left")
net.place("signal", (0, -3.3), tokens=1, label="podnět", label_pos="below")
net.arc("gen", "stop")
net.arc("signal", "stop")
net.place("pauza", (1.5, -1.8))
net.timed("p10", (3, -1.8), "10")
net.chain("stop", "pauza", "p10")
net.arc("p10", "gen", via=[(4.2, -1.8), (4.2, 1.1), (0, 1.1)])
