from pn import Net

net = Net("12–04", "Jahodová farma (půlsemestrálky 2014–19, Z23)")

# 10 sběračů: každá značka má vlastní odpočet exp(15 min) (slajd 138)
net.place("sberaci", (0, 0), tokens=10, label="Sběrači", label_pos="above")
net.timed("sber", (1.5, 0), "exp(15 min)")
net.loop("sberaci", "sber")
net.place("bedynky", (3, 0), label="Bedýnky", label_pos="above")
net.arc("sber", "bedynky")

# vaření: vařič (nad řadou) + stroj (pod řadou) + 5 bedýnek; příprava s vařičem, pak stroj vaří sám
net.place("varici", (4.5, 1.6), tokens=2, label="Vařiči", label_pos="above left")
net.place("stroje", (4.5, -1.6), tokens=5, label="Stroje", label_pos="below")
net.immediate("zahajeni", (4.5, 0))
net.arc("bedynky", "zahajeni", w=5, w_pos="above")
net.arc("varici", "zahajeni")
net.arc("stroje", "zahajeni")
net.place("priprava", (6, 0), label="příprava", label_pos="below")
net.timed("pripr", (7.5, 0), "10–15 min", param_pos="below")
net.chain("zahajeni", "priprava", "pripr")
net.arc("pripr", "varici", out=90, into=0)      # návrat vařiče: oblouk z horní strany přechodu
net.place("vari", (9, 0), label="stroj vaří", label_pos="below")
net.timed("vareni", (10.5, 0), "60–70 min", param_pos="above")
net.chain("pripr", "vari", "vareni")
net.arc("vareni", "stroje", out=270, into=0)    # návrat stroje (stroje jsou pod řadou)
net.place("marmelada", (12, 0), label="Marmeláda", label_pos="below")
net.arc("vareni", "marmelada", w=20, w_pos="below")

# start balicí linky nad marmeládou (přednostně před vařením: p=1), pak lahvování
net.place("linka", (12, 3.6), tokens=1, label="Linka", label_pos="left")
net.immediate("start", (12, 2), p=1, label="start linky", label_pos="below right",
              param_pos="above right")
net.loop("marmelada", "start")
net.arc("varici", "start", via=[(4.5, 2.8), (11.2, 2.8), (11.2, 2)])
net.arc("linka", "start")
net.place("startuje", (14.25, 2))
net.timed("rozjezd", (15.75, 2), "10 min", param_pos="below")
net.place("bezi", (17.5, 2), label="linka běží", label_pos="above right")
net.chain("start", "startuje", "rozjezd", "bezi")
net.immediate("plneni", (17.5, 0), p=1, param_pos="below")
net.place("plni", (19, 0))
net.timed("lahvovani", (20.5, 0), "1–2 min", param_pos="below")
net.chain("marmelada", "plneni", "plni", "lahvovani")
net.arc("bezi", "plneni")
net.arc("lahvovani", "bezi", out=90, into=0)
net.place("sklenice", (22, 0), label="zabaleno", label_pos="above")
net.immediate("odchod", (23.5, 0), exit=True, label="odchod", label_pos="above")
net.chain("lahvovani", "sklenice", "odchod")

# žádná marmeláda: vařič linku opouští (p=0 < plnění p=1)
net.immediate("konec", (17.5, 3.6), label="konec lahvování", label_pos="right")
net.arc("bezi", "konec")
net.arc("konec", "linka")
net.arc("konec", "varici", via=[(17.5, 4.8), (2.6, 4.8), (2.6, 1.6)])

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
