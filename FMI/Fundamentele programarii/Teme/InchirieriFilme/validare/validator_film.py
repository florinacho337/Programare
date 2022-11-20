from erori.validation_error import ValidationError


class ValidareFilm:

    def __init__(self):
        pass

    def valideaza(self, film):
        '''
        valideaza un film daca id-ul este pozitiv, si daca titlul, descrierea si genul
        sunt nevide
        :param film: film
        :return: -
        :raises: ValidationError daca parametrii filmului sunt invalizi
                                 daca id_film < 0 -> "Id invalid!"
                                 daca titlu_film == "" -> "Titlu invalid!"
                                 daca gen_film == "" -> "Gen invalid!"
                                 daca descriere_film == "" -> "Descriere invalida!"
        '''
        erori = ""
        if film.get_id_film() < 0:
            erori += "Id invalid!\n"
        if film.get_titlu_film() == "":
            erori += "Titlu invalid!\n"
        if film.get_gen_film() == "":
            erori += "Gen invalid!\n"
        if film.get_descriere_film() == "":
            erori += "Descriere invalida!"

        if len(erori) > 0:
            raise ValidationError(erori)
