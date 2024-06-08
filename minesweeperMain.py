import copy
import random
from typing import Tuple
import minesweeperWindow
import pygame
from pygame.locals import *
from config import *
from board import Board

# definitions
BOMB = -1
BLANK = -2
WON = 1
ONGOING = 0
FAILED = -1


def possible_squares_checker(x: int, y: int, main_board: list[list[int]]) -> set[Tuple[int, int]]:
    """
    checks which squares around a point can be accessed
    :param x:
    :param y:
    :param main_board:
    :return: returns a set of tuples which can be accessed
    """
    possible_moves: set[Tuple[int, int]] = {(x - 1, y - 1), (x, y - 1),
                                            (x + 1, y - 1), (x - 1, y),
                                            (x + 1, y), (x - 1, y + 1),
                                            (x, y + 1), (x + 1, y + 1)}
    height: int = len(main_board) - 1
    width: int = len(main_board[0]) - 1
    if y == 0:
        possible_moves.discard((x - 1, y - 1))
        possible_moves.discard((x, y - 1))
        possible_moves.discard((x + 1, y - 1))
    elif y == height:
        possible_moves.discard((x + 1, y + 1))
        possible_moves.discard((x, y + 1))
        possible_moves.discard((x - 1, y + 1))
    if x == 0:
        possible_moves.discard((x - 1, y + 1))
        possible_moves.discard((x - 1, y))
        possible_moves.discard((x - 1, y - 1))
    elif x == width:
        possible_moves.discard((x + 1, y + 1))
        possible_moves.discard((x + 1, y - 1))
        possible_moves.discard((x + 1, y))
    return possible_moves


def create_board() -> Tuple[list[Tuple[int, int]], list[list[int]]]:
    """
    creates the answer board, blank board and generates the bombs
    :return: bomb positions, the answer board, the "blank" board the user sees
    """
    answer_board: list[list[int]] = []
    for i in range(Y_LENGTH):
        answer_board.append([])
        for j in range(X_LENGTH):
            answer_board[i].append(0)

    bombs_pos = create_bomb_positions()

    answer_board = add_bombs(answer_board, bombs_pos)

    return bombs_pos, answer_board


def create_bomb_positions() -> list[Tuple[int, int]]:
    """
    adds positions for the number of bombs input
    :return: list of tuples which are the bomb pos
    """
    bombs_pos: list[Tuple[int, int]] = []

    for i in range(NUM_MINES):
        random_pos = (random.randint(0, Y_LENGTH - 1), random.randint(0, X_LENGTH - 1))
        while random_pos in bombs_pos:
            random_pos = (random.randint(0, Y_LENGTH - 1), random.randint(0, X_LENGTH - 1))
        bombs_pos.append(random_pos)
    return bombs_pos


def add_bombs(answer_board: list[list[int]], bombs_pos: list[Tuple[int, int]]) -> list[list[int]]:
    """
    calculates the surrounding values of bombs
    :param answer_board:
    :param bombs_pos:
    :return:
    """
    for location in bombs_pos:
        y = location[0]
        x = location[1]
        squares_to_change = possible_squares_checker(x, y, answer_board)
        for squares in squares_to_change:
            answer_board[squares[1]][squares[0]] += 1
        answer_board[y][x] = BOMB
    return answer_board


def print_board_text(board: list[list[int]]) -> None:
    """
    prints the board to the terminal
    :param board:
    """
    print("\n")
    for row in board:
        for number in row:
            if number == BLANK:
                print(" - ", end="")
            elif number == BOMB:
                print(" B ", end="")
            else:
                print(f" {number} ", end="")
        print("")


def input_guess(answer_board: list[list[int]], shown_board: Board, guess: Tuple[int, int],
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
    affected_squares = possible_squares_checker(x, y, answer_board)
    for square in affected_squares:
        relative_x = square[0]
        relative_y = square[1]
        if shown_board.get_board_value(relative_x, relative_y) != 0:
            if((not game_started and answer_board[relative_y][relative_x] != BOMB)
                or
               (game_started and answer_board[y][x] == 0)):
                shown_board.set_square_value(relative_x, relative_y, answer_board[relative_y][relative_x])
                if shown_board.get_board_value(relative_x, relative_y) == 0:
                    shown_board = input_guess(answer_board, shown_board, (relative_y, relative_x), game_started)
                    if shown_board.get_board_value(relative_x, relative_y) == BOMB:
                        shown_board.set_square_value(x, y, BOMB)
                        break
            elif not game_started and answer_board[relative_y][relative_x] == BOMB:
                shown_board.set_square_value(x, y, BOMB)
                break
    return shown_board


def main():
    # variables that change
    game_state: int = ONGOING
    mine_counter: int = copy.deepcopy(NUM_MINES)
    shown_board: Board = Board(X_LENGTH, Y_LENGTH)
    bombs_pos, answer_board = create_board()
    game_started: bool = False
    minesweeperWindow.print_board_screen(shown_board, game_state, mine_counter)
    shown_board.print()

    while True:
        minesweeperWindow.refresh_screen()
        for event in pygame.event.get():
            if game_state != FAILED:
                if event.type == QUIT:
                    raise SystemExit

                if event.type == MOUSEBUTTONDOWN:
                    event_info = event.__dict__
                    pos = list(event_info["pos"])
                    x_guess = int(round((pos[0] - 20) / 80, 0))
                    y_guess = int(round((pos[1] - 20) / 72, 0))
                    if shown_board.get_board_value(x_guess, y_guess) in [BLANK, BOMB]:  # Checks if it can be edited
                        if event_info["button"] == 1:  # if the user thinks there isn't a bomb there
                            # creates a new board until 0 is at the point of clicking when starting
                            while not game_started and answer_board[y_guess][x_guess] != 0:
                                bombs_pos, answer_board = create_board()
                            if answer_board[y_guess][x_guess] == BOMB:
                                print("Failed")
                                game_state = FAILED
                                minesweeperWindow.print_board_screen(shown_board, game_state, mine_counter)
                                print_board_text(answer_board)
                                break
                            else:
                                shown_board = input_guess(answer_board, shown_board, (y_guess, x_guess), game_started)
                                shown_board.set_square_value(x_guess, y_guess, answer_board[y_guess][x_guess])
                                game_started = True
                        elif event_info["button"] == 3:  # if the user thinks there is a bomb there
                            if shown_board.get_board_value(x_guess, y_guess) == BOMB:  # removes a bomb
                                shown_board.set_square_value(x_guess, y_guess, BLANK)
                                mine_counter += 1
                            elif mine_counter != 0:  # adds a bomb
                                mine_counter -= 1
                                shown_board.set_square_value(x_guess, y_guess, BOMB)
                    else:
                        print("You already guessed here.")
                    if shown_board == answer_board:
                        game_state = WON
                    shown_board.print()
                    minesweeperWindow.print_board_screen(shown_board, game_state, mine_counter)


if __name__ == '__main__':
    main()
