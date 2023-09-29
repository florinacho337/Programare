//
// Created by florin on 29.03.2023.
//

#ifndef LABREFACUT_SERVICE_H
#define LABREFACUT_SERVICE_H

#include "MyList.h"

typedef struct service{
    MyList* undoList;
    MyList* listaTranzactii;
}Service;

/*
 * creeaza un service
 */
Service createService();

/*
 * distruge service-ul
 */
void destroyService(Service* service);

//adauga in repo o tranzactie prin intermediul service-ului
//param id: id-ul tranzactiei
//type: int
//param zi: ziua tranzactiei
//type: int
//param suma: suma tranzactiei
//type: int
//param tip: tipul tranzactiei (intrare/iesire)
//type: string
//param descriere: descrierea tranzactiei
//type string
void service_add(Service* service, int zi, int suma, char* tip, char* descriere);

//sterge din repo o tranzactie prin intermediul service-ului
//param poz: pozitia tranzactiei
//type: int
void service_delete(Service* service, int poz);

//modifica in repo o tranzactie prin intermediul service-ului
//param poz: pozitia tranzactiei
//type: int
//param zi: ziua tranzactiei
//type: int
//param suma: suma tranzactiei
//type: int
//param tip: tipul tranzactiei (intrare/iesire)
//type: string
//param descriere: descrierea tranzactiei
//type string
void service_modify(Service* service, int poz, int zi, int suma, char* tip, char* descriere);

//creeaza un vector nou care contine doar tranzactiile care au un anumit tip (intrare/iesire)
//param criteriu: criteriul dupa care alegem tranzactiile (intrare/iesire)
//type: string
//returns:  un dynamic array repo_nou care contine doar tranzactile cu criteriul ales
//rtype: dynamic array de tip struct tranzactie
MyList* service_view_type(Service *service, char* criteriu);

//creeaza un vector nou care contine doar tranzactiile care au suma mai mare, respectiv mai mica decat suma data
//param suma: suma cu care comparam sumele tranzactiilor din repo
//type: int
//param ordine: "partea" din care punem tranzactiile din repo in lista noua (1-greater; 2-less)
//type: int
//returns:  un dynamic array repo_nou care contine doar tranzactile cu suma mai mica/mai mare decat suma data
//rtype: dynamic array de tip struct tranzactie
MyList* service_view_sum(Service *service, int suma, int ordine);

//sorteaza elementele din repo in functie de suma sau zi, in mod crescator/descrescator
//param criteriu: criteriul dupa care sortam elementele (1 = zi / 2 = suma)
//type: int
//param ordine: ordinea in care sortam elementele (1 = ascending / 2 = descending)
//type: int
//returns: un repo nou care contine elementele sortate
//rtype: dynamic array cu elemente de tip struct tranzactie
MyList* service_select_sort(Service * service, int criteriu, int ordine);

/*
 * reface ultima actiune
 * returneaza 1 daca nu se mai poate realiza undo
 *            0 altfel
 */
int service_undo(Service* service);

#endif //LABREFACUT_SERVICE_H
