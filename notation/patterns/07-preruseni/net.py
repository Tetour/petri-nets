from pn import Net

net = Net("P07", "Přerušení probíhající obsluhy (porucha)")
net.closed = True
net.simulate = False
net.place("s", (0, 0), tokens=1, label="obsluha", label_pos="above")
net.timed("obsl", (1.5, 0), "exp(10)")
net.place("o", (3, 0), label="hotovo", label_pos="above")
net.chain("s", "obsl", "o")
net.place("porucha", (-1.5, -1.6), tokens=1, label="porucha", label_pos="above")
net.immediate("prer", (0, -1.6), p=1, label="přerušení", label_pos="below",
              param_pos="above right")
net.place("pr", (1.5, -1.6), label="přerušená transakce", label_pos="below right")
net.arc("s", "prer")
net.arc("porucha", "prer")
net.arc("prer", "pr")
net.immediate("zanik", (-1.5, -3.2), label="porucha bez účinku (p=0)",
              label_pos="right")
net.arc("porucha", "zanik")
