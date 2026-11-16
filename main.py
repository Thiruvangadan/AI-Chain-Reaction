import pygame
import sys
import os
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
red = (231, 76, 60)
violet = (136, 78, 160)
LIGHT_GREEN = (0, 255, 0)

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

# Create a function to draw rounded buttons
def draw_rounded_button(screen, color, x, y, width, height, text, font):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=height//2)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Create a function to check if a point is inside a rectangle
def is_inside(rect, pos):
    x, y, width, height = rect
    px, py = pos
    return x < px < x + width and y < py < y + height

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chain Reaction")

# Create fonts
font = pygame.font.SysFont("Arial", 24)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if is_inside((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50, BUTTON_WIDTH, BUTTON_HEIGHT), mouse_pos):
                pygame.quit()
                subprocess.Popen([sys.executable, "play_with_computer.py"])
                sys.exit()

            elif is_inside((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT), mouse_pos):
                pygame.quit()
                subprocess.Popen([sys.executable, "play_with_friend.py"])
                sys.exit()

                # Fill the screen with white color
    screen.fill(BLACK)

    # Draw labels
    label_font = pygame.font.SysFont("Arial", 46)
    label_text = label_font.render("Chain Reaction", True, WHITE)
    label_rect = label_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(label_text, label_rect)

    # Draw rounded buttons
    draw_rounded_button(screen, red, WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50, BUTTON_WIDTH, BUTTON_HEIGHT, "Play with Computer", font)
    draw_rounded_button(screen, red, WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, "Play with Friend", font)

    # Update the display
    pygame.display.update()
