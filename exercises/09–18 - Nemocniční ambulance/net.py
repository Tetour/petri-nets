from pn import Net

net = Net("09–18", "Nemocniční ambulance (půlsemestrálky 2014–19, Z6)")

# pacienti: registrace u přepážky, čekárna, vyšetření u jednoho ze dvou lékařů
net.place("gen", (0, 0), tokens=1, label="generátor", label_pos="below")
net.timed("prichod", (1.5, 0), "exp(20 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("fronta", (3, 0), label="Fronta", label_pos="below")
net.place("prepazka", (4.5, 1.7), tokens=1, label="Přepážka", label_pos="left")
net.immediate("obsaz_p", (4.5, 0))
net.place("registrace", (6, 0))
net.timed("reg", (7.5, 0), "1–2 min", param_pos="below")
net.chain("prichod", "fronta", "obsaz_p", "registrace", "reg")
net.arc("prepazka", "obsaz_p")
net.arc("reg", "prepazka", bend=-25)
net.place("cekarna", (9.75, 0), label="Čekárna", label_pos="below")
net.place("lekari", (12, 1.7), tokens=2, label="Lékaři", label_pos="left")
net.immediate("obsaz_l", (12, 0))
net.place("vysetreni", (13.5, 0), label="vyšetření", label_pos="below")
net.timed("vys", (15, 0), "exp(10 min)", param_pos="below")
net.chain("reg", "cekarna", "obsaz_l", "vysetreni", "vys")
net.arc("lekari", "obsaz_l")
net.arc("vys", "lekari", bend=-25)
net.place("konec", (16.5, 0), label="konec", label_pos="below")
net.immediate("odchod", (18, 0), exit=True, label="odchod", label_pos="below")
net.chain("vys", "konec", "odchod")

# sanita: lékaři přeruší vyšetřování a odjíždí oba na 3–4 h
net.place("gen_s", (18.75, 3.6), tokens=1, label="generátor sanit", label_pos="above")
net.timed("sanita_t", (17.25, 3.6), "exp(5 h)", param_pos="below")
net.loop("gen_s", "sanita_t")
net.place("sanita", (15.75, 3.6), label="sanita", label_pos="above right")
net.arc("sanita_t", "sanita")
net.immediate("preruseni", (14.25, 2.4), p=1, horizontal=True, label="přerušení",
              label_pos="below right", param_pos="above left")
net.arc("vysetreni", "preruseni")
net.arc("sanita", "preruseni", bend=-15)
net.arc("preruseni", "sanita", bend=-15)
net.arc("preruseni", "lekari")
net.immediate("odjezd", (12, 3.6), p=1, horizontal=True, label="odjezd lékařů",
              label_pos="above", param_pos="below left")
net.arc("lekari", "odjezd", w=2, w_pos="right")
net.arc("sanita", "odjezd")
net.place("zasah", (10.5, 3.6), label="urgentní zásah", label_pos="left")
net.timed("zasah_t", (10.5, 2.4), "3–4 h", horizontal=True, param_pos="left")
net.chain("odjezd", "zasah", "zasah_t")
net.arc("zasah_t", "lekari", w=2, w_pos="above right")
net.immediate("bez_ucinku", (15.75, 5.0), horizontal=True, label="sanita během zásahu",
              label_pos="right", param_pos="right")
net.arc("sanita", "bez_ucinku")

# přerušení pacienti se přednostně přeobjednají u přepážky a odcházejí
net.place("preobj_f", (3, 3.4), label="k přeobjednání", label_pos="left")
net.arc("preruseni", "preobj_f", via=[(14.25, 6.0), (3, 6.0)])
net.immediate("obsaz_r", (4.5, 3.4), p=1, param_pos="above")
net.place("preobj", (6, 3.4))
net.timed("preobj_t", (7.5, 3.4), "1–2 min", param_pos="below right")
net.chain("preobj_f", "obsaz_r", "preobj", "preobj_t")
net.arc("prepazka", "obsaz_r")
net.arc("preobj_t", "prepazka", bend=20)
net.place("preobjednan", (7.5, 4.8), label="přeobjednaný", label_pos="left")
net.immediate("odchod_r", (9, 4.8), exit=True, label="odchod", label_pos="right")
net.chain("preobj_t", "preobjednan", "odchod_r")

net.invariant({"prepazka": 1, "registrace": 1, "preobj": 1}, 1)
net.invariant({"lekari": 1, "vysetreni": 1, "zasah": 2}, 2,
              name="lékaři: volní + vyšetřující + 2·zásah = 2")
net.bound("sanita", 1)
