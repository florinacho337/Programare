class TopClientiDTO:

    def __init__(self, nume_client, nr_inchirieri):
        self.__nume_client = nume_client
        self.__nr_inchirieri = nr_inchirieri

    def get_nume(self):
        return self.__nume_client

    def __lt__(self, other):
        return self.__nr_inchirieri < other.__nr_inchirieri

    def __str__(self):
        return f"{self.__nume_client} are {self.__nr_inchirieri} filme inchiriate"
