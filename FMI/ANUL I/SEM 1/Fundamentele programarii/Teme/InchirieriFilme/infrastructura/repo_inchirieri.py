from erori.repo_error import RepoError


class RepoInchirieri:

    def __init__(self):
        self._inchirieri = {}

    def adauga_inchiriere(self, inchiriere):
        '''
        adauga in repository inchirierea inchiriere
        :param inchiriere: inchiriere
        :return: -
        :raises: RepoError daca id-ul inchirierii inchiriere este deja existent
        '''
        if inchiriere.get_id_inchiriere() in self._inchirieri:
            raise RepoError("Inchiriere existenta!")
        self._inchirieri[inchiriere.get_id_inchiriere()] = inchiriere

    def get_all(self):
        '''
        returneaza toate inchirerile din repository
        :return: toate inchirierile din repository
        '''
        inchirieri = []
        for id_inchiriere in self._inchirieri:
            inchirieri.append(self._inchirieri[id_inchiriere])
        return inchirieri

    def sterge_inchiriere_dupa_id(self, id_inchiriere):
        '''
        sterge din repository inchirierea cu id-ul intreg id_inchiriere
        :param id_inchiriere: intreg
        :return: - (sterge din repository inchirierea cu id-ul intreg id_inchiriere)
        :raises: RepoError daca id-ul id_inchiriere nu exista
        '''
        if id_inchiriere not in self._inchirieri:
            raise RepoError("Inchiriere inexistenta!")
        del self._inchirieri[id_inchiriere]

    def cauta_inchiriere_dupa_id(self, id_inchiriere):
        '''
        returneaza inchirierea cu id-ul intreg id_inchiriere
        :param id_inchiriere: intreg
        :return: inchirierea cu id-ul intreg id_inchiriere
        :raises: RepoError daca id-ul id_inchiriere nu exista
        '''
        if id_inchiriere not in self._inchirieri:
            raise RepoError("Inchiriere inexistenta!")
        return self._inchirieri[id_inchiriere]

    def modifica_inchiriere(self, inchiriere_modificata):
        '''
        modifica inchirierea cu id-ul intreg al inchirierii modificate inchiriere_modificata cu inchirierea
        inchiriere_modificata
        :param inchiriere_modificata: inchiriere
        :return: -
        :raises: RepoError daca id-ul inchirierii id_inchiriere nu exista
        '''
        if inchiriere_modificata.get_id_inchiriere() not in self._inchirieri:
            raise RepoError("Client inexistent!")
        self._inchirieri[inchiriere_modificata.get_id_inchiriere()] = inchiriere_modificata
