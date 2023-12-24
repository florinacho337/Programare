//EXERCITIUL 1 - ALGORITMUL LUI MOORE
#include <iostream>
#include <fstream>
#include <queue>
#include <vector>

using namespace std;
ifstream fin("/home/florin/FMI/SEM2/Algoritmica Grafelor/Laborator/Lab2/ex1/graf1.txt");

typedef struct l_p{
    vector<int> l; // l = vectorul lungimilor, p = vectorul parintilor
    vector<int> p;
}LP;

LP Moore(vector<queue<int>> Graf, int varf, int n){
    LP lp;
    lp.l.assign(n+1, n); // se initializeaza vectorul de lungimi, in acest caz, infinit va fi
                                // numarul de noduri, deoarece intr-un graf neorientat nu exista un drum
                                // care va avea lungimea mai mare decat numarul de noduri - 1
    lp.p.assign(n+1, 0); // se initializeaza vectorul de parinti
    lp.l[varf] = 0; // lungimea drumului varfului sursa se va intializa cu 0
    queue<int> Queue; // se formeaza o coada
    Queue.push(varf); //se introduce in coada varful transmis ca parametru
    while(!Queue.empty()){
        int x = Queue.front(); //se scoate din coada varful salvat anterior
        Queue.pop();
        while(!Graf[x].empty()) {
            int y = Graf[x].front(); // y - vecin al lui x
            Graf[x].pop();
            //se itereaza vecinii varfului x
            if (lp.l[y] == n) {
                lp.p[y] = x; // parintele varfului y va fi x
                lp.l[y] = lp.l[x] + 1; // lungimea de la varful sursa pana la y va fi lungimea pana la x + 1
                Queue.push(y);// se adauga in coada pe y, apoi se reia procesul
            }
        }
    }
    return lp; // se returneaza perechea de vectori lungimi, parinti
}

vector<int> MooreDrum(LP lp, int sursa){
    int k = lp.l[sursa]; // k = lungimea de la varful determinat in algoritmul lui Moore la varful sursa
    vector<int> drum(k+1, 0);
    drum[k] = sursa; // ultimul element din vectorul drum va fi nodul sursa
    while(k != 0){
        drum[k-1] = lp.p[drum[k]]; // urmatoarele elemente, de la final spre inceput, sunt nodurile parinte ale nodurilor curent interate
        k--;
    }
    return drum;
}

int main() {
    int nr_v;
    fin >> nr_v;
    vector<queue<int>> listaDeAdiacenta(nr_v+1);
    while(!fin.eof()){
        int x, y;
        fin >> x >> y;
        listaDeAdiacenta[x].push(y); // se adauga vecinii
        listaDeAdiacenta[y].push(x);
    }
    int sursa;
    cout << "Introduceti varful sursa: ";
    cin >> sursa;
    LP moore = Moore(listaDeAdiacenta, sursa, nr_v);
    for(int i = 1; i <= nr_v; ++i) {
        vector<int> drum = MooreDrum(moore, i);
        cout << "Cel mai scurt lant din sursa la nodul " << i << " este: ";
        if(drum.size() == nr_v+1)
            cout << "inf";
        else {
            for (int j = 0; j <= moore.l[i]; ++j)
                cout << drum[j] << " ";
        }
        cout << "\n";
    }
    return 0;
}
