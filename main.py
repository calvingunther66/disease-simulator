"""
Main application file for the disease simulator.
"""

import pygame
import sys
from map import Map
from simulation import Simulation
from disease import Influenza, COVID19, Measles
import config

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Disease Simulator")

# Load map and initialize population
world_map = Map(screen, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

# Disease selection
def select_disease():
    font = pygame.font.Font(None, 36)
    diseases = {
        "1": Influenza(),
        "2": COVID19(),
        "3": Measles()
    }
    selected_disease = None

    while selected_disease is None:
        screen.fill(config.BLACK)
        text = font.render("Select a disease:", True, config.WHITE)
        screen.blit(text, (config.SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        y_offset = 150
        for key, disease_obj in diseases.items():
            text = font.render(f"{key}. {disease_obj.name}", True, config.WHITE)
            screen.blit(text, (config.SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 40

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in diseases:
                    selected_disease = diseases[event.unicode]
    return selected_disease

selected_disease = select_disease()
simulation = Simulation(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, selected_disease)

# Game loop
running = True
clock = pygame.time.Clock()

# State variables
infection_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not infection_started:
                x, y = event.pos
                simulation.infect_location(x, y)
                infection_started = True

    # Update simulation (only if infection has started)
    if infection_started:
        simulation.update()

    # Drawing
    world_map.draw()
    world_map.draw_infection(simulation.simulation_grid)

    # Display stats
    font = pygame.font.Font(None, 24)
    stats_text = f"Infected: {simulation.total_infected} | Dead: {simulation.total_dead} | Recovered: {simulation.total_recovered}"
    text_surface = font.render(stats_text, True, config.WHITE)
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10) # Adjust this value to control simulation speed

pygame.quit()
sys.exit()
