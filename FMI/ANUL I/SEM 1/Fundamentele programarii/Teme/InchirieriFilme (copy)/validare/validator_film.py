from erori.validation_error import ValidationError


class ValidareFilm:

    def __init__(self):
        pass

    def valideaza(self, film):
        erori = ""
        if film.get_id_film() < 0:
            erori += "Id invalid!\n"
        if film.get_titlu_film() == "":
            erori += "Titlu invalid!\n"
        if film.get_gen_film() == "":
            erori += "Gen invalid!\n"
        if film.get_descriere_film() == "":
            erori += "Descriere invalida!\n"

        if len(erori) > 0:
            raise ValidationError(erori)
