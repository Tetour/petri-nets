from pn import Net

net = Net("09–16", "Menza (půlsemestrálky 2014–19, Z9)")

# studenti: příchod, výdej u 5 kuchařek, konzumace (každý jí souběžně, slajd 138)
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(3 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("kucharky", (4.5, -1.7), tokens=5, label="Kuchařky", label_pos="below")
net.immediate("obsaz", (4.5, 0))
net.place("vydej", (6, 0), label="výdej", label_pos="below")
net.timed("vyd", (7.5, 0), "exp(1 min)", param_pos="above")
net.chain("prichod", "fronta", "obsaz", "vydej", "vyd")
net.arc("kucharky", "obsaz")
net.arc("vyd", "kucharky", bend=25)
net.place("ji", (9, 0), label="jí", label_pos="below")
net.timed("konzumace", (10.5, 0), "10–15 min", param_pos="below")
net.place("ven", (12, 0), label="ven", label_pos="below")
net.immediate("odchod", (13.5, 0), exit=True, label="odchod", label_pos="below")
net.chain("vyd", "ji", "konzumace", "ven", "odchod")

# hlášení: všichni studenti ven (p=1, smyčka dokud je koho vyhodit), kuchařka se uvolní
net.place("hlaseni", (6, 3.6), label="hlášení", label_pos="right")
net.immediate("v_fronta", (3, 1.8), p=1, horizontal=True, param_pos="above left")
net.immediate("v_vydej", (6, 1.8), p=1, horizontal=True, param_pos="above right")
net.immediate("v_ji", (9, 1.8), p=1, horizontal=True, param_pos="above right")
net.arc("fronta", "v_fronta")
net.arc("vydej", "v_vydej")
net.arc("ji", "v_ji")
net.loop("hlaseni", "v_fronta", bend=8)
net.loop("hlaseni", "v_vydej", bend=20)
net.loop("hlaseni", "v_ji", bend=8)
net.arc("v_vydej", "kucharky", via=[(5.25, 1.8), (5.25, -1.7)])
net.arc("v_ji", "ven")
net.arc("v_vydej", "ven", via=[(7.2, 1.8), (7.2, 1.0), (12, 1.0)])
net.place("vyhnani", (1.5, 1.8), label="vyhnaní", label_pos="left")
net.immediate("odchod2", (1.5, 3.3), exit=True, horizontal=True, label="odchod", label_pos="left")
net.chain("v_fronta", "vyhnani", "odchod2")

# hlášení přichází exp(100 d) od konce poslední karantény
net.immediate("zahajeni", (2.6, 5.4), horizontal=True, label="zahájení karantény", label_pos="above left")
net.place("karantena", (4.4, 5.4), label="Karanténa", label_pos="above")
net.timed("konec_k", (6.2, 5.4), "10 d", param_pos="below")
net.place("bez", (8, 5.4), tokens=1, label="bez karantény", label_pos="above")
net.timed("hlaseni_t", (9.8, 5.4), "exp(100 d)", param_pos="above")
net.chain("hlaseni", "zahajeni", "karantena", "konec_k", "bez", "hlaseni_t", "hlaseni")
# po vyprázdnění (p=0) zastavení příchodů: zahájení karantény vezme značku generátoru
net.arc("gen", "zahajeni", via=[(0, 5.4)])
net.arc("konec_k", "gen", via=[(6.2, 6.8), (-0.9, 6.8), (-0.9, 0)])

net.invariant({"kucharky": 1, "vydej": 1}, 5)
net.invariant({"bez": 1, "hlaseni": 1, "karantena": 1}, 1)
net.invariant({"gen": 1, "karantena": 1}, 1)
net.bound("hlaseni", 1)
# hlášení chodí po exp(100 d): 300 000 událostí je asi 200 dní, tedy 1–3 karantény na běh
net.sim_events = 300000
# při hlášení je fronta skoro vždy prázdná (5 kuchařek, výdej 1 min, příchody po 3 min) a u výdeje
# je někdo jen asi třetinu času; obě vyhánění ověřena zrychleným během (viz poznámka)
net.may_not_fire = {"v_fronta", "v_vydej", "odchod2"}
