from pn import Net

net = Net("Tiskárna M/M/1: každá 10. úloha má vyšší prioritu obsluhy (přeruší probíhající tisk)")

Y = 2.4  # vzdálenost řad od středu

net.place("gen", (0, 0), tokens=1, label="příchody úloh", label_pos="above")
net.timed("prichod", (1.5, 0), "exp(6 min)", param_pos="below")
net.loop("gen", "prichod")
net.place("nova", (3, 0), label="úloha", label_pos="right")
net.arc("prichod", "nova")

# čítač příchodů: 10. úloha jde do prioritní fronty a čítač se vynuluje
net.place("citac", (1.5, Y + 1.6), label="čítač", label_pos="left")
net.arc("prichod", "citac")
net.immediate("vyber_p", (4.5, Y), p=1, param_pos="below")
net.immediate("vyber_n", (4.5, -Y))
net.arc("citac", "vyber_p", w=10, via=[(4.5, Y + 1.6)], w_pos="above")

# horní řada úlohy vedení (každá 10.), dolní běžné; tiskárna je mezi řadami
for row, y, name in (("p", Y, "fronta P"), ("n", -Y, "fronta N")):
    up = y > 0
    net.arc("nova", f"vyber_{row}", via=[(3, y)], corner=20)
    net.place(f"fronta_{row}", (6, y), label=name, label_pos="above" if up else "below")
    net.place(f"tisk_{row}", (9.5, y))
    net.timed(f"konec_{row}", (11, y), "exp(4 min)", param_pos="above" if up else "below")
    net.chain(f"vyber_{row}", f"fronta_{row}")
    net.chain(f"obsaz_{row}", f"tisk_{row}", f"konec_{row}")

net.place("tiskarna", (8, 0), tokens=1, label="tiskárna", label_pos="above left")
net.immediate("obsaz_p", (8, Y), p=1, param_pos="above")
net.immediate("obsaz_n", (8, -Y))
net.arc("fronta_p", "obsaz_p")
net.arc("fronta_n", "obsaz_n")
net.arc("tiskarna", "obsaz_p")
net.arc("tiskarna", "obsaz_n")
net.arc("konec_p", "tiskarna", out=270, into=25)
net.arc("konec_n", "tiskarna", out=90, into=-25)

# priorita obsluhy: čekající prioritní úloha vyhodí běžnou z tisku a tiskárnu hned zabere (p=1).
# Síť s jednou tiskárnou, společným odchodem a tímto přechodem nejde nakreslit bez křížení
# (není rovinná): hrana z tisku N kříží hranu tiskárna → obsazení N.
net.immediate("preruseni", (6, 0), label="přerušení", label_pos="below right")
net.loop("fronta_p", "preruseni", bend=20)
net.arc("tisk_n", "preruseni", via=[(9.5, -1.0), (6, -1.0)])
net.arc("preruseni", "fronta_n", via=[(5.25, 0), (5.25, -1.5), (6, -1.5)])
net.arc("preruseni", "tiskarna")

net.place("konec", (12.5, 0), label="vytištěno", label_pos="left")
net.immediate("odchod", (14, 0), exit=True, label="odchod")
net.arc("konec_p", "konec", via=[(12.5, Y)], corner=20)
net.arc("konec_n", "konec", via=[(12.5, -Y)], corner=20)
net.arc("konec", "odchod")

net.invariant({"tiskarna": 1, "tisk_p": 1, "tisk_n": 1}, 1)
net.bound("citac", 10)
