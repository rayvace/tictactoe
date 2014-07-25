from rules import Rules
from ..board.board import Board
import unittest


class TestRules(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.rule = Rules(self.board)

    def test_next_play(self):
        self.assertTrue(True)

    def test_end_game_vertical(self):
        for position in xrange(1, 10, 3):
            self.rule.get_current_player()
            self.board.add_mark('X', position) # 1, 4, 7

        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 6)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'win')

        self.board.reset_board()
        for position in xrange(2, 11, 3):
            self.rule.get_current_player()
            self.board.add_mark('X', position) # 2, 5, 8

        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 3)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'win')

    def test_end_game_horizontal(self):
        for position in xrange(1, 4):
            self.rule.get_current_player()
            self.board.add_mark('O', position)

        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 6)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'win')

    def test_end_game_forward_diaganol(self):
        for position in xrange(3, 9, 2):
            self.rule.get_current_player()
            self.board.add_mark('X', position)
            
        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 6)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'win')

    def test_end_game_reverse_diaganol(self):
        for position in xrange(1, 10, 4):
            self.rule.get_current_player()
            self.board.add_mark('O', position)

        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 6)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'win')

    def test_end_game_draw(self):
        for position in xrange(1, 10):
            self.rule.get_current_player()

        is_end, result = self.rule.end_game(position)

        self.assertEqual(self.rule.remaining_moves, 0)
        self.assertEqual(is_end, True)
        self.assertEqual(result, 'draw')
