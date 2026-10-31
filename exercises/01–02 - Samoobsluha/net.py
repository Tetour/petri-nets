from pn import Net

net = Net("01–02", "Samoobsluha (přednáška, slajdy 195–198)")

# příchody a vozíky (sklad 50)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(8 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta_V", (3, 0), label="fronta na vozík", label_pos="above")
net.place("voziky", (4.5, -1.7), tokens=50, label="Vozíky", label_pos="left")
net.immediate("vzit_vozik", (4.5, 0))
net.place("prodejna", (6, 0), label="v prodejně", label_pos="below")
net.chain("prichod", "fronta_V", "vzit_vozik", "prodejna")
net.arc("voziky", "vzit_vozik")

# 30 % k lahůdkám (sklad 2 prodavačky), 70 % rovnou nakupovat
net.immediate("k_lahudkam", (7.5, 1.8), prob=30, param_pos="above")
net.immediate("bez_lahudek", (7.5, 0), prob=70)
net.place("fronta_L", (9, 1.8), label="fronta u lahůdek", label_pos="below")
net.place("prodavacky", (10.5, 3.5), tokens=2, label="Prodavačky", label_pos="left")
net.immediate("obsaz_L", (10.5, 1.8))
net.place("u_pultu", (12, 1.8))
net.timed("obsl_L", (13.5, 1.8), "exp(2 min)", param_pos="right")
net.chain("prodejna", "k_lahudkam", "fronta_L", "obsaz_L", "u_pultu", "obsl_L")
net.arc("prodavacky", "obsaz_L")
net.arc("obsl_L", "prodavacky", bend=-25)
net.place("nakup", (15, 0), label="nákup", label_pos="below")
net.arc("prodejna", "bez_lahudek")
net.arc("bez_lahudek", "nakup")
net.arc("obsl_L", "nakup")

# běžný nákup a výběr pokladny
net.timed("nakupuje", (16.5, 0), "10–15 min", param_pos="below")
net.place("vyber", (18, 0), label="výběr", label_pos="above left")
net.chain("nakup", "nakupuje", "vyber")

# pět pokladen, každá s vlastní frontou
net.place("zaplaceno", (27, 0))
for i, y in enumerate((5.2, 2.6, 0, -2.6, -5.2), start=1):
    net.immediate(f"k_{i}", (19.5, y), label=f"k {i}.", label_pos="above" if y >= 0 else "below")
    net.place(f"fronta_{i}", (21, y), label=f"fronta {i}", label_pos="below")
    net.place(f"pokladna_{i}", (22.5, y + 1.25), tokens=1, label=f"Pokladna {i}", label_pos="left")
    net.immediate(f"obsaz_{i}", (22.5, y))
    net.place(f"plati_{i}", (24, y))
    net.timed(f"plat_{i}", (25.5, y), "exp(3 min)", param_pos="below")
    net.chain("vyber", f"k_{i}", f"fronta_{i}", f"obsaz_{i}", f"plati_{i}", f"plat_{i}")
    net.arc(f"plat_{i}", "zaplaceno", via=[(26.3, y)] if y else [])
    net.arc(f"pokladna_{i}", f"obsaz_{i}")
    net.arc(f"plat_{i}", f"pokladna_{i}", bend=-30)
net.notes.append(((18.6, -6.3), "k 1.–k 5.: zákazník volí pokladnu s nejkratší frontou (jen poznámka, síť tu volí náhodně)"))

# vrácení vozíku a odchod
net.immediate("vratit_vozik", (28.5, 0), label="vrácení vozíku", label_pos="above")
net.place("odchazi", (30, 0))
net.immediate("odchod", (31.5, 0), exit=True, label="odchod")
net.chain("zaplaceno", "vratit_vozik", "odchazi", "odchod")
net.arc("vratit_vozik", "voziky", via=[(28.5, -7.4), (4.5, -7.4)])

net.invariant({"prodavacky": 1, "u_pultu": 1}, 2)
for i in range(1, 6):
    net.invariant({f"pokladna_{i}": 1, f"plati_{i}": 1}, 1)
inside = ["voziky", "prodejna", "fronta_L", "u_pultu", "nakup", "vyber", "zaplaceno"]
inside += [f"{p}_{i}" for i in range(1, 6) for p in ("fronta", "plati")]
net.invariant({p: 1 for p in inside}, 50, name="vozíky celkem = 50")
