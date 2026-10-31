from pn import Net

net = Net("P10", "Dočasné zastavení příchodů (odebrání značky generátoru)")
net.closed = True
net.simulate = False
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(10)")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="above")
net.arc("prichod", "fronta")
net.place("signal", (-1.6, -1.8), tokens=1, label="podnět", label_pos="below")
net.immediate("stop", (0, -1.8), horizontal=True, label="zastav", label_pos="below")
net.arc("signal", "stop")
net.arc("gen", "stop")
net.place("pauza", (1.6, -1.8))
net.timed("p10", (3.2, -1.8), "10", horizontal=True, param_pos="right")
net.chain("stop", "pauza", "p10")
net.arc("p10", "gen", via=[(3.2, -0.9), (0.6, -0.9)])
