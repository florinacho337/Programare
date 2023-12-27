def adauga_cheltuiala_noua(lst, cheltuiala):
    '''
    adauga in lista de cheltuieli o cheltuiala de tip cheltuiala
    :param lst: dictionary
    :param cheltuiala: cheltuiala
    :return: - (adauga in lista de cheltuieli o noua cheltuiala)
    '''
    cnt = 1
    while cnt in lst.keys():
        cnt = cnt + 1
    lst[cnt] = cheltuiala


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
