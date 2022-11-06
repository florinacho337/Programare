from domain.cheltuiala import cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua
from validare.validator_cheltuiala import valideaza_cheltuiala


def adauga_cheltuiala_service(l, zi, suma, tip):
    '''
    pe baza zilei intregi zi, a sumei float suma si a tipului string tip, va crea o cheltuiala,
    va incerca sa o valideze, apoi daca e valida, o va adauga in lista de cheltuieli l
    :param l: list
    :param zi: integer
    :param suma: float
    :param tip: string
    :return: - (daca cheltuiala ete valida)
    :raises: ValueError daca cel putin o data din player este gresita:
                        daca ziua < 1 sau ziua > 31 -> "Zi invalida!\n"
                        daca suma <= 0 -> "Suma invalida!\n"
                        daca tip nu apartine ["mancare", "intretinere", "imbracaminte", "telefon", "altele"] -> "Tip de cheltuiala invalid!\n"
    '''
    cheltuiala_noua = cheltuiala(zi, suma, tip)
    valideaza_cheltuiala(cheltuiala_noua)
    adauga_cheltuiala_noua(l, cheltuiala_noua)