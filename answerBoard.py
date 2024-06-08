from typing import Tuple

import minesweeperMain
from board import Board


class AnswerBoard(Board):
    def __init__(self, width: int, height: int, bombs: list[Tuple[int, int]]):
        super(width, height)

        for coords in bombs:
            y = coords[0]
            x = coords[1]
            squares_to_change = self.possible_squares_checker(x, y)
            for square in squares_to_change:
                if square == minesweeperMain.BOMB:
                    continue
                self.board[y][x] += 1
            self.board[y][x] = minesweeperMain.BOMB

    def possible_squares_checker(self, x: int, y: int) -> set[Tuple[int, int]]:
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
        if y == 0:
            possible_moves.discard((x - 1, y - 1))
            possible_moves.discard((x, y - 1))
            possible_moves.discard((x + 1, y - 1))
        elif y == self.height:
            possible_moves.discard((x + 1, y + 1))
            possible_moves.discard((x, y + 1))
            possible_moves.discard((x - 1, y + 1))
        if x == 0:
            possible_moves.discard((x - 1, y + 1))
            possible_moves.discard((x - 1, y))
            possible_moves.discard((x - 1, y - 1))
        elif x == self.width:
            possible_moves.discard((x + 1, y + 1))
            possible_moves.discard((x + 1, y - 1))
            possible_moves.discard((x + 1, y))
        return possible_moves
