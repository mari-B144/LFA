neterminale = set(input().split())

terminale = set(input().split())

nr_productii = int(input())

productii = {}
for _ in range(nr_productii):
    linie = input().split()
    stanga = linie[0]
    dreapta = linie[1:]

    if stanga not in productii:
        productii[stanga] = []

    if dreapta == ["λ"]:
        productii[stanga].append([])
    else:
        productii[stanga].append(dreapta)

start = input().strip()

X = int(input())

vizitat = set()
vizitat.add(tuple([start]))

coada = [[start]]
rezultate = set()

while coada:
    sir_curent = coada.pop(0)

    nr_terminale = sum(1 for s in sir_curent if s in terminale)
    nr_neterminale = sum(1 for s in sir_curent if s in neterminale)

    if nr_terminale > X:
        continue

    if nr_neterminale == 0:
        if len(sir_curent) == X:
            rezultate.add(tuple(sir_curent))
        continue

    for i, simbol in enumerate(sir_curent):
        if simbol in neterminale:
            for productie in productii.get(simbol, []):
                sir_nou = sir_curent[:i] + productie + sir_curent[i+1:]

                nr_term_nou = sum(1 for s in sir_nou if s in terminale)
                if nr_term_nou > X:
                    continue

                if len(sir_nou) > X and all(s in terminale for s in sir_nou):
                    continue

                cheie = tuple(sir_nou)
                if cheie not in vizitat:
                    vizitat.add(cheie)
                    coada.append(sir_nou)

            break

if not rezultate:
    print("NU EXISTA")
else:
    for cuvant in sorted(rezultate):
        print("".join(cuvant))
