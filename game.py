# This file contains the 'Game' class, which represents the overall state of a chess game,
# including the current board, the current player, the move history and methods for making moves and
# checking game status.

import copy
from board import Board
from player import Player


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Player('white')
        self.move_history = []
        self.half_move_clock = 0
        self.full_move_number = 1
        self.castling_rights = {
            'white': {
                'K': True,
                'Q': True
            },
            'black': {
                'K': True,
                'Q': True
            }
        }
        self.game_result = None

    def make_move(self, start, end):
        """Make a move on the board and update the game state"""
        # Get the piece at the start position
        piece = self.board.get_piece_by_square(start)
        if piece is None or piece.color != self.current_player.color:
            # If there is no piece at the start position or the piece is not the current player's color,
            # the move is invalid.
            return False
        if end not in piece.get_legal_moves(self.board):
            # If the end position is not in the list of legal moves for the piece, the move is invalid.
            return False
        captured_piece = self.board.move_piece(start, end)
        self.move_history.append((start, end, captured_piece))

        # Update the half move clock
        if captured_piece is not None or piece.piece_type == 'pawn':
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1

        # Update the full move number
        if self.current_player.color == 'black':
            self.full_move_number += 1

        # Update castling rights
        if piece.piece_type == 'king':
            self.castling_rights[piece.color]['K'] = False
            self.castling_rights[piece.color]['Q'] = False
        elif piece.piece_type == 'rook':
            if piece.color == 'white':
                if piece.x == 0:
                    self.castling_rights['white']['Q'] = False
                elif piece.x == 7:
                    self.castling_rights['white']['K'] = False
            else:
                if piece.x == 0:
                    self.castling_rights['black']['Q'] = False
                elif piece.x == 7:
                    self.castling_rights['black']['K'] = False

        # Check for game result
        if self.board.is_in_checkmate(self.current_player.color):
            self.game_result = 'checkmate'
        elif self.board.is_in_stalemate(self.current_player.color):
            self.game_result = 'stalemate'
        elif self.board.is_insufficient_material():
            self.game_result = 'insufficient material'
        elif self.board.is_threefold_repetition():
            self.game_result = 'threefold repetition'
        elif self.board.is_draw_by_fifty_move_rule():
            self.game_result = 'draw by fifty move rule'

        # Switch players
        if self.current_player.color == 'white':
            self.current_player = Player('black')
        else:
            self.current_player = Player('white')
        return True

    def get_current_player(self):
        return self.current_player

    def get_game_result(self):
        return self.game_result

    def get_move_history(self):
        return self.move_history

    def get_legal_moves(self, square):
        """Return a list of legal moves for the piece at the given square"""
        piece = self.board.get_piece_by_square(square)
        if piece is None or piece.color != self.current_player.color:
            return []
        return piece.get_legal_moves(self.board)

    def is_valid_move(self, start, end):
        """Return True if the given move is valid, False otherwise"""
        piece = self.board.get_piece_by_square(start)
        if piece is None or piece.color != self.current_player.color:
            return False
        return end in piece.get_legal_moves(self.board)

    def would_be_check(self, start, end):
        """Return True if the given move would put the current player in check, False otherwise.
        Uses deep copy of the board to avoid changing the actual board state."""

        # Make a deep copy of the board
        board_copy = copy.deepcopy(self.board)

        # Make the move on the copy of the board
        board_copy.move_piece(start, end)

        # Check if the current player is in check
        return board_copy.is_in_check(self.current_player.color)
