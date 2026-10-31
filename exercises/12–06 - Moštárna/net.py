from pn import Net

net = Net("12–06", "Moštárna (půlsemestrálky 2014–19, Z16)")

# 5 sběračů: každý nosí bedýnku po exp(30 min) (každá značka má vlastní odpočet)
net.place("sberaci", (0, 0), tokens=5, label="Sběrači", label_pos="above")
net.timed("prinos", (1.5, 0), "exp(30 min)", param_pos="below")
net.loop("sberaci", "prinos")
net.place("bedynky", (3, 0), label="Bedýnky", label_pos="above")

# plnění lisu (lis nad řadou + moštař pod řadou), pak lis lisuje sám
net.place("lisy", (4.5, 1.6), tokens=5, label="Lisy", label_pos="above")
net.immediate("plneni_start", (4.5, 0))
net.place("plni", (6, 0))
net.timed("plneni", (7.5, 0), "5–7 min", param_pos="above")
net.place("lisuje", (9, 0), label="lisuje", label_pos="above")
net.timed("lisovani", (10.5, 0), "30–40 min", param_pos="below")
net.chain("prinos", "bedynky", "plneni_start", "plni", "plneni", "lisuje", "lisovani")
net.arc("lisy", "plneni_start")
net.arc("lisovani", "lisy", out=90, into=0)     # návrat lisu: oblouk z horní strany přechodu

# moštaři pod nádobou: plní lisy (vlevo) i lahvují (vpravo)
net.place("mostari", (12, -1.6), tokens=2, label="Moštaři", label_pos="below right")
net.arc("mostari", "plneni_start", via=[(12, -2.4), (4.5, -2.4)])
net.arc("plneni", "mostari", out=270, into=180)

# mošt na 20 lahví do nádoby; lahvování má přednost (p=1) před plněním lisu
net.place("nadoba", (12, 0), label="Nádoba", label_pos="above")
net.arc("lisovani", "nadoba", w=20, w_pos="above")
net.place("linka", (13.5, 1.6), tokens=1, label="Lahvovací linka", label_pos="above")
net.immediate("lahv_start", (13.5, 0), p=1, param_pos="below right")
net.place("lahvuje", (15, 0))
net.timed("lahvovani", (16.5, 0), "1–2 min", param_pos="above right")
net.place("lahve", (18, 0), label="láhev", label_pos="below")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("nadoba", "lahv_start", "lahvuje", "lahvovani", "lahve", "odchod")
net.arc("linka", "lahv_start")
net.arc("mostari", "lahv_start", via=[(12, -0.8), (13.5, -0.8)])
net.arc("lahvovani", "linka", out=90, into=0)
net.arc("lahvovani", "mostari", out=270, into=0)

net.invariant({"lisy": 1, "plni": 1, "lisuje": 1}, 5)
net.invariant({"mostari": 1, "plni": 1, "lahvuje": 1}, 2)
net.invariant({"linka": 1, "lahvuje": 1}, 1)
# zadání je přetížené: bedýnek přibývá 10/h, 5 lisů zvládne asi 7,3/h (lis obsazený ~41 min) a mošt na 20 lahví
# z každé bedýnky je mnohem víc, než jedna linka nalahvuje (asi 40 lahví/h)
net.unbounded_ok = {"bedynky", "nadoba"}
