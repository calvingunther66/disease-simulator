#!/bin/bash

# This script sets up the environment for the disease simulator.

echo "Creating Python virtual environment in 'venv'..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages from requirements.txt..."
venv/bin/pip install -r requirements.txt

echo "Installation complete. To run the simulator, use the run.sh script."
