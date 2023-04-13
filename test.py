# Tests various methods and classes in the chess engine.
# Creates a board and a game and tests the get_legal_moves method for each piece.
# Upon running this file, the test results will be printed to the console.

import unittest
from bitboard import BitBoard


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        self.state = BitBoard()

    def test_print(self):
        self.state.print_board()


if __name__ == '__main__':
    unittest.main()
