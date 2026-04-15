import subprocess
import numpy as np

# Configuration
M = 1000
PROCS = 64 # Switch to 25/64
BUILD_PATH = "./cmake-build-debug/"
EXECUTABLE = BUILD_PATH + "P4"
RUNS = 10

def run_test():
    readings, mults, writes = [], [], []

    print(f"Running {RUNS} iterations with {PROCS} MPI processes (Matrix {M}x{M})...")
    for i in range(RUNS):
        cmd = [
            "mpirun",
            "--oversubscribe", # COMMENT THIS FLAG WHEN TESTING IN CLUSTER
            "-np", str(PROCS),
            EXECUTABLE,
            str(M),
            BUILD_PATH + "matrixA.bin",
            BUILD_PATH + "matrixB.bin",
            BUILD_PATH + "matrixC.bin"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse output
            found_times = False
            for line in res.stdout.splitlines():
                if "t_read:" in line:
                    readings.append(float(line.split(":")[1].split()[0]))
                    found_times = True
                if "t_mult:" in line:
                    mults.append(float(line.split(":")[1].split()[0]))
                if "t_write:" in line:
                    writes.append(float(line.split(":")[1].split()[0]))

            if found_times:
                print(f"Iteration {i+1} done.")
            else:
                print(f"Iteration {i+1} failed to report times. Check MPI output.")

        except subprocess.CalledProcessError as e:
            print(f"Error at iteration {i+1}: {e}")
            print(f"Stderr: {e.stderr}")
            break

    if readings:
        avg_read = np.mean(readings)
        avg_mult = np.mean(mults)
        avg_write = np.mean(writes)

        print(f"\nAVERAGES for {PROCS} processes (M={M}):")
        print(f"Read:  {avg_read:.2f} ms")
        print(f"Mult:  {avg_mult:.2f} ms")
        print(f"Write: {avg_write:.2f} ms")
        print(f"Total: {avg_read + avg_mult + avg_write:.2f} ms")

if __name__ == "__main__":
    run_test()