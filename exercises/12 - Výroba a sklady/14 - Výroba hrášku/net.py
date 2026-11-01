from pn import Net

net = Net("Výroba hrášku (půlsemestrálka 2013/14, varianta B)")

# dodávky a stroj na přípravu: z dodávky vznikne 100 várek
net.place("gen", (0, 0), tokens=1, label="příjezdy dodávek", label_pos="above")
net.timed("prijezd", (1.5, 0), "exp(3 h)")
net.loop("gen", "prijezd")
net.place("fronta_d", (3, 0), label="Dodávky", label_pos="below")
net.place("stroj_p", (4.5, 1.6), tokens=1, label="Stroj na přípravu", label_pos="above")
net.immediate("obsaz_p", (4.5, 0))
net.place("priprava", (6, 0))
net.timed("prip", (7.5, 0), "30–50 min")
net.chain("prijezd", "fronta_d", "obsaz_p", "priprava")
net.arc("priprava", "prip")
net.arc("stroj_p", "obsaz_p")
net.arc("prip", "stroj_p", out=90, into=0)

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
net.arc("upr", "kapacita", out=270, into=0)

# balení (kapacita 1 várka)
net.place("cekaji", (15.6, 0), label="Čekají na balení", label_pos="below")
net.place("stroj_b", (17.1, -1.6), tokens=1, label="Balicí stroj", label_pos="left")
net.immediate("obsaz_b", (17.1, 0))
net.place("bali", (18.6, 0))
net.timed("bal", (20.1, 0), "1 min", param_pos="below right")
net.chain("upr", "cekaji", "obsaz_b", "bali", "bal")
net.arc("stroj_b", "obsaz_b")
net.arc("bal", "stroj_b", out=270, into=0)
net.place("zabaleno", (21.6, 0), label="zabaleno", label_pos="above")
net.immediate("odvoz", (23.1, 0), exit=True, label="odchod", label_pos="right")
net.chain("bal", "zabaleno", "odvoz")

# trvanlivost čekajících várek a čítač znehodnocených
net.timed("trvanlivost", (15.6, 1.8), "1 h", param_pos="left")
net.place("znehodnocene", (17.1, 1.8), label="Znehodnocené", label_pos="above")
net.chain("cekaji", "trvanlivost", "znehodnocene")

# porucha: projeví se při nejbližším balení a znehodnotí balenou várku; hned nato
# odstavení (p=1, před dalším vstupem do úpravy) vezme „v provozu“ a stroj jde do opravy;
# další porucha se plánuje až po opravě (proces poruch je cyklus)
net.place("gen_p", (23.1, 1.8), tokens=1, label="bez poruchy", label_pos="right")
net.timed("vznik", (21.6, 1.8), "exp(10 h)", param_pos="above")
net.place("porucha", (20.1, 1.8), label="porucha", label_pos="below")
net.chain("gen_p", "vznik", "porucha")
net.immediate("projev", (18.6, 1.8), p=1, param_pos="above right")
net.arc("bali", "projev")
net.arc("porucha", "projev")
net.arc("projev", "znehodnocene")
net.place("v_poruse", (18.6, 3.4), label="stroj v poruše", label_pos="left")
net.arc("projev", "v_poruse")
net.immediate("odstaveni", (20.1, 3.4), p=1, param_pos="below")
net.arc("v_poruse", "odstaveni")
net.arc("provoz", "odstaveni", via=[(11.3, 1.6), (11.3, 5.0), (20.1, 5.0)])
net.place("oprava", (21.6, 3.4), label="Oprava", label_pos="above")
net.timed("opr", (23.1, 3.4), "30–80 min", param_pos="above right")
net.chain("odstaveni", "oprava", "opr", "gen_p")
net.arc("opr", "provoz", via=[(23.1, 5.8), (10.5, 5.8)])
net.arc("opr", "stroj_b", via=[(25.8, 3.4), (25.8, -2.8), (17.1, -2.8)])

net.invariant({"stroj_p": 1, "priprava": 1}, 1)
net.invariant({"kapacita": 1, "uprava": 1}, 50)
net.invariant({"stroj_b": 1, "bali": 1, "v_poruse": 1, "oprava": 1}, 1)
net.invariant({"provoz": 1, "oprava": 1}, 1)
net.invariant({"gen_p": 1, "porucha": 1, "v_poruse": 1, "oprava": 1}, 1)
net.bound("v_poruse", 0)  # odstavení proběhne v tomtéž okamžiku jako projev poruchy
net.bound("cekaji", 50)
# čítač znehodnocených várek (zadání ho chce evidovat) roste s časem
net.unbounded_ok.add("znehodnocene")
# stabilní (zátěž asi 0,7: 100 várek za exp(3 h) proti 50 várkám za hodinu), ale každá
# dodávka přidá 100 značek najednou, takže fronta občas přesáhne 500
net.unbounded_ok.add("fronta_t")
