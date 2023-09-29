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
from domeniu.inchiriere_film import InchiriereFilm
from infrastructura.repo_inchirieri import RepoInchirieri
from validare.validator_inchiriere import ValidareInchiriere
from business.service_inchiriere import ServiceInchiriere
from infrastructura.repo_clienti_file import RepoClientiFile
from infrastructura.repo_filme_file import RepoFilmeFile
from infrastructura.repo_inchirieri_file import RepoInchirieriFile


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
        # parametrii teste inchirieri
        self.__id_inchiriere = 1
        self.__inchiriere = InchiriereFilm(self.__id_inchiriere, self.__id_client, self.__id_film)
        self.__validare_inchiriere = ValidareInchiriere()
        self.__alta_inchiriere_acelasi_id = InchiriereFilm(self.__id_inchiriere, self.__alt_client, self.__alt_film)
        self.__alt_id_inchiriere = 0

    def __teste_inchirieri(self):
        assert(self.__inchiriere.get_id_inchiriere() == self.__id_inchiriere)
        assert(self.__inchiriere.get_id_client() == self.__id_client)
        assert(self.__inchiriere.get_id_film() == self.__id_film)

    def __teste_clienti(self):
        assert(self.__client.get_id_client() == self.__id_client)
        assert(self.__client.get_nume_client() == self.__nume_client)
        assert(self.__client.get_cnp_client() == self.__cnp_client)
        self.__client.set_nume_client("Baciu")
        self.__client.set_cnp_client("5030405341187")
        assert(self.__client.get_nume_client() == "Baciu")
        assert(self.__client.get_cnp_client() == "5030405341187")
        assert(self.__client.__str__() == "1,Baciu,5030405341187")
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
        assert(self.__film.__str__() == '1,Matrix,SF,Nu e real')
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

    def __teste_repo_inchirieri(self):
        self.__repo_inchirieri = RepoInchirieri()
        self.__repo_inchirieri.adauga_inchiriere(self.__inchiriere)
        assert(self.__repo_inchirieri.get_all() == [self.__inchiriere])
        assert(self.__repo_inchirieri.cauta_inchiriere_dupa_id(self.__id_inchiriere) == self.__inchiriere)
        self.__repo_inchirieri.modifica_inchiriere(self.__alta_inchiriere_acelasi_id)
        assert(self.__repo_inchirieri.get_all() == [self.__alta_inchiriere_acelasi_id])
        self.__repo_inchirieri.sterge_inchiriere_dupa_id(self.__id_inchiriere)
        assert(self.__repo_inchirieri.get_all() == [])

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

    def __teste_service_inchirieri(self):
        self.__repo_inchirieri = RepoInchirieri()
        self.__repo_clienti = RepoClienti()
        self.__repo_filme = RepoFilme()
        self.__service_inchirieri = ServiceInchiriere(self.__validare_inchiriere, self.__repo_inchirieri, self.__repo_clienti, self.__repo_filme)
        self.__repo_clienti.adauga_client(self.__client)
        self.__repo_filme.adauga_film(self.__film)
        self.__service_inchirieri.adauga_inchiriere(self.__id_inchiriere, self.__id_client, self.__id_film)
        assert(self.__repo_inchirieri.get_all()[0].get_id_client() == self.__inchiriere.get_id_client())
        try:
            self.__service_inchirieri.adauga_inchiriere(self.__id_inchiriere, self.__id_client, self.__id_film)
            assert False
        except RepoError as re:
            assert(str(re) == "Inchiriere existenta!")
        self.__service_inchirieri.sterge_client_si_inchirieri(self.__id_client)
        assert(len(self.__repo_clienti) == 0)
        assert(self.__repo_filme.get_all() == [self.__film])
        self.__repo_clienti.adauga_client(self.__client)
        self.__service_inchirieri.adauga_inchiriere(self.__id_inchiriere, self.__id_client, self.__id_film)
        self.__service_inchirieri.sterge_inchirierea_cu_id(self.__id_inchiriere)
        assert(self.__repo_inchirieri.get_all() == [])
        self.__service_inchirieri.adauga_inchiriere(self.__id_inchiriere, self.__id_client, self.__id_film)
        assert(len(self.__repo_inchirieri.get_all()) == 1)
        self.__service_inchirieri.sterge_film_si_inchirieri(self.__id_film)
        assert(self.__repo_inchirieri.get_all() == [])
        #teste rapoarte
        self.__repo_clienti = RepoClienti()
        self.__repo_filme = RepoFilme()
        self.__repo_inchirieri = RepoInchirieri()
        self.__service_film = ServiceFilm(self.__validare_film, self.__repo_filme)
        self.__service_clienti = ServiceClient(self.__validare_client, self.__repo_clienti)
        self.__service_inchirieri = ServiceInchiriere(self.__validare_inchiriere, self.__repo_inchirieri, self.__repo_clienti, self.__repo_filme)
        for i in range(0, 10):
            self.__service_film.adauga_film(i, f"titlu{i}", f"descriere{i}", f"gen{i}")
            self.__service_clienti.adauga_client(i, f"nume{i}", f"{i}111111111111")
        self.__service_inchirieri.adauga_inchiriere(1, 4, 5)
        self.__service_inchirieri.adauga_inchiriere(2, 8, 2)
        self.__service_inchirieri.adauga_inchiriere(3, 4, 2)
        self.__service_inchirieri.adauga_inchiriere(4, 4, 3)
        self.__service_inchirieri.adauga_inchiriere(5, 8, 8)
        self.__service_inchirieri.adauga_inchiriere(6, 8, 3)
        self.__service_inchirieri.adauga_inchiriere(7, 4, 8)
        self.__service_inchirieri.adauga_inchiriere(8, 1, 3)
        self.__service_inchirieri.adauga_inchiriere(9, 1, 8)
        self.__service_inchirieri.adauga_inchiriere(10, 2, 8)
        assert(len(self.__service_inchirieri.get_top_30_clienti()) == 3)
        assert(self.__service_inchirieri.get_top_30_clienti()[0].get_nume() == "nume4")
        assert(self.__service_inchirieri.get_top_30_clienti()[1].get_nume() == "nume8")
        assert(self.__service_inchirieri.get_top_30_clienti()[2].get_nume() == "nume1")
        assert(self.__service_inchirieri.get_top_clienti()[3].get_nume() == "nume2")
        assert(self.__service_clienti.get_clienti_dupa_nume()[0].get_nume_client() == "nume0")
        assert(self.__service_clienti.get_clienti_dupa_nume()[1].get_nume_client() == "nume1")
        assert(len(self.__service_inchirieri.get_top_filme()) == 3)
        assert(self.__service_inchirieri.get_top_filme()[0].get_titlu_film() == "titlu8")
        assert(self.__service_inchirieri.get_top_filme()[1].get_titlu_film() == "titlu3")
        assert(self.__service_inchirieri.get_top_filme()[2].get_titlu_film() == "titlu2")
        assert(len(self.__service_inchirieri.get_clienti_ale_caror_nume_incep_cu_litera('t')) == 4)
        assert(self.__service_inchirieri.get_clienti_ale_caror_nume_incep_cu_litera('t')[0].get_nume_client() == "nume4")
        assert(self.__service_inchirieri.get_clienti_ale_caror_nume_incep_cu_litera('t')[1].get_nume_client() == "nume8")
        assert (self.__service_inchirieri.get_clienti_ale_caror_nume_incep_cu_litera('t')[2].get_nume_client() == "nume1")
        assert (self.__service_inchirieri.get_clienti_ale_caror_nume_incep_cu_litera('t')[3].get_nume_client() == "nume2")

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

    def __teste_fisiere(self):
        # fisiere clienti
        with open("testare/teste_clienti.txt", "w") as f:
            f.write("")
        self.__repo_clienti = RepoClientiFile("testare/teste_clienti.txt")
        self.__service_clienti = ServiceClient(self.__validare_client, self.__repo_clienti)
        self.__service_clienti.adauga_client(1, "nume", "0000000000000")
        client = self.__service_clienti.gaseste_client(1)
        assert(client.get_nume_client() == self.__service_clienti.get_all()[0].get_nume_client())
        assert(len(self.__service_clienti.get_all()) == 1)
        self.__service_clienti.adauga_client(2, "nume2", "0000000000000")
        assert(len(self.__service_clienti.get_all()) == 2)
        self.__service_clienti.modifica_client(1, "nume1", "1111111111111")
        assert(self.__service_clienti.gaseste_client(1).get_nume_client() == "nume1")

        # fisiere filme
        with open("testare/teste_filme.txt", "w") as f:
            f.write("")
        self.__repo_filme = RepoFilmeFile("testare/teste_filme.txt")
        self.__service_filme = ServiceFilm(self.__validare_film, self.__repo_filme)
        self.__service_filme.adauga_film(1, "titlu", "descriere", "gen")
        film = self.__service_filme.gaseste_film(1)
        assert(film.get_titlu_film() == self.__service_filme.get_all_filme()[0].get_titlu_film())
        assert(len(self.__service_filme.get_all_filme()) == 1)
        self.__service_filme.adauga_film(2, "titlu2", "descriere2", "gen2")
        assert (len(self.__service_filme.get_all_filme()) == 2)
        self.__service_filme.modifica_filmul(1, "titlu1", "descriere1", "gen1")
        assert(self.__service_filme.gaseste_film(1).get_titlu_film() == "titlu1")

        # fisiere inchirieri
        with open("testare/teste_inchirieri.txt", "w") as f:
            f.write("")
        self.__repo_inchirieri = RepoInchirieriFile("testare/teste_inchirieri.txt")
        self.__service_inchirieri = ServiceInchiriere(self.__validare_inchiriere, self.__repo_inchirieri, self.__repo_clienti, self.__repo_filme)
        self.__service_inchirieri.adauga_inchiriere(1, 1, 1)
        inchiriere = self.__service_inchirieri.gaseste_inchiriere(1)
        assert(inchiriere.get_id_client() == self.__service_inchirieri.get_all()[0].get_id_client())
        assert(len(self.__service_inchirieri.get_all()) == 1)
        self.__service_inchirieri.adauga_inchiriere(2, 2, 2)
        assert (len(self.__service_inchirieri.get_all()) == 2)
        self.__service_inchirieri.sterge_client_si_inchirieri(2)



    def ruleaza_toate_testele(self):
        self.__teste_filme()
        self.__teste_repo_filme()
        self.__teste_validare_filme()
        self.__teste_service_filme()
        self.__teste_clienti()
        self.__teste_validare_client()
        self.__teste_repo_clienti()
        self.__teste_service_clienti()
        self.__teste_inchirieri()
        self.__teste_repo_inchirieri()
        self.__teste_service_inchirieri()
        self.__teste_fisiere()

