from domeniu.inchiriere_film import InchiriereFilm
from domeniu.top_clienti_dto import TopClientiDTO
from domeniu.top_filme_dto import TopFilmeDTO


class ServiceInchiriere:

    def __init__(self, validator_inchiriere, repo_inchirieri, repo_clienti, repo_filme):
        self.__validator_inchiriere = validator_inchiriere
        self.__repo_inchirieri = repo_inchirieri
        self.__repo_clienti = repo_clienti
        self.__repo_filme = repo_filme

    def sterge_client_si_inchirieri(self, id_client):
        '''
        cauta un client, apoi sterge fiecare inchiriere facuta de acesta si pe acesta
        :param id_client: intreg
        :return: -
        :raises: RepoError daca id-ul clientului este inexistent
        '''
        client = self.__repo_clienti.cauta_client_dupa_id(id_client)
        inchirieri = self.__repo_inchirieri.get_all()
        inchirieri_client = [x for x in inchirieri if self.__repo_clienti.cauta_client_dupa_id(x.get_id_client()) == client]
        for inchiriere_client in inchirieri_client:
            self.__repo_inchirieri.sterge_inchiriere_dupa_id(inchiriere_client.get_id_inchiriere())
        self.__repo_clienti.sterge_client_dupa_id(id_client)

    def sterge_film_si_inchirieri(self, id_film):
        '''
        caut un film, apoi sterge fiecare inchiriere a filmului apoi filmul
        :param id_film: intreg
        :return: -
        :raises: RepoError daca id-ul filmului nu exista

        '''
        film = self.__repo_filme.cauta_film_dupa_id(id_film)
        inchirieri = self.__repo_inchirieri.get_all()
        inchirieri_film = [x for x in inchirieri if self.__repo_filme.cauta_film_dupa_id(x.get_id_film()) == film]
        for inchiriere_film in inchirieri_film:
            self.__repo_inchirieri.sterge_inchiriere_dupa_id(inchiriere_film.get_id_inchiriere())
        self.__repo_filme.sterge_film_dupa_id(id_film)

    def adauga_inchiriere(self, id_inchiriere, id_client, id_film):
        '''
        creeaza o inchiriere cu id-ul id_inchiriere intre clientul cu id-ul id_client si
        filmul cu id-ul id_film, incearca sa o valideze si incearca sa o adauge in repository
        :param id_inchiriere: intreg
        :param id_client: intreg
        :param id_film: intreg
        :return: -
        :raises: ValidationError daca id-ul este invalid
                                 daca id_inchiriere < 0 -> "Id invalid!"
                 RepoError daca id-ul inchirierii inchiriere este deja existent
                           daca id-ul id_client este inexistent
                           daca id-ul id_film nu exista
        '''
        inchiriere = InchiriereFilm(id_inchiriere, id_client, id_film)
        self.__validator_inchiriere.valideaza(inchiriere)
        self.__repo_inchirieri.adauga_inchiriere(inchiriere)

    def get_all(self):
        '''
        returneaza toate inchirierile din repository
        :return: toate inchirierile din repository
        '''
        return self.__repo_inchirieri.get_all()

    def sterge_inchirierea_cu_id(self, id_inchiriere):
        '''
        sterge inchirierea cu id-ul intreg id_inchiriere
        :param id_inchiriere: intreg
        :return: -
        :raises: RepoError daca id-ul id_inchiriere nu exista
        '''
        self.__repo_inchirieri.sterge_inchiriere_dupa_id(id_inchiriere)

    def gaseste_inchiriere(self, id_inchiriere):
        '''
        returneaza inchirierea cu id-ul intreg id_inchiriere
        :param id_inchiriere: intreg
        :return: inchirierea cu id-ul intreg id_inchiriere
        :raises: RepoError daca id-ul inchirierii id_inchiriere nu exista
        '''
        return self.__repo_inchirieri.cauta_inchiriere_dupa_id(id_inchiriere)

    def get_top_clienti(self):
        '''
        returneaza topul clientilor dupa numarul de filme inchiriate
        :return: topul clientilor dupa numarul de filme inchiriate
        '''
        info_clienti = {}
        inchirieri = self.__repo_inchirieri.get_all()
        for inchiriere in inchirieri:
            id_client_inchiriere = inchiriere.get_id_client()
            if id_client_inchiriere not in info_clienti:
                info_clienti[id_client_inchiriere] = 0
            info_clienti[id_client_inchiriere] += 1
        clienti = self.__repo_clienti.get_all()
        for client in clienti:
            id_client = client.get_id_client()
            if id_client not in info_clienti:
                info_clienti[id_client] = 0
        top_clienti = []
        for id_client in info_clienti:
            client = self.__repo_clienti.cauta_client_dupa_id(id_client)
            nume_client = client.get_nume_client()
            nr_filme = info_clienti[id_client]
            top_client_dto = TopClientiDTO(nume_client, nr_filme)
            top_clienti.append(top_client_dto)
        self.__insertion_sort(top_clienti, reverse=True)
        return top_clienti

    def get_top_30_clienti(self):
        '''
        returneaza topul celor mai activi 30% clienti
        :return: topul celor mai activi 30% clienti
        '''
        info_clienti = {}
        inchirieri = self.__repo_inchirieri.get_all()
        for inchiriere in inchirieri:
            id_client_inchiriere = inchiriere.get_id_client()
            if id_client_inchiriere not in info_clienti:
                info_clienti[id_client_inchiriere] = 0
            info_clienti[id_client_inchiriere] += 1
        top_clienti = []
        for id_client in info_clienti:
            client = self.__repo_clienti.cauta_client_dupa_id(id_client)
            nume_client = client.get_nume_client()
            nr_filme = info_clienti[id_client]
            top_client_dto = TopClientiDTO(nume_client, nr_filme)
            top_clienti.append(top_client_dto)
        self.__insertion_sort(top_clienti, reverse=True)
        top_30 = int(0.3 * len(self.__repo_clienti.get_all()))
        return top_clienti[:top_30]

    def get_top_filme(self):
        '''
        returneaza primele 3 cele mai inchiriate filme
        :return: primele 3 cele mai inchiriate filme
        '''
        info_filme = {}
        inchirieri = self.__repo_inchirieri.get_all()
        for inchiriere in inchirieri:
            id_film_inchiriere = inchiriere.get_id_film()
            if id_film_inchiriere not in info_filme:
                info_filme[id_film_inchiriere] = 0
            info_filme[id_film_inchiriere] += 1
        top_filme = []
        for id_film in info_filme:
            film = self.__repo_filme.cauta_film_dupa_id(id_film)
            titlu_film = film.get_titlu_film()
            nr_inchirieri = info_filme[id_film]
            top_film_dto = TopFilmeDTO(titlu_film, nr_inchirieri)
            top_filme.append(top_film_dto)
        self.__comb_sort(top_filme, reverse=True)
        return top_filme[:3]

    def get_clienti_ale_caror_nume_incep_cu_litera(self, litera):
        info_clienti = {}
        inchirieri = self.__repo_inchirieri.get_all()
        for inchiriere in inchirieri:
            id_client_inchiriere = inchiriere.get_id_client()
            titlu_film = self.__repo_filme.cauta_film_dupa_id(inchiriere.get_id_film()).get_titlu_film()
            id_film = inchiriere.get_id_film()
            if titlu_film[0] == litera and id_client_inchiriere not in info_clienti:
                info_clienti[id_client_inchiriere] = id_film
        clienti = []
        for id_client in info_clienti:
            client = self.__repo_clienti.cauta_client_dupa_id(id_client)
            clienti.append(client)
        return clienti

    def __insertion_sort(self, lista, key = None, reverse = False):
        # complexity: best case: O(n), unde n este numarul de elemente din lista. Acest caz
        # apare atunci cand elementele listei sunt deja sortate crescator
        #              worst case: O(n2), unde n este nr de elemente din lista. Acest caz
        # apare atunci cand elementele listei sunt sortate descrescator.
        #              average case: O(n2), unde n este nr de elemente din lista.
        if key is None:
            key = lambda x: x

        for i in range(1, len(lista)):
            ind = i - 1
            a = lista[i]
            while ind >= 0 and key(a) < key(lista[ind]):
                lista[ind + 1] = lista[ind]
                ind = ind - 1
            lista[ind+1] = a

        if reverse:
            lista.reverse()
        return lista

    def __comb_sort(self, lista, key = None, reverse = False):
        if key is None:
            key = lambda x: x

        gap = len(lista)
        shrink_factor = 1.3
        sort = False

        while not sort:
            gap = int(gap / shrink_factor)
            if gap <= 1:
                gap = 1
                sort = True

        for i in range(len(lista) - gap):
            sm = gap + i
            if key(lista[i]) > key(lista[sm]):
                lista[i], lista[sm] = lista[sm], lista[i]
                sort = False

        if reverse:
            lista.reverse()

        return lista

