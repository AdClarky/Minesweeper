class Board:
    board: list[list[int]] = []

    def __init__(self, width: int, height: int):
        for i in range(width):
            self.board.append([])
            for j in range(height):
                self.board[i].append(0)

    def set_square_value(self, x: int, y: int, value: int) -> None:
        self.board[y][x] = value

    def get_board_value(self, x: int, y: int) -> int:
        return self.board[y][x]

    def print(self):
        for row in self.board:
            print(row)