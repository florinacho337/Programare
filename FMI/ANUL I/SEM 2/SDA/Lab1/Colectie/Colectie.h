#pragma once

typedef int TElem;

typedef bool(*Relatie)(TElem, TElem);

//in implementarea operatiilor se va folosi functia (relatia) rel (de ex, pentru <=)
// va fi declarata in .h si implementata in .cpp ca functie externa colectiei
bool rel(TElem, TElem);

class IteratorColectie;

class Colectie {

	friend class IteratorColectie;

private:
	/* aici e reprezentarea */
    int cp;
    int n;
    TElem *elemente;
    //complexitate medie O(n), unde n reprezinta capacitatea veche
    void redim();
    Relatie relatie;
public:
		//constructorul implicit
        //complexitate teta(1)
		Colectie();

		//adauga un element in colectie
        //complexitate amortizata O(n), unde n este numarul de elemente din colectie
		void adauga(TElem e);

        //adauga un element in colectie de nr_aparitii ori
        //complexitate amortizata O(n), unde n este numarul de elemente din colectie
        void adaugaElemente(TElem e, int nr_aparitii);

		//sterge o aparitie a unui element din colectie
		//returneaza adevarat daca s-a putut sterge
        //complexitate medie O(n), unde n este numarul de elemente din colectie
		bool sterge(TElem e);

		//verifica daca un element se afla in colectie
        //complexitate medie O(n), unde n este numarul de elemente din colectie
		bool cauta(TElem elem) const;

		//returneaza numar de aparitii ale unui element in colectie
        //complexitate medie O(n), unde n este numarul de elemente din colectie
		int nrAparitii(TElem elem) const;


		//intoarce numarul de elemente din colectie;
        //complexitate teta(1)
		int dim() const;

		//verifica daca colectia e vida;
        //complexitate teta(1)
		bool vida() const;

		//returneaza un iterator pe colectie
        //complexitate teta(1)
		IteratorColectie iterator() const;

		// destructorul colectiei
        //complexitate teta(1)
		~Colectie();


};

