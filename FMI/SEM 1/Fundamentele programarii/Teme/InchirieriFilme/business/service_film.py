from domeniu.film import Film
import random
import string


class ServiceFilm:

    def __init__(self, validator_film, repo_filme):
        self.__validator_film = validator_film
        self.__repo_filme = repo_filme
        self.__litere = string.ascii_lowercase
        self.__litere_si_semne_de_punctuatie = self.__litere + ".,!?"

    def adauga_film(self, id_film, titlu_film, descriere_film, gen_film):
        '''
        creeaza un film cu id-ul intreg id_film, string-ul titlu_film, string-ul descriere_film si
        string-ul gen_film, incearca sa-l valideze apoi incearca sa adauge in repository filmul creat
        :param id_film: intreg
        :param titlu_film: string
        :param descriere_film: string
        :param gen_film: string
        :return: -
        :raises: ValidationError daca filmul este invalid
                 "Id invalid!" daca id_film < 0
                 "Titlu invalid!" daca titlu_film == ""
                 "Gen invalid!" daca gen_film == ""
                 "Descriere invalida!" daca descriere_film == ""
                 RepoError daca id-ul filmului film_adaugat este deja existent
        '''
        film = Film(id_film, titlu_film, descriere_film, gen_film)
        self.__validator_film.valideaza(film)
        self.__repo_filme.adauga_film(film)

    def modifica_filmul(self, id_film, titlu_nou, descriere_noua, gen_nou):
        '''
        creeaza un film cu id-ul intreg id_film deja existent, titlul string titlu_nou, descrierea
        string descriere_noua si genul string gen_nou, incearca sa-l valideze si apoi incearca sa
        modifice in repository filmul de pe id-ul id_film cu filmul modificat
        :param id_film: intreg
        :param titlu_nou: string
        :param descriere_noua: string
        :param gen_nou: string
        :return: -
        :raises: ValidationError daca filmul este invalid
                 "Id invalid!" daca id_film < 0
                 "Titlu invalid!" daca titlu_film == ""
                 "Gen invalid!" daca gen_film == ""
                 "Descriere invalida!" daca descriere_film == ""
                 RepoError daca id-ul filmului film_adaugat este inexistent
        '''
        film_modificat = Film(id_film, titlu_nou, descriere_noua, gen_nou)
        self.__validator_film.valideaza(film_modificat)
        self.__repo_filme.modifica_film(film_modificat)

    def gaseste_film(self, id_film):
        '''
        returneaza filmul cu id-ul intreg id_film
        :param id_film: intreg
        :return: filmul cu id-ul intreg id_film
        :raises: RepoError daca id-ul id_film nu exista
        '''
        return self.__repo_filme.cauta_film_dupa_id(id_film)

    def get_all_filme(self):
        '''
        returneaza toate filmele din repository
        :return: toate filmele din repository
        '''
        return self.__repo_filme.get_all()

    def genereaza_film(self):
        '''
        se genereaza un film cu un id intreg intre 0 si 100, un titlu, un gen si o descriere
        :return: -
        '''
        id_film = random.randrange(0, 100)
        while id_film in self.__repo_filme.get_all_ids():
            id_film = random.randrange(0, 100)
        titlu_film = "".join(random.choice(self.__litere) for i in range(10))
        gen_film = "".join(random.choice(self.__litere) for i in range(10))
        descriere_film = "".join(random.choice(self.__litere_si_semne_de_punctuatie) for i in range(50))
        film = Film(id_film, titlu_film, descriere_film, gen_film)
        self.__repo_filme.adauga_film(film)

