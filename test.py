# Tests various methods and classes in the chess engine.
# Creates a board and a game and tests the get_legal_moves method for each piece.
# Upon running this file, the test results will be printed to the console.

import unittest
from bitboard import BitboardGameState


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        self.state = BitboardGameState()

    def test_get_legal_moves_pawn(self):
        # Test pawn moves
        move_bb = self.state.get_legal_moves_for_bishop(2)
        move_list = self.state.bitboard_to_move_list(move_bb)
        print(move_list)


if __name__ == '__main__':
    unittest.main()
