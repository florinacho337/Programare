#!/bin/bash

# Check if the required parameters are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./run_java_program.sh <MainClassName> <NumberOfRuns>"
    exit 1
fi

# Assign parameters to variables
main_class=$1
num_runs=$2

# Check if the number of runs is a valid positive integer
if ! [[ $num_runs =~ ^[0-9]+$ ]] || [ $num_runs -le 0 ]; then
    echo "Error: Number of runs must be a positive integer."
    exit 1
fi

# Compile the Java program
echo "Compiling the Java program..."
mkdir -p out
javac -d out src/main/java/ro/orgexample/*.java  # Compile all .java files in the package

# Check if the compilation was successful
if [ $? -ne 0 ]; then
    echo "Java compilation failed. Please check the error messages."
    exit 1
fi

# Initialize variables
total=0.0

# Loop to run the Java program the specified number of times
for ((i = 1; i <= num_runs; i++)); do
    # Run the Java program and capture its output
    result=$(java -cp out ro.orgexample.Main)  # Make sure to call the correct main class

    # Check if the result is a valid number
    if [[ $result =~ ^-?[0-9]*\.?[0-9]+$ ]]; then
        echo "Run $i: $result"
        total=$(echo "$total + $result" | bc -l)  # Add the result to the total using bc for floating-point arithmetic
    else
        echo "Run $i: Error - Invalid result from Java program: $result"
    fi
done

# Calculate the average using floating-point division
average=$(echo "$total / $num_runs" | bc -l)

# Display the average
echo "Average result after $num_runs runs: $average"

