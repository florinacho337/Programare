from business.adauga_services import *
from business.cautari_services import *
from business.rapoarte_services import *
from business.stergeri_services import *
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
    lista = {}
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    assert(get_lungime_lista(lista) == 0)
    cheltuiala1 = cheltuiala(ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    adauga_cheltuiala_noua(lista, cheltuiala1)
    assert(get_lungime_lista(lista) == 1)


def teste_service_adaugari():
    lista = {}
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    assert(len(lista) == 0)
    adauga_cheltuiala_service(lista, ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    assert(len(lista) == 1)
    zi_cheltuiala_gresita = -1
    suma_cheltuiala_gresita = 0.0
    tip_cheltuiala_gresita = "iesiri"
    try:
        adauga_cheltuiala_service(lista, zi_cheltuiala_gresita, suma_cheltuiala_gresita, tip_cheltuiala_gresita)
        assert False
    except ValueError as ve:
        assert (str(ve) == "Zi invalida!\nSuma invalida!\nTip de cheltuiala invalid!")


def teste_service_stergeri():
    lista = {}
    ziua_cheltuiala = 12
    suma_cheltuiala = 75.6
    tip_cheltuiala = 'telefon'
    adauga_cheltuiala_service(lista, ziua_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    assert(get_lungime_lista(lista) == 1)
    adauga_cheltuiala_service(lista, 13, 10.5, 'altele')
    assert(get_lungime_lista(lista) == 2)
    sterge_cheltuieli_zi(lista, 12)
    assert(get_lungime_lista(lista) == 1)

    adauga_cheltuiala_service(lista, 15, 76.9, 'altele')
    assert(get_lungime_lista(lista) == 2)
    tip_stergere_cheltuieli = 'altele'
    sterge_cheltuieli_tip(lista, tip_stergere_cheltuieli)
    assert(get_lungime_lista(lista) == 0)

    adauga_cheltuiala_service(lista, 1, 12.9, 'telefon')
    adauga_cheltuiala_service(lista, 13, 10.5, 'altele')
    adauga_cheltuiala_service(lista, 15, 76.9, 'altele')
    adauga_cheltuiala_service(lista, 20, 10.4, 'mancare')
    assert(get_lungime_lista(lista) == 4)
    sterge_cheltuieli_perioada(lista, 10, 20)
    assert(get_lungime_lista(lista) == 1)


def teste_service_cautari():
    lista = {}
    cnt = 1
    lista[cnt] = cheltuiala(25, 7.0, "altele")
    cnt = cnt+1
    lista[cnt] = cheltuiala(10, 12.0, "telefon")
    cnt = cnt+1
    lista[cnt] = cheltuiala(12, 1.0, "mancare")
    assert(cheltuieli_mai_mari_decat_suma(lista, 5.0) == {1: [25, 7.0, 'altele'], 2: [10, 12.0, 'telefon']})

    ziua = 20
    suma = 10.0
    tip = "telefon"
    assert(cheltuieli_inainte_de_ziua_si_mai_mici_decat_suma(lista, ziua, suma) == {3: [12, 1.0, 'mancare']})
    assert(cheltuieli_de_tip(lista, tip) == {2: [10, 12.0, 'telefon']})


def teste_service_rapoarte():
    lista = {}
    cnt = 1
    lista[cnt] = cheltuiala(25, 7.0, "altele")
    cnt = cnt + 1
    lista[cnt] = cheltuiala(10, 12.0, "telefon")
    cnt = cnt + 1
    lista[cnt] = cheltuiala(12, 1.0, "telefon")
    tip = "telefon"
    assert(suma_totala_tip_cheltuiala(lista, tip) == 13.0)
    assert(zi_suma_maxima(lista) == 10)


def ruleaza_toate_testele():
    teste_cheltuieli()
    print("ok1")
    teste_validare_cheltuiala()
    print("ok2")
    teste_repository()
    print("ok3")
    teste_service_adaugari()
    print("ok4")
    teste_service_stergeri()
    print("ok5")
    teste_service_cautari()
    print("ok6")
    teste_service_rapoarte()
    print("ok7")
