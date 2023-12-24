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
            "sterge_film_si_inchirieri": self.__ui_sterge_film_si_inchirieri,
            "modifica_film": self.__ui_modifica_film,
            "gaseste_film": self.__ui_gaseste_film,
            "adauga_client": self.__ui_adauga_client,
            "afiseaza_clienti": self.__ui_afiseaza_clienti,
            "modifica_client": self.__ui_modifica_client,
            "gaseste_client": self.__ui_gaseste_client,
            "sterge_client_si_inchirieri": self.__ui_sterge_client_si_inchirieri,
            "adauga_inchiriere": self.__ui_adauga_inchiriere,
            "afiseaza_inchirieri": self.__ui_afiseaza_inchirieri,
            "genereaza_clienti": self.__ui_genereaza_clienti,
            "genereaza_filme": self.__ui_genereaza_filme,
            "returneaza_film": self.__ui_returneaza_film,
            "top_30": self.__ui_top_30,
            "top_clienti": self.__ui_top_clienti,
            "afiseaza_clienti_dupa_nume": self.__ui_afiseaza_clienti_dupa_nume,
            "top_filme": self.__ui_top_filme,
            "afiseaza_clienti_titluri_filme_inchiriate_incep_cu_litera": self.__ui_get_clienti_ale_caror_nume_incepe_cu_litera
        }

    def __print_menu(self):
        print("1. Adauga film (adauga_film id_film titlu_film descriere_film gen_film")
        print("2. Afiseaza filme (afiseaza_filme)")
        print("3. Sterge film si inchirieri (sterge_film_si_inchirieri id_film)")
        print("4. Modifica film (modifica_film id_film titlu_nou descriere_noua gen_nou")
        print("5. Gaseste film dupa id (gaseste_film id_film)")
        print("6. Adauga client (adauga_client id_client nume_client cnp_client)")
        print("7. Afiseaza clienti (afiseaza_clienti)")
        print("8. Modifica client (modifica_client id_client nume_nou cnp_nou)")
        print("9. Gaseste client dupa id (gaseste_client id_client)")
        print("10. Sterge clienti si inchirieri (sterge_client_si_inchirieri id_client)")
        print("11. Adauga inchiriere (adauga_inchiriere id_inchiriere id_client id_film")
        print("12. Afiseaza inchirieri (afiseaza_inchirieri)")
        print("13. Returneaza film (returneaza_film id_inchiriere)")
        print("13. Genereaza clienti (genereaza_clienti numar_clienti_generati)")
        print("14. Genereaza filme (genereaza_filme numar_filme_generate)")
        print("15. Afiseaza primii 30% clienti cu cele mai multe filme inchiriate (top_30)")
        print("16. Afiseaza clientii dupa numarul de filme inchiriate (top_clienti)")
        print("17. Afiseaza clientii sortati dupa nume (afiseaza_clienti_dupa_nume)")
        print("18. Afiseaza topul celor mai inchiriate filme (top_filme)")
        print("19. Afiseaza clienti care au inchiriat filme ale caror titluri incep cu litera (afiseaza_clienti_titluri_filme_inchiriate_incep_cu_litera litera")
        print("20. Afiseaza numarul de clienti inregsitrati (nr_clienti)")
        print("21. Afiseaza numarul de filme inregistrate (nr_filme)")

    def __ui_nr_clienti(self, lista_clienti):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        if lista_clienti == []:
            return 0
        return self.__ui_nr_clienti(lista_clienti[1:]) + 1

    def __ui_nr_filme(self, lista_filme):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        if lista_filme == []:
            return 0
        return self.__ui_nr_filme(lista_filme[1:]) + 1


    def __ui_get_clienti_ale_caror_nume_incepe_cu_litera(self):
        if len(self.__params) != 1:
            print("Numar de paramterii invalid!")
            return
        litera = self.__params[0]
        clienti = self.__service_inchiriere.get_clienti_ale_caror_nume_incep_cu_litera(litera)
        for client in clienti:
            print(client)

    def __ui_top_filme(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        filme = self.__service_inchiriere.get_top_filme()
        for film in filme:
            print(film)

    def __ui_afiseaza_clienti_dupa_nume(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        clienti = self.__service_client.get_clienti_dupa_nume()
        for client in clienti:
            print(client)

    def __ui_top_clienti(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        top_clienti = self.__service_inchiriere.get_top_clienti()
        for client in top_clienti:
            print(client)

    def __ui_top_30(self):
        if len(self.__params) != 0:
            print("Numar de parametrii invalid!")
            return
        top_30 = self.__service_inchiriere.get_top_30_clienti()
        for client in top_30:
            print(client)

    def __ui_returneaza_film(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        id_inchiriere = int(self.__params[0])
        self.__service_inchiriere.sterge_inchirierea_cu_id(id_inchiriere)
        print("Film returnat cu succes!")

    def __ui_genereaza_clienti(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        clienti_generati = int(self.__params[0])
        for i in range(0, clienti_generati):
            self.__service_client.genereaza_client()
        print("Clienti generati cu succes!")

    def __ui_genereaza_filme(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        filme_generate = int(self.__params[0])
        for i in range(0, filme_generate):
            self.__service_film.genereaza_film()
        print("Filme generate cu succes!")

    def __ui_afiseaza_inchirieri(self):
        if len(self.__params) != 0:
            print("Numar de paramterii invalid!")
            return
        inchirieri = self.__service_inchiriere.get_all()
        if len(inchirieri) == 0:
            print("Nu exista inchirieri!")
            return
        for inchiriere in inchirieri:
            print(inchiriere)

    def __ui_adauga_inchiriere(self):
        if len(self.__params) != 3:
            print("Numar de parametrii invalid!")
            return
        id_inchiriere = int(self.__params[0])
        id_client = int(self.__params[1])
        id_film = int(self.__params[2])
        self.__service_inchiriere.adauga_inchiriere(id_inchiriere, id_client, id_film)
        print("Inchiriere adaugata cu succes!")

    def __ui_sterge_client_si_inchirieri(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        id_client = int(self.__params[0])
        self.__service_inchiriere.sterge_client_si_inchirieri(id_client)
        print("Client si inchirieri sterse cu succes!")

    def __ui_gaseste_client(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
            return
        id_client = int(self.__params[0])
        print(self.__service_client.gaseste_client(id_client))

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

    def __ui_sterge_film_si_inchirieri(self):
        if len(self.__params) != 1:
            print("Numar de parametrii invalid!")
        id_film = int(self.__params[0])
        self.__service_inchiriere.sterge_film_si_inchirieri(id_film)
        print("Film si inchirieri sterse cu succes!")

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
            elif nume_comanda == "nr_clienti":
                lista_clienti = self.__service_client.get_all()
                print(self.__ui_nr_clienti(lista_clienti))
            elif nume_comanda == "nr_filme":
                lista_filme = self.__service_film.get_all_filme()
                print(self.__ui_nr_filme(lista_filme))
            else:
                print("Comanda invalida!")

