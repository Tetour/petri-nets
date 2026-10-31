from pn import Net

net = Net("01–02", "Samoobsluha (přednáška, slajdy 195–198)")

# příchody a vozíky (sklad 50)
net.place("gen", (0, 0), tokens=1, label="příchody zákazníků", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(8 min)")
net.loop("gen", "prichod")
net.place("fronta_V", (3, 0), label="fronta na vozík", label_pos="above")
net.place("voziky", (4.5, -1.8), tokens=50, label="Vozíky", label_pos="left")
net.immediate("vzit_vozik", (4.5, 0))
net.place("prodejna", (6, 0), label="v prodejně", label_pos="below")
net.chain("prichod", "fronta_V", "vzit_vozik", "prodejna")
net.arc("voziky", "vzit_vozik")

# 30 % nahoru k lahůdkám (sklad 2 prodavačky), 70 % rovně rovnou nakupovat
net.immediate("k_lahudkam", (7.5, 1.8), prob=30, param_pos="above")
net.immediate("bez_lahudek", (7.5, 0), prob=70, param_pos="below")
net.arc("prodejna", "k_lahudkam", via=[(6, 1.8)], corner=20)
net.arc("prodejna", "bez_lahudek")
net.place("fronta_L", (9, 1.8), label="fronta u lahůdek", label_pos="below")
net.place("prodavacky", (10.5, 3.4), tokens=2, label="Prodavačky", label_pos="left")
net.immediate("obsaz_L", (10.5, 1.8))
net.place("u_pultu", (12, 1.8))
net.timed("obsl_L", (13.5, 1.8), "exp(2 min)", param_pos="below")
net.chain("k_lahudkam", "fronta_L", "obsaz_L", "u_pultu", "obsl_L")
net.arc("prodavacky", "obsaz_L")
net.arc("obsl_L", "prodavacky", out=90, into=0)
net.place("nakup", (15, 0), label="nákup", label_pos="below")
net.arc("bez_lahudek", "nakup")
net.arc("obsl_L", "nakup", via=[(15, 1.8)], corner=20)

# běžný nákup a výběr pokladny
net.timed("nakupuje", (16.5, 0), "10–15 min")
net.place("vyber", (18, 0), label="výběr", label_pos="above left")
net.chain("nakup", "nakupuje", "vyber")

# pět pokladen, každá s vlastní frontou; z místa výběr a do místa zaplaceno vede pět hran,
# na čtyři strany místa se nevejdou, proto se rozbíhají a sbíhají vějířem
net.place("zaplaceno", (29, 0))
rows = ((5.2, 70), (2.6, 40), (0, 0), (-2.6, -40), (-5.2, -70))
for i, (y, angle) in enumerate(rows, start=1):
    side = "above" if y >= 0 else "below"
    net.immediate(f"k_{i}", (20.5, y), label=f"k {i}.", label_pos=side)
    net.place(f"fronta_{i}", (22, y), label=f"fronta {i}", label_pos="below")
    net.place(f"pokladna_{i}", (23.5, y + 1.25), tokens=1, label=f"Pokladna {i}", label_pos="left")
    net.immediate(f"obsaz_{i}", (23.5, y))
    net.place(f"plati_{i}", (25, y))
    net.timed(f"plat_{i}", (26.5, y), "exp(3 min)", param_pos="below")
    net.chain(f"k_{i}", f"fronta_{i}", f"obsaz_{i}", f"plati_{i}", f"plat_{i}")
    if angle:
        net.arc("vyber", f"k_{i}", out=angle, into=180)
        net.arc(f"plat_{i}", "zaplaceno", out=0, into=180 - angle)
    else:
        net.arc("vyber", f"k_{i}")
        net.arc(f"plat_{i}", "zaplaceno")
    net.arc(f"pokladna_{i}", f"obsaz_{i}")
    net.arc(f"plat_{i}", f"pokladna_{i}", out=90, into=0)
net.notes.append(((18.6, -6.9), "k 1.–k 5.: zákazník volí pokladnu s nejkratší frontou (jen poznámka, síť tu volí náhodně)"))

# vrácení vozíku a odchod
net.immediate("vratit_vozik", (30.5, 0), label="vrácení vozíku", label_pos="above")
net.place("odchazi", (32, 0))
net.immediate("odchod", (33.5, 0), exit=True, label="odchod")
net.chain("zaplaceno", "vratit_vozik", "odchazi", "odchod")
net.arc("vratit_vozik", "voziky", via=[(30.5, -7.8), (4.5, -7.8)])

net.invariant({"prodavacky": 1, "u_pultu": 1}, 2)
for i in range(1, 6):
    net.invariant({f"pokladna_{i}": 1, f"plati_{i}": 1}, 1)
inside = ["voziky", "prodejna", "fronta_L", "u_pultu", "nakup", "vyber", "zaplaceno"]
inside += [f"{p}_{i}" for i in range(1, 6) for p in ("fronta", "plati")]
net.invariant({p: 1 for p in inside}, 50, name="vozíky celkem = 50")
