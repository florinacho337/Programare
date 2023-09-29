#include "IteratorMD.h"
#include "MD.h"

using namespace std;

void IteratorMD::deplasare() {
    while(this->curent < this->md.n && this->md.e[this->curent].second.empty())
        this->curent++;
}

void IteratorMD::deplasareInapoi() {
    while(this->curent >= 0 && this->md.e[this->curent].second.empty())
        this->curent--;
}

IteratorMD::IteratorMD(const MD& _md): md(_md) {
	/* de adaugat */
    this->curent = 0;
    this->curent_vector = 0;
    this->cnt = 0;
    this->deplasare();
}

TElem IteratorMD::element() const{
	/* de adaugat */
    if(!valid())
        throw exception();
    TElem elem;
    elem.first = this->md.e[this->curent].first;
	elem.second = this->md.e[this->curent].second[this->curent_vector];
    return elem;
}

bool IteratorMD::valid() const {
	/* de adaugat */
	return this->cnt < this->md.dim() && this->cnt >= 0;
}

void IteratorMD::urmator() {
	/* de adaugat */
    if(!valid())
        throw exception();
    if (this->curent_vector < this->md.e[this->curent].second.size()-1)
        this->curent_vector++;
    else {
        this->curent_vector = 0;
        this->curent++;
        this->deplasare();
    }
    this->cnt++;
}

void IteratorMD::prim() {
	/* de adaugat */
    this->curent = 0;
    this->curent_vector = 0;
    this->cnt = 0;
    this->deplasare();
}

void IteratorMD::revinoKPasi(int k){
    if(k <= 0 || !valid())
        throw exception();
    while(k > 0 && valid()) {
        if (this->curent_vector > 0)
            this->curent_vector--;
        else{
            this->curent--;
            this->deplasareInapoi();
            this->curent_vector = this->md.e[this->curent].second.size()-1;
        }
        k--;
        this->cnt--;
    }
}

