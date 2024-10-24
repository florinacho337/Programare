package ro.orgexample;

public class MyThread extends Thread{
    private final int[][] matrix;
    private final int[][] kernel;
    private final int[][] result;
    private final int k;
    private final int n;
    private final int start;
    private final int end;
    private final int offset;
    private final char decomposition;

    MyThread(int[][] matrix, int[][] kernel, int[][] result, int k, int n, int start, int end, int offset, char decomposition) {
        this.matrix = matrix;
        this.kernel = kernel;
        this.result = result;
        this.n = n;
        this.k = k;
        this.offset = offset;
        this.start = start;
        this.end = end;
        this.decomposition = decomposition;
    }

    @Override
    public void run() {
        for (int i = start; i <= end; i++) {
            for (int j = offset; j <= n + offset - 1; j++) {
                int sum = 0;
                for (int ki = 0; ki < k; ki++) {
                    for (int kj = 0; kj < k; kj++) {
                        if (decomposition == 'h') {
                            sum += matrix[i + ki - offset][j + kj - offset] * kernel[ki][kj];
                        } else {
                            sum += matrix[j + ki - offset][i + kj - offset] * kernel[ki][kj];
                        }
                    }
                }
                if (decomposition == 'h') {
                    result[i - offset][j - offset] = sum;
                } else {
                    result[j - offset][i - offset] = sum;
                }
            }
        }
    }
}