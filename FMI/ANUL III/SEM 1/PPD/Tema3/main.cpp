#include <iostream>
#include <fstream>
#include <algorithm>
#include <mpi.h>
#include <cassert>
#include <chrono>

using namespace std;

string absolutePath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema3/";

void genereaza_fisier(int n1, int n2) {
    ofstream fout1(absolutePath + "Numar1-" + to_string(n1) + ".txt"),
    fout2(absolutePath + "Numar2-" + to_string(n2) + ".txt");

    fout1 << n1 << endl;
    fout2 << n2 << endl;
    for (int i = 0; i < n1; i++)
        fout1 << random() % 10 << " ";
    fout1 << endl;

    for (int i = 0; i < n2; i++)
        fout2 << random() % 10 << " ";
    fout2 << endl;

    fout1.close();
    fout2.close();
}

int* citeste_numar(const string &nume_fisier, int &n) {
    ifstream fin(absolutePath + nume_fisier);
    fin >> n;
    int* numar = new int[n];
    for (int i = 0; i < n; ++i) {
        fin >> numar[i];
    }
    fin.close();
    return numar;
}

int* suma_numere_mari(const int* numar1, int n1, const int* numar2, int n2, int &n_rezultat) {
    const int n = max(n1, n2);
    auto* rezultat = new int[n + 1];
    int carry = 0;

    for (int i = 0; i < n; ++i) {
        int cifra1 = (i < n1) ? numar1[i] : 0;
        int cifra2 = (i < n2) ? numar2[i] : 0;
        int suma = cifra1 + cifra2 + carry;
        rezultat[i] = suma % 10;
        carry = suma / 10;
    }

    if (carry) {
        rezultat[n] = carry;
        n_rezultat = n + 1;
    } else {
        n_rezultat = n;
    }

    return rezultat;
}

void scrie_numar(const int* numar, int n, const string &nume_fisier) {
    ofstream fout(absolutePath + nume_fisier);
    fout << n << "\n";
    for (int i = 0; i < n; ++i) {
        fout << numar[i] << " ";
    }
    fout << "\n";
    fout.close();
}

void citeste_si_trimite_cifre(ifstream &fin1, ifstream &fin2, int n1, int n2, int max_size, int size, int carry) {

    int num_cifre_per_proces = max_size / (size - 1);
    int cifre_ramase = max_size % (size - 1);

    int id_proces_curent = 1;
    int cifre_trimise = 0;

    while (cifre_trimise < max_size) {
        int segment_size = num_cifre_per_proces + (id_proces_curent <= cifre_ramase ? 1 : 0);

        int *segment1 = new int[segment_size];
        int *segment2 = new int[segment_size];
        for (int i = 0; i < segment_size; ++i) {
            if (cifre_trimise + i < n1) {
                fin1 >> segment1[i];
            } else {
                segment1[i] = 0;
            }

            if (cifre_trimise + i < n2) {
                fin2 >> segment2[i];
            } else {
                segment2[i] = 0;
            }
        }

        MPI_Send(&segment_size, 1, MPI_INT, id_proces_curent, 2, MPI_COMM_WORLD);
        MPI_Send(segment1, segment_size, MPI_INT, id_proces_curent, 0, MPI_COMM_WORLD);
        MPI_Send(segment2, segment_size, MPI_INT, id_proces_curent, 1, MPI_COMM_WORLD);
        if (id_proces_curent == 1) {
            MPI_Send(&carry, 1, MPI_INT, id_proces_curent, 3, MPI_COMM_WORLD);
        }

        cifre_trimise += segment_size;
        id_proces_curent++;
        delete[] segment1;
        delete[] segment2;
    }
}

bool areSame(const int* numar1, const int* numar2, int n) {
    for (int i = 0; i < n; ++i) {
        if (numar1[i] != numar2[i]) return false;
    }
    return true;
}

//  SECVENTIAL
// int main() {
//      int n1, n2, n_rezultat;
//
//      auto startTime = chrono::high_resolution_clock::now();
//      int* numar1 = citeste_numar("Numar1-16.txt", n1);
//      int* numar2 = citeste_numar("Numar2-16.txt", n2);
//
//      int* rezultat = suma_numere_mari(numar1, n1, numar2, n2, n_rezultat);
//
//      auto endTime = chrono::high_resolution_clock::now();
//      scrie_numar(rezultat, n_rezultat, "Numar3.txt");
//      delete[] numar1;
//      delete[] numar2;
//      delete[] rezultat;
//
//      double elapsed_time_ms = chrono::duration<double, std::milli>(endTime-startTime).count();
//      cout << elapsed_time_ms;
// }

// VARIANTA 1
// int main(int argc, char *argv[]) {
//     MPI_Init(&argc, &argv);
//     int rank, size;
//     MPI_Comm_rank(MPI_COMM_WORLD, &rank);
//     MPI_Comm_size(MPI_COMM_WORLD, &size);
//
//     int *rezultat = nullptr;
//     int max_size = 0;
//     ifstream fin1(absolutePath + "Numar1-16.txt"), fin2(absolutePath + "Numar2-16.txt");
//     int n2 = 0;
//     int n1 = 0;
//     int carry = 0;
//     chrono::time_point<chrono::system_clock> startTime;
//
//     if (rank == 0) {
//         fin1 >> n1;
//         fin2 >> n2;
//         max_size = max(n1, n2);
//
//         rezultat = new int[max_size + 1];
//         fill(rezultat, rezultat + max_size + 1, 0);
//
//         startTime = chrono::high_resolution_clock::now();
//         citeste_si_trimite_cifre(fin1, fin2, n1, n2, max_size, size, carry);
//     }
//
//     if (rank != 0) {
//         MPI_Status status;
//         int segment_size;
//
//         MPI_Recv(&segment_size, 1, MPI_INT, 0, 2, MPI_COMM_WORLD, &status);
//         int *sub_numar1 = new int[segment_size];
//         int *sub_numar2 = new int[segment_size];
//         int *local_sum = new int[segment_size];
//         int local_carry = 0;
//
//         MPI_Recv(sub_numar1, segment_size, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
//         MPI_Recv(sub_numar2, segment_size, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
//
//         for (int i = 0; i < segment_size; ++i) {
//             int suma = sub_numar1[i] + sub_numar2[i] + local_carry;
//             local_sum[i] = suma % 10;
//             local_carry = suma / 10;
//         }
//
//         MPI_Recv(&carry, 1, MPI_INT, rank - 1, 3, MPI_COMM_WORLD, &status);
//
//         if (carry) {
//             local_carry = carry;
//             for (int i = 0; i < segment_size; ++i) {
//                 int suma = sub_numar1[i] + sub_numar2[i] + local_carry;
//                 local_sum[i] = suma % 10;
//                 local_carry = suma / 10;
//                 if (!local_carry) break;
//             }
//         }
//
//         if (rank < size - 1) {
//             MPI_Send(&local_carry, 1, MPI_INT, rank + 1, 3, MPI_COMM_WORLD);
//         } else if (rank == size - 1) {
//             MPI_Send(&local_carry, 1, MPI_INT, 0, 3, MPI_COMM_WORLD);
//         }
//
//         MPI_Send(&segment_size, 1, MPI_INT, 0, 2, MPI_COMM_WORLD);
//         MPI_Send(local_sum, segment_size, MPI_INT, 0, 4, MPI_COMM_WORLD);
//
//         delete[] sub_numar1;
//         delete[] sub_numar2;
//         delete[] local_sum;
//     }
//
//     if (rank == 0) {
//         MPI_Status status;
//         int offset = 0;
//
//         for (int id_proces = 1; id_proces < size; ++id_proces) {
//             if (id_proces == size - 1) {
//                 MPI_Recv(&carry, 1, MPI_INT, id_proces, 3, MPI_COMM_WORLD, &status);
//                 if (carry)
//                     rezultat[max_size] = carry;
//             }
//             int segment_size;
//             MPI_Recv(&segment_size, 1, MPI_INT, id_proces, 2, MPI_COMM_WORLD, &status);
//
//             int* segment = new int[segment_size];
//             MPI_Recv(segment, segment_size, MPI_INT, id_proces, 4, MPI_COMM_WORLD, &status);
//
//             copy_n(segment, segment_size, rezultat + offset);
//             offset += segment_size;
//
//             delete[] segment;
//         }
//
//         auto endTime = chrono::high_resolution_clock::now();
//
//         // verifica daca rezultatul din varianta secventiala este la fel cu cel din varianta MPI
//         int *numar3 = citeste_numar("Numar3.txt", max_size);
//         assert(areSame(numar3, rezultat, max_size));
//
//         scrie_numar(rezultat, max_size, "Numar3.txt");
//
//         delete[] numar3;
//         delete[] rezultat;
//         double elapsed_time_ms = chrono::duration<double, std::milli>(endTime-startTime).count();
//         cout << elapsed_time_ms;
//         fin1.close();
//         fin2.close();
//     }
//
//     MPI_Finalize();
//     return 0;
// }

// VARIANTA 2
int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int *num1 = nullptr, *num2 = nullptr, *result = nullptr;
    int N1 = 0, N2 = 0, N = 0;
    chrono::time_point<chrono::system_clock> startTime;

    if (rank == 0) {
        num1 = citeste_numar("Numar1-16.txt", N1);
        num2 = citeste_numar("Numar2-16.txt", N2);

        N = max(N1, N2);
        int* extended_num1 = new int[N]();
        int* extended_num2 = new int[N]();

        copy_n(num1, N1, extended_num1);
        copy_n(num2, N2, extended_num2);

        delete[] num1;
        delete[] num2;
        num1 = extended_num1;
        num2 = extended_num2;

        if (N % size != 0) {
            int padding = size - (N % size);
            int* padded_num1 = new int[N + padding]();
            int* padded_num2 = new int[N + padding]();

            copy_n(num1, N, padded_num1);
            copy_n(num2, N, padded_num2);

            delete[] num1;
            delete[] num2;
            num1 = padded_num1;
            num2 = padded_num2;
            N += padding;
        }

        result = new int[N]();
        startTime = chrono::high_resolution_clock::now();
    }

    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int block_size = N / size;
    int* local_num1 = new int[block_size];
    int* local_num2 = new int[block_size];
    int* local_result = new int[block_size];

    MPI_Scatter(num1, block_size, MPI_INT, local_num1, block_size, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Scatter(num2, block_size, MPI_INT, local_num2, block_size, MPI_INT, 0, MPI_COMM_WORLD);

    int carry = 0;
    int local_carry = 0;

    for (int i = 0; i < block_size; ++i) {
        int sum = local_num1[i] + local_num2[i] + local_carry;
        local_result[i] = sum % 10;
        local_carry = sum / 10;
    }

    if (rank > 0) {
        MPI_Recv(&carry, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }

    if (carry) {
        local_carry = carry;
        for (int i = 0; i < block_size; ++i) {
            int sum = local_num1[i] + local_num2[i] + local_carry;
            local_result[i] = sum % 10;
            local_carry = sum / 10;
            if (!local_carry) break;
        }
    }

    MPI_Send(&local_carry, 1, MPI_INT, rank == size - 1 ? 0: rank + 1, 0, MPI_COMM_WORLD);

    MPI_Gather(local_result, block_size, MPI_INT, result, block_size, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        MPI_Recv(&carry, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        int num_digits = N;
        if (carry == 1) {
            auto* extended_result = new int[num_digits + 1];
            copy_n(result, num_digits, extended_result);
            extended_result[num_digits] = 1;
            num_digits += 1;

            delete[] result;
            result = extended_result;
        }

        auto endTime = chrono::high_resolution_clock::now();

        int* numar3 = citeste_numar("Numar3.txt", N);
        for (int i = 0; i < N; ++i)
            if (result[i] != numar3[i])
                cout << i << ": " << result[i] << " != " << numar3[i] << endl;

        assert(areSame(numar3, result, N));

        scrie_numar(result, N, "Numar3.txt");

        double elapsed_time_ms = chrono::duration<double, std::milli>(endTime - startTime).count();
        cout << elapsed_time_ms << endl;

        delete[] num1;
        delete[] numar3;
        delete[] num2;
        delete[] result;
    }

    delete[] local_num1;
    delete[] local_num2;
    delete[] local_result;

    MPI_Finalize();
    return 0;
}




