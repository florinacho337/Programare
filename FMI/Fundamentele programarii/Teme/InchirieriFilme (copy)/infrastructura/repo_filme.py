from erori.repo_error import RepoError


class RepoFilme:

    def __init__(self):
        self.__filme = []

    def adauga_film(self, film_adaugat):
        id_film = film_adaugat.get_id_film()
        for film in self.__filme:
            if id_film == film.get_id_film():
                raise RepoError("Film existent!")
        self.__filme.append(film_adaugat)

    def sterge_film_dupa_id(self, id_film):
        id_filme = []
        for film in self.__filme:
            id_filme.append(film.get_id_film())
        if id_film not in id_filme:
            raise RepoError("Film inexistent!")
        for i in range(0, self.__filme.__len__()):
            film = self.__filme[i]
            if film.get_id_film() == id_film:
                del self.__filme[i]

    def cauta_film_dupa_id(self, id_film):
        ok = 0
        for film in self.__filme:
            if film.get_id_film() == id_film:
                ok = 1
                return film
        if ok == 0:
            raise RepoError("Film inexistent!")

    def modifica_film(self, film_modificat):
        id_film = film_modificat.get_id_film()
        ok = 0
        for film in self.__filme:
            if film.get_id_film() == id_film:
                ok = 1
                film = film_modificat
                return
        if ok == 0:
            raise RepoError("Film inexistent!")

    def get_all(self):
        return self.__filme

    def __len__(self):
        return len(self.__filme)



