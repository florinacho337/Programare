from domain.cheltuiala import get_tip_cheltuiala, get_suma_cheltuiala, get_zi_cheltuiala


def valideaza_cheltuiala(cheltuiala):
    '''
    valideaza o cheltuiala daca ziua apartine intervalului [1, 31], suma este pozitiva si nenula, iar tipul
    este unul din urmatoarele: "mancare", "intretinere", "imbracaminte", "telefon", "altele"
    :param cheltuiala: cheltuiala
    :return: -
    :raises: ValueError daca cel putin o data din player este gresita:
                        daca ziua < 1 sau ziua > 31 -> "Zi invalida!\n"
                        daca suma <= 0 -> "Suma invalida!\n"
                        daca tip nu apartine ["mancare", "intretinere", "imbracaminte", "telefon", "altele"] -> "Tip de cheltuiala invalid!\n"
    '''
    errors = ""
    tipuri = ["mancare", "intretinere", "imbracaminte", "telefon", "altele"]
    if get_zi_cheltuiala(cheltuiala) < 1 or get_zi_cheltuiala(cheltuiala) > 31:
        errors += "Zi invalida!"
    if get_suma_cheltuiala(cheltuiala) <= 0:
        errors += "\nSuma invalida!"
    if not(get_tip_cheltuiala(cheltuiala) in tipuri):
        errors += "\nTip de cheltuiala invalid!"

    if len(errors) > 0:
        raise ValueError(errors)
