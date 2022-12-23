import unittest
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

class TesteUnit(unittest.TestCase):

    def SetUp(self):
        validator = ValidareInchiriere()
        validator_film = ValidareFilm()
        validator_client = ValidareClient()
        self.__repository_inchirieri = RepoInchirieriFile("teste_inchirieri.txt")
        self.__repository_clienti = RepoClientiFile("teste_clienti.txt")
        self.__repository_filme = RepoFilmeFile("teste_filme.txt")
        repository_clienti = RepoClientiFile("teste_clienti.txt")
        repository_filme = RepoFilmeFile("teste_filme.txt")
        self.__service = ServiceInchiriere(validator, self.__repository_inchirieri, repository_clienti, repository_filme)
        self.__service_film = ServiceFilm(validator_film, self.__repository_filme)
        self.__service_clienti = ServiceClient(validator_client, self.__repository_clienti)
        client = self.__service_clienti.adauga_client(1, "Florin", "0000000000000")
        film = self.__service_film.adauga_film(1, "titlu", "descriere", "gen")
        inchiriere = self.__service.adauga_inchiriere(1, 1, 1)

    def TearDown(self):
        with open("teste_inchirieri.txt", "w") as f:
            f.write("")
        with open("teste_clienti.txt", "w") as f:
            f.write("")
        with open("teste_filme.txt", "w") as f:
            f.write("")

    def TesteAdaugare(self):
        self.assertTrue(self.__service_clienti.get_all() == 1)
        # white box testing adauga_client
        # client invalid
        self.assertRaises(ValidationError, self.__service_clienti.adauga_client, -1, "", "10")
        # client cu acelasi id
        self.assertRaises(RepoError, self.__service_clienti.adauga_client, 1, "nume", "1111111111111")

        self.assertTrue(self.__service_film.get_all_filme() == 1)

        # white box testing adauga_film
        # film invalid
        self.assertRaises(ValidationError, self.__service_film.adauga_film, -1, "", "", "")
        # film cu acelasi id
        self.assertRaises(RepoError, self.__service_film.adauga_film, 1, "titlu", "descriere", "gen")

        self.assertTrue(self.__service.get_all() == 1)
        # white box testing adauga_ichiriere
        # inchiriere invalida
        self.assertRaises(ValidationError, self.__service.adauga_inchiriere, -1, 0, 0)
        # inchiriere cu acelasi id
        self.assertRaises(RepoError, self.__service.adauga_inchiriere, 1, 2, 2)

    def TesteModificare(self):
        # white box testing modifica_client
        # client invalid
        self.assertRaises(ValidationError, self.__service_clienti.modifica_client, -1, "", "10")

        # client cu acelasi id
        self.assertRaises(RepoError, self.__service_clienti.modifica_client, 1, "nume", "1111111111111")

        # white box testing modifica_filmul
        # film invalid
        self.assertRaises(ValidationError, self.__service_film.modifica_filmul, -1, "", "", "")
        # film cu acelasi id
        self.assertRaises(RepoError, self.__service_film.modifica_filmul, 1, "titlu1", "descriere1", "gen1")

    def TesteCautare(self):
        # white box testing gaseste_clienti
        # client inexistent
        self.assertRaises(RepoError, self.__service_clienti.gaseste_client, 0)

        # white box testing gaseste_film
        # film inexistent
        self.assertRaises(RepoError, self.__service_film.gaseste_film, 0)

        # white box testing gaseste_inchiriere
        # inchiriere inexistenta
        self.assertRaises(RepoError, self.__service.gaseste_inchiriere, 0)

    def TesteStergereClienti(self):
        # white box testing sterge_client_si_inchirieri
        # client inexistent
        self.assertRaises(RepoError, self.__service.sterge_client_si_inchirieri, 0)

    def TesteStergeriFilme(self):
        # white box testing sterge_film_si_inchirieri
        # film inexistent
        self.assertRaises(RepoError, self.__service.sterge_film_si_inchirieri, 0)

    def TesteStatistici(self):
        # black box testing get_top_filme
        self.__service_film.adauga_film(1, "titlu1", "desccriere1", "gen1")
        self.__service_film.adauga_film(2, "titlu2", "descriere2", "gen2")
        self.__service_film.adauga_film(3, "titlu3", "descriere3", "gen3")
        self.__service_clienti.adauga_client(1, "Florin", "0000000000000")
        self.__service.adauga_inchiriere(1, 1, 1)
        self.__service.adauga_inchiriere(1, 1, 2)
        self.__service.adauga_inchiriere(1, 1, 3)
        self.assertEquals(self.__service.get_top_filme()[0].get_titlu_film(), "titlu1")
        self.assertEquals(self.__service.get_top_filme()[1].get_titlu_film(), "titlu2")
        self.assertEquals(self.__service.get_top_filme()[2].get_titlu_film(), "titlu3")

        # black box testing get_top_clienti
        self.assertEquals(self.__service.get_top_clienti()[0].get_nume(), "Florin")
        self.assertTrue(len(self.__service.get_top_clienti()) == 1)


