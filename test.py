# Tests various methods and classes in the chess engine.
# Creates a board and a game and tests the get_legal_moves method for each piece.
# Upon running this file, the test results will be printed to the console.

import unittest
from game import Game
from gui import PygameGUI
from amsel_engine import Engine
import util


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_util_translations(self):
        # Test the translations in util.py
        self.assertEqual(util.square_to_coordinates("e2"), (4, 6))

    def test_get_legal_moves_for_white_pawn(self):
        # Test white pawn
        white_pawn = self.game.board.get_piece_by_coordinates(4, 6)
        # assert that the white pawn on e2 can move to e3 and e4 (there are no other legal moves)
        # print the legal moves for the white pawn
        expected = [(4, 4), (4, 5)]
        actual = white_pawn.get_legal_moves(self.game.board)
        self.assertCountEqual(expected, actual)

    def test_get_legal_moves_for_black_pawn(self):
        # Test black pawn
        black_pawn = self.game.board.get_piece_by_coordinates(0, 1)
        # assert that the black pawn on a7 can move to a6 and a5 (there are no other legal moves)
        self.assertCountEqual(black_pawn.get_legal_moves(self.game.board), [(0, 2), (0, 3)])

    def test_get_legal_moves_for_white_knight(self):
        # Test white knight
        white_knight = self.game.board.get_piece_by_coordinates(1, 0)
        # assert that the white knight on b1 can move to a3 and c3
        # (there are no other legal moves in the initial board state)
        self.assertCountEqual(white_knight.get_legal_moves(self.game.board), [(0, 2), (2, 2)])

    def test_get_legal_moves_for_black_knight(self):
        # Test black knight
        black_knight = self.game.board.get_piece_by_coordinates(1, 7)
        # assert that the black knight on b8 can move to a6 and c6
        # (there are no other legal moves in the initial board state)
        self.assertCountEqual(black_knight.get_legal_moves(self.game.board), [(0, 5), (2, 5)])

    def test_get_legal_moves_for_white_bishop(self):
        # Tests the bishops' legal move on the initial board states (there are none)
        # Test white bishop
        white_bishop = self.game.board.get_piece_by_coordinates(2, 0)
        # assert that the white bishop on c1 has no legal moves
        self.assertCountEqual(white_bishop.get_legal_moves(self.game.board), [])

    def test_engine(self):
        # Tests the engine
        engine = Engine()
        # print(engine.get_legal_moves())
        print(engine.evaluate_position(self.game))

    def test_gui(self):
        # Tests the GUI
        gui = PygameGUI(self.game)
        gui.run()


if __name__ == '__main__':
    unittest.main()
