//EXERCITIUL 5 - DFS
#include <iostream>
#include <vector>
#include <queue>
#include <fstream>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab2/ex5/graf5.txt");

void DFS_VISIT(vector<queue<int>> listaDeAdiacenta, vector<int> &culori, int varf){
    culori[varf] = 0; // culoarea pentru varful ales devine gri
    cout << varf << " ";
    while(!listaDeAdiacenta[varf].empty()){
        int vecin = listaDeAdiacenta[varf].front(); // luam fiecare vecin al varfului varf
        listaDeAdiacenta[varf].pop(); // apoi il scoatem din coada
        if(culori[vecin] == -1)
            DFS_VISIT(listaDeAdiacenta, culori, vecin); // si reluam procesul pentru acesta
    }
    culori[varf] = 1; // varful a fost parcurs complet
}

void DFS(vector<queue<int>> listaDeAdiacenta, int varfuri, int inceput){
    //initializare vector de culori, -1 = alb, 0 = gri, 1 = negru
    vector<int> culori(varfuri+1, -1);
    cout << "Varfuri vizitate, incepand de la varful " << inceput << ":\n";
    for(int i = inceput; i < varfuri + inceput; ++i) {
        int j = i;
        if(j > varfuri)
            j = j - varfuri;
        if (culori[j] == -1)
            DFS_VISIT(listaDeAdiacenta, culori, j); // aplicam algoritmul de vizitare al varfului i
    }

}

int main() {
    int nr_vf;
    fin >> nr_vf;
    vector<queue<int>> listaDeAdiacenta(nr_vf+1);
    while(!fin.eof()){
        int x, y; // nodurile ce compun o muchie
        fin >> x >> y;
        listaDeAdiacenta[x].push(y); // adaugam vecinii in cozile aferente
        //listaDeAdiacenta[y].push(x);//se decomenteaza linia pentru varianta de graf neorientat
    }
    for(int i = 1; i <= nr_vf; ++i) {
        DFS(listaDeAdiacenta, nr_vf, i);
        cout << "\n";
    }
    return 0;
}
