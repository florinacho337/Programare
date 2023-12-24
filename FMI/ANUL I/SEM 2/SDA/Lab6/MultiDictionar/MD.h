#pragma once
#include<vector>
#include<utility>

using namespace std;

#define MAX 100000
typedef int TCheie;
typedef int TValoare;

typedef std::pair<TCheie, TValoare> TElem;
typedef std::pair<TCheie, vector<TValoare>> TSectiune;

class IteratorMD;

class MD
{
	friend class IteratorMD;

private:
	/* aici e reprezentarea */
    int n, primLiber, m;
    int* urm;
    TSectiune* e;

    //functia de dispersie
    //complexitate teta(1)
    int d(TCheie c) const ;

    //functia de actualizare primLiber
    //complexitate O(n)
    void actPrimLiber();

public:
	// constructorul implicit al MultiDictionarului
    //complexitate teta(n)
	MD();

	// adauga o pereche (cheie, valoare) in MD
    //complexitate O(n)
	void adauga(TCheie c, TValoare v);

	//cauta o cheie si returneaza vectorul de valori asociate
    //complexitate O(n)
	vector<TValoare> cauta(TCheie c) const;

	//sterge o cheie si o valoare 
	//returneaza adevarat daca s-a gasit cheia si valoarea de sters
    //complexitate O(n)
	bool sterge(TCheie c, TValoare v);

	//returneaza numarul de perechi (cheie, valoare) din MD
    //complexitate teta(1)
	int dim() const;

	//verifica daca MultiDictionarul e vid
    //complexitate teta(1)
	bool vid() const;

	// se returneaza iterator pe MD
    //complexitate teta(1)
	IteratorMD iterator() const;

	// destructorul MultiDictionarului
    //complexitate teta(1)
	~MD();



};

