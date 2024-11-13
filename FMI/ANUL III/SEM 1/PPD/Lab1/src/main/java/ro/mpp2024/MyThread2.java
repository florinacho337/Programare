package ro.mpp2024;

public class MyThread2 extends Thread{
    private int[] A;
    private int[] B;
    private int[] C;
    private int p;
    private int n;
    private int id;

    MyThread2(int[] A, int[] B, int[] C, int p, int n, int id) {
        this.A = A;
        this.B = B;
        this.C = C;
        this.n = n;
        this.p = p;
        this.id = id;
    }

    @Override
    public void run() {
        for (int i = id; i < n; i+=p) {
            C[i] = (int) Math.sqrt(A[i] * A[i] * A[i] * A[i] * A[i] + B[i] * B[i] * B[i] * B[i] * B[i]);
        }
    }
}
