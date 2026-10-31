from pn import Net

net = Net("11–12", "Přehrada s přístavišti (půlsemestrálka 2011/12, příklad 3)")

# turisté na přístavišti A; na loď čekají nejvýš 20 min (každý vlastní odpočet)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(2 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Čekají na loď", label_pos="above")
net.timed("netrp", (3, -1.6), "20 min", param_pos="left")
net.arc("fronta", "netrp")

# u mola stojí loď („nástup volný“ je jen tehdy): čekající přejdou do fronty k nástupu
net.immediate("na_molo", (4.5, 0), p=1, param_pos="below")
net.place("nf", (6, 0), label="k nástupu", label_pos="below right")
net.chain("prichod", "fronta", "na_molo", "nf")

# nástup po jednom 20–30 s
net.place("nastup", (7.5, 1.6), label="nástup volný", label_pos="above left")
net.loop("nastup", "na_molo", bend=10)
net.immediate("obsaz", (7.5, 0))
net.place("nastupuje", (9, 0))
net.timed("t_nastup", (10.5, 0), "20–30 s", param_pos="below")
net.place("paluba", (12, 0), label="Na palubě", label_pos="right")
net.chain("nf", "obsaz", "nastupuje", "t_nastup", "paluba")
net.arc("nastup", "obsaz")
net.arc("t_nastup", "nastup")

# lodě: první příjezd po exp(3 h); přístaviště A má kapacitu 1
net.place("start", (0, 4.4), tokens=2, label="lodě na začátku", label_pos="below")
net.timed("t_start", (1.5, 4.4), "exp(3 h)", param_pos="above")
net.place("ceka_a", (3, 4.4), label="loď čeká na A", label_pos="below")
net.chain("start", "t_start", "ceka_a")
net.place("molo_a", (4.5, 6.0), tokens=1, label="přístaviště A volné", label_pos="left")
net.immediate("pristani", (4.5, 4.4))
net.arc("ceka_a", "pristani")
net.arc("molo_a", "pristani")
net.arc("pristani", "nastup")
net.place("odpocet", (6, 4.4))
net.timed("t_15", (7.5, 4.4), "15 min", param_pos="above")
net.place("vyprselo", (9, 4.4))
net.chain("pristani", "odpocet", "t_15", "vyprselo")

# odjezd po 15 min (p=1) nebo s plnou lodí (p=1, test 50 na palubě);
# obojí bere „nástup volný“, takže nastupující turista smí dokončit nástup
net.immediate("cas", (10.5, 4.4), p=1, label="po 15 min", label_pos="above", param_pos="below")
net.arc("vyprselo", "cas")
net.arc("nastup", "cas")
net.immediate("plna", (12, 1.6), p=1, label="plná loď", label_pos="right", param_pos="above right")
net.loop("paluba", "plna", w=50, bend=20)
net.arc("nastup", "plna")
net.place("odplouva", (12, 4.4), label="odplouvá", label_pos="above")
net.arc("cas", "odplouva")
net.arc("plna", "odplouva")
net.immediate("odpluti", (13.5, 4.4))
net.arc("odplouva", "odpluti")
net.arc("odpluti", "molo_a", via=[(13.5, 6.6), (4.5, 6.6)])
# po plné lodi ještě běží odpočet 15 min: zrušit ho dřív, než přistane další loď
net.immediate("zrus", (6, 6.0), p=1, label="zruš odpočet", label_pos="above right",
              param_pos="right")
net.arc("odpocet", "zrus")
net.loop("molo_a", "zrus", bend=20)

# s odplutím: turisté na palubě jedou (dál je nesledujeme), neobsloužení odcházejí
net.place("odplula", (9, -3.0), label="loď odplula", label_pos="below right")
net.arc("odpluti", "odplula", via=[(13.5, 3.4), (16.2, 3.4), (16.2, -4.4), (9, -4.4)])
net.immediate("jedou_t", (12, -1.6), p=1, param_pos="below right")
net.arc("paluba", "jedou_t")
net.loop("odplula", "jedou_t", bend=10)
net.place("jedou", (13.5, -1.6), label="na vyhlídce", label_pos="above right")
net.immediate("vyhlidka", (15, -1.6), exit=True, label="odchod", label_pos="below")
net.chain("jedou_t", "jedou", "vyhlidka")
net.immediate("vycisti", (6, -1.6), p=1, label="vyčisti", label_pos="left", param_pos="above right")
net.arc("nf", "vycisti")
net.loop("odplula", "vycisti", bend=-10)
net.immediate("konec_o", (7.5, -4.2), label="hotovo", label_pos="left")
net.arc("odplula", "konec_o")
net.place("odchazi", (4.5, -3.0), label="odcházejí", label_pos="below")
net.immediate("odchod", (3, -3.0), exit=True, label="odchod", label_pos="below")
net.arc("netrp", "odchazi")
net.arc("vycisti", "odchazi")
net.arc("odchazi", "odchod")

# plavba do B 30–40 min, výstup 5 min (přístaviště B s kapacitou 1), zpět 20 min
net.place("plavba", (16.5, 4.4), label="plavba", label_pos="above")
net.arc("odpluti", "plavba")
net.timed("t_plavba", (18, 4.4), "30–40 min", param_pos="below")
net.place("ceka_b", (19.5, 4.4), label="loď čeká na B", label_pos="below")
net.chain("plavba", "t_plavba", "ceka_b")
net.place("molo_b", (21, 6.0), tokens=1, label="přístaviště B volné", label_pos="above")
net.immediate("pristani_b", (21, 4.4))
net.place("vystup", (22.5, 4.4), label="výstup", label_pos="below")
net.timed("t_vystup", (24, 4.4), "5 min", param_pos="below")
net.chain("ceka_b", "pristani_b", "vystup", "t_vystup")
net.arc("molo_b", "pristani_b")
net.arc("t_vystup", "molo_b", bend=-25)
net.place("zpet", (25.5, 4.4), label="cesta do A", label_pos="below")
net.timed("t_zpet", (27, 4.4), "20 min", param_pos="below")
net.chain("t_vystup", "zpet", "t_zpet")
net.arc("t_zpet", "ceka_a", via=[(27, 7.4), (3, 7.4)])

net.invariant({"molo_a": 1, "nastup": 1, "nastupuje": 1, "odplouva": 1}, 1)
net.invariant({"start": 1, "ceka_a": 1, "nastup": 1, "nastupuje": 1, "odplouva": 1,
               "plavba": 1, "ceka_b": 1, "vystup": 1, "zpet": 1}, 2)
net.invariant({"molo_b": 1, "vystup": 1}, 1)
net.bound("paluba", 50)
net.bound("odpocet", 1)
net.bound("odplula", 1)
# nástup 50 turistů trvá aspoň 50 × 20 s ≈ 17 min > 15 min, takže loď s danými čísly
# vždy odplouvá po 15 minutách (plná loď ani rušení odpočtu nenastanou);
# ověřeno zvlášť s rychlejším nástupem
net.may_not_fire |= {"plna", "zrus"}
