from domain.cheltuiala import cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua, actualizeaza_cheltuiala
from validare.validator_cheltuiala import valideaza_cheltuiala


def adauga_cheltuiala_service(l, undolist, zi, suma, tip):
    '''
    pe baza zilei intregi zi, a sumei float suma si a tipului string tip, va crea o cheltuiala,
    va incerca sa o valideze, apoi daca e valida, o va adauga in lista de cheltuieli l
    :param l: list
    :param undolist: list
    :param zi: integer
    :param suma: float
    :param tip: string
    :return: - (daca cheltuiala este valida)
    :raises: ValueError daca cel putin o data din player este gresita:
                        daca ziua < 1 sau ziua > 31 -> "Zi invalida!\n"
                        daca suma <= 0 -> "Suma invalida!\n"
                        daca tip nu apartine ["mancare", "intretinere", "imbracaminte", "telefon", "altele"] -> "Tip de cheltuiala invalid!\n"
    '''
    undolist.append(l[:])
    cheltuiala_noua = cheltuiala(zi, suma, tip)
    valideaza_cheltuiala(cheltuiala_noua)
    adauga_cheltuiala_noua(l, cheltuiala_noua)


def actualizeaza_cheltuiala_service(l, undolist, pozitie, zi_noua, suma_noua, tip_nou):
    '''
    pe baza zilei intregi zi_noua, a sumei float suma_noua si a tipului string tip_nou, va crea
    o cheltuiala, va incerca sa o valideze, apoi daca e valida, o va adauga in lista de cheltuieli
    lst, pe pozitia intreaga pozitie
    :param l: list
    :param undolist: list
    :param pozitie: integer
    :param zi_noua: integer
    :param suma_noua: float
    :param tip_nou: sstring
    :return: - (daca cheltuiala este valida)
    :raises: ValueError daca pozititia intreaga pozitie este inexistenta:
                        daca pozitie < 1 sau pozitie > lungimea listei -> "Pozitie inexistenta!\n"
                        sau
                        daca cel putin o data din player este gresita:
                        daca ziua < 1 sau ziua > 31 -> "Zi invalida!\n"
                        daca suma <= 0 -> "Suma invalida!\n"
                        daca tip nu apartine ["mancare", "intretinere", "imbracaminte", "telefon", "altele"] -> "Tip de cheltuiala invalid!\n"
    '''
    undolist.append(l[:])
    actualizeaza_cheltuiala(l, pozitie, zi_noua, suma_noua, tip_nou)
