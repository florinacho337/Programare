import subprocess
import numpy as np

# --- CONFIGURATION ---
M = 1000
EXECUTABLE = "./cmake-build-debug/P1"
FILE_A = "./cmake-build-debug/matrixA.bin"
FILE_B = "./cmake-build-debug/matrixB.bin"
FILE_C = "./cmake-build-debug/matrixC.bin"
ITERATIONS = 10


def run_benchmark():
    t_reading_list = []
    t_mult_list = []
    t_writing_list = []
    t_total_list = []

    print(f"--- Starting Benchmark: M={M}, Iterations={ITERATIONS} ---")

    for i in range(ITERATIONS):
        process = subprocess.run(
            [EXECUTABLE, str(M), FILE_A, FILE_B, FILE_C],
            capture_output=True,
            text=True
        )

        if process.returncode != 0:
            print(f"Run {i + 1} failed: {process.stderr}")
            continue

        # Parse the execution times from C++ stdout
        try:
            current_times = {}
            for line in process.stdout.splitlines():
                if ":" in line:
                    label, value = line.split(":")
                    # Extract the first float found in the string
                    current_times[label.strip()] = float(value.strip().split()[0])

            t_reading_list.append(current_times['t_reading'])
            t_mult_list.append(current_times['t_multiplication'])
            t_writing_list.append(current_times['t_writing'])
            t_total_list.append(current_times['t_total'])

            print(f"Run {i + 1}/{ITERATIONS} completed.")
        except Exception as e:
            print(f"Parsing error on run {i + 1}: {e}")

    # Display Average Results
    if t_total_list:
        print("\n" + "=" * 40)
        print(f"AVERAGE RESULTS FOR M={M}")
        print(f"Avg Reading:        {sum(t_reading_list) / len(t_reading_list):.3f} ms")
        print(f"Avg Multiplication: {sum(t_mult_list) / len(t_mult_list):.3f} ms")
        print(f"Avg Writing:        {sum(t_writing_list) / len(t_writing_list):.3f} ms")
        print(f"Avg Total Time:     {sum(t_total_list) / len(t_total_list):.3f} ms")
        print("=" * 40)


def verify_math():
    print("\nStarting Mathematical Verification...")
    try:
        # Load matrices using numpy
        a = np.fromfile(FILE_A, dtype=np.float64).reshape((M, M))
        b = np.fromfile(FILE_B, dtype=np.float64).reshape((M, M))
        c_actual = np.fromfile(FILE_C, dtype=np.float64).reshape((M, M))

        # Calculate reference
        c_ref = np.matmul(a, b)

        # Compare with tolerance for floating point precision
        if np.allclose(c_actual, c_ref, atol=1e-9):
            print("VERIFICATION: SUCCESS! Your C++ result matches Numpy.")
        else:
            print("VERIFICATION: FAILED! Results do not match.")

    except MemoryError:
        print("Verification skipped: Matrix is too large for System RAM.")
    except Exception as e:
        print(f"Verification error: {e}")


if __name__ == "__main__":
    run_benchmark()
    verify_math()