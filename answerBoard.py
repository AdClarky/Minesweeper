import random
from typing import Tuple
from config import *
from board import Board


class AnswerBoard(Board):
    bombs_pos: list[Tuple[int, int]]

    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.create_bomb_positions()
        for coords in self.bombs_pos:
            y = coords[0]
            x = coords[1]
            squares_to_change = self.possible_squares_checker(x, y)
            for square in squares_to_change:
                if square == BOMB:
                    continue
                self.board[square[1]][square[0]] += 1
            self.board[y][x] = BOMB

    def possible_squares_checker(self, x: int, y: int) -> set[Tuple[int, int]]:
        """
        checks which squares around a point can be accessed
        :param x:
        :param y:
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

    def create_bomb_positions(self) -> None:
        """
        adds positions for the number of bombs input
        :return: list of tuples which are the bomb pos
        """
        self.bombs_pos = []

        for i in range(NUM_MINES):
            random_pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            while random_pos in self.bombs_pos:
                random_pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            self.bombs_pos.append(random_pos)
