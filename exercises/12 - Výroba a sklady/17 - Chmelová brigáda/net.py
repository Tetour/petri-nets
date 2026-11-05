from pn import Net

net = Net("Chmelová brigáda (půlsemestrálka 2010/11)")

# 100 sběračů, každý sbírá svůj košík (každá značka má vlastní odpočet)
net.place("sbira", (-1.5, -1.8), tokens=100, label="Sběrači", label_pos="above")
net.timed("sber", (0, -1.8), "exp(20 min)", label="sběr", label_pos="above")
net.place("plny", (3, -1.8), label="Plný košík", label_pos="above left")
net.chain("sbira", "sber", "plny")

# uložení do skladu, je-li volné místo (p=1, nahoru), jinak procházka (dolů)
net.place("volna", (4.5, 1.6), tokens=20, label="Volná místa ve skladu", label_pos="above")
net.immediate("ulozit", (4.5, 0), p=1, param_pos="below")
net.arc("plny", "ulozit", via=[(3, 0)])
net.place("uklada", (6, 0))
net.timed("ulozeni", (7.5, 0), "1–2 min", label="uložení", label_pos="above",
          param_pos="below right")
net.chain("ulozit", "uklada", "ulozeni")
net.arc("volna", "ulozit")
net.arc("ulozeni", "sbira", via=[(7.5, -5.0), (-1.5, -5.0)])

net.immediate("prochazka", (4.2, -3.4), label="není místo", label_pos="below")
net.arc("plny", "prochazka", via=[(3, -3.4)])
net.place("na_proch", (5.4, -3.4), label="Procházka", label_pos="right")
net.timed("navrat", (5.4, -1.8), "10–15 min", param_pos="right")
net.chain("prochazka", "na_proch", "navrat", "plny")

# sklad a dodávka: začátek nakládání uvolní místo ve skladu
net.place("sklad", (9, 0), label="Sklad", label_pos="above")
net.arc("ulozeni", "sklad")
net.place("dodavka", (10.5, -1.6), tokens=1, label="Dodávka u skladu", label_pos="below right")
net.immediate("nakl_start", (10.5, 0))
net.place("naklada", (12, 0))
net.timed("nakl", (13.5, 0), "exp(2 min)", label="naložení", label_pos="above",
          param_pos="below right")
net.chain("sklad", "nakl_start", "naklada", "nakl")
net.arc("dodavka", "nakl_start")
net.arc("nakl_start", "volna", via=[(10.5, 1.6)])
net.arc("nakl", "dodavka", out=270, into=0)
net.place("nalozeno", (15.2, 0), label="Naloženo", label_pos="above")
net.arc("nakl", "nalozeno")

# 10 košíků: odjezd (p=1 před dalším nakládáním), návrat prázdná za 1 h
net.immediate("odjezd", (16.8, 0), p=1, label="odjezd", label_pos="below right",
              param_pos="above left")
net.arc("nalozeno", "odjezd", w=10, w_pos="below")
net.arc("dodavka", "odjezd", via=[(10.5, -2.6), (16.8, -2.6)])
net.place("na_ceste", (18.3, 0), label="Na cestě", label_pos="above")
net.timed("cesta", (19.8, 0), "1 h", label="návrat", label_pos="above", param_pos="right")
net.chain("odjezd", "na_ceste", "cesta")
net.arc("cesta", "dodavka", via=[(19.8, -3.4), (9.6, -3.4), (9.6, -1.6)])

# odvezené košíky opouštějí systém
net.place("odvezeno", (16.8, 1.6), label="Odvezené košíky", label_pos="above")
net.arc("odjezd", "odvezeno", w=10, w_pos="right")
net.immediate("odchod", (18.3, 1.6), exit=True, label="odchod", label_pos="right")
net.arc("odvezeno", "odchod")

net.invariant({"sbira": 1, "plny": 1, "uklada": 1, "na_proch": 1}, 100)
net.invariant({"volna": 1, "uklada": 1, "sklad": 1}, 20)
net.invariant({"dodavka": 1, "naklada": 1, "na_ceste": 1}, 1)
net.bound("nalozeno", 10)
