# Disease Simulator

This program simulates the spread of infectious diseases, focusing on data-driven analysis rather than visual representation.

## Features

*   **CLI-driven Interaction**: Select disease and starting location via command-line prompts.
*   **Flexible Simulation Control**: Run indefinitely, or terminate based on target counts for infected, dead, or recovered populations, or a specific simulated day.
*   **Detailed Statistics**: Real-time console output of healthy, exposed, infected, recovered, and dead populations.
*   **Comprehensive Logging**: Generates a `simulation_log.csv` file with second-by-second data of the simulation's progression.
*   **HTML Report**: Creates a `simulation_report.html` file with an interactive chart visualizing population states over time.

## Installation (for Crostini Linux)

Follow these steps to set up and run the simulator on your Crostini Linux environment.

1.  **Navigate to the project directory:**
    ```bash
    cd /home/calvingunther66/disease-simulator
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
    cd /home/calvingunther66/disease-simulator
    ```

2.  **Make the run script executable:**
    ```bash
    chmod +x run.sh
    ```

3.  **Run the simulator:**
    ```bash
    ./run.sh
    ```
    Upon running, you will be prompted to:
    *   **Select a Disease**: Choose from a list of predefined diseases.
    *   **Enter Starting Location**: Provide a city name (e.g., "New York") or coordinates (e.g., "100,200") to initiate the infection.
    *   **Choose Termination Condition**: Decide whether the simulation runs indefinitely (until Ctrl+C), or stops when a certain number of infected, dead, or recovered individuals is reached, or after a specific number of simulated days.

## Output Files

After the simulation completes (or is interrupted), the following files will be generated in the project root directory:

*   `simulation_log.csv`: A comma-separated values file containing a detailed, second-by-second log of the simulation's state (healthy, exposed, infected, recovered, dead counts).
*   `simulation_report.html`: An interactive HTML file that visualizes the population states over time using a line chart. Open this file in a web browser to view the report.

## Customization

You can modify the simulation parameters by editing the `config.py`, `disease.py`, and `simulation.py` files:

*   `config.py`: Adjust file paths and other global settings.
*   `disease.py`: Modify disease attributes (infectivity, severity, lethality, transmission rates) or add new disease types.
*   `simulation.py`: Tweak the core simulation logic, such as spread mechanics or long-distance transmission probabilities.