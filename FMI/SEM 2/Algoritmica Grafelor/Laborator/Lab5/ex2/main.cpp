#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

int minim(const vector<int>& K, int nr_vf){
    vector<int> frecv(nr_vf, 0);
    for(auto i: K)
        frecv[i] = 1;
    int rez;
    for(int i = nr_vf-1; i >= 0; i--)
        if(frecv[i] == 0)
            rez = i;
    return rez;
}

vector<int> decodare_prufer(vector<int>& K, int nr_vf){
    vector<int> tati(nr_vf, -1);
    for(int i = 1; i < nr_vf; ++i){
        int x = K[0];
        int y = minim(K, nr_vf);
        tati[y] = x;
        K.erase(K.begin());
        K.push_back(y);
    }
    return tati;
}

int main(int argc, char* argv[]) {
    ifstream fin(argv[1]);
    ofstream fout(argv[2]);
//    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex2/9-in.txt");
//    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex2/out.txt");
    vector<int> K;
    int nr_vf;
    fin >> nr_vf;
    for(int i = 0; i < nr_vf; ++i){
        int x;
        fin >> x;
        K.push_back(x);
    }
    vector<int> tati = decodare_prufer(K, nr_vf+1);
    fout << tati.size() << "\n";
    for(auto i: tati)
        fout << i << " ";
    fin.close();
    fout.close();
    return 0;
}
