#include <iostream>
#include <vector>
#include <fstream>
#include <queue>
#include <climits>

using namespace std;

bool bfs(const vector<vector<int>>& graf_rezidual, int s, int t, vector<int>& parinti){
    vector<bool> vizitat(graf_rezidual.size(), false);

    queue<int> Q;
    Q.push(s);
    parinti[s] = -1;
    vizitat[s] = true;

    while(!Q.empty()){
        int u = Q.front();
        Q.pop();

        for(int v = 0; v < graf_rezidual.size(); ++v){
            if(!vizitat[v] && graf_rezidual[u][v] > 0){
                Q.push(v);
                vizitat[v] = true;
                parinti[v] = u;
            }
        }
    }

    return vizitat[t]; // daca vizitat[t] este true, inseamna ca exista drum de la s la t
}

int edmonds_karp(vector<vector<int>> graf, int s, int t){
    int u, v;

    vector<int> parinti(graf.size());
    int flux_maxim = 0;

    while(bfs(graf, s, t, parinti)){
        //cat timp exista drum de la s la t
        int flux_drum = INT_MAX;
        for(v = t; v != s; v = parinti[v]){ // cautam fluxul maxim care poate trece de la s la t
            u = parinti[v];
            flux_drum = min(flux_drum, graf[u][v]);
        }

        for(v = t; v != s; v = parinti[v]){ // actualizare valori graf rezidual
            u = parinti[v];
            graf[u][v] -= flux_drum;
            graf[v][u] += flux_drum;
        }
        flux_maxim += flux_drum;
    }

    return flux_maxim;
}

int main(int argc, char* argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex1/1/10-in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex1/out.txt");
    int nr_vf, nr_arce;
    fin >> nr_vf >> nr_arce;
    vector<vector<int>> graf(nr_vf, vector<int>(nr_vf)); // graful va retine datele sub forma graf[u][v] = f
    for(int i = 0; i < nr_arce; ++i){
        int u, v, f;
        fin >> u >> v >> f;
        graf[u][v] = f;
    }
    fout << edmonds_karp(graf, 0, nr_vf-1);
    fin.close();
    fout.close();
    return 0;
}
