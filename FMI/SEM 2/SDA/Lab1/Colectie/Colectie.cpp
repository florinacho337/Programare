#include "Colectie.h"
#include "IteratorColectie.h"
#include <iostream>

using namespace std;

void Colectie::redim(){
    TElem *eNou = new TElem[2*cp];
    for(int i = 0; i < n; ++i)
        eNou[i] = elemente[i];
    cp = 2*cp;
    delete[] elemente;
    elemente = eNou;
}

bool rel(TElem e1, TElem e2) {
    if(e1 <= e2) return true;
    else return false;
}

Colectie::Colectie() {
    this->cp = 100;
    elemente = new TElem[cp];
    this->n = 0;
    this->relatie = rel;
}

void Colectie::adauga(TElem e) {
    if(n == cp)
        redim();
    this->elemente[n++] = e;
    int i = n-1;
    while(this->relatie(e, elemente[i]) && i >= 0)
        i--;
    for(int j = n-1; j > i+1; --j)
        elemente[j] = elemente[j-1];
    elemente[i+1] = e;
}

void Colectie::adaugaElemente(TElem e, int nr_aparitii){
    while(n + nr_aparitii >= cp)
        redim();
    int i = n-1;

    while(this->relatie(e, elemente[i]) && i >= 0)
        i--;
    for(int j = n + nr_aparitii - 1; j > i+nr_aparitii+1; --j) {
        elemente[j] = elemente[j - nr_aparitii];
    }
    for(int j = i+1; j <= i + nr_aparitii+1; ++j)
        elemente[j] = e;
    n = n + nr_aparitii;
}


bool Colectie::sterge(TElem e) {
    for(int i = 0; i < n; ++i)
        if(elemente[i] == e) {
            for (int j = i + 1; j < n; ++j)
                elemente[j - 1] = elemente[j];
            n--;
            return true;
        }
	return false;
}


bool Colectie::cauta(TElem elem) const {
    for(int i = 0; i < n; ++i)
        if(elemente[i] == elem)
            return true;
	return false;
}


int Colectie::nrAparitii(TElem elem) const {
    int c = 0;
	for(int i = 0; i < n; ++i)
        if(elemente[i] == elem)
            c++;
	return c;
}



int Colectie::dim() const {
	return n;
}


bool Colectie::vida() const {
	return n == 0;
}


IteratorColectie Colectie::iterator() const {
	return  IteratorColectie(*this);
}


Colectie::~Colectie() {
    delete[] elemente;
}
