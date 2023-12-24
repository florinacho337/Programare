from infrastructura.repo_filme import RepoFilme
from domeniu.film import Film


class RepoFilmeFile(RepoFilme):

    def __init__(self, calea_catre_fisier):
        RepoFilme.__init__(self)
        self.__calea_catre_fisier = calea_catre_fisier

    def __read_all_from_file(self):
        with open(self.__calea_catre_fisier, "r") as f:
            lines = f.readlines()
            self._filme.clear()
            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(',')
                    id_film = int(parts[0])
                    titlu_film = parts[1]
                    descriere_film = parts[2]
                    gen_film = parts[2]
                    film = Film(id_film, titlu_film, descriere_film, gen_film)
                    self._filme[id_film] = film

    def __write_all_to_file(self):
        with open(self.__calea_catre_fisier, "w") as f:
            for film in self._filme.values():
                f.write(str(film) + "\n")

    def adauga_film(self, film):
        self.__read_all_from_file()
        RepoFilme.adauga_film(self, film)
        self.__write_all_to_file()

    def modifica_film(self, film):
        self.__read_all_from_file()
        RepoFilme.modifica_film(self, film)
        self.__write_all_to_file()

    def sterge_film_dupa_id(self, id_film):
        self.__read_all_from_file()
        RepoFilme.sterge_film_dupa_id(self, id_film)
        self.__write_all_to_file()

    def get_all(self):
        self.__read_all_from_file()
        return RepoFilme.get_all(self)

    def cauta_film_dupa_id(self, id_film):
        self.__read_all_from_file()
        return RepoFilme.cauta_film_dupa_id(self, id_film)

    def __len__(self):
        self.__read_all_from_file()
        return RepoFilme.__len__(self)



