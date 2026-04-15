#!/bin/bash

# Check if correct number of arguments provided
if [ "$#" -ne 3 ]; then
    echo "Usage: ./startnodes.sh <config_file> <first_index> <last_index>"
    exit 1
fi

CONFIG=$1
FIRST=$2
LAST=$3

echo "Starting nodes from index $FIRST to $LAST..."

for i in $(seq $FIRST $LAST); do
    # Run in background
    python3 bcastnode.py "$CONFIG" "$i" &
    echo "Node $i started."
done

echo "All nodes launched. They will wait 15s before broadcasting."
