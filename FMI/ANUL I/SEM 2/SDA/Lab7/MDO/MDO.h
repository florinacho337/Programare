#pragma once

#include <vector>

typedef int TCheie;
typedef int TValoare;
#define CP_MAX 10000;

#include <utility>
typedef std::pair<TCheie, TValoare> TElem;

using namespace std;

class IteratorMDO;

typedef bool(*Relatie)(TCheie, TCheie);

class MDO {
	friend class IteratorMDO;
    private:
	/* aici e reprezentarea */
    Relatie rel;
    TElem* elemente;
    int* stanga, *dreapta;
    int primLiber, radacina, cp, n;

    //aloca un nod nou
    //teta(1)
    int aloca();

    //dealoca un nod
    //teta(1)
    void dealoca(int i);

    //creeaza un nod
    //teta(1)
    int creeazaNod(TElem elem);

    //adauga recursiv un element
    //O(h), unde h este inaltimea arborelui
    int adauga_rec(int nod, TElem elem);

    //sterge recursiv un element
    //O(h), unde h este inaltimea arborelui
    int sterge_rec(int nod, TElem elem, bool& sters);

    //returneaza nodul minim (sau maxim, in functie de relatie) dintr-un subarbore
    //O(h), unde h este inaltimea arborelui
    int minim(int nod);

    public:

	// constructorul implicit al MultiDictionarului Ordonat
    // O(n), unde n este capacitatea MDO
	MDO(Relatie r);

	// adauga o pereche (cheie, valoare) in MDO
    //O(h), unde h este inaltimea arborelui
	void adauga(TCheie c, TValoare v);

	//cauta o cheie si returneaza vectorul de valori asociate
    //O(h), unde h este inaltimea arborelui
	vector<TValoare> cauta(TCheie c) const;

	//sterge o cheie si o valoare 
	//returneaza adevarat daca s-a gasit cheia si valoarea de sters
    //O(h), unde h este inaltimea arborelui
	bool sterge(TCheie c, TValoare v);

	//returneaza numarul de perechi (cheie, valoare) din MDO
    //teta(1)
	int dim() const;

	//verifica daca MultiDictionarul Ordonat e vid
    //teta(1)
	bool vid() const;

	// se returneaza iterator pe MDO
	// iteratorul va returna perechile in ordine in raport cu relatia de ordine
    //teta(1)
	IteratorMDO iterator() const;

    // adauga în multidicționarul curent toate perechile din mdo care nu se află
    // deja în multidicționar.
    // returnează numărul de perechi adăugate
    // O(max{h1, h2}), unde h1 este inaltimea arborelui curent, iar h2 inaltimea
    // arborelui folosit pentru mdo
    int adaugaInexistente(MDO& mdo);

	// destructorul
    //teta(1)
	~MDO();

};
