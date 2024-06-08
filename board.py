class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board: list[list[int]] = []
        for y in range(height):
            self.board.append([])
            for x in range(width):
                self.board[y].append(0)

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        for row1, row2 in zip(self.board, other.board):
            if row1 != row2:
                return False
        return True

    def set_square_value(self, x: int, y: int, value: int) -> None:
        self.board[y][x] = value

    def get_board_value(self, x: int, y: int) -> int:
        return self.board[y][x]

    def print(self) -> None:
        for row in self.board:
            print(row)
