#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cmath>
#include <string>
#include <iomanip>
#include <omp.h>

using namespace std;
using namespace std::chrono;

typedef double matrix_t;

bool readMatrixSequential(const string& filename, matrix_t* mat, uint32_t M) {
    ifstream in(filename, ios::binary);
    if (!in) return false;
    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    in.read(reinterpret_cast<char*>(mat), total_elements * sizeof(matrix_t));
    return in.good();
}

bool writeMatrixSequential(const string& filename, const matrix_t* mat, uint32_t M) {
    ofstream out(filename, ios::binary);
    if (!out) return false;
    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    out.write(reinterpret_cast<const char*>(mat), total_elements * sizeof(matrix_t));
    return out.good();
}

// --- PARALLEL READING (OpenMP) ---
void readChunk(const string& filename, matrix_t* mat, uint64_t start_el, uint64_t count) {
    ifstream in(filename, ios::binary);
    if (!in) return;
    in.seekg(start_el * sizeof(matrix_t));
    in.read(reinterpret_cast<char*>(mat + start_el), count * sizeof(matrix_t));
}

bool readMatrixParallel(const string& filename, matrix_t* mat, uint32_t M, int numThreads) {
#pragma omp parallel num_threads(numThreads)
    {
        int tid = omp_get_thread_num();
        int n_threads = omp_get_num_threads();

        uint32_t rows_per_thread = M / n_threads;
        uint32_t remainder = M % n_threads;

        uint32_t start_row = tid * rows_per_thread + min(static_cast<uint32_t>(tid), remainder);
        uint32_t end_row = start_row + rows_per_thread + (tid < remainder ? 1 : 0);

        uint64_t start_el = static_cast<uint64_t>(start_row) * M;
        uint64_t count = static_cast<uint64_t>(end_row - start_row) * M;

        if (count > 0) {
            readChunk(filename, mat, start_el, count);
        }
    }
    return true;
}

// --- PARALLEL MULTIPLICATION USING ROW PARTITIONING ---

void multiplyMatricesParallelRow(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];

    // 1. Transpose B using Row Partitioning
    #pragma omp parallel for num_threads(numThreads) schedule(static, 1) // CYCLING
    // #pragma omp parallel for num_threads(numThreads) schedule(static) // BLOCK
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            BT[j * M + i] = B[i * M + j];
        }
    }

    // 2. Parallel Multiplication using Row Partitioning
    #pragma omp parallel for num_threads(numThreads) schedule(static, 1) // CYCLING
    // #pragma omp parallel for num_threads(numThreads) schedule(static) // BLOCK
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }
    delete[] BT;
}

// --- PARALLEL MULTIPLICATION USING 2D PARTITIONING ---

void getGridDimensions(int numThreads, int& rows, int& cols) {
    rows = static_cast<int>(sqrt(numThreads));
    while (numThreads % rows != 0) rows--;
    cols = numThreads / rows;
}

void multiplyMatricesParallel2DManual(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    int p_rows, p_cols;
    getGridDimensions(numThreads, p_rows, p_cols);

    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];

    #pragma omp parallel num_threads(numThreads)
    {
        int tid = omp_get_thread_num();
        int r = tid / p_cols;
        int c = tid % p_cols;

        if (r < p_rows) {
            uint32_t rows_per_block = M / p_rows;
            uint32_t row_remainder = M % p_rows;
            uint32_t cols_per_block = M / p_cols;
            uint32_t col_remainder = M % p_cols;

            uint32_t r_start = r * rows_per_block + min(static_cast<uint32_t>(r), row_remainder);
            uint32_t r_end = r_start + rows_per_block + (r < row_remainder ? 1 : 0);

            uint32_t c_start = c * cols_per_block + min(static_cast<uint32_t>(c), col_remainder);
            uint32_t c_end = c_start + cols_per_block + (c < col_remainder ? 1 : 0);

            // 1. Transpose B using 2D Partitioning
            for (uint32_t i = r_start; i < r_end; ++i) {
                for (uint32_t j = c_start; j < c_end; ++j) {
                    BT[j * M + i] = B[i * M + j];
                }
            }

            #pragma omp barrier // Asteptam ca toate thread-urile sa termine transpunerea

            // 2. Parallel Multiplication using 2D Partitioning
            for (uint32_t i = r_start; i < r_end; ++i) {
                for (uint32_t j = c_start; j < c_end; ++j) {
                    matrix_t sum = 0;
                    for (uint32_t k = 0; k < M; ++k) {
                        sum += A[i * M + k] * BT[j * M + k];
                    }
                    C[i * M + j] = sum;
                }
            }
        }
    }
    delete[] BT;
}

void multiplyMatricesParallel2DOMP(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];

    // 1. Transpose B using 2D Partitioning
    #pragma omp parallel for collapse(2) num_threads(numThreads) schedule(static)
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            BT[j * M + i] = B[i * M + j];
        }
    }

    // implicit pragma omp barrier

    // 2. Parallel Multiplication using 2D Partitioning
    #pragma omp parallel for collapse(2) num_threads(numThreads) schedule(static)
    for (uint32_t i = 0; i < M; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }

    delete[] BT;
}

int main(int argc, char* argv[]) {
    if (argc < 6) {
        cout << "Usage: " << argv[0] << " <M> <FileA> <FileB> <FileC> <Threads>" << endl;
        return 1;
    }

    uint32_t M = stoul(argv[1]);
    string fileA = argv[2], fileB = argv[3], fileC = argv[4];
    int numThreads = stoi(argv[5]);

    uint64_t total_elements = static_cast<uint64_t>(M) * M;
    auto *A = new matrix_t[total_elements];
    auto *B = new matrix_t[total_elements];
    auto *C = new matrix_t[total_elements];

    // --- READING ---
    auto s1 = high_resolution_clock::now();

    readMatrixSequential(fileA, A, M); readMatrixSequential(fileB, B, M); // Requirement 3a
    // readMatrixParallel(fileA, A, M, numThreads); readMatrixParallel(fileB, B, M, numThreads); // Requirement 3b

    auto e1 = high_resolution_clock::now();

    // --- MULTIPLICATION ---
    auto s2 = high_resolution_clock::now();
    multiplyMatricesParallelRow(A, B, C, M, numThreads);
    // multiplyMatricesParallel2DManual(A, B, C, M, numThreads);
    // multiplyMatricesParallel2DOMP(A, B, C, M, numThreads);
    auto e2 = high_resolution_clock::now();

    // --- WRITING ---
    auto s3 = high_resolution_clock::now();
    writeMatrixSequential(fileC, C, M);
    auto e3 = high_resolution_clock::now();

    // Output times for the script to parse
    cout << "t_read: " << duration<double, std::milli>(e1 - s1).count() << " ms" << endl;
    cout << "t_mult: " << duration<double, std::milli>(e2 - s2).count() << " ms" << endl;
    cout << "t_write: " << duration<double, std::milli>(e3 - s3).count() << " ms" << endl;

    delete[] A; delete[] B; delete[] C;
    return 0;
}
