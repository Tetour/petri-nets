from pn import Net

net = Net("Kravín (příklad z přednášky, tabule luppo)")

# krávy: 100 značek, každá má vlastní odpočet exp(15 h) (slajd 138)
net.place("kravy", (0, 0), tokens=100, label="Krávy", label_pos="above")
net.timed("potreba", (1.5, 0), "exp(15 h)")
net.place("ceka", (3, 0), label="čeká na dojení", label_pos="above")
net.place("dojicky", (4.5, 1.8), tokens=5, label="Dojičky", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("dojeni", (6, 0))
net.chain("kravy", "potreba", "ceka", "obsaz", "dojeni")
net.arc("dojicky", "obsaz")

# 90 % exp(8 min) nahoře, 10 % exp(15 min) dole
for row, y, prob, t, time in (("bezne", 1.8, 90, "dojeni_8", "exp(8 min)"),
                              ("dlouhe", -1.8, 10, "dojeni_15", "exp(15 min)")):
    side = "above" if y > 0 else "below"
    net.immediate(row, (7.5, y), prob=prob, param_pos=side)
    net.arc("dojeni", row, via=[(6, y)], corner=20)
    net.place(f"d_{row}", (9, y))
    net.timed(t, (10.5, y), time, param_pos=side)
    net.chain(row, f"d_{row}", t)
    net.arc(t, "podojeno", via=[(12, y)], corner=20)
net.place("podojeno", (12, 0), label="podojeno", label_pos="left")

# uvolnění dojičky (nahoru) a krávy (dolů), vznikne konvice
net.immediate("konvice_vznik", (13.5, 0))
net.arc("podojeno", "konvice_vznik")
net.arc("konvice_vznik", "dojicky", via=[(13.5, 3.4), (4.5, 3.4)])
net.arc("konvice_vznik", "kravy", via=[(13.5, -3.4), (0, -3.4)])
net.place("konvice", (15, 0), label="Konvice", label_pos="above")
net.arc("konvice_vznik", "konvice")

# nakládání: auto na rampě přinese 20 volných míst; plné auto odjíždí
net.immediate("nalozit", (16.5, 0), label="naložit", label_pos="above")
net.place("nalozeno", (18, 0), label="naloženo", label_pos="above")
net.immediate("odjezd", (19.5, 0), label="odjezd", label_pos="below right")
net.chain("konvice", "nalozit", "nalozeno")
net.arc("nalozeno", "odjezd", w=20)
# konvice odjíždějí nahoru k výstupu, auto pokračuje doprava
net.place("odvezeno", (19.5, 1.8))
net.immediate("odvoz", (21, 1.8), exit=True, label="konvice odvezena", label_pos="above")
net.arc("odjezd", "odvezeno", w=20, w_pos="left")
net.arc("odvezeno", "odvoz")

net.place("volno", (16.5, -1.8), label="volná místa v autě", label_pos="left")
net.arc("volno", "nalozit")
net.immediate("pristaveni", (16.5, -3.4), label="přistavení auta", label_pos="below")
net.arc("pristaveni", "volno", w=20, w_pos="right")
net.place("auta", (15, -3.4), tokens=2, label="Auta", label_pos="left")
net.place("rampa", (18, -3.4), tokens=1, label="Rampa", label_pos="above")
net.arc("auta", "pristaveni")
net.arc("rampa", "pristaveni")
net.arc("odjezd", "rampa", via=[(19.5, -3.4)])
net.place("jede", (21, 0), label="auto jede", label_pos="above")
net.timed("cesta", (22.5, 0), "1 h", param_pos="right")
net.arc("odjezd", "jede")
net.arc("jede", "cesta")
net.arc("cesta", "auta", via=[(22.5, -5.0), (15, -5.0)])

cows = ["kravy", "ceka", "dojeni", "d_bezne", "d_dlouhe", "podojeno"]
net.invariant({p: 1 for p in cows}, 100, name="krávy celkem = 100")
net.invariant({"dojicky": 1, "dojeni": 1, "d_bezne": 1, "d_dlouhe": 1, "podojeno": 1}, 5)
# rampa je obsazená, dokud auto nakládá: volná místa + naloženo = 20
net.invariant({"rampa": 20, "volno": 1, "nalozeno": 1}, 20, name="20 rampa + volno + naloženo = 20")
net.invariant({"auta": 20, "jede": 20, "volno": 1, "nalozeno": 1}, 40,
              name="20 auta + 20 jede + volno + naloženo = 40")
