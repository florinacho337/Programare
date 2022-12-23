from domeniu.inchiriere_film import InchiriereFilm
from infrastructura.repo_inchirieri import RepoInchirieri


class RepoInchirieriFile(RepoInchirieri):

    def __init__(self, calea_catre_fisier):
        RepoInchirieri.__init__(self)
        self.__calea_catre_fisier = calea_catre_fisier

    def __read_all_from_file(self):
        with open(self.__calea_catre_fisier, "r") as f:
            lines = f.readlines()
            self._inchirieri.clear()
            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(',')
                    id_inchiriere = int(parts[0])
                    id_client = int(parts[1])
                    id_film = int(parts[2])
                    inchiriere = InchiriereFilm(id_inchiriere, id_client, id_film)
                    self._inchirieri[id_inchiriere] = inchiriere

    def __write_all_to_file(self):
        with open(self.__calea_catre_fisier, "w") as f:
            for inchiriere in self._inchirieri.values():
                f.write(str(inchiriere) + "\n")

    def adauga_inchiriere(self, inchiriere):
        self.__read_all_from_file()
        RepoInchirieri.adauga_inchiriere(self, inchiriere)
        self.__write_all_to_file()

    def get_all(self):
        self.__read_all_from_file()
        return RepoInchirieri.get_all(self)

    def sterge_inchiriere_dupa_id(self, id_inchiriere):
        self.__read_all_from_file()
        RepoInchirieri.sterge_inchiriere_dupa_id(self, id_inchiriere)
        self.__write_all_to_file()

    def cauta_inchiriere_dupa_id(self, id_inchiriere):
        self.__read_all_from_file()
        return RepoInchirieri.cauta_inchiriere_dupa_id(self, id_inchiriere)

    def modifica_inchiriere(self, inchiriere_modificata):
        self.__read_all_from_file()
        RepoInchirieri.modifica_inchiriere(self, inchiriere_modificata)
        self.__write_all_to_file()
