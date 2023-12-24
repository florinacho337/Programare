#pragma once

#include "MDO.h"
#include <stack>


class IteratorMDO{
	friend class MDO;
private:

	//constructorul primeste o referinta catre Container
	//iteratorul va referi primul element din container
    //O(h), unde h este inaltimea arborelui
	IteratorMDO(const MDO& dictionar);

	//contine o referinta catre containerul pe care il itereaza
	const MDO& dict;
	/* aici e reprezentarea  specifica a iteratorului */
    stack<int> S;
    int curent;


public:

		//reseteaza pozitia iteratorului la inceputul containerului
        //O(h), unde h este inaltimea arborelui
		void prim();

		//muta iteratorul in container
		// arunca exceptie daca iteratorul nu e valid
        //O(h), unde h este inaltimea arborelui
		void urmator();

		//verifica daca iteratorul e valid (indica un element al containerului)
        //teta(1)
		bool valid() const;

		//returneaza valoarea elementului din container referit de iterator
		//arunca exceptie daca iteratorul nu e valid
        //teta(1)
		TElem element() const;
};

