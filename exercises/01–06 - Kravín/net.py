from pn import Net

net = Net("01–06", "Kravín (příklad z přednášky, tabule luppo)")

# krávy: 100 značek, každá má vlastní odpočet exp(15 h) (slajd 138)
net.place("kravy", (0, 0), tokens=100, label="Krávy", label_pos="below left")
net.timed("potreba", (1.5, 0), "exp(15 h)", param_pos="below")
net.place("ceka", (3, 0), label="čeká na dojení", label_pos="above")
net.place("dojicky", (4.5, 1.7), tokens=5, label="Dojičky", label_pos="left")
net.immediate("obsaz", (4.5, 0))
net.place("dojeni", (6, 0))
net.chain("kravy", "potreba", "ceka", "obsaz", "dojeni")
net.arc("dojicky", "obsaz")

# 90 % exp(8 min), 10 % exp(15 min)
net.immediate("bezne", (7.5, 0), prob=90, param_pos="above")
net.immediate("dlouhe", (7.5, -1.7), prob=10, param_pos="below")
net.place("d_bezne", (9, 0))
net.place("d_dlouhe", (9, -1.7))
net.timed("dojeni_8", (10.5, 0), "exp(8 min)", param_pos="above")
net.timed("dojeni_15", (10.5, -1.7), "exp(15 min)", param_pos="below")
net.place("podojeno", (12, 0), label="podojeno", label_pos="above")
net.chain("dojeni", "bezne", "d_bezne", "dojeni_8", "podojeno")
net.chain("dojeni", "dlouhe", "d_dlouhe", "dojeni_15", "podojeno")

# uvolnění dojičky a krávy, vznikne konvice
net.immediate("konvice_vznik", (13.5, 0))
net.arc("podojeno", "konvice_vznik")
net.arc("konvice_vznik", "dojicky", via=[(13.5, 1.7)])
net.arc("konvice_vznik", "kravy", via=[(13.5, -3.0), (0, -3.0)])
net.place("konvice", (15, 0), label="Konvice", label_pos="above")
net.arc("konvice_vznik", "konvice")

# nakládání: auto na rampě přinese 20 volných míst
net.immediate("nalozit", (16.5, 0), label="naložit", label_pos="above")
net.place("nalozeno", (18, 0), label="naloženo", label_pos="above")
net.immediate("odjezd", (19.5, 0), label="odjezd", label_pos="above")
net.place("odvezeno", (21, 0))
net.immediate("odvoz", (22.5, 0), exit=True, label="konvice odvezena", label_pos="above")
net.chain("konvice", "nalozit", "nalozeno")
net.arc("nalozeno", "odjezd", w=20)
net.arc("odjezd", "odvezeno", w=20)
net.arc("odvezeno", "odvoz")

net.place("volno", (16.5, -1.7), label="volná místa v autě", label_pos="left")
net.arc("volno", "nalozit")
net.immediate("pristaveni", (16.5, -3.4), horizontal=True, label="přistavení auta",
              label_pos="left")
net.arc("pristaveni", "volno", w=20, w_pos="right")
net.place("auta", (15, -5), tokens=2, label="Auta", label_pos="left")
net.place("rampa", (18, -5), tokens=1, label="Rampa", label_pos="below")
net.arc("auta", "pristaveni")
net.arc("rampa", "pristaveni")
net.arc("odjezd", "rampa", via=[(19.5, -3.4)])
net.place("jede", (21, -1.7), label="auto jede", label_pos="right")
net.timed("cesta", (21, -3.4), "1 h", horizontal=True, param_pos="right")
net.arc("odjezd", "jede")
net.arc("jede", "cesta")
net.arc("cesta", "auta", via=[(21, -6.3), (15, -6.3)])

cows = ["kravy", "ceka", "dojeni", "d_bezne", "d_dlouhe", "podojeno"]
net.invariant({p: 1 for p in cows}, 100, name="krávy celkem = 100")
net.invariant({"dojicky": 1, "dojeni": 1, "d_bezne": 1, "d_dlouhe": 1, "podojeno": 1}, 5)
# rampa je obsazená, dokud auto nakládá: volná místa + naloženo = 20
net.invariant({"rampa": 20, "volno": 1, "nalozeno": 1}, 20, name="20 rampa + volno + naloženo = 20")
net.invariant({"auta": 20, "jede": 20, "volno": 1, "nalozeno": 1}, 40,
              name="20 auta + 20 jede + volno + naloženo = 40")
