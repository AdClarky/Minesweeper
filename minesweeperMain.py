import copy
import random
from typing import Tuple
import minesweeperWindow
import pygame
from pygame.locals import *

bombsCoords = 0
mainBoard: list[list[int]] = [[]]
boardToShow = []


# colours
class Colours:
    white = [255, 255, 255]
    red = [255, 0, 0]
    gradient = [[255, 0, 0], [255, 146, 0], [219, 255, 0], [73, 255, 0],
                [0, 255, 73], [0, 255, 219], [0, 146, 255], [0, 0, 255]]
    black = [0, 0, 0]
    blue = [0, 0, 255]
    green = [0, 255, 0]


def possible_squares_checker(x_guess: int, y_guess: int) -> set[Tuple[int, int]]:
    """
    checks which squares around a point can be accessed
    :param x_guess: the position of x
    :param y_guess: the position of y
    :return: returns a set of tuples which can be accessed
    """
    possible_moves: set[Tuple[int, int]] = {(x_guess - 1, y_guess - 1), (x_guess, y_guess - 1),
                                             (x_guess + 1, y_guess - 1), (x_guess - 1, y_guess),
                                             (x_guess + 1, y_guess), (x_guess - 1, y_guess + 1),
                                             (x_guess, y_guess + 1), (x_guess + 1, y_guess + 1)}
    height: int = len(mainBoard) - 1
    width: int = len(mainBoard[0]) - 1
    if y_guess == 0:
        possible_moves.discard((x_guess - 1, y_guess - 1))
        possible_moves.discard((x_guess, y_guess - 1))
        possible_moves.discard((x_guess + 1, y_guess - 1))
    elif y_guess == height:
        possible_moves.discard((x_guess + 1, y_guess + 1))
        possible_moves.discard((x_guess, y_guess + 1))
        possible_moves.discard((x_guess - 1, y_guess + 1))
    if x_guess == 0:
        possible_moves.discard((x_guess - 1, y_guess + 1))
        possible_moves.discard((x_guess - 1, y_guess))
        possible_moves.discard((x_guess - 1, y_guess - 1))
    elif x_guess == width:
        possible_moves.discard((x_guess + 1, y_guess + 1))
        possible_moves.discard((x_guess + 1, y_guess - 1))
        possible_moves.discard((x_guess + 1, y_guess))
    return possible_moves


def create_board(column_size: int,
                 row_size: int,
                 num_of_mines: int) -> Tuple[list[list[int, int]], list[list[int]], list[list[str]]]:
    """
    creates the answer board, blank board and generates the bombs
    :param column_size:
    :param row_size:
    :param num_of_mines:
    :return: bomb positions, the answer board, the "blank" board the user sees
    """
    bomb_pos: list[list[int, int]] = []
    answer_board: list[list[int]] = []
    board_shown: list[list[str]] = []
    for i in range(column_size):
        answer_board.append([])
        board_shown.append([])
        for j in range(row_size):
            answer_board[i].append(0)
            board_shown[i].append("-")
    temp_board = copy.deepcopy(answer_board)
    for i in range(num_of_mines):
        while True:
            random_column = random.randint(0, column_size - 1)
            random_row = random.randint(0, row_size - 1)
            if answer_board[random_column][random_row] != -1:
                break
        bomb_pos.append([random_column, random_row])
        answer_board[random_column][random_row] = -1
    return bomb_pos, temp_board, board_shown


# mainBoard creation, creates a fully completed board
def bombsClose(board_array, bomb_locations):
    for location in bomb_locations:
        y = location[0]
        x = location[1]
        squares_to_change = possible_squares_checker(x, y)
        for squares in squares_to_change:
            board_array[squares[1]][squares[0]] += 1
    for locations in bomb_locations:
        board_array[locations[0]][locations[1]] = "B"


# prints the board in a good-looking way, j = x, i = y
def print_board(board):
    text_size = 30
    minesweeperWindow.background.fill((67, 67, 67))
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            text = board[i][j]
            if failed:
                minesweeperWindow.add_text(text_size, [255, 0, 0], text, j * 80 + 20, i * 72 + 20)
            elif won:
                minesweeperWindow.add_text(text_size, Colours.green, text, j * 80 + 20, i * 72 + 20)
            else:
                if text == 0:
                    minesweeperWindow.add_text(text_size, Colours.white, text, j * 80 + 20, i * 72 + 20)
                elif text == "-":
                    minesweeperWindow.add_text(text_size, Colours.black, text, j * 80 + 20, i * 72 + 20)
                elif text == "B":
                    minesweeperWindow.add_text(text_size, Colours.blue, text, j * 80 + 20, i * 72 + 20)
                else:
                    minesweeperWindow.add_text(text_size, Colours.gradient[text - 1],
                                               text, j * 80 + 20, i * 72 + 20)
    minesweeperWindow.add_text(50, Colours.white, "Number of mines:" + str(mineCount), 1730, 50)


# prints the board in a good-looking way
def print_board_text(board):
    print("\n")
    for row in board:
        print(*row)


# checks the value of surrounding squares, returns the board with the squares filled in
def check_surrounding(board, show_board, guess_pos):
    x = guess_pos[1]
    y = guess_pos[0]
    squares_to_change = possible_squares_checker(x, y)
    for squares in squares_to_change:
        local_row = squares[0]
        local_column = squares[1]
        # line 1: checks if it has already checked the surroundings of the current square
        # line 2: ONLY on the first go, checks its not uncovering a bomb
        # line 3: NOT on the first go, only happens if the central piece is 0
        # in other words: checks if it has already checked this square, makes sure it isn't uncovering a bomb and
        # only works when the central piece is 0
        # inside: sets the show board to the actual value, if the new value is zero it checks the surrounding
        if show_board[local_column][local_row] != 0 and \
                ((mainBoard[local_column][local_row] != "B" and not gameStarted)
                 or (gameStarted and mainBoard[y][x] == 0)):
            show_board[local_column][local_row] = mainBoard[local_column][local_row]
            if show_board[local_column][local_row] == 0:
                check_surrounding(board, show_board, (local_column, local_row))
    return show_board


def board_creation():
    global bombsCoords, mainBoard, boardToShow
    bombsCoords, mainBoard, boardToShow = create_board(yLength, xLength, numMine)
    bombsClose(mainBoard, bombsCoords)


# variables you can change
xLength = 20
yLength = 15

# variables that change
highlightCoords = []
failed = False
won = False
numMine = 70
mineCount = copy.deepcopy(numMine)
board_creation()
gameStarted = False
print_board(boardToShow)
print_board_text(boardToShow)

while True:
    minesweeperWindow.refresh_screen()
    for event in pygame.event.get():
        if not failed:
            if event.type == QUIT:
                raise SystemExit
            if event.type == MOUSEBUTTONDOWN:
                eventInfo = event.__dict__
                pos = list(eventInfo["pos"])
                xGuess = int(round((pos[0] - 20) / 80, 0))
                yGuess = int(round((pos[1] - 20) / 72, 0))
                if boardToShow[yGuess][xGuess] == "-" or "B":
                    if eventInfo["button"] == 1:  # bomb isn't
                        while mainBoard[yGuess][xGuess] != 0 and not gameStarted:
                            board_creation()
                        if mainBoard[yGuess][xGuess] == "B":
                            print("Failed")
                            failed = True
                            print_board(boardToShow)
                            break
                        else:
                            boardToShow = check_surrounding(mainBoard, boardToShow, (yGuess, xGuess))
                            boardToShow[yGuess][xGuess] = mainBoard[yGuess][xGuess]
                            gameStarted = True
                    elif eventInfo["button"] == 3:  # bomb is
                        if boardToShow[yGuess][xGuess] == "B":  # removes a bomb
                            boardToShow[yGuess][xGuess] = "-"
                            mineCount += 1
                        elif mineCount != 0:  # adds a bomb
                            mineCount -= 1
                            boardToShow[yGuess][xGuess] = "B"
                else:
                    print("You already guessed here.")
                if boardToShow == mainBoard:
                    won = True
                print_board_text(boardToShow)
                print_board(boardToShow)
