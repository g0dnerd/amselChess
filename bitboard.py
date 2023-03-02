import util


def bitboard_to_square_list(bitboard):
    """
    Convert a bitboard to a list of squares.
    """
    squares = []
    while bitboard:
        square_index = bin(bitboard & -bitboard).count('0') - 1
        squares.append(square_index)
        # Clear the least significant bit
        bitboard &= bitboard - 1
    return squares


class BitboardGameState:
    def __init__(self, fen=None):
        if fen is not None:
            # Initialize the board state from a FEN string
            self.init_from_fen(fen)
        else:
            self.white_pawns = 0x000000000000FF00
            self.white_knights = 0x0000000000000042
            self.white_bishops = 0x0000000000000024
            self.white_rooks = 0x0000000000000081
            self.white_queens = 0x0000000000000008
            self.white_king = 0x0000000000000010
            self.black_pawns = 0x00FF000000000000
            self.black_knights = 0x4200000000000000
            self.black_bishops = 0x2400000000000000
            self.black_rooks = 0x8100000000000000
            self.black_queens = 0x0800000000000000
            self.black_king = 0x1000000000000000

        self.empty_squares = ~(self.white_pawns | self.white_knights | self.white_bishops | self.white_rooks |
                               self.white_queens | self.white_king | self.black_pawns | self.black_knights |
                               self.black_bishops | self.black_rooks | self.black_queens | self.black_king)
        self.occupied_squares = ~self.empty_squares

        self.bitboards = {
            'white': {
                'pawns': self.white_pawns,
                'knights': self.white_knights,
                'bishops': self.white_bishops,
                'rooks': self.white_rooks,
                'queens': self.white_queens,
                'king': self.white_king
            },
            'black': {
                'pawns': self.black_pawns,
                'knights': self.black_knights,
                'bishops': self.black_bishops,
                'rooks': self.black_rooks,
                'queens': self.black_queens,
                'king': self.black_king
            }
        }

        self.not_h_file = 0xfefefefefefefefe
        self.not_a_file = 0x7f7f7f7f7f7f7f7f
        self.rank_2 = 0x000000000000ff00
        self.rank_7 = 0x00ff000000000000

        self.en_passant_target = 0

    def init_from_fen(self, fen):
        # Set up the board state from a FEN string
        pass  # TODO: implement

    def get_legal_moves(self, color):
        """
        Generate a bitboard of all legal moves of a given color.
        :param color: str
        :return: bitboard
        """
        # Initialize bitboard for legal moves
        legal_moves = 0

        legal_moves |= self.get_legal_pawn_moves(color)
        legal_moves |= self.get_legal_knight_moves(color)
        legal_moves |= self.get_legal_bishop_moves(color)
        legal_moves |= self.get_legal_rook_moves(color)
        legal_moves |= self.get_legal_queen_moves(color)
        legal_moves |= self.get_legal_king_moves(color)

        return legal_moves

    def get_legal_pawn_moves(self, color):
        # Initialize bitboard for legal moves
        legal_moves = 0
        opponent = util.get_opponent_color(color)
        # Calculate bitboard for all opponent pieces
        opponent_pieces = self.bitboards[opponent]["all"]

        # Get all legal moves for pawns of a given color
        # Calculate bitboard for all pawns
        pawns = self.bitboards[color]['pawns']

        # Calculate bitboard for all forward moves
        if color == "white":
            forward_moves = (pawns << 8) & ~self.occupied_squares
        else:
            forward_moves = (pawns >> 8) & ~self.occupied_squares

        # Calculate bitboard for all captures to the left
        if color == "white":
            captures_left = ((pawns & self.not_a_file) << 7) & opponent_pieces
        else:
            captures_left = ((pawns & self.not_h_file) >> 9) & opponent_pieces

        # Calculate bitboard for all captures to the right
        if color == "white":
            captures_right = ((pawns & self.not_h_file) << 9) & opponent_pieces
        else:
            captures_right = ((pawns & self.not_a_file) >> 7) & opponent_pieces

        # Add forward moves and captures to legal moves
        legal_moves |= forward_moves | captures_left | captures_right

        # Calculate bitboard for all double pawn pushes
        if color == "white":
            double_pushes = ((pawns & self.rank_2) << 16) & ~self.occupied_squares & ~(self.occupied_squares << 8)
        else:
            double_pushes = ((pawns & self.rank_7) >> 16) & ~self.occupied_squares & ~(self.occupied_squares >> 8)

        # Add double pawn pushes to legal moves
        legal_moves |= double_pushes

        # Calculate bitboard for all en passant captures
        if color == "white":
            en_passant_captures = ((pawns & self.not_a_file) << 7) & self.en_passant_target
        else:
            en_passant_captures = ((pawns & self.not_h_file) >> 9) & self.en_passant_target

        # Add en passant captures to legal moves
        legal_moves |= en_passant_captures

    def bitboard_to_move_list(self, bitboard):
        """
        Convert a bitboard to a list of moves.
        :param: bitboard
        :return: list
        """
        # Convert a bitboard to a list of moves
        move_list = []
        # Iterate over each square in the bitboard
        for square in bitboard_to_square_list(bitboard):
            # Add the move to the move list
            moves = self.get_legal_moves(square)
            # Add each move to the move list
            for move in moves:
                move_list.append((square, move))
        return move_list

    def is_legal_move(self, move):
        # Check if a move is legal
        pass  # TODO: implement

    def is_check(self, color):
        # Check if the given color is in check
        pass  # TODO: implement

    def is_checkmate(self, color):
        # Check if the given color is in checkmate
        pass  # TODO: implement

    def is_stalemate(self, color):
        # Check if the given color is in stalemate
        pass  # TODO: implement

    def is_insufficient_material(self):
        # Check if the game is in a draw due to insufficient material
        pass  # TODO: implement

    def is_game_over(self):
        # Check if the game is over (due to checkmate, stalemate, insufficient material, etc.)
        pass  # TODO: implement

    def get_piece_at_square(self, square):
        # Return the piece at the given square
        pass  # TODO: implement

    def get_all_pieces(self, color=None):
        # Return a list of all pieces on the board (optionally filtered by color)
        pass  # TODO: implement

    def get_king_square(self, color):
        # Return the square of the king of the given color
        pass  # TODO: implement

    def make_move(self, move):
        # Make a move and update the board state
        pass  # TODO: implement

    def undo_move(self):
        # Undo the last move and restore the previous board state
        pass  # TODO: implement
