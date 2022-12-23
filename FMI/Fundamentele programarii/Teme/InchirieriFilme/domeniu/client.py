class Client:

    def __init__(self, id_client, nume_client, cnp_client):
        self.__id_client = id_client
        self.__nume_client = nume_client
        self.__cnp_client = cnp_client

    def get_id_client(self):
        return self.__id_client

    def get_nume_client(self):
        return self.__nume_client

    def get_cnp_client(self):
        return self.__cnp_client

    def set_nume_client(self, nume_nou):
        self.__nume_client = nume_nou

    def set_cnp_client(self, cnp_nou):
        self.__cnp_client = cnp_nou

    def __eq__(self, other):
        return self.__id_client == other.__id_client

    def __str__(self):
        return f"{self.__id_client},{self.__nume_client},{self.__cnp_client}"

    def __lt__(self, other):
        return self.__nume_client < other.__nume_client



