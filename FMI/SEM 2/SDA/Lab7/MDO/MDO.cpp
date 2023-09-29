#include "IteratorMDO.h"
#include "MDO.h"
#include <vector>

#include <exception>
using namespace std;

int MDO::aloca() {
    int i = this->primLiber;
    this->primLiber = this->stanga[this->primLiber];
    return i;
}

void MDO::dealoca(int i) {
    this->dreapta[i] = -1;
    this->stanga[i] = this->primLiber;
    this->primLiber = i;
}

int MDO::creeazaNod(TElem elem) {
    int i = aloca();
    if(i != -1){
        this->elemente[i] = elem;
        this->stanga[i] = -1;
        this->dreapta[i] = -1;
    }
    return i;
}

MDO::MDO(Relatie r) {
	/* de adaugat */
    this->cp = CP_MAX
    this->n = 0;
    this->rel = r;
    this->elemente = new TElem[this->cp];
    this->stanga = new int[this->cp];
    this->dreapta = new int[this->cp];
    for(int i = 0; i < this->cp-1; ++i) {
        this->stanga[i] = i + 1;
        this->dreapta[i] = -1;
    }
    this->stanga[this->cp-1] = this->dreapta[this->cp-1] = -1;
    this->primLiber = 0;
    this->radacina = -1;
}

int MDO::adauga_rec(int nod, TElem elem) {
    if(nod == -1)
        nod = creeazaNod(elem);
    else{
        if(this->rel(elem.first, this->elemente[nod].first))
            this->stanga[nod] = adauga_rec(this->stanga[nod], elem);
        else
            this->dreapta[nod] = adauga_rec(this->dreapta[nod], elem);
    }
    return nod;
}

int MDO::minim(int nod) {
    while(stanga[nod] != -1)
        nod = stanga[nod];
    return nod;
}

int MDO::sterge_rec(int nod, TElem elem, bool& sters) {
    if(nod == -1)
        return nod;
    if(elem.first == this->elemente[nod].first && elem.second == this->elemente[nod].second){
        int temp;
        sters = true;
        if(this->stanga[nod] != -1 && this->dreapta[nod] != -1){
            temp = this->minim(this->dreapta[nod]);
            this->elemente[nod] = elemente[temp];
            this->dreapta[nod] = sterge_rec(this->dreapta[nod], elem, sters);
            return nod;
        } else{
            temp = nod;
            int repl;
            if(this->stanga[nod] == -1)
                repl = this->dreapta[nod];
            else
                repl = this->stanga[nod];
            this->dealoca(temp);
            return repl;
        }
    }
    if(rel(elem.first, this->elemente[nod].first))
        this->stanga[nod] = sterge_rec(this->stanga[nod], elem, sters);
    else
        this->dreapta[nod] = sterge_rec(this->dreapta[nod], elem, sters);
    return nod;
}

void MDO::adauga(TCheie c, TValoare v) {
	/* de adaugat */
    this->radacina = this->adauga_rec(this->radacina, TElem(c, v));
    this->n++;
}

vector<TValoare> MDO::cauta(TCheie c) const {
	/* de adaugat */
    int nod = this->radacina;
    while(nod != -1 && this->elemente[nod].first != c){
        if(this->rel(c, this->elemente[nod].first))
            nod = this->stanga[nod];
        else
            nod = this->dreapta[nod];
    }
    vector<TValoare> valori;
    while(nod != -1 && this->elemente[nod].first == c){
        valori.push_back(this->elemente[nod].second);
        nod = this->stanga[nod];
    }
	return valori;
}

bool MDO::sterge(TCheie c, TValoare v) {
	/* de adaugat */
    bool sters = false;
    this->radacina = sterge_rec(this->radacina, TElem(c, v), sters);
    if(sters)
        this->n--;
	return sters;
}

int MDO::dim() const {
	/* de adaugat */
	return this->n;
}

bool MDO::vid() const {
	/* de adaugat */
	return this->n == 0;
}

int MDO::adaugaInexistente(MDO& mdo){
    int n_vechi = this->n;
    IteratorMDO it = mdo.iterator();
    while(it.valid()){
        TElem elem = it.element();
        this->adauga(elem.first, elem.second);
        it.urmator();
    }
    return this->n - n_vechi;
}

IteratorMDO MDO::iterator() const {
	return IteratorMDO(*this);
}

MDO::~MDO() {
	/* de adaugat */
    delete[] this->elemente;
    delete[] this->stanga;
    delete[] this->dreapta;
}
