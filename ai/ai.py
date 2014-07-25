import collections


class ArtificialIntelligence(object):

    """
    Using Wikipedia Tic Tac Toe AI strategy

    Referece: 
    http://www.cs.berkeley.edu/~bh/pdf/v1ch06.pdf

    1 | 2 | 3
    ----------
    4 | 5 | 6
    ----------
    7 | 8 | 8

    """
    #bot uses X as default mark
    DEFAULT_MARK = 'X'
    DEFAULT_OPPONENT_MARK = 'O'
    MARK_OPTIONS = ['X', 'O']

    def __init__(self, board):
        if not board:
            raise ValueError
            
        self.board = board
        self.mark = self.DEFAULT_MARK
        self.opponent_mark = self.DEFAULT_OPPONENT_MARK
        self.position = None
        self._clear_cache()

    def _get_opposite_corner(self, last_play):
        if last_play == self.board.TOP_LEFT:
            return self.board.BOTTOM_RIGHT
        if last_play == self.board.BOTTOM_RIGHT:
            return self.board.TOP_LEFT
        elif last_play == self.board.TOP_RIGHT:
            return self.board.BOTTOM_LEFT
        elif last_play == self.board.BOTTOM_LEFT:
            return self.board.TOP_RIGHT

    def set_board(self, board):
        self.board = board

    def set_mark(self, mark):
        if mark not in self.MARK_OPTIONS:
            raise ValueError

        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'

    def next_move(self):
        """
        Return position for next move based on 
        established tic tac toe strategy.

        Reference:
        http://en.wikipedia.org/wiki/Tic-tac-toe
        """
        position = self.random_position()
        if self.winning_move():
            position = self.position
        elif self.blocking_move():
            position = self.position
        elif self.forking_move():
            position = self.position
        elif self.blocking_fork_move():
            position = self.position
        elif self.center_move():
            position = self.position
        elif self.opposite_corner():
            position = self.position
        elif self.empty_corner():
            position = self.position
        elif self.empty_edge():
            position = self.position

        #clear cached combinations
        self._clear_cache()
        return position

    def _clear_cache(self):
        self.cached_singles = {
            self.mark: [],
            self.opponent_mark: []
        }

    def _update_cache(self, row_str, mark, opponent):
        if opponent in row_str:
            return
        self.cached_singles[mark].append(row_str)

    def _end_game(self, mark, opponent):
        """
        Helper for determining whether there is a 
        move that will result in an end game
        """
        
        #short circuit if we're at start of game
        if self.board.total_moves < 2:
            return False

        #check for opportunities to win row
        for x in xrange(0, 3):
            row_str = ''.join(self.board.get_horizontal(x))
            if (row_str.count(mark) < 2) or (opponent in row_str):
                self._update_cache(row_str, mark, opponent)
                continue
            self.position = int(row_str.replace(mark, ''))
            return True

        #check for opportunities to win column
        for y in xrange(0, 3):
            col_str = ''.join(self.board.get_vertical(y))
            if (col_str.count(mark) < 2) or (opponent in col_str):
                self._update_cache(col_str, mark, opponent)
                continue
            self.position = int(col_str.replace(mark, ''))
            return True

        #check for opportunities to win forward diagonal
        f_str = ''.join(self.board.get_forward_diagonal())
        if (f_str.count(mark) > 1) and (opponent not in f_str):
            self.position = int(f_str.replace(mark, ''))
            return True

        self._update_cache(f_str, mark, opponent)

        #check for opportunities to win reverse diagonal
        r_str = ''.join(self.board.get_reverse_diagonal())
        if (r_str.count(mark) > 1) and (opponent not in r_str):
            self.position = int(r_str.replace(mark, ''))
            return True

        self._update_cache(r_str, mark, opponent)
        return False

    def _find_fork(self, mark):
        """
        Helper used to find forks by looking for
        3-in-a-row opportunities that share
        a common cell.

        [4X6 X47 3X7]
        """
        fork_opts = []
        d = collections.defaultdict(int)
        
        fork_check = ''.join(self.cached_singles[mark])
        for fc in fork_check:
            try:
                int(fc)
                d[fc] += 1
                fork_opts.append(int(fc)) if d[fc] > 1 else None
            except ValueError:
                continue

        if len(fork_opts) == 0:
            return None

        return fork_opts

    def _find_double(self, mark):
        """
        Helper used to find opportunities to 
        create 2 in a row.
        """
        double_opts = self.cached_singles[mark]         # e.g., [X23, X47]
        position = double_opts[0].replace(mark, '')[0]  #e.g., 
        
        return int(position)

    def winning_move(self):
        """
        If the bot has two in a row, it can place a third to get 
        three in a row.
        """
        return self._end_game(self.mark, self.opponent_mark)

    def blocking_move(self):
        """
        If the opponent has two in a row, the bot must 
        play the third itself to block the opponent.
        """
        return self._end_game(self.opponent_mark, self.mark)

    def forking_move(self):
        """
        Create an opportunity where the bot has two 
        threats to win (two non-blocked lines of 2).
        """

        #short circuit if less than 4 moves
        if self.board.total_moves < 4:
            return False

        forks = self._find_fork(self.mark)
        if forks:
            self.position = forks[0]
            return True
        return False

    def blocking_fork_move(self):
        """
        Options 1: create two in a row to force the 
        opponent into defending

        Option 2: if opponent can fork, the bot should block
        that fork
        """
        forks = self._find_fork(self.opponent_mark)
        if not forks:
            return False

        double = self._find_double(self.mark)
        if double:
            self.position = double
            return True
        
        self.position = forks[0]
        return True

    def center_move(self):
        """
        The bot marks the center.
        """
        if self.board.is_open(self.board.CENTER):
            self.position = self.board.CENTER
            return True
        return False

    def opposite_corner(self):
        """
        If the opponent is in the corner, the bot plays
        the opposite corner.
        """
        last_play = self.board.last_play
        if last_play in self.board.CORNER:
            self.position = self._get_opposite_corner(last_play)
            return True
        return False

    def empty_corner(self):
        """
        The bot plays in a corner square.
        """
        if self.board.is_open(self.board.TOP_LEFT):
            self.position = self.board.TOP_LEFT
            return True
        elif self.board.is_open(self.board.TOP_RIGHT):
            self.position = self.board.TOP_RIGHT
            return True
        elif self.board.is_open(self.board.BOTTOM_LEFT):
            self.position = self.board.BOTTOM_LEFT
            return True
        elif self.board.is_open(self.board.BOTTOM_RIGHT):
            self.position = self.board.BOTTOM_RIGHT
            return True
        return False

    def empty_edge(self):
        """
        The bot plays in a middle square on any of the 4 edges.
        """
        if self.board.is_open(self.board.TOP_EDGE):
            self.position = self.board.TOP_EDGE
            return True
        elif self.board.is_open(self.board.BOTTOM_EDGE):
            self.position = self.board.BOTTOM_EDGE
            return True
        elif self.board.is_open(self.board.LEFT_EDGE):
            self.position = self.board.LEFT_EDGE
            return True
        elif self.board.is_open(self.board.RIGHT_EDGE):
            self.position = self.board.RIGHT_EDGE
            return True
        return False

    def random_position(self):
        return self.board.random_open_position()
