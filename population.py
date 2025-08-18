"""
Handles loading and processing of population data.
"""

import pandas as pd
import numpy as np
import config

class Population:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.population_grid = np.zeros((screen_height, screen_width))
        self._load_population_data()

    def _load_population_data(self):
        """Loads population data from the CSV and populates the grid."""
        df = pd.read_csv(config.POPULATION_DATA)

        # Filter out cities with no population data
        df = df.dropna(subset=['population'])

        for _, row in df.iterrows():
            lat, lon, pop = row['lat'], row['lng'], row['population']
            x, y = self._latlon_to_screen(lat, lon)

            if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                self.population_grid[y, x] += pop

    def _latlon_to_screen(self, lat, lon):
        """Converts latitude and longitude to screen coordinates."""
        # Simple equirectangular projection
        x = int((lon + 180) / 360 * self.screen_width)
        y = int((-lat + 90) / 180 * self.screen_height)
        return x, y

    def get_population(self, x, y):
        """Returns the population at a given screen coordinate."""
        return self.population_grid[y, x]
