class InchiriereFilm:

    def __init__(self, id_inchiriere, id_client, id_film):
        self.__id_inchiriere = id_inchiriere
        self.__id_client = id_client
        self.__id_film = id_film

    def get_id_inchiriere(self):
        return self.__id_inchiriere

    def get_id_client(self):
        return self.__id_client

    def get_id_film(self):
        return self.__id_film

    def __str__(self):
        return f"{self.__id_inchiriere},{self.__id_client},{self.__id_film}"
