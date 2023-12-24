//
// Created by florin on 29.03.2023.
//

#ifndef LABREFACUT_DOMAIN_H
#define LABREFACUT_DOMAIN_H

//structul care tine locul unui "obiect" de tip tranzactie
//param zi: ziua tranzactiei
//type: int
//param suma: suma tranzactiei
//type: int
//param tip: tipul tranzactiei (intrare/iesire)
//type: string
//param descriere: descrierea tranzactiei
//type string
typedef struct tranzactie{
    int zi;
    int suma;
    char* tip;
    char* descriere;
}Tranzactie;

/*
 * creeaza o tranzactie cu id-ul id, ziua zi, suma suma, string-l tip si string-ul descriere
 * id, zi, suma - intreg; tip, descriere - string
 * returneaza o tranzactie cu id-ul id, ziua zi, suma suma, string-l tip si string-ul descriere
 */
Tranzactie* creeazaTranzactie(int zi, int suma, char* tip, char* descriere);

/*
 * distruge o tranzactie
 */
void destroyTranzactie(Tranzactie* tr);

/*
 * copiaza o tranzactie
 * returneaza o copie a tranzactiei tranzactie
 */
Tranzactie* copyTranzactie(Tranzactie* tranzactie);

#endif //LABREFACUT_DOMAIN_H
