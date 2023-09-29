#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

bool exista(const vector<int>& tati){
    for(int i = 0; i < tati.size(); ++i)
        if(tati[i] != -1 && tati[i] != i)
            return true;
    return false;
}

int frunza_minima(const vector<int>& tati){
    vector<int> frecv(tati.size(), 0);
    int rez = -1;
    for(auto i: tati)
        if(i != -1)
            frecv[i] = 1;
    for(int i = 0; i < frecv.size(); ++i)
        if(frecv[i] == 0 && rez == -1)
            rez = i;
    return rez;
}

vector<int> Prufer(vector<int>& tati){
    vector<int> rez;
    while (exista(tati)){
        int u = frunza_minima(tati); //extrage frunza minima
        rez.push_back(tati[u]); // adauga in vectorul rezultat predecesorul frunzei extrase
        tati[u] = u; // se "elimina" din vectorul de tati frunza
    }
    return rez;
}

int main(int argc, char* argv[]) {
    ifstream fin(argv[1]);
    ofstream fout(argv[2]);
//    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex1/8-in.txt");
//    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex1/out.txt");
    int nr_noduri;
    fin >> nr_noduri;
    vector<int> tati;
    for(int i = 0; i < nr_noduri; ++i) {
        int x;
        fin >> x;
        tati.push_back(x);
    }
    fin.close();
    vector<int> rez = Prufer(tati);
    fout << rez.size() << "\n";
    for(auto i: rez)
        fout << i << " ";
    fout.close();
    return 0;
}
