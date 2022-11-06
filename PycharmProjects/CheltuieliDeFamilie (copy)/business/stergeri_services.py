from domain.cheltuiala import get_zi_cheltuiala, get_tip_cheltuiala


def sterge_cheltuieli_zi(lista, zi):
    '''
    sterge toate cheltuielile din ziua intreg zi
    :param lista: lista
    :param zi: integer
    :return: - (se sterg cheltuielile din ziua intreg zi)
    '''
    elemente_de_sters = {}
    for index in lista.keys():
        if get_zi_cheltuiala(lista[index]) == zi:
            elemente_de_sters[index] = lista[index]

    for index in elemente_de_sters.keys():
        if index in lista:
            del lista[index]


def sterge_cheltuieli_tip(lista, tip):
    '''
    sterge toate cheltuielile de tipul string tip
    :param lista: list
    :param tip: string
    :return: - (sterge toate cheltuielile de tipul string tip)
    '''
    elemente_de_sters = {}
    for index in lista.keys():
        if get_tip_cheltuiala(lista[index]) == tip:
            elemente_de_sters[index] = lista[index]

    for index in elemente_de_sters.keys():
        if index in lista:
            del lista[index]


def sterge_cheltuieli_perioada(lista, zi_inceput, zi_sfarsit):
    '''
    sterge toate cheltuielile din perioada delimitata de ziua intreaga zi_inceput si ziua intreaga zi_sfarsit
    :param lista: list
    :param zi_inceput: integer
    :param zi_sfarsit: integer
    :return: - (sterge toate cheltuielile din perioada delimitata de ziua intreaga zi_inceput si ziua intreaga zi_sfarsit)
    '''
    elemente_de_sters = {}
    for index in lista.keys():
        if get_zi_cheltuiala(lista[index]) >= zi_inceput and get_zi_cheltuiala(lista[index]) <= zi_sfarsit:
            elemente_de_sters[index] = lista[index]

    for index in elemente_de_sters.keys():
        if index in lista:
            del lista[index]
