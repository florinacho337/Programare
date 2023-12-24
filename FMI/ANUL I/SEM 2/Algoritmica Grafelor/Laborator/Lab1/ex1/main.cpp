#include <iostream>
#include <fstream>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab1/ex1/in.txt");

struct Muchie{
    int x, y;
    Muchie(int x = 0, int y = 0){
        this->x=x;
        this->y=y;
    }
};

int m; //nr muchii
int n; //nr noduri

int matriceDeAdiacenta1[100][100];
int matriceDeAdiacenta2[100][100];
int listaDeAdiacenta1[100][100];
int listaDeAdiacenta2[100][100];
int listaDeAdiacenta3[100][100];
int matriceDeIncidenta[100][100];

bool exista1(Muchie muchie){
    if(matriceDeAdiacenta1[muchie.x][muchie.y] == 1)
        return true;
    return false;
}

void insert(Muchie muchie){
    if(!exista1(muchie))
        matriceDeAdiacenta1[muchie.x][muchie.y] = matriceDeAdiacenta1[muchie.y][muchie.x] = 1;
}

void lista_de_adiacenta1(){
    for(int i = 1; i <= n; ++i){
        int c = 0; //numarul vecinilor
        for(int j = 1; j <= n; ++j)
            if(matriceDeAdiacenta1[i][j] == 1)
                listaDeAdiacenta1[i][++c] = j;
        listaDeAdiacenta1[i][0] = c;
    }
}

void matrice_de_incidenta(){
    for(int i = 1; i <= n; ++i)
        for(int j = 1; j <= listaDeAdiacenta1[i][0]; ++j){
            int vecin = listaDeAdiacenta1[i][j]; // i - nod, vecin - nod vecin
            if(i < vecin)
                matriceDeIncidenta[i][m] = matriceDeIncidenta[vecin][++m] = 1;
        }
}

void lista_de_adiacenta2(){
    for(int j = 1; j <= m; ++j) {
        int n1 = -1, n2 = -1; // n1, n2 - perechea de noduri
        for (int i = 1; i <= n; ++i)
            if (matriceDeIncidenta[i][j] == 1) {
                if (n1 != -1)
                    n2 = i;
                else
                    n1 = i;
            }
        int v1 = ++listaDeAdiacenta2[n1][0];
        int v2 = ++listaDeAdiacenta2[n2][0];
        listaDeAdiacenta2[n1][v1] = n2;
        listaDeAdiacenta2[n2][v2] = n1;
    }
}

void matrice_de_adiacenta(){
    for(int i = 1; i <= n; ++i)
        for(int j = 1; j <= listaDeAdiacenta2[i][0]; ++j){
            int vecin = listaDeAdiacenta2[i][j];
            if(i < vecin)
                matriceDeAdiacenta2[i][vecin] = matriceDeAdiacenta2[vecin][i] = 1;
        }
}

void lista_de_adiacenta3(){
    for(int i = 1; i <= n; ++i){
        int c = 0; //numarul vecinilor
        for(int j = 1; j <= n; ++j)
            if(matriceDeAdiacenta2[i][j] == 1)
                listaDeAdiacenta3[i][++c] = j;
        listaDeAdiacenta3[i][0] = c;
    }
}

int main()
{
    fin >> n;
    for(int i = 1; i <= n; ++i){
        int a, b;
        fin >> a >> b;
        Muchie muchie = Muchie(a, b);
        insert(muchie);
    }

    cout << "FISIER -> MATRICE DE ADIACENTA\n";
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; ++j)
            cout << matriceDeAdiacenta1[i][j] << " ";
        cout << endl;
    }

    cout << "\nMATRICE DE ADIACENTA -> LISTA DE ADIACENTA\n";
    lista_de_adiacenta1();
    for(int i = 1; i <= n; i++){
        cout << i << ": ";
        for(int j = 1; j <= listaDeAdiacenta1[i][0]; ++j)
            cout << listaDeAdiacenta1[i][j] << " ";
        cout << endl;
    }

    cout << "\nLISTA DE ADIACENTA -> MATRICE DE INCIDENTA\n";
    matrice_de_incidenta();
    for(int i = 1; i <= n; ++i){
        for(int j = 1; j <= m; ++j)
            cout << matriceDeIncidenta[i][j] << " ";
        cout << endl;
    }

    cout << "\nMATRICE DE INCIDENTA -> LISTA DE ADIACENTA\n";
    lista_de_adiacenta2();
    for(int i = 1; i <= n; ++i){
        cout << i << ": ";
        for(int j = 1; j <= listaDeAdiacenta2[i][0]; ++j)
            cout << listaDeAdiacenta2[i][j] << " ";
        cout << endl;
    }

    cout << "\nLISTA DE ADIACENTA -> MATRICE DE ADIACENTA\n";
    matrice_de_adiacenta();
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; ++j)
            cout << matriceDeAdiacenta2[i][j] << " ";
        cout << endl;
    }

    cout << "\nMATRICE DE ADIACENTA -> LISTA DE ADIACENTA\n";
    lista_de_adiacenta3();
    for(int i = 1; i <= n; i++){
        cout << i << ": ";
        for(int j = 1; j <= listaDeAdiacenta3[i][0]; ++j)
            cout << listaDeAdiacenta3[i][j] << " ";
        cout << endl;
    }
    return 0;
}