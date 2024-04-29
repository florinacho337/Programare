# ex1 - Să se determine ultimul (din punct de vedere alfabetic) cuvânt care poate apărea într-un text care conține
# mai multe cuvinte separate prin ” ” (spațiu). De ex. ultimul (dpdv alfabetic) cuvânt din ”Ana are mere rosii si
# galbene” este cuvântul "si".
# ultimul_cuvant(propozitie)
# propozitie - sir de caractere
# returns: un string ce reprezinta ultimul cuvant din punct de vedere alfabetic din string-ul propozitie
def ultimul_cuvant(propozitie):
    # se ia un string vid care se compara cu fiecare string din propozitie
    cuv = ""
    # se salveaza intr-un vector cuvintele dintr-o propozitie
    cuvinte = propozitie.strip().split()
    # se parcurg cuvintele si se compara cu string-ul maxim gasit
    for c in cuvinte:
        if c > cuv:
            cuv = c
    # returneaza cuvantul maxim gasit
    return cuv


# solutie generata de AI:
def ultimul_cuvant_ai(text):
    cuvinte = text.split()

    ultimul_cuvant1 = ""
    for cuvant in cuvinte:
        if cuvant > ultimul_cuvant1:
            ultimul_cuvant1 = cuvant

    return ultimul_cuvant1
