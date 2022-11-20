from erori.validation_error import ValidationError


class ValidareClient:

    def __int__(self):
        pass

    def valideaza(self, client):
        '''
        valideaza un client daca id-ul este pozitiv, daca numele este nevid, iar cnp-ul are 13 caractere
        :param client: client
        :return: -
        :raises: ValidationError daca parametrii clientului sunt invalizi
                                 daca id_client < 0 -> "Id invalid!"
                                 daca nume_client == "" -> "Nume invalid!"
                                 daca len(cnp_client) != 13 -> "CNP invalid!"
        '''
        errors = ""
        if client.get_id_client() < 0:
            errors += "Id invalid!\n"
        if client.get_nume_client() == "":
            errors += "Nume invalid!\n"
        if len(client.get_cnp_client()) != 13:
            errors += "CNP invalid!"

        if len(errors) > 0:
            raise ValidationError(errors)
