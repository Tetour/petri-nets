from pn import Net

net = Net("01–01", "Opravářská dílna (přednáška, slajdy 157–164)")

net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(20 min)")
net.loop("gen", "prichod")
net.place("zakazka", (3, 0), label="zakázka", label_pos="right")
net.arc("prichod", "zakazka")

# horní řada náročné zakázky (opravář nad ní), dolní řada normální (opravář pod ní)
for row, y, prob, name, time in (("N", 1.7, 33.3, "Náročné", "exp(45 min)"),
                                 ("B", -1.7, 66.7, "Normální", "exp(15 min)")):
    up = y > 0
    net.immediate(f"vyber_{row}", (4.5, y), prob=prob, param_pos="above" if up else "below")
    net.arc("zakazka", f"vyber_{row}", via=[(3, y)])
    net.place(f"fronta_{row}", (6, y), label="fronta", label_pos="below" if up else "above")
    net.place(f"opravar_{row}", (7.5, y + (1.6 if up else -1.6)), tokens=1,
              label=name, label_pos="above" if up else "below")
    net.immediate(f"obsaz_{row}", (7.5, y))
    net.place(f"oprava_{row}", (9, y))
    net.timed(f"opr_{row}", (10.5, y), time, param_pos="below" if up else "above")
    net.chain(f"vyber_{row}", f"fronta_{row}", f"obsaz_{row}", f"oprava_{row}", f"opr_{row}")
    net.arc(f"opravar_{row}", f"obsaz_{row}")
    # návrat opraváře: oblouk z horní (u dolní řady ze spodní) strany přechodu
    net.arc(f"opr_{row}", f"opravar_{row}", out=90 if up else 270, into=0)

net.place("konec", (12, 0), label="hotovo", label_pos="left")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.arc("opr_N", "konec", via=[(12, 1.7)])
net.arc("opr_B", "konec", via=[(12, -1.7)])
net.arc("konec", "odchod")

net.invariant({"opravar_N": 1, "oprava_N": 1}, 1)
net.invariant({"opravar_B": 1, "oprava_B": 1}, 1)
