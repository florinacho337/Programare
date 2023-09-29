#include <iostream>
#include <vector>
#include <fstream>
#include <limits>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab3/ex1/1/7-in.txt");

typedef struct{
    int x, y, w; // x - nodul sursa, y - nodul destinatie, w - pondere
}arc;

void Bellman_Ford(vector<arc> arce, int nr_noduri, int sursa, vector<int> &costuri){
    //initializare
    costuri.assign(nr_noduri, INT32_MAX);
    costuri[sursa] = 0;

    //algoritm
    for(int i = 1; i < nr_noduri; ++i){
        for(auto arc : arce){
            if(costuri[arc.x] != INT32_MAX && costuri[arc.y] > costuri[arc.x] + arc.w)
                costuri[arc.y] = costuri[arc.x] + arc.w;
        }
    }
}

int main(int argc, char* argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    int nr_noduri, nr_arce, sursa;
    vector<arc> arce; // graful va fi stocat sub forma unui vector de arce
    vector<int> costuri; // vectorul rezultat
    fin >> nr_noduri >> nr_arce >> sursa;
    for(int i = 0; i < nr_arce; ++i) {
        int x, y, w;
        fin >> x >> y >> w;
        arce.push_back(arc{x, y, w});
    }
    Bellman_Ford(arce, nr_noduri, sursa, costuri);
    for(auto cost: costuri)
        if(cost == INT32_MAX)
            cout << "INF ";
        else
            cout << cost << " ";
    fin.close();
    //fout.close();
    return 0;
}
