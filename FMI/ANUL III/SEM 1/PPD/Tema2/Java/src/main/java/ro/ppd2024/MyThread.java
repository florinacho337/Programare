package ro.ppd2024;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;

import static java.lang.Math.max;
import static java.lang.Math.min;

public class MyThread extends Thread {
    private final int[][] F;
    private final int[][] C;
    private final int[] linie_anterioara;
    private final int[] linie_modificata;
    private final int[] linie_urmatoare;
    private final int n;
    private final int m;
    private final int k;
    private final int margine;
    private final int start;
    private final int end;
    private final CyclicBarrier barrier;

    public MyThread(int[][] F, int[][] C, int[] linie_anterioara, int[] linie_urmatoare, int n, int m, int k, int margine, int start, int end, CyclicBarrier barrier) {
        this.F = F;
        this.C = C;
        this.linie_anterioara = linie_anterioara;
        this.linie_modificata = new int[m];
        this.linie_urmatoare = linie_urmatoare;
        this.n = n;
        this.m = m;
        this.k = k;
        this.margine = margine;
        this.start = start;
        this.end = end;
        this.barrier = barrier;
    }

    @Override
    public void run() {
        try {
            barrier.await();
            for (int i = start; i < end; ++i) {
                for (int j = 0; j < m; ++j) {
                    int suma = 0;

                    for (int ci = 0; ci < k; ++ci) {
                        for (int cj = 0; cj < k; ++cj) {
                            int x = i + ci - margine;
                            int y = j + cj - margine;

                            int valoare;
                            if (x >= 0 && x < n && y >= 0 && y < m) {
                                valoare = ci < margine
                                        ? linie_anterioara[y]
                                        : x == i && j > 0 && cj < margine
                                                ? F[i][j - 1]
                                                : i == end - 1 && ci > margine
                                                    ? linie_urmatoare[y]
                                                    : F[x][y];
                            } else {
                                int x_clona = min(max(x, 0), n - 1);
                                int y_clona = min(max(y, 0), m - 1);
                                valoare = ci < margine
                                        ? linie_anterioara[y_clona] :
                                        j > 0 && cj < margine
                                                ? F[i][j - 1]
                                                : i == end - 1 && ci > margine
                                                        ? linie_urmatoare[y_clona]
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
        } catch (InterruptedException | BrokenBarrierException e) {
            System.out.println(e.getMessage());
        }
    }
}
