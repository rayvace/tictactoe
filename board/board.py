class Board(object):

    """
    Board represented with numbers 1-9 and mapped to
    x, y coordinates:

    1 | 2 | 3
    ----------
    4 | 5 | 6  
    ----------
    7 | 8 | 9

    where:

    0, 0 is top left
    2, 2 is bottom right

    Referece:
    http://en.wikipedia.org/wiki/Tic-tac-toe
    http://www.cs.berkeley.edu/~bh/pdf/v1ch06.pdf

    """
    ALLOWED_MARKS = ['X', 'O']

    TOP_LEFT = 1         # TL
    TOP_EDGE = 2         # TE
    TOP_RIGHT = 3        # TR
    LEFT_EDGE = 4        # LE
    CENTER = 5           # CP
    RIGHT_EDGE = 6       # RE
    BOTTOM_LEFT = 7      # BL
    BOTTOM_EDGE = 8      # BE
    BOTTOM_RIGHT = 9     # BR

    CORNER = [1, 3, 7, 9]

    # looks cryptic, but simple helper used for array slicing
    HORIZONTAL_GROUP = [0, 3, 6]
    VERTICAL_GROUP = [0, 1, 2]

    BOARD_MAPPING = [
        TOP_LEFT,
        TOP_EDGE,
        TOP_RIGHT,
        LEFT_EDGE,
        CENTER,
        RIGHT_EDGE,
        BOTTOM_LEFT,
        BOTTOM_EDGE,
        BOTTOM_RIGHT
    ]

    def __init__(self):
        """
        initialize board
        http://stackoverflow.com/questions/19517374/pythonic-way-to-print-a-chess-board-in-console
        """
        self.grid = [str(x) for x in xrange(1, 10)]
        self.last_play = None
        self.total_moves = 0

    def _is_valid_position(self, position):
        """
        position should be of type dict, have x, y keys
        and values between 0 and 2

        """
        if type(position) is not int:
            raise TypeError

        if position > 9 or position < 1:
            raise ValueError

        #confirm position is open
        try:
            int(self.grid[position - 1])
        except ValueError:
            return False

        return True

    def reset_board(self):
        """
        clear the board
        """
        self.grid = [str(x) for x in xrange(1, 10)]

    def add_mark(self, mark, position):
        """
        add X or O to board based on position

        """
        if mark not in self.ALLOWED_MARKS:
            raise ValueError

        valid = self._is_valid_position(position)
        if not valid:
            return False

        self.grid[position - 1] = mark
        self.last_play = position
        self.total_moves += 1
        
        return True

    def get_horizontal(self, row):
        """
        return values along a specified row

        i.e., row = 0, return [1, 2, 3]

        """
        start = self.HORIZONTAL_GROUP[row]
        end = start + 3
        return self.grid[start:end]

    def get_vertical(self, column):
        """
        return values along a specified column

        i.e., column = 0, return [1, 4, 7]

        """
        start = self.VERTICAL_GROUP[column]
        end = start + 10
        step = 3

        return self.grid[start:end:step] # array[start:end:step]

    def get_forward_diagonal(self):
        """
        return values along the forward diagnol (/)

        given:

        1 | 2 | O
        ----------
        4 | O | 6
        ----------
        X | 8 | 9

        return:

        ['O', 'O', 'X']

        """
        start = 2
        end = 7
        step = 2

        return self.grid[start:end:step] # array[start:end:step]

    def get_reverse_diagonal(self):
        """
        return values along the reverse diagnol (\)

        given:

        X | 2 | 3
        ----------
        4 | O | 6
        ----------
        7 | 8 | 9

        return:

        ['X', 'O', '9']

        """
        start = 0
        end = 9
        step = 4

        return self.grid[start:end:step] # array[start:end:step]

    def is_open(self, position):
        try:
            int(self.grid[position - 1])
        except ValueError:
            return False

        return True

    def random_open_position(self):
        grid_str = ''.join(self.grid)
        openings = grid_str.replace('X', '').replace('O', '')
        return int(openings[0])
