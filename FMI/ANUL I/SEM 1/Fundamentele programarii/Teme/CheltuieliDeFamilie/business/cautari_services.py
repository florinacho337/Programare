from domain.cheltuiala import get_suma_cheltuiala, get_zi_cheltuiala, get_tip_cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua


def cheltuieli_mai_mari_decat_suma(lista, suma):
    '''
    tipareste toate cheltuielile mai mari decat suma float suma
    :param lista: list
    :param suma: float
    :return: toate cheltuielile mai mari decat suma float suma
    '''
    rezultat = []
    for cheltuiala in lista:
        if get_suma_cheltuiala(cheltuiala) > suma:
            adauga_cheltuiala_noua(rezultat, cheltuiala)
    return rezultat


def cheltuieli_inainte_de_ziua_si_mai_mici_decat_suma(lista, ziua, suma):
    '''
    tipareste toate cheltuielile efectuate inainte de ziua intreg ziua si mai mici decat suma float suma
    :param lista: list
    :param ziua: integer
    :param suma: float
    :return: toate cheltuielile efectuate inainte de ziua intreg ziua si mai mici decat suma float suma
    '''
    rezultat = []
    for cheltuiala in lista:
        if get_zi_cheltuiala(cheltuiala) < ziua and get_suma_cheltuiala(cheltuiala) < suma:
            adauga_cheltuiala_noua(rezultat, cheltuiala)
    return rezultat


def cheltuieli_de_tip(lista, tip):
    '''
    tipareste toate cheltuielile de tipul string tip
    :param lista: list
    :param tip: string
    :return: toate cheltuielile de tipul string tip
    '''
    rezultat = []
    for cheltuiala in lista:
        if get_tip_cheltuiala(cheltuiala) == tip:
            adauga_cheltuiala_noua(rezultat, cheltuiala)
    return rezultat
