//
// Created by florin on 29.03.2023.
//

#ifndef LABREFACUT_UI_H
#define LABREFACUT_UI_H

#include "service.h"

//afisaza meniul principal al programului
void meniu();

//adauga in repo din ui, prin intermediul service-ului
void ui_add(Service* repo_ui);

//sterge din repo din ui prin intermediul service-ului
void ui_delete(Service* repo_ui);

//modifica in repo din ui prin intermediul service-ului
void ui_modify(Service * repo);

//afiseaza elementele din repo
void ui_print(Service * repo);

//afiseaza elementele din repo in functie de tipul tranzactiei
void ui_print_by_type(Service *repo);

void ui_print_by_sum(Service* repo);

void ui_select_sort(Service* repo_ui, int criteriu, int ordine);

/*
 * reface ultima operatie
 */
void ui_undo(Service* service);
#endif //LABREFACUT_UI_H
