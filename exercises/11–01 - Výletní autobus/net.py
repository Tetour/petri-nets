from pn import Net

net = Net("11–01", "Výletní autobus (půlsemestrálka 2025/26, varianta C – zadání rekonstruované)")

# turisté
net.place("gen_t", (6, 2.9), tokens=1, label="generátor turistů", label_pos="left")
net.timed("prichod_t", (7.5, 2.9), "exp(3 min)", param_pos="right")
net.loop("gen_t", "prichod_t")
net.place("fronta", (7.5, 1.5), label="Fronta turistů", label_pos="right")
net.arc("prichod_t", "fronta")

# každou hodinu přijede autobus: 20 volných míst a odpočet 20 min
net.place("gen_b", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prijezd", (1.5, 0), "1 h", param_pos="above")
net.loop("gen_b", "prijezd")
net.place("bus", (3, 0), label="autobus", label_pos="above right")
net.place("kapacita", (4.5, -1.5), label="kapacita", label_pos="below")
net.place("timer", (1.5, -3), label="timeout", label_pos="left")
net.arc("prijezd", "bus")
net.arc("prijezd", "kapacita", w=20, via=[(2.2, -1.5)], w_pos="left")
net.arc("prijezd", "timer")

# nabírání turistů po jednom (if–else: je volné místo?)
net.immediate("nabira", (4.5, 0), p=1, param_pos="below right")
net.place("ceka", (6, 0), label="čeká na turistu", label_pos="above")
net.immediate("nastup", (7.5, 0))
net.place("nastupuje", (9, 0))
net.timed("nastup_30s", (10.5, 0), "exp(30 s)")
net.chain("bus", "nabira", "ceka", "nastup", "nastupuje", "nastup_30s")
net.arc("kapacita", "nabira")
net.arc("fronta", "nastup")
net.arc("nastup_30s", "bus", via=[(10.5, 4.0), (3, 4.0)])

# odjezd (1): plno
net.immediate("plno", (3, -3), label="plno", label_pos="above right")
net.arc("bus", "plno")
net.arc("timer", "plno")

# odjezd (2): čeká na turistu a uplynulo 20 min
net.timed("t20", (1.5, -4.6), "20 min", param_pos="left")
net.arc("timer", "t20")
net.place("vyprselo", (3, -4.6), label="po 20 min", label_pos="above")
net.arc("t20", "vyprselo")
net.immediate("cekal", (4.5, -4.6), p=1, label="čekal 20 min", label_pos="below right",
              param_pos="above left")
net.arc("vyprselo", "cekal")
net.arc("ceka", "cekal", via=[(6.6, -0.8), (8.4, -0.8), (8.4, -5.5), (4.5, -5.5)])

# odjezd (3): po 20 min se vrátil z nástupu a je plno
net.immediate("plno_po", (3, -6.4), label="plno po 20 min", label_pos="below")
net.arc("vyprselo", "plno_po")
net.arc("bus", "plno_po", via=[(2.3, 1.3), (-0.9, 1.3), (-0.9, -6.4)])

# odjezd: zbylá volná místa zaniknou, autobus odjíždí
net.place("odjezd", (6, -3), label="odjezd", label_pos="above left")
net.arc("plno", "odjezd")
net.arc("cekal", "odjezd")
net.arc("plno_po", "odjezd", via=[(6, -6.4)])
net.immediate("vyprazdni", (6, -1.5), p=1, param_pos="right")
net.loop("odjezd", "vyprazdni", bend=-20)
net.arc("kapacita", "vyprazdni")
net.immediate("pryc", (7.5, -3), exit=True, label="autobus pryč", label_pos="below")
net.arc("odjezd", "pryc")

net.invariant({"bus": 1, "ceka": 1, "nastupuje": 1, "timer": -1, "vyprselo": -1}, 0,
              name="autobus na zastávce = běžící nebo vypršelý odpočet")
for p in ("bus", "ceka", "nastupuje", "timer", "vyprselo", "odjezd"):
    net.bound(p, 1)  # autobus odjede dřív, než přijede další
net.bound("kapacita", 20)  # zbylá místa se při odjezdu vynulují

# Turisté přichází v průměru 20 za hodinu a autobus jich za hodinu odveze nejvýš 20:
# kritické zatížení, fronta turistů se chová jako náhodná procházka a v dlouhé
# simulaci roste (to je vlastnost zadaných čísel, ne chyba sítě).
net.unbounded_ok.add("fronta")
