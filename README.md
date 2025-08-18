# Disease Simulator

This program simulates the spread of infectious diseases across a world map, inspired by games like Plague Inc.

## Features

*   Interactive world map visualization.
*   Population data based on real-world city populations.
*   Selectable disease types (Influenza, COVID-19, Measles) with customizable attributes.
*   Simulation of land-based and long-distance (air/sea) transmission.
*   Real-time tracking of infected, dead, and recovered populations.

## Installation (for Crostini Linux)

Follow these steps to set up and run the simulator on your Crostini Linux environment.

1.  **Navigate to the project directory:**
    ```bash
    cd /home/calvingunther66/disease_simulator
    ```

2.  **Make the installation script executable:**
    ```bash
    chmod +x install.sh
    ```

3.  **Run the installation script:**
    This script will create a Python virtual environment and install all necessary dependencies.
    ```bash
    ./install.sh
    ```

    *Note: If you encounter any errors during installation, ensure you have `python3-venv` and `pip` installed. You might need to run `sudo apt update && sudo apt install python3-venv python3-pip`.*

## Running the Simulator

1.  **Navigate to the project directory (if not already there):**
    ```bash
    cd /home/calvingunther66/disease_simulator
    ```

2.  **Make the run script executable:**
    ```bash
    chmod +x run.sh
    ```

3.  **Run the simulator:**
    ```bash
    ./run.sh
    ```

## How to Play

1.  **Select a Disease:** When the application starts, you will be prompted to select a disease (Influenza, COVID-19, or Measles) by pressing the corresponding number key.
2.  **Start Infection:** Once the map loads, click anywhere on the map to initiate the first infection. The disease will begin to spread from that point.
3.  **Observe:** Watch as the disease spreads across the world. Infected areas will be highlighted in red. Statistics for infected, dead, and recovered populations will be displayed at the top left.

## Customization

You can modify the simulation parameters by editing the `config.py`, `disease.py`, and `simulation.py` files:

*   `config.py`: Adjust screen dimensions, colors, and file paths.
*   `disease.py`: Modify disease attributes (infectivity, severity, lethality, transmission rates) or add new disease types.
*   `simulation.py`: Tweak the simulation logic, such as spread mechanics or long-distance transmission probabilities.
