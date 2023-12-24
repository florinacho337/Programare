#include <exception>
#include "Iterator.h"
#include "DO.h"

using namespace std;

Iterator::Iterator(const DO& d) : dict(d){
	/* de adaugat */
    this->curent = dict.prim;
}

void Iterator::prim(){
	/* de adaugat */
    this->curent = dict.prim;
}

void Iterator::urmator(){
	/* de adaugat */
    if (!valid())
        throw exception();
    this->curent = dict.urm[this->curent];
}

bool Iterator::valid() const{
	/* de adaugat */
	return this->curent != -1;
}

TElem Iterator::element() const{
	/* de adaugat */
    if(!valid())
        throw exception();
	return dict.e[curent];
}


