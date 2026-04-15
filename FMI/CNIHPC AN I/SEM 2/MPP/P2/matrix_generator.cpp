#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <string>

using namespace std;

const uint32_t M = 1000;

void generateBinaryMatrix(const string& filename, uint32_t size, uint32_t seed) {
    ofstream out(filename, ios::binary);
    
    if (!out) {
        cerr << "Eroare la crearea fisierului: " << filename << endl;
        return;
    }

    mt19937 gen(seed);
    uniform_real_distribution<double> dist(1.0, 100.0);

    vector<double> row(size);

    cout << "Se genereaza fisierul " << filename << " (" << size << "x" << size << ")..." << endl;

    for (uint32_t i = 0; i < size; ++i) {
        for (uint32_t j = 0; j < size; ++j) {
            row[j] = dist(gen);
        }
        out.write(reinterpret_cast<const char*>(row.data()), size * sizeof(double));

        if (size >= 10000 && i % (size / 10) == 0) {
            cout << "Progres: " << (i * 100 / size) << "%" << endl;
        }
    }

    out.close();
    cout << "Finalizat: " << filename << endl;
}

int main() {
    generateBinaryMatrix("matrixA.bin", M, 123);
    generateBinaryMatrix("matrixB.bin", M, 456);

    return 0;
}