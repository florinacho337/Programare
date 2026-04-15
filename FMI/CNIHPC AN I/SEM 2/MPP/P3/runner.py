import subprocess
import numpy as np

# Configuration
M = 1000
THREADS = 20 # Switch to 20/40
EXECUTABLE = "./cmake-build-debug/P3"
RUNS = 10

def run_test():
    readings, mults, writes = [], [], []

    print(f"Running {RUNS} iterations with {THREADS} threads...")
    for i in range(RUNS):
        res = subprocess.run([EXECUTABLE, str(M), "matrixA.bin", "matrixB.bin", "matrixC.bin", str(THREADS)],
                             capture_output=True, text=True)

        # Parse output
        for line in res.stdout.splitlines():
            if "t_read:" in line: readings.append(float(line.split(":")[1].split()[0]))
            if "t_mult:" in line: mults.append(float(line.split(":")[1].split()[0]))
            if "t_write:" in line: writes.append(float(line.split(":")[1].split()[0]))
        print(f"Iteration {i+1} done.")

    print(f"\nAVERAGES for {THREADS} threads:")
    print(f"Read:  {np.mean(readings):.2f} ms")
    print(f"Mult:  {np.mean(mults):.2f} ms")
    print(f"Write: {np.mean(writes):.2f} ms")
    print(f"Total: {np.mean(readings)+np.mean(mults)+np.mean(writes):.2f} ms")

if __name__ == "__main__":
    run_test()