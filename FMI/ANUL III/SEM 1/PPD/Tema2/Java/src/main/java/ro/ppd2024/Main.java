package ro.ppd2024;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.CyclicBarrier;

import static java.lang.Math.max;
import static java.lang.Math.min;

public class Main {
    public static void readMatrix(Scanner scanner, int[][] matrice, int n, int m) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                matrice[i][j] = scanner.nextInt();
            }
        }
    }

    public static void writeMatrix(String path, int[][] matrix, int n, int m) {
        try {
            FileWriter fileWriter = new FileWriter(path + "outputJava.txt");
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    fileWriter.write(matrix[i][j] + " ");
                }
                fileWriter.write("\n");
            }
            fileWriter.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) {
        String defaultPath = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema2/";

        int n = 10;
        int m = 10;
        int k = 3;
        int[][] F = new int[n][m];
        int[][] C = new int[k][k];

        Scanner scanner;
        try {
            scanner = new Scanner(new File(defaultPath + "data" + n + ".txt"));
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        readMatrix(scanner, F, n, m);
        readMatrix(scanner, C, k, k);
        scanner.close();

        int[] linie_anterioara = new int[m];
        int[] linie_modificata = new int[m];

        // 1. PROGRAM SECVENTIAL
        int margine = k / 2;

//        long startTime = System.currentTimeMillis();

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                int suma = 0;

                for (int ci = 0; ci < k; ++ci) {
                    for (int cj = 0; cj < k; ++cj) {
                        int x = i + ci - margine;
                        int y = j + cj - margine;

                        int valoare;
                        if (x >= 0 && x < n && y >= 0 && y < m) {
                            valoare = i > 0 && ci < margine
                                    ? linie_anterioara[y]
                                    : x == i && j > 0 && cj < margine
                                            ? F[i][j-1]
                                            : F[x][y];
                        } else {
                            int x_clona = min(max(x, 0), n - 1);
                            int y_clona = min(max(y, 0), m - 1);
                            valoare = i > 0 && ci < margine
                                    ? linie_anterioara[y_clona]
                                    : j > 0 && cj < margine
                                            ? F[i][j-1]
                                            : F[x_clona][y_clona];
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
//        long endTime = System.currentTimeMillis();

        writeMatrix(defaultPath, F, n, m);

        // 2. PROGRAM PARALEL
        Scanner scanParallel;
        Scanner scanResult;
        try {
            scanParallel = new Scanner(new File(defaultPath + "data" + n + ".txt"));
            scanResult = new Scanner(new File(defaultPath + "outputJava.txt"));
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }

        int[][] R = new int[n][m];
        F = new int[n][m];
        C = new int[k][k];

        readMatrix(scanParallel, F, n, m);
        readMatrix(scanParallel, C, k, k);
        readMatrix(scanResult, R, n, m);
        scanResult.close();
        scanParallel.close();

        int p = 2;
        int startRow = 0;
        int endRow = n / p;
        int remainingRows = n % p;
        MyThread[] threads = new MyThread[p];
        CyclicBarrier barrier = new CyclicBarrier(p);

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < p; ++i) {
            if (remainingRows > 0) {
                endRow++;
                remainingRows--;
            }

            // pregatire threads
            linie_anterioara = new int[m];
            int[] linie_urmatoare = new int[m];

            for (int j = 0; j < m; ++j) {
                linie_anterioara[j] = startRow > 0
                        ? F[startRow - 1][j]
                        : F[startRow][j];
                linie_urmatoare[j] = endRow < n
                        ? F[endRow][j]
                        : F[endRow - 1][j];
            }

            // initializare threads
            threads[i] = new MyThread(F, C, linie_anterioara, linie_urmatoare, n, m, k, margine, startRow, endRow, barrier);
            threads[i].start();

            startRow = endRow;
            endRow += n/p;
        }

        for (int i = 0; i < p; ++i) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
        }

        long endTime = System.currentTimeMillis();

        assert R == F;
        writeMatrix(defaultPath, F, n, m);
        System.out.println(endTime - startTime);
    }
}