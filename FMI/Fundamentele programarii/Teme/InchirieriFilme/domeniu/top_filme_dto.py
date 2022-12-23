class TopFilmeDTO:

    def __init__(self, titlu_film, nr_inchirieri):
        self.__titlu_film = titlu_film
        self.__nr_inchirieri = nr_inchirieri

    def get_titlu_film(self):
        return self.__titlu_film

    def __str__(self):
        return f"Filmul {self.__titlu_film} este inchiriat de {self.__nr_inchirieri} clienti"

    def __lt__(self, other):
        return self.__nr_inchirieri < other.__nr_inchirieri
