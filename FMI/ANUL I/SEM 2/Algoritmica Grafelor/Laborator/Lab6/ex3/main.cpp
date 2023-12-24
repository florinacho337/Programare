#include <iostream>
#include <vector>
#include <fstream>
#include <stack>

using namespace std;

struct muchie{
    int x, y;
    bool vizitat;
};

void Euler(vector<vector<int>>& graf, vector<muchie>& M, int s, vector<int>& ciclu){
    stack<int> S;
    S.push(s);
    while(!S.empty()){
        int nod = S.top();
        if(graf[nod].empty()) {
            ciclu.push_back(nod);
            S.pop();
        } else{
            int muchie = graf[nod].back();
            graf[nod].pop_back();
            if(!M[muchie].vizitat){
                M[muchie].vizitat = true;
                if(M[muchie].x == nod)
                    S.push(M[muchie].y);
                else
                    S.push(M[muchie].x);
            }
        }
    }
}

int main(/*int argc, char* argv[]*/) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex3/3/7-in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab6/ex3/out.txt");
    int nr_vf, nr_muchii;
    fin >> nr_vf >> nr_muchii;
    vector<vector<int>> graf(nr_vf, vector<int>(nr_vf, 0));
    vector<muchie> M;
    vector<int> ciclu;
    for(int i = 0; i < nr_muchii; ++i){
        int x, y;
        fin >> x >> y;
        M.push_back({x, y, false});
        graf[x].push_back(i);
        graf[y].push_back(i);
    }
    Euler(graf, M, 0, ciclu);
    for(int i = (int)ciclu.size()-1; i > 0; --i)
        fout << ciclu[i] << " ";
    return 0;
}
