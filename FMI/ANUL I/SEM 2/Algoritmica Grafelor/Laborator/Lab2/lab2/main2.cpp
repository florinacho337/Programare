//EXERCITIUL 2 - INCHIDERE TRANZITIVA
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab2/ex2/graf2.txt");

void DFS(int **matriceDeAdiacenta, int n, int* viz, int i) {
    viz[i] = 1; // nodul i este vizitat
    for(int j = 0; j < n; ++j)
        //daca nodul j nu este vizitat, iar pe pozitia j de pe randul nodului se afla 1 (i si j sunt vecini)
        //atunci se repeta procesul pentru j (viz[j] = 1 la urmatorul apel al functiei DFS)
        if(matriceDeAdiacenta[i][j] == 1 && viz[j] == 0)
            DFS(matriceDeAdiacenta, n, viz, j);
}

void initializeaza(int* lista, int n){
    for(int i = 0; i < n; ++i)
        lista[i] = 0;
}

void matriceDeExistentaDrumuri(int** matriceDeAdiacenta, int n){
    int *viz = new int[n];
    for(int i = 0; i < n; ++i){
        initializeaza(viz, n); // de fiecare data lista de noduri vizitate se initializeaza la 0
        DFS(matriceDeAdiacenta, n, viz, i);
        for(int j = 0; j < n; ++j)
            //se observa ca pe liniile fiecarui nod sursa valoarea 1 apare in dreptul nodurilor accesibile din sursa
            //astfel, in lista viz se va salva 1 daca exista un drum de la sursa pana la nodul respectiv si 0 altfel
            matriceDeAdiacenta[i][j] = viz[j]; // se copiaza valorile din lista de varfuri vizitate in matricea rezultat
    }
    delete[] viz;
}

int main() {
    int v; //v- nr varfuri
    fin >> v;
    int** matriceDeAdiacenta = new int*[v]; // graful se retine sub forma unei matrice de adiacenta
    for(int i = 0; i < v; ++i) {
        matriceDeAdiacenta[i] = new int[v];
        matriceDeAdiacenta[i][i] = 1;
    }
    while(!fin.eof()){
        int x, y; //x, y - varfuri
        fin >> x >> y;
        matriceDeAdiacenta[x-1][y-1] = 1;
        //matriceDeAdiacenta[y-1][x-1] = 1; // se decomenteaza daca se vrea graf neorientat
    }
    //afiseaza matricea initiala
    for(int i = 0; i < v; ++i){
        for(int j = 0; j < v; ++j)
            cout << matriceDeAdiacenta[i][j] << " ";
        cout << "\n";
    }
    matriceDeExistentaDrumuri(matriceDeAdiacenta, v);

    cout << "=================\n";
    //afiseaza matricea finala
    for(int i = 0; i < v; ++i){
        for(int j = 0; j < v; ++j)
            cout << matriceDeAdiacenta[i][j] << " ";
        cout << "\n";
    }
    //dealocare
    for(int i = 0; i < v; ++i)
        delete[] matriceDeAdiacenta[i];
    delete[] matriceDeAdiacenta;
    return 0;
}
