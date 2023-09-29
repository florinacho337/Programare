#include "IteratorColectie.h"
#include "Colectie.h"


IteratorColectie::IteratorColectie(const Colectie& c): col(c) {
	curent = col.elemente;
}

TElem IteratorColectie::element() const{
    if(!valid())
        throw;
	return *curent;
}

bool IteratorColectie::valid() const {
	return curent - col.elemente < col.dim();
}

void IteratorColectie::urmator() {
    if(!valid())
        throw;
    curent++;
}

void IteratorColectie::prim() {
	curent = col.elemente;
}
