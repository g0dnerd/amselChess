# Tests various methods and classes in the chess engine.
# Creates a board and a game and tests the get_legal_moves method for each piece.
# Upon running this file, the test results will be printed to the console.

import unittest
from board import Board
from game import Game


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.game = Game()

    def test_get_legal_moves_for_white_pawn(self):
        # Test white pawn
        white_pawn = self.board.get_piece_by_coordinates(0, 1)
        # assert that the white pawn on a2 can move to a3 and a4 (there are no other legal moves)
        self.assertCountEqual(white_pawn.get_legal_moves(self.board), [(0, 2), (0, 3)])

    def test_get_legal_moves_for_black_pawn(self):
        # Test black pawn
        black_pawn = self.board.get_piece_by_coordinates(0, 6)
        # assert that the black pawn on a7 can move to a6 and a5 (there are no other legal moves)
        self.assertCountEqual(black_pawn.get_legal_moves(self.board), [(0, 5), (0, 4)])

    def test_get_legal_moves_for_white_knight(self):
        # Test white knight
        white_knight = self.board.get_piece_by_coordinates(1, 0)
        # assert that the white knight on b1 can move to a3 and c3
        # (there are no other legal moves in the initial board state)
        self.assertCountEqual(white_knight.get_legal_moves(self.board), [(0, 2), (2, 2)])

    def test_get_legal_moves_for_black_knight(self):
        # Test black knight
        black_knight = self.board.get_piece_by_coordinates(1, 7)
        # assert that the black knight on b8 can move to a6 and c6
        # (there are no other legal moves in the initial board state)
        self.assertCountEqual(black_knight.get_legal_moves(self.board), [(0, 5), (2, 5)])

    def test_get_legal_moves_for_white_bishop(self):
        # Tests the bishops' legal move on the initial board states (there are none)
        # Test white bishop
        white_bishop = self.board.get_piece_by_coordinates(2, 0)
        # assert that the white bishop on c1 has no legal moves
        self.assertCountEqual(white_bishop.get_legal_moves(self.board), [])

    def test_print_board(self):
        # Tests the print_board method
        print(self.board)


if __name__ == '__main__':
    unittest.main()
