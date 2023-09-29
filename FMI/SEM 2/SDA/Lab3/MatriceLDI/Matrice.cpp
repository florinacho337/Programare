#include "Matrice.h"

#include <exception>

using namespace std;

Linii::Linii(int i, Linii *urm, Linii *prec) {
    this->i = i;
    this->urm = urm;
    this->prec = prec;
}

int Linii::linie() const {
    return this->i;
}

Linii* Linii::precedent() {
    return this->prec;
}

Linii* Linii::urmator() {
    return this->urm;
}

Coloane::Coloane(int j, Coloane *urm, Coloane *prec) {
    this->j = j;
    this->urm = urm;
    this->prec = prec;
}

int Coloane::coloana() const {
    return this->j;
}

Coloane* Coloane::precedent() {
    return this->prec;
}

Coloane* Coloane::urmator() {
    return this->urm;
}

Elemente::Elemente(TElem e, Elemente *urm, Elemente *prec) {
    this->elem = e;
    this->urm = urm;
    this->prec = prec;
}

TElem Elemente::element() const {
    return this->elem;
}

Elemente* Elemente::precedent() {
    return this->prec;
}

Elemente* Elemente::urmator() {
    return this->urm;
}


Matrice::Matrice(int m, int n) {
    /* de adaugat */
    if(m <= 0 || n <= 0)
        throw exception();
    this->nr_coloane = n;
    this->nr_linii = m;
    this->prim_col = nullptr;
    this->prim_elem = nullptr;
    this->prim_lin = nullptr;
}



int Matrice::nrLinii() const{
    /* de adaugat */
    return this->nr_linii;
}


int Matrice::nrColoane() const{
    /* de adaugat */
    return this->nr_coloane;
}


TElem Matrice::element(int i, int j) const{
    /* de adaugat */
    if(i >= nrLinii() || j >= nrColoane() || i < 0 || j < 0)
        throw exception();
    Linii *l = this->prim_lin;
    Coloane *c = this->prim_col;
    Elemente *elem = this->prim_elem;
    while (l != nullptr && i > l->linie()) {
        l = l->urmator();
        c = c->urmator();
        elem = elem->urmator();
    }
    while (l != nullptr && c != nullptr && j > c->coloana() && i == l->linie()) {
        l = l->urmator();
        c = c->urmator();
        elem = elem->urmator();
    }
    if(l != nullptr && c != nullptr && elem != nullptr && j == c->coloana() && i == l->linie())
        return elem->element();
    return NULL_TELEMENT;
}



TElem Matrice::modifica(int i, int j, TElem e) {
    /* de adaugat */
    if (i >= nrLinii() || j >= nrColoane() || i < 0 || j < 0)
        throw exception();

    Linii *l = this->prim_lin;
    Coloane *c = this->prim_col;
    Elemente *elem = this->prim_elem;
    //daca nu exista inca elemente, vom adauga unul
    if(l == nullptr){
        if(e != 0){
            auto *p = new Linii(i, l, nullptr);
            this->prim_lin = p;
            auto *q = new Coloane(j, c, nullptr);
            this->prim_col = q;
            auto *r = new Elemente(e, elem, nullptr);
            this->prim_elem = r;
            return NULL_TELEMENT;
        }
        return NULL_TELEMENT;
    }

    while (l->urmator() != nullptr && i > l->linie()) {
        l = l->urmator();
        c = c->urmator();
        elem = elem->urmator();
    }
    while (l->urmator() != nullptr && j > c->coloana() && i == l->linie()) {
        l = l->urmator();
        c = c->urmator();
        elem = elem->urmator();
    }
    if (j == c->coloana() && l->urmator() != nullptr && l->precedent() != nullptr && i == l->linie()) {
        TElem vechi = elem->element();
        if (e != 0)
            elem->elem = e; // in cazul in care exista un i si j in listele respective, inseamna ca
                            // se va aplica doar modificarea/stergerea, altfel adaugare
        else {
            if(l->precedent() == nullptr) {
                l->urmator()->prec = l->precedent();
                c->urmator()->prec = c->precedent();
                elem->urmator()->prec = elem->precedent();
            } else if(l->urmator() == nullptr){
                l->precedent()->urm = l->urmator();
                c->precedent()->urm = c->urmator();
                elem->precedent()->urm = elem->urmator();
            } else{
                l->urmator()->prec = l->precedent();
                c->urmator()->prec = c->precedent();
                elem->urmator()->prec = elem->precedent();
                l->precedent()->urm = l->urmator();
                c->precedent()->urm = c->urmator();
                elem->precedent()->urm = elem->urmator();
            }
            delete[] l;
            delete[] c;
            delete[] elem;

        }
        return vechi;
    }
    if(e != 0) {
        auto *nl = new Linii(i, nullptr, nullptr);
        auto *nc = new Coloane(j, nullptr, nullptr);
        auto *nelem = new Elemente(e, nullptr, nullptr);
        if((i < l->linie()) || (i == l->linie() && j < c->coloana())) {
            if(l->precedent() == nullptr) {
                nl->urm = l;
                l->prec = nl;
                this->prim_lin = nl;
                nc->urm = c;
                c->prec = nc;
                this->prim_col = nc;
                nelem->urm = elem;
                elem->prec = nelem;
                this->prim_elem = nelem;
            }else {
                nl->urm = l;
                l->precedent()->urm = nl;
                nl->prec = l->precedent();
                l->prec = nl;
                nc->urm = c;
                c->precedent()->urm = nc;
                nc->prec = c->precedent();
                c->prec = nc;
                nelem->urm = elem;
                elem->precedent()->urm = nelem;
                nelem->prec = elem->prec;
                elem->prec = nelem;
            }
        } else {
            nl->urm = l->urmator();
            nl->prec = l;
            l->urm = nl;
            nc->urm = c->urmator();
            nc->prec = c;
            c->urm = nc;
            nelem->urm = elem->urmator();
            nelem->prec = elem;
            elem->urm = nelem;
        }
    }
    return NULL_TELEMENT;
}

void Matrice::transpusa(){
    Linii* l = this->prim_lin;
    Coloane* c = this->prim_col;
    Elemente* elem = this->prim_elem;
    while(l != nullptr){
        swap(l->i, c->j);
        l = l->urmator();
        c = c->urmator();
    }
    l = this->prim_lin;
    c = this->prim_col;
    while(l->urmator()->urmator() != nullptr){
        Linii* nextl = l->urmator();
        Coloane* nextc = c->urmator();
        Elemente* nextelem = elem->urmator();
        while(nextl != nullptr){
            if ((l->linie() > nextl->linie()) || (l->linie() == nextl->linie() && c->coloana() > nextc->coloana())){
                swap(l->i, nextl->i);
                swap(c->j, nextc->j);
                swap(elem->elem, nextelem->elem);
            }
            nextl = nextl->urmator();
            nextc = nextc->urmator();
            nextelem = nextelem->urmator();
        }
        l = l->urmator();
        c = c->urmator();
        elem = elem->urmator();
    }
}