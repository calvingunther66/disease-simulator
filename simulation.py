"""
Core simulation logic for disease spread with multiprocessing support.
"""

import numpy as np
import random
import csv
import multiprocessing
from population import Population
from disease import Disease
import config

def update_chunk(args):
    susceptible, exposed, infected, recovered, dead, population, disease, seconds_elapsed = args

    secs_in_day = 24 * 60 * 60
    exposure_rate = disease.infectivity
    infection_rate = 1 / (disease.incubation_period * secs_in_day)
    recovery_rate = (1 - disease.lethality) / (disease.infection_duration * secs_in_day)
    death_rate = disease.lethality / (disease.infection_duration * secs_in_day)

    newly_infected = exposed * infection_rate
    exposed -= newly_infected
    infected += newly_infected

    newly_recovered = infected * recovery_rate
    newly_dead = infected * death_rate
    infected -= (newly_recovered + newly_dead)
    recovered += newly_recovered
    dead += newly_dead

    total_population_grid = susceptible + exposed + infected + recovered
    safe_total_pop = np.where(total_population_grid == 0, 1, total_population_grid)
    infection_pressure = infected / safe_total_pop * exposure_rate
    newly_exposed = susceptible * infection_pressure
    susceptible -= newly_exposed
    exposed += newly_exposed

    return susceptible, exposed, infected, recovered, dead

class Simulation:
    def __init__(self, screen_width, screen_height, disease: Disease):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.disease = disease
        self.population = Population(screen_width, screen_height)

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

        self.num_cores = min(multiprocessing.cpu_count(), 10)  # Use up to 10 cores

        self.log_file = open(config.LOG_FILE, 'w', newline='')
        self.log_writer = csv.writer(self.log_file)
        self.log_writer.writerow(['Second', 'Healthy', 'Exposed', 'Infected', 'Recovered', 'Dead'])

    def infect_location(self, x, y, radius=5):
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
        self.seconds_elapsed += 1

        # Split grids into chunks by rows
        chunk_size = self.screen_height // self.num_cores
        chunks = []
        for i in range(self.num_cores):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < self.num_cores - 1 else self.screen_height
            chunks.append((
                self.susceptible_grid[start:end].copy(),
                self.exposed_grid[start:end].copy(),
                self.infected_grid[start:end].copy(),
                self.recovered_grid[start:end].copy(),
                self.dead_grid[start:end].copy(),
                self.population.population_grid[start:end],
                self.disease,
                self.seconds_elapsed
            ))

        # Parallel update
        with multiprocessing.Pool(self.num_cores) as pool:
            results = pool.map(update_chunk, chunks)
        for i, (sus, exp, inf, rec, dead) in enumerate(results):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < self.num_cores - 1 else self.screen_height
            self.susceptible_grid[start:end] = sus
            self.exposed_grid[start:end] = exp
            self.infected_grid[start:end] = inf
            self.recovered_grid[start:end] = rec
            self.dead_grid[start:end] = dead

        # Handle long-distance transmission (single-threaded for simplicity)
        if self.seconds_elapsed % 3600 == 0:
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
        self.total_healthy = int(np.sum(self.susceptible_grid))
        self.total_exposed = int(np.sum(self.exposed_grid))
        self.total_infected = int(np.sum(self.infected_grid))
        self.total_dead = int(np.sum(self.dead_grid))
        self.total_recovered = int(np.sum(self.recovered_grid))

    def log_data(self):
        self.log_writer.writerow([
            self.seconds_elapsed,
            self.total_healthy,
            self.total_exposed,
            self.total_infected,
            self.total_recovered,
            self.total_dead
        ])

    def __del__(self):
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.close()
