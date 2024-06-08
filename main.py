import copy
import random
from typing import Tuple
import window
import pygame
from pygame.locals import *

from config import *
from board import Board
from answerBoard import AnswerBoard


def input_guess(answer_board: AnswerBoard, shown_board: Board, guess: Tuple[int, int],
                game_started: bool) -> Board:
    """
    reveals squares around input
    :param answer_board:
    :param shown_board:
    :param guess:
    :param game_started:
    :return:
    """
    x = guess[1]
    y = guess[0]
    affected_squares = answer_board.possible_squares_checker(x, y)
    for square in affected_squares:
        relative_x = square[0]
        relative_y = square[1]
        if shown_board.get_board_value(relative_x, relative_y) != 0:
            if ((not game_started and answer_board.get_board_value(relative_x, relative_y) != BOMB)
                    or
                    (game_started and answer_board.get_board_value(x, y) == 0)):
                shown_board.set_square_value(relative_x, relative_y,
                                             answer_board.get_board_value(relative_x, relative_y))
                if shown_board.get_board_value(relative_x, relative_y) == 0:
                    shown_board = input_guess(answer_board, shown_board, (relative_y, relative_x), game_started)
                    if shown_board.get_board_value(relative_x, relative_y) == BOMB:
                        shown_board.set_square_value(x, y, BOMB)
                        break
            elif not game_started and answer_board.get_board_value(relative_x, relative_y) == BOMB:
                shown_board.set_square_value(x, y, BOMB)
                break
    return shown_board


def main():
    # variables that change
    game_state: int = ONGOING
    mine_counter: int = copy.deepcopy(NUM_MINES)
    shown_board: Board = Board(WIDTH, HEIGHT)
    answer_board: AnswerBoard = AnswerBoard(WIDTH, HEIGHT)
    game_started: bool = False
    window.print_board_screen(shown_board, game_state, mine_counter)
    shown_board.print()

    while True:
        window.refresh_screen()
        for event in pygame.event.get():
            if game_state == FAILED:
                continue
            if event.type == QUIT:
                raise SystemExit

            if event.type != MOUSEBUTTONDOWN:  # if they didn't click
                continue

            event_info = event.__dict__
            pos = list(event_info["pos"])
            x_guess = int(round((pos[0] - 20) / 80, 0))
            y_guess = int(round((pos[1] - 20) / 72, 0))
            if shown_board.get_board_value(x_guess, y_guess) not in [BLANK, BOMB]:  # Checks if it can be edited
                print("You already guessed here.")
                continue

            if event_info["button"] == 1:  # if the user thinks there isn't a bomb there
                # creates a new board until 0 is at the point of clicking when starting
                while not game_started and answer_board.get_board_value(x_guess, y_guess) != 0:
                    answer_board: AnswerBoard = AnswerBoard(WIDTH, HEIGHT)
                
                if answer_board.get_board_value(x_guess, y_guess) == BOMB:
                    print("Failed")
                    game_state = FAILED
                    window.print_board_screen(shown_board, game_state, mine_counter)
                    answer_board.print()
                    break

                shown_board = input_guess(answer_board, shown_board, (y_guess, x_guess), game_started)
                shown_board.set_square_value(x_guess, y_guess, answer_board.get_board_value(x_guess, y_guess))
                game_started = True
            elif event_info["button"] == 3:  # if the user thinks there is a bomb there
                if shown_board.get_board_value(x_guess, y_guess) == BOMB:  # removes a bomb
                    shown_board.set_square_value(x_guess, y_guess, BLANK)
                    mine_counter += 1
                elif mine_counter != 0:  # adds a bomb
                    mine_counter -= 1
                    shown_board.set_square_value(x_guess, y_guess, BOMB)

            if shown_board.__eq__(answer_board):
                game_state = WON
            shown_board.print()
            window.print_board_screen(shown_board, game_state, mine_counter)


if __name__ == '__main__':
    main()
