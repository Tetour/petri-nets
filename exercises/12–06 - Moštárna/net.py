from pn import Net

net = Net("12–06", "Moštárna (půlsemestrálky 2014–19, Z16)")

# 5 sběračů: každý nosí bedýnku po exp(30 min) (každá značka má vlastní odpočet)
net.place("sberaci", (0, 0), tokens=5, label="Sběrači", label_pos="below")
net.timed("prinos", (1.5, 0), "exp(30 min)", param_pos="below")
net.loop("sberaci", "prinos")
net.place("bedynky", (3, 0), label="Bedýnky", label_pos="above")

# plnění lisu (lis + moštař), pak lis lisuje sám
net.place("lisy", (4.5, 1.7), tokens=5, label="Lisy", label_pos="above")
net.immediate("plneni_start", (4.5, 0))
net.place("plni", (6, 0))
net.timed("plneni", (7.5, 0), "5–7 min", param_pos="above")
net.place("lisuje", (9, 0), label="lisuje", label_pos="above")
net.timed("lisovani", (10.5, 0), "30–40 min", param_pos="above right")
net.chain("prinos", "bedynky", "plneni_start", "plni", "plneni", "lisuje", "lisovani")
net.arc("lisy", "plneni_start")
net.arc("lisovani", "lisy", via=[(10.5, 1.7)])
net.place("mostari", (7.5, -1.8), tokens=2, label="Moštaři", label_pos="right")
net.arc("mostari", "plneni_start")
net.arc("plneni", "mostari")

# mošt na 20 lahví do nádoby; lahvování má přednost (p=1) před plněním lisu
net.place("nadoba", (10.5, -3.6), label="Nádoba", label_pos="right")
net.arc("lisovani", "nadoba", w=20, w_pos="right")
net.immediate("lahv_start", (9, -3.6), p=1, param_pos="below")
net.place("lahvuje", (7.5, -3.6))
net.timed("lahvovani", (6, -3.6), "1–2 min", param_pos="above left")
net.place("lahve", (4.5, -3.6), label="láhev", label_pos="below")
net.immediate("odchod", (3, -3.6), exit=True, label="odchod", label_pos="above")
net.chain("nadoba", "lahv_start", "lahvuje", "lahvovani", "lahve", "odchod")
net.arc("mostari", "lahv_start")
net.arc("lahvovani", "mostari")
net.place("linka", (7.5, -5.3), tokens=1, label="Lahvovací linka", label_pos="below")
net.arc("linka", "lahv_start")
net.arc("lahvovani", "linka")

net.invariant({"lisy": 1, "plni": 1, "lisuje": 1}, 5)
net.invariant({"mostari": 1, "plni": 1, "lahvuje": 1}, 2)
net.invariant({"linka": 1, "lahvuje": 1}, 1)
# zadání je přetížené: bedýnek přibývá 10/h, 5 lisů zvládne asi 8,6/h a mošt na 20 lahví
# z každé bedýnky je mnohem víc, než jedna linka nalahvuje (asi 40 lahví/h)
net.unbounded_ok = {"bedynky", "nadoba"}
