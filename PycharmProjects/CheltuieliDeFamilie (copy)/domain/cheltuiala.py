def cheltuiala(ziua, suma, tip):
    '''
    creeaza o cheltuiala din ziua intreg ziua, cu suma float suma, de tipul string tip
    :param ziua: integer
    :param suma: float
    :param tip: string
    :return: o cheltuiala din ziua intreg ziua, cu suma float suma, de tipul string tip
    '''
    #return [ziua, suma, tip]
    return [ziua, suma, tip]


def get_zi_cheltuiala(cheltuiala):
    '''
    obtine ziua intreaga zi a cheltuielii cheltuiala
    :param cheltuiala: cheltuiala
    :return: ziua intreaga zi a cheltuielii cheltuiala
    '''
    return cheltuiala[0]


def get_suma_cheltuiala(cheltuiala):
    '''
    obtine suma float suma a cheltuielii cheltuiala
    :param cheltuiala: cheltuiala
    :return: suma float suma a cheltuielii cheltuiala
    '''
    return cheltuiala[1]


def get_tip_cheltuiala(cheltuiala):
    '''
    obtine tipul string tip a cheltuielii cheltuiala
    :param cheltuiala: cheltuiala
    :return: tipul string tip a cheltuielii cheltuiala
    '''
    return cheltuiala[2]


def set_zi_cheltuiala(cheltuiala, zi_noua):
    '''
    modifica ziua intreaga a cheltuielii cheltuiala cu valoarea intreaga din zi_noua
    :param cheltuiala: cheltuiala
    :param zi_noua: integer
    :return: - (se modifica ziua intreaga a cheltuielii cheltuiala cu valoarea intreaga din zi_noua)
    '''
    cheltuiala[0] = zi_noua


def set_suma_cheltuiala(cheltuiala, suma_noua):
    '''
    modifica suma float a cheltuielii cheltuiala cu valoarea float din suma_noua
    :param cheltuiala: cheltuiala
    :param suma_noua: float
    :return: - (se modifica suma float a cheltuielii cheltuiala cu valoarea float din suma_noua)
    '''
    cheltuiala[1] = suma_noua


def set_tip_cheltuiala(cheltuiala, tip_nou):
    '''
    modifica tipul string a cheltuielii cheltuiala cu stringul tip_nou
    :param cheltuiala: cheltuiala
    :param tip_nou: string
    :return: - (se modifica tipul string a cheltuielii cheltuiala cu stringul tip_nou)
    '''
    cheltuiala[2] = tip_nou
