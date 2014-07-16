from ai import ArtificialIntelligence
from ..rules.rules import Rules
from ..board.board import Board

import unittest


class TestAI(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.rules = Rules()
        self.player = ArtificialIntelligence()

        self.player.set_board(self.board)

    def test_next_winning_move(self):
        """

        X | X | 3
        ----------
        4 | 5 | 6
        ----------
        O | O | 9

        """
        self.board.reset_board()
        play_sequence = [1, 7, 2, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 3)

        """

        1 | X | O
        ----------
        4 | X | 6
        ----------
        O | 8 | 9

        """
        self.board.reset_board()
        play_sequence = [5, 3, 2, 7]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 8)

        """
        
        X | 2 | 3
        ----------
        4 | X | 6
        ----------
        O | O | 9

        """
        self.board.reset_board()
        play_sequence = [5, 7, 1, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 9)

        """
        
        1 | 2 | 3
        ----------
        O | X | 6
        ----------
        X | O | 9

        """
        self.board.reset_board()
        play_sequence = [5, 4, 7, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 3)

    def test_next_blocking_move(self):
        """

        X | X | 3
        ----------
        4 | 5 | 6
        ----------
        O | O | 9

        """
        #Switch AI to play as O
        self.player.set_mark('O')
        
        self.board.reset_board()
        play_sequence = [1, 7, 2, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 9)

        """

        1 | X | O
        ----------
        4 | X | 6
        ----------
        O | 8 | 9

        """
        self.board.reset_board()
        play_sequence = [5, 3, 2, 7]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 8)

        """
        
        X | 2 | 3
        ----------
        4 | X | 6
        ----------
        O | O | 9

        """
        self.board.reset_board()
        play_sequence = [5, 7, 1, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 9)

        """
        
        1 | 2 | 3
        ----------
        O | X | 6
        ----------
        X | O | 9

        """
        self.board.reset_board()
        play_sequence = [5, 4, 7, 8]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 3)

    def test_forking_move(self):
    	"""
        
        X | O | 3
        ----------
        4 | X | 6
        ----------
        7 | 8 | O

        """
        self.board.reset_board()
        play_sequence = [5, 2, 1, 9]

        for i in xrange(0, 4):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 4
        self.assertEqual(self.player.next_move(), 4)

    def test_blocking_fork_move(self):
    	"""
        
        O | 2 | 3
        ----------
        4 | X | 6
        ----------
        7 | 8 | X

        """
        #Switch AI to play as O
        self.player.set_mark('O')

        self.board.reset_board()
        self.player._clear_cache()
        play_sequence = [5, 1, 9]

        for i in xrange(0, 3):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 3
        self.assertEqual(self.player.next_move(), 2)

        """
        
        X | 2 | 3
        ----------
        4 | O | 6
        ----------
        7 | 8 | X

        """
        self.board.reset_board()
        self.player._clear_cache()
        self.rules.next_play = 'X'

        play_sequence = [1, 5, 9]

        for i in xrange(0, 3):
            mark = self.rules.get_current_player()
            self.board.add_mark(mark, play_sequence[i])

        #fake number of total moves played
        self.player.total_moves = 3
        self.assertEqual(self.player.next_move(), 4)

    def test_center_move(self):
    	"""
    	
    	1 | 2 | 3
	    ----------
	    4 | 5 | 6
	    ----------
	    7 | 8 | 8
    	
    	"""
    	self.assertEqual(self.player.next_move(), 5)

    	"""
    	
    	X | 2 | 3
	    ----------
	    4 | 5 | 6
	    ----------
	    7 | 8 | 8
    	
    	"""
    	#Switch AI to play as O
        self.player.set_mark('O')
    	self.board.reset_board()
        self.player._clear_cache()
        self.rules.next_play = 'X'

    	mark = self.rules.get_current_player()
        self.board.add_mark(mark, 1)
        self.assertEqual(self.player.next_move(), 5)

    def test_opposite_corner(self):
    	return

    def test_empty_corner(self):
    	"""
    	
    	1 | 2 | 3
	    ----------
	    4 | O | 6
	    ----------
	    7 | 8 | 9
    	
    	"""
    	self.rules.next_play = 'O'
    	mark = self.rules.get_current_player()

    	self.board.add_mark(mark, 5)
    	self.assertEqual(self.player.next_move(), 1)


    def test_empty_side(self):
    	return
