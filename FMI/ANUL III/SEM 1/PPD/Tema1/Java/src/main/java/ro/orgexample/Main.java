package ro.orgexample;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    static String path = "/home/florin/Documents/GitHub/Programare/FMI/ANUL III/SEM 1/PPD/Tema1/";
    public static void generateMatrixAndKernel(int n, int m, int k) {
        try {
            FileWriter fileWriter = new FileWriter(path + "data10000.txt");
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    int nr = (int)(Math.random() * 100);
                    fileWriter.write(nr + " ");
                }
                fileWriter.write("\n");
            }

            for (int i = 0; i < k; i++) {
                for (int j = 0; j < k; j++) {
                    if (i == k/2 && j == k/2) {
                        fileWriter.write("8 ");
                    } else {
                        fileWriter.write("-1 ");
                    }
                }
                fileWriter.write("\n");
            }
            fileWriter.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public static void borderValues(int[][] matrix, int n, int m, int k) {
        int offset = k / 2;
        // Fill left and right borders
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < offset; j++) {
                matrix[i][j] = matrix[i][offset];
                matrix[i][m + offset + j] = matrix[i][m + offset - 1];
            }
        }
        // Fill top and bottom borders
        for (int j = 0; j < m + 2 * offset; j++) {
            for (int i = 0; i < offset; i++) {
                matrix[i][j] = matrix[offset][j];
                matrix[n + offset + i][j] = matrix[n + offset - 1][j];
            }
        }
    }

    public static void readData(int[][] matrix, int[][] kernel, int n, int m, int k) {
        try {
            int offset = k/2;
            Scanner scanner = new Scanner(new File(path + "data" + n + ".txt"));
            for (int i = offset; i <= n + offset - 1; i++) {
                for (int j = offset; j <= m + offset - 1; j++) {
                    matrix[i][j] = scanner.nextInt();
                }
            }

            for (int i = 0; i < k; i++) {
                for (int j = 0; j < k; j++) {
                    kernel[i][j] = scanner.nextInt();
                }
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }

    public static void writeMatrix(int[][] matrix, int n, int m) {
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
        int n = 10000;
        int m = 10000;
        int k = 5;
        int[][] matrix = new int[n+k-1][m+k-1];
        int[][] kernel = new int[k][k];
        int[][] result = new int[n][m];
        int nrThreads = 16;
        int offset = k / 2;

//        generateMatrixAndKernel(n, m, k);

        readData(matrix, kernel, n, m, k);

        borderValues(matrix, n, m, k);

        // 1. SEQUENTIAL PROGRAM
//        long startTime = System.currentTimeMillis();
        for (int i = offset; i <= n + offset - 1; i++) {
            for (int j = offset; j <= m + offset - 1; j++) {
                int sum = 0;
                for (int ki = 0; ki < k; ki++) {
                    for (int kj = 0; kj < k; kj++) {
                        sum += matrix[i - offset + ki][j - offset + kj] * kernel[ki][kj];
                    }
                }
                result[i - offset][j - offset] = sum;
            }
        }
//        long endTime = System.currentTimeMillis();
//        System.out.println(endTime - startTime);
//        writeMatrix(result, n, m);

        // 2. PARALLEL PROGRAM
        MyThread[] threads = new MyThread[nrThreads];

        // 2.1. Split the matrix horizontally
        int rowsPerThread = n / nrThreads;
        int remainingRows = n % nrThreads;
        int startRow = offset;
        int endRow = rowsPerThread + offset - 1;

        int[][] resultParallel = new int[n][m];
        long startTime = System.currentTimeMillis();


        for (int i = 0; i < nrThreads; i++) {
            if (remainingRows > 0) {
                remainingRows--;
                endRow++;
            }
            threads[i] = new MyThread(matrix, kernel, resultParallel, k, m, startRow, endRow, offset, 'h');
            threads[i].start();

            startRow = endRow + 1;
            endRow += rowsPerThread;
        }

        for (int i = 0; i < nrThreads; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                System.out.println(e.getMessage());
            }
        }

        long endTime = System.currentTimeMillis();
        assert result == resultParallel;
        System.out.println(endTime - startTime);
        writeMatrix(resultParallel, n, m);

        // 2.2. Split the matrix vertically
//        int colsPerThread = m / nrThreads;
//        int remainingCols = m % nrThreads;
//        int startCol = offset;
//        int endCol = colsPerThread + offset - 1;
//
//        int[][] resultParallel2 = new int[n][m];
//        long startTime = System.currentTimeMillis();
//
//        for (int i = 0; i < nrThreads; i++) {
//            if (remainingCols > 0) {
//                remainingCols--;
//                endCol++;
//            }
//            threads[i] = new MyThread(matrix, kernel, resultParallel2, k, n, startCol, endCol, offset, 'v');
//            threads[i].start();
//
//            startCol = endCol + 1;
//            endCol += colsPerThread;
//        }
//
//        for (int i = 0; i < nrThreads; i++) {
//            try {
//                threads[i].join();
//            } catch (InterruptedException e) {
//                System.out.println(e.getMessage());
//            }
//        }
//
//        long endTime = System.currentTimeMillis();
//        assert result == resultParallel;
//        System.out.println(endTime - startTime);
//        writeMatrix(resultParallel2, n, m);
    }
}
