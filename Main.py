import pygame
import pygame_menu
from pygame_menu import Theme
from typing import Tuple, Any

from game import wordsearch_launch

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode((1280, 720))

# Define global variables to store the player's name and difficulty
player_name = 'Player'
difficulty_setting = 1  # Default to easy
menu = None  # Global variable to store the menu

def set_difficulty(value: Tuple[int, Any], difficulty: int):
    global difficulty_setting
    difficulty_setting = difficulty

def set_name(value: str):
    global player_name
    player_name = value

def start_the_game(pygame_window):
    global player_name, difficulty_setting, menu

    # Disable the menu
    menu.disable()

    menu.full_reset()

    # Call the game function with the player's name and difficulty
    wordsearch_launch(pygame_window, player_name, difficulty_setting)

def comeback_to_menu():
    global menu

    # Enable the menu
    menu.enable()

def main_menu():
    global player_name, menu

    theme = pygame_menu.themes.THEME_BLUE

    menu = pygame_menu.Menu('Mots mêlés', 1280, 720,
                            theme=theme,
                            column_max_width=1280)

    menu.add.text_input('Name :', default='Player', onchange=set_name)
    menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game, surface)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    if menu.is_enabled():
        menu.mainloop(surface)

    pygame.display.flip()


if __name__ == '__main__':
    main_menu()

pygame.quit()