"""
Handles the rendering of the world map and simulation state.
"""

import pygame
import config

class Map:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_map_image = self._load_map_image()

    def _load_map_image(self):
        """Loads and scales the world map image."""
        try:
            image = pygame.image.load(config.WORLD_MAP_IMAGE).convert()
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
            return image
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            print(f"Please ensure '{config.WORLD_MAP_IMAGE}' exists in the 'data' directory.")
            pygame.quit()
            exit()

    def draw(self):
        """Draws the world map on the screen."""
        self.screen.blit(self.world_map_image, (0, 0))

    def draw_infection(self, simulation_grid):
        """Draws infected areas on the map based on the simulation grid."""
        # This is a simplified visualization. A more advanced one would use alpha blending
        # or draw circles/rectangles based on infected cell populations.
        for y in range(self.screen_height):
            for x in range(self.screen_width):
                if simulation_grid[y, x] > 0: # Assuming > 0 means infected population
                    # Draw a red pixel for infected areas
                    self.screen.set_at((x, y), config.RED)
