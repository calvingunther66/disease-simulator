"""
Main application file for the disease simulator.
"""

import sys
from simulation import Simulation

import config
import city_data_loader # For loading city coordinates
import cli_interface
import stats_display # For displaying statistics
import html_reporter # For generating HTML reports
import time # For time.sleep

def main():
    # Get simulation parameters from CLI
    selected_disease = cli_interface.select_disease_cli()
    start_location_data = cli_interface.get_starting_location_cli()
    sim_control = cli_interface.get_simulation_control_cli()

    # Initialize simulation
    # Note: SCREEN_WIDTH and SCREEN_HEIGHT are removed from config.
    # For now, pass dummy values or remove if not needed by Simulation constructor.
    # Will need to verify Simulation constructor in simulation.py
    simulation = Simulation(1280, 720, selected_disease) # Using dummy values for now

    # Handle starting location
    if start_location_data['type'] == 'coordinates':
        # Need to map these coordinates to a city or directly infect
        # For now, directly infect at these coordinates
        simulation.infect_location(start_location_data['x'], start_location_data['y'], radius=5)
    elif start_location_data['type'] == 'city_name':
        city_name = start_location_data['name']
        # Use dummy screen dimensions for lookup as actual screen is not used
        x, y, population = city_data_loader.get_city_coordinates(city_name, 1280, 720)
        if x is not None and y is not None:
            simulation.infect_location(x, y, radius=5)
            print(f"Infection started in {city_name} at coordinates ({x}, {y}). Population: {population}")
        else:
            print(f"City '{city_name}' not found in data. Skipping initial infection.")
        

    print("\nStarting simulation...")

    running = True
    infection_started = True # Assume infection starts immediately after setup

    # Simulation loop
    while running:
        # Update simulation (run 60 steps per simulated hour)
        if infection_started:
            for _ in range(60): # This loop runs 60 times per "frame" in old code, now per iteration
                simulation.update()

        # Display statistics (placeholder, will be replaced by stats_display.py)
        total_seconds = simulation.seconds_elapsed
        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        stats_display.display_stats(simulation)

        # Check termination conditions
        if sim_control['type'] == 'infected_target' and simulation.total_infected >= sim_control['value']:
            print(f"Simulation terminated: Target infected count ({sim_control['value']}) reached.")
            running = False
        elif sim_control['type'] == 'dead_target' and simulation.total_dead >= sim_control['value']:
            print(f"Simulation terminated: Target dead count ({sim_control['value']}) reached.")
            running = False
        elif sim_control['type'] == 'recovered_target' and simulation.total_recovered >= sim_control['value']:
            print(f"Simulation terminated: Target recovered count ({sim_control['value']}) reached.")
            running = False
        elif sim_control['type'] == 'day_target' and days >= sim_control['value']:
            print(f"Simulation terminated: Target day ({sim_control['value']}) reached.")
            running = False
        # For indefinite, loop continues until Ctrl+C

        # Small delay to make output readable, can be removed for faster simulation
        time.sleep(0.01) 

    print("\nSimulation finished.")
    # Generate detailed log (already handled by simulation.py)
    html_reporter.generate_html_report(config.LOG_FILE, "simulation_report.html")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
