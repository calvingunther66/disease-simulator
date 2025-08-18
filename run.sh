#!/bin/bash

# This script runs the disease simulator.

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running simulator..."
python3 main.py
