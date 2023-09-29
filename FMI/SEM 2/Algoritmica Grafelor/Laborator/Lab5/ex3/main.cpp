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
        cout << x.text << " " << y.text << " " << z.text << "\n";
        for(const auto& c: x.text)
            codare[c] = '0'+codare[c];
        for(const auto& c: y.text)
            codare[c] = '1'+codare[c];
    }
}

int main(int argc, char* argv[]) {
//    ifstream fin(argv[1]);
//    ofstream fout(argv[2]);
    ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex3/in.txt");
    ofstream fout("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab5/ex3/out.txt");

    //CITIRE
    string text;
    map<char, int> caractere;
    getline(fin, text);
    for(auto c: text)
        caractere[c]++;

    //AFISARE
    fout << caractere.size() << "\n";
    for(auto c: caractere)
        fout << c.first << " " << c.second << "\n";

    map<char, string> codare;
    Huffman(caractere, codare);

    for(const auto& c: codare)
        cout << c.first << ":" << c.second << "\n";

    for(const auto& c: text) {
        fout << codare[c];
    }

    fin.close();
    fout.close();
    return 0;
}
