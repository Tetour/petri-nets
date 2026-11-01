from pn import Net

net = Net("Kritická sekce (poznámky MSI, P/T sítě, příklad 2)")
# Uzavřená P/T síť bez času: dva procesy obíhají dokola, nic nepřichází ani neodchází.
net.closed = True
# Všechny přechody jsou okamžité a tvoří cykly, takže v nulovém čase by se prováděly
# donekonečna (simulátor to hlásí jako livelock). Síť proto nesimulujeme; vzájemné
# vyloučení zaručuje P-invariant volná KS + A v KS + B v KS = 1.
net.simulate = False

# proces 1 v horní řadě (návrat nad ní), proces 2 v dolní řadě (návrat pod ní)
Y = 2.2
for proc, y, n, ks in (("A", Y, 1, "KS1"), ("B", -Y, 5, "KS2")):
    up = y > 0
    side, back = ("above", y + 1.6) if up else ("below", y - 1.6)
    net.place(f"{proc}1", (0, y), tokens=1, label=f"{proc}1", label_pos="left")
    net.immediate(f"t{n}", (1.5, y), label=f"t{n}", label_pos=side)
    net.place(f"{proc}_pred", (3, y), label=f"{proc} před KS", label_pos=side)
    net.immediate(f"t{n + 1}", (4.5, y), label=f"t{n + 1}", label_pos=side)
    net.place(f"{proc}_v", (6, y), label=ks, label_pos=side)
    net.immediate(f"t{n + 2}", (7.5, y), label=f"t{n + 2}", label_pos=side)
    net.place(f"{proc}2", (9, y), label=f"{proc}2", label_pos=side)
    net.immediate(f"t{n + 3}", (10.5, y), label=f"t{n + 3}", label_pos="right")
    net.chain(f"{proc}1", f"t{n}", f"{proc}_pred", f"t{n + 1}", f"{proc}_v", f"t{n + 2}",
              f"{proc}2", f"t{n + 3}")
    net.arc(f"t{n + 3}", f"{proc}1", via=[(10.5, back), (0, back)])

# zámek kritické sekce mezi řadami; každá hrana má vlastní stranu místa
net.place("volna", (6, 0), tokens=1, label="volná KS", label_pos="below left")
net.arc("volna", "t2", via=[(4.5, 0)])                   # vlevo, nahoru do t2
net.arc("t3", "volna", via=[(7.5, 1.1), (6, 1.1)])       # shora
net.arc("volna", "t6", via=[(6, -1.1), (4.5, -1.1)])     # zespodu, dolů do t6
net.arc("t7", "volna", via=[(7.5, 0)])                   # zprava

net.invariant({"A1": 1, "A_pred": 1, "A_v": 1, "A2": 1}, 1)
net.invariant({"B1": 1, "B_pred": 1, "B_v": 1, "B2": 1}, 1)
net.invariant({"volna": 1, "A_v": 1, "B_v": 1}, 1, name="vzájemné vyloučení")
