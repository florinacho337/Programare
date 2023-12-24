from domeniu.client import Client
import random
import string


class ServiceClient:

    def __init__(self, validator_client, repo_clienti):
        self.__validator_client = validator_client
        self.__repo_clienti = repo_clienti
        self.__cifre = string.digits
        self.__litere = string.ascii_lowercase

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

    def genereaza_client(self):
        '''
        se genereaza un client cu un id intreg intre 0 si 100, un nume de lungimea len_nume si
        un cnp din 13 cifre in format string
        :return: -
        '''
        id_client = random.randrange(0, 100)
        while id_client in self.__repo_clienti.get_all_ids():
            id_client = random.randrange(0, 100)
        nume_client = "".join(random.choice(self.__litere) for i in range(10))
        cnp_client = "".join(random.choice(self.__cifre) for i in range(13))
        client = Client(id_client, nume_client, cnp_client)
        self.__repo_clienti.adauga_client(client)

    def get_clienti_dupa_nume(self):
        '''
        returneaza clientii sortati dupa nume
        :return: clientii sortati dupa nume
        complexitate: O(nlogn), unde n este numarul de clienti

        '''
        clienti = self.__repo_clienti.get_all()
        clienti.sort()
        return clienti

