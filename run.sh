#!/bin/bash

# This script runs the disease simulator (now CLI-driven).

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running simulator..."
python3 main.py
