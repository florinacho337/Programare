class Film:

    def __init__(self, id_film, titlu_film, descriere_film, gen_film):
        self.__id_film = id_film
        self.__titlu_film = titlu_film
        self.__descriere_film = descriere_film
        self.__gen_film = gen_film

    def get_id_film(self):
        return int(self.__id_film)

    def get_titlu_film(self):
        return self.__titlu_film

    def get_descriere_film(self):
        return self.__descriere_film

    def get_gen_film(self):
        return self.__gen_film

    def set_titlu_film(self, titlu_film):
        self.__titlu_film = titlu_film

    def set_descriere_film(self, descriere_film):
        self.__descriere_film = descriere_film

    def set_gen_film(self, gen_film):
        self.__gen_film = gen_film

    def __eq__(self, other):
        return self.__id_film == other.__id_film

    def __str__(self):
        return f"{self.__id_film}. {self.__titlu_film}, {self.__gen_film}, {self.__descriere_film}"
