#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <exception>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab3/ex2/2/6-in.txt");
ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab3/ex2/out.txt");

struct Varf{
    int x, cost;
    Varf(int x, int cost){
        this->x = x;
        this->cost = cost;
    }
};

struct Muchie{
    int x, y, w;
    Muchie(int x, int y, int w){
        this->x = x;
        this->w = w;
        this->y = y;
    }
};

struct Compare{
    bool operator()(Varf v1, Varf v2){
        return v1.cost > v2.cost;
    }
};

void Dijkstra(vector<vector<Muchie>> listaAdiacenta, int n, int sursa, vector<int> &costuri){
    costuri.assign(n, INT32_MAX);
    costuri[sursa] = 0;
    priority_queue<Varf, vector<Varf>, Compare> varfuri;
    varfuri.emplace(sursa, 0);
    while(!varfuri.empty()){
        Varf u = varfuri.top();
        varfuri.pop();
        for (auto v: listaAdiacenta[u.x])
            if(costuri[v.x] != INT32_MAX && costuri[v.x] + v.w < costuri[v.y]) {
                costuri[v.y] = costuri[v.x] + v.w;
                varfuri.emplace(v.y, costuri[v.y]);
            }
    }
}

bool BellmanFord(const vector<vector<Muchie>>& listaAdiacenta, int n, int sursa, vector<int> &costuri){
    costuri[sursa] = 0;
    for(int i = 1; i < n; ++i){
        for(auto & j : listaAdiacenta)
            for(auto m : j)
                if(costuri[m.x] != INT32_MAX && costuri[m.x] + m.w < costuri[m.y])
                    costuri[m.y] = costuri[m.x] + m.w;
    }
    for(auto & j : listaAdiacenta)
        for(auto m : j)
            if(costuri[m.x] != INT32_MAX && costuri[m.x] + m.w < costuri[m.y])
                return false;
    return true;
}

vector<vector<int>> Johnson(vector<vector<Muchie>> &listaAdiacenta, int n){
    vector<int> costuri1(n+1, INT32_MAX);
    vector<Muchie> vecini_sursa;
    vecini_sursa.reserve(n);
    for(int i = 0; i < n; ++i)
        vecini_sursa.emplace_back(n, i, 0);
    listaAdiacenta.push_back(vecini_sursa);
    if(!BellmanFord(listaAdiacenta, n+1, n, costuri1))
        throw exception();
    for(auto & i : listaAdiacenta)
        for(auto &j : i) {
            int cost_nou = j.w + costuri1[j.x] - costuri1[j.y];
            j.w = cost_nou;
        }
    vector<vector<int>> rez(n, vector<int>(n));
    listaAdiacenta.pop_back();
    vector<int> costuri2;
    for(int i = 0; i < n; ++i){
        Dijkstra(listaAdiacenta, n, i, costuri2);
        for(int j = 0; j < costuri2.size(); ++j)
            if(costuri2[j] == INT32_MAX)
                rez[i][j] = costuri2[j];
            else
                rez[i][j] = costuri2[j] + costuri1[j] - costuri1[i];
    }
    return rez;
}

int main(int argc, char * argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    int v, e;
    fin >> v >> e;
    vector<vector<Muchie>> listaAdiacenta(v);
    vector<int> costuri(v);
    for(int i = 0; i < e; ++i){
        int x, y, w;
        fin >> x >> y >> w;
        listaAdiacenta[x].emplace_back(x, y, w);
    }
    try {
        vector<vector<int>> rezultat = Johnson(listaAdiacenta, v);
        for(auto &i: listaAdiacenta)
            for(auto j: i)
                fout << j.x << " " << j.y << " " << j.w << "\n";
        for (int i = 0; i < v; ++i) {
            for (int j = 0; j < v; ++j)
                if (rezultat[i][j] != INT32_MAX)
                    fout << rezultat[i][j] << " ";
                else
                    fout << "INF ";
            fout << "\n";
        }
    }catch(exception& e) {
        fout << -1;
    }
    fin.close();
    fout.close();
    return 0;
}
