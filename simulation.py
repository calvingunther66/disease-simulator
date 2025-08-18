"""
Core simulation logic for disease spread.
"""

import numpy as np
import random
import csv
from population import Population
from disease import Disease
import config

class Simulation:
    def __init__(self, screen_width, screen_height, disease: Disease):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.disease = disease
        self.population = Population(screen_width, screen_height)

        # Population grids
        self.susceptible_grid = np.copy(self.population.population_grid)
        self.exposed_grid = np.zeros((screen_height, screen_width), dtype=int)
        self.infected_grid = np.zeros((screen_height, screen_width), dtype=int)
        self.recovered_grid = np.zeros((screen_height, screen_width), dtype=int)
        self.dead_grid = np.zeros((screen_height, screen_width), dtype=int)
        
        self.simulation_grid = self.infected_grid 

        self.hours_elapsed = 0
        self.total_healthy = np.sum(self.susceptible_grid)
        self.total_exposed = 0
        self.total_infected = 0
        self.total_dead = 0
        self.total_recovered = 0
        self.air_travel_lines = []

        # Logging
        self.log_file = open(config.LOG_FILE, 'w', newline='')
        self.log_writer = csv.writer(self.log_file)
        self.log_writer.writerow(['Hour', 'Healthy', 'Exposed', 'Infected', 'Recovered', 'Dead'])

    def infect_location(self, x, y, radius=5):
        """Starts the infection in a radius around a screen coordinate."""
        infection_started = False
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if 0 <= i < self.screen_width and 0 <= j < self.screen_height:
                    if self.susceptible_grid[j, i] > 0:
                        initial_infections = min(self.susceptible_grid[j, i], 100)
                        self.susceptible_grid[j, i] -= initial_infections
                        self.exposed_grid[j, i] += initial_infections
                        infection_started = True
        
        if infection_started:
            self.update_totals()
            print(f"Infection started around ({x}, {y})")
        return infection_started

    def update(self):
        """Advances the simulation by one hour."""
        self.hours_elapsed += 1

        # Calculate transition rates (per hour)
        exposure_rate = self.disease.infectivity
        infection_rate = 1 / (self.disease.incubation_period * 24)
        recovery_rate = (1 - self.disease.lethality) / (self.disease.infection_duration * 24)
        death_rate = self.disease.lethality / (self.disease.infection_duration * 24)

        # E -> I
        newly_infected = self.exposed_grid * infection_rate
        self.exposed_grid -= newly_infected
        self.infected_grid += newly_infected

        # I -> R/D
        newly_recovered = self.infected_grid * recovery_rate
        newly_dead = self.infected_grid * death_rate
        self.infected_grid -= (newly_recovered + newly_dead)
        self.recovered_grid += newly_recovered
        self.dead_grid += newly_dead

        # S -> E (Local Spread)
        # Simplified: spread from infected to susceptible neighbors
        total_population_grid = self.susceptible_grid + self.exposed_grid + self.infected_grid + self.recovered_grid
        # Avoid division by zero
        safe_total_pop = np.where(total_population_grid == 0, 1, total_population_grid)
        infection_pressure = self.infected_grid / safe_total_pop * exposure_rate
        newly_exposed = self.susceptible_grid * infection_pressure
        self.susceptible_grid -= newly_exposed
        self.exposed_grid += newly_exposed

        # Long-distance transmission
        if self.total_infected > 1000 and random.random() < self.disease.transmission_air * 0.05:
            infected_cities = np.argwhere(self.infected_grid > 10)
            high_pop_cities = np.argwhere(self.population.population_grid > 100000)

            if len(infected_cities) > 0 and len(high_pop_cities) > 0:
                source_y, source_x = random.choice(infected_cities)
                target_y, target_x = random.choice(high_pop_cities)

                if self.susceptible_grid[target_y, target_x] > 100:
                    travel_infections = min(self.susceptible_grid[target_y, target_x], 10)
                    self.susceptible_grid[target_y, target_x] -= travel_infections
                    self.exposed_grid[target_y, target_x] += travel_infections
                    self.air_travel_lines.append(((source_x, source_y), (target_x, target_y)))

        self.update_totals()
        self.log_data()
        self.simulation_grid = self.infected_grid + self.exposed_grid # Visualize both exposed and infected

    def update_totals(self):
        """Recalculates total counts from the grids."""
        self.total_healthy = int(np.sum(self.susceptible_grid))
        self.total_exposed = int(np.sum(self.exposed_grid))
        self.total_infected = int(np.sum(self.infected_grid))
        self.total_dead = int(np.sum(self.dead_grid))
        self.total_recovered = int(np.sum(self.recovered_grid))

    def log_data(self):
        """Logs the current simulation state to the CSV file."""
        """
Core simulation logic for disease spread.
"""

import numpy as np
import random
import csv
from population import Population
from disease import Disease
import config

class Simulation:
    def __init__(self, screen_width, screen_height, disease: Disease):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.disease = disease
        self.population = Population(screen_width, screen_height)

        # Population grids
        self.susceptible_grid = np.copy(self.population.population_grid).astype(float)
        self.exposed_grid = np.zeros((screen_height, screen_width), dtype=float)
        self.infected_grid = np.zeros((screen_height, screen_width), dtype=float)
        self.recovered_grid = np.zeros((screen_height, screen_width), dtype=float)
        self.dead_grid = np.zeros((screen_height, screen_width), dtype=float)
        
        self.simulation_grid = self.infected_grid 

        self.seconds_elapsed = 0
        self.total_healthy = np.sum(self.susceptible_grid)
        self.total_exposed = 0
        self.total_infected = 0
        self.total_dead = 0
        self.total_recovered = 0
        self.air_travel_lines = []

        # Logging
        self.log_file = open(config.LOG_FILE, 'w', newline='')
        self.log_writer = csv.writer(self.log_file)
        self.log_writer.writerow(['Second', 'Healthy', 'Exposed', 'Infected', 'Recovered', 'Dead'])

    def infect_location(self, x, y, radius=5):
        """Starts the infection in a radius around a screen coordinate."""
        infection_started = False
        for i in range(x - radius, x + radius):
            for j in range(y - radius, y + radius):
                if 0 <= i < self.screen_width and 0 <= j < self.screen_height:
                    if self.susceptible_grid[j, i] > 0:
                        initial_infections = min(self.susceptible_grid[j, i], 100)
                        self.susceptible_grid[j, i] -= initial_infections
                        self.exposed_grid[j, i] += initial_infections
                        infection_started = True
        
        if infection_started:
            self.update_totals()
            print(f"Infection started around ({x}, {y})")
        return infection_started

    def update(self):
        """Advances the simulation by one second."""
        self.seconds_elapsed += 1

        # Calculate transition rates (per second)
        secs_in_day = 24 * 60 * 60
        exposure_rate = self.disease.infectivity
        infection_rate = 1 / (self.disease.incubation_period * secs_in_day)
        recovery_rate = (1 - self.disease.lethality) / (self.disease.infection_duration * secs_in_day)
        death_rate = self.disease.lethality / (self.disease.infection_duration * secs_in_day)

        # E -> I
        newly_infected = self.exposed_grid * infection_rate
        self.exposed_grid -= newly_infected
        self.infected_grid += newly_infected

        # I -> R/D
        newly_recovered = self.infected_grid * recovery_rate
        newly_dead = self.infected_grid * death_rate
        self.infected_grid -= (newly_recovered + newly_dead)
        self.recovered_grid += newly_recovered
        self.dead_grid += newly_dead

        # S -> E (Local Spread)
        total_population_grid = self.susceptible_grid + self.exposed_grid + self.infected_grid + self.recovered_grid
        safe_total_pop = np.where(total_population_grid == 0, 1, total_population_grid)
        infection_pressure = self.infected_grid / safe_total_pop * exposure_rate
        newly_exposed = self.susceptible_grid * infection_pressure
        self.susceptible_grid -= newly_exposed
        self.exposed_grid += newly_exposed

        # Long-distance transmission (happens less frequently)
        if self.seconds_elapsed % 3600 == 0: # Once per hour
            if self.total_infected > 1000 and random.random() < self.disease.transmission_air * 0.05:
                infected_cities = np.argwhere(self.infected_grid > 10)
                high_pop_cities = np.argwhere(self.population.population_grid > 100000)

                if len(infected_cities) > 0 and len(high_pop_cities) > 0:
                    source_y, source_x = random.choice(infected_cities)
                    target_y, target_x = random.choice(high_pop_cities)

                    if self.susceptible_grid[target_y, target_x] > 100:
                        travel_infections = min(self.susceptible_grid[target_y, target_x], 10)
                        self.susceptible_grid[target_y, target_x] -= travel_infections
                        self.exposed_grid[target_y, target_x] += travel_infections
                        self.air_travel_lines.append(((source_x, source_y), (target_x, target_y)))

        self.update_totals()
        self.log_data()
        self.simulation_grid = self.infected_grid + self.exposed_grid

    def update_totals(self):
        """Recalculates total counts from the grids."""
        self.total_healthy = int(np.sum(self.susceptible_grid))
        self.total_exposed = int(np.sum(self.exposed_grid))
        self.total_infected = int(np.sum(self.infected_grid))
        self.total_dead = int(np.sum(self.dead_grid))
        self.total_recovered = int(np.sum(self.recovered_grid))

    def log_data(self):
        """Logs the current simulation state to the CSV file."""
        self.log_writer.writerow([
            self.seconds_elapsed,
            self.total_healthy,
            self.total_exposed,
            self.total_infected,
            self.total_recovered,
            self.total_dead
        ])

    def __del__(self):
        """Destructor to ensure the log file is closed."""
        if self.log_file:
            self.log_file.close()

    def __del__(self):
        """Destructor to ensure the log file is closed."""
        if self.log_file:
            self.log_file.close()
