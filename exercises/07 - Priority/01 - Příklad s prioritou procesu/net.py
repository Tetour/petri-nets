from pn import Net

net = Net("Ambulance M/M/1: akutní pacienti mají vyšší prioritu procesu (předbíhají ve frontě)")

net.place("gen", (0, 0), tokens=1, label="příchody pacientů", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(15 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("novy", (3, 0), label="pacient", label_pos="right")
net.arc("prichod", "novy")

# horní řada akutní pacienti (20 %), dolní ostatní (80 %); lékař je mezi řadami
for row, y, prob, name in (("a", 1.7, 20, "fronta akutních"), ("o", -1.7, 80, "fronta ostatních")):
    up = y > 0
    net.immediate(f"vyber_{row}", (4.5, y), prob=prob, param_pos="above" if up else "below")
    net.arc("novy", f"vyber_{row}", via=[(3, y)])
    net.place(f"fronta_{row}", (6, y), label=name, label_pos="below" if up else "above")
    net.place(f"vys_{row}", (9, y))
    net.timed(f"konec_{row}", (10.5, y), "exp(10 min)", param_pos="above" if up else "below")
    net.chain(f"vyber_{row}", f"fronta_{row}")
    net.chain(f"obsaz_{row}", f"vys_{row}", f"konec_{row}")

# lékař: akutní pacient má přednost (p=1), probíhající vyšetření se nepřerušuje
net.place("lekar", (7.5, 0), tokens=1, label="lékař", label_pos="left")
net.immediate("obsaz_a", (7.5, 1.7), p=1, param_pos="above")
net.immediate("obsaz_o", (7.5, -1.7))
net.arc("fronta_a", "obsaz_a")
net.arc("fronta_o", "obsaz_o")
net.arc("lekar", "obsaz_a")
net.arc("lekar", "obsaz_o")
# návrat lékaře: oblouky ze spodní (horní) strany přechodů, každý do jiného místa pravé strany
net.arc("konec_a", "lekar", out=270, into=25)
net.arc("konec_o", "lekar", out=90, into=-25)

net.place("konec", (12, 0), label="vyšetřen", label_pos="left")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod")
net.arc("konec_a", "konec", via=[(12, 1.7)])
net.arc("konec_o", "konec", via=[(12, -1.7)])
net.arc("konec", "odchod")

net.invariant({"lekar": 1, "vys_a": 1, "vys_o": 1}, 1)
