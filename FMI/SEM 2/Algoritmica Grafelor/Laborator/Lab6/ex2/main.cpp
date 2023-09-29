#include <iostream>
#include <vector>
#include <fstream>
#include <climits>
#include <list>

using namespace std;

void initializare_preflux(vector<vector<int>> graf, int s, int t, vector<int>& exces, vector<int>& inaltime){
    inaltime[s] = (int)graf.size();
    for(int v = 0; v < graf.size(); ++v){
        if(graf[s][v] > 0){
            exces[v] = graf[s][v];
            exces[s] -= graf[s][v];
        }
    }
}

void inaltare(int u, vector<int>& inaltime, const vector<int>& vecini){
    int minim = INT_MAX;
    for(int i = 0; i < vecini.size(); ++i)
        if(vecini[i] > 0 && inaltime[i] < minim)
            minim = inaltime[i];
    if(minim != INT_MAX)
        inaltime[u] = 1 + minim;
}

void pompare(vector<vector<int>>& graf, int u, int v, vector<int>& exces){
    int flux = min(exces[u], graf[u][v]);
    graf[u][v] -= flux;
    graf[v][u] += flux;
    exces[u] -= flux;
    exces[v] += flux;
}

bool are_vecini(int u, const vector<int>& vecini){
    bool are = false;
    for(const auto& v: vecini)
        if(v != 0)
            are = true;
    return are;
}

void descarcare(int u, vector<int>& exces, vector<int>& inaltime, vector<vector<int>>& graf){
    while(exces[u] > 0 && are_vecini(u, graf[u])) {
        for(int v = 0; v < graf.size(); ++v){
            if(graf[u][v] > 0 && inaltime[u] == inaltime[v] + 1)
                pompare(graf, u, v, exces);
        }
        inaltare(u, inaltime, graf[u]);
    }
}

int pompare_topologica(vector<vector<int>>& graf, int s, int t){
    vector<int> exces(graf.size(), 0);
    vector<int> inaltime(graf.size(), 0);
    initializare_preflux(graf, s, t, exces, inaltime);
    list<int> L;
    for(int i = 0; i < graf.size(); ++i)
        if(i != s && i != t)
            L.push_back(i);
    auto it = L.begin();
    while(it != L.end() && inaltime[*it] <= inaltime[s]){
        auto inaltime_veche = inaltime[*it];
        descarcare(*it, exces, inaltime, graf);
        if(inaltime[*it] > inaltime_veche)
            L.splice(L.begin(), L, it);
        it++;
    }
    return exces[t];
}

int main(int argc, char* argv[]) {
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex2/2/9-in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex2/out.txt");
    int nr_vf, nr_muchii;
    fin >> nr_vf >> nr_muchii;
    vector<vector<int>> graf(nr_vf, vector<int>(nr_vf));
    for(int i = 0; i < nr_muchii; ++i){
        int u, v, f;
        fin >> u >> v >> f;
        graf[u][v] = f;
    }
    fout << pompare_topologica(graf, 0, (int)graf.size()-1);
    return 0;
}
