from pn import Net

net = Net("01–05", "Kritická sekce (poznámky MSI, P/T sítě, příklad 2)")
# Uzavřená P/T síť bez času: dva procesy obíhají dokola, nic nepřichází ani neodchází.
net.closed = True
# Všechny přechody jsou okamžité a tvoří cykly, takže v nulovém čase by se prováděly
# donekonečna (simulátor to hlásí jako livelock). Síť proto nesimulujeme; vzájemné
# vyloučení zaručuje P-invariant volná KS + A v KS + B v KS = 1.
net.simulate = False

for proc, x, side, outer in (("A", 0, "left", -1.6), ("B", 5, "right", 6.6)):
    n = 1 if proc == "A" else 5
    other = "right" if side == "left" else "left"
    net.place(f"{proc}1", (x, 6), tokens=1, label=f"{proc}1", label_pos=other)
    net.immediate(f"t{n}", (x, 4.5), horizontal=True, label=f"t{n}", label_pos=other)
    net.place(f"{proc}_pred", (x, 3), label=f"{proc} před KS", label_pos=other)
    net.immediate(f"t{n + 1}", (x, 1.5), horizontal=True, label=f"t{n + 1}", label_pos=side)
    net.place(f"{proc}_v", (x, 0), label=f"KS{1 if proc == 'A' else 2}", label_pos=other)
    net.immediate(f"t{n + 2}", (x, -1.5), horizontal=True, label=f"t{n + 2}", label_pos=side)
    net.place(f"{proc}2", (x, -3), label=f"{proc}2", label_pos=other)
    net.immediate(f"t{n + 3}", (outer, 1.5), label=f"t{n + 3}", label_pos=side)
    net.chain(f"{proc}1", f"t{n}", f"{proc}_pred", f"t{n + 1}", f"{proc}_v", f"t{n + 2}", f"{proc}2")
    net.arc(f"{proc}2", f"t{n + 3}", via=[(outer, -3)])
    net.arc(f"t{n + 3}", f"{proc}1", via=[(outer, 6)])

net.place("volna", (2.5, 0), tokens=1, label="volná KS", label_pos="below")
net.arc("volna", "t2")
net.arc("t3", "volna")
net.arc("volna", "t6")
net.arc("t7", "volna")

net.invariant({"A1": 1, "A_pred": 1, "A_v": 1, "A2": 1}, 1)
net.invariant({"B1": 1, "B_pred": 1, "B_v": 1, "B2": 1}, 1)
net.invariant({"volna": 1, "A_v": 1, "B_v": 1}, 1, name="vzájemné vyloučení")
