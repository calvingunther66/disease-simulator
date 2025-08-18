"""
Main application file for the disease simulator.
"""

import pygame
import sys
from map import Map
from simulation import Simulation
from disease import Influenza, COVID19, Measles, Ebola, Smallpox, CommonCold
import config

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Disease Simulator")

# Font for UI
ui_font = pygame.font.Font(None, 36)

# Zoom buttons
zoom_in_button = pygame.Rect(10, 100, 30, 30)
zoom_out_button = pygame.Rect(50, 100, 30, 30)

# Load map and initialize population
world_map = Map(screen, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

# Disease selection
def select_disease():
    font = pygame.font.Font(None, 36)
    diseases = {
        "1": Influenza(),
        "2": COVID19(),
        "3": Measles(),
        "4": Ebola(),
        "5": Smallpox(),
        "6": CommonCold()
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
panning = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            world_map.handle_zoom(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if zoom_in_button.collidepoint(event.pos):
                    world_map.zoom_in()
                elif zoom_out_button.collidepoint(event.pos):
                    world_map.zoom_out()
                elif not infection_started:
                    x, y = event.pos
                    # Adjust coordinates based on zoom and pan
                    map_x = int((x - world_map.map_offset_x) / world_map.zoom_level)
                    map_y = int((y - world_map.map_offset_y) / world_map.zoom_level)
                    if simulation.infect_location(map_x, map_y, radius=5):
                        infection_started = True
            elif event.button == 3: # Right mouse button
                panning = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                panning = False
        elif event.type == pygame.MOUSEMOTION:
            if panning:
                world_map.handle_pan(event.rel)


    # Update simulation (run 60 steps per frame to achieve 1 simulated hour per second)
    if infection_started:
        for _ in range(60):
            simulation.update()

    # Drawing
    screen.fill(config.BLACK) # Clear screen before drawing
    world_map.draw()
    world_map.draw_infection(simulation.simulation_grid)
    world_map.draw_air_travel(simulation.air_travel_lines)

    # Display stats
    font = pygame.font.Font(None, 24)
    
    total_seconds = simulation.seconds_elapsed
    days = total_seconds // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    time_text = f"Day: {days} {hours:02d}:{minutes:02d}:{seconds:02d}"

    healthy_text = f"Healthy: {simulation.total_healthy}"
    exposed_text = f"Exposed: {simulation.total_exposed}"
    stats_text = f"Infected: {simulation.total_infected} | Dead: {simulation.total_dead} | Recovered: {simulation.total_recovered}"
    
    time_surface = font.render(time_text, True, config.GREEN)
    healthy_surface = font.render(healthy_text, True, config.GREEN)
    exposed_surface = font.render(exposed_text, True, config.GREEN)
    stats_surface = font.render(stats_text, True, config.GREEN)
    
    screen.blit(time_surface, (10, 10))
    screen.blit(healthy_surface, (10, 30))
    screen.blit(exposed_surface, (10, 50))
    screen.blit(stats_surface, (10, 70))

    # Draw zoom buttons
    pygame.draw.rect(screen, config.WHITE, zoom_in_button)
    pygame.draw.rect(screen, config.WHITE, zoom_out_button)
    plus_text = ui_font.render("+", True, config.BLACK)
    minus_text = ui_font.render("-", True, config.BLACK)
    screen.blit(plus_text, (zoom_in_button.x + 7, zoom_in_button.y + 2))
    screen.blit(minus_text, (zoom_out_button.x + 9, zoom_out_button.y + 2))


    pygame.display.flip()

pygame.quit()
sys.exit()
