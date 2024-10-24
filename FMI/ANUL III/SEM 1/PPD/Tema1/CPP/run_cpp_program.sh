#!/bin/bash

# Check if the required parameters are provided
if [ -z "$1" ]; then
    echo "Usage: ./run_cpp_program.sh <NumberOfRuns>"
    exit 1
fi

# Assign parameters to variables
num_runs=$1

# Check if the number of runs is a valid positive integer
if ! [[ $num_runs =~ ^[0-9]+$ ]] || [ $num_runs -le 0 ]; then
    echo "Error: Number of runs must be a positive integer."
    exit 1
fi

# Compile the C++ program
echo "Compiling the C++ program..."
g++ -o main_program main.cpp

# Check if the compilation was successful
if [ $? -ne 0 ]; then
    echo "C++ compilation failed. Please check the error messages."
    exit 1
fi

# Initialize variables
total=0.0

# Loop to run the C++ program the specified number of times
for ((i = 1; i <= num_runs; i++)); do
    # Run the C++ program and capture its output
    result=$(./main_program)

    # Check if the result is a valid double
    if [[ $result =~ ^-?[0-9]*\.?[0-9]+$ ]]; then
        echo "Run $i: $result"
        total=$(echo "$total + $result" | bc -l)  # Add the result to the total using bc for floating-point arithmetic
    else
        echo "Run $i: Error - Invalid result from C++ program: $result"
    fi
done

# Calculate the average using floating-point division
average=$(echo "$total / $num_runs" | bc -l)

# Display the average
echo "Average result after $num_runs runs: $average"
