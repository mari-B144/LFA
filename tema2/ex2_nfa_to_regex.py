# Exercitiul 2: Transformare λ-NFA → Expresie Regulata
# Metoda: eliminarea starilor intermediare (State Elimination)
# Adaugam o stare initiala noua si o stare finala noua,
# apoi eliminam starile intermediare una cate una,
# actualizand etichetele tranzitiilor cu expresii regulate.

# ---- Citire input ----

states = input().split()
alphabet = input().split()
n = int(input())

# Stocam tranzitiile ca un dictionar de dictionare
# tranz[src][dst] = expresie regulata (sir de caractere)
tranz = {}

for _ in range(n):
    linie = input().split()
    src = linie[0]
    dst = linie[1]
    sym = linie[2]

    if sym == "λ":
        sym = ""  # λ = sirul vid, in expresii regulate il reprezentam ca ""

    if src not in tranz:
        tranz[src] = {}
    if dst not in tranz[src]:
        tranz[src][dst] = sym
    else:
        # Daca exista deja o tranzitie intre aceleasi stari, facem reuniune
        tranz[src][dst] = "(" + tranz[src][dst] + "|" + sym + ")"

start = input().strip()
finals = input().split()


# ---- Adaugam stare initiala noua si stare finala noua ----
# Asta simplifica eliminarea: vom avea un singur start si un singur final

nou_start = "S_NOU"
nou_final = "F_NOU"

# Tranzitie λ (vida) de la start nou la startul original
if nou_start not in tranz:
    tranz[nou_start] = {}
tranz[nou_start][start] = ""  # "" = λ

# Tranzitii λ de la fiecare stare finala originala la finalul nou
for f in finals:
    if f not in tranz:
        tranz[f] = {}
    if nou_final not in tranz[f]:
        tranz[f][nou_final] = ""
    else:
        tranz[f][nou_final] = "(" + tranz[f][nou_final] + "|)"

# Lista tuturor starilor (fara start nou si final nou - acestea nu se elimina)
stari_intermediare = [s for s in states if s != start or True]
# De fapt eliminam toate starile originale (nu nou_start si nu nou_final)
stari_de_eliminat = list(states)


# ---- Functie de eliminare a unei stari intermediare ----
# Cand eliminam starea 'q':
# Pentru fiecare pereche (i, j) unde i→q si q→j exista:
#   Adaugam/actualizam tranzitia i→j cu: R(i,q) · R(q,q)* · R(q,j)
#   unde R(q,q) este bucla pe q (daca exista)

def elimina_stare(tranz, q):
    # Gasim toate starile care au tranzitie spre q
    predecesori = []
    for src in list(tranz.keys()):
        if src != q and q in tranz.get(src, {}):
            predecesori.append(src)

    # Gasim toate starile spre care q are tranzitie
    succesori = list(tranz.get(q, {}).keys())
    succesori = [dst for dst in succesori if dst != q]

    # Bucla pe q (tranzitia q→q daca exista)
    bucla = tranz.get(q, {}).get(q, None)

    for i in predecesori:
        for j in succesori:
            r_iq = tranz[i][q]   # expresia de la i la q
            r_qj = tranz[q][j]   # expresia de la q la j

            # Construim noua expresie: r_iq · bucla* · r_qj
            if bucla is not None and bucla != "":
                mijloc = "(" + bucla + ")*"
                nou = r_iq + mijloc + r_qj
            else:
                nou = r_iq + r_qj

            # Curatam concatenarile cu sirul vid
            # (daca o parte e "", nu o mai scriem)
            # Simplificare de baza
            def simplifica(expr):
                # Inlocuim "" (lambda) in concatenari
                while "()" in expr:
                    expr = expr.replace("()", "")
                return expr

            nou = simplifica(nou)

            # Actualizam sau adaugam tranzitia i→j
            if j not in tranz[i]:
                tranz[i][j] = nou
            else:
                # Reuniune cu ce exista deja
                vechi = tranz[i][j]
                if vechi == nou:
                    pass
                elif vechi == "":
                    tranz[i][j] = "(" + nou + "|)"  # nou sau lambda
                elif nou == "":
                    tranz[i][j] = "(" + vechi + "|)"
                else:
                    tranz[i][j] = "(" + vechi + "|" + nou + ")"

    # Stergem starea q din toate tranzitiile
    if q in tranz:
        del tranz[q]
    for src in tranz:
        if q in tranz[src]:
            del tranz[src][q]


# ---- Eliminam toate starile intermediare ----
for q in stari_de_eliminat:
    elimina_stare(tranz, q)


# ---- Rezultatul este tranzitia de la S_NOU la F_NOU ----
rezultat = tranz.get(nou_start, {}).get(nou_final, "")

# Daca e gol, inseamna ca limbajul accepta doar sirul vid
if rezultat == "":
    rezultat = "λ"

print(rezultat)
