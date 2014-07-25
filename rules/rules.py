import random


class Rules(object):

    """

    1 | 2 | 3
    ----------
    4 | 5 | 6
    ----------
    7 | 8 | 9

    """
    WIN = 'win'
    DRAW = 'draw'

    TOTAL_MOVES = 9
    END_GAME_STRINGS = ['XXX', 'OOO']

    #Helpers
    ROW0 = [1, 2, 3]
    ROW1 = [4, 5, 6]
    ROW2 = [7, 8, 9]

    COL0 = [1, 4, 7]
    COL1 = [2, 5, 8]
    COL2 = [3, 6, 9]

    F_DIAG = [7, 5, 3]
    R_DIAG = [1, 5, 9]

    DEFAULT_START = 'X'
    MARKS = {
        0: 'X',
        1: 'O'
    }

    def __init__(self, board):
        """
        initialize next play
        """
        if not board:
            raise ValueError
            
        self.board = board
        self.next_play = self.DEFAULT_START
        self.remaining_moves = self.TOTAL_MOVES

    def _next(self):
        """
        returns the next player
        """
        current_play = self.next_play
        if current_play == 'X':
            self.next_play = 'O'
        else:
            self.next_play = 'X'

        self.remaining_moves -= 1
        return current_play

    def _get_row(self, last_play):
        if last_play in self.ROW0:
            return 0
        elif last_play in self.ROW1:
            return 1
        else:
            return 2

    def _get_column(self, last_play):
    	if last_play in self.COL0:
            return 0
        elif last_play in self.COL1:
            return 1
        else:
            return 2

    def _is_horizontal_win(self, last_play):
        """
        check if 3 in row horizontally (---)
        """
        row = self._get_row(last_play)
        res = self.board.get_horizontal(row)
        if ''.join(res) in self.END_GAME_STRINGS:
            return True
        return False

    def _is_vertical_win(self, last_play):
        """
        check if 3 in row vertically (|)
        """
        column = self._get_column(last_play)
        res = self.board.get_vertical(column)

        if ''.join(res) in self.END_GAME_STRINGS:
            return True
        return

    def _is_diagnol_win(self, last_play):
        """
        check if 3 in row diagonally (/ or \)
        """
        fdiag = [" ", " ", " "]
        rdiag = [" ", " ", " "]

        if (last_play in self.R_DIAG) and (last_play in self.F_DIAG):
            fdiag = self.board.get_forward_diagonal()
            rdiag = self.board.get_reverse_diagonal()

        elif last_play in self.F_DIAG:
            fdiag = self.board.get_forward_diagonal()

        elif last_play in self.R_DIAG:
            rdiag = self.board.get_reverse_diagonal()

        if ''.join(fdiag) in self.END_GAME_STRINGS or ''.join(rdiag) in self.END_GAME_STRINGS:
            return True

        return False

    def _is_draw(self):
        if self.remaining_moves <= 0:
            return True
        return False

    def random_start(self):
        """
        select starting player at random
        """
        self.next_play = self.MARKS(random.randint(0, 1))

    def set_board(self, board):
        self.board = board

    def get_current_player(self):
        """
        who's move is it?
        """
        return self._next()

    def end_game(self, last_play):
        """
        check for end game conditions where last_play is a number
        between 1 and 9

        passing in last_play ensures we only check for wins along the
        last column, row, and diag (if applicable) played

        http://stackoverflow.com/questions/3311119/determining-three-in-a-row-in-python-2d-array
        """
        #check horizontal win
        if self._is_horizontal_win(last_play):
            return True, self.WIN

        #check vertical win
        if self._is_vertical_win(last_play):
            return True, self.WIN

        #check diagnol win
        if self._is_diagnol_win(last_play):
            return True, self.WIN

        if self._is_draw():
            return True, self.DRAW

        return False, None
