import os

def display_stats(simulation):
    os.system('cls' if os.name == 'nt' else 'clear') # Clear console

    total_seconds = simulation.seconds_elapsed
    days = total_seconds // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    print("\n--- Simulation Statistics ---")
    print(f"Current Time: Day: {days} {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"Healthy:    {simulation.total_healthy}")
    print(f"Exposed:    {simulation.total_exposed}")
    print(f"Infected:   {simulation.total_infected}")
    print(f"Recovered:  {simulation.total_recovered}")
    print(f"Dead:       {simulation.total_dead}")
    print("-----------------------------")
