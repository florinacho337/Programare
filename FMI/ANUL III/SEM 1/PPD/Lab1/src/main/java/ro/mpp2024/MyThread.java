package ro.mpp2024;

public class MyThread extends Thread {
    private int[] A;
    private int[] B;
    private int[] C;
    private int start;
    private int end;

    MyThread (int[] A, int[] B, int[] C, int start, int end) {
        this.A = A;
        this.B = B;
        this.C = C;
        this.start = start;
        this.end = end;
    }

    @Override
    public void run() {
        for (int i = start; i < end; i++) {
            C[i] = (int) Math.sqrt(A[i] * A[i] * A[i] * A[i] * A[i] + B[i] * B[i] * B[i] * B[i] * B[i]);
        }
    }
}
