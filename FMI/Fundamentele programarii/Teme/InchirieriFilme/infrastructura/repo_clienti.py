from erori.repo_error import RepoError


class RepoClienti:

    def __init__(self):
        self.__clienti = {}

    def adauga_client(self, client):
        '''
        adauga in repository clientul client
        :param client: client
        :return: -
        :raises: RepoError daca id-ul clientului client_nou este deja existent
        '''
        if client.get_id_client() in self.__clienti:
            raise RepoError("Client existent!")
        self.__clienti[client.get_id_client()] = client



    def get_all(self):
        '''
        returneaza toti clientii din repository
        :return: toti clientii din repository
        '''
        clienti = []
        for id_client in self.__clienti:
            clienti.append(self.__clienti[id_client])
        return clienti

    def __len__(self):
        '''
        returneaza numarul de clienti din repository
        :return: numarul de clienti din repository
        '''
        return len(self.__clienti)

    def modifica_client(self, client_modificat):
        '''
        modifica clientul cu id-ul intreg al clientului modificat client_modificat cu clientul
        client_modificat
        :param client_modificat: client
        :return: -
        :raises: RepoError daca id-ul clientului id_client nu exista
        '''
        if client_modificat.get_id_client() not in self.__clienti:
            raise RepoError("Client inexistent!")
        self.__clienti[client_modificat.get_id_client()] = client_modificat

    def cauta_client_dupa_id(self, id_client):
        '''
        returneaza clientul cu id-ul intreg id_client
        :param id_client: intreg
        :return: clientul cu id-ul intreg id_client
        :raises: RepoError daca id-ul clientului este inexistent
        '''
        if id_client not in self.__clienti:
            raise RepoError("Client inexistent!")
        return self.__clienti[id_client]
