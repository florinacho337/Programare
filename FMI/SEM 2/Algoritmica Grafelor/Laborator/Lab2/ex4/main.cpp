//EXERCITIUL 4 - BFS
#include <iostream>
#include <queue>
#include <fstream>
#include <vector>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab2/ex4/graf.txt");

void BFS(vector<queue<int>> listaDeAdiacenta, int n, int sursa){
    queue<int> q;//coada
    int* culori = new int[n+1]; // vectorul de culori, -1 este alb, 0 este gri, 1 este negru
    int* distante = new int[n+1]; // vectorul de distante de la sursa la varfurile respective
    //initializeaza vectorii de distante si de culori
    for(int i = 1; i <= n; ++i)
        distante[i] = culori[i] = -1;
    culori[sursa] = 0; // sursa este vizitata, dar are vecini nevizitati
    distante[sursa] = 0; // distanta initiala a nodului sursa va fi 0
    q.push(sursa); // adaugam nodul sursa in coada
    while(!q.empty()){
        int nod = q.front();
        q.pop();
        while(!listaDeAdiacenta[nod].empty()){
            int vecin = listaDeAdiacenta[nod].front(); // se ia cate un vecin din lista vecinilor nodului
            listaDeAdiacenta[nod].pop(); // nod si se scoate din coada
            if (culori[vecin] == -1) {
                culori[vecin] = 0; // se actualizeaza culoarea vecinului
                distante[vecin] = distante[nod] + 1; // se actualizeaza distanta vecinului
                q.push(vecin); // se pune in coada vecinul
            }
        }
        culori[nod] = 1; // nodul a fost parcurs complet
    }
    //afisare
    cout << "varf distanta\n";
    for(int i = 1; i <= n; ++i){
        if(distante[i] != -1) // daca exista o distanta de la sursa la nodul i, atunci afiseaza
            cout << i << "     " << distante[i] << "\n";
        else
            cout << i << "     inf\n";
    }
    delete[] culori;
    delete[] distante;
}

int main() {
    int varfuri;
    fin >> varfuri;
    vector<queue<int>> listaDeAdiacenta(varfuri+1);
    while(!fin.eof()){
        int x, y;
        fin >> x >> y;
        listaDeAdiacenta[x].push(y);//se adauga in lista de vecini a nodului x, nodul y
        //listaDeAdiacenta[y].push(x);//vice-versa ca mai sus, se decomenteaza linia pentru varianta de graf neorientat
    }
    cout << "Introduceti varful sursa: ";
    int sursa;
    cin >> sursa;
    cout << "Varfuri accesibile din varful sursa: \n";
    BFS(listaDeAdiacenta, varfuri, sursa);
    return 0;
}
