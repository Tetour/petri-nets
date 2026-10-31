from pn import Net

net = Net("11–06", "Festivalový autobus (půlsemestrálky 2014–19, Z21)")

# registrace návštěvníků
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("registrace", (1.5, 0), "exp(5 min)", param_pos="below")
net.loop("gen", "registrace")
net.place("registrovani", (3, 0), label="Registrovaní", label_pos="below")
net.arc("registrace", "registrovani")

# 4 h před koncem festivalu (po 8 h z 12) se registrace zastaví
net.place("festival", (-1.5, 5.6), tokens=1, label="festival", label_pos="above")
net.timed("t8h", (-1.5, 4), "8 h", param_pos="left")
net.place("uzaverka", (-1.5, 2))
net.immediate("uzavreni", (-1.5, 0), label="konec registrací", label_pos="left")
net.chain("festival", "t8h", "uzaverka", "uzavreni")
net.arc("gen", "uzavreni")
net.place("uzavreno", (0, 2.2), label="uzavřeno", label_pos="below right")
net.arc("uzavreni", "uzavreno")

# vyzvednutí návštěvníka = jízda k němu exp(3 min)
net.place("volne", (5, -1.7), tokens=20, label="Volná místa", label_pos="left")
net.immediate("vyzvednuti", (5, 0), p=1, param_pos="below right")
net.place("jede", (6.75, 0))
net.timed("jizda", (8.5, 0), "exp(3 min)", param_pos="below")
net.chain("registrovani", "vyzvednuti", "jede", "jizda")
net.arc("volne", "vyzvednuti")
net.place("v_busu", (10.5, 0), label="V autobusu", label_pos="below")
net.arc("jizda", "v_busu")

# autobus vyráží z areálu, když je koho svážet, a spustí odpočet 40 min
net.place("areal", (3, 4), tokens=1, label="Areál", label_pos="above left")
net.immediate("vyjezd", (3, 2), p=1, label="výjezd", label_pos="left", param_pos="above left")
net.arc("areal", "vyjezd")
net.loop("registrovani", "vyjezd", bend=20)
net.place("hleda", (6.75, 2), label="na svozu", label_pos="above left")
net.arc("vyjezd", "hleda")
net.arc("hleda", "vyzvednuti")
net.arc("jizda", "hleda")
net.place("timer", (5, 4), label="odpočet", label_pos="left")
net.arc("vyjezd", "timer")
net.timed("t40", (5, 5.6), "40 min", param_pos="left")
net.arc("timer", "t40")
net.place("vyprselo", (6.75, 5.6), label="40 min uplynulo", label_pos="above")
net.arc("t40", "vyprselo")

# návrat: plno, nebo na svozu déle než 40 min (rozjetá jízda se dokončí)
net.immediate("timeout", (6.75, 4), p=2, horizontal=True, label="po 40 min", label_pos="above right",
              param_pos="below right")
net.arc("hleda", "timeout")
net.arc("vyprselo", "timeout")
net.immediate("plno", (8.5, 2), label="plno", label_pos="below left")
net.arc("hleda", "plno")
net.arc("timer", "plno")
net.arc("v_busu", "plno", w=20, bend=15, w_pos="right")
net.arc("plno", "v_busu", w=20, bend=15, w_pos="right")
net.place("vraci", (10.5, 4), label="vrací se", label_pos="above")
net.arc("timeout", "vraci")
net.arc("plno", "vraci")
net.timed("navrat", (12.5, 4), "exp(3 min)", param_pos="above")
net.place("prijezd", (12.5, 2), label="v areálu", label_pos="left")
net.chain("vraci", "navrat", "prijezd")

# vyložení všech návštěvníků (doba zanedbána), pak je autobus znovu připraven
net.immediate("vylozeni", (12.5, 0), p=1, param_pos="below right")
net.arc("v_busu", "vylozeni")
net.loop("prijezd", "vylozeni", bend=20)
net.arc("vylozeni", "volne", via=[(12.5, -1.7)])
net.place("vystoupil", (14, 0), label="na festivalu", label_pos="above")
net.immediate("odchod", (15.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("vylozeni", "vystoupil", "odchod")
net.immediate("vylozeno", (14, 2), label="vyloženo", label_pos="right")
net.arc("prijezd", "vylozeno")
net.arc("vylozeno", "areal", via=[(14, 7), (3, 7)])

# po uzávěrce a bez registrovaných končí činnost autobusu (p=0 < výjezd p=1)
net.immediate("konec", (1.25, 4), horizontal=True, label="konec činnosti", label_pos="left")
net.arc("areal", "konec")
net.loop("uzavreno", "konec", bend=15)
net.place("skoncil", (1.25, 5.6), label="autobus skončil", label_pos="above")
net.arc("konec", "skoncil")

net.invariant({"areal": 1, "hleda": 1, "jede": 1, "vraci": 1, "prijezd": 1, "skoncil": 1}, 1,
              name="autobus je právě v jednom stavu")
net.invariant({"volne": 1, "jede": 1, "v_busu": 1}, 20)
net.invariant({"hleda": 1, "jede": 1, "timer": -1, "vyprselo": -1}, 0,
              name="na svozu = běží nebo uplynul odpočet")

# model jednoho festivalu: po uzávěrce registrací autobus doveze poslední návštěvníky a skončí,
# síť se pak zastaví (to je správný konec, ne deadlock)
net.closed = True
# Naplnění autobusu je se zadanými čísly téměř nemožné: 20 jízd po exp(3 min) trvá v průměru
# 60 min, svoz ale končí po 40 min. Ověřeno zvlášť s registracemi exp(1 min): „plno“ se provede.
net.may_not_fire = {"plno"}
