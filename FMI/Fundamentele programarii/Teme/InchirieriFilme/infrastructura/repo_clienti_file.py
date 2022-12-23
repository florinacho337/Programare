from domeniu.client import Client
from infrastructura.repo_clienti import RepoClienti


class RepoClientiFile(RepoClienti):

    def __init__(self, calea_catre_fisier):
        RepoClienti.__init__(self)
        self.__calea_catre_fisier = calea_catre_fisier

    def __read_all_from_file(self):
        with open(self.__calea_catre_fisier, "r") as f:
            lines = f.readlines()
            self._clienti.clear()
            for line in lines:
                line = line.strip()
                if line != "":
                    parts = line.split(',')
                    id_client = int(parts[0])
                    nume_client = parts[1]
                    cnp_client = parts[2]
                    client = Client(id_client, nume_client, cnp_client)
                    self._clienti[id_client] = client

    def __write_all_to_file(self):
        with open(self.__calea_catre_fisier, "w") as f:
            for client in self._clienti.values():
                f.write(str(client) + "\n")

    def adauga_client(self, client):
        self.__read_all_from_file()
        RepoClienti.adauga_client(self, client)
        self.__write_all_to_file()

    def modifica_client(self, client):
        self.__read_all_from_file()
        RepoClienti.modifica_client(self, client)
        self.__write_all_to_file()

    def sterge_client_dupa_id(self, id_client):
        self.__read_all_from_file()
        RepoClienti.sterge_client_dupa_id(self, id_client)
        self.__write_all_to_file()

    def get_all(self):
        self.__read_all_from_file()
        return RepoClienti.get_all(self)

    def cauta_client_dupa_id(self, id_client):
        self.__read_all_from_file()
        return RepoClienti.cauta_client_dupa_id(self, id_client)

    def __len__(self):
        self.__read_all_from_file()
        return RepoClienti.__len__(self)
