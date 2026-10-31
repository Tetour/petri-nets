from pn import Net

net = Net("09–10", "Kopírovací centrum (půlsemestrálka 2022/23, varianta A)")

# příchody a registrace u přepážky
net.place("gen", (0, 0), tokens=1, label="příchody klientů", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(3 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("prepazka", (4.5, 1.6), tokens=1, label="Přepážka", label_pos="above")
net.immediate("reg_start", (4.5, 0))
net.place("registrace", (6, 0))
net.timed("reg", (7.5, 0), "1–2 min", param_pos="below")
net.chain("prichod", "fronta", "reg_start", "registrace", "reg")
net.arc("prepazka", "reg_start")
net.arc("reg", "prepazka", out=90, into=0)
net.place("rozdeleni", (9, 0), label="rozdělování", label_pos="right")
net.arc("reg", "rozdeleni")

# horní řada stroj A (70 %, stroj nad ní), dolní řada stroj B (30 %, stroj pod ní)
for row, y, prob in (("A", 2, 70), ("B", -2, 30)):
    up = y > 0
    net.immediate(f"na_{row}", (10.5, y), prob=prob, param_pos="above" if up else "below")
    net.arc("rozdeleni", f"na_{row}", via=[(9, y)], corner=20)
    net.place(f"fronta_{row}", (12, y), label=f"Fronta {row}", label_pos="above" if up else "below")
    net.place(f"stroj_{row}", (13.5, y + (1.6 if up else -1.6)), tokens=1,
              label=f"Stroj {row}", label_pos="above" if up else "below")
    net.immediate(f"obsaz_{row}", (13.5, y))
    net.place(f"kopiruje_{row}", (15, y))
    net.timed(f"kop_{row}", (16.5, y), "exp(3 min)", param_pos="below" if up else "above")
    net.chain(f"na_{row}", f"fronta_{row}", f"obsaz_{row}", f"kopiruje_{row}", f"kop_{row}")
    net.arc(f"stroj_{row}", f"obsaz_{row}")
    net.arc(f"kop_{row}", f"stroj_{row}", out=90 if up else 270, into=0)

# netrpělivost: po 10 min ve Frontě B klient odchází
net.timed("netrpelivost", (13.5, 0), "10 min", label="netrpělivost", label_pos="above",
          param_pos="below")
net.arc("fronta_B", "netrpelivost", via=[(12, 0)], corner=20)

# odchod ze systému
net.place("konec", (18, 0), label="konec", label_pos="above left")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod")
net.arc("kop_A", "konec", via=[(18, 2)], corner=20)
net.arc("kop_B", "konec", via=[(18, -2)], corner=20)
net.arc("netrpelivost", "konec")
net.arc("konec", "odchod")

net.invariant({"prepazka": 1, "registrace": 1}, 1)
net.invariant({"stroj_A": 1, "kopiruje_A": 1}, 1)
net.invariant({"stroj_B": 1, "kopiruje_B": 1}, 1)
