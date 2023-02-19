# This file contains the Board class, which represents the state of the chess board,
# including the positions of the pieces and methods for moving pieces, checking for valid moves
# and checking game status (e.g., checkmate, stalemate).

from piece import *


class Board:
    def __init__(self):
        # Initialize the board as an empty dictionary
        self.board = {"a1": Rook("white", 0, 7), "b1": Knight("white", 1, 7), "c1": Bishop("white", 2, 7),
                      "d1": Queen("white", 3, 7), "e1": King("white", 4, 7), "f1": Bishop("white", 5, 7),
                      "g1": Knight("white", 6, 7), "h1": Rook("white", 7, 7),
                      "a8": Rook("black", 0, 0), "b8": Knight("black", 1, 0), "c8": Bishop("black", 2, 0),
                      "d8": Queen("black", 3, 0), "e8": King("black", 4, 0), "f8": Bishop("black", 5, 0),
                      "g8": Knight("black", 6, 0), "h8": Rook("black", 7, 0)}
        # Add the pieces to the board using the squares they start on as keys
        for i in range(8):
            self.board[f"{chr(ord('a') + i)}2"] = Pawn("white", i, 6)
        for i in range(8):
            self.board[f"{chr(ord('a') + i)}7"] = Pawn("black", i, 1)
        # Add the empty squares to the board
        for y in range(2, 6):
            for x in range(8):
                self.board[f"{chr(ord('a') + x)}{y + 1}"] = None

    def __str__(self):
        """Return a string representation of the board.
        Because the board is represented as a dictionary, we have to print it in a specific order.
        The board is printed from the white player's perspective."""

        # Create a list of the squares on the board
        rows = []
        # Iterate over the squares from a1 to h8
        for y in range(8):
            row = []
            for x in range(8):
                row.append(f"{chr(ord('h') - x)}{8 - y}")
            rows.append(row)
        # Create a string representation of the board
        ranks = ['']
        for row in rows:
            rank = []
            for square in row:
                piece = self.get_piece_by_square(square)
                if piece:
                    rank.append(piece.letter)
                else:
                    rank.append('-')
            ranks.append(' | '.join(rank))
        return '\n'.join(ranks)

    def get_piece_by_square(self, square):
        """Return the piece at the given position"""
        return self.board[square]

    def get_piece_by_coordinates(self, x, y):
        """Return the piece at the given position"""
        square = util.coordinates_to_square(x, y)
        return self.get_piece_by_square(square)

    def set_piece(self, square, piece):
        """Set the piece at the given position"""
        self.board[square] = piece

    def move_piece(self, start, end):
        """Move the piece from the start position to the end position"""
        piece = self.get_piece_by_square(start)
        captured_piece = self.get_piece_by_square(end)
        self.set_piece(start, None)
        self.set_piece(end, piece)
        piece.move(end)
        return captured_piece

    def is_in_check(self, color):
        """Return True if the given player is in check, False otherwise"""
        # Get the king's position
        king_position = self.get_king_position(color)
        # Get the opponent's pieces
        opponent_pieces = self.get_all_pieces(util.get_opponent_color(color))
        # Check if any of the opponent's pieces can move to the king's position
        for piece in opponent_pieces:
            if self.is_legal_move(piece, king_position[0], king_position[1]):
                return True
        return False

    def is_legal_move(self, piece, x, y):
        """Uses the get_legal_moves() method of the Piece class to
        check if the given move is legal for the given piece"""
        return (x, y) in piece.get_legal_moves(self)

    def get_king_position(self, color):
        """Return the position of the given player's king"""
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece is not None and piece.color == color and piece.type == 'king':
                return piece.position

    def get_all_pieces(self, color):
        """Return a list of all the pieces of the given color"""
        pieces = []
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece is not None and piece.color == color:
                pieces.append(piece)
        return pieces

    def get_all_moves(self, player):
        """Return a list of all the legal moves for the given player
        Uses the get_legal_moves() method of the Piece class"""

        moves = []
        for piece in self.get_all_pieces(player.color):
            moves.extend(piece.get_legal_moves(self))
        return moves

    def is_in_checkmate(self, player):
        """Return True if the given player is in checkmate, False otherwise"""
        # Check if the player is in check
        if not self.is_in_check(player):
            return False
        # Check if the player has any legal moves
        if len(self.get_all_moves(player)) > 0:
            return False
        return True

    def is_in_stalemate(self, player):
        """Return True if the game is in stalemate, False otherwise"""
        # Check if the player is in check
        if self.is_in_check(player):
            return False
        # Check if the player has any legal moves
        if len(self.get_all_moves(player)) > 0:
            return False
        return True

    def is_insufficient_material(self):
        """Return True if the game is in a draw due to insufficient material, False otherwise"""
        # Check if the board has any pawns, queens, rooks or bishops
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece is not None and piece.type in ['pawn', 'queen', 'rook', 'bishop']:
                return False
        # Check if there are only two knights
        num_knights = 0
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece is not None and piece.type == 'knight':
                num_knights += 1
        if num_knights > 2:
            return False
        return True

    def is_threefold_repetition(self):
        """Return True if the game is in a draw due to threefold repetition, False otherwise"""
        # TODO
        return False

    def is_draw_by_fifty_move_rule(self):
        """Return True if the game is in a draw due to the fifty move rule, False otherwise"""
        # TODO
        return False

    def is_in_bounds(self, position):
        """Return True if the given position is on the board, False otherwise"""
        x, y = position
        return 0 <= x <= 7 and 0 <= y <= 7

