from domeniu.film import Film
from infrastructura.repo_filme import RepoFilme
from erori.repo_error import RepoError
from erori.validation_error import ValidationError
from validare.validator_film import ValidareFilm
from business.service_film import ServiceFilm
from domeniu.client import Client
from infrastructura.repo_clienti import RepoClienti
from validare.validator_client import ValidareClient
from business.service_client import ServiceClient


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
        self.__alt_id_film = 0
        self.__alt_titlu = "Pulp Fiction"
        self.__alta_descriere = "Aparut inainte de 2000"
        self.__alt_gen = "Comedie neagra"
        self.__alt_film_acelasi_id = Film(self.__id_film, self.__alt_titlu, self.__alta_descriere, self.__alt_gen)
        self.__repo_filme = RepoFilme()
        self.__validare_film = ValidareFilm()
        self.__service_film = ServiceFilm(self.__validare_film, self.__repo_filme)
        # parametrii teste clienti
        self.__id_client = 1
        self.__nume_client = "Florin"
        self.__cnp_client = "5040204341187"
        self.__client = Client(self.__id_client, self.__nume_client, self.__cnp_client)
        self.__alt_id_client = 2
        self.__alt_nume_client = "Andrei"
        self.__alt_cnp_client = "6030405341187"
        self.__alt_client = Client(self.__alt_id_client, self.__alt_nume_client, self.__alt_cnp_client)
        self.__alt_client_acelasi_id = Client(self.__id_client, self.__alt_nume_client, self.__alt_cnp_client)
        self.__validare_client = ValidareClient()
        self.__id_client_gresit = -1
        self.__nume_client_gresit = ""
        self.__cnp_client_gresit = ""
        self.__client_gresit = Client(self.__id_client_gresit, self.__nume_client_gresit, self.__cnp_client_gresit)

    def __teste_clienti(self):
        assert(self.__client.get_id_client() == self.__id_client)
        assert(self.__client.get_nume_client() == self.__nume_client)
        assert(self.__client.get_cnp_client() == self.__cnp_client)
        self.__client.set_nume_client("Baciu")
        self.__client.set_cnp_client("5030405341187")
        assert(self.__client.get_nume_client() == "Baciu")
        assert(self.__client.get_cnp_client() == "5030405341187")
        assert(self.__client.__str__() == "1. Baciu, 5030405341187")
        assert(not(self.__client == self.__alt_client))

    def __teste_filme(self):
        assert(self.__film.get_id_film() == self.__id_film)
        assert(self.__film.get_descriere_film() == self.__descriere_film)
        assert(self.__film.get_gen_film() == self.__gen_film)
        assert(self.__film.get_titlu_film() == self.__titlu_film)
        self.__film.set_titlu_film("Matrix")
        self.__film.set_gen_film("SF")
        self.__film.set_descriere_film("Nu e real")
        assert(self.__film.get_descriere_film() == "Nu e real")
        assert(self.__film.get_gen_film() == "SF")
        assert(self.__film.get_titlu_film() == "Matrix")
        assert(self.__film.__str__() == '1. Matrix, SF, Nu e real')
        assert(not(self.__film == self.__alt_film))

    def __teste_validare_client(self):
        try:
            self.__validare_client.valideaza(self.__client_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nNume invalid!\nCNP invalid!")

    def __teste_validare_filme(self):
        try:
            self.__validare_film.valideaza(self.__film_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nTitlu invalid!\nGen invalid!\nDescriere invalida!")

    def __teste_repo_clienti(self):
        self.__repo_clienti = RepoClienti()
        self.__repo_clienti.adauga_client(self.__client)
        assert(self.__repo_clienti.get_all() == [self.__client])
        assert(len(self.__repo_clienti) == 1)
        try:
            self.__repo_clienti.adauga_client(self.__client)
            assert False
        except RepoError as re:
            assert(str(re) == "Client existent!")
        assert(len(self.__repo_clienti) == 1)
        self.__repo_clienti.modifica_client(self.__alt_client_acelasi_id)
        assert(self.__repo_clienti.get_all()[0].get_nume_client() == "Andrei")
        try:
            self.__repo_clienti.modifica_client(self.__alt_client)
            assert False
        except RepoError as re:
            assert(str(re) == "Client inexistent!")
        assert(self.__repo_clienti.cauta_client_dupa_id(self.__alt_client_acelasi_id.get_id_client()) == self.__alt_client_acelasi_id)
        try:
            self.__repo_clienti.cauta_client_dupa_id(2)
            assert False
        except RepoError as re:
            assert(str(re) == "Client inexistent!")

    def __teste_repo_filme(self):
        self.__repo_filme.adauga_film(self.__film)
        assert(self.__repo_filme.get_all() == [self.__film])
        assert(len(self.__repo_filme) == 1)
        self.__repo_filme.adauga_film(self.__alt_film)
        assert(self.__repo_filme.get_all() == [self.__film, self.__alt_film])
        assert(self.__repo_filme.__len__() == 2)
        try:
            self.__repo_filme.adauga_film(self.__film)
            assert False
        except RepoError as re:
            assert(str(re) == 'Film existent!')
        self.__repo_filme.modifica_film(self.__alt_film_acelasi_id)
        assert(self.__repo_filme.get_all()[0].get_titlu_film() == "Pulp Fiction")
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

    def __teste_service_clienti(self):
        self.__repo_clienti = RepoClienti()
        self.__service_clienti = ServiceClient(self.__validare_client, self.__repo_clienti)
        self.__service_clienti.adauga_client(self.__id_client, self.__nume_client, self.__cnp_client)
        assert(self.__service_clienti.get_all() == [self.__client])
        try:
            self.__service_clienti.adauga_client(self.__id_client_gresit, self.__nume_client_gresit, self.__cnp_client_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nNume invalid!\nCNP invalid!")
        try:
            self.__service_clienti.adauga_client(self.__id_client, self.__nume_client, self.__cnp_client)
            assert False
        except RepoError as re:
            assert(str(re) == "Client existent!")
        self.__service_clienti.modifica_client(self.__id_client, self.__alt_nume_client, self.__alt_cnp_client)
        assert(self.__repo_clienti.get_all()[0].get_nume_client() == self.__alt_nume_client)
        try:
            self.__service_clienti.modifica_client(self.__alt_id_client, self.__nume_client, self.__cnp_client)
            assert False
        except RepoError as re:
            assert(str(re) == "Client inexistent!")
        try:
            self.__service_clienti.modifica_client(self.__id_client, self.__nume_client_gresit, self.__cnp_client_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Nume invalid!\nCNP invalid!")
        assert(self.__service_clienti.gaseste_client(self.__id_client) == self.__alt_client_acelasi_id)
        try:
            self.__service_clienti.gaseste_client(self.__alt_id_client)
            assert False
        except RepoError as re:
            assert(str(re) == "Client inexistent!")

    def __teste_service_filme(self):
        self.__service_film.adauga_film(self.__id_film, self.__titlu_film, self.__descriere_film, self.__gen_film)
        assert(self.__repo_filme.get_all() == [self.__film])
        try:
            self.__service_film.adauga_film(self.__id_film_gresit, self.__titlu_film_gresit, self.__descriere_film_gresit, self.__gen_film_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nTitlu invalid!\nGen invalid!\nDescriere invalida!")
        try:
            self.__service_film.adauga_film(self.__id_film, self.__titlu_film, self.__descriere_film, self.__gen_film)
            assert False
        except RepoError as re:
            assert(str(re) == "Film existent!")
        assert(self.__service_film.get_all_filme() == [self.__film])
        self.__service_film.modifica_filmul(self.__id_film, self.__alt_titlu, self.__alta_descriere, self.__alt_gen)
        assert(self.__repo_filme.get_all()[0].get_titlu_film() == self.__alt_film_acelasi_id.get_titlu_film())
        try:
            self.__service_film.modifica_filmul(self.__alt_id_film, self.__titlu_film, self.__descriere_film, self.__gen_film)
            assert False
        except RepoError as re:
            assert(str(re) == "Film inexistent!")
        try:
            self.__service_film.modifica_filmul(self.__id_film_gresit, self.__titlu_film_gresit, self.__descriere_film_gresit, self.__gen_film_gresit)
            assert False
        except ValidationError as ve:
            assert(str(ve) == "Id invalid!\nTitlu invalid!\nGen invalid!\nDescriere invalida!")
        try:
            self.__service_film.gaseste_film(self.__alt_id_film)
            assert False
        except RepoError as re:
            assert(str(re) == "Film inexistent!")
        assert(self.__service_film.gaseste_film(self.__id_film) == self.__film)
        try:
            self.__service_film.sterge_filmul_cu_id(self.__alt_id_film)
            assert False
        except RepoError as re:
            assert(str(re) == "Film inexistent!")
        self.__service_film.sterge_filmul_cu_id(self.__id_film)
        assert(self.__service_film.get_all_filme() == [])

    def ruleaza_toate_testele(self):
        self.__teste_filme()
        self.__teste_repo_filme()
        self.__teste_validare_filme()
        self.__teste_service_filme()
        self.__teste_clienti()
        self.__teste_validare_client()
        self.__teste_repo_clienti()
        self.__teste_service_clienti()
