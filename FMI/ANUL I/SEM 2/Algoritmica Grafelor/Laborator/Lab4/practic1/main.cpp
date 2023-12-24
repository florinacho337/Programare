#include <iostream>
#include <vector>
//lista de adiacenta, cate noduri izolate sunt?

using namespace std;

int main() {
    int n;
    cout << "Introduceti numarul de noduri:\n";
    cin >> n;
    vector<vector<int>> listaAdiacenta(n);
    cout << "Introduceti muchiile:(la -1 -1 executia se opreste)\n";
    int x, y;
    cin >> x >> y;
    while(x != -1 && y != -1) { //cand se introduce -1, -1 executia se termina
        listaAdiacenta[x].push_back(y);
        listaAdiacenta[y].push_back(x);
        cin >> x >> y;
    }
    int cnt = 0;
    for(int i = 0; i < n; ++i)
        if(listaAdiacenta[i].empty())
            cnt++;
    cout << "Numarul de noduri izolate este " << cnt << ".";
    return 0;
}
