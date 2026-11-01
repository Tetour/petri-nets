from pn import Net

net = Net("Menza (půlsemestrálky 2014–19, Z9)")

# studenti: příchod, výdej u 5 kuchařek, konzumace (každý jí souběžně, slajd 138)
net.place("gen", (0, 0), tokens=1, label="příchody studentů", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(3 min)", param_pos="above")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="fronta", label_pos="below")
net.place("kucharky", (4.5, -1.6), tokens=5, label="Kuchařky", label_pos="below")
net.immediate("obsaz", (4.5, 0))
net.place("vydej", (6, 0), label="výdej", label_pos="below left")
net.timed("vyd", (7.5, 0), "exp(1 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "vydej", "vyd")
net.arc("kucharky", "obsaz")
# návrat kuchařky: oblouk ze spodní strany přechodu do skladu vlevo dole
net.arc("vyd", "kucharky", out=270, into=0)
net.place("ji", (10.5, 0), label="jí", label_pos="below")
net.timed("konzumace", (12, 0), "10–15 min", param_pos="below")
net.place("ven", (13.5, 0), label="ven", label_pos="below")
net.immediate("odchod", (15, 0), exit=True, label="odchod", label_pos="below")
net.chain("vyd", "ji", "konzumace", "ven", "odchod")

# hlášení: všichni studenti ven (p=1, smyčka, dokud je koho vyhodit), kuchařka se uvolní
net.place("hlaseni", (6, 4), label="hlášení", label_pos="above right")
net.immediate("v_fronta", (3, 1.6), p=1, param_pos="above left")
net.immediate("v_vydej", (6, 1.6), p=1, param_pos="below right")
net.immediate("v_ji", (10.5, 1.6), p=1, param_pos="above right")
net.arc("fronta", "v_fronta")
net.arc("vydej", "v_vydej")
net.arc("ji", "v_ji")
net.loop("hlaseni", "v_fronta", bend=8)
net.loop("hlaseni", "v_vydej", bend=20)
net.loop("hlaseni", "v_ji", bend=8)
# vyhnaní z fronty odcházejí vlevo, od výdeje vpravo, od jídla přes „ven“
net.place("vyhnani", (1.5, 1.6), label="vyhnaní", label_pos="above left")
net.immediate("odchod_f", (1.5, 2.8), exit=True, label="odchod", label_pos="right")
net.chain("v_fronta", "vyhnani", "odchod_f")
net.place("vyhnani_v", (7.5, 1.6), label="vyhnaní", label_pos="above")
net.immediate("odchod_v", (9, 1.6), exit=True, label="odchod", label_pos="below")
net.chain("v_vydej", "vyhnani_v", "odchod_v")
# kuchařka vyhnaného studenta se vrací do skladu zleva (jediné křížení s hlavní řadou)
net.arc("v_vydej", "kucharky", via=[(3.75, 1.6), (3.75, -1.6)])
net.arc("v_ji", "ven", via=[(13.5, 1.6)])

# karanténa: zahájení (p=0, až je menza prázdná) bere i značku příchodů studentů
net.immediate("zahajeni", (4.2, 4), label="zahájení karantény", label_pos="above left")
net.arc("hlaseni", "zahajeni")
net.arc("gen", "zahajeni", via=[(0, 4)])
net.place("karantena", (4.2, 5.6), label="karanténa", label_pos="left")
net.timed("konec_k", (6, 5.6), "10 d", param_pos="below")
net.place("bez", (7.8, 5.6), tokens=1, label="bez karantény", label_pos="above")
net.timed("hlaseni_t", (9.6, 5.6), "exp(100 d)", param_pos="above")
net.chain("zahajeni", "karantena", "konec_k", "bez", "hlaseni_t")
net.arc("hlaseni_t", "hlaseni", via=[(9.6, 4)])
# po karanténě se příchody studentů obnoví
net.arc("konec_k", "gen", via=[(6, 7), (-0.9, 7), (-0.9, 0)])

net.invariant({"kucharky": 1, "vydej": 1}, 5)
net.invariant({"bez": 1, "hlaseni": 1, "karantena": 1}, 1)
net.invariant({"gen": 1, "karantena": 1}, 1)
net.bound("hlaseni", 1)
# hlášení chodí po exp(100 d): 300 000 událostí je asi 200 dní, tedy 1–3 karantény na běh
net.sim_events = 300000
# při hlášení je fronta skoro vždy prázdná (5 kuchařek, výdej 1 min, příchody po 3 min) a u výdeje
# je někdo jen asi třetinu času; obě vyhánění ověřena zrychleným během (viz poznámka)
net.may_not_fire = {"v_fronta", "v_vydej", "odchod_f", "odchod_v"}
