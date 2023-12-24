//5. Gestiune cont bancar
//
//Creati o aplicatie care permite gestiunea tranzactiilor unui cont bancar.
//O tranzactie are urmatoarele elemente: ziua (ziua din luna in care s-a efectuat tranzactia),
//suma, tip (intrare/iesire), descriere.
//Aplicatia permite:
//a) adaugare de tranzactii
//b) modificare tranzactie existenta
//c) stergere  tranzactie existenta
//d) Vizualizare tranzactii dupa un criteriu (tranzactii de un anumit tip, tranzactii cu suma mai mare/mai mica decat o suma data)
//e) Vizualizare tranzactii ordonat dupa suma sau zi (crescator/descrescator)


#include "teste.h"
#include "ui.h"
#include<stdio.h>


int main()
{
    run_teste();
    Service repo;
    repo = createService();
    int status = 1;
    int status_criteriu;
    int optiune_criteriu;
    int status_ordine;
    int optiune;
    int ordine;
    int criteriu;

    while (status) {
        meniu();
        scanf("%d", &optiune);
        if (optiune == 0) {
            status = 0;
            printf("Exiting...");
        } else if (optiune == 1)
            ui_add(&repo);
        else if (optiune == 2)
            ui_modify(&repo);
        else if (optiune == 3)
            ui_delete(&repo);
        else if (optiune == 4) {
            status_criteriu = 1;
            while (status_criteriu) {
                printf("1. Vizualizati dupa tip: \n2. Vizualizati in functie de suma: \n");
                scanf("%d", &optiune_criteriu);
                if (optiune_criteriu == 1) {
                    status_criteriu = 0;
                    ui_print_by_type(&repo);

                } else if (optiune_criteriu == 2) {
                    status_criteriu = 0;
                    ui_print_by_sum(&repo);

                } else printf("Optiune inexistenta!\n");
            }
        } else if (optiune == 5) {
            status_criteriu = 1;
            while (status_criteriu) {
                printf("Sortati dupa criteriu (1. Dupa zi / 2. Dupa suma): \n");
                scanf("%d", &criteriu);
                if (criteriu == 1 || criteriu == 2) {
                    status_criteriu = 0;
                    status_ordine = 1;
                    while (status_ordine) {
                        printf("Ordine sortare (1. ascending / 2. descending): \n");
                        scanf("%d", &ordine);
                        if (ordine == 1 || ordine == 2)
                        {
                            status_ordine = 0;
                            ui_select_sort(&repo, criteriu, ordine);
                        }
                        else printf( "Ordine invalida!\n");
                    }

                }
                else printf("Criteriu invalid!\n");
            }
        } else if (optiune == 6)
            ui_print(&repo);
        else if (optiune == 7)
            ui_undo(&repo);
        else printf("Optiune invalida!\n");


    }
    destroyService(&repo);
    return 0;

}

