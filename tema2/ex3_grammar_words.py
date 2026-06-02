fin = open("ex3_input.txt", "r")
fout = open("ex3_output.txt", "w")

def citeste():
    return fin.readline().strip()

neterminale = set(citeste().split())
terminale = set(citeste().split())
nr_productii = int(citeste())

productii = {}
for _ in range(nr_productii):
    linie = citeste().split()
    stanga = linie[0]
    dreapta = linie[1:]

    if stanga not in productii:
        productii[stanga] = []

    if dreapta == ["λ"]:
        # productia genereaza sirul vid
        productii[stanga].append([])
    else:
        productii[stanga].append(dreapta)

start = citeste()
X = int(citeste())


# generam cuvintele prin bfs, pornim din simbolul de start
# la fiecare pas inlocuim primul neterminal cu o productie posibila
vizitat = set()
vizitat.add(tuple([start]))

coada = [[start]]
rezultate = set()

while coada:
    sir_curent = coada.pop(0)

    nr_terminale = sum(1 for s in sir_curent if s in terminale)
    nr_neterminale = sum(1 for s in sir_curent if s in neterminale)

    # daca avem deja mai multe terminale decat X, nu mai are rost sa continuam
    if nr_terminale > X:
        continue

    # daca nu mai avem neterminale verificam daca lungimea e exacta
    if nr_neterminale == 0:
        if len(sir_curent) == X:
            rezultate.add(tuple(sir_curent))
        continue

    # gasim primul neterminal si aplicam toate productiile posibile pentru el
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
    fout.write("NU EXISTA\n")
else:
    for cuvant in sorted(rezultate):
        fout.write("".join(cuvant) + "\n")

fin.close()
fout.close()
