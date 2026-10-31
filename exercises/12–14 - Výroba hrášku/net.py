from pn import Net

net = Net("12–14", "Výroba hrášku (půlsemestrálka 2013/14, varianta B)")

# dodávky a stroj na přípravu: z dodávky vznikne 100 várek
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prijezd", (1.5, 0), "exp(3 h)", param_pos="above")
net.loop("gen", "prijezd")
net.place("fronta_d", (3, 0), label="Dodávky", label_pos="below")
net.place("stroj_p", (4.5, 1.6), tokens=1, label="Stroj na přípravu")
net.immediate("obsaz_p", (4.5, 0))
net.place("priprava", (6, 0))
net.timed("prip", (7.5, 0), "30–50 min")
net.chain("prijezd", "fronta_d", "obsaz_p", "priprava", "prip")
net.arc("stroj_p", "obsaz_p")
net.arc("prip", "stroj_p", bend=-25)

# tepelná úprava: kapacita 50 várek, nové várky nevstupují během poruchy balicího stroje
net.place("fronta_t", (9, 0), label="Várky", label_pos="below")
net.arc("prip", "fronta_t", w=100, w_pos="above")
net.place("kapacita", (10.5, -1.6), tokens=50, label="Kapacita tepelné úpravy", label_pos="below")
net.place("provoz", (10.5, 1.6), tokens=1, label="balicí stroj v provozu", label_pos="left")
net.immediate("obsaz_t", (10.5, 0))
net.place("uprava", (12, 0))
net.timed("upr", (13.5, 0), "1 h", param_pos="above")
net.chain("fronta_t", "obsaz_t", "uprava", "upr")
net.arc("kapacita", "obsaz_t")
net.loop("provoz", "obsaz_t", bend=25)
net.arc("upr", "kapacita", bend=25)

# balení (kapacita 1 várka)
net.place("cekaji", (15, 0), label="Čekají na balení", label_pos="below")
net.place("stroj_b", (16.5, -1.6), tokens=1, label="Balicí stroj", label_pos="left")
net.immediate("obsaz_b", (16.5, 0))
net.place("bali", (18, 0))
net.timed("bal", (19.5, 0), "1 min", param_pos="below right")
net.chain("upr", "cekaji", "obsaz_b", "bali", "bal")
net.arc("stroj_b", "obsaz_b")
net.arc("bal", "stroj_b", bend=25)
net.place("zabaleno", (21, 0), label="zabaleno", label_pos="below")
net.immediate("odvoz", (22.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("bal", "zabaleno", "odvoz")

# trvanlivost čekajících várek a čítač znehodnocených
net.timed("trvanlivost", (15, 1.8), "1 h", param_pos="left")
net.place("znehodnocene", (16.5, 1.8), label="Znehodnocené", label_pos="below")
net.chain("cekaji", "trvanlivost", "znehodnocene")

# porucha: projeví se při nejbližším balení, znehodnotí várku, stroj jde do opravy;
# další porucha se plánuje až po opravě (proces poruch je cyklus)
net.place("gen_p", (21.6, 3.6), tokens=1, label="bez poruchy", label_pos="above")
net.timed("vznik", (19.8, 3.6), "exp(10 h)", param_pos="above")
net.place("porucha", (18, 3.6), label="porucha", label_pos="above")
net.chain("gen_p", "vznik", "porucha")
net.immediate("projev", (18, 1.8), p=1, param_pos="below right")
net.arc("bali", "projev")
net.arc("porucha", "projev")
net.arc("provoz", "projev", via=[(11.2, 3.0), (17.3, 3.0)])
net.arc("projev", "znehodnocene")
net.place("oprava", (19.8, 1.8), label="Oprava", label_pos="above")
net.timed("opr", (21.6, 1.8), "30–80 min", param_pos="below")
net.chain("projev", "oprava", "opr", "gen_p")
net.arc("opr", "provoz", via=[(22.8, 2.2), (22.8, 5.2), (10.5, 5.2)])
net.arc("opr", "stroj_b", via=[(23.6, 1.4), (23.6, -2.6), (16.5, -2.6)])

net.invariant({"stroj_p": 1, "priprava": 1}, 1)
net.invariant({"kapacita": 1, "uprava": 1}, 50)
net.invariant({"stroj_b": 1, "bali": 1, "oprava": 1}, 1)
net.invariant({"provoz": 1, "oprava": 1}, 1)
net.invariant({"gen_p": 1, "porucha": 1, "oprava": 1}, 1)
net.bound("cekaji", 50)
# čítač znehodnocených várek (zadání ho chce evidovat) roste s časem
net.unbounded_ok.add("znehodnocene")
# stabilní (zátěž asi 0,7: 100 várek za exp(3 h) proti 50 várkám za hodinu), ale každá
# dodávka přidá 100 značek najednou, takže fronta občas přesáhne 500
net.unbounded_ok.add("fronta_t")
