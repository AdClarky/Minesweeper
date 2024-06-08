import copy
import window
import pygame
from pygame.locals import *

from config import *
from board import Board
from answerBoard import AnswerBoard


def input_guess(answer_board: AnswerBoard, shown_board: Board, x: int, y: int) -> None:
    shown_board.set_square_value(x, y, answer_board.get_board_value(x, y))
    if answer_board.get_board_value(x, y) != 0:  # if the square clicked we can just display it
        return

    # if the square clicked is a 0 we need to display the surrounding squares too
    affected_squares = answer_board.possible_squares_checker(x, y)
    for square in affected_squares:
        relative_x = square[0]
        relative_y = square[1]
        if shown_board.get_board_value(relative_x, relative_y) != -2:  # skip if the position has been checked already
            continue
        input_guess(answer_board, shown_board, relative_x, relative_y)


def main():
    # variables that change
    game_state: int = ONGOING
    mine_counter: int = copy.deepcopy(NUM_MINES)
    shown_board: Board = Board(WIDTH, HEIGHT)
    answer_board: AnswerBoard = AnswerBoard(WIDTH, HEIGHT)
    game_started: bool = False
    window.print_board_screen(shown_board, game_state, mine_counter)

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
                while (not game_started) and answer_board.get_board_value(x_guess, y_guess) != 0:
                    answer_board: AnswerBoard = AnswerBoard(WIDTH, HEIGHT)
                game_started = True
                if answer_board.get_board_value(x_guess, y_guess) == BOMB:
                    print("Failed")
                    game_state = FAILED
                    window.print_board_screen(shown_board, game_state, mine_counter)
                    break

                input_guess(answer_board, shown_board, x_guess, y_guess)
            elif event_info["button"] == 3:  # if the user thinks there is a bomb there
                if shown_board.get_board_value(x_guess, y_guess) == BOMB:  # removes a bomb
                    shown_board.set_square_value(x_guess, y_guess, BLANK)
                    mine_counter += 1
                elif mine_counter != 0:  # adds a bomb
                    mine_counter -= 1
                    shown_board.set_square_value(x_guess, y_guess, BOMB)

            if shown_board.__eq__(answer_board):
                game_state = WON
            window.print_board_screen(shown_board, game_state, mine_counter)


if __name__ == '__main__':
    main()
