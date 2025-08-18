"""
Handles the rendering of the world map and simulation state.
"""

import pygame
import config
import numpy as np

class Map:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.original_map_image = self._load_map_image()
        self.zoom_level = 1.0
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.update_map_surface()

    def _load_map_image(self):
        """Loads the world map image."""
        try:
            return pygame.image.load(config.WORLD_MAP_IMAGE).convert()
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            print(f"Please ensure '{config.WORLD_MAP_IMAGE}' exists in the 'data' directory.")
            pygame.quit()
            exit()

    def update_map_surface(self):
        """Updates the map surface based on zoom and offset."""
        new_width = int(self.screen_width * self.zoom_level)
        new_height = int(self.screen_height * self.zoom_level)
        self.zoomed_map_image = pygame.transform.scale(self.original_map_image, (new_width, new_height))

    def zoom_in(self):
        """Zooms in the map."""
        self.zoom_level = min(self.zoom_level * 1.1, 10.0)
        self.update_map_surface()

    def zoom_out(self):
        """Zooms out the map."""
        self.zoom_level = max(self.zoom_level / 1.1, 1.0)
        if self.zoom_level == 1.0:
            self.map_offset_x = 0
            self.map_offset_y = 0
        self.update_map_surface()

    def handle_zoom(self, event):
        """Handles zooming with the mouse wheel."""
        if event.y > 0:  # Zoom in
            self.zoom_in()
        else:  # Zoom out
            self.zoom_out()


    def handle_pan(self, rel):
        """Handles panning with mouse drag."""
        if self.zoom_level > 1.0:
            self.map_offset_x += rel[0]
            self.map_offset_y += rel[1]

            # Clamp offsets to keep map on screen
            max_offset_x = self.zoomed_map_image.get_width() - self.screen_width
            max_offset_y = self.zoomed_map_image.get_height() - self.screen_height
            self.map_offset_x = max(-max_offset_x, min(0, self.map_offset_x))
            self.map_offset_y = max(-max_offset_y, min(0, self.map_offset_y))

    def draw(self):
        """Draws the world map on the screen."""
        self.screen.blit(self.zoomed_map_image, (self.map_offset_x, self.map_offset_y))

    def draw_infection(self, simulation_grid):
        """Draws infected areas on the map based on the simulation grid."""
        if self.zoom_level == 1.0:
            for y in range(self.screen_height):
                for x in range(self.screen_width):
                    if simulation_grid[y, x] > 0:
                        self.screen.set_at((x, y), config.RED)
        else:
            # If zoomed, iterate through the map grid and draw scaled circles
            infected_y, infected_x = np.where(simulation_grid > 0)
            for y, x in zip(infected_y, infected_x):
                screen_x = int(x * self.zoom_level + self.map_offset_x)
                screen_y = int(y * self.zoom_level + self.map_offset_y)
                
                # Basic culling to avoid drawing off-screen circles
                radius = int(self.zoom_level)
                if -radius < screen_x < self.screen_width + radius and \
                   -radius < screen_y < self.screen_height + radius:
                    pygame.draw.circle(self.screen, config.RED, (screen_x, screen_y), radius)

    def draw_air_travel(self, air_travel_lines):
        """Draws lines for air travel."""
        for start_pos, end_pos in air_travel_lines:
            # Scale positions based on zoom and offset
            start_x = int(start_pos[0] * self.zoom_level + self.map_offset_x)
            start_y = int(start_pos[1] * self.zoom_level + self.map_offset_y)
            end_x = int(end_pos[0] * self.zoom_level + self.map_offset_x)
            end_y = int(end_pos[1] * self.zoom_level + self.map_offset_y)

            pygame.draw.line(self.screen, config.YELLOW, (start_x, start_y), (end_x, end_y), 1)
