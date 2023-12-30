import pygame

# definitions
BOMB = -1
BLANK = -2
WON = 1
ONGOING = 0
FAILED = -1


# colours
class Colours:
    """
    Include basic colours used in the program
    """
    white = [255, 255, 255]
    red = [255, 0, 0]
    gradient = [[255, 255, 255], [255, 0, 0], [255, 146, 0], [219, 255, 0], [73, 255, 0],
                [0, 255, 73], [0, 255, 219], [0, 146, 255], [0, 0, 255]]
    black = [0, 0, 0]
    blue = [0, 0, 255]
    green = [0, 255, 0]


textSize = 30

# default
pygame.init()

height = 1080
length = 1920
# screen = pygame.display.set_mode((length, height), flags=FULLSCREEN)
screen = pygame.display.set_mode((length, height))
pygame.display.set_caption("Minesweeper")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((67, 67, 67))

# next button
button = pygame.Rect(50, 50, 50, 50)


def add_text(font_size, colour, words, x_centre, y_centre):
    words = str(words)
    font = pygame.font.Font(None, font_size)
    text = font.render(words, True, colour)
    text_position = text.get_rect()
    text_position.centerx = x_centre
    text_position.centery = y_centre
    background.blit(text, text_position)


def print_board_screen(board_shown: list[list[int]], game_state: int, mine_counter: int) -> None:
    """
    Prints the board shown to the screen
    :param board_shown:
    :param game_state: 0 ongoing, 1 won, -1 lost
    :param mine_counter:
    """
    background.fill((67, 67, 67))
    for i, row in enumerate(board_shown):
        for j, text in enumerate(row):
            if game_state == FAILED:
                add_text(textSize, Colours.red, text, j * 80 + 20, i * 72 + 20)
            elif game_state == WON:
                add_text(textSize, Colours.green, text, j * 80 + 20, i * 72 + 20)
            else:
                if text == BLANK:
                    add_text(textSize, Colours.black, "-", j * 80 + 20, i * 72 + 20)
                elif text == BOMB:
                    add_text(textSize, Colours.blue, "B", j * 80 + 20, i * 72 + 20)
                else:
                    add_text(textSize, Colours.gradient[int(text)], text, j * 80 + 20, i * 72 + 20)
    add_text(50, Colours.white, "Number of mines:" + str(mine_counter), 1730, 50)


def refresh_screen():
    screen.blit(background, (0, 0))
    pygame.display.flip()
