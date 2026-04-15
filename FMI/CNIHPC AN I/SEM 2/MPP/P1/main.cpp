#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <numeric>
#include <iomanip>
#include <cmath>

using namespace std;
using namespace std::chrono;

typedef double matrix_t;
const int NR_EXECUTIONS = 10;

bool readMatrixBinary(const string& filename, matrix_t* mat, uint32_t M) {
    ifstream in(filename, ios::binary);
    if (!in) return false;

    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    in.read(reinterpret_cast<char*>(mat), total_elements * sizeof(matrix_t));

    bool success = in.good();
    in.close();
    return success;
}

bool writeMatrixBinary(const string& filename, const matrix_t* mat, uint32_t M) {
    ofstream out(filename, ios::binary);
    if (!out) return false;

    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    out.write(reinterpret_cast<const char*>(mat), total_elements * sizeof(matrix_t));

    bool success = out.good();
    out.close();
    return success;
}

void multiplyMatrices(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M) {
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                // Flat array indexing: row * width + column
                sum += A[i * M + k] * B[k * M + j];
            }
            C[i * M + j] = sum;
        }
    }
}

void multiplyMatricesOptimized(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M) {
    // 1. Create a temporary transposed copy of B
    matrix_t* BT = new matrix_t[M * M];
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            BT[i * M + j] = B[j * M + i]; // BT row i is B column i
        }
    }

    // 2. Multiply A row by BT row (which is B column)
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                // Now both A and BT are accessed linearly!
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }
    delete[] BT;
}

bool verifyResult(const matrix_t* A, const matrix_t* B, const matrix_t* C, uint32_t M) {
    uint32_t row = M / 2;
    uint32_t col = M / 2;
    matrix_t expected = 0;

    for (uint32_t k = 0; k < M; ++k) {
        expected += A[row * M + k] * B[k * M + col];
    }

    return std::abs(C[row * M + col] - expected) < 1e-9;
}

int main(int argc, char* argv[]) {
    if (argc < 5) {
        cout << "Usage: " << argv[0] << " <M> <FileA> <FileB> <FileC>" << endl;
        return 1;
    }

    uint32_t M = stoul(argv[1]);
    string fileA = argv[2], fileB = argv[3], fileC = argv[4];

    vector<double> t_readings, t_multiplications, t_writings;

    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    matrix_t *A = new (nothrow) matrix_t[total_elements];
    matrix_t *B = new (nothrow) matrix_t[total_elements];
    matrix_t *C = new (nothrow) matrix_t[total_elements];

    if (!A || !B || !C) {
        cerr << "Critical Error: Failed to allocate memory for M=" << M << endl;
        return 1;
    }

    cout << "--- Starting benchmark for M=" << M << " (" << NR_EXECUTIONS << " iterations) ---" << endl;

    for (int run = 0; run < NR_EXECUTIONS; ++run) {
        // 1. Reading
        auto start_r = high_resolution_clock::now();
        if (!readMatrixBinary(fileA, A, M) || !readMatrixBinary(fileB, B, M)) {
            cerr << "Error reading input files!" << endl;
            break;
        }
        auto end_r = high_resolution_clock::now();

        // 2. Multiplication
        auto start_m = high_resolution_clock::now();
        multiplyMatricesOptimized(A, B, C, M);
        auto end_m = high_resolution_clock::now();

        // 3. Writing
        auto start_w = high_resolution_clock::now();
        if (!writeMatrixBinary(fileC, C, M)) {
            cerr << "Error writing output file!" << endl;
            break;
        }
        auto end_w = high_resolution_clock::now();

        // Calculate run metrics
        double tr = duration<double, std::milli>(end_r - start_r).count();
        double tm = duration<double, std::milli>(end_m - start_m).count();
        double tw = duration<double, std::milli>(end_w - start_w).count();

        t_readings.push_back(tr);
        t_multiplications.push_back(tm);
        t_writings.push_back(tw);

        cout << fixed << setprecision(3) << "Run " << (run + 1)
             << " | Read: " << tr << "ms | Mult: " << tm << "ms | Write: " << tw << "ms" << endl;
    }

    // Performance Summary
    bool is_correct = verifyResult(A, B, C, M);
    auto get_avg = [](const vector<double>& v) {
        return v.empty() ? 0.0 : accumulate(v.begin(), v.end(), 0.0) / v.size();
    };

    cout << "\n" << string(50, '=') << "\n";
    cout << "PERFORMANCE SUMMARY (Averages in ms)\n";
    cout << "Verification: " << (is_correct ? "SUCCESS (Sample match)" : "FAILURE") << "\n";
    cout << fixed << setprecision(3);
    cout << "Avg Reading Time:    " << get_avg(t_readings) << " ms\n";
    cout << "Avg Multiplication:  " << get_avg(t_multiplications) << " ms\n";
    cout << "Avg Writing Time:    " << get_avg(t_writings) << " ms\n";
    cout << "Total Avg Execution: " << (get_avg(t_readings) + get_avg(t_multiplications) + get_avg(t_writings)) << " ms\n";
    cout << string(50, '=') << endl;

    delete[] A; delete[] B; delete[] C;
    return 0;
}