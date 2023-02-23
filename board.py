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

    def get_pieces_by_type(self, piece_type, color):
        """Return a list of all pieces of the given type"""
        pieces = []
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece and piece.type == piece_type and piece.color == color:
                pieces.append(piece)
        return pieces

    def get_pieces_by_type_and_file(self, piece_type, color, file):
        """Return a list of all pieces of the given type and file"""
        pieces = []
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece and piece.type == piece_type and piece.color == color and piece.position[0] == file:
                pieces.append(piece)
        return pieces

    def set_piece(self, square, piece):
        """Set the piece at the given position"""
        self.board[square] = piece

    def remove_piece(self, square):
        """Remove the piece at the given position"""
        self.board[square] = None

    def move_piece(self, start, end):
        """Move the piece from the start position to the end position"""
        piece = self.get_piece_by_square(start)
        captured_piece = self.get_piece_by_square(end)
        self.set_piece(start, None)
        self.set_piece(end, piece)
        piece.move(end)
        # if the move is a promotion
        if piece.type == 'pawn':
            if piece.color == 'white' and end[1] == '8':
                self.promote_pawn(end, 'q', piece.color)
            elif piece.color == 'black' and end[1] == '1':
                self.promote_pawn(end, 'q', piece.color)
        return captured_piece

    def promote_pawn(self, square, target_piece, color):
        self.remove_piece(square)
        x = util.square_to_coordinates(square)[0]
        y = util.square_to_coordinates(square)[1]
        if target_piece == 'q':
            self.board[square] = Queen(color, x, y)

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

    def get_all_piece_positions(self, color):
        """Return a list of all the positions of the pieces of the given color"""
        positions = []
        for square in self.board:
            piece = self.get_piece_by_square(square)
            if piece is not None and piece.color == color:
                positions.append(square)
        return positions

    def get_all_moves(self, player):
        """Return a list of all the legal moves for the given player
        Uses the get_legal_moves() method of the Piece class"""

        moves = []
        for piece in self.get_all_pieces(player.color):
            moves.extend(piece.get_legal_moves(self))
        return moves
