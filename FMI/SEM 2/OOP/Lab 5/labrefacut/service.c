#include "MyList.h"
#include "domain.h"
#include "service.h"
#include <string.h>

Service createService(){
    Service rez;
    rez.undoList = createEmpty((DestroyFct)destroyList);
    rez.listaTranzactii = createEmpty((DestroyFct)destroyTranzactie);
    return rez;
}

void destroyService(Service* service){
    destroyList(service->listaTranzactii);
    destroyList(service->undoList);
}

void service_add(Service* service, int zi, int suma, char* tip, char* descriere)
{
    Tranzactie* tranzactie = creeazaTranzactie(zi, suma, tip, descriere);
    MyList* toUndo = copyList(service->listaTranzactii, (CopyFct)copyTranzactie);
    add(service->listaTranzactii, tranzactie);
    add(service->undoList, toUndo);
}

void service_delete(Service* service, int poz)
{
    MyList* toUndo = copyList(service->listaTranzactii, (CopyFct)copyTranzactie);
    removeP(service->listaTranzactii, poz);
    add(service->undoList, toUndo);
}

void service_modify(Service* service, int poz, int zi, int suma, char* tip, char* descriere)
{
    Tranzactie* tranzactie = creeazaTranzactie(zi, suma, tip, descriere);
    MyList* toUndo = copyList(service->listaTranzactii, (CopyFct)copyTranzactie);
    Tranzactie* tr = set(service->listaTranzactii, poz, tranzactie);
    destroyTranzactie(tr);
    add(service->undoList, toUndo);
}


MyList* service_view_type(Service *service, char* criteriu) {
    MyList *repo_nou;
    repo_nou = createEmpty((DestroyFct)destroyTranzactie);
    int i;
    if(strcmp(criteriu,"intrare") == 0) {
        for (i = 0; i < size(service->listaTranzactii); i++) {
            Tranzactie *tr = (Tranzactie *) get(service->listaTranzactii, i);
            if (strcmp(tr->tip, "intrare") == 0) {
                add(repo_nou, copyTranzactie(tr));
            }
        }
    }
    else if (strcmp(criteriu,"iesire") == 0)
    {
        for(i=0; i<size(service->listaTranzactii); i++) {
            Tranzactie *tr = (Tranzactie*) get(service->listaTranzactii, i);
            if (strcmp(tr->tip, "iesire") == 0) {
                add(repo_nou, copyTranzactie(tr));
            }
        }
    }
    return repo_nou;
}

MyList* service_view_sum(Service *service, int suma, int ordine){
    MyList* repo_nou;
    repo_nou = createEmpty((DestroyFct)destroyTranzactie);
    int i;
    //luam ordine = 1 ca greater si ordine = 2 ca less
    if (ordine == 1)
    {
        for(i=0;i<size(service->listaTranzactii);i++)
        {
            Tranzactie *tr = (Tranzactie*) get(service->listaTranzactii, i);
            if(tr->suma >= suma)
                add(repo_nou, copyTranzactie(tr));
        }
    }
    else if (ordine == 2)
    {
        for(i=0;i<size(service->listaTranzactii);i++)
        {
            Tranzactie *tr = (Tranzactie*) get(service->listaTranzactii, i);
            if(tr->suma <= suma)
                add(repo_nou, copyTranzactie(tr));
        }
    }
    return repo_nou;
}

MyList* service_select_sort(Service * service, int criteriu, int ordine) {
    int i, j;
    MyList* repo_nou;
    repo_nou = copyList(service->listaTranzactii, (CopyFct)copyTranzactie);
    for (i = 0; i < size(service->listaTranzactii)-1; i++)
                for (j = i + 1; j < size(service->listaTranzactii); j++)
                {
                    Tranzactie * tr1 = (Tranzactie *)get(repo_nou, i);
                    Tranzactie * tr2 = (Tranzactie *)get(repo_nou, j);
                    if (criteriu == 1 && ordine == 1 && tr1->suma > tr2->suma && tr1->suma != 0 && tr2->suma != 0)
                    {
                        set(repo_nou, i, tr2);
                        set(repo_nou, j, tr1);
                    }
                    else if (criteriu == 1 && ordine == 2 && tr1->suma < tr2->suma && tr1->suma != 0 && tr2->suma != 0)
                    {
                        set(repo_nou, i, tr2);
                        set(repo_nou, j, tr1);
                    }
                    else if (criteriu == 2 && ordine == 1 && tr1->zi > tr2->zi && tr1->zi != 0 && tr2->zi != 0)
                    {
                        set(repo_nou, i, tr2);
                        set(repo_nou, j, tr1);
                    }
                    else if (criteriu == 2 && ordine == 2 && tr1->zi < tr2->zi && tr1->zi != 0 && tr2->zi != 0)
                    {
                        set(repo_nou, i, tr2);
                        set(repo_nou, j, tr1);
                    }
                }
    return repo_nou;

}

int service_undo(Service* service){
    if (size(service->undoList) == 0)
        return 1;
    destroyList(service->listaTranzactii);
    service->listaTranzactii = removeLast(service->undoList);
    return 0;
}