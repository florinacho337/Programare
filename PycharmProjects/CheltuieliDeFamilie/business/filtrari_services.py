from domain.cheltuiala import get_suma_cheltuiala, get_tip_cheltuiala
from infrastructura.repository_cheltuieli import adauga_cheltuiala_noua


def elimina_cheltuieli_tip(lista, tip):
    '''
    se elimina din lista lista cheltuielile cheltuieli de tipul string tip si se returneaza cheltuielile
    ramase
    :param lista: list
    :param tip: string
    :return: lista noua fara cheltuielile cheltuieli de tipul string tip
    '''
    lista_noua = []
    for cheltuiala in lista:
        if not(get_tip_cheltuiala(cheltuiala) == tip):
            adauga_cheltuiala_noua(lista_noua, cheltuiala)
    return lista_noua


def elimina_cheltuieli_mai_mici_decat(lista, suma):
    '''
    se elimina din lista lista cheltuielile cheltuieli care sunt mai mici decat valoarea intreaga suma,
    apoi se returneaza cheltuielile ramase
    :param lista: list
    :param suma: integer
    :return: cheltuielile ramase dupa eliminarea tuturor cheltuielilor cheltuieli mai mici decat valoarea
    intreaga suma
    '''
    lista_noua = []
    for cheltuiala in lista:
        if get_suma_cheltuiala(cheltuiala) >= suma:
            adauga_cheltuiala_noua(lista_noua, cheltuiala)
    return lista_noua
