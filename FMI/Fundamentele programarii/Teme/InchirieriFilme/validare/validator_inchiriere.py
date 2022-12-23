from erori.validation_error import ValidationError


class ValidareInchiriere:

    def __init__(self):
        pass

    def valideaza(self, inchiriere):
        '''
        valideaza p inchiriere daca id-ul este pozitiv
        :param: inchiriere: inchiriere
        :return: -
        :raises: ValidationError daca id-ul este invalid
                                 daca id_inchiriere < 0 -> "Id invalid!"
        '''
        erori = ""
        if inchiriere.get_id_inchiriere() < 0:
            erori += "Id invalid!\n"

        if len(erori) > 0:
            raise ValidationError(erori)