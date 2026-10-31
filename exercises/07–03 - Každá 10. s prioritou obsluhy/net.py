from pn import Net

net = Net("07–03", "Tiskárna M/M/1: každá 10. úloha má vyšší prioritu obsluhy (přeruší probíhající tisk)")

net.place("gen", (0, 2), tokens=1, label="generátor", label_pos="above")
net.timed("prichod", (1.5, 2), "exp(6 min)")
net.loop("gen", "prichod")
net.place("nova", (3, 2), label="úloha", label_pos="above")
net.arc("prichod", "nova")

# čítač příchodů: 10. úloha jde do prioritní fronty a čítač se vynuluje
net.place("citac", (3, 4), label="čítač", label_pos="above")
net.arc("prichod", "citac")
net.immediate("desata", (4.5, 4), p=1, param_pos="above")
net.immediate("ostatni", (4.5, 0))
net.arc("citac", "desata", w=10, w_pos="above")
net.arc("nova", "desata")
net.arc("nova", "ostatni")
net.place("fronta_p", (6, 4), label="Fronta P", label_pos="above")
net.place("fronta_n", (6, 0), label="Fronta N", label_pos="below")
net.arc("desata", "fronta_p")
net.arc("ostatni", "fronta_n")

# tiskárna
net.place("tiskarna", (8.4, 2), tokens=1, label="Tiskárna", label_pos="above right")
net.immediate("obsaz_p", (7.5, 4), p=1, param_pos="above")
net.immediate("obsaz_n", (7.5, 0))
net.place("tisk_p", (9.3, 4))
net.place("tisk_n", (9.3, 0))
net.timed("konec_p", (10.8, 4), "exp(4 min)", param_pos="above")
net.timed("konec_n", (10.8, 0), "exp(4 min)")
net.chain("fronta_p", "obsaz_p", "tisk_p", "konec_p")
net.chain("fronta_n", "obsaz_n", "tisk_n", "konec_n")
net.arc("tiskarna", "obsaz_p")
net.arc("tiskarna", "obsaz_n")
net.arc("konec_p", "tiskarna", bend=40)
net.arc("konec_n", "tiskarna", bend=-40)

# priorita obsluhy: čekající prioritní úloha vyhodí běžnou z tisku a tiskárnu hned zabere (p=1)
net.immediate("preruseni", (6, 2), label="přerušení", label_pos="left")
net.loop("fronta_p", "preruseni", bend=20)
net.arc("tisk_n", "preruseni")
net.arc("preruseni", "fronta_n")
net.arc("preruseni", "tiskarna")

net.place("konec", (12.3, 2))
net.immediate("odchod", (13.8, 2), exit=True, label="odchod")
net.arc("konec_p", "konec")
net.arc("konec_n", "konec")
net.arc("konec", "odchod")

net.invariant({"tiskarna": 1, "tisk_p": 1, "tisk_n": 1}, 1)
net.bound("citac", 10)
