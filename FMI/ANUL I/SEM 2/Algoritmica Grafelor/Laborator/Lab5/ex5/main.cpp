#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <algorithm>

using namespace std;

struct muchie{
    int x, y, w;
};

class DisjointSet { //to represent disjoint set
    unordered_map<int, int> parent;
public:
    void makeSet(vector<int> const &wholeset){
        //perform makeset operation
        for (int i : wholeset) // create n disjoint sets
            parent[i] = i;
    }
    int Find(int l) { // Find the root of the set in which element l belongs
        if (parent[l] == l) // if l is root
            return l;
        return Find(parent[l]); // recurs for parent till we find root
    }
    void Union(int m, int n) { // perform Union of two subsets m and n
        int x = Find(m);
        int y = Find(n);
        parent[x] = y;
    }
};

vector<muchie> Kruskal(vector<muchie>& muchii, int nr_vf){
    vector<muchie> A;
    vector<int> varfuri(nr_vf);
    for(int i = 0; i < nr_vf; ++i)
        varfuri.push_back(i);
    DisjointSet sets;
    sets.makeSet(varfuri);
    sort(muchii.begin(), muchii.end(), [](muchie m1, muchie m2){
        return m1.w < m2.w;
    });
    for(auto m: muchii)
        if(sets.Find(m.x) != sets.Find(m.y)){
            A.push_back(m);
            sets.Union(m.x, m.y);
        }
    sort(A.begin(), A.end(), [](muchie m1, muchie m2){ //pentru testul 10 vectorul A nu trebuie sortat
        if(m1.x < m2.x || (m1.x == m2.x && m1.y < m2.y))
            return true;
        return false;
    });
    return A;
}

int main(int argc, char* argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex5/9-in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex5/out.txt");
    int nr_vf, nr_muchii;

    //CITIRE
    vector<muchie> muchii;
    fin >> nr_vf >> nr_muchii;
    for(int i = 0; i < nr_muchii; ++i){
        int x, y, w;
        fin >> x >> y >> w;
        muchii.push_back(muchie{x, y, w});
    }

    //AFISARE
    vector<muchie> K = Kruskal(muchii, nr_vf);
    int cost = 0;
    for(auto m: K)
        cost += m.w;
    fout << cost << "\n" << K.size() << "\n"; // costul si nr de varfuri existente in arbore
    for(auto m: K)
        fout << m.x << " " << m.y << "\n"; // muchiile din arbore
    fin.close();
    fout.close();
    return 0;
}
