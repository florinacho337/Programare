from infrastructura.repository_cheltuieli import get_cheltuieli


def afiseaza_cheltuieli(lista):
    '''
    returneaza cheltuielile din lista lista
    :param lista: list
    :return: cheltuielile din lista lista
    '''
    cheltuieli = get_cheltuieli(lista)
    return cheltuieli
