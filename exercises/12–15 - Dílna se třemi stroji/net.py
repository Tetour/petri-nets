from pn import Net

net = Net("12–15", "Dílna se třemi stroji (půlsemestrálka 2011/12, příklad 4)")

# pracovník volí stroj A nebo B s pravděpodobností 50 %
net.place("volba", (0, 0), tokens=1, label="pracovník volí", label_pos="left")
net.immediate("k_a", (1.5, 2.6), prob=50, param_pos="above")
net.immediate("k_b", (1.5, -2.6), prob=50, param_pos="below")
net.arc("volba", "k_a")
net.arc("volba", "k_b")

# stroj A: příprava 3–5 min (pracovník), pak sám 10 min, výsledek 20 kusů
net.place("u_a", (3, 2.6), label="u stroje A", label_pos="above")
net.timed("prip_a", (4.5, 2.6), "3–5 min", param_pos="above right")
net.place("a_vol", (4.5, 4.2), tokens=1, label="Stroj A volný", label_pos="above")
net.place("a_vyrabi", (6, 2.6), label="A vyrábí", label_pos="above")
net.timed("t_a", (7.5, 2.6), "10 min", param_pos="above")
net.place("kont_a", (9, 2.6), label="Kontejner A", label_pos="above")
net.chain("k_a", "u_a", "prip_a", "a_vyrabi", "t_a")
net.arc("a_vol", "prip_a")
net.arc("t_a", "a_vol", bend=-25)
net.arc("t_a", "kont_a", w=20, w_pos="below")
net.arc("prip_a", "volba")

# stroj B: příprava 4–6 min, pak sám 15 min, výsledek 20 kusů
net.place("u_b", (3, -2.6), label="u stroje B", label_pos="below")
net.timed("prip_b", (4.5, -2.6), "4–6 min", param_pos="below right")
net.place("b_vol", (4.5, -4.2), tokens=1, label="Stroj B volný", label_pos="below")
net.place("b_vyrabi", (6, -2.6), label="B vyrábí", label_pos="below")
net.timed("t_b", (7.5, -2.6), "15 min", param_pos="below")
net.place("kont_b", (9, -2.6), label="Kontejner B", label_pos="below")
net.chain("k_b", "u_b", "prip_b", "b_vyrabi", "t_b")
net.arc("b_vol", "prip_b")
net.arc("t_b", "b_vol", bend=25)
net.arc("t_b", "kont_b", w=20, w_pos="above")
net.arc("prip_b", "volba")

# pracovník je k dispozici, když neopravuje stroj C (testováno přípravou A i B)
net.place("k_disp", (3, 0), tokens=1, label="k dispozici", label_pos="below left")
net.loop("k_disp", "prip_a", bend=12)
net.loop("k_disp", "prip_b", bend=12)

# stroj C: cyklus 1 min, bere současně kus z kontejneru A i B (p=1)
net.place("c_vol", (6, 0), tokens=1, label="Stroj C volný", label_pos="above right")
net.immediate("c_start", (10.5, 0), p=1, param_pos="below right")
net.arc("c_vol", "c_start")
net.arc("kont_a", "c_start")
net.arc("kont_b", "c_start")
net.place("c_vyrabi", (12, 0))
net.timed("t_c", (13.5, 0), "1 min", param_pos="above")
net.place("vyrobek", (15, 0), label="výrobek", label_pos="above")
net.immediate("odchod", (16.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("c_start", "c_vyrabi", "t_c", "vyrobek", "odchod")
net.arc("t_c", "c_vol", via=[(13.5, -1.3), (6.6, -1.3)])

# chybí mezivýrobek: porucha C (p=0) okamžitě zabere pracovníka, oprava exp(20 min);
# rozpracovaná příprava ztratí test „k dispozici“, takže po opravě začne od začátku
net.immediate("porucha", (4.5, -1.2), horizontal=True, label="porucha C", label_pos="below")
net.arc("c_vol", "porucha")
net.arc("k_disp", "porucha")
net.place("oprava", (4.5, 0))
net.arc("porucha", "oprava")
net.timed("t_oprava", (4.5, 1.2), "exp(20 min)", horizontal=True, param_pos="right")
net.arc("oprava", "t_oprava")
net.arc("t_oprava", "k_disp")
net.arc("t_oprava", "c_vol")

net.invariant({"volba": 1, "u_a": 1, "u_b": 1}, 1)
net.invariant({"k_disp": 1, "oprava": 1}, 1)
net.invariant({"c_vol": 1, "c_vyrabi": 1, "oprava": 1}, 1)
net.invariant({"a_vol": 1, "a_vyrabi": 1}, 1)
net.invariant({"b_vol": 1, "b_vyrabi": 1}, 1)
# S danými čísly a prázdnými kontejnery na začátku má C hned poruchu, po každé opravě
# znovu (kontejnery jsou pořád prázdné), takže pracovník jen opravuje a nic se nevyrobí.
# Je to vlastnost zadání (C spotřebuje 60 kusů z A i z B za hodinu), ne chyba sítě;
# výrobu a přerušení přípravy jsem ověřil zvlášť s počáteční zásobou 200 kusů.
net.may_not_fire |= {"prip_a", "prip_b", "t_a", "t_b", "c_start", "t_c", "odchod"}
