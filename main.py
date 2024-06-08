import copy
import window
import pygame
from pygame.locals import *

from config import *
from board import Board
from answerBoard import AnswerBoard


def main():
    # variables that change
    mine_counter: int = copy.deepcopy(NUM_MINES)
    shown_board: Board = Board(WIDTH, HEIGHT)
    answer_board: AnswerBoard = AnswerBoard(WIDTH, HEIGHT)
    game_started: bool = False
    window.print_board_screen(shown_board, shown_board.lost, mine_counter)

    while True:
        window.refresh_screen()
        for event in pygame.event.get():
            if shown_board.lost:
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
                answer_board.board_input(shown_board, x_guess, y_guess)

            elif event_info["button"] == 3:  # if the user thinks there is a bomb there
                if shown_board.get_board_value(x_guess, y_guess) == BOMB:  # removes a bomb
                    shown_board.set_square_value(x_guess, y_guess, BLANK)
                    mine_counter += 1
                elif mine_counter != 0:  # adds a bomb
                    mine_counter -= 1
                    shown_board.set_square_value(x_guess, y_guess, BOMB)

            if shown_board.__eq__(answer_board):
                print("You have won!")
            window.print_board_screen(shown_board, shown_board.lost, mine_counter)


if __name__ == '__main__':
    main()
