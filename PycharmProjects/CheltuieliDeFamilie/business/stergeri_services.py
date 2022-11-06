from domain.cheltuiala import get_zi_cheltuiala, get_tip_cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua


def sterge_cheltuieli_zi(lista, undolist, zi):
    '''
    sterge toate cheltuielile din ziua intreg zi
    :param lista: list
    :param undolist: list
    :param zi: integer
    :return: - (se sterg cheltuielile din ziua intreg zi)
    '''
    lista_actualizata = []
    for cheltuiala in lista:
        if not(get_zi_cheltuiala(cheltuiala) == zi):
            adauga_cheltuiala_noua(lista_actualizata, cheltuiala)
    undolist.append(lista[:])
    lista[:] = lista_actualizata


def sterge_cheltuieli_tip(lista, undolist, tip):
    '''
    sterge toate cheltuielile de tipul string tip
    :param lista: list
    :param undolist: list
    :param tip: string
    :return: - (sterge toate cheltuielile de tipul string tip)
    '''
    lista_actualizata = []
    for cheltuiala in lista:
        if not(get_tip_cheltuiala(cheltuiala) == tip):
            adauga_cheltuiala_noua(lista_actualizata, cheltuiala)
    undolist.append(lista[:])
    lista[:] = lista_actualizata


def sterge_cheltuieli_perioada(lista, undolist, zi_inceput, zi_sfarsit):
    '''
    sterge toate cheltuielile din perioada delimitata de ziua intreaga zi_inceput si ziua intreaga zi_sfarsit
    :param lista: list
    :param undolist: list
    :param zi_inceput: integer
    :param zi_sfarsit: integer
    :return: - (sterge toate cheltuielile din perioada delimitata de ziua intreaga zi_inceput si ziua intreaga zi_sfarsit)
    '''
    lista_actualizata = []
    for cheltuiala in lista:
        if get_zi_cheltuiala(cheltuiala) < zi_inceput or get_zi_cheltuiala(cheltuiala) > zi_sfarsit:
            adauga_cheltuiala_noua(lista_actualizata, cheltuiala)
    undolist.append(lista[:])
    lista[:] = lista_actualizata
