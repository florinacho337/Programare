#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <cstring>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab2/ex3/labirint_1.txt");

vector<vector<int>> citesteLabirint(int &xstart, int &ystart, int &xfinish, int &yfinish){
    vector<vector<int>> labirint;
    char* str = new char[1000];
    fin.getline(str, 1000);
    size_t m = strlen(str); // lungimea liniilor care alcatuiesc matricea
    labirint.emplace_back(m+2, -1); // pentru bordarea matricei
    int n = 1; // numarul de linii citite
    while(!fin.eof()) {
        vector<int> linie;
        linie.push_back(-1); // la inceputul liniei se adauga -1 pentru a borda matricea
        for(int i = 0; i < m; ++i){
            switch(str[i]){
                case 'S': // pozitia de start
                    xstart = n;
                    ystart = i+1;
                    linie.push_back(0);
                    break;
                case 'F': // pozitia de finish
                    xfinish = n;
                    yfinish = i+1;
                    linie.push_back(0);
                    break;
                case '1': // zid
                    linie.push_back(-1);
                    break;
                default: // drum liber
                    linie.push_back(0);
            }
        }
        linie.push_back(-1);// la final se adauga -1 pentru a borda matricea
        labirint.push_back(linie); // se adauga linia creata in labirint
        n++; // numarul de linii se incrementeaza
        fin.getline(str, 1000);
    }
    vector<int> linie;
    for(int i = 0; i < m; ++i){
        switch(str[i]){
            case 'S': // pozitia de start
                xstart = n;
                ystart = i+1;
                linie.push_back(0);
                break;
            case 'F': // pozitia de finish
                xfinish = n;
                yfinish = i+1;
                linie.push_back(0);
                break;
            case '1': // zid
                linie.push_back(-1);
                break;
            default: // drum liber
                linie.push_back(0);
        }
    }
    labirint.push_back(linie); // se adauga linia creata in labirint
    labirint.emplace_back(m+2, -1); // se adauga o ultima linie pentru bordarea matricei
    delete[] str;
    return labirint;
}

void setListaDeAdiacenta(vector<vector<int>> labirint, vector<vector<int>> listaDeAdiacenta, int xstart, int ystart, int xfinish, int yfinish, int &start, int &finish){
    int nod = 1; // vom considera spatiile goale ca fiind noduri
    for(int i = 1; i < labirint.size(); ++i)
        for(int j = 1; j < labirint[i].size(); ++j)
            if(labirint[i][j] == 0)
                labirint[i][j] = nod++; // atribuim pe pozitia i,j din labirint valoarea lui nod, apoi o incrementam
    vector<int> vecini;
    listaDeAdiacenta.assign(nod, vecini); // se creeaza o lista de adiacenta
    start = labirint[xstart][ystart]; // se seteaza nodul sursa
    finish = labirint[xfinish][yfinish]; // se seteaza nodul destinatie
    for(int i = 1; i < labirint.size(); ++i)
        for(int j = 1; j < labirint[i].size(); ++j)
            if(labirint[i][j] != -1){
                if(labirint[i-1][j] != -1)
                    listaDeAdiacenta[labirint[i][j]].push_back(labirint[i-1][j]);
                if(labirint[i][j-1] != -1)
                    listaDeAdiacenta[labirint[i][j]].push_back(labirint[i][j-1]);
                if(labirint[i+1][j] != -1)
                    listaDeAdiacenta[labirint[i][j]].push_back(labirint[i+1][j]);
                if(labirint[i][j+1] != -1)
                    listaDeAdiacenta[labirint[i][j]].push_back(labirint[i][j+1]);
            }

}

void bfs(vector<vector<int>> listaDeAdiacenta, int start, vector<int> &lungimi){
    lungimi.assign(listaDeAdiacenta.size(), -1);
    queue<int> Queue;
    Queue.push(start);
    lungimi[start] = 0; // lungimea varfului sursa va fi initializata cu 0
    while(!Queue.empty()){
        int varf = Queue.front(); // luam varful din coada, apoi il stergem
        Queue.pop();
        for(int i = 0; i < listaDeAdiacenta[varf].size(); ++i) {
            int vecin = listaDeAdiacenta[varf][i]; // iteram prin vecinii nodului ales
            if (lungimi[vecin] == -1){
                lungimi[vecin] = lungimi[varf] + 1; // lungimea de la sursa pana la vecin va fi lungimea pana la varf +1
                Queue.push(vecin); // se adauga in coada varful vecin
            }
        }
    }
}
void reconstruieste_drum(vector<vector<int>> labirint, vector<int> lungimi, int xstart, int ystart, int xfinish, int yfinish){
    int i = xfinish, j = yfinish;
    while(i != xstart || j != ystart){
        cout << i << " " << j << endl;
        if(labirint[i-1][j] != -1 && lungimi[labirint[i-1][j]] + 1 == lungimi[labirint[i][j]])
            i--;
        else if(labirint[i+1][j] != -1 && lungimi[labirint[i+1][j]] + 1 == lungimi[labirint[i][j]])
            i++;
        else if(labirint[i][j-1] != -1 && lungimi[labirint[i][j-1]] + 1 == lungimi[labirint[i][j]])
            j--;
        else if(labirint[i][j+1] != -1 && lungimi[labirint[i][j+1]] + 1 == lungimi[labirint[i][j]])
            j++;
    }
    cout << i << " " << j << endl;
}

int main() {
    int xstart, ystart, xfinish, yfinish, start, finish;
    vector<vector<int>> listaDeAdiacenta;
    vector<vector<int>> labirint = citesteLabirint(xstart, ystart, xfinish, yfinish);
    setListaDeAdiacenta(labirint, listaDeAdiacenta, xstart, ystart, xfinish, yfinish, start, finish);
    vector<int> lungimi;
    bfs(listaDeAdiacenta, start, lungimi);
//    reconstruieste_drum(labirint, lungimi, xstart, ystart, xfinish, yfinish);
    return 0;
}
