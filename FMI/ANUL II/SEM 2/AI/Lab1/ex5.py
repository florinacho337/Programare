# ex5 - Pentru un șir cu n elemente care conține valori din mulțimea {1, 2, ..., n - 1} astfel încât o singură
# valoare se repetă de două ori, să se identifice acea valoare care se repetă. De ex. în șirul [1,2,3,4,2] valoarea 2
# apare de două ori.
# valoare_duplicata(vector)
# vector - vector de numere
# returns: valoarea care apare de doua ori, daca exista o astfel de valoare
#          False, altfel
def valoare_duplicata(vector):
    # se numara aparitiile numerelor si se salveaza intr-un dictionar ale caror chei sunt numerele
    aparitii_numere = {}
    for nr in vector:
        if nr in aparitii_numere:
            aparitii_numere[nr] += 1
        else:
            aparitii_numere[nr] = 1
    # se returneaza numarul care apare de 2 ori
    for c in aparitii_numere:
        if aparitii_numere[c] == 2:
            return c
    # daca nu exista un astfel de numar, se returneaza False
    return False


# solutie generata de AI
def valoare_duplicata_ai(sir):
    # Calculăm XOR-ul tuturor numerelor din șir
    xor_sir = 0
    for numar in sir:
        xor_sir ^= numar

    # Calculăm XOR-ul tuturor numerelor de la 1 la n - 1
    xor_toate = 0
    for i in range(1, len(sir)):
        xor_toate ^= i

    # Valoarea care se repetă de două ori este rezultatul XOR între cele două XOR-uri
    valoare_repetata = xor_sir ^ xor_toate

    # Verificăm dacă valoarea repetată este validă
    if valoare_repetata in sir and sir.count(valoare_repetata) == 2:
        return valoare_repetata
    else:
        return False
