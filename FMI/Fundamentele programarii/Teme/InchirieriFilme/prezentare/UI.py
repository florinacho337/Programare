from erori.repo_error import RepoError
from erori.validation_error import ValidationError


class UI:

    def __init__(self, service_client, service_film, service_inchiriere):
        self.__service_client = service_client
        self.__service_film = service_film
        self.__service_inchiriere = service_inchiriere
        self.__comenzi = {
            "adauga_film": self.__ui_adauga_film,
            "afiseaza_filme": self.__ui_afiseaza_filme,
            "sterge_film_id": self.__ui_sterge_film_id,
            "modifica_film": self.__ui_modifica_film,
            "gaseste_film": self.__ui_gaseste_film,
            "adauga_client": self.__ui_adauga_client,
            "afiseaza_clienti": self.__ui_afiseaza_clienti,
            "modifica_client": self.__ui_modifica_client
        }

    def __print_menu(self):
        print("1. Adauga film (adauga_film id_film titlu_film descriere_film gen_film")
        print("2. Afiseaza filme (vezi_filme)")
        print("3. Sterge film dupa id (sterge_film_id id_film)")
        print("4. Modifica film (modifica_film id_film titlu_nou descriere_noua gen_nou")
        print("5. Gaseste film dupa id (gaseste_film id_film)")
        print("6. Adauga client (adauga_client id_client nume_client cnp_client)")
        print("7. Afiseaza clienti (vezi_clienti)")
        print("8. Modifica client (modifica_client id_client nume_nou cnp_nou)")

    def __ui_modifica_client(self):
        if len(self.__params) != 3:
            print("Numar de parametrii invalid!")
            return
        id_client = int(self.__params[0])
        nume_nou = self.__params[1]
        cnp_nou = self.__params[2]
        self.__service_client.modifica_client(id_client, nume_nou, cnp_nou)
        print("Client modificat cu succes!")

    def __ui_afiseaza_clienti(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        clienti = self.__service_client.get_all()
        if len(clienti) == 0:
            print("Nu exista clienti!")
            return
        for client in clienti:
            print(client)

    def __ui_adauga_client(self):
        if len(self.__params) != 3:
            print("Numar de parametrii invalid!")
            return
        id_client = int(self.__params[0])
        nume_client = self.__params[1]
        cnp_client = self.__params[2]
        self.__service_client.adauga_client(id_client, nume_client, cnp_client)
        print("Client adaugat cu succes!")

    def __ui_gaseste_film(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        id_film = int(self.__params[0])
        print(self.__service_film.gaseste_film(id_film))

    def __ui_modifica_film(self):
        if len(self.__params) != 4:
            print("Numar de parametrii invalid!")
            return
        id_film = int(self.__params[0])
        titlu_film = self.__params[1]
        descriere_film = self.__params[2]
        gen_film = self.__params[3]
        self.__service_film.modifica_filmul(id_film, titlu_film, descriere_film, gen_film)
        print("Film modificat cu succes!")

    def __ui_sterge_film_id(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
        filme = self.__service_film.get_all_filme()
        if len(filme) == 0:
            print("Nu exista filme!")
            return
        id_film = int(self.__params[0])
        self.__service_film.sterge_filmul_cu_id(id_film)
        print("Film sters cu succes!")

    def __ui_adauga_film(self):
        if len(self.__params) != 4:
            print("Numar de parametrii invalid!")
            return
        id_film = int(self.__params[0])
        titlu_film = self.__params[1]
        descriere_film = self.__params[2]
        gen_film = self.__params[3]
        self.__service_film.adauga_film(id_film, titlu_film, descriere_film, gen_film)
        print("Film adaugat cu succes!")

    def __ui_afiseaza_filme(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        filme = self.__service_film.get_all_filme()
        if len(filme) == 0:
            print("Nu exista filme!")
            return
        for film in filme:
            print(film)

    def run(self):
        print("Scrie \"exit\" pentru a iesi")
        print("Scrie \"menu\" pentru a afisa meniul")
        while True:
            comanda = input(">>>")
            comanda = comanda.strip()
            if comanda == "":
                continue
            if comanda == "exit":
                return
            if comanda == "menu":
                self.__print_menu()
                continue
            parti = comanda.split()
            nume_comanda = parti[0]
            self.__params = parti[1:]
            if nume_comanda in self.__comenzi:
                try:
                    self.__comenzi[nume_comanda]()
                except ValueError:
                    print("Eroare UI: tip numeric invalid")
                except ValidationError as ve:
                    print(f"Valid Error: {ve}")
                except RepoError as re:
                    print(f"Repository Error: {re}")
            else:
                print("Comanda invalida!")

