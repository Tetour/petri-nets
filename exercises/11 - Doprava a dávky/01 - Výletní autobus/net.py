from pn import Net

net = Net("Výletní autobus (půlsemestrálka 2025/26, varianta C – zadání rekonstruované)")

# autobus: každou hodinu přijede proces „autobus“ s 20 volnými místy a vlastním odpočtem 20 min
net.place("gen_b", (0, -1.8), tokens=1, label="příjezdy autobusů", label_pos="below")
net.timed("prijezd", (1.75, -1.8), "1 h", param_pos="below right")
net.loop("gen_b", "prijezd")
net.place("bus", (3.5, 0), label="autobus", label_pos="above left")
net.arc("prijezd", "bus", via=[(1.75, 0)])
net.place("kapacita", (5.25, -1.8), label="kapacita", label_pos="above left")
net.arc("prijezd", "kapacita", w=20, via=[(2.7, -1.8)], w_pos="above")
net.place("timer", (1.75, -5.4), label="timeout", label_pos="left")
net.arc("prijezd", "timer")

# turisté
net.place("gen_t", (5.25, 2), tokens=1, label="příchody turistů", label_pos="above")
net.timed("prichod_t", (7, 2), "exp(3 min)", param_pos="below")
net.loop("gen_t", "prichod_t")
net.place("fronta", (8.75, 2), label="fronta turistů", label_pos="right")
net.arc("prichod_t", "fronta")

# if–else „je volné místo?“: p=1 nabírá, jinak (p=0) je plno
net.immediate("nabira", (5.25, 0), p=1, param_pos="above")
net.place("ceka", (7, 0), label="čeká na turistu", label_pos="above")
net.immediate("nastup", (8.75, 0))
net.place("nastupuje", (10.5, 0), label="nastupuje", label_pos="below")
net.timed("nastup_30s", (12.25, 0), "exp(30 s)", param_pos="below")
net.chain("bus", "nabira", "ceka", "nastup", "nastupuje", "nastup_30s")
net.arc("kapacita", "nabira")
net.arc("fronta", "nastup")
net.arc("nastup_30s", "bus", via=[(12.25, 3.8), (3.5, 3.8)])
net.immediate("plno", (3.5, -7.2), label="plno", label_pos="left")
net.arc("bus", "plno")
net.place("plny", (5.25, -7.2), label="plný autobus", label_pos="above")
net.arc("plno", "plny")

# odpočet 20 min; po něm už autobus nikoho nenabere: zbylá místa zaniknou (p=2)
net.timed("t20", (7, -5.4), "20 min", param_pos="right")
net.arc("timer", "t20")
net.place("vyprselo", (7, -3.6), label="po 20 min", label_pos="below right")
net.arc("t20", "vyprselo")
net.immediate("vyprazdni", (5.25, -3.6), p=2, param_pos="below")
net.loop("vyprselo", "vyprazdni")
net.arc("kapacita", "vyprazdni")

# odjezd (1): plný autobus, odpočet zanikne
net.immediate("odjezd_plny", (5.25, -9), label="odjezd plného", label_pos="below")
net.arc("plny", "odjezd_plny")
net.arc("timer", "odjezd_plny", via=[(1.75, -9)])
# odjezd (2): čeká na turistu a uplynulo 20 min
net.immediate("cekal", (7, -1.8), p=1, label="čekal 20 min", label_pos="above right",
              param_pos="left")
net.arc("ceka", "cekal")
net.arc("vyprselo", "cekal")
# odjezd (3): odpočet vypršel během nástupu posledního turisty, autobus se vrátil plný
net.immediate("plny_po", (9.25, -3.6), label="plný po 20 min", label_pos="above")
net.arc("vyprselo", "plny_po")
net.arc("plny", "plny_po", via=[(9.25, -7.2)])

net.place("odjezd", (10.5, -3.6), label="odjezd", label_pos="above right")
net.arc("cekal", "odjezd", via=[(10.5, -1.8)])
net.arc("plny_po", "odjezd")
net.arc("odjezd_plny", "odjezd", via=[(10.5, -9)])
net.immediate("pryc", (12.25, -3.6), exit=True, label="autobus pryč", label_pos="below")
net.arc("odjezd", "pryc")

net.invariant({"bus": 1, "ceka": 1, "nastupuje": 1, "plny": 1, "timer": -1, "vyprselo": -1}, 0,
              name="autobus na zastávce = běžící nebo vypršelý odpočet")
for p in ("bus", "ceka", "nastupuje", "plny", "timer", "vyprselo", "odjezd"):
    net.bound(p, 1)  # autobus odjede dřív, než přijede další
net.bound("kapacita", 20)  # zbylá místa po 20 minutách zaniknou

# Turisté přichází v průměru 20 za hodinu a autobus jich za hodinu odveze nejvýš 20:
# kritické zatížení, fronta turistů se chová jako náhodná procházka a v dlouhé
# simulaci roste (to je vlastnost zadaných čísel, ne chyba sítě).
net.unbounded_ok.add("fronta")
