import sys

fin = open("ex1_input.txt", "r")
fout = open("ex1_output.txt", "w")

def citeste():
    return fin.readline().strip()

states = citeste().split()
alphabet = citeste().split()
n = int(citeste())

tranzitii = {}
for _ in range(n):
    linie = citeste().split()
    src = linie[0]
    dst = linie[1]
    sym = linie[2]

    if src not in tranzitii:
        tranzitii[src] = {}
    if sym not in tranzitii[src]:
        tranzitii[src][sym] = []
    tranzitii[src][sym].append(dst)

start = citeste()
finals = set(citeste().split())


def lambda_closure(stare, tranzitii):
    inchidere = set()
    inchidere.add(stare)
    stiva = [stare]

    while stiva:
        curenta = stiva.pop()
        vecini_lambda = tranzitii.get(curenta, {}).get("λ", [])
        for vecin in vecini_lambda:
            if vecin not in inchidere:
                inchidere.add(vecin)
                stiva.append(vecin)

    return frozenset(inchidere)


def closure_multime(multime, tranzitii):
    rezultat = set()
    for s in multime:
        rezultat |= lambda_closure(s, tranzitii)
    return frozenset(rezultat)


# construim dfa prin subset construction
start_dfa = closure_multime({start}, tranzitii)

coada = [start_dfa]
stari_dfa = {start_dfa}
dfa_tranzitii = {}

while coada:
    curenta = coada.pop(0)
    dfa_tranzitii[curenta] = {}

    for simbol in alphabet:
        urmatoare = set()
        for s in curenta:
            destinatii = tranzitii.get(s, {}).get(simbol, [])
            urmatoare |= set(destinatii)

        urmatoare_closure = closure_multime(urmatoare, tranzitii)

        if urmatoare_closure:
            dfa_tranzitii[curenta][simbol] = urmatoare_closure
            if urmatoare_closure not in stari_dfa:
                stari_dfa.add(urmatoare_closure)
                coada.append(urmatoare_closure)

# starile finale dfa sunt cele care contin cel putin o stare finala din nfa
finals_dfa = set()
for sd in stari_dfa:
    if sd & finals: #verif existenta reuniniunii
        finals_dfa.add(sd)


# minimizare prin partitionare
finale = frozenset(finals_dfa)
non_finale = frozenset(stari_dfa - finals_dfa)

partitie = set()
if finale:
    partitie.add(finale)
if non_finale:
    partitie.add(non_finale)


def gaseste_grup(stare, partitie):
    for grup in partitie:
        if stare in grup:
            return grup
    return None


while True:
    partitie_noua = set()
    schimbare = False

    for grup in partitie:
        subgrupuri = {}

        for stare in grup:
            # semnatura = in ce grup ajunge pentru fiecare simbol
            semnatura = []
            for simbol in alphabet:
                dest = dfa_tranzitii.get(stare, {}).get(simbol, None)
                if dest is None:
                    semnatura.append(None)
                else:
                    semnatura.append(gaseste_grup(dest, partitie))
            semnatura = tuple(semnatura)

            if semnatura not in subgrupuri:
                subgrupuri[semnatura] = set()
            subgrupuri[semnatura].add(stare)

        for sg in subgrupuri.values():
            partitie_noua.add(frozenset(sg))
        if len(subgrupuri) > 1:
            schimbare = True

    partitie = partitie_noua
    if not schimbare:
        break


def repr_grup(grup):
    return sorted(grup, key=lambda x: sorted(x))[0]


grupuri_lista = sorted(partitie, key=lambda g: sorted(g, key=lambda x: sorted(x)))
grup_la_nume = {}
for i, grup in enumerate(grupuri_lista):
    grup_la_nume[frozenset(grup)] = "q" + str(i)


def grup_al_starii(stare):
    for grup in partitie:
        if stare in grup:
            return frozenset(grup)
    return None


grup_start = grup_al_starii(start_dfa)
start_min = grup_la_nume[grup_start]

finals_min = set()
for grup in partitie:
    if grup & finals_dfa:
        finals_min.add(grup_la_nume[frozenset(grup)])

tranzitii_min = {}
for grup in partitie:
    repr_s = repr_grup(grup)
    nume_grup = grup_la_nume[frozenset(grup)]
    tranzitii_min[nume_grup] = {}
    for simbol in alphabet:
        dest = dfa_tranzitii.get(repr_s, {}).get(simbol, None)
        if dest is not None:
            dest_grup = grup_al_starii(dest)
            if dest_grup is not None:
                tranzitii_min[nume_grup][simbol] = grup_la_nume[dest_grup]


# dam nume starilor dfa echivalent
stari_dfa_lista = sorted(stari_dfa, key=lambda x: sorted(x))
stare_dfa_la_nume = {}
for i, sd in enumerate(stari_dfa_lista):
    stare_dfa_la_nume[sd] = "d" + str(i)

start_dfa_nume = stare_dfa_la_nume[start_dfa]
finals_dfa_nume = sorted(stare_dfa_la_nume[sd] for sd in finals_dfa)

nr_tranzitii_dfa = sum(len(v) for v in dfa_tranzitii.values())

fout.write("DFA echivalent:\n")
fout.write(" ".join(sorted(stare_dfa_la_nume.values())) + "\n")
fout.write(" ".join(alphabet) + "\n")
fout.write(str(nr_tranzitii_dfa) + "\n")

for src, tranz in dfa_tranzitii.items():
    src_nume = stare_dfa_la_nume[src]
    for sym, dst in tranz.items():
        dst_nume = stare_dfa_la_nume[dst]
        fout.write(src_nume + " " + dst_nume + " " + sym + "\n")

fout.write(start_dfa_nume + "\n")
fout.write(" ".join(finals_dfa_nume) + "\n")

nr_tranzitii_min = sum(len(v) for v in tranzitii_min.values())

fout.write("\nDFA minim:\n")
fout.write(" ".join(sorted(grup_la_nume.values())) + "\n")
fout.write(" ".join(alphabet) + "\n")
fout.write(str(nr_tranzitii_min) + "\n")

for src, tranz in tranzitii_min.items():
    for sym, dst in tranz.items():
        fout.write(src + " " + dst + " " + sym + "\n")

fout.write(start_min + "\n")
fout.write(" ".join(sorted(finals_min)) + "\n")

fin.close()
fout.close()
