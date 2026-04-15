#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cmath>
#include <string>
#include <iomanip>
#include <thread>

using namespace std;
using namespace std::chrono;

typedef double matrix_t;

struct Block {
    uint32_t row_start, row_end;
    uint32_t col_start, col_end;
};

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

// --- PARALLEL READING ---

void readChunk(const string& filename, matrix_t* mat, uint64_t start_el, uint64_t count) {
    ifstream in(filename, ios::binary);
    if (!in) return;
    in.seekg(start_el * sizeof(matrix_t));
    in.read(reinterpret_cast<char*>(mat + start_el), count * sizeof(matrix_t));
}

bool readMatrixParallel(const string& filename, matrix_t* mat, uint32_t M, int numThreads) {
    uint32_t rows_per_thread = M / numThreads;
    uint32_t remainder = M % numThreads;
    vector<thread> threads;
    uint32_t start_row = 0;

    for (int i = 0; i < numThreads; ++i) {
        uint32_t end_row = start_row + rows_per_thread + (i < remainder ? 1 : 0);

        uint64_t start_el = static_cast<uint64_t>(start_row) * M;
        uint64_t count = static_cast<uint64_t>(end_row - start_row) * M;

        threads.emplace_back(readChunk, filename, mat, start_el, count);
        start_row = end_row;
    }

    for (auto& t : threads) t.join();
    return true;
}

// --- PARALLEL MULTIPLICATION USING ROW PARTITIONING (CYCLING) ---

void multiplyRowsCycling(const matrix_t* A, const matrix_t* BT, matrix_t* C, const uint32_t M, const int tid, const int numThreads) {
    for (uint32_t i = tid; i < M; i += numThreads) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }
}

void transposeChunkCycling(const matrix_t* B, matrix_t* BT, const uint32_t M, const int tid, const int numThreads) {
    for (uint32_t i = tid; i < M; i += numThreads) {
        for (uint32_t j = 0; j < M; ++j) {
            BT[j * M + i] = B[i * M + j];
        }
    }
}

void transposeParallelCycling(const matrix_t* B, matrix_t* BT, uint32_t M, int numThreads) {
    vector<thread> threads;
    threads.reserve(numThreads);

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(transposeChunkCycling, B, BT, M, i, numThreads);
    }
    for (auto& t : threads) t.join();
}

void multiplyMatricesParallelRowCycling(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];
    
    // 1. Transpose B using Row Partitioning
    transposeParallelCycling(B, BT, M, numThreads);

    // 2. Parallel Multiplication using Row Partitioning
    vector<thread> threads;
    threads.reserve(numThreads);

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(multiplyRowsCycling, A, BT, C, M, i, numThreads);
    }

    for (auto& t : threads) t.join();
    delete[] BT;
}


// --- PARALLEL MULTIPLICATION USING ROW PARTITIONING (BLOCK) ---

void multiplyRowsBlock(const matrix_t* A, const matrix_t* BT, matrix_t* C, uint32_t M, uint32_t start_row, uint32_t end_row) {
    for (uint32_t i = start_row; i < end_row; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                // Optimized linear access on both A and BT
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }
}

void transposeChunkBlock(const matrix_t* B, matrix_t* BT, uint32_t M, uint32_t start_row, uint32_t end_row) {
    for (uint32_t i = start_row; i < end_row; ++i) {
        for (uint32_t j = 0; j < M; ++j) {
            // Read from B is linear, write to BT is strided
            BT[j * M + i] = B[i * M + j];
        }
    }
}

void transposeParallelBlock(const matrix_t* B, matrix_t* BT, uint32_t M, int numThreads, uint32_t rows_per_thread, uint32_t remainder) {
    vector<thread> threads;
    threads.reserve(numThreads);
    uint32_t start = 0;

    for (int i = 0; i < numThreads; ++i) {
        uint32_t end = start + rows_per_thread + (i < remainder ? 1 : 0);
        threads.emplace_back(transposeChunkBlock, B, BT, M, start, end);
        start = end;
    }
    for (auto& t : threads) t.join();
}

void multiplyMatricesParallelRowBlock(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    uint32_t rows_per_thread = M / numThreads;
    uint32_t remainder = M % numThreads;

    // 1. Transpose B using Row Partitioning
    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];
    transposeParallelBlock(B, BT, M, numThreads, rows_per_thread, remainder);

    // 2. Parallel Multiplication using Row Partitioning
    vector<thread> threads;
    threads.reserve(numThreads);
    uint32_t start = 0;

    for (int i = 0; i < numThreads; ++i) {
        uint32_t end = start + rows_per_thread + (i < remainder ? 1 : 0);
        threads.emplace_back(multiplyRowsBlock, A, BT, C, M, start, end);
        start = end;
    }
    for (auto& t : threads) t.join();

    delete[] BT;
}

// --- PARALLEL MULTIPLICATION USING 2D PARTITIONING ---

void multiplyBlock2D(const matrix_t* A, const matrix_t* BT, matrix_t* C, uint32_t M, Block b) {
    for (uint32_t i = b.row_start; i < b.row_end; ++i) {
        for (uint32_t j = b.col_start; j < b.col_end; ++j) {
            matrix_t sum = 0;
            for (uint32_t k = 0; k < M; ++k) {
                sum += A[i * M + k] * BT[j * M + k];
            }
            C[i * M + j] = sum;
        }
    }
}

void transposeBlock2D(const matrix_t* B, matrix_t* BT, uint32_t M, Block b) {
    for (uint32_t i = b.row_start; i < b.row_end; ++i) {
        for (uint32_t j = b.col_start; j < b.col_end; ++j) {
            BT[j * M + i] = B[i * M + j];
        }
    }
}

void getGridDimensions(int numThreads, int& rows, int& cols) {
    rows = (int)sqrt(numThreads);
    while (numThreads % rows != 0) {
        rows--;
    }
    cols = numThreads / rows;
}

void transposeParallel2D(const matrix_t* B, matrix_t* BT, uint32_t M, int numThreads, int p_rows, int p_cols,
    uint32_t rows_per_block, uint32_t row_remainder, uint32_t cols_per_block, uint32_t col_remainder) {
    vector<thread> threads;
    threads.reserve(numThreads);

    uint32_t current_row_start = 0;
    for (int r = 0; r < p_rows; ++r) {
        uint32_t r_count = rows_per_block + (r < row_remainder ? 1 : 0);
        uint32_t current_col_start = 0;

        for (int c = 0; c < p_cols; ++c) {
            uint32_t c_count = cols_per_block + (c < col_remainder ? 1 : 0);

            Block b = {
                current_row_start, current_row_start + r_count,
                current_col_start, current_col_start + c_count
            };

            // Verificăm să nu lansăm thread-uri goale
            if (r_count > 0 && c_count > 0) {
                threads.emplace_back(transposeBlock2D, B, BT, M, b);
            }

            current_col_start += c_count;
        }
        current_row_start += r_count;
    }

    for (auto& t : threads) t.join();
}

void multiplyMatricesParallel2D(const matrix_t* A, const matrix_t* B, matrix_t* C, uint32_t M, int numThreads) {
    int p_rows, p_cols;
    getGridDimensions(numThreads, p_rows, p_cols);
    
    auto* BT = new matrix_t[static_cast<uint64_t>(M) * M];

    uint32_t rows_per_block = M / p_rows;
    uint32_t row_remainder = M % p_rows;
    uint32_t cols_per_block = M / p_cols;
    uint32_t col_remainder = M % p_cols;

    // 1. Transpose B using 2D Partitioning
    transposeParallel2D(B, BT, M, numThreads, p_rows, p_cols, rows_per_block, row_remainder, cols_per_block, col_remainder);

    // 2. Parallel Multiplication using 2D Partitioning
    vector<thread> threads;
    uint32_t current_row_start = 0;

    for (int r = 0; r < p_rows; ++r) {
        uint32_t r_count = rows_per_block + (r < row_remainder ? 1 : 0);
        uint32_t current_col_start = 0;

        for (int c = 0; c < p_cols; ++c) {
            uint32_t c_count = cols_per_block + (c < col_remainder ? 1 : 0);

            Block b = {
                current_row_start, current_row_start + r_count,
                current_col_start, current_col_start + c_count
            };

            threads.emplace_back(multiplyBlock2D, A, BT, C, M, b);

            current_col_start += c_count;
        }
        current_row_start += r_count;
    }

    for (auto& t : threads) t.join();
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

    readMatrixSequential(fileA, A, M); readMatrixSequential(fileB, B, M); // Requirement 2a
    //readMatrixParallel(fileA, A, M, numThreads); readMatrixParallel(fileB, B, M, numThreads); // Requirement 2b

    auto e1 = high_resolution_clock::now();

    // --- MULTIPLICATION ---
    auto s2 = high_resolution_clock::now();
    //multiplyMatricesParallelRowCycling(A, B, C, M, numThreads);
    //multiplyMatricesParallelRowBlock(A, B, C, M, numThreads);
    multiplyMatricesParallel2D(A, B, C, M, numThreads);
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
