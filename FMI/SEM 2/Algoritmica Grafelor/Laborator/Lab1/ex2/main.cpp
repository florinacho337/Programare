#include <iostream>
#include <fstream>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab1/ex2/in.txt");

struct Muchie{
    int x, y; // cele doua noduri ce compun muchia
    Muchie(int x, int y){
        this->x = x;
        this->y = y;
    }
};

int n; // numarul de noduri
int **matriceDeAdiacenta; // matricea de adiacenta

void alocare_matrice_adiacenta(){
    // se aloca memorie pentru matrice
    matriceDeAdiacenta = new int*[n];
    for(int i = 0; i < n; ++i){
        matriceDeAdiacenta[i] = new int[n];
    }
}

void dealocare_matrice_adiacenta(){
    //se dealoca spatiul utilizat de matricea de adiacenta
    for(int i = 0; i < n; ++i)
        delete[] matriceDeAdiacenta[i];
    delete[] matriceDeAdiacenta;
}

bool exista(Muchie muchie){
    // verifica daca exista muchia in matricea de adiacenta
    if(matriceDeAdiacenta[muchie.x-1][muchie.y-1] == 1)
        return true;
    return false;
}

void adauga(Muchie muchie){
    // adauga o noua muchie in matricea de adiacenta
    if(!exista(muchie))
        matriceDeAdiacenta[muchie.x-1][muchie.y-1] = matriceDeAdiacenta[muchie.y-1][muchie.x-1] = 1;
}

void noduri_izolate(int *lista, int &c) {
    // in lista se vor salva nodurile izolate, iar in c numarul acestora
    for (int i = 0; i < n; ++i) {
        bool izolat = true;
        for (int j = 0; j < n; ++j)
            if (matriceDeAdiacenta[i][j] == 1)
                izolat = false;
        if (izolat)
            lista[c++] = i+1;
    }
}

bool graf_regular(){
    int nr_vecini1 = 0; // se vor numara vecinii primului nod
    for(int j = 0; j < n; ++j)
        if(matriceDeAdiacenta[0][j] == 1)
            nr_vecini1++;
    for(int i = 1; i < n; ++i){
        int nr_vecini = 0; // pentru fiecare nod se numara vecinii
        for(int j = 0; j < n; ++j)
            if(matriceDeAdiacenta[i][j] == 1)
                nr_vecini++;
        if(nr_vecini != nr_vecini1)
            return false; // daca numarul vecinilor primului nod nu coincide cu numarul vecinilor unui alt nod, graful nu este regular
    }

    return true;
}

void matricea_distantelor(int** md){
    //se formeaza matricea distantelor
    for(int i = 0; i < n; ++i)
        for(int j = 0; j < n; ++j)
            //se initializeaza matricea distantelor
            if(matriceDeAdiacenta[i][j] == 0 && i != j)
                md[i][j] = n;
            else
                md[i][j] = matriceDeAdiacenta[i][j];

    for(int k = 0; k < n; ++k)
        for(int i = 0; i < n; ++i)
            for(int j = 0; j < n; ++j)
                if(i != j)
                    if(md[i][j] > md[i][k] + md[k][j])
                        md[i][j] = md[i][k] + md[k][j]; // lungimea lantului de la i la j este minimul dintre
                                                        // valoarea curenta si lungimea prin nodul intermediar k

}

void DFS(int* viz, int x){
    // se parcurge graful in adancime, iar pentru nodurile parcurse se stocheaza in viz valoarea 1
    viz[x-1] = 1;
    for(int i = 0; i < n; ++i)
        if(matriceDeAdiacenta[x-1][i] == 1 && viz[i] == 0)
            DFS(viz, i+1);
}

bool graf_conex(int* viz){
    // se verifica daca graful este conex
    DFS(viz, 1);
    for(int i = 0; i < n; ++i)
        if(viz[i] == 0) return false; // daca nodul i+1 nu a fost vizitat/parcurs, inseamna ca nu exista
                                      // cel putin un drum de la acesta catre oricare alt nod
    return true;
}

int main() {
    fin >> n; // se introduce numarul de noduri
    alocare_matrice_adiacenta(); // se aloca memorie pentru matricea de adiacenta
    while(!fin.eof()){
        int x, y;
        fin >> x >> y; // se citesc din fisier nodurile x, y
        Muchie muchie(x, y); // se creaza o muchie cu nodurile x, y
        adauga(muchie); // se adauga muchia la matricea de adiacenta
    }

    //afisare noduri izolate
    int *lista_noduri_izolate = new int[n];
    int c = 0;
    noduri_izolate(lista_noduri_izolate, c);
    if(c != 0) {
        cout << "Noduri izolate: ";
        for (int i = 0; i < c; ++i)
            cout << lista_noduri_izolate[i] << " ";
    } else
        cout << "Nu exista noduri izolate.";
    //dealocare memorie
    delete[] lista_noduri_izolate;
    cout << "\n";

    //verifica daca graful e regular
    if(graf_regular())
        cout << "Graful este regular.";
    else
        cout << "Graful nu este regular.";
    cout << "\n";

    //calculeaza matricea distantelor
    int** md = new int*[n]; //se aloca spatiu pentru matricea distantelor
    for(int i = 0; i < n; ++i)
        md[i] = new int[n];
    matricea_distantelor(md);
    //se afiseaza matricea distantelor
    cout << "Matricea distantelor:\n";
    for(int i = 0; i < n; ++i){
        for(int j = 0; j < n; ++j)
            if(md[i][j] == n)
                cout << "inf ";
            else
                cout << md[i][j] << " ";
        cout << "\n";
    }
    //se dealoca spatiul utilizat
    for(int i = 0; i < n; ++i)
        delete[] md[i];
    delete[] md;

    //verifica daca graful este conex
    int *viz = new int[n]; // se aloca spatiu pentru lista de noduri vizitate/parcurse
    if(graf_conex(viz))
        cout << "Graful este conex.";
    else
        cout << "Graful nu este conex.";
    delete[] viz; // se dealoca spatiul ocupat de lista de noduri vizitate

    dealocare_matrice_adiacenta();// se dealoca spatiul ocupat de matricea de adiacenta
    return 0;
}
