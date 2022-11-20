from domeniu.client import Client


class ServiceClient:

    def __init__(self, validator_client, repo_clienti):
        self.__validator_client = validator_client
        self.__repo_clienti = repo_clienti

    def adauga_client(self, id_client, nume_client, cnp_client):
        '''
        creeaza un client nou cu id-ul intreg id_client, numele string nume_client si cnp-ul string
        cnp_client, incearca sa-l valideze, iar apoi incearca sa-l adauge in repository
        :param id_client: intreg
        :param nume_client: string
        :param cnp_client: string
        :return: -
        :raises: ValidationError daca parametrii clientului sunt invalizi
                                 daca id_client < 0 -> "Id invalid!"
                                 daca nume_client == "" -> "Nume invalid!"
                                 daca len(cnp_client) != 13 -> "CNP invalid!"
                 RepoError daca id-ul clientului este inexistent
        '''
        client = Client(id_client, nume_client, cnp_client)
        self.__validator_client.valideaza(client)
        self.__repo_clienti.adauga_client(client)

    def get_all(self):
        '''
        retruneaza toti clientii din repository
        :return: toti clientii din repository
        '''
        return self.__repo_clienti.get_all()

    def modifica_client(self, id_client, nume_client, cnp_client):
        '''
        creeaza un client cu id-ul intreg id_client, numele string nume_client si cnp-ul string
        cnp_client, incearca sa-l valideze, apoi incearca sa modifice clientul de pe id-ul id_client
        cu cel nou creat
        :param id_client: intreg
        :param nume_client: string
        :param cnp_client: string
        :return: -
        :raises: ValidationError daca parametrii clientului sunt invalizi
                                 daca id_client < 0 -> "Id invalid!"
                                 daca nume_client == "" -> "Nume invalid!"
                                 daca len(cnp_client) != 13 -> "CNP invalid!"
                 RepoError daca id-ul clientului id_client nu exista
        '''
        client = Client(id_client, nume_client, cnp_client)
        self.__validator_client.valideaza(client)
        self.__repo_clienti.modifica_client(client)

    def gaseste_client(self, id_client):
        '''
        returneaza clientul cu id-ul intreg id_client
        :param id_client: intreg
        :return: clientul cu id-ul intreg id_client
        :raises: RepoError daca id-ul clientului id_client nu exista
        '''
        return self.__repo_clienti.cauta_client_dupa_id(id_client)
