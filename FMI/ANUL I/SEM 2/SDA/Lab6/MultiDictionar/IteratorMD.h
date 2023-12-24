#pragma once
#include "MD.h"

class MD;

class IteratorMD
{
	friend class MD;

private:

	//constructorul primeste o referinta catre Container
	//iteratorul va referi primul element din container
    //complexitate O(n)
	IteratorMD(const MD& c);

	//contine o referinta catre containerul pe care il itereaza
	const MD& md;

	/* aici e reprezentarea  specifica a iteratorului */
    int curent;
    unsigned int curent_vector;
    int cnt;

    //deplaseaza iteratorul la urmatorul element
    //O(n)
    void deplasare();

    //deplaseaza iteratorul la precedentul element
    //O(n)
    void deplasareInapoi();

public:

		//reseteaza pozitia iteratorului la inceputul containerului
        //O(n)
		void prim();

		//muta iteratorul in container
		// arunca exceptie daca iteratorul nu e valid
        //O(n)
		void urmator();

		//verifica daca iteratorul e valid (indica un element al containerului)
        //teta(1)
		bool valid() const;

		//returneaza valoarea elementului din container referit de iterator
		//arunca exceptie daca iteratorul nu e valid
        //teta(1)
		TElem element() const;

        //muta cursuroul iteratorului astfel incat sa refere a k-a pereche in urma,
        //incepand de la cea curenta. Iteratorul devine nevalid in cazul in care
        //exista mai putin de k perechi anterioare perechii curente in multidictionar.
        //arunca exceptie in cazul in care iteratorul este nevalid sau k este zero sau negativ
        //O(k*n)
        void revinoKPasi(int k);
};

