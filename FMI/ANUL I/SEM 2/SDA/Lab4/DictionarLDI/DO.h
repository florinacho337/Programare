#pragma once

typedef int TCheie;
typedef int TValoare;

#define NULL_TVALOARE -1

#include <utility>
typedef std::pair<TCheie, TValoare> TElem;

class Iterator;

typedef bool(*Relatie)(TCheie, TCheie);
class DO {
	friend class Iterator;
    private:
	/* aici e reprezentarea */
    Relatie rel;
    int cp = 500;
    TElem *e;
    int *urm, *prec;
//    const static auto cp = 10000;
//    TElem e[cp];
//    int urm[cp], prec[cp];
    int prim, ultim, primLiber, n;

    //se retruneaza pozitia unui spatiu liber din lista
    //complexitate teta(1)
    int aloca();

    //dealoca spatiul de indice i
    //complexitate teta(1)
    void dealoca(int i);

    //functie petru creazarea unui nod in lista inlantuita
    //returneaza pozitia nodului nou creat
    //complexitate teta(1)
    int creeazaNod(TElem elem);

    //functie de redimenzionare
    //complexitate teta(n)
    void redim();

    public:

	// constructorul implicit al dictionarului
    //complexitate teta(n)
	DO(Relatie r);


	// adauga o pereche (cheie, valoare) in dictionar
	//daca exista deja cheia in dictionar, inlocuieste valoarea asociata cheii si returneaza vechea valoare
	// daca nu exista cheia, adauga perechea si returneaza null: NULL_TVALOARE
    // complexitate amortizata O(n)
	TValoare adauga(TCheie c, TValoare v);

	//cauta o cheie si returneaza valoarea asociata (daca dictionarul contine cheia) sau null: NULL_TVALOARE
    //complexitate O(n)
	TValoare cauta(TCheie c) const;


	//sterge o cheie si returneaza valoarea asociata (daca exista) sau null: NULL_TVALOARE
    //complexitate O(n)
	TValoare sterge(TCheie c);

    // returneaza valoarea care apare cel mai frecvent în dicționar.
    // Dacă mai multe valori apar cel mai frecvent, se returnează una (oricare) dintre ele.
    // Dacă dicționarul este vid, operațiea returnează NULL_TVALOARE
    // complexitate O(n^2)
    TValoare ceaMaiFrecventaValoare() const;

	//returneaza numarul de perechi (cheie, valoare) din dictionar
    //complexitate teta(1)
	int dim() const;

	//verifica daca dictionarul e vid
    //complexitate teta(1)
	bool vid() const;

	// se returneaza iterator pe dictionar
	// iteratorul va returna perechile in ordine dupa relatia de ordine (pe cheie)
    //complexitate teta(1)
	Iterator iterator() const;


	// destructorul dictionarului
    //com[lexitate teta(1)
	~DO();

};
