from pn import Net

net = Net("12–01", "Zahradnictví a bouřka (půlsemestrálka 2024/25, varianta A)")

# 1) život zahradníka: obchůzka po 10 záhoncích, pak 30 min v budce
net.place("zacatek", (0, 0), tokens=1, label="začátek obchůzky", label_pos="above left")
net.immediate("vyrazi", (1.5, 0), label="vyráží", label_pos="below left")
net.arc("zacatek", "vyrazi")
net.place("prace", (3, 0), label="záhonky k okopání", label_pos="below")
net.arc("vyrazi", "prace", w=10, w_pos="above")
net.place("zahradnik", (4.5, -1.7), label="zahradník", label_pos="left")
net.arc("vyrazi", "zahradnik")
net.immediate("okopat", (4.5, 0), p=1, param_pos="above left")
net.place("okopavani", (6, 0), label="okopávání", label_pos="below")
net.timed("okop", (7.8, 0), "exp(10 min)", param_pos="below right")
net.chain("prace", "okopat", "okopavani", "okop")
net.arc("zahradnik", "okopat")
net.arc("okop", "zahradnik", via=[(7.8, -1.7)])
net.place("okopano", (10.2, 0), label="okopaný záhonek", label_pos="above")
net.immediate("odchod", (11.7, 0), exit=True, label="odchod", label_pos="below")
net.chain("okop", "okopano", "odchod")

net.immediate("hotovo", (4.5, -3.2), horizontal=True, label="obchůzka hotova", label_pos="right")
net.place("budka", (3, -3.2), label="v budce", label_pos="below")
net.timed("odpocinek", (1.5, -3.2), "30 min", param_pos="below")
net.chain("zahradnik", "hotovo", "budka", "odpocinek")
net.arc("odpocinek", "zacatek", via=[(0, -3.2)])

# 2) život bouřky
net.place("ne_bourka", (3, 2.8), tokens=1, label="není bouřka", label_pos="left")
net.place("je_bourka", (9, 2.8), label="je bouřka", label_pos="right")
net.place("gen_b", (7.5, 7.4), tokens=1, label="generátor bouřek", label_pos="above")
net.timed("vznik", (6, 7.4), "exp(48 h)", param_pos="below")
net.place("nastava", (4.5, 7.4), label="bouřka začíná", label_pos="above")
net.immediate("zac_b", (3, 5.8), label="začátek bouřky", label_pos="left")
net.place("proces", (4.5, 5.8), label="trvání", label_pos="above")
net.timed("trvani", (6, 5.8), "exp(1 h)", param_pos="below")
net.place("skoncila", (7.5, 5.8))
net.immediate("konec_b", (9, 5.8), label="konec bouřky", label_pos="right")
net.chain("gen_b", "vznik", "nastava", "zac_b", "proces", "trvani", "skoncila", "konec_b")
net.arc("konec_b", "gen_b")
net.arc("ne_bourka", "zac_b")
net.arc("zac_b", "je_bourka")
net.arc("je_bourka", "konec_b")
net.arc("konec_b", "ne_bourka")
net.loop("ne_bourka", "vyrazi", bend=15)

# 3) interakce: bouřka zastihne zahradníka při okopávání
net.immediate("preruseni", (6.75, 1.5), label="schová se", label_pos="below right")
net.place("schovany", (6, 2.9), label="úkryt", label_pos="above")
net.immediate("navrat", (5.25, 1.5), label="návrat", label_pos="below left")
net.arc("okopavani", "preruseni")
net.arc("preruseni", "schovany")
net.arc("schovany", "navrat")
net.arc("navrat", "okopavani")
net.loop("je_bourka", "preruseni", bend=15)
net.loop("ne_bourka", "navrat", bend=15)

net.invariant({"zacatek": 1, "zahradnik": 1, "okopavani": 1, "schovany": 1, "budka": 1}, 1,
              name="zahradník je právě v jednom stavu")
net.invariant({"ne_bourka": 1, "je_bourka": 1}, 1)
net.invariant({"gen_b": 1, "nastava": 1, "proces": 1, "skoncila": 1}, 1)
net.bound("prace", 10)
net.sim_events = 60000
