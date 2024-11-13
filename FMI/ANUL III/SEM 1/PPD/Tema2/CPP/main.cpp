#include <barrier>
#include <cassert>
#include <iostream>
#include <fstream>
#include <thread>
#include <vector>

using namespace std;

void readMatrix(ifstream &fin, int** matrice, int n, int m) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            fin >> matrice[i][j];
        }
    }
}

void writeMatrix(ofstream &fout, int** matrice, int n, int m) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            fout << matrice[i][j] << " ";
        }
        fout << "\n";
    }
}

void task(int** F, int** C, int* linie_anterioara, const int* linie_urmatoare,
    int* linie_modificata, int n, int m, int k, int margine, int start, int end, barrier<>& barrier) {
    barrier.arrive_and_wait();

    for (int i = start; i < end; ++i) {
        for (int j = 0; j < m; ++j) {
            int suma = 0;

            for (int ci = 0; ci < k; ++ci) {
                for (int cj = 0; cj < k; ++cj) {
                    int x = i + ci - margine;
                    int y = j + cj - margine;

                    int valoare = 0;
                    if (x >= 0 && x < n && y >= 0 && y < m) {
                        ci < margine ? valoare = linie_anterioara[y] :
                        x == i && j > 0 && cj < margine ? valoare = F[i][j-1] :
                        i == end-1 && ci > margine ? valoare = linie_urmatoare[y] :
                        valoare = F[x][y];
                    } else {
                        int x_clona = min(max(x, 0), n - 1);
                        int y_clona = min(max(y, 0), m - 1);
                        ci < margine ? valoare = linie_anterioara[y_clona] :
                        j > 0 && cj < margine ? valoare = F[i][j-1] :
                        i == end-1 && ci > margine ? valoare = linie_urmatoare[y_clona] :
                        valoare = F[x_clona][y_clona];
                    }
                    suma += valoare * C[ci][cj];
                }
            }

            linie_modificata[j] = suma;
        }

        for (int j = 0; j < m; ++j) {
            linie_anterioara[j] = F[i][j];
            F[i][j] = linie_modificata[j];
        }
    }

    delete[] linie_anterioara;
    delete[] linie_urmatoare;
    delete[] linie_modificata;
}

int areSame(int** A, int** B, int n, int m)
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (A[i][j] != B[i][j])
                return 0;
    return 1;
}

int main() {
    string defaultPath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema2/";

    int n = 10;
    int m = 10;
    int k = 3;

    int** F = new int*[n];
    for (int i = 0; i < n; ++i) {
        F[i] = new int[m];
    }
    int** C = new int*[k];
    for (int i = 0; i < k; ++i) {
        C[i] = new int[k];
    }

    ifstream fin(defaultPath + "data" + to_string(n) + ".txt");
    ofstream fout(defaultPath + "outputCPP.txt");

    readMatrix(fin, F, n, m);
    readMatrix(fin, C, k, k);

    int* linie_anterioara = new int[m];
    int* linie_modificata = new int[m];

    // 1. PROGRAM SECVENTIAL
    int margine = k / 2;

    // auto startTime = chrono::high_resolution_clock::now();

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            int suma = 0;

            for (int ci = 0; ci < k; ++ci) {
                for (int cj = 0; cj < k; ++cj) {
                    int x = i + ci - margine;
                    int y = j + cj - margine;

                    int valoare = 0;
                    if (x >= 0 && x < n && y >= 0 && y < m) {
                        i > 0 && ci < margine ? valoare = linie_anterioara[y] :
                        x == i && j > 0 && cj < margine ? valoare = F[i][j-1] : valoare = F[x][y];
                    } else {
                        int x_clona = min(max(x, 0), n - 1);
                        int y_clona = min(max(y, 0), m - 1);
                        i > 0 && ci < margine ? valoare = linie_anterioara[y_clona] :
                        j > 0 && cj < margine ? valoare = F[i][j-1] : valoare = F[x_clona][y_clona];
                    }
                    suma += valoare * C[ci][cj];
                }
            }

            linie_modificata[j] = suma;
        }

        for (int j = 0; j < m; ++j) {
            linie_anterioara[j] = F[i][j];
            F[i][j] = linie_modificata[j];
        }
    }

    // auto endTime = chrono::high_resolution_clock::now();

    writeMatrix(fout, F, n, m);

    delete[] linie_anterioara;
    delete[] linie_modificata;

    for (int i = 0; i < n; ++i) {
        delete[] F[i];
    }
    delete[] F;

    for (int i = 0; i < k; ++i) {
        delete[] C[i];
    }
    delete[] C;

    fin.close();
    fout.close();

    // 2. PROGRAM PARALEL
    int** R = new int*[n];
    for (int i = 0; i < n; ++i) {
        R[i] = new int[m];
    }
    F = new int*[n];
    for (int i = 0; i < n; ++i) {
        F[i] = new int[m];
    }
    C = new int*[k];
    for (int i = 0; i < k; ++i) {
        C[i] = new int[k];
    }

    ifstream finParallel(defaultPath + "data" + to_string(n) + ".txt");
    ifstream finRes(defaultPath + "outputCPP.txt");

    readMatrix(finParallel, F, n, m);
    readMatrix(finParallel, C, k, k);
    readMatrix(finRes, R, n, m);

    ofstream foutParallel(defaultPath + "outputCPP.txt");

    int p = 2;
    int startRow = 0;
    int endRow = n / p;
    int remainingRows = n % p;
    vector<thread> threads(p);
    barrier barrier{p};

    auto startTime = chrono::high_resolution_clock::now();

    for (int i = 0; i < p; ++i) {
        if (remainingRows > 0) {
            endRow++;
            remainingRows--;
        }

        // pregatire threads
        linie_anterioara = new int[m];
        linie_modificata = new int[m];
        int* linie_urmatoare = new int[m];

        for (int j = 0; j < m; ++j) {
            startRow > 0 ? linie_anterioara[j] = F[startRow - 1][j] : linie_anterioara[j] = F[startRow][j];
            endRow < n ? linie_urmatoare[j] = F[endRow][j] : linie_urmatoare[j] = F[endRow - 1][j];
        }

        // initializare threads
        threads[i] = thread(task, F, C, linie_anterioara, linie_urmatoare,
            linie_modificata, n, m, k, margine, startRow, endRow, ref(barrier));

        startRow = endRow;
        endRow += n/p;
    }

    for (int i = 0; i < p; ++i) {
        threads[i].join();
    }

    auto endTime = chrono::high_resolution_clock::now();
    double elapsed_time_ms = chrono::duration<double, std::milli>(endTime-startTime).count();

    assert(areSame(F, R, n, m));
    writeMatrix(foutParallel, F, n, m);
    cout << elapsed_time_ms;

    for (int i = 0; i < n; ++i) {
        delete[] F[i];
    }
    delete[] F;

    for (int i = 0; i < k; ++i) {
        delete[] C[i];
    }
    delete[] C;

    for (int i = 0; i < n; ++i) {
        delete[] R[i];
    }
    delete[] R;

    finParallel.close();
    finRes.close();
    foutParallel.close();

    return 0;
}
