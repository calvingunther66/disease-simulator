import sys
from disease import Influenza, COVID19, Measles, Ebola, Smallpox, CommonCold

def select_disease_cli():
    diseases = {
        "1": Influenza(),
        "2": COVID19(),
        "3": Measles(),
        "4": Ebola(),
        "5": Smallpox(),
        "6": CommonCold()
    }

    print("\nSelect a disease:")
    for key, disease_obj in diseases.items():
        print(f"{key}. {disease_obj.name}")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice in diseases:
            return diseases[choice]
        else:
            print("Invalid choice. Please try again.")

def get_starting_location_cli():
    print("\nEnter the starting location for the infection.")
    print("You can provide a city name (e.g., 'New York') or coordinates (e.g., '100,200').")
    while True:
        location_input = input("Enter location: ").strip()
        # Basic validation for coordinates (x,y)
        if ',' in location_input:
            try:
                x, y = map(int, location_input.split(','))
                return {'type': 'coordinates', 'x': x, 'y': y}
            except ValueError:
                print("Invalid coordinate format. Please use 'x,y'.")
        else:
            # Assume it's a city name for now.
            # Further validation/lookup will be needed in main.py or simulation.py
            return {'type': 'city_name', 'name': location_input}

def get_simulation_control_cli():
    print("\nChoose simulation termination condition:")
    print("1. Run indefinitely (until manually stopped with Ctrl+C)")
    print("2. Run until a target number of infected people is reached")
    print("3. Run until a target number of dead people is reached")
    print("4. Run until a target number of recovered people is reached")
    print("5. Run until a specific day is reached")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            return {'type': 'indefinite'}
        elif choice == '2':
            while True:
                try:
                    target = int(input("Enter target number of infected people: ").strip())
                    if target > 0:
                        return {'type': 'infected_target', 'value': target}
                    else:
                        print("Target must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == '3':
            while True:
                try:
                    target = int(input("Enter target number of dead people: ").strip())
                    if target > 0:
                        return {'type': 'dead_target', 'value': target}
                    else:
                        print("Target must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == '4':
            while True:
                try:
                    target = int(input("Enter target number of recovered people: ").strip())
                    if target > 0:
                        return {'type': 'recovered_target', 'value': target}
                    else:
                        print("Target must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == '5':
            while True:
                try:
                    target_day = int(input("Enter target day: ").strip())
                    if target_day > 0:
                        return {'type': 'day_target', 'value': target_day}
                    else:
                        print("Target day must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Example usage
    selected_disease = select_disease_cli()
    print(f"Selected disease: {selected_disease.name}")

    start_location = get_starting_location_cli()
    print(f"Starting location: {start_location}")

    sim_control = get_simulation_control_cli()
    print(f"Simulation control: {sim_control}")
