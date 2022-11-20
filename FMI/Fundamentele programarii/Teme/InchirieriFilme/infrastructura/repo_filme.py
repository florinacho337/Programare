from erori.repo_error import RepoError


class RepoFilme:

    def __init__(self):
        self.__filme = {}

    def adauga_film(self, film):
        '''
        adauga in repository filmul film
        :param film_adaugat: film
        :return: - (adauga in repository filmul film_adaugat)
        :raises: RepoError daca id-ul filmului film_adaugat este deja existent
        '''
        if film.get_id_film() in self.__filme:
            raise RepoError("Film existent!")
        self.__filme[film.get_id_film()] = film

    def sterge_film_dupa_id(self, id_film):
        '''
        sterge din repository filmul cu id-ul intreg id_film
        :param id_film: intreg
        :return: - (sterge din repository filmul cu id-ul intreg id_film)
        :raises: RepoError daca id-ul id_film nu exista
        '''
        if id_film not in self.__filme:
            raise RepoError("Film inexistent!")
        del self.__filme[id_film]

    def cauta_film_dupa_id(self, id_film):
        '''
        returneaza filmul cu id-ul intreg id_film
        :param id_film: intreg
        :return: filmul cu id-ul intreg id_film
        :raises: RepoError daca id-ul id_film nu exista
        '''
        if id_film not in self.__filme:
            raise RepoError("Film inexistent!")
        return self.__filme[id_film]

    def modifica_film(self, film):
        '''
        modifica filmul de pe id-ul intreg al filmului modificat film cu filmul modificat film
        :param film: film
        :return: - (modifica filmul de pe id-ul intreg al filmului modificat film cu filmul modificat film)
        :raises: RepoError daca id-ul id_film nu exista
        '''
        if film.get_id_film() not in self.__filme:
            raise RepoError("Film inexistent!")
        self.__filme[film.get_id_film()] = film

    def get_all(self):
        '''
        returneaza toate filmele din repository
        :return: toate filmele din repository
        '''
        filme = []
        for id_film in self.__filme:
            filme.append(self.__filme[id_film])
        return filme

    def __len__(self):
        '''
        returneaza numarul de filme din repository
        :return: numarul de filme din repository
        '''
        return len(self.__filme)



