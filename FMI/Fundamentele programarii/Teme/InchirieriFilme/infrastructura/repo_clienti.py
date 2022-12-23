from erori.repo_error import RepoError


class RepoClienti:

    def __init__(self):
        self._clienti = {}

    def adauga_client(self, client):
        '''
        adauga in repository clientul client
        :param client: client
        :return: -
        :raises: RepoError daca id-ul clientului client_nou este deja existent
        '''
        if client.get_id_client() in self._clienti:
            raise RepoError("Client existent!")
        self._clienti[client.get_id_client()] = client

    def get_all(self):
        '''
        returneaza toti clientii din repository
        :return: toti clientii din repository
        '''
        clienti = []
        for id_client in self._clienti:
            clienti.append(self._clienti[id_client])
        return clienti

    def __len__(self):
        '''
        returneaza numarul de clienti din repository
        :return: numarul de clienti din repository
        '''
        return len(self._clienti)

    def modifica_client(self, client_modificat):
        '''
        modifica clientul cu id-ul intreg al clientului modificat client_modificat cu clientul
        client_modificat
        :param client_modificat: client
        :return: -
        :raises: RepoError daca id-ul clientului id_client nu exista
        '''
        if client_modificat.get_id_client() not in self._clienti:
            raise RepoError("Client inexistent!")
        self._clienti[client_modificat.get_id_client()] = client_modificat

    def cauta_client_dupa_id(self, id_client):
        '''
        returneaza clientul cu id-ul intreg id_client
        :param id_client: intreg
        :return: clientul cu id-ul intreg id_client
        :raises: RepoError daca id-ul clientului este inexistent
        '''
        if id_client not in self._clienti:
            raise RepoError("Client inexistent!")
        return self._clienti[id_client]

    def sterge_client_dupa_id(self, id_client):
        '''
        sterge din repository clientu cu id-ul intreg id_client
        :param id_client: intreg
        :return: - (sterge din repository clientul cu id-ul intreg id_client)
        :raises: RepoError daca id-ul id_client nu exista
        '''
        if id_client not in self._clienti:
            raise RepoError("Client inexistent!")
        del self._clienti[id_client]

    def get_all_ids(self):
        '''
        returneaza toate id-urile clientilor din repository
        :return: toate id-urile clientilor din repository
        '''
        ids = []
        for id_client in self._clienti:
            ids.append(id_client)
        return ids

