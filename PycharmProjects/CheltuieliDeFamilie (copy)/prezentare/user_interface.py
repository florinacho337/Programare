from business.adauga_services import *
from business.cautari_services import *
from business.rapoarte_services import *
from business.stergeri_services import *
from infrastructura.repository_cheltuieli import get_cheltuieli


def ui_vezi_cheltuieli(lista, params):
    if len(params) != 0:
        print("Numar de parametrii invalid!")
        return
    cheltuieli = get_cheltuieli(lista)
    pozitie = 1
    for cheltuiala in cheltuieli:
        print(f"{pozitie}.{cheltuiala}")
        pozitie = pozitie + 1


def ui_adauga_cheltuiala(lista, params):
    if len(params) != 3:
        print("Numar de parametrii invalid!")
        return
    zi_cheltuiala = int(params[0])
    suma_cheltuiala = float(params[1])
    tip_cheltuiala = params[2]
    adauga_cheltuiala_service(lista, zi_cheltuiala, suma_cheltuiala, tip_cheltuiala)
    print("Cheltuiala adaugata cu succes!")


def ui_sterge_cheltuieli_zi(lista, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    zi_cheltuiala = int(params[0])
    sterge_cheltuieli_zi(lista, zi_cheltuiala)
    print("Cheltuieli sterse cu succes!")


def ui_sterge_cheltuieli_perioada(lista, params):
    if len(params) != 2:
        print("Numar de parametrii invalid!")
        return
    zi_inceput = params[0]
    zi_sfarsit = params[1]
    sterge_cheltuieli_perioada(lista, zi_inceput, zi_sfarsit)
    print("Cheltuieli sterse cu succes!")


def ui_sterge_cheltuieli_tip(lista, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip_cheltuiala = params[0]
    sterge_cheltuieli_tip(lista, tip_cheltuiala)
    print("Cheltuieli sterse cu succes!")


def ui_cheltuieli_mai_mari_decat(lista, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    suma_cheltuiala = float(params[0])
    cheltuieli = cheltuieli_mai_mari_decat_suma(lista, suma_cheltuiala)
    for cheltuiala in cheltuieli:
        print(cheltuiala)


def ui_cheltuieli_inainte_de_si_mai_mici_decat(lista, params):
    if len(params) != 2:
        print("Numar de parametrii invalid!")
        return
    ziua = int(params[0])
    suma = float(params[1])
    cheltuieli = cheltuieli_inainte_de_ziua_si_mai_mici_decat_suma(lista, ziua, suma)
    for cheltuiala in cheltuieli:
        print(cheltuiala)

def ui_suma_totala_tip(lista, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip_cheltuiala = params[0]
    print(f"Suma totala pentru cheltuielile de tip {tip_cheltuiala} este {suma_totala_tip_cheltuiala(lista, tip_cheltuiala)}.")


def ui_zi_suma_maxima(lista, params):
    if len(params) != 0:
        print("Numar de parametrii invalid!")
        return
    print(f"Ziua in care suma cheltuita este maxima este {zi_suma_maxima(lista)}.")


def ui_cheltuieli_de_tip(lista, params):
    if len(params) != 1:
        print("Numar de parametrii invalid!")
        return
    tip = params[0]
    afisare = cheltuieli_de_tip(lista, tip)
    for cheltuiala in afisare:
        print(cheltuiala)


def menu():
    print("Selectati o optiune:")
    print("Afiseaza cheltuielile (vezi_cheltuieli)")
    print("Adauga cheltuiala noua (adauga_cheltuiala zi suma tip)")
    print("Sterge cheltuielile pentru o zi data (sterge_cheltuieli_zi zi)")
    print("Sterge cheltuielile pentru o perioada data (sterge_cheltuieli_perioada zi_inceput zi_sfarsit)")
    print("Sterge cheltuielile de un anumit tip (sterge_cheltuieli_tip tip)")
    print("Tipareste cheltuieli mai mari decat o suma (cheltuieli_mai_mari_decat suma)")
    print("Tipareste cheltuieli efectuate inainte de o zi si mai mici decat o suma (cheltuieli_inainte_de_mai_mici_decat zi suma)")
    print("Tipareste totalul pentru un tip de cheltuiala (suma_totala_tip tip)")
    print("Gaseste ziua in care suma cheltuita este maxima (zi_suma_maxima)")
    print("Tipareste toate cheltuielile de un anumit tip (cheltuieli_de_tip tip)")
    print("Iesire (exit)")


def ui():
    cheltuieli = {

    }
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
            "sterge_cheltuieli_perioada": ui_sterge_cheltuieli_perioada
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
                comenzi[nume_comanda](cheltuieli, params)
            except ValueError as ve:
                print(ve)
        else:
            print("Comanda invalida!")