from domain.cheltuiala import cheltuiala, set_zi_cheltuiala, set_tip_cheltuiala, set_suma_cheltuiala
from validare.validator_cheltuiala import valideaza_cheltuiala


def adauga_cheltuiala_noua(lst, cheltuiala):
    '''
    adauga in lista de cheltuieli o cheltuiala de tip cheltuiala
    :param lst: list
    :param cheltuiala: cheltuiala
    :return: - (adauga in lista de cheltuieli o noua cheltuiala)
    '''
    lst.append(cheltuiala)


def actualizeaza_cheltuiala(lst, pozitie, zi_noua, suma_noua, tip_nou):
    '''
    actualizeaza cheltuiala cheltuiala de pe pozitita intreg pozitie schimband ziua cu valoarea intreaga
    din zi_noua, suma cu valoarea float suma_noua si tipul cu stringul tip_nou
    :param lst: list
    :param pozitie: integer
    :param zi_noua: integer
    :param suma_noua: float
    :param tip_nou: string
    :return: - (actualizeaza cheltuiala cheltuiala de pe pozitita intreg pozitie schimband ziua cu valoarea intreaga
    din zi_noua, suma cu valoarea float suma_noua si tipul cu stringul tip_nou)
    :raises: ValueError daca cel putin o data din player este gresita:
                        daca ziua < 1 sau ziua > 31 -> "Zi invalida!\n"
                        daca suma <= 0 -> "Suma invalida!\n"
                        daca tip nu apartine ["mancare", "intretinere", "imbracaminte", "telefon", "altele"] -> "Tip de cheltuiala invalid!\n"
                        sau
                        daca pozititia intreaga pozitie este inexistenta:
                        daca pozitie < 1 sau pozitie > lungimea listei -> "Pozitie inexistenta!\n"
    '''
    errors = ""
    cheltuiala_noua = cheltuiala(zi_noua, suma_noua, tip_nou)
    valideaza_cheltuiala(cheltuiala_noua)
    if pozitie < 1 or pozitie > get_lungime_lista(lst):
        errors += "Pozitie inexistenta!\n"
    if len(errors) > 0:
        raise ValueError(errors)
    else:
        cheltuiala_noua[:] = lst[pozitie-1]
        set_zi_cheltuiala(cheltuiala_noua, zi_noua)
        set_suma_cheltuiala(cheltuiala_noua, suma_noua)
        set_tip_cheltuiala(cheltuiala_noua, tip_nou)
        lst[pozitie-1] = cheltuiala_noua



def get_cheltuieli(lst):
    '''
    returneaza lista cu toate cheltuielile
    :param lst: list
    :return: lista de cheltuieli
    '''
    return lst


def get_lungime_lista(lst):
    '''
    returneaza lungimea listei de cheltuieli
    :param lst: list
    :return: lungimea listei de cheltuieli
    '''
    return len(lst)
