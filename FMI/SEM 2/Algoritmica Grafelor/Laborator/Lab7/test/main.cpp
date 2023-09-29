#include <iostream>
#include <vector>
#include <fstream>
#include <climits>
#include <queue>

using namespace std;

bool bfs(const vector<vector<int>>& graf, int s, int t, vector<int>& parinti){
    vector<bool> vizitat(graf.size(), false);

    queue<int> Q;
    vizitat[s] = true;
    Q.push(s);
    parinti[s] = -1;

    while(!Q.empty()){
        int u = Q.front();
        Q.pop();

        for(int v = 0; v < graf.size(); ++v){
            if(!vizitat[v] && graf[u][v] > 0){
                Q.push(v);
                parinti[v] = u;
                vizitat[v] = true;
            }
        }
    }
    return vizitat[t];
}

int edmonds_karp(vector<vector<int>>& graf, int s, int t){
    int u, v;
    vector<int> parinti(graf.size());
    int flux_maxim = 0;

    while(bfs(graf, s, t, parinti)){
        int flux_drum = INT_MAX;
        for(v = t; v != s; v=parinti[v]){
            u = parinti[v];
            flux_drum = min(flux_drum, graf[u][v]);
        }

        for(v = t; v != s; v = parinti[v]){
            u = parinti[v];
            graf[u][v] -= flux_drum;
            graf[v][u] += flux_drum;
        }
        flux_maxim += flux_drum;

    }
    return flux_maxim;
}

int main(int agrc, char* argv[]) {
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab7/test/2/10-in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab7/test/out.txt");
    int nr_vf, nr_muchii;
    fin >> nr_vf >>  nr_muchii;
    vector<vector<int>> graf(nr_vf, vector<int>(nr_vf));
    for(int i = 0; i < nr_muchii; ++i){
        int u, v, f;
        fin >> u >> v >> f;
        graf[u][v] = f;
    }

    fout << edmonds_karp(graf, 0, (int)graf.size()-1);
    fin.close();
    fout.close();
    return 0;
}
