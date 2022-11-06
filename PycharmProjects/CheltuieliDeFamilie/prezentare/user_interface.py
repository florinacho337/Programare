from business.adauga_services import *
from business.cautari_services import *
from business.rapoarte_services import *
from business.stergeri_services import *
from business.filtrari_services import *
from business.undo_service import *
from business.afiseaza_service import *


def ui_vezi_cheltuieli(lista, undolist, params):
    if len(params) != 0:
        print("Numar de parametrii invalid!")
        return
    cheltuieli = afiseaza_cheltuieli(lista)
    pozitie = 1
    if cheltuieli == []:
        print("Nu exista cheltuieli!")
        return
    for cheltuiala in cheltuieli:
        print(f"{pozitie}.{cheltuiala}")
        pozitie = pozitie + 1


# 1.Adaugari
def ui_adauga_cheltuiala(lista, undolist, params):
    if len(params) != 3:
        print("Numar de parametrii invalid!")
        return
    zi_cheltuiala = int(params[0])
    suma_cheltuiala = float(params[1])
    tip_cheltuiala = params[2]
    adauga_cheltuiala_service(lista, undolist, zi_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    print("Cheltuiala adaugata cu succes!")


def ui_actualizeaza_cheltuiala(lista, undolist, params):
    if len(params) != 4:
        print("Numar de parametrii invalid!")
        return
    pozitie = int(params[0])
    zi_noua = int(params[1])
    suma_noua = float(params[2])
    tip_nou = params[3]
    actualizeaza_cheltuiala_service(lista, undolist, pozitie, zi_noua, suma_noua, tip_nou)
    print("Cheltuiala actualizata cu succes!")


# 2.Stergeri
def ui_sterge_cheltuieli_zi(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    zi_cheltuiala = int(params[0])
    sterge_cheltuieli_zi(lista, undolist, zi_cheltuiala)
    print("Cheltuieli sterse cu succes!")


def ui_sterge_cheltuieli_perioada(lista, undolist, params):
    if len(params) != 2:
        print("Numar de parametrii invalid!")
        return
    zi_inceput = int(params[0])
    zi_sfarsit = int(params[1])
    sterge_cheltuieli_perioada(lista, undolist, zi_inceput, zi_sfarsit)
    print("Cheltuieli sterse cu succes!")


def ui_sterge_cheltuieli_tip(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip_cheltuiala = params[0]
    sterge_cheltuieli_tip(lista, undolist, tip_cheltuiala)
    print("Cheltuieli sterse cu succes!")


# 3.Cautari
def ui_cheltuieli_mai_mari_decat(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    suma_cheltuiala = float(params[0])
    cheltuieli = cheltuieli_mai_mari_decat_suma(lista, suma_cheltuiala)
    for cheltuiala in cheltuieli:
        print(cheltuiala)


def ui_cheltuieli_inainte_de_si_mai_mici_decat(lista, undolist, params):
    if len(params) != 2:
        print("Numar de parametrii invalid!")
        return
    ziua = int(params[0])
    suma = float(params[1])
    cheltuieli = cheltuieli_inainte_de_ziua_si_mai_mici_decat_suma(lista, ziua, suma)
    for cheltuiala in cheltuieli:
        print(cheltuiala)


def ui_cheltuieli_de_tip(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip = params[0]
    afisare = cheltuieli_de_tip(lista, tip)
    for cheltuiala in afisare:
        print(cheltuiala)


# 4.Rapoarte
def ui_suma_totala_tip(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip_cheltuiala = params[0]
    print(
        f"Suma totala pentru cheltuielile de tip {tip_cheltuiala} este {suma_totala_tip_cheltuiala(lista, tip_cheltuiala)}.")


def ui_zi_suma_maxima(lista, undolist, params):
    if len(params) != 0:
        print("Numar de parametrii invalid!")
        return
    print(f"Ziua in care suma cheltuita este maxima este {zi_suma_maxima(lista)}.")


def ui_cheltuieli_de_suma(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    suma = float(params[0])
    afisare = cheltuieli_de_suma(lista, suma)
    for cheltuiala in afisare:
        print(cheltuiala)


# 5.Filtrari
def ui_elimina_cheltuieli_tip(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip = params[0]
    afisare = elimina_cheltuieli_tip(lista, tip)
    for cheltuiala in afisare:
        print(cheltuiala)


def ui_elimina_cheltuieli_mai_mici_decat(lista, undolist, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    suma = float(params[0])
    afisare = elimina_cheltuieli_mai_mici_decat(lista, suma)
    for cheltuiala in afisare:
        print(cheltuiala)


# 6.Undo
def ui_undo(lista, undolist, params):
    if len(params) != 0:
        print("Numar de parametrii invalid!")
        return
    try:
        undo_service(lista, undolist)
        print("Te-ai intors la lista anterioara cu succes!")
    except ValueError as ve:
        print(ve)


def menu():
    print("Selectati o optiune:")
    print("Afiseaza cheltuielile (vezi_cheltuieli)")
    print("Adauga cheltuiala noua (adauga_cheltuiala zi suma tip)")
    print("Modifica o cheltuiala (actualizeaza_cheltuiala pozitie zi_noua suma_noua tip_nou)")
    print("Sterge cheltuielile pentru o zi data (sterge_cheltuieli_zi zi)")
    print("Sterge cheltuielile pentru o perioada data (sterge_cheltuieli_perioada zi_inceput zi_sfarsit)")
    print("Sterge cheltuielile de un anumit tip (sterge_cheltuieli_tip tip)")
    print("Tipareste cheltuieli mai mari decat o suma (cheltuieli_mai_mari_decat suma)")
    print("Tipareste cheltuieli efectuate inainte de o zi si mai mici decat o suma (cheltuieli_inainte_de_mai_mici_decat zi suma)")
    print("Tipareste totalul pentru un tip de cheltuiala (suma_totala_tip tip)")
    print("Gaseste ziua in care suma cheltuita este maxima (zi_suma_maxima)")
    print("Tipareste toate cheltuielile de un anumit tip (cheltuieli_de_tip tip)")
    print("Tipareste toate cheltuielile ce au o anumita suma (cheltuieli_de_suma suma)")
    print("Elimina toate cheltuielile de un anumit tip (elimina_cheltuieli_tip tip)")
    print("Elimina toate cheltuielile mai mici decat o suma data (elimina_cheltuieli_mai_mici_decat suma)")
    print("Revino la pasul anterior (undo)")
    print("Iesire (exit)")


def ui():
    cheltuieli = []
    undolist = []
    print("Pentru a afisa meniul, tasteaza \"meniu\".")
    print("Pentru a iesi, tasteaza \"exit\".")
    while True:
        comenzi = {
            "adauga_cheltuiala": ui_adauga_cheltuiala,
            "cheltuieli_mai_mari_decat": ui_cheltuieli_mai_mari_decat,
            "cheltuieli_inainte_de_mai_mici_decat": ui_cheltuieli_inainte_de_si_mai_mici_decat,
            "suma_totala_tip": ui_suma_totala_tip,
            "zi_suma_maxima": ui_zi_suma_maxima,
            "cheltuieli_de_tip": ui_cheltuieli_de_tip,
            "sterge_cheltuieli_zi": ui_sterge_cheltuieli_zi,
            "vezi_cheltuieli": ui_vezi_cheltuieli,
            "sterge_cheltuieli_tip": ui_sterge_cheltuieli_tip,
            "sterge_cheltuieli_perioada": ui_sterge_cheltuieli_perioada,
            "actualizeaza_cheltuiala": ui_actualizeaza_cheltuiala,
            "cheltuieli_de_suma": ui_cheltuieli_de_suma,
            "elimina_cheltuieli_tip": ui_elimina_cheltuieli_tip,
            "elimina_cheltuieli_mai_mici_decat": ui_elimina_cheltuieli_mai_mici_decat,
            "undo": ui_undo
        }
        comanda = str(input(">>>"))
        comanda = comanda.strip()
        if comanda == "":
            continue
        if comanda == "exit":
            return
        if comanda == "meniu":
            menu()
            continue
        parti = comanda.split()
        nume_comanda = parti[0]
        params = parti[1:]
        if nume_comanda in comenzi:
            try:
                comenzi[nume_comanda](cheltuieli, undolist, params)
            except ValueError as ve:
                print(ve)
        else:
            print("Comanda invalida!")
