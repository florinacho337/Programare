# ex4 - Să se determine cuvintele unui text care apar exact o singură dată în acel text. De ex. cuvintele care apar o
# singură dată în ”ana are ana are mere rosii ana" sunt: 'mere' și 'rosii'.
# cuvinte_o_data(propozitie)
# propozitie - sir de caractere
# returns: un vector care contine cuvintele care apar o singura data in propozitia propozitie
def cuvinte_o_data(propozitie):
    # se elimina spatiile de la inceputul si finalul propozitiei
    propozitie = propozitie.strip()
    # se salveaza cuvintele intr-un vector
    cuvinte = propozitie.split()
    # se numara aparitiile cuvintelor si se salveaza intr-un dictionar ale caror chei sunt cuvintele
    aparitii_cuvinte = {}
    for cuv in cuvinte:
        if cuv in aparitii_cuvinte:
            aparitii_cuvinte[cuv] += 1
        else:
            aparitii_cuvinte[cuv] = 1
    # se returneaza doar cuvintele care apar o singura data
    return [c for c in aparitii_cuvinte if aparitii_cuvinte[c] == 1]


# solutie generata de AI
def cuvinte_o_data_ai(text):
    aparitii_cuvinte = {}

    # Separăm textul în cuvinte
    cuvinte = text.split()

    # Numărăm de câte ori apare fiecare cuvânt în text
    for cuvant in cuvinte:
        if cuvant in aparitii_cuvinte:
            aparitii_cuvinte[cuvant] += 1
        else:
            aparitii_cuvinte[cuvant] = 1

    # Selectăm cuvintele care apar o singură dată
    cuvinte_aparitie_unica = [cuvant for cuvant, frecventa in aparitii_cuvinte.items() if frecventa == 1]

    return cuvinte_aparitie_unica
