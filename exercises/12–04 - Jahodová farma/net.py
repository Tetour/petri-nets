from pn import Net

net = Net("12–04", "Jahodová farma (půlsemestrálky 2014–19, Z23)")

# 10 sběračů: každá značka má vlastní odpočet exp(15 min) (slajd 138)
net.place("sberaci", (0, 0), tokens=10, label="Sběrači", label_pos="above")
net.timed("sber", (1.5, 0), "exp(15 min)")
net.loop("sberaci", "sber")
net.place("bedynky", (3, 0), label="Bedýnky", label_pos="above")
net.arc("sber", "bedynky")

# vaření: vařič + stroj + 5 bedýnek; příprava s vařičem, pak stroj vaří sám
net.place("varici", (7.5, 3.4), tokens=2, label="Vařiči", label_pos="above left")
net.place("stroje", (3, -1.7), tokens=5, label="Stroje", label_pos="left")
net.immediate("zahajeni", (4.5, 0))
net.arc("bedynky", "zahajeni", w=5)
net.arc("varici", "zahajeni")
net.arc("stroje", "zahajeni")
net.place("priprava", (6, 0), label="příprava", label_pos="above")
net.timed("pripr", (7.5, 0), "10–15 min")
net.chain("zahajeni", "priprava", "pripr")
net.arc("pripr", "varici")
net.place("vari", (9, 0), label="stroj vaří", label_pos="below")
net.timed("vareni", (10.5, 0), "60–70 min", param_pos="above left")
net.chain("pripr", "vari", "vareni")
net.arc("vareni", "stroje", via=[(10.5, -1.7)])
net.place("marmelada", (12, 0), label="Marmeláda", label_pos="below")
net.arc("vareni", "marmelada", w=20, w_pos="below")

# start balicí linky (přednostně před vařením: p=1), pak lahvování dokud je marmeláda
net.place("linka", (12, 5), tokens=1, label="Linka", label_pos="above")
net.immediate("start", (9, 3.4), p=1, label="start linky", label_pos="above", param_pos="below")
net.arc("varici", "start")
net.arc("linka", "start")
net.loop("marmelada", "start", bend=8)
net.place("startuje", (10.5, 3.4))
net.timed("rozjezd", (12, 3.4), "10 min")
net.chain("start", "startuje", "rozjezd")
net.place("bezi", (13.5, 1.7), label="linka běží", label_pos="left")
net.arc("rozjezd", "bezi")
net.immediate("plneni", (13.5, 0), p=1, param_pos="below right")
net.place("plni", (15, 0))
net.timed("lahvovani", (16.5, 0), "1–2 min")
net.chain("marmelada", "plneni", "plni", "lahvovani")
net.arc("bezi", "plneni")
net.arc("lahvovani", "bezi", bend=-25)
net.place("sklenice", (18, 0), label="zabaleno", label_pos="above")
net.immediate("odchod", (19.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("lahvovani", "sklenice", "odchod")

# žádná marmeláda: vařič linku opouští (p=0 < plnění p=1)
net.immediate("konec", (13.5, 3.4), horizontal=True, label="konec lahvování", label_pos="right")
net.arc("bezi", "konec")
net.arc("konec", "linka")
net.arc("konec", "varici", via=[(13.5, 6.2), (7.5, 6.2)])

net.invariant({"varici": 1, "priprava": 1, "startuje": 1, "bezi": 1, "plni": 1}, 2)
net.invariant({"stroje": 1, "priprava": 1, "vari": 1}, 5)
net.invariant({"linka": 1, "startuje": 1, "bezi": 1, "plni": 1}, 1)
# Zadaná čísla dávají nestabilní systém: sběrači přinesou 40 bedýnek za hodinu, 5 strojů
# zpracuje nejvýš asi 19 (cyklus stroje ≈ 77,5 min na 5 bedýnek) a linka zabalí nejvýš
# 40 jednotek za hodinu, zatímco stroje jich uvaří až 77. Bedýnky i marmeláda proto rostou
# a po prvním startu linky marmeláda už nikdy nedojde, takže konec lahvování se neprovede.
# Se sběrem exp(90 min) se konec lahvování provádí pravidelně a invarianty platí (ověřeno).
net.unbounded_ok = {"bedynky", "marmelada"}
net.may_not_fire = {"konec"}
