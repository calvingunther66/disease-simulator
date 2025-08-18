"""
Core simulation logic for disease spread.
"""

import numpy as np
import random
from population import Population
from disease import Disease
import config

class Simulation:
    def __init__(self, screen_width, screen_height, disease: Disease):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.disease = disease
        self.population = Population(screen_width, screen_height)

        # Simulation grid: 0 = susceptible, 1 = infected, 2 = recovered, 3 = dead
        self.simulation_grid = np.zeros((screen_height, screen_width), dtype=int)
        self.infected_counts = np.zeros((screen_height, screen_width), dtype=int)

        self.total_infected = 0
        self.total_dead = 0
        self.total_recovered = 0

    def infect_location(self, x, y):
        """Starts the infection at a specific screen coordinate."""
        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
            if self.simulation_grid[y, x] == 0 and self.population.get_population(x, y) > 0:
                self.simulation_grid[y, x] = 1  # Set to infected
                self.infected_counts[y, x] = 1 # Initial infected count
                self.total_infected += 1
                print(f"Infection started at ({x}, {y})")

    def update(self):
        """Advances the simulation by one step."""
        new_infected_counts = np.copy(self.infected_counts)
        new_simulation_grid = np.copy(self.simulation_grid)

        for y in range(self.screen_height):
            for x in range(self.screen_width):
                if self.simulation_grid[y, x] == 1:  # If currently infected
                    current_infected = self.infected_counts[y, x]
                    if current_infected == 0: # Should not happen if simulation_grid[y,x] is 1
                        continue

                    # Progression: recovery/death
                    if random.random() < self.disease.lethality:
                        new_simulation_grid[y, x] = 3  # Dead
                        self.total_dead += current_infected
                        new_infected_counts[y, x] = 0
                    elif random.random() < self.disease.severity * 0.1: # Simplified recovery chance
                        new_simulation_grid[y, x] = 2  # Recovered
                        self.total_recovered += current_infected
                        new_infected_counts[y, x] = 0
                    else:
                        # Spread to neighbors (land transmission)
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if dx == 0 and dy == 0: continue

                                nx, ny = x + dx, y + dy
                                if 0 <= nx < self.screen_width and 0 <= ny < self.screen_height:
                                    if new_simulation_grid[ny, nx] == 0: # If susceptible
                                        target_population = self.population.get_population(nx, ny)
                                        if target_population > 0:
                                            spread_chance = self.disease.infectivity * self.disease.transmission_land
                                            if random.random() < spread_chance:
                                                new_simulation_grid[ny, nx] = 1
                                                new_infected_counts[ny, nx] += 1 # Infect one person for simplicity
                                                self.total_infected += 1

        # Long-distance transmission (air/sea) - simplified: infect a random high-population city
        if random.random() < self.disease.transmission_air * 0.01: # Small chance for air travel
            # Find a random high-population city to infect
            # This is a very basic implementation. A more advanced one would consider actual flight paths.
            high_pop_cities = np.argwhere(self.population.population_grid > 100000) # Cities with > 100k people
            if len(high_pop_cities) > 0:
                target_y, target_x = random.choice(high_pop_cities)
                if new_simulation_grid[target_y, target_x] == 0:
                    new_simulation_grid[target_y, target_x] = 1
                    new_infected_counts[target_y, target_x] += 1
                    self.total_infected += 1
                    print(f"Air travel infection to ({target_x}, {target_y})")

        self.simulation_grid = new_simulation_grid
        self.infected_counts = new_infected_counts

        print(f"Total Infected: {self.total_infected}, Total Dead: {self.total_dead}, Total Recovered: {self.total_recovered}")
