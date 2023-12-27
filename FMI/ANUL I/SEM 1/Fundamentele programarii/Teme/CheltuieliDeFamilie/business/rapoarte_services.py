from domain.cheltuiala import get_tip_cheltuiala, get_suma_cheltuiala, get_zi_cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua


def suma_totala_tip_cheltuiala(lista, tip):
    '''
    returneaza suma totala float pentru tipul string tip de cheltuiala
    :param lista: list
    :param tip: string
    :return: suma totala float pentru tipul string tip de cheltuiala
    '''
    suma = 0
    for cheltuiala in lista:
        if get_tip_cheltuiala(cheltuiala) == tip:
            suma = suma + get_suma_cheltuiala(cheltuiala)
    return suma


def zi_suma_maxima(lista):
    '''
    returneaza ziua intreg zi pentru cheltuiala cu suma float suma maxima
    :param lista: list
    :return: ziua in care suma cheltuita este maxima
    '''
    sum_max = 0
    zi = 0
    for cheltuiala in lista:
        if get_suma_cheltuiala(cheltuiala) > sum_max:
            sum_max = get_suma_cheltuiala(cheltuiala)
            zi = get_zi_cheltuiala(cheltuiala)
    return zi


def cheltuieli_de_suma(lista, suma):
    '''
    returneaza toate cheltuielile cheltuieli care au suma float suma
    :param lista: list
    :param suma: float
    :return: toate cheltuielile cheltuieli care au suma float suma
    '''
    rezultat = []
    for cheltuiala in lista:
        if abs(get_suma_cheltuiala(cheltuiala) - suma) < 0.00001:
            adauga_cheltuiala_noua(rezultat, cheltuiala)
    return rezultat
