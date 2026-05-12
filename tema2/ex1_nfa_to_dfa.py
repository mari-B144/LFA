# Exercitiul 1: Transformare λ-NFA → DFA minim
# Citim input-ul, construim DFA prin subset construction, apoi minimizam DFA-ul

# ---- Citire input ----

# Prima linie: multimea starilor (separate prin spatii)
states = input().split()

# A doua linie: alfabetul de intrare (simboluri separate prin spatii)
alphabet = input().split()

# A treia linie: numarul de tranzitii
n = int(input())

# Citim fiecare tranzitie si o stocam intr-un dictionar
# tranzitii[stare][simbol] = lista de stari urmatoare
tranzitii = {}
for _ in range(n):
    linie = input().split()
    src = linie[0]
    dst = linie[1]
    sym = linie[2]  # poate fi "λ" pentru tranzitii lambda

    if src not in tranzitii:
        tranzitii[src] = {}
    if sym not in tranzitii[src]:
        tranzitii[src][sym] = []
    tranzitii[src][sym].append(dst)

# Starea initiala
start = input().strip()

# Multimea starilor finale (separate prin spatii)
finals = set(input().split())


# ---- Lambda-closure ----
# Functie care returneaza toate starile accesibile din 'stare' folosind doar tranzitii λ
def lambda_closure(stare, tranzitii):
    # Pornim cu starea insasi
    inchidere = set()
    inchidere.add(stare)
    stiva = [stare]

    while stiva:
        curenta = stiva.pop()
        # Vedem daca exista tranzitii λ din starea curenta
        vecini_lambda = tranzitii.get(curenta, {}).get("λ", [])
        for vecin in vecini_lambda:
            if vecin not in inchidere:
                inchidere.add(vecin)
                stiva.append(vecin)

    return frozenset(inchidere)


# Lambda-closure pentru o multime de stari
def closure_multime(multime, tranzitii):
    rezultat = set()
    for s in multime:
        rezultat |= lambda_closure(s, tranzitii)
    return frozenset(rezultat)


# ---- Subset construction (NFA → DFA) ----
# Fiecare stare DFA este o multime inghetata (frozenset) de stari NFA

# Starea initiala a DFA = lambda-closure a starii initiale NFA
start_dfa = closure_multime({start}, tranzitii)

# Coada de stari DFA neexplorate inca
coada = [start_dfa]

# Tinem evidenta starilor DFA deja create
stari_dfa = {start_dfa}

# Tranzitiile DFA: dfa_tranzitii[stare_dfa][simbol] = stare_dfa_urmatoare
dfa_tranzitii = {}

while coada:
    curenta = coada.pop(0)
    dfa_tranzitii[curenta] = {}

    for simbol in alphabet:
        # Calculam multimea starilor NFA accesibile cu 'simbol' din starile curente
        urmatoare = set()
        for s in curenta:
            destinatii = tranzitii.get(s, {}).get(simbol, [])
            urmatoare |= set(destinatii)

        # Aplicam lambda-closure pe rezultat
        urmatoare_closure = closure_multime(urmatoare, tranzitii)

        # Daca multimea nu e vida, adaugam tranzitia
        if urmatoare_closure:
            dfa_tranzitii[curenta][simbol] = urmatoare_closure
            if urmatoare_closure not in stari_dfa:
                stari_dfa.add(urmatoare_closure)
                coada.append(urmatoare_closure)

# Starile finale DFA sunt cele care contin cel putin o stare finala NFA
finals_dfa = set()
for sd in stari_dfa:
    if sd & finals:  # intersectie nevida
        finals_dfa.add(sd)


# ---- Minimizare DFA (algoritmul de partitionare) ----
# Impartim starile in doua grupuri: finale si non-finale
finale = frozenset(finals_dfa)
non_finale = frozenset(stari_dfa - finals_dfa)

# Partitia initiala (ignoram multimile vide)
partitie = set()
if finale:
    partitie.add(finale)
if non_finale:
    partitie.add(non_finale)


# Functie care gaseste in ce grup din partitie se afla o stare
def gaseste_grup(stare, partitie):
    for grup in partitie:
        if stare in grup:
            return grup
    return None  # stare moarta (trap state), nu exista in DFA


# Rafinam partitia pana cand nu mai putem
while True:
    partitie_noua = set()
    schimbare = False

    for grup in partitie:
        # Incercam sa spargem grupul
        subgrupuri = {}

        for stare in grup:
            # Semnatura = pentru fiecare simbol, in ce grup ajungem
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

        # Daca grupul s-a spart in mai multe subgrupuri, avem o schimbare
        for sg in subgrupuri.values():
            partitie_noua.add(frozenset(sg))
        if len(subgrupuri) > 1:
            schimbare = True

    partitie = partitie_noua
    if not schimbare:
        break


# ---- Construim DFA minim din partitie ----
# Fiecare grup devine o singura stare in DFA-ul minim
# Reprezentantul unui grup = primul element (sortat pentru determinism)

def repr_grup(grup):
    return sorted(grup, key=lambda x: sorted(x))[0]


# Mapam fiecare grup la un nume simplu: q0, q1, ...
grupuri_lista = sorted(partitie, key=lambda g: sorted(g, key=lambda x: sorted(x)))
grup_la_nume = {}
for i, grup in enumerate(grupuri_lista):
    grup_la_nume[frozenset(grup)] = "q" + str(i)


# Functie care gaseste grupul unei stari DFA
def grup_al_starii(stare):
    for grup in partitie:
        if stare in grup:
            return frozenset(grup)
    return None


# Starea initiala minima = grupul care contine start_dfa
grup_start = grup_al_starii(start_dfa)
start_min = grup_la_nume[grup_start]

# Starile finale minime = grupurile care contin cel putin o stare finala DFA
finals_min = set()
for grup in partitie:
    if grup & finals_dfa:
        finals_min.add(grup_la_nume[frozenset(grup)])

# Tranzitiile DFA minim
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


# ---- Numim starile DFA echivalent (inainte de minimizare) ----
# Sortam starile DFA dupa continut pentru nume deterministe: d0, d1, ...
stari_dfa_lista = sorted(stari_dfa, key=lambda x: sorted(x))
stare_dfa_la_nume = {}
for i, sd in enumerate(stari_dfa_lista):
    stare_dfa_la_nume[sd] = "d" + str(i)

start_dfa_nume = stare_dfa_la_nume[start_dfa]
finals_dfa_nume = sorted(stare_dfa_la_nume[sd] for sd in finals_dfa)

# ---- Afisare DFA echivalent (fara λ) ----
# Numaram tranzitiile DFA (inainte de minimizare)
nr_tranzitii_dfa = sum(len(v) for v in dfa_tranzitii.values())

print("DFA echivalent:")
print(" ".join(sorted(stare_dfa_la_nume.values())))  # starile
print(" ".join(alphabet))  # alfabetul
print(nr_tranzitii_dfa)  # numarul de tranzitii

for src, tranz in dfa_tranzitii.items():
    src_nume = stare_dfa_la_nume[src]
    for sym, dst in tranz.items():
        dst_nume = stare_dfa_la_nume[dst]
        print(src_nume, dst_nume, sym)

print(start_dfa_nume)  # starea initiala
print(" ".join(finals_dfa_nume))  # starile finale

# ---- Afisare DFA minim ----
# Numaram tranzitiile DFA minim
nr_tranzitii_min = sum(len(v) for v in tranzitii_min.values())

print("\nDFA minim:")
print(" ".join(sorted(grup_la_nume.values())))
print(" ".join(alphabet))
print(nr_tranzitii_min)

for src, tranz in tranzitii_min.items():
    for sym, dst in tranz.items():
        print(src, dst, sym)

print(start_min)
print(" ".join(sorted(finals_min)))
