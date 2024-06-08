# consts
TEXT_SIZE = 30
WIDTH: int = 20
HEIGHT: int = 15
NUM_MINES: int = int((WIDTH * HEIGHT) * 0.20)  # int((X_LENGTH * Y_LENGTH) * 0.25)
FULLSCREEN_BOOL = False

# definitions
BOMB = -1
BLANK = -2
WON = 1
ONGOING = 0
FAILED = -1