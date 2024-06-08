class Board:
    board: list[list[int]] = []
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        for y in range(height):
            self.board.append([])
            for x in range(width):
                self.board[y].append(0)

    def set_square_value(self, x: int, y: int, value: int) -> None:
        self.board[y][x] = value

    def get_board_value(self, x: int, y: int) -> int:
        return self.board[y][x]

    def print(self) -> None:
        for row in self.board:
            print(row)
