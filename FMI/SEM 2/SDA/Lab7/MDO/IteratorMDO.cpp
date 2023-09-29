#include "IteratorMDO.h"
#include "MDO.h"

IteratorMDO::IteratorMDO(const MDO& d) : dict(d){
	/* de adaugat */
    this->curent = this->dict.radacina;
    this->S = {};
    while(this->curent != -1){
        this->S.push(this->curent);
        this->curent = this->dict.stanga[this->curent];
    }
    if(!this->S.empty())
        this->curent = this->S.top();
}

void IteratorMDO::prim(){
	/* de adaugat */
    this->curent = this->dict.radacina;
    this->S = {};
    while(this->curent != -1){
        this->S.push(this->curent);
        this->curent = this->dict.stanga[this->curent];
    }
    if(!this->S.empty())
        this->curent = this->S.top();
}

void IteratorMDO::urmator(){
	/* de adaugat */
    if(!this->valid())
        throw exception();
    this->curent = this->S.top();
    this->S.pop();
    if(this->dict.dreapta[this->curent] != -1){
        this->curent = this->dict.dreapta[this->curent];
        while(this->curent != -1){
            this->S.push(this->curent);
            this->curent = this->dict.stanga[this->curent];
        }
    }
    if(!this->S.empty())
        this->curent = this->S.top();
    else
        this->curent = -1;
}

bool IteratorMDO::valid() const{
	/* de adaugat */
	return this->curent != -1;
}

TElem IteratorMDO::element() const{
	/* de adaugat */
    if(!this->valid())
        throw exception();
	return this->dict.elemente[this->curent];
}


