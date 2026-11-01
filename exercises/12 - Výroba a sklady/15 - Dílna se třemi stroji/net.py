from pn import Net

net = Net("Dílna se třemi stroji (půlsemestrálka 2011/12, příklad 4)")

# pracovník volí stroj A (horní řada) nebo B (dolní řada) s pravděpodobností 50 %
net.place("volba", (0, 1.2), tokens=1, label="pracovník volí", label_pos="above left")
net.immediate("k_a", (2, 4.2), prob=50, param_pos="above")
net.immediate("k_b", (2, -4.2), prob=50, param_pos="below")
net.arc("volba", "k_a", via=[(0, 4.2)], corner=20)
net.arc("volba", "k_b", via=[(-1.2, 1.2), (-1.2, -4.2)], corner=20)

# stroj A: obsazení, příprava 3–5 min (pracovník), pak sám 10 min, výsledek 20 kusů
# stroj B: příprava 4–6 min, pak sám 15 min, výsledek 20 kusů
for m, y, prep, run in (("a", 4.2, "3–5 min", "10 min"), ("b", -4.2, "4–6 min", "15 min")):
    up = y > 0
    out, inn = ("above", "below") if up else ("below", "above")
    M = m.upper()
    net.place(f"u_{m}", (3.5, y), label=f"u stroje {M}", label_pos=out)
    net.place(f"{m}_vol", (5, y + (1.6 if up else -1.6)), tokens=1, label=f"Stroj {M} volný",
              label_pos=out)
    net.immediate(f"obsaz_{m}", (5, y))
    net.place(f"pripr_{m}", (6.5, y))
    net.timed(f"prip_{m}", (8, y), prep, param_pos=out)
    net.place(f"{m}_vyrabi", (9.5, y), label=f"{M} vyrábí", label_pos=out)
    net.timed(f"t_{m}", (11, y), run, param_pos=inn)
    net.place(f"kont_{m}", (13, y), label=f"Kontejner {M}", label_pos=out)
    net.chain(f"k_{m}", f"u_{m}", f"obsaz_{m}", f"pripr_{m}", f"prip_{m}", f"{m}_vyrabi", f"t_{m}")
    net.arc(f"{m}_vol", f"obsaz_{m}")
    net.arc(f"t_{m}", f"{m}_vol", out=90 if up else 270, into=0)
    net.arc(f"t_{m}", f"kont_{m}", w=20, w_pos=inn)

# pracovník se po přípravě vrací k volbě (mezi řadami)
net.arc("prip_a", "volba", via=[(8, 1.2)])
net.arc("prip_b", "volba", via=[(8, -1.2), (0, -1.2)])

# pracovník je k dispozici, když neopravuje stroj C (testováno přípravou A i B)
net.place("k_disp", (10.4, 0), tokens=1, label="k dispozici", label_pos="above right")
net.loop("k_disp", "prip_a", bend=-10)
net.loop("k_disp", "prip_b", bend=10)

# stroj C: cyklus 1 min, bere současně kus z kontejneru A i B (p=1)
net.place("c_vol", (15.5, 0), tokens=1, label="Stroj C volný", label_pos="above right")
net.immediate("c_start", (18, 0), p=1, param_pos="below right")
net.arc("c_vol", "c_start")
net.arc("kont_a", "c_start", via=[(18, 4.2)])
net.arc("kont_b", "c_start", via=[(18, -4.2)])
net.place("c_vyrabi", (19.5, 0))
net.timed("t_c", (21, 0), "1 min", param_pos="below")
net.place("vyrobek", (22.5, 0), label="výrobek", label_pos="above")
net.immediate("odchod", (24, 0), exit=True, label="odchod", label_pos="above")
net.chain("c_start", "c_vyrabi", "t_c", "vyrobek", "odchod")
net.arc("t_c", "c_vol", via=[(21, 1.6), (15.5, 1.6)])

# chybí mezivýrobek: porucha C (p=0) okamžitě zabere pracovníka, oprava exp(20 min);
# rozpracovaná příprava ztratí test „k dispozici“, takže po opravě začne od začátku
net.immediate("porucha", (12, -1.6), label="porucha C", label_pos="above")
net.arc("k_disp", "porucha", via=[(10.4, -1.6)])
net.arc("c_vol", "porucha", via=[(15.5, -2.8), (12, -2.8)])
net.place("oprava", (13.6, -1.6), label="oprava", label_pos="right")
net.arc("porucha", "oprava")
net.timed("t_oprava", (13.6, 0), "exp(20 min)", param_pos="above")
net.arc("oprava", "t_oprava")
net.arc("t_oprava", "c_vol")
net.arc("t_oprava", "k_disp")

net.invariant({"volba": 1, "u_a": 1, "u_b": 1, "pripr_a": 1, "pripr_b": 1}, 1)
net.invariant({"k_disp": 1, "oprava": 1}, 1)
net.invariant({"c_vol": 1, "c_vyrabi": 1, "oprava": 1}, 1)
net.invariant({"a_vol": 1, "pripr_a": 1, "a_vyrabi": 1}, 1)
net.invariant({"b_vol": 1, "pripr_b": 1, "b_vyrabi": 1}, 1)
# S danými čísly a prázdnými kontejnery na začátku má C hned poruchu, po každé opravě
# znovu (kontejnery jsou pořád prázdné), takže pracovník jen opravuje a nic se nevyrobí.
# Je to vlastnost zadání (C spotřebuje 60 kusů z A i z B za hodinu), ne chyba sítě;
# výrobu a přerušení přípravy jsem ověřil zvlášť s počáteční zásobou 200 kusů.
net.may_not_fire |= {"prip_a", "prip_b", "t_a", "t_b", "c_start", "t_c", "odchod"}
