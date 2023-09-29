#include "Iterator.h"
#include "DO.h"
#include <iostream>

#include <exception>
using namespace std;

int DO::aloca() {
    int i = this->primLiber;
    primLiber = urm[primLiber];
    return i;
}

void DO::dealoca(int i) {
    prec[i] = -1;
    urm[i] = primLiber;
    primLiber = i;
}

int DO::creeazaNod(TElem elem) {
    int i = aloca();
    if(i != -1){
        this->e[i] = elem;
        urm[i] = -1;
        prec[i] = -1;
    }
    return i;
}

void DO::redim() {
    this->cp = 2*this->cp;
    auto *nElems = new TElem[this->cp];
    int *nUrm = new int[this->cp];
    int *nPrec = new int[this->cp];
    for(int i = 0; i < this->cp - 1; ++i) {
        if(i < this->n){
            nElems[i] = this->e[i];
            nUrm[i] = this->urm[i];
            nPrec[i] = this->prec[i];
        } else {
            nUrm[i] = i + 1;
            nPrec[i + 1] = i;
        }
    }
    nPrec[this->n] = nUrm[this->cp - 1] = -1;
    this->primLiber = this->n;
    delete[] this->e;
    delete[] this->urm;
    delete[] this->prec;
    this->e = nElems;
    this->urm = nUrm;
    this->prec = nPrec;
}

DO::DO(Relatie r) {
	/* de adaugat */
    this->rel = r;
    this->prim = this->ultim = -1;
    this->e = new TElem[this->cp];
    this->urm = new int[this->cp];
    this->prec = new int[this->cp];
    for(int i = 0; i < this->cp - 1; ++i) {
        urm[i] = i + 1;
        prec[i + 1] = i;
    }
    urm[cp-1] = prec[0] = -1;
    this->primLiber = 0;
    this->n = 0;
}

//adauga o pereche (cheie, valoare) in dictionar
//daca exista deja cheia in dictionar, inlocuieste valoarea asociata cheii si returneaza vechea valoare
//daca nu exista cheia, adauga perechea si returneaza null
TValoare DO::adauga(TCheie c, TValoare v) {
	/* de adaugat */
    if(this->n == this->cp)
        redim();
    TElem elem;
    elem.first = c;
    elem.second = v;
    TValoare val = NULL_TVALOARE;

    int nou = creeazaNod(elem);
    if(this->prim == -1) {
        this->prim = nou;
        this->ultim = nou;
    }
    else{
        int poz = this->prim;
        while(poz != -1 && !rel(c, this->e[poz].first))
            poz = urm[poz];
        if(poz == -1) {
            prec[nou] = this->ultim;
            urm[this->ultim] = nou;
            this->ultim = nou;
        } else if(c == this->e[poz].first) {
            val = this->e[poz].second;
            this->e[poz].second = v;
        } else if(poz == this->prim){
            urm[nou] = this->prim;
            prec[this->prim] = nou;
            this->prim = nou;
        } else {
            urm[nou] = poz;
            urm[prec[poz]] = nou;
            prec[nou] = prec[poz];
            prec[poz] = nou;
        }
    }
    if(val != NULL_TVALOARE)
        return val;
    this->n++;
	return NULL_TVALOARE;
}

//cauta o cheie si returneaza valoarea asociata (daca dictionarul contine cheia) sau null
TValoare DO::cauta(TCheie c) const {
	/* de adaugat */
    int poz = this->prim;
    while(poz != -1 && !rel(c, this->e[poz].first))
        poz = urm[poz];
    if(poz != -1 && c == this->e[poz].first)
        return this->e[poz].second;
	return NULL_TVALOARE;	
}

TValoare DO::ceaMaiFrecventaValoare() const {
    TValoare maxim = NULL_TVALOARE;
    int frecv_maxima = 0;
    int poz = this->prim;
    DO frecvente = DO{this->rel};
    while(poz != -1){
        TCheie val = this->e[poz].second;
        TValoare frecventa = frecvente.cauta(val);
        if(frecventa == NULL_TVALOARE)
            frecvente.adauga(val, 1);
        else
            frecvente.adauga(val, frecventa + 1);
        poz = urm[poz];
    }
    Iterator it = frecvente.iterator();
    it.prim();
    while (it.valid()) {
        int frecv = it.element().second;
        TValoare val = it.element().first;
        if(frecv > frecv_maxima) {
            frecv_maxima = frecv;
            maxim = val;
        }
        it.urmator();
    }
    return maxim;
}

//sterge o cheie si returneaza valoarea asociata (daca exista) sau null
TValoare DO::sterge(TCheie c) {
	/* de adaugat */
    int poz = this->prim;
    while(poz != -1 && !rel(c, this->e[poz].first))
        poz = urm[poz];
    if(poz != -1 && c == this->e[poz].first){
        TValoare val = this->e[poz].second;
        if(poz == this->prim)
            this->prim = urm[poz];
        if(poz == this->ultim)
            this->ultim = prec[poz];
        if(urm[poz] != -1)
            prec[urm[poz]] = prec[poz];
        if(prec[poz] != -1)
            urm[prec[poz]] = urm[poz];
        dealoca(poz);
        this->n--;
        return val;
    }
	return NULL_TVALOARE;
}

//returneaza numarul de perechi (cheie, valoare) din dictionar
int DO::dim() const {
	/* de adaugat */
	return this->n;
}

//verifica daca dictionarul e vid
bool DO::vid() const {
	/* de adaugat */
	return this->n == 0;
}

Iterator DO::iterator() const {
	return  Iterator(*this);
}

DO::~DO() {
	/* de adaugat */
    delete[] this->e;
    delete[] this->prec;
    delete[] this->urm;
}
