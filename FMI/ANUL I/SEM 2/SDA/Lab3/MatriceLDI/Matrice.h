#pragma once

typedef int TElem;

#define NULL_TELEMENT 0

class Linii {
private:
    int i;
    Linii *urm, *prec;
public:
    friend class Matrice;

    //constructor
    Linii(int i, Linii *urm, Linii *prec);

    int linie() const;

    Linii *precedent();

    Linii *urmator();
};

class Coloane {
private:
    int j;
    Coloane *urm, *prec;
public:
    friend class Matrice;

    //constructor
    Coloane(int j, Coloane *urm, Coloane *prec);

    int coloana() const;

    Coloane *precedent();

    Coloane *urmator();
};

class Elemente {
private:
    TElem elem;
    Elemente *urm, *prec;
public:
    friend class Matrice;

    //constructor
    Elemente(TElem e, Elemente *urm, Elemente *prec);

    TElem element() const;

    Elemente *precedent();

    Elemente *urmator();
};

class Matrice {

private:
    /* aici e reprezentarea */
    int nr_linii, nr_coloane;
    Linii* prim_lin;
    Coloane* prim_col;
    Elemente* prim_elem;

public:

    //constructor
    //se arunca exceptie daca nrLinii<=0 sau nrColoane<=0
    //complexitate teta(1)
    Matrice(int nrLinii, int nrColoane);


    //destructor
    ~Matrice(){};

    //returnare element de pe o linie si o coloana
    //se arunca exceptie daca (i,j) nu e pozitie valida in Matrice
    //indicii se considera incepand de la 0
    //complexitate O(n)
    TElem element(int i, int j) const;


    // returnare numar linii
    //complexitate teta(1)
    int nrLinii() const;

    // returnare numar coloane
    //complexitate teta(1)
    int nrColoane() const;


    // modificare element de pe o linie si o coloana si returnarea vechii valori
    // se arunca exceptie daca (i,j) nu e o pozitie valida in Matrice
    //complexitate O(n)
    TElem modifica(int i, int j, TElem e);

    // complexitate teta(n^2)
    void transpusa();

};
