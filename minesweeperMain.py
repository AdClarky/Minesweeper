import copy
import random
import minesweeperWindow
import pygame
from pygame.locals import *
from colour import Color

# constant variables
bombsCoords = 0
mainBoard = 0
boardToShow = []


# colours
class Colours:
    white = [255, 255, 255]
    red = Color("red")
    gradient = [[255, 0, 0], [255, 146, 0], [219, 255, 0], [73, 255, 0],
                [0, 255, 73], [0, 255, 219], [0, 146, 255], [0, 0, 255]]
    black = [0, 0, 0]
    blue = [0, 0, 255]
    green = [0, 255, 0]


# checks which squares can be checked/placed on, returns the coords of squares around the input square that can be used
def possible_squares_bool_checker(x_guess, y_guess):
    coords = []
    bool_array = [True, True, True, True, True, True, True, True]
    height = len(mainBoard) - 1
    width = len(mainBoard[0]) - 1
    if y_guess == 0:
        bool_array[0] = False
        bool_array[1] = False
        bool_array[2] = False
    elif y_guess == height:
        bool_array[5] = False
        bool_array[6] = False
        bool_array[7] = False
    if x_guess == 0:
        bool_array[0] = False
        bool_array[3] = False
        bool_array[5] = False
    elif x_guess == width:
        bool_array[2] = False
        bool_array[4] = False
        bool_array[7] = False
    for index, possible in enumerate(bool_array):
        if possible:
            local_x = 0
            local_y = 0
            if index == 0:
                local_x = x_guess - 1
                local_y = y_guess - 1
            elif index == 1:
                local_x = x_guess
                local_y = y_guess - 1
            elif index == 2:
                local_x = x_guess + 1
                local_y = y_guess - 1
            elif index == 3:
                local_x = x_guess - 1
                local_y = y_guess
            elif index == 4:
                local_x = x_guess + 1
                local_y = y_guess
            elif index == 5:
                local_x = x_guess - 1
                local_y = y_guess + 1
            elif index == 6:
                local_x = x_guess
                local_y = y_guess + 1
            elif index == 7:
                local_x = x_guess + 1
                local_y = y_guess + 1
            coords.append((local_x, local_y))
    return coords


def createBoard(column_size, row_size, num_of_mines):
    bombs = []
    board = []
    show_board = []
    for i in range(column_size):
        board.append([])
        show_board.append([])
        for j in range(row_size):
            board[i].append(0)
            show_board[i].append("-")
    temp_board = copy.deepcopy(board)
    for i in range(num_of_mines):
        while True:
            randomColumn = random.randint(0, column_size - 1)
            randomRow = random.randint(0, row_size - 1)
            if board[randomColumn][randomRow] != "B":
                break
        bombs.append([randomColumn, randomRow])
        board[randomColumn][randomRow] = "B"
    return bombs, temp_board, show_board


# mainBoard creation, creates a fully completed board
def bombsClose(board_array, bomb_locations):
    for location in bomb_locations:
        # print(location)
        y = location[0]
        x = location[1]
        squares_to_change = possible_squares_bool_checker(x, y)
        for squares in squares_to_change:
            board_array[squares[1]][squares[0]] += 1
    for locations in bomb_locations:
        board_array[locations[0]][locations[1]] = "B"


# prints the board in a good looking way, jindex = x, index = y
def printBoard(board):
    textSize = 30
    minesweeperWindow.background.fill((67, 67, 67))
    for index, row in enumerate(board):
        for jindex, item in enumerate(row):
            text = board[index][jindex]
            if failed:
                minesweeperWindow.add_text(textSize, [255, 0, 0], text, jindex * 80 + 20, index * 72 + 20)
            elif won:
                minesweeperWindow.add_text(textSize, Colours.green, text, jindex * 80 + 20, index * 72 + 20)
            else:
                if text == 0:
                    minesweeperWindow.add_text(textSize, Colours.white, text, jindex * 80 + 20, index * 72 + 20)
                elif text == "-":
                    minesweeperWindow.add_text(textSize, Colours.black, text, jindex * 80 + 20, index * 72 + 20)
                elif text == "B":
                    minesweeperWindow.add_text(textSize, Colours.blue, text, jindex * 80 + 20, index * 72 + 20)
                else:
                    minesweeperWindow.add_text(textSize, Colours.gradient[text - 1],
                                               text, jindex * 80 + 20, index * 72 + 20)
    minesweeperWindow.add_text(50, Colours.white, "Number of mines:" + str(mineCount), 1730, 50)


# prints the board in a good looking way
def print_board_text(board):
    print("\n")
    for row in board:
        print(*row)


# validates and converts an input to an integer, returns an integer
def number_validation(input_message):
    while True:
        try:
            num = int(input(input_message))
            break
        except ValueError:
            print("Please enter a valid number.")
    return num


# checks the value of surrounding squares, returns the board with the squares filled in
def check_surrounding(board, show_board, guess_pos):
    x = guess_pos[1]
    y = guess_pos[0]
    squares_to_change = possible_squares_bool_checker(x, y)
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
    boardCreation = createBoard(yLength, xLength, numMine)
    bombsCoords = boardCreation[0]
    mainBoard = boardCreation[1]
    boardToShow = boardCreation[2]
    bombsClose(mainBoard, bombsCoords)


# variables you can change
xLength = 20
yLength = 15

# variables that change
highlightCoords = []
failed = False
won = False
numMine = int((xLength * yLength) * 0.25)
mineCount = copy.deepcopy(numMine)
board_creation()
gameStarted = False
printBoard(boardToShow)
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
                            printBoard(boardToShow)
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
                printBoard(boardToShow)
