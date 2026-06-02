fin = open("ex2_input.txt", "r")
fout = open("ex2_output.txt", "w")

def citeste():
    return fin.readline().strip()

states = citeste().split()
alphabet = citeste().split()
n = int(citeste())

# tranzitiile sunt stocate ca tranz[src][dst] = expresie regulata
tranz = {}

for _ in range(n):
    linie = citeste().split()
    src = linie[0]
    dst = linie[1]
    sym = linie[2]

    # lambda il reprezentam ca sir vid
    if sym == "λ":
        sym = ""

    if src not in tranz:
        tranz[src] = {}
    if dst not in tranz[src]:
        tranz[src][dst] = sym
    else:
        # daca exista deja o tranzitie intre aceleasi stari, facem reuniunea lor
        tranz[src][dst] = "(" + tranz[src][dst] + "|" + sym + ")"

start = citeste()
finals = citeste().split()


# adaugam o stare initiala noua si o stare finala noua
nou_start = "S_NOU"
nou_final = "F_NOU"

if nou_start not in tranz:
    tranz[nou_start] = {}
tranz[nou_start][start] = ""

for f in finals:
    if f not in tranz:
        tranz[f] = {}
    if nou_final not in tranz[f]:
        tranz[f][nou_final] = ""
    else:
        tranz[f][nou_final] = "(" + tranz[f][nou_final] + "|)"

stari_de_eliminat = list(states)


# eliminam starea q si actualizam tranzitiile care treceau prin ea
def elimina_stare(tranz, q):
    predecesori = []
    for src in list(tranz.keys()):
        if src != q and q in tranz.get(src, {}):
            predecesori.append(src)

    succesori = [dst for dst in tranz.get(q, {}).keys() if dst != q]

    # verificam daca exista o bucla pe q
    bucla = tranz.get(q, {}).get(q, None)

    for i in predecesori:
        for j in succesori:
            r_iq = tranz[i][q]
            r_qj = tranz[q][j]

            if bucla is not None and bucla != "":
                mijloc = "(" + bucla + ")*"
                nou = r_iq + mijloc + r_qj
            else:
                nou = r_iq + r_qj

            # curatam concatenarile cu sirul vid
            def simplifica(expr):
                while "()" in expr:
                    expr = expr.replace("()", "")
                return expr

            nou = simplifica(nou)

            if j not in tranz[i]: #vreau sa elimin q intermediar
                tranz[i][j] = nou
            else:
                vechi = tranz[i][j]
                if vechi == nou:
                    pass
                elif vechi == "":
                    tranz[i][j] = "(" + nou + "|)"
                elif nou == "":
                    tranz[i][j] = "(" + vechi + "|)"
                else:
                    tranz[i][j] = "(" + vechi + "|" + nou + ")"

    if q in tranz:
        del tranz[q]
    for src in tranz:
        if q in tranz[src]:
            del tranz[src][q]


# eliminam pe rand fiecare stare originala
for q in stari_de_eliminat:
    elimina_stare(tranz, q)

# ce ramane intre starea initiala noua si cea finala noua e expresia regulata
rezultat = tranz.get(nou_start, {}).get(nou_final, "")

if rezultat == "":
    rezultat = "λ"

fout.write(rezultat + "\n")

fin.close()
fout.close()
