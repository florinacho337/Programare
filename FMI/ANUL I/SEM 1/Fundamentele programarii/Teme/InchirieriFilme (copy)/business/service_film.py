from domeniu.film import Film


class ServiceFilm:

    def __init__(self, validator_film, repo_filme):
        self.__validator_film = validator_film
        self.__repo_filme = repo_filme

    def adauga_film(self, id_film, titlu_film, descriere_film, gen_film):
        film = Film(id_film, titlu_film, descriere_film, gen_film)
        self.__validator_film.valideaza(film)
        self.__repo_filme.adauga_film(film)

    def sterge_filmul_cu_id(self, id_film):
        self.__repo_filme.sterge_film_dupa_id(id_film)

    def modifica_filmul(self, id_film, titlu_nou, descriere_noua, gen_nou):
        film_modificat = Film(id_film, titlu_nou, descriere_noua, gen_nou)
        self.__repo_filme.modifica_film(film_modificat)

    def gaseste_film(self, id_film):
        self.__repo_filme.cauta_film_dupa_id(id_film)

    def get_all_filme(self):
        return self.__repo_filme.get_all()

