import pygame
from pygame import FULLSCREEN

from board import Board
from config import *

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



# default
pygame.init()

height = 1080
length = 1920
if FULLSCREEN_BOOL:
    screen = pygame.display.set_mode((length, height), flags=FULLSCREEN)
else:
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


def print_board_screen(board_shown: Board, game_state: int, mine_counter: int) -> None:
    """
    Prints the board shown to the screen
    :param board_shown:
    :param game_state: 0 ongoing, 1 won, -1 lost
    :param mine_counter:
    """
    background.fill((67, 67, 67))

    for y in range(board_shown.height):
        for x in range(board_shown.width):
            text = board_shown.get_board_value(x, y)
            if game_state == FAILED:
                add_text(TEXT_SIZE, Colours.red, text, x * 80 + 20, y * 72 + 20)
            elif game_state == WON:
                add_text(TEXT_SIZE, Colours.green, text, x * 80 + 20, y * 72 + 20)
            else:
                if text == BLANK:
                    add_text(TEXT_SIZE, Colours.black, "-", x * 80 + 20, y * 72 + 20)
                elif text == BOMB:
                    add_text(TEXT_SIZE, Colours.blue, "B", x * 80 + 20, y * 72 + 20)
                else:
                    add_text(TEXT_SIZE, Colours.gradient[int(text)], text, x * 80 + 20, y * 72 + 20)
    add_text(50, Colours.white, "Number of mines:" + str(mine_counter), 1730, 50)


def refresh_screen():
    screen.blit(background, (0, 0))
    pygame.display.flip()
