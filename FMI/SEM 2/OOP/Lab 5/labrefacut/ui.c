#include <stdio.h>
#include "service.h"
#include <malloc.h>
#include <string.h>
#include "MyList.h"
#include "domain.h"
#include <stdbool.h>

void meniu()
{
    printf("1. Adaugati o tranzactie: \n");
    printf("2. Modificati o tranzactie: \n");
    printf("3. Stergeti o tranzactie: \n");
    printf("4. Vizualizati tranzactiile dupa un criteriu: \n");
    printf("5. Vizualizati tranzactiile ordonate: \n");
    printf("6. Vizualizati toate tranzactiile: \n");
    printf("7. Undo ultima operatie efectuata:\n");
    printf("0. Iesire din aplicatie.\n");
}

void ui_add(Service* repo_ui){
    int zi, suma;
    char* tip = (char*)malloc(100);
    char* descriere = (char*)malloc(100);
    bool intrare = true;
    while (intrare) {
        printf("Introduceti ziua tranzactiei: \n");
        scanf("%d", &zi);
        printf("Introduceti suma tranzactiei: \n");
        scanf("%d", &suma);
        printf("Introduceti tipul tranzactiei (intrare/iesire): \n");
        scanf("%s", tip);
        printf("Introduceti descrierea tranzactiei: \n");
        scanf("%s", descriere);
        if (strcmp(tip, "intrare") == 0 || strcmp(tip, "iesire") == 0)
            intrare = false;
        else printf("Tip invalid!\n");
    }
    service_add(repo_ui, zi, suma, tip, descriere);
    free(tip);
    free(descriere);
    printf("Tranzactia a fost adaugata cu succes!\n");
}

void ui_delete(Service* repo_ui)
{
    int poz;
    printf("Introduceti pozitia tranzactiei pe care doriti s-o stergeti: \n");
    scanf("%d", &poz);
    service_delete(repo_ui, poz);
    printf("Tranzactia a fost stearsa cu succes!\n");
}

void ui_modify(Service * repo)
{
    int poz, zi, suma;
    char* tip = (char*)malloc(100);
    char* descriere = (char*)malloc(100);
    bool intrare = true;
    while (intrare) {
        printf("Introduceti pozitia tranzactiei pe care doriti sa o stergeti:\n");
        scanf("%d", &poz);
        printf("Introduceti ziua tranzactiei: \n");
        scanf("%d",&zi);
        printf("Introduceti suma tranzactiei: \n");
        scanf("%d", &suma);
        printf("Introduceti tipul tranzactiei (intrare/iesire): \n");
        scanf("%s", tip);
        printf("Introduceti descrierea tranzactiei: \n");
        scanf("%s", descriere);
        if (strcmp(tip, "intrare") == 0 || strcmp(tip, "iesire") == 0)
            intrare = false;
        else printf("Tip invalid!\n");
        service_modify(repo, poz, zi, suma, tip, descriere);
        printf("Tranzactie modificata cu succes!\n");
    }
    free(tip);
    free(descriere);
}

void ui_print(Service * repo)
{
    int i;
    int nr = 0;
    for (i =0; i< size(repo->listaTranzactii); i++) {
        Tranzactie* tr = (Tranzactie*)get(repo->listaTranzactii, i);
        if (tr->suma != 0) {
            printf("%d. %d %d %s %s\n", i, tr->zi, tr->suma, tr->tip, tr->descriere);
            nr++;
        }
    }
    if (nr==0)
        printf("Nu exista tranzactii!\n");

}


void ui_print_by_type(Service *repo) {
    char* tip = (char*)malloc(100);
    MyList *repo_nou;
    int i;
    int nr = 0;
    bool run = true;
    while(run){
        printf("Alegeti tipul (intrare/iesire):\n");
        scanf("%s", tip);
        if(strcmp(tip,"intrare") == 0 || strcmp(tip,"iesire")==0) {
            run = false;
            repo_nou = service_view_type(repo, tip);
        }
        else printf("Tip invalid!\n");
    }
    for(i=0;i<= size(repo_nou);i++) {
        Tranzactie* tr = (Tranzactie*) get(repo_nou, i);
        if (tr->suma != 0) {
            printf("%d. %d %d %s %s\n", i, tr->zi, tr->suma, tr->tip, tr->descriere);
            nr++;
        }
    }
    if(nr==0) printf("Nu exista tranzactii cu acest tip!\n");
}

void ui_print_by_sum(Service* repo){
    int ordine;
    bool run = true;
    int i;
    int suma;
    int nr = 0;
    MyList* repo_nou;
    printf("Introduceti suma: \n");
    scanf("%d", &suma);
    printf("Introduceti ordinea (1. Greater/ 2. Less): \n");
    while(run){
    scanf("%d", &ordine);
    if (ordine == 1 || ordine == 2) {
        run = false;
        repo_nou = service_view_sum(repo, suma, ordine);
    }
    else printf("Optiune invalida!\n");

    }
    for(i=0;i< size(repo_nou);i++) {
        Tranzactie *tr = (Tranzactie*)get(repo_nou, i);
        if (tr->suma != 0) {
            printf("%d. %d %d %s %s\n", i, tr->zi, tr->suma, tr->tip, tr->descriere);
            nr++;
        }
    }
    if (nr==0) printf("Nu exista tranzactii cu aceasta suma!\n");


}

void ui_select_sort(Service* repo_ui, int criteriu, int ordine)
{
    MyList * repo_nou;
    repo_nou = service_select_sort(repo_ui, criteriu, ordine);
    int i;
    int nr = 0;
    for(i=0;i< size(repo_nou);i++) {
        Tranzactie *tr = (Tranzactie*)get(repo_nou, i);
        if (tr->suma != 0) {
            printf("%d. %d %d %s %s\n", i, tr->zi, tr->suma, tr->tip, tr->descriere);
            nr++;
        }
    }
    if (nr==0)
        printf("Nu exista tranzactii!\n");
}

void ui_undo(Service* service){
    int undo = service_undo(service);
    if(undo == 1)
        printf("Nu se mai poate da undo!\n");
    else
        printf("Undo executat cu succes!\n");
}