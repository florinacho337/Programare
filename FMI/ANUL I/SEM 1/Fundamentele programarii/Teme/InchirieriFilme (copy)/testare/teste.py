from domeniu.film import Film
from infrastructura.repo_filme import RepoFilme
from erori.repo_error import RepoError
from erori.validation_error import ValidationError
from validare.validator_film import ValidareFilm
from business.service_film import ServiceFilm


class teste:

    def __init__(self):
        # parametrii teste filme
        self.__id_film = 1
        self.__titlu_film = "Forrest Gump"
        self.__gen_film = "Biografie"
        self.__descriere_film = "Inspirat din fapte reale"
        self.__id_film_gresit = -1
        self.__titlu_film_gresit = ""
        self.__descriere_film_gresit = ""
        self.__gen_film_gresit = ""
        self.__film = Film(self.__id_film, self.__titlu_film, self.__descriere_film, self.__gen_film)
        self.__film_gresit = Film(self.__id_film_gresit, self.__titlu_film_gresit, self.__descriere_film_gresit, self.__gen_film_gresit)
        self.__alt_film = Film(2, "Forrest Gump", "Inspirat din fapte reale", "Biografie")
        self.__alt_titlu = "Pulp Fiction"
        self.__alta_descriere = "Aparut inainte de 2000"
        self.__alt_gen = "Comedie neagra"
        self.__alt_film_acelasi_id = Film(self.__id_film, self.__alt_titlu, self.__alta_descriere, self.__alt_gen)
        self.__repo_filme = RepoFilme()
        self.__validare_film = ValidareFilm()
        self.__service_film = ServiceFilm(self.__validare_film, self.__repo_filme)
        # parametrii teste clienti

    def __teste_filme(self):
        assert(self.__film.get_id_film() == 1)
        assert(self.__film.get_descriere_film() == "Inspirat din fapte reale")
        assert(self.__film.get_gen_film() == "Biografie")
        assert(self.__film.get_titlu_film() == "Forrest Gump")
        self.__film.set_titlu_film("Matrix")
        self.__film.set_gen_film("SF")
        self.__film.set_descriere_film("Nu e real")
        assert(self.__film.get_descriere_film() == "Nu e real")
        assert(self.__film.get_gen_film() == "SF")
        assert(self.__film.get_titlu_film() == "Matrix")
        assert(self.__film.__str__() == '1. Matrix, SF, Nu e real')
        assert(self.__film.__eq__(self.__alt_film) is False)

    def __teste_validare_filme(self):
        try:
            self.__validare_film.valideaza(self.__film_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nTitlu invalid!\nGen invalid!\nDescriere invalida!\n")

    def __teste_repo_filme(self):
        self.__repo_filme.adauga_film(self.__film)
        assert(self.__repo_filme.get_all() == [self.__film])
        assert(self.__repo_filme.__len__() == 1)
        self.__repo_filme.adauga_film(self.__alt_film)
        assert(self.__repo_filme.get_all() == [self.__film, self.__alt_film])
        assert(self.__repo_filme.__len__() == 2)
        try:
            self.__repo_filme.adauga_film(self.__film)
            assert False
        except RepoError as re:
            assert(str(re) == 'Film existent!')
        self.__repo_filme.modifica_film(self.__alt_film_acelasi_id)
        assert(self.__repo_filme.get_all() == [self.__alt_film_acelasi_id, self.__alt_film])
        try:
            self.__repo_filme.sterge_film_dupa_id(3)
            assert False
        except RepoError as re:
            assert(str(re) == 'Film inexistent!')
        self.__repo_filme.sterge_film_dupa_id(2)
        assert(self.__repo_filme.__len__() == 1)
        try:
            self.__repo_filme.modifica_film(self.__alt_film)
            assert False
        except RepoError as re:
            assert(str(re) == 'Film inexistent!')
        assert(self.__repo_filme.cauta_film_dupa_id(1) == self.__alt_film_acelasi_id)
        try:
            self.__repo_filme.cauta_film_dupa_id(3)
            assert False
        except RepoError as re:
            assert(str(re) == 'Film inexistent!')
        self.__repo_filme.sterge_film_dupa_id(1)

    def __teste_service_filme(self):
        self.__service_film.adauga_film(self.__id_film, self.__titlu_film, self.__descriere_film, self.__gen_film)
        assert(self.__repo_filme.get_all() == [self.__film])
        try:
            self.__service_film.adauga_film(self.__id_film_gresit, self.__titlu_film_gresit, self.__descriere_film_gresit, self.__gen_film_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nTitlu invalid!\nGen invalid!\nDescriere invalida!\n")
        assert(self.__service_film.get_all_filme() == [self.__film])
        self.__service_film.modifica_filmul(self.__id_film, self.__alt_titlu, self.__alta_descriere, self.__alt_gen)
        assert(self.__repo_filme.get_all() == [self.__alt_film_acelasi_id])
        self.__service_film.sterge_filmul_cu_id(1)
        assert(self.__service_film.get_all_filme() == [])

    def ruleaza_toate_testele(self):
        self.__teste_filme()
        self.__teste_repo_filme()
        self.__teste_validare_filme()
        self.__teste_service_filme()
