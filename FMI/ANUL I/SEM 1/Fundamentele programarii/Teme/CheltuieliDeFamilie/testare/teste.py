from business.adauga_services import *
from business.cautari_services import *
from business.filtrari_services import *
from business.rapoarte_services import *
from business.stergeri_services import *
from business.undo_service import undo_service
from domain.cheltuiala import *
from infrastructura.repository_cheltuieli import *
from validare.validator_cheltuiala import valideaza_cheltuiala


def teste_cheltuieli():
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    cheltuiala1 = cheltuiala(ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    assert(get_zi_cheltuiala(cheltuiala1) == ziua_cheltuiala)
    assert(abs(get_suma_cheltuiala(cheltuiala1) - suma_cheltuiala) < 0.00001)
    assert(get_tip_cheltuiala(cheltuiala1) == tip_cheltuiala)

    ziua_cheltuiala_noua = 14
    suma_cheltuiala_noua = 12.5
    tip_cheltuiala_nou = 'altele'
    set_zi_cheltuiala(cheltuiala1, ziua_cheltuiala_noua)
    assert(get_zi_cheltuiala(cheltuiala1) == ziua_cheltuiala_noua)
    set_suma_cheltuiala(cheltuiala1, suma_cheltuiala_noua)
    assert(abs(get_suma_cheltuiala(cheltuiala1) - suma_cheltuiala_noua) < 0.00001)
    set_tip_cheltuiala(cheltuiala1, tip_cheltuiala_nou)
    assert(get_tip_cheltuiala(cheltuiala1) == tip_cheltuiala_nou)


def teste_validare_cheltuiala():
    cheltuiala_gresita = cheltuiala(-1, 0.0, "iesiri")
    try:
        valideaza_cheltuiala(cheltuiala_gresita)
        assert False
    except ValueError as ve:
        assert(str(ve) == "Zi invalida!\nSuma invalida!\nTip de cheltuiala invalid!")


def teste_repository():
    lista = []
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    assert(get_lungime_lista(lista) == 0)
    cheltuiala1 = cheltuiala(ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    adauga_cheltuiala_noua(lista, cheltuiala1)
    assert(get_lungime_lista(lista) == 1)
    assert(get_cheltuieli(lista) == [[12, 75.6, 'telefon']])
    zi_noua = 13
    suma_noua = 73.2
    tip_nou = 'altele'
    actualizeaza_cheltuiala(lista, 1, zi_noua, suma_noua, tip_nou)
    assert(get_lungime_lista(lista) == 1)
    assert(get_cheltuieli(lista) == [[13, 73.2, 'altele']])


def teste_service_adaugari():
    lista = []
    undolist = []
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    assert(get_lungime_lista(lista) == 0)
    adauga_cheltuiala_service(lista, undolist, ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    assert(get_lungime_lista(lista) == 1)
    zi_cheltuiala_gresita = -1
    suma_cheltuiala_gresita = 0.0
    tip_cheltuiala_gresita = "iesiri"
    try:
        adauga_cheltuiala_service(lista, undolist, zi_cheltuiala_gresita, suma_cheltuiala_gresita, tip_cheltuiala_gresita)
        assert False
    except ValueError as ve:
        assert (str(ve) == "Zi invalida!\nSuma invalida!\nTip de cheltuiala invalid!")
    assert(get_lungime_lista(lista) == 1)
    zi_cheltuiala_actualizata = 15
    suma_cheltuiala_actualizata = 22.3
    tip_cheltuiala_actualizata = 'mancare'
    pozitie = 1
    actualizeaza_cheltuiala_service(lista, undolist, pozitie, zi_cheltuiala_actualizata, suma_cheltuiala_actualizata, tip_cheltuiala_actualizata)
    assert(get_lungime_lista(lista) == 1)
    assert(get_cheltuieli(lista) == [[15, 22.3, 'mancare']])
    zi_cheltuiala_actualizata = 1
    suma_cheltuiala_actualizata = 2.0
    tip_cheltuiala_actualizata = 'altele'
    pozitie_gresita = -1
    try:
        actualizeaza_cheltuiala_service(lista, undolist, pozitie_gresita, zi_cheltuiala_actualizata, suma_cheltuiala_actualizata, tip_cheltuiala_actualizata)
        assert False
    except ValueError as ve:
        assert(str(ve) == "Pozitie inexistenta!\n")


def teste_service_stergeri():
    lista = []
    undolist = []
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    adauga_cheltuiala_service(lista, undolist, ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    assert(get_lungime_lista(lista) == 1)
    adauga_cheltuiala_service(lista, undolist, 13, 10.5, 'altele')
    assert(get_lungime_lista(lista) == 2)
    sterge_cheltuieli_zi(lista, undolist, 12)
    assert(get_lungime_lista(lista) == 1)

    adauga_cheltuiala_service(lista, undolist, 15, 76.9, 'altele')
    assert(get_lungime_lista(lista) == 2)
    tip_stergere_cheltuieli = 'altele'
    sterge_cheltuieli_tip(lista, undolist, tip_stergere_cheltuieli)
    assert(get_lungime_lista(lista) == 0)

    adauga_cheltuiala_service(lista, undolist, 1, 12.9, 'telefon')
    adauga_cheltuiala_service(lista, undolist, 13, 10.5, 'altele')
    adauga_cheltuiala_service(lista, undolist, 15, 76.9, 'altele')
    adauga_cheltuiala_service(lista, undolist, 20, 10.4, 'mancare')
    assert(get_lungime_lista(lista) == 4)
    sterge_cheltuieli_perioada(lista, undolist, 10, 20)
    assert(get_lungime_lista(lista) == 1)


def teste_service_cautari():
    lista = []
    cheltuiala1 = cheltuiala(25, 7.0, "altele")
    cheltuiala2 = cheltuiala(10, 12.0, "telefon")
    cheltuiala3 = cheltuiala(12, 1.0, "mancare")
    adauga_cheltuiala_noua(lista, cheltuiala1)
    adauga_cheltuiala_noua(lista, cheltuiala2)
    adauga_cheltuiala_noua(lista, cheltuiala3)
    assert(cheltuieli_mai_mari_decat_suma(lista, 5.0) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon']])

    ziua = 20
    suma = 10.0
    tip = "telefon"
    assert(cheltuieli_inainte_de_ziua_si_mai_mici_decat_suma(lista, ziua, suma) == [[12, 1.0, 'mancare']])
    assert(cheltuieli_de_tip(lista, tip) == [[10, 12.0, 'telefon']])


def teste_service_rapoarte():
    lista = []
    cheltuiala1 = cheltuiala(25, 7.0, "altele")
    cheltuiala2 = cheltuiala(10, 12.0, "telefon")
    cheltuiala3 = cheltuiala(12, 1.0, "telefon")
    adauga_cheltuiala_noua(lista, cheltuiala1)
    adauga_cheltuiala_noua(lista, cheltuiala2)
    adauga_cheltuiala_noua(lista, cheltuiala3)
    tip = "telefon"
    assert(suma_totala_tip_cheltuiala(lista, tip) == 13.0)
    assert(zi_suma_maxima(lista) == 10)
    suma = 12.000000000001
    assert(cheltuieli_de_suma(lista, suma) == [[10, 12.0, 'telefon']])


def teste_service_filtrari():
    lista = []
    cheltuiala1 = cheltuiala(25, 7.0, "altele")
    cheltuiala2 = cheltuiala(10, 12.0, "telefon")
    cheltuiala3 = cheltuiala(12, 1.0, "telefon")
    adauga_cheltuiala_noua(lista, cheltuiala1)
    adauga_cheltuiala_noua(lista, cheltuiala2)
    adauga_cheltuiala_noua(lista, cheltuiala3)
    tip_eliminat = "telefon"
    assert(elimina_cheltuieli_tip(lista, tip_eliminat) == [[25, 7.0, 'altele']])
    assert(get_lungime_lista(lista) == 3)
    assert(elimina_cheltuieli_mai_mici_decat(lista, 10.5) == [[10, 12.0, 'telefon']])
    assert(get_lungime_lista(lista) == 3)


def teste_service_undo():
    lista = []
    undolist = []
    try:
        undo_service(lista, undolist)
        assert False
    except ValueError as ve:
        assert(str(ve) == "Nu se mai poate da undo!")
    adauga_cheltuiala_service(lista, undolist, 25, 7.0, "altele")
    adauga_cheltuiala_service(lista, undolist, 10, 12.0, "telefon")
    adauga_cheltuiala_service(lista, undolist, 12, 1.0, "telefon")
    assert(get_lungime_lista(lista) == 3)
    undo_service(lista, undolist)
    assert(get_lungime_lista(lista) == 2)
    assert(get_cheltuieli(lista) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon']])
    adauga_cheltuiala_service(lista, undolist, 12, 1.0, "telefon")
    assert(get_lungime_lista(lista) == 3)
    zi_noua = 13
    suma_noua = 73.2
    tip_nou = 'altele'
    actualizeaza_cheltuiala_service(lista, undolist, 2, zi_noua, suma_noua, tip_nou)
    assert(get_cheltuieli(lista) == [[25, 7.0, 'altele'], [13, 73.2, 'altele'], [12, 1.0, 'telefon']])
    undo_service(lista, undolist)
    assert(get_cheltuieli(lista) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon'], [12, 1.0, 'telefon']])
    sterge_cheltuieli_zi(lista, undolist, 25)
    assert(get_lungime_lista(lista) == 2)
    undo_service(lista, undolist)
    assert(get_lungime_lista(lista) == 3)
    assert(get_cheltuieli(lista) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon'], [12, 1.0, 'telefon']])
    sterge_cheltuieli_tip(lista, undolist, 'telefon')
    assert(get_lungime_lista(lista) == 1)
    undo_service(lista, undolist)
    assert(get_lungime_lista(lista) == 3)
    assert (get_cheltuieli(lista) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon'], [12, 1.0, 'telefon']])
    sterge_cheltuieli_perioada(lista, undolist, 10, 25)
    assert(get_lungime_lista(lista) == 0)
    undo_service(lista, undolist)
    assert(get_lungime_lista(lista) == 3)
    assert(get_cheltuieli(lista) == [[25, 7.0, 'altele'], [10, 12.0, 'telefon'], [12, 1.0, 'telefon']])


def ruleaza_toate_testele():
    teste_cheltuieli()
    teste_validare_cheltuiala()
    teste_repository()
    teste_service_adaugari()
    teste_service_stergeri()
    teste_service_cautari()
    teste_service_rapoarte()
    teste_service_filtrari()
    teste_service_undo()
    