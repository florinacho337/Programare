#include <exception>
#include <assert.h>
#include <algorithm>
#include <vector>
#include "IteratorMDO.h"
#include "MDO.h"
#include "TestExtins.h"

using namespace std;

bool cresc(TCheie c1, TCheie c2) {
	if (c1 <= c2) {
		return true;
	} else {
		return false;
	}
}

bool desc(TCheie c1, TCheie c2) {
	if (c1 >= c2) {
		return true;
	} else {
		return false;
	}
}

void testCreeaza() {
	MDO d = MDO(cresc);
	assert(d.dim() == 0);
	assert(d.vid());

	IteratorMDO it = d.iterator();
	it.prim();
	assert(!it.valid());

	for (int i = 0; i < 10; i++) {
        vector<TValoare> v= d.cauta(i);
        assert(v.size()==0);
	}

	for (int i = -10; i < 10; i++) {
		vector<TValoare> v= d.cauta(i);
        assert(v.size()==0);
	}
}

void testCauta(Relatie r) {
	MDO d = MDO(r);
	int cMin = 0;
	int cMax = 10;
	for (int i = cMin; i <= cMax; i++) {
			d.adauga(i, i + 1);
			d.adauga(i, i + 2);
	}
	int intervalDim = 10;
	for (int i = cMin; i <= cMax; i++) {
        vector<TValoare> v= d.cauta(i);
        assert(v.size()==2);
	}
	for (int i = cMin - intervalDim; i < cMin; i++) {
        vector<TValoare> v= d.cauta(i);
        assert(v.size()==0);
	}
	for (int i = cMax + 1; i < cMax + intervalDim; i++) {
        vector<TValoare> v= d.cauta(i);
        assert(v.size()==0);
	}
}

void testCauta() {
	testCauta(cresc);
	testCauta(desc);
}

void populeazaMDOVidIdentic(MDO& mdo, int min, int max) {
	for (int i = min; i <= max; i++) {
        mdo.adauga(i, i);
		if (i%2 ==0)
            mdo.adauga(i, i+2); //cheile pare le adaug de 2 ori
	}
}

void testStergeCauta(Relatie r) {
	MDO d = MDO(r);
	int min = 10;
	int max = 20;
	populeazaMDOVidIdentic(d, min, max);
	for (int c = min; c <= max; c++) {
		assert(d.sterge(c, c+1) == false);
		if (c%2==0)
            assert(d.sterge(c,c) == true);
	}
	//raman doar cheile impare, o singura data
	for (int c = min; c <= max; c++) {
		if (c%2==1){
            assert(d.sterge(c,c+1) == false);
            assert(d.sterge(c,c) == true);
		}
        else{
              assert(d.sterge(c,c+2) == true);
        }
	}
    //MDO devine vid
	assert(d.dim() == 0);
}

void testSterge() {
	testStergeCauta(cresc);
	testStergeCauta(desc);
}

//genereaza un vector continand in ordine aleatoare valorile naturale din intervalul inchis [cMin, cMax]
vector<int> cheiInOrdineAleatoare(int cMin, int cMax) {
	vector<int> chei;
	for (int c = cMin; c <= cMax; c++) {
		chei.push_back(c);
	}
	int n = chei.size();
	for (int i = 0; i < n - 1; i++) {
		int j = i + rand() % (n - i);
		swap(chei[i], chei[j]);
	}
	return chei;
}


void testIterator(Relatie r) {
	MDO d = MDO(r);
	IteratorMDO it = d.iterator();
	assert(!it.valid());
	it.prim();
	assert(!it.valid());
	int cMin = 100;
	int cMax = 300;
	vector<int> chei = cheiInOrdineAleatoare(cMin, cMax);
	int n = chei.size();
	for (int i = 0; i < n; i++) {
      d.adauga(chei[i], 100);
	  if (chei[i]%2==0)	{
		d.adauga(chei[i], 200);
	  }
	}

	IteratorMDO itD = d.iterator();
	assert(itD.valid());
	itD.prim();
	assert(itD.valid());

	TCheie cPrec = itD.element().first;

    itD.urmator();
	while (itD.valid()) {
		TCheie c = itD.element().first;
		assert(r(cPrec, c));
		cPrec = c;
		itD.urmator();
	}
}

void testIterator() {
	testIterator(cresc);
	testIterator(desc);
}

void testAdaugaInexistente(){
        auto d1 = MDO(cresc);
        auto d2 = MDO(desc);
        vector<int> chei1 = cheiInOrdineAleatoare(100, 300);
        vector<int> chei2 = cheiInOrdineAleatoare(400, 600);
        for (int i = 0; i < chei1.size(); i++) {
            d1.adauga(chei1[i], 100);
            d2.adauga(chei2[i], 99);
            if (chei1[i]%2==0)	{
                d1.adauga(chei1[i], 200);
            }
            if(chei2[i]%2==0){
                d2.adauga(chei2[i], 199);
            }
        }
        int dim_veche = d1.dim();
        assert(dim_veche + d1.adaugaInexistente(d2) == d1.dim());
        IteratorMDO itD1 = d1.iterator();
        TCheie cPrec = itD1.element().first;

        itD1.urmator();
        while (itD1.valid()) {
            TCheie c = itD1.element().first;
            assert(cresc(cPrec, c));
            cPrec = c;
            itD1.urmator();
        }

        IteratorMDO itD2 = d2.iterator();
        while(itD2.valid()){
            TCheie c = itD2.element().first;
            assert(!d1.cauta(c).empty());
            itD2.urmator();
        }
};

void testAllExtins() {
	testCreeaza();
	testCauta();
	testSterge();
	testIterator();
}
