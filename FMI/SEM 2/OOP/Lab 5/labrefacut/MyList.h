//
// Created by florin on 29.03.2023.
//

#ifndef LABREFACUT_MYLIST_H
#define LABREFACUT_MYLIST_H

typedef void* ElemType;
typedef void(*DestroyFct) (ElemType);
typedef ElemType(*CopyFct) (ElemType);

typedef struct lista{
    int l, cp;
    ElemType* list;
    DestroyFct destroy;
}MyList;

/*
 * creeaza o lista goala
 * destroy - functie de dstroy specifica elementelor
 * returneaza o lista goala de elemente de tip ElemType
 */
MyList* createEmpty(DestroyFct destroy);

/*
 * distruge lista
 */
void destroyList(MyList* l);

/*
 * ia un element de pe pozitia poz
 * poz - intreg
 * returneaza elementul de pe pozitia poz
 */
ElemType get(MyList* l, int poz);

/*
* modifica elementul de pe pozitia poz cu elementul p
* returneaza elementul rescris
*/
ElemType set(MyList* l, int poz, ElemType p);

/*
 * returneaza dimensiunea listei
 */
int size(MyList* l);

/*
 * adauga elementul p la finalul listei
 */
void add(MyList* l, ElemType p);

/*
* sterge ultimul element din lista
* returneaza ultimul element din lista
*/
ElemType removeLast(MyList* l);

/*
 * sterge elementul de pe pozitia poz din lista
 * poz - intreg
 */
void removeP(MyList* l, int poz);

/*
 * face o copie a listei
 * returneaza o lista cu aceleasi elemente din lista l
 */
MyList* copyList(MyList* l, CopyFct copy);

void testCreateList();
void testIterateList();
void testCopyList();
void testResize();
void testListOfLists();
void testListOfInts();
void testRemoveLast();

#endif //LABREFACUT_MYLIST_H
