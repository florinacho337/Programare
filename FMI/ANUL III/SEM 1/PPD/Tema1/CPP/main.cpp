#include <assert.h>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>

using namespace std;

constexpr int n = 10;
constexpr int m = 10;
constexpr int k = 3;
int offset = k/2;
int matrix[n+k-1][m+k-1];
int kernel[k][k];
int result[n][m];
int resultParallel[n][m];
int nrThreads = 4;
string path = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema1/";

void borderValues(int** dynamicMatrix = nullptr) {
    // Fill left and right borders
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < offset; j++) {
            dynamicMatrix ? dynamicMatrix[i][j] = dynamicMatrix[i][offset] : matrix[i][j] = matrix[i][offset];
            dynamicMatrix ? dynamicMatrix[i][m + offset + j] = dynamicMatrix[i][m + offset - 1] : matrix[i][m + offset + j] = matrix[i][m + offset - 1];
        }
    }
    // Fill top and bottom borders
    for (int j = 0; j < m + 2 * offset; j++) {
        for (int i = 0; i < offset; i++) {
            dynamicMatrix ? dynamicMatrix[i][j] = dynamicMatrix[offset][j] : matrix[i][j] = matrix[offset][j];
            dynamicMatrix ? dynamicMatrix[n + offset + i][j] = dynamicMatrix[n + offset - 1][j] : matrix[n + offset + i][j] = matrix[n + offset - 1][j];
        }
    }
}

void task(int start, int end, char decomposition, int** dynamicMatrix = nullptr, int** dynamicKernel = nullptr, int** dynamicResult = nullptr) {
    for (int i = start; i <= end; i++) {
            for (int j = offset; j <= m + offset - 1; j++) {
                int sum = 0;
                for (int ki = 0; ki < k; ki++) {
                    for (int kj = 0; kj < k; kj++) {
                        if (decomposition == 'h') {
                            dynamicMatrix ? sum += dynamicMatrix[i + ki - offset][j + kj - offset] * dynamicKernel[ki][kj]
                            : sum += matrix[i + ki - offset][j + kj - offset] * kernel[ki][kj];
                        } else {
                            dynamicMatrix ? sum += dynamicMatrix[j + ki - offset][i + kj - offset] * dynamicKernel[ki][kj]
                            : sum += matrix[j + ki - offset][i + kj - offset] * kernel[ki][kj];
                        }
                    }
                }
                if (decomposition == 'h') {
                    dynamicResult ? dynamicResult[i - offset][j - offset] = sum : resultParallel[i - offset][j - offset] = sum;
                } else {
                    dynamicResult ? dynamicResult[j - offset][i - offset] = sum : resultParallel[j - offset][i - offset] = sum;
                }
            }
        }
}

void taskBlock(int startRow, int endRow, int startCol, int endCol, int** dynamicMatrix = nullptr, int** dynamicKernel = nullptr, int** dynamicResult = nullptr) {
    for (int i = startRow; i <= endRow; i++) {
        for (int j = startCol; j <= endCol; j++) {
            int sum = 0;
            for (int ki = 0; ki < k; ki++) {
                for (int kj = 0; kj < k; kj++) {
                    dynamicMatrix ? sum += dynamicMatrix[i + ki - offset][j + kj - offset] * dynamicKernel[ki][kj]
                    : sum += matrix[i + ki - offset][j + kj - offset] * kernel[ki][kj];
                }
            }
            dynamicResult ? dynamicResult[i - offset][j - offset] = sum : result[i - offset][j - offset] = sum;
        }
    }
}

void readData(int** dynamicMatrix = nullptr, int** dynamicKernel = nullptr) {
    ifstream fin(path + "data" + to_string(n) + ".txt");
    for (int i = offset; i <= n + offset - 1; i++) {
        for (int j = offset; j <= m + offset - 1; j++) {
            dynamicMatrix ? fin >> dynamicMatrix[i][j] : fin >> matrix[i][j];
        }
    }

    for (int i = 0; i < k; i++) {
        for (int j = 0; j < k; j++) {
            dynamicKernel ? fin >> dynamicKernel[i][j] : fin >> kernel[i][j];
        }
    }
    fin.close();
}

void writeMatrix(const string &program, int** dynamicResult = nullptr) {
    ofstream fout(path + "outputCPP.txt");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (program == "s") fout << resultParallel[i][j] << ' ';
            else if (program == "d" && dynamicResult) fout << dynamicResult[i][j] << ' ';
        }
        fout << endl;
    }
    fout.close();
}

int areSame(int A[][n], int B[][n])
{
    int i, j;
    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++)
            if (A[i][j] != B[i][j])
                return 0;
    return 1;
}

int areSame(int** A, int B[][n])
{
    int i, j;
    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++)
            if (A[i][j] != B[i][j])
                return 0;
    return 1;
}

int main() {
    // Dynamic initialization
    // int** dynamicMatrix = nullptr;
    // int** dynamicKernel = nullptr;
    // int** dynamicResult = nullptr;
    // dynamicMatrix = new int*[n+k-1];
    // for (int i = 0; i < n+k-1; i++)
    //     dynamicMatrix[i] = new int[m+k-1];
    //
    // dynamicKernel = new int*[k];
    // for (int i = 0; i < k; i++)
    //     dynamicKernel[i] = new int[k];
    //
    // dynamicResult = new int*[n];
    // for (int i = 0; i < n; i++)
    //     dynamicResult[i] = new int[m];
    // readData(dynamicMatrix, dynamicKernel);

    readData();
    borderValues();
    // borderValues(dynamicMatrix);

    // 1. SEQUENTIAL PROGRAM
    for (int i = offset; i <= n + offset - 1; i++) {
        for (int j = offset; j <= m + offset - 1; j++) {
            int sum = 0;
            for (int ki = 0; ki < k; ki++) {
                for (int kj = 0; kj < k; kj++) {
                    sum += matrix[i + ki - offset][j + kj - offset] * kernel[ki][kj];
                }
            }
            result[i - offset][j - offset] = sum;
        }
    }

    // 2. PARALLEL PROGRAM
    vector<thread> threads(nrThreads);

    // 2.1. Split the matrix horizontally
    int rowsPerThread = n / nrThreads;
    int remainingRows = n % nrThreads;
    int startRow = offset;
    int endRow = rowsPerThread + offset - 1;

    auto startTime = chrono::high_resolution_clock::now();

    for (int i = 0; i < nrThreads; i++) {
        if (remainingRows > 0) {
            remainingRows--;
            endRow++;
        }
        // threads[i] = thread(task, startRow, endRow, 'h', ref(dynamicMatrix), ref(dynamicKernel), ref(dynamicResult));
        threads[i] = thread(task, startRow, endRow, 'h', nullptr, nullptr, nullptr);

        startRow = endRow + 1;
        endRow += rowsPerThread;
    }

    for (int i = 0; i < nrThreads; i++) {
        threads[i].join();
    }
    //
    // // 2.2. Split the matrix vertically
    // int colsPerThread = m / nrThreads;
    // int remainingCols = m % nrThreads;
    // int startCol = offset;
    // int endCol = colsPerThread + offset - 1;
    //
    // auto startTime = chrono::high_resolution_clock::now();
    //
    // for (int i = 0; i < nrThreads; i++) {
    //     if (remainingCols > 0) {
    //         remainingCols--;
    //         endCol++;
    //     }
    //     // threads[i] = thread(task, startCol, endCol, 'v', nullptr, nullptr, nullptr);
    //     threads[i] = thread(task, startCol, endCol, 'v', ref(dynamicMatrix), ref(dynamicKernel), ref(dynamicResult));
    //
    //     startCol = endCol + 1;
    //     endCol += colsPerThread;
    // }
    //
    // for (int i = 0; i < nrThreads; i++) {
    //     threads[i].join();
    // }

    // 2.3 Split the matrix in blocks
    // int rowsPerThread = n / nrThreads;
    // int colsPerThread = m / nrThreads;
    // int remainingRows = n % nrThreads;
    // int remainingCols = m % nrThreads;
    // int startRow = offset;
    // int startCol = offset;
    // int endRow = offset + rowsPerThread - 1;
    // int endCol = offset + colsPerThread - 1;
    //
    // for (int i = 0; i < nrThreads; i++) {
    //
    // }

    auto endTime = chrono::high_resolution_clock::now();
    double elapsed_time_ms = chrono::duration<double, std::milli>(endTime-startTime).count();

    assert(areSame(result, resultParallel) == 1);
    // assert(areSame(dynamicResult, result) == 1);
    cout << elapsed_time_ms;
    writeMatrix("s");
    // deallocate memory
    // for (int i = 0; i < n+k-1; i++)
    //     delete[] dynamicMatrix[i];
    // delete[] dynamicMatrix;
    //
    // for(int i = 0; i < k; i++)
    //     delete[] dynamicKernel[i];
    // delete[] dynamicKernel;
    //
    // for (int i = 0; i < n; i++)
    //     delete[] dynamicResult[i];
    // delete[] dynamicResult;
    return 0;
}
