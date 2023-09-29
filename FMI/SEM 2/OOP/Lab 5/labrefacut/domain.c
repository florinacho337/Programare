#include <string.h>
#include <malloc.h>

#include "domain.h"

Tranzactie* creeazaTranzactie(int zi, int suma, char* tip, char* descriere){
    Tranzactie *tr = malloc(sizeof(Tranzactie));
    tr->suma = suma;
    tr->zi = zi;
    tr->descriere = malloc(strlen(descriere) + 1);
    strncpy(tr->descriere, descriere, strlen(descriere)+1);
    tr->tip = malloc(strlen(tip) + 1);
    strncpy(tr->tip, tip, strlen(tip)+1);
    return tr;
}


void destroyTranzactie(Tranzactie* tr){
    free(tr->descriere);
    free(tr->tip);
    free(tr);
}

Tranzactie* copyTranzactie(Tranzactie* tranzactie){
    return creeazaTranzactie(tranzactie->zi, tranzactie->suma, tranzactie->tip, tranzactie->descriere);
}
