from domain.cheltuiala import get_tip_cheltuiala, get_suma_cheltuiala, get_zi_cheltuiala


def suma_totala_tip_cheltuiala(lista, tip):
    '''
    tipareste suma totala float pentru tipul string tip de cheltuiala
    :param lista: list
    :param tip: string
    :return: suma totala float pentru tipul string tip de cheltuiala
    '''
    suma = 0
    for index in lista:
        if get_tip_cheltuiala(lista[index]) == tip:
            suma = suma + get_suma_cheltuiala(lista[index])
    return suma


def zi_suma_maxima(lista):
    '''
    tipareste ziua intreg zi pentru cheltuiala cu suma float suma maxima
    :param lista: list
    :return: ziua in care suma cheltuita este maxima
    '''
    sum_max = 0
    zi = 0
    for index in lista:
        if get_suma_cheltuiala(lista[index]) > sum_max:
            sum_max = get_suma_cheltuiala(lista[index])
            zi = get_zi_cheltuiala(lista[index])
    return zi