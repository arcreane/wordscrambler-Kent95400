import random
import string
import pygame
import pygame_gui

# This function is used to fetch the words from the liste_francais.txt file, and return a random list of words.
# remove accents, and convert to uppercase
def fetch_words(number_of_words=10):
    # Open the file
    with open('liste_francais.txt', 'r', encoding='utf-8') as file:
        # Read the lines
        lines = file.readlines()

    # Remove accents and convert to uppercase
    words = [line.strip().upper() for line in lines]

    # Return a random selection of words
    return random.sample(words, number_of_words)


def generate_table(x, y, words):
    # Define the directions
    directions = {
        'right': (0, 1),
        'left': (0, -1),
        'up': (-1, 0),
        'down': (1, 0),
        'up-right': (-1, 1),
        'up-left': (-1, -1),
        'down-right': (1, 1),
        'down-left': (1, -1)
    }

    # Create an empty table
    table = [['' for _ in range(y)] for _ in range(x)]

    # Create an empty dictionary to store the positions of the words
    word_positions = {}

    # Place the words in the table
    for word in words:
        placed = False

        while not placed:
            # Choose a random direction for the word
            direction = random.choice(list(directions.keys()))

            # Get the direction values
            dx, dy = directions[direction]

            # Adjust the start position based on the direction
            if dx > 0:  # If the direction is down
                start_x = random.randint(0, x - len(word))
            elif dx < 0:  # If the direction is up
                start_x = random.randint(len(word) - 1, x - 1)
            else:
                start_x = random.randint(0, x - 1)

            if dy > 0:  # If the direction is right
                start_y = random.randint(0, y - len(word))
            elif dy < 0:  # If the direction is left
                start_y = random.randint(len(word) - 1, y - 1)
            else:
                start_y = random.randint(0, y - 1)

            # Check if the word can be placed at the current position
            for i in range(len(word)):
                if table[start_x + dx*i][start_y + dy*i] not in ('', word[i]):
                    break
            else:  # No break, the word can be placed
                placed = True

        # Place the word in the table
        for i in range(len(word)):
            table[start_x + dx*i][start_y + dy*i] = word[i]

        # Store the start position, end position, and direction of the word in word_positions
        word_positions[word] = (start_x, start_y, start_x + dx*(len(word) - 1), start_y + dy*(len(word) - 1), direction)

    # Fill the remaining empty cells with random letters
    for i in range(x):
        for j in range(y):
            if table[i][j] == '':
                table[i][j] = random.choice(string.ascii_uppercase)

    # Convert the table to a string
    table_str = '\n'.join([''.join(row) for row in table])

    return table_str, word_positions


def display_table(table, window, cell_size=35, found_words=None, word_positions=None):
    # Calculate the window size
    table_lines = table.split('\n')

    # Create a font object
    font = pygame.font.Font(None, cell_size)

    # Loop over each cell in the table
    for i, row in enumerate(table_lines):
        for j, letter in enumerate(row):
            # Draw a rectangle for the cell with 40 pixel padding up and left
            pygame.draw.rect(window, (255, 255, 255), (j * cell_size + 40, i * cell_size + 40, cell_size, cell_size))

            # Render the letter
            text = font.render(letter, True, (0, 0, 0))  # Render the letter in black

            # Calculate the position to center the letter in the cell
            text_rect = text.get_rect(center=((j * cell_size + 40) + cell_size // 2, (i * cell_size + 40) + cell_size // 2))

            # Blit the letter onto the window
            window.blit(text, text_rect)

    # Cross out the found words
    if found_words and word_positions:
        for word in found_words:
            if word in word_positions:
                start_x, start_y, end_x, end_y, direction = word_positions[word]
                pygame.draw.line(window, (255, 0, 0), 
                                 ((start_y * cell_size + 40) + cell_size // 2, (start_x * cell_size + 40) + cell_size // 2), 
                                 ((end_y * cell_size + 40) + cell_size // 2, (end_x * cell_size + 40) + cell_size // 2), 5)


def display_words(words, found_words, window, font_size=35, start_x=800):
    # Create a font object
    font = pygame.font.Font(None, font_size)

    # Calculate the start y position
    start_y = 40

    # Calculate the length of the longest word
    max_word_length = max(len(word) for word in words)

    # Set a fixed width for the rectangle based on the length of the longest word
    rect_width = max_word_length * font_size

    # Loop over each word in the words list
    for word in words:
        # Draw a white rectangle behind the word with the fixed width
        pygame.draw.rect(window, (255, 255, 255), (start_x, start_y, rect_width, font_size))

        # Render the word
        text = font.render(word, True, (0, 0, 0))  # Render the word in black

        # Calculate the position to center the text in the rectangle
        text_rect = text.get_rect(center=((start_x + rect_width // 2), start_y + font_size // 2))

        # Blit the text onto the window at the calculated position
        window.blit(text, text_rect)

        # Check if the word is in the found_words list
        if word in found_words:
            # Draw a line through the word
            pygame.draw.line(window, (255, 0, 0), (start_x, start_y + font_size // 2), (start_x + rect_width, start_y + font_size // 2), 2)

        # Move the start y position down
        start_y += font_size

def verify_word(word, x, y, direction, table_str, found_words):
    print('Verifying word:', word, 'at position:', (x, y), 'in direction:', direction, 'in table:', table_str)
    # Define the directions
    directions = {
        'right': (0, 1),
        'left': (0, -1),
        'up': (-1, 0),
        'down': (1, 0),
        'up-right': (-1, 1),
        'up-left': (-1, -1),
        'down-right': (1, 1),
        'down-left': (1, -1)
    }

    x = int(x) - 1
    y = int(y) - 1

    # Get the direction values
    dx, dy = directions[direction]

    # Convert the string representation of the table back into a 2D list
    table = [list(row) for row in table_str.split('\n')]

    # Check if the word goes out of bounds
    if not (0 <= x + dx*(len(word)-1) < len(table) and 0 <= y + dy*(len(word)-1) < len(table[0])):
        print('Word goes out of bounds')
        return found_words

    # Extract the word from the table
    try:
        extracted_word = ''.join([table[x + dx*i][y + dy*i] for i in range(len(word))])
    except IndexError:
        print('Error while extracting word from table')
        return found_words

    # Compare the extracted word with the given word
    if word == extracted_word:
        found_words.append(word)

    return found_words


# This is the main function to launch the game.
def wordsearch_launch(pygame_window, name, difficulty): 
    # Set parameters
    found_words = []
    # Fetch the words from the file
    words = fetch_words()
    print('Words :')
    print(words)


    # Generate the table
    table, word_positions = generate_table(14, 14, words)
    print('Table :')
    print(table)

    print('Word positions :')
    print(word_positions)

    #Set window background to light blue
    pygame_window.fill((37, 150, 190))

    # Display the table
    display_table(table, pygame_window)

    # Display the words
    display_words(words, found_words, pygame_window)

    # Create TextInput-object for user input of word found


    # But more customization possible: Pass your own font object
    font_title = pygame.font.SysFont("Consolas", 35)
    font_title.set_bold(True)

    # Render the title
    title = font_title.render('Enter found word:', True, (0, 0, 0))  # Render the title in black

    uimanager = pygame_gui.UIManager((1280, 720))

    # Label for the word input written in black
    wordfound_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600, 420), (200, 50)), text='Enter found word:', manager=uimanager)
    # Text input for the user found word
    wordfound_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, 470), (200, 50)), manager=uimanager)

    # Label for the row input written in black
    row_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((820, 420), (200, 50)), text='Enter row:', manager=uimanager)
    # Text input for the user row
    row_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((820, 470), (200, 50)), manager=uimanager)

    # Label for the column input written in black
    column_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1040, 420), (200, 50)), text='Enter column:', manager=uimanager)
    # Text input for the user column
    column_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1040, 470), (200, 50)), manager=uimanager)

    # Label for the direction input
    direction_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((860, 520), (200, 50)), text='Enter direction:', manager=uimanager)
    # Dropdown for the user direction
    direction_dropdown = pygame_gui.elements.UIDropDownMenu(['right', 'left', 'up', 'down', 'up-right', 'up-left', 'down-right', 'down-left'], 'right', pygame.Rect((860, 570), (200, 50)), manager=uimanager)

    # Button to verify the word
    verify_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 650), (100, 50)), text='Verify', manager=uimanager)
    # Button to quit the game
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1100, 650), (100, 50)), text='Quit', manager=uimanager)

    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        time_delta = clock.tick(60)/1000.0

        pygame_window.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == verify_button:
                    found_words = verify_word(wordfound_input.get_text(), row_input.get_text(), column_input.get_text(), direction_dropdown.selected_option , table, found_words)
                    print('Found words:', found_words)
                if event.ui_element == quit_button:
                    running = False
                    

            uimanager.process_events(event)
            
        uimanager.update(time_delta)
        

        # Draw the manager
        uimanager.draw_ui(pygame_window)

        # Redraw the table
        display_table(table, pygame_window, found_words=found_words, word_positions=word_positions)
        # Redraw the words list
        display_words(words, found_words, pygame_window)

        pygame.display.update()

    # Return to the main menu (or quit the game) when the loop ends
    pass






