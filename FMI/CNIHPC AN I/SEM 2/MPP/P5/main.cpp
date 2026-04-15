#include <mpi.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <string>

using namespace std;

typedef double matrix_t;

constexpr bool USE_PARALLEL_READ = true;
constexpr int NUM_THREADS = 10;

void localMultiplyHybrid(int n, const vector<matrix_t>& A, const vector<matrix_t>& B, vector<matrix_t>& C) {
    #pragma omp parallel for num_threads(NUM_THREADS)
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            matrix_t valA = A[i * n + k];
            for (int j = 0; j < n; ++j) {
                C[i * n + j] += valA * B[k * n + j];
            }
        }
    }
}

// --- SEQUENTIAL READING ---
void readSequential(const string& fileA, const string& fileB, vector<matrix_t>& localA, vector<matrix_t>& localB,
                    uint32_t M, int n, int q, int rank, MPI_Comm cart_comm) {
    if (rank == 0) {
        FILE* fA = fopen(fileA.c_str(), "rb");
        FILE* fB = fopen(fileB.c_str(), "rb");

        vector<matrix_t> buffer(n * n);

        for (int r = 0; r < q; ++r) {
            for (int c = 0; c < q; ++c) {
                for (int i = 0; i < n; ++i) {
                    long long offset = (static_cast<long long>(r * n + i) * M + (c * n)) * sizeof(matrix_t);
                    fseek(fA, offset, SEEK_SET);
                    fread(&buffer[i * n], sizeof(matrix_t), n, fA);
                }

                int target_rank;
                int coords[2] = {r, c};
                MPI_Cart_rank(cart_comm, coords, &target_rank);

                if (target_rank == 0) localA = buffer;
                else MPI_Send(buffer.data(), n * n, MPI_DOUBLE, target_rank, 0, cart_comm);

                for (int i = 0; i < n; ++i) {
                    long long offset = (static_cast<long long>(r * n + i) * M + (c * n)) * sizeof(matrix_t);
                    fseek(fB, offset, SEEK_SET);
                    fread(&buffer[i * n], sizeof(matrix_t), n, fB);
                }
                if (target_rank == 0) localB = buffer;
                else MPI_Send(buffer.data(), n * n, MPI_DOUBLE, target_rank, 1, cart_comm);
            }
        }
        fclose(fA); fclose(fB);
    } else {
        MPI_Recv(localA.data(), n * n, MPI_DOUBLE, 0, 0, cart_comm, MPI_STATUS_IGNORE);
        MPI_Recv(localB.data(), n * n, MPI_DOUBLE, 0, 1, cart_comm, MPI_STATUS_IGNORE);
    }
}

// --- PARALLEL READING (MPI-IO) ---
void readParallel(const string& filename, vector<matrix_t>& local_mat, uint32_t M, int n, int rank, MPI_Comm cart_comm) {
    int coords[2];
    MPI_Cart_coords(cart_comm, rank, 2, coords);

    MPI_File file;

    if (int err = MPI_File_open(cart_comm, filename.c_str(), MPI_MODE_RDONLY, MPI_INFO_NULL, &file); err == MPI_SUCCESS) {
        for (int i = 0; i < n; ++i) {
            MPI_Offset offset = (static_cast<MPI_Offset>(coords[0] * n + i) * M + (coords[1] * n)) * sizeof(matrix_t);
            MPI_File_read_at(file, offset, &local_mat[i * n], n, MPI_DOUBLE, MPI_STATUS_IGNORE);
        }
        MPI_File_close(&file);
    } else {
        char err_buffer[MPI_MAX_ERROR_STRING];
        int resultlen;
        MPI_Error_string(err, err_buffer, &resultlen);
        cout << "Rank " << rank << " nu poate deschide fisierul: " << err_buffer << endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
}

// --- SEQUENTIAL WRITING ---
void writeSequential(const string& fileC, const vector<matrix_t>& localC, uint32_t M, int n, int q, int rank, MPI_Comm cart_comm) {
    if (rank == 0) {
        FILE* f = fopen(fileC.c_str(), "wb");
        vector<matrix_t> buffer(n * n);

        for (int r = 0; r < q; ++r) {
            for (int c = 0; c < q; ++c) {
                int src_rank;
                int coords[2] = {r, c};
                MPI_Cart_rank(cart_comm, coords, &src_rank);

                if (src_rank == 0) buffer = localC;
                else MPI_Recv(buffer.data(), n * n, MPI_DOUBLE, src_rank, 0, cart_comm, MPI_STATUS_IGNORE);

                for (int i = 0; i < n; ++i) {
                    long long offset = (static_cast<long long>(r * n + i) * M + (c * n)) * sizeof(matrix_t);
                    fseek(f, offset, SEEK_SET);
                    fwrite(&buffer[i * n], sizeof(matrix_t), n, f);
                }
            }
        }
        fclose(f);
    } else {
        MPI_Send(localC.data(), n * n, MPI_DOUBLE, 0, 0, cart_comm);
    }
}

int main(int argc, char* argv[]) {
    int provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    if (argc < 5) {
        if (world_rank == 0) cout << "Usage: mpirun ./P5 <M> <A.bin> <B.bin> <C.bin>" << endl;
        MPI_Finalize(); return 1;
    }

    uint32_t M = stoul(argv[1]);
    string fA = argv[2], fB = argv[3], fC = argv[4];

    int q = sqrt(world_size);
    int n = M / q;

    // 1. Cartesian topology initialization
    int dims[2] = {q, q}, periods[2] = {1, 1};
    MPI_Comm cart_comm;
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 1, &cart_comm);

    int coords[2], left, right, up, down;
    MPI_Cart_coords(cart_comm, world_rank, 2, coords);
    MPI_Cart_shift(cart_comm, 1, 1, &left, &right); // Row shift (left-right)
    MPI_Cart_shift(cart_comm, 0, 1, &up, &down);    // Column shift (up-down)

    vector<matrix_t> localA(n * n), localB(n * n), localC(n * n, 0.0);

    // --- READING ---
    double t1 = MPI_Wtime();
    if constexpr (!USE_PARALLEL_READ) {
        readSequential(fA, fB, localA, localB, M, n, q, world_rank, cart_comm);
    } else {
        readParallel(fA, localA, M, n, world_rank, cart_comm);
        readParallel(fB, localB, M, n, world_rank, cart_comm);
    }
    double t2 = MPI_Wtime();

    // --- HYBRID MULTIPLICATION (CANNON + OPENMP) ---
    double t3 = MPI_Wtime();

    // Step 1: Initial skew
    int src, dest;
    // Shift A to left with 'row' positions
    MPI_Cart_shift(cart_comm, 1, coords[0], &src, &dest);
    MPI_Sendrecv_replace(localA.data(), n * n, MPI_DOUBLE, dest, 10, src, 10, cart_comm, MPI_STATUS_IGNORE);
    // Shift B up with 'col' positions
    MPI_Cart_shift(cart_comm, 0, coords[1], &src, &dest);
    MPI_Sendrecv_replace(localB.data(), n * n, MPI_DOUBLE, dest, 20, src, 20, cart_comm, MPI_STATUS_IGNORE);

    // Step 2: Main loop (q steps)
    for (int step = 0; step < q; ++step) {
        localMultiplyHybrid(n, localA, localB, localC);
        // Circular shift A (left 1)
        MPI_Sendrecv_replace(localA.data(), n * n, MPI_DOUBLE, left, 10, right, 10, cart_comm, MPI_STATUS_IGNORE);
        // Circular shift B (up 1)
        MPI_Sendrecv_replace(localB.data(), n * n, MPI_DOUBLE, up, 20, down, 20, cart_comm, MPI_STATUS_IGNORE);
    }
    double t4 = MPI_Wtime();

    // --- WRITING ---
    double t5 = MPI_Wtime();
    writeSequential(fC, localC, M, n, q, world_rank, cart_comm);
    double t6 = MPI_Wtime();

    // RESULTS (Rank 0)
    if (world_rank == 0) {
        cout << "t_read: " << (t2 - t1) * 1000 << " ms" << endl;
        cout << "t_mult: " << (t4 - t3) * 1000 << " ms" << endl;
        cout << "t_write: " << (t6 - t5) * 1000 << " ms" << endl;
    }

    MPI_Comm_free(&cart_comm);
    MPI_Finalize();
    return 0;
}