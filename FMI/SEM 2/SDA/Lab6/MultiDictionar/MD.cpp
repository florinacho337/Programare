#include "MD.h"
#include "IteratorMD.h"
#include <cmath>

using namespace std;

int MD::d(TCheie c) const {
    return abs(c) % this->n;
}

MD::MD() {
	/* de adaugat */
    this->n = MAX;
    this->m = 0;
    this->primLiber = 0;
    this->e = new TSectiune[MAX];
    this->urm = new int[MAX];
    for (int i = 0; i < MAX; ++i)
        this->urm[i] = -1;
}

void MD::actPrimLiber() {
    this->primLiber++;
    while(this->primLiber < this->n && !this->e[this->primLiber].second.empty())
        this->primLiber++;
}

void MD::adauga(TCheie c, TValoare v) {
	/* de adaugat */
    int i = this->d(c);
    if(this->e[i].second.empty()){
        if(i == this->primLiber)
            this->actPrimLiber();
        this->e[i].first = c;
        this->e[i].second.push_back(v);
    } else {
        int j = -1; // salvam valoarea precedenta a lui i
        while (i != -1 && this->e[i].first != c) { // cautam cheia
            j = i;
            i = this->urm[i];
        }
        if (i == -1) { // nu am gasit cheia
            this->e[this->primLiber].first = c;
            this->e[this->primLiber].second.push_back(v);
            this->urm[j] = this->primLiber;
            this->actPrimLiber();
        } else // am gasit cheia
            this->e[i].second.push_back(v);
    }
    this->m++;
}


bool MD::sterge(TCheie c, TValoare v) {
	/* de adaugat */
    int i = this->d(c);
    int j = -1; // pozitia anterioara a lui i

    //se afla pozitia anterioara a lui i, in cazul in care aceasta exista
    int k = 0;
    while(k < this->n && this->urm[k] != i)
        k++;
    if(k < this->n)
        j = k;

    while(i != -1 && this->e[i].first != c){
        j = i;
        i = this->urm[i];
    }
    if(i != -1){
        int poz = 0;
        while(poz < this->e[i].second.size() && this->e[i].second[poz] != v)
            poz++;
        if(poz == this->e[i].second.size()) // nu am gasit valoarea
            return false;
        else // am gasit valoarea
            this->e[i].second.erase(this->e[i].second.begin()+poz);
        if(this->e[i].second.empty()) {
            bool gata = false;
            do {
                int p = this->urm[i], pp = i; // retinem pozitiile nodurilor urmator si actual
                while (p != -1 && this->d(this->e[p].first) != i) {
                    pp = p;
                    p = this->urm[p];
                }
                if (p == -1)
                    gata = true;
                else {
                    this->e[i] = this->e[p];
                    i = p;
                    j = pp;
                }
            } while (!gata);
            if(j != -1)
                this->urm[j] = this->urm[i];
            this->urm[i] = -1;
            if(i < this->primLiber)
                this->primLiber = i;
        }
        this->m--;
        return true;
    }
    return false;
}


vector<TValoare> MD::cauta(TCheie c) const {
	/* de adaugat */
    int poz = this->d(c);
    while(poz != -1 && this->e[poz].first != c)
        poz = urm[poz];
    if(poz != -1)
	    return this->e[poz].second;
    return {};
}


int MD::dim() const {
	/* de adaugat */
	return this->m;
}


bool MD::vid() const {
	/* de adaugat */
	return this->m == 0;
}

IteratorMD MD::iterator() const {
	return IteratorMD(*this);
}


MD::~MD() {
	/* de adaugat */
    delete[] this->urm;
    delete[] this->e;
}
