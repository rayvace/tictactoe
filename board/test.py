from board import Board
import unittest


class TestBoard(unittest.TestCase):

    """
    1 | 2 | 3
    ----------
    4 | 5 | 6  
    ----------
    7 | 8 | 9

    """

    def setUp(self):
        self.board = Board()

    def test_add_mark(self):
        #position must be a dict
        position = None
        self.assertRaises(TypeError, self.board.add_mark, 'X', position)

        #fail if passed a value that's not X or O
        position = 5
        self.assertRaises(ValueError, self.board.add_mark, 'M', position)

        #fail if x, y passed position greater than 2
        position = 10
        self.assertRaises(ValueError, self.board.add_mark, 'X', position)

        position = 5
        self.board.add_mark('X', position)
        #assert self.board.get_value

    def test_valid_position(self):
        position1 = 5
        position2 = 5
        position3 = 4

        self.board.add_mark('X', position1)
        valid = self.board._is_valid_position(position2)
        self.assertEqual(valid, False)

        valid = self.board._is_valid_position(position3)
        self.assertEqual(valid, True)

    def test_reset_board(self):
        position1 = 5
        position2 = 5

        self.board.add_mark('X', position1)
        valid = self.board._is_valid_position(position2)
        self.assertEqual(valid, False)

        self.board.reset_board()
        valid = self.board._is_valid_position(position2)
        self.assertEqual(valid, True)

    def test_get_horizontal(self):
        position1 = 1
        position2 = 2
        position3 = 3

        """
        
        X | X | X
        ----------
        4 | 5 | 6  
        ----------
        7 | 8 | 9

        """

        self.board.reset_board()
        self.board.add_mark('X', position1)
        self.board.add_mark('X', position2)
        self.board.add_mark('X', position3)

        self.assertEqual(self.board.get_horizontal(0), ['X', 'X', 'X'])

    def test_get_vertical(self):
        position4 = 3
        position5 = 6
        position6 = 9

        """

        1 | 2 | X
        ----------
        4 | 5 | X  
        ----------
        7 | 8 | X
        
        """

        self.board.reset_board()
        self.board.add_mark('X', position4)
        self.board.add_mark('X', position5)
        self.board.add_mark('X', position6)

        #check if other combinations match expected
        self.assertEqual(self.board.get_vertical(2), ['X', 'X', 'X'])
        self.assertEqual(self.board.get_forward_diagonal(), ['X', '5', '7'])
        self.assertEqual(self.board.get_reverse_diagonal(), ['1', '5', 'X'])

    def test_get_reverse_diagonal(self):
        position7 = 1
        position8 = 5
        position9 = 9

        """

        O | 2 | 3
        ----------
        4 | O | 6  
        ----------
        7 | 8 | O
        
        """

        self.board.reset_board()
        self.board.add_mark('O', position7)
        self.board.add_mark('O', position8)
        self.board.add_mark('O', position9)

        self.assertEqual(self.board.get_reverse_diagonal(), ['O', 'O', 'O'])

        #check if other combinations match expected
        self.assertEqual(self.board.get_horizontal(2), ['7', '8', 'O'])
        self.assertEqual(self.board.get_vertical(2), ['3', '6', 'O'])
        self.assertEqual(self.board.get_forward_diagonal(), ['3', 'O', '7'])

    def test_get_forward_diagonal(self):
        position10 = 7
        position11 = 5
        position12 = 3
        """

        1 | 2 | X
        ----------
        4 | X | 6  
        ----------
        X | 8 | 9 
        
        """

        self.board.reset_board()
        self.board.add_mark('X', position10)
        self.board.add_mark('X', position11)
        self.board.add_mark('X', position12)

        self.assertEqual(self.board.get_forward_diagonal(), ['X', 'X', 'X'])

        #check if other combinations match expected
        self.assertEqual(self.board.get_horizontal(1), ['4', 'X', '6'])
        self.assertEqual(self.board.get_vertical(1), ['2', 'X', '8'])
        self.assertEqual(self.board.get_reverse_diagonal(), ['1', 'X', '9'])
