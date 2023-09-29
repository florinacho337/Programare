//
// Created by florin on 26.03.2023.
//


#include <assert.h>
#include <malloc.h>
#include <string.h>
#include "domain.h"
#include "MyList.h"

MyList* createEmpty(DestroyFct destroy){
    MyList* l = malloc(sizeof(MyList));
    l->l = 0;
    l->cp = 2;
    l->destroy = destroy;
    l->list = malloc(sizeof(ElemType) * l->cp);
    return l;
}


void destroyList(MyList* l){
    for(int i = 0; i < l->l; ++i)
        l->destroy(l->list[i]);
    free(l->list);
    free(l);
}

ElemType get(MyList* l, int poz){
    return l->list[poz];
}

ElemType set(MyList* l, int poz, ElemType p){
    ElemType rez = l->list[poz];
    l->list[poz] = p;
    return rez;
}

int size(MyList* l){
    return l->l;
}

/*
 * asigura ca exista destul loc in lista pentru adaugarea elementelor
 */
void ensureCapacity(MyList* l){
    if(l->l < l->cp)
        return;
    ElemType* nElems = malloc(sizeof(ElemType) * (l->cp + 4));
    for(int i = 0; i < l->l; ++i)
        nElems[i] = l->list[i];
    free(l->list);
    l->list = nElems;
    l->cp = l->cp + 4;
}

/*
 * adauga elementul p la finalul listei
 */
void add(MyList* l, ElemType p){
    ensureCapacity(l);
    l->list[l->l] = p;
    l->l++;
}

/*
 * sterge ultimul element din lista
 * returneaza ultimul element din lista
 */
ElemType removeLast(MyList* l){
    ElemType rez = l->list[l->l - 1];
    l->l--;
    return rez;
}

/*
 * sterge elementul de pe pozitia poz din lista
 * poz - intreg
 */
void removeP(MyList* l, int poz){
    l->destroy(l->list[poz]);
    for(int i = poz; i < l->l-1; ++i)
        l->list[i] = l->list[i+1];
    l->l--;
}

/*
 * face o copie a listei
 * returneaza o lista cu aceleasi elemente din lista l
 */
MyList* copyList(MyList* l, CopyFct copy){
    MyList* copie = createEmpty(l->destroy);
    for(int i = 0; i < size(l); ++i) {
        ElemType e = get(l, i);
        add(copie, copy(e));
    }
    return copie;
}

void testCreateList() {
    MyList* l = createEmpty((DestroyFct) destroyTranzactie);
    assert(size(l) == 0);
    destroyList(l);
}
void testIterateList() {
    MyList* l = createEmpty((DestroyFct)destroyTranzactie);
    add(l, creeazaTranzactie( 10, 100, "tip1", "descriere1"));
    add(l, creeazaTranzactie( 15, 245, "tip2", "descriere2"));
    assert(size(l) == 2);
    Tranzactie* p = (Tranzactie*)get(l,0);

    assert(strcmp(p->tip,"tip1") == 0);
    p = (Tranzactie*)get(l, 1);
    assert(strcmp(p->descriere, "descriere2") == 0);
    destroyList(l);
}
void testCopyList() {
    MyList* l = createEmpty((DestroyFct)destroyTranzactie);
    add(l, creeazaTranzactie(10, 100, "tip1", "descriere1"));
    add(l, creeazaTranzactie(15, 245, "tip2", "descriere2"));
    MyList *l2;
    l2 = copyList(l, (CopyFct)copyTranzactie);
    assert(size(l2) == 2);
    Tranzactie* p = (Tranzactie*)get(l2, 0);
    assert(strcmp(p->tip, "tip1") == 0);
    destroyList(l);
    destroyList(l2);
}
void testResize() {
    MyList* l = createEmpty((DestroyFct)destroyTranzactie);
    for (int i = 0; i < 10; i++) {
        add(l, creeazaTranzactie(20, 10, "tip", "b"));
    }
    assert(size(l) == 10);
    destroyList(l);
}
void testListOfLists() {
    MyList *listOfLists = createEmpty((DestroyFct)destroyList);
    MyList* listOfTranzactii = createEmpty((DestroyFct)destroyTranzactie);
    add(listOfTranzactii, creeazaTranzactie(20, 10, "tip", "b"));
    add(listOfTranzactii, creeazaTranzactie(20, 10, "tip", "b"));
    add(listOfTranzactii, creeazaTranzactie(20, 10, "tip", "b"));
    add(listOfLists, listOfTranzactii);
    MyList* cpy = copyList(listOfTranzactii, (CopyFct)copyTranzactie);
    add(listOfLists, cpy);
    assert(size(listOfLists) == 2);
    assert(size(listOfTranzactii) == 3);

    MyList* el2 = (MyList*)get(listOfLists, 1);
    assert(size(el2) == 3);
    removeP(listOfLists, 0);
    assert(size(listOfLists) == 1);

    destroyList(listOfLists);
}
int* createIntOnHeap(int value) {
    int* pi = (int*)malloc(sizeof(int));
    *pi = value;
    return pi;
}
void testListOfInts() {
    MyList* l = createEmpty(free);//use stdlib free to free memory

    add(l, createIntOnHeap(0));
    add(l, createIntOnHeap(1));
    add(l, createIntOnHeap(2));
    add(l, createIntOnHeap(3));
    add(l, createIntOnHeap(4));
    add(l, createIntOnHeap(0));
    assert(size(l) == 6);

    int* nr = (int*)get(l, 3);
    assert(*nr == 3);

    destroyList(l);
}
void testRemoveLast() {
    MyList* l = createEmpty((DestroyFct)destroyTranzactie);
    add(l, creeazaTranzactie(20, 10, "tip", "b"));
    add(l, creeazaTranzactie(20, 10, "tip", "b"));
    assert(size(l) == 2);
    Tranzactie* el = (Tranzactie*)removeLast(l);
    assert(size(l) == 1);
    destroyTranzactie(el);

    el = (Tranzactie*)removeLast(l);
    assert(size(l) == 0);
    destroyTranzactie(el);

    destroyList(l);
}
