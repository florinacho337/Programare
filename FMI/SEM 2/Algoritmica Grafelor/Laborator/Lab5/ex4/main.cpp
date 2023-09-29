#include <iostream>
#include <fstream>
#include <queue>
#include <string>
#include <map>

using namespace std;

struct nod{
    string text;
    int frecv;
};

struct cmp{
    bool operator()(const nod& n1, const nod& n2){
        char min1=n1.text[0];
        for(const auto& c: n1.text)
            if(c < min1)
                min1 = c;
        char min2=n2.text[0];
        for(const auto& c: n2.text)
            if(c < min2)
                min2 = c;
        return (n1.frecv == n2.frecv && min1 > min2) || n1.frecv > n2.frecv;
    }
};

void Huffman(map<char, int>& caractere, map<char, string>& codare){
    //initializare priority queue
    priority_queue<nod, vector<nod>, cmp> Q;
    for(auto c: caractere)
        Q.push(nod{string(1, c.first), c.second});


    for(int i = 1; i < caractere.size(); ++i){
        nod z, x, y;
        x = Q.top();
        Q.pop();
        y = Q.top();
        Q.pop();
        z.text = x.text+y.text;
        z.frecv = x.frecv+y.frecv;
        Q.push(z);
        for(const auto& c: x.text)
            codare[c] = '0'+codare[c];
        for(const auto& c: y.text)
            codare[c] = '1'+codare[c];
    }
}

string decodare(const map<char, string>& codare, string sir){
    string text;
    map<string, char> decodare;
    for(const auto& p: codare){
        string path = p.second;
        char c = p.first;
        decodare[path] = c;
    }
    int st = 0, dr = 0;
    while(st < sir.size()){
        dr++;
        string substr = sir.substr(st, dr);
        if(decodare.find(substr) != decodare.end()){
            text += decodare[substr];
            st += dr;
            dr = 0;
        }
    }
    return text;
}

int main(int argc, char* argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex4/in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex4/out.txt");

    //CITIRE
    int nr_litere;
    map<char, int> caractere;
    fin >> nr_litere;
    for(int i = 0; i < nr_litere; ++i) {
        char car;
        int frecv;
        fin.get();
        fin.get(car);
        fin >> frecv;
        caractere[car] = frecv;
    }
    string sir;
    fin >> sir;

    map<char, string> codare;
    Huffman(caractere, codare);

    // AFISARE
    fout << decodare(codare, sir);

    fin.close();
    fout.close();
    return 0;
}