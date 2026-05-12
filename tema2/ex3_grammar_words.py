# Exercitiul 3: Generarea tuturor cuvintelor de lungime fixa folosind o gramatica
# Citim gramatica si lungimea X, apoi generam toate cuvintele de lungime X
# prin derivari BFS/coada, evitand derivarile infinite.

# ---- Citire input ----

# Prima linie: multimea neterminalelor (separate prin spatii)
neterminale = set(input().split())

# A doua linie: multimea terminalelor (separate prin spatii)
terminale = set(input().split())

# A treia linie: numarul de productii
nr_productii = int(input())

# Citim fiecare productie si o stocam
# productii[neterminal] = lista de siruri de simboluri
productii = {}
for _ in range(nr_productii):
    linie = input().split()
    stanga = linie[0]      # neterminalul din stanga
    dreapta = linie[1:]    # sirul de simboluri din dreapta (poate fi ["λ"])

    if stanga not in productii:
        productii[stanga] = []

    if dreapta == ["λ"]:
        # Productia genereaza sirul vid
        productii[stanga].append([])
    else:
        productii[stanga].append(dreapta)

# Simbolul de start
start = input().strip()

# Lungimea X a cuvintelor de generat
X = int(input())


# ---- Generare prin BFS ----
# Fiecare element din coada este un sir partial de simboluri (lista)
# Pornim de la [start] si aplicam productii pana obtinem doar terminale

# Folosim o multime pentru a nu procesa acelasi sir de doua ori
vizitat = set()
vizitat.add(tuple([start]))

coada = [[start]]  # incepem cu sirul format din simbolul de start
rezultate = set()  # cuvintele finale gasite

while coada:
    sir_curent = coada.pop(0)  # luam primul sir din coada

    # Calculam lungimea minima posibila a sirului curent:
    # fiecare neterminal poate contribui cu cel putin 0 simboluri terminale
    # dar pentru simplitate: daca avem deja mai mult de X terminale, abandonam
    nr_terminale = sum(1 for s in sir_curent if s in terminale)
    nr_neterminale = sum(1 for s in sir_curent if s in neterminale)

    # Daca avem deja prea multe terminale, nu mai putem obtine un cuvant de lungime X
    if nr_terminale > X:
        continue

    # Daca sirul contine doar terminale
    if nr_neterminale == 0:
        if len(sir_curent) == X:
            rezultate.add(tuple(sir_curent))
        continue

    # Lungimea minima posibila = nr_terminale (daca toate neterminalele dispar)
    # Lungimea maxima nedeterminata, dar putem taia daca e clar imposibil
    # Daca lungimea curenta fara neterminale e deja X, atunci neterminalele trebuie sa dispara
    # Heuristica de taiere: daca nr_terminale + nr_neterminale > X si nu exista productii vide
    # Nu taiem prea agresiv, lasam BFS-ul sa se ocupe

    # Gasim primul neterminal din sir si aplicam toate productiile posibile
    for i, simbol in enumerate(sir_curent):
        if simbol in neterminale:
            # Aplicam fiecare productie pentru acest neterminal
            for productie in productii.get(simbol, []):
                # Construim noul sir: inainte + productie + dupa
                sir_nou = sir_curent[:i] + productie + sir_curent[i+1:]

                # Verificam daca sirul nou nu e deja prea lung
                nr_term_nou = sum(1 for s in sir_nou if s in terminale)
                if nr_term_nou > X:
                    continue  # deja prea lung, abandonam

                # Verificam daca lungimea totala posibila poate ajunge la X
                # (daca avem doar terminale de la acest punct, e prea lung)
                if len(sir_nou) > X and all(s in terminale for s in sir_nou):
                    continue

                # Convertim la tuplu pentru a putea stoca in multime
                cheie = tuple(sir_nou)
                if cheie not in vizitat:
                    vizitat.add(cheie)
                    coada.append(sir_nou)

            break  # procesam doar primul neterminal (derivare stanga)


# ---- Afisare rezultate ----
if not rezultate:
    print("NU EXISTA")
else:
    for cuvant in sorted(rezultate):
        print("".join(cuvant))
