from pn import Net

net = Net("Festivalový autobus (půlsemestrálky 2014–19, Z21)")

# registrace návštěvníků
net.place("gen", (0, 0), tokens=1, label="registrace návštěvníků", label_pos="below left")
net.timed("registrace", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "registrace")
net.place("registrovani", (3, 0), label="registrovaní", label_pos="below")
net.arc("registrace", "registrovani")

# 4 h před koncem festivalu (po 8 h z 12) se registrace zastaví
net.place("festival", (-3, -3.6), tokens=1, label="festival", label_pos="below")
net.timed("t8h", (-1.5, -3.6), "8 h", param_pos="below")
net.place("uzaverka", (0, -3.6), label="po 8 h", label_pos="below")
net.chain("festival", "t8h", "uzaverka")
net.immediate("uzavreni", (0, -1.8), label="konec registrací", label_pos="right")
net.arc("uzaverka", "uzavreni")
net.arc("gen", "uzavreni")
net.place("uzavreno", (-1.5, 1.8), label="uzavřeno", label_pos="left")
net.arc("uzavreni", "uzavreno", via=[(-1.5, -1.8)])

# autobus vyráží z areálu, když je koho svážet (p=1), a spustí odpočet 40 min
net.place("areal", (1.5, 1.8), tokens=1, label="areál", label_pos="above right")
net.immediate("vyjezd", (3, 1.8), p=1, label="výjezd", label_pos="below right",
              param_pos="above right")
net.arc("areal", "vyjezd")
net.loop("registrovani", "vyjezd", bend=20)
net.place("hleda", (6, 1.8), label="na svozu", label_pos="above left")
net.arc("vyjezd", "hleda")
net.place("timer", (3, 3.6), label="odpočet", label_pos="left")
net.arc("vyjezd", "timer")
net.timed("t40", (4.5, 5.4), "40 min", param_pos="above")
net.arc("timer", "t40", via=[(4.5, 3.6)])
net.place("vyprselo", (6, 5.4), label="40 min uplynulo", label_pos="right")
net.arc("t40", "vyprselo")

# vyzvednutí návštěvníka = jízda k němu exp(3 min); po jízdě rozhoduje „po jízdě“
net.place("volne", (6, -1.8), tokens=20, label="volná místa", label_pos="left")
net.immediate("vyzvednuti", (6, 0), p=1, param_pos="below right")
net.place("jede", (7.5, 0), label="jede", label_pos="below")
net.timed("jizda", (9, 0), "exp(3 min)", param_pos="below")
net.chain("registrovani", "vyzvednuti", "jede", "jizda")
net.arc("hleda", "vyzvednuti")
net.arc("volne", "vyzvednuti")
net.place("v_busu", (10.5, 0), label="v autobusu", label_pos="below")
net.arc("jizda", "v_busu")
net.place("po_jizde", (9, 1.8), label="po jízdě", label_pos="above")
net.arc("jizda", "po_jizde")
net.immediate("pokracuje", (7.5, 1.8))
net.chain("po_jizde", "pokracuje", "hleda")

# návrat: plno (test 20 v autobusu), nebo na svozu déle než 40 min (p=2 před dalším vyzvednutím)
net.immediate("plno", (10.5, 1.8), p=1, label="plno", label_pos="above left", param_pos="right")
net.arc("po_jizde", "plno")
net.loop("v_busu", "plno", bend=20, w=20)
net.immediate("timeout", (6, 3.6), p=2, label="po 40 min", label_pos="below left", param_pos="above left")
net.arc("hleda", "timeout")
net.arc("vyprselo", "timeout")
net.place("vraci", (10.5, 3.6), label="vrací se", label_pos="below right")
net.arc("plno", "vraci")
net.arc("timeout", "vraci")
# plný autobus se vrací dřív: běžící odpočet zanikne (p=1)
net.immediate("zrus", (10.5, 5.4), p=1, label="zruš odpočet", label_pos="right", param_pos="left")
net.loop("vraci", "zrus", bend=20)
net.arc("timer", "zrus", via=[(3, 7.2), (10.5, 7.2)])
net.timed("navrat", (12, 3.6), "exp(3 min)", param_pos="above")
net.arc("vraci", "navrat")
net.place("prijezd", (13.5, 1.8), label="v areálu", label_pos="left")
net.arc("navrat", "prijezd", via=[(13.5, 3.6)])

# vyložení všech návštěvníků (doba zanedbána), pak je autobus znovu připraven
net.immediate("vylozeni", (13.5, 0), p=1, param_pos="below left")
net.arc("v_busu", "vylozeni")
net.loop("prijezd", "vylozeni", bend=20)
net.arc("vylozeni", "volne", via=[(13.5, -1.8)])
net.place("vystoupil", (15, 0), label="na festivalu", label_pos="below")
net.immediate("odchod", (16.5, 0), exit=True, label="odchod", label_pos="below")
net.chain("vylozeni", "vystoupil", "odchod")
net.immediate("vylozeno", (15, 1.8), label="vyloženo", label_pos="right")
net.arc("prijezd", "vylozeno")
net.arc("vylozeno", "areal", via=[(15, 8.2), (1.5, 8.2)])

# po uzávěrce a bez registrovaných končí činnost autobusu (p=0 < výjezd p=1)
net.immediate("konec", (0, 1.8), label="konec činnosti", label_pos="above left")
net.arc("areal", "konec")
net.arc("uzavreno", "konec")
net.place("skoncil", (0, 3.6), label="autobus skončil", label_pos="left")
net.arc("konec", "skoncil")

net.invariant({"areal": 1, "hleda": 1, "jede": 1, "po_jizde": 1, "vraci": 1, "prijezd": 1,
               "skoncil": 1}, 1, name="autobus je právě v jednom stavu")
net.invariant({"volne": 1, "jede": 1, "v_busu": 1}, 20)
net.bound("timer", 1)     # odpočet se nehromadí: plný autobus ho zruší
net.bound("vyprselo", 1)

# model jednoho festivalu: po uzávěrce registrací autobus doveze poslední návštěvníky a skončí,
# síť se pak zastaví (to je správný konec, ne deadlock)
net.deadlock_ok = True
# Naplnění autobusu je se zadanými čísly téměř nemožné: 20 jízd po exp(3 min) trvá v průměru
# 60 min, svoz ale končí po 40 min. Ověřeno zvlášť s registracemi exp(1 min): „plno“ se provede.
net.may_not_fire = {"plno", "zrus"}
