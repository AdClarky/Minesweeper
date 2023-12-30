import pygame
from pygame.locals import *

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# default
pygame.init()

height = 1080
length = 1920
screen = pygame.display.set_mode((length, height), flags=FULLSCREEN)
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


def refresh_screen():
    screen.blit(background, (0, 0))
    pygame.display.flip()
