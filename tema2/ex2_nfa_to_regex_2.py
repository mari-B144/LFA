states = input().split()
alphabet = input().split()
n = int(input())

tranz = {}

for _ in range(n):
    linie = input().split()
    src = linie[0]
    dst = linie[1]
    sym = linie[2]

    if sym == "λ":
        sym = ""

    if src not in tranz:
        tranz[src] = {}
    if dst not in tranz[src]:
        tranz[src][dst] = sym
    else:
        tranz[src][dst] = "(" + tranz[src][dst] + "|" + sym + ")"

start = input().strip()
finals = input().split()

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

stari_intermediare = [s for s in states if s != start or True]
stari_de_eliminat = list(states)

def elimina_stare(tranz, q):
    predecesori = []
    for src in list(tranz.keys()):
        if src != q and q in tranz.get(src, {}):
            predecesori.append(src)

    succesori = list(tranz.get(q, {}).keys())
    succesori = [dst for dst in succesori if dst != q]

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

            def simplifica(expr):
                while "()" in expr:
                    expr = expr.replace("()", "")
                return expr

            nou = simplifica(nou)

            if j not in tranz[i]:
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

for q in stari_de_eliminat:
    elimina_stare(tranz, q)

rezultat = tranz.get(nou_start, {}).get(nou_final, "")

if rezultat == "":
    rezultat = "λ"

print(rezultat)
