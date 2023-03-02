import util
import bit_utils


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


def get_bishop_mask(square):
    """
    Returns a bitboard representing the squares a bishop on the given square attacks.
    :param square: int
    :return: bitboard
    """
    mask = 0

    # North-East
    for i in range(square, 64, 9):
        if i % 8 == 0:
            break
        mask |= 1 << i
        if i & 7 == 0:
            break

    # South-East
    for i in range(square, 64, 7):
        if i % 8 == 0:
            break
        mask |= 1 << i
        if i & 7 == 7:
            break

    # North-West
    for i in range(square, -1, -7):
        if i % 8 == 7:
            break
        mask |= 1 << i
        if i & 7 == 0:
            break

    # South-West
    for i in range(square, -1, -9):
        if i % 8 == 7:
            break
        mask |= 1 << i
        if i & 7 == 7:
            break

    return mask


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

        # Initialize the en passant target
        self.en_passant_target = 0

        # Define constants for the a and h files and the second and seventh ranks
        self.NOT_A_FILE = 0xfefefefefefefefe
        self.NOT_H_FILE = 0x7f7f7f7f7f7f7f7f
        self.NOT_OFF_BOARD = self.NOT_A_FILE & self.NOT_H_FILE
        self.RANK_2 = 0x000000000000ff00
        self.RANK_7 = 0x00ff000000000000
        self.EMPTY = 0x0000000000000000
        self.EN_PASSANT_LEFT = 0b0000000000000000000000000000000000100000000000000
        self.EN_PASSANT_RIGHT = 0b0000000000000000000000000000000000010000000000000

    def init_from_fen(self, fen):
        # Set up the board state from a FEN string
        pass  # TODO: implement

    def starting_rank(self, color):
        """
        Return the starting rank for a given color.
        :param color:
        :return: bitboard
        """
        if color == 'white':
            return self.RANK_2
        else:
            return self.RANK_7

    def opponent_pieces(self, color):
        """
        Return a bitboard representing the pieces of the opponent of the given color.
        :param color: str
        :return: bitboard
        """
        if color == 'white':
            return self.black_pawns | self.black_knights | self.black_bishops | self.black_rooks | self.black_queens | \
                self.black_king
        else:
            return self.white_pawns | self.white_knights | self.white_bishops | self.white_rooks | self.white_queens | \
                self.white_king

    def get_all_legal_moves(self, color):
        """
        Generate a bitboard of all legal moves of a given color.
        :param color: str
        :return: bitboard
        """
        # Initialize bitboard for legal moves
        legal_moves = 0

        legal_moves |= self.get_all_legal_pawn_moves(color)
        legal_moves |= self.get_all_legal_knight_moves(color)
        legal_moves |= self.get_all_legal_bishop_moves(color)
        legal_moves |= self.get_all_legal_rook_moves(color)
        legal_moves |= self.get_all_legal_queen_moves(color)
        legal_moves |= self.get_all_legal_king_moves(color)

        return legal_moves

    def get_all_legal_pawn_moves(self, color):
        pass
        # TODO: implement

    def get_legal_moves_for_pawn(self, piece_bitboard, color):
        """
        Returns a bitboard representing all legal moves for a pawn piece on the given square, given the occupancy
        of the board and the color of the pawn.
        :param piece_bitboard: bitboard
        :param color: str
        :return: bitboard
        """
        moves = 0

        if color == 'white':
            # Single step forward
            single_step = bit_utils.shift_north(piece_bitboard) & self.empty_squares
            moves |= single_step

            # Double step forward
            double_step = bit_utils.shift_north(single_step) & self.empty_squares & \
                self.starting_rank(color) & bit_utils.shift_north(self.EMPTY)
            moves |= double_step

            # Capture left
            left_capture = bit_utils.shift_nw(piece_bitboard) & self.occupied_squares & \
                self.opponent_pieces(color) & self.NOT_A_FILE
            moves |= left_capture

            # Capture right
            right_capture = bit_utils.shift_ne(piece_bitboard) & self.occupied_squares & \
                self.opponent_pieces(color) & self.NOT_H_FILE
            moves |= right_capture

            # En passant left
            if piece_bitboard in self.EN_PASSANT_LEFT and self.en_passant_target == bit_utils.shift_west(piece_bitboard):
                moves |= bit_utils.shift_nw(piece_bitboard)

            # En passant right
            if piece_bitboard in self.EN_PASSANT_RIGHT and self.en_passant_target == bit_utils.shift_east(piece_bitboard):
                moves |= bit_utils.shift_ne(piece_bitboard)
        else:
            # Single step forward
            single_step = bit_utils.shift_south(piece_bitboard) & self.empty_squares
            moves |= single_step

            # Double step forward
            double_step = bit_utils.shift_south(single_step) & self.empty_squares & \
                self.starting_rank(color) & bit_utils.shift_south(self.EMPTY)
            moves |= double_step

            # Capture left
            left_capture = bit_utils.shift_sw(piece_bitboard) & self.occupied_squares & \
                self.opponent_pieces(color) & self.NOT_A_FILE
            moves |= left_capture

            # Capture right
            right_capture = bit_utils.shift_se(piece_bitboard) & self.occupied_squares & \
                self.opponent_pieces(color) & self.NOT_H_FILE
            moves |= right_capture

            # En passant left
            if piece_bitboard in self.EN_PASSANT_LEFT and self.en_passant_target == bit_utils.shift_west(piece_bitboard):
                moves |= bit_utils.shift_sw(piece_bitboard)

            # En passant right
            if piece_bitboard in self.EN_PASSANT_RIGHT and self.en_passant_target == bit_utils.shift_east(piece_bitboard):
                moves |= bit_utils.shift_se(piece_bitboard)

    def get_legal_moves_for_knight(self, square):
        """
        Returns a bitboard representing all legal moves for a knight piece on the given square, given the occupancy
        of the board and the color of the knight.
        :param square:
        :param color:
        :return: bitboard
        """
        moves = 0

        # Shift north and south 1 rank, then west and east 2 files
        west = bit_utils.shift_west(square)
        east = bit_utils.shift_east(square)
        west2 = bit_utils.shift_west(west)
        east2 = bit_utils.shift_east(east)
        north = bit_utils.shift_north(square)
        south = bit_utils.shift_south(square)
        north2 = bit_utils.shift_north(north)
        south2 = bit_utils.shift_south(south)

        moves |= (bit_utils.shift_nw(west2) | bit_utils.shift_ne(east2) | bit_utils.shift_sw(west2) |
                  bit_utils.shift_se(east2) | bit_utils.shift_nw(north2) | bit_utils.shift_ne(north2) |
                  bit_utils.shift_sw(south2) | bit_utils.shift_se(south2))

        # Remove moves that go off the board or would capture own piece
        moves &= ~self.occupied_squares & self.NOT_OFF_BOARD

        return moves

        def get_legal_moves_for_bishop(self, square):
        """
        Returns a bitboard representing all legal moves for a bishop piece on the given square, given the occupancy
        of the board and the color of the bishop.
        :param square: int
        :return: bitboard
        """
        moves = 0
        bishop_mask = get_bishop_mask(square)

        # diagonal north-west
        nw_moves = bit_utils.mask_to_moves(bit_utils.diagonal_nw(square))
        nw_attacks = nw_moves & self.occupied_squares & bishop_mask
        nw_blockers = self.get_blockers(nw_attacks)
        nw_moves &= ~self.occupied_squares
        nw_moves = self.get_slider_moves(square, nw_blockers)

        # diagonal north-east
        ne_moves = bit_utils.mask_to_moves(bit_utils.diagonal_ne(square))
        ne_attacks = ne_moves & self.occupied_squares & bishop_mask
        ne_blockers = self.get_blockers(ne_attacks)
        ne_moves &= ~self.occupied_squares
        ne_moves = self.get_slider_moves(square, ne_blockers)

        # diagonal south-west
        sw_moves = bit_utils.mask_to_moves(bit_utils.diagonal_sw(square))
        sw_attacks = sw_moves & self.occupied_squares & bishop_mask
        sw_blockers = self.get_blockers(sw_attacks)
        sw_moves &= ~self.occupied_squares
        sw_moves = self.get_slider_moves(square, sw_blockers)

        # diagonal south-east
        se_moves = bit_utils.mask_to_moves(bit_utils.diagonal_se(square))
        se_attacks = se_moves & self.occupied_squares & bishop_mask
        se_blockers = self.get_blockers(se_attacks)
        se_moves &= ~self.occupied_squares
        se_moves = self.get_slider_moves(square, se_blockers)

        moves |= nw_moves | ne_moves | sw_moves | se_moves

        return moves

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
            moves = self.get_legal_moves_for_square(square)
            # Add each move to the move list
            for move in moves:
                move_list.append((square, move))
        return move_list

    def get_legal_moves_for_square(self, square):
        """
        Get all legal moves for the piece on the given square.
        :param square:
        :return: list
        """
        legal_moves = 0
        # Get the piece type and color for the piece on the given square
        piece_type, color = self.get_piece_type_and_color(square)
        # Get the bitboard for the piece on the given square
        piece_bitboard = self.bitboards[color][piece_type]
        # Call the appropriate function to get the legal moves for the piece
        if piece_type == 'pawn':
            legal_moves = self.get_legal_moves_for_pawn(square, piece_bitboard, color)
        elif piece_type == 'knight':
            legal_moves = self.get_legal_moves_for_knight(square, piece_bitboard, color)
        elif piece_type == 'bishop':
            legal_moves = self.get_legal_moves_for_bishop(square, piece_bitboard, color)
        elif piece_type == 'rook':
            legal_moves = self.get_legal_moves_for_rook(square, piece_bitboard, color)
        elif piece_type == 'queen':
            legal_moves = self.get_legal_moves_for_queen(square, piece_bitboard, color)
        elif piece_type == 'king':
            legal_moves = self.get_legal_moves_for_king(square, piece_bitboard, color)
        # Return the list of legal moves
        return bitboard_to_square_list(legal_moves)

    def get_piece_type_and_color(self, square):
        """
        Get the piece type and color for the piece on the given square.
        :param square: int
        :return: tuple
        """
        # Get the bitboard for the given square
        square_bitboard = 1 << square
        # Check if the square is occupied by a white piece
        if self.white_pawns & square_bitboard:
            return 'pawn', 'white'
        elif self.white_knights & square_bitboard:
            return 'knight', 'white'
        elif self.white_bishops & square_bitboard:
            return 'bishop', 'white'
        elif self.white_rooks & square_bitboard:
            return 'rook', 'white'
        elif self.white_queens & square_bitboard:
            return 'queen', 'white'
        elif self.white_king & square_bitboard:
            return 'king', 'white'
        # Check if the square is occupied by a black piece
        elif self.black_pawns & square_bitboard:
            return 'pawn', 'black'
        elif self.black_knights & square_bitboard:
            return 'knight', 'black'
        elif self.black_bishops & square_bitboard:
            return 'bishop', 'black'
        elif self.black_rooks & square_bitboard:
            return 'rook', 'black'
        elif self.black_queens & square_bitboard:
            return 'queen', 'black'
        elif self.black_king & square_bitboard:
            return 'king', 'black'
        # If the square is empty, return None
        else:
            return None, None

    def is_legal_move(self, move):
        # Check if a move is legal
        pass  # TODO: implement

    def is_check(self, color, opponent_attacks):
        """
        Takes in the bitboard for the current game state and the bitboard for all
        possible attacks by the opponent's pieces.
        Returns True if the king of the moving player is in check, and False otherwise.
        :param color: str
        :param opponent_attacks: bitboard
        :return: bool
        """
        # Check if the given color is in check
        return (self.bitboards[color]['king'] & opponent_attacks) != 0

    def get_opponent_attacks_bitboard(self, color):
        """
        Takes in the color of the player whose turn it is, and returns a bitboard
        of all squares that are attacked by the opponent's pieces.
        :param color: str
        :return: bitboard
        """
        # Get the opponent's color
        opponent = util.get_opponent_color(color)
        # Initialize bitboard for opponent attacks
        opponent_attacks = 0
        # Iterate over each piece type
        for piece_type in self.bitboards[opponent]:
            # Get the bitboard for the current piece type
            piece_bitboard = self.bitboards[opponent][piece_type]
            while piece_bitboard:
                square_index = bit_utils.get_lsb_index(piece_bitboard)
                attacks = attack_utils.get_attacks_for_piece(piece_type, square_index, self.occupied_squares)
                opponent_attacks |= attacks
                piece_bitboard ^= bit_utils.get_bitboard_for_square(square_index)
        return opponent_attacks

    def get_slider_moves(self, square, blockers):
        """
        Returns a bitboard representing all sliding moves a piece on the given square can make, given the current
        occupancy of the board.
        :param square: int
        :param blockers: bitboard
        :return: bitboard
        """
        attacks = self.get_ray_attacks(square, mask) & blockers
        moves = bit_utils.mask_to_moves(attacks)
        return moves

    def get_blockers(self, square):
        """
        Returns a bitboard representing all squares occupied by any piece on the board that are blocking a sliding
        piece on the given square from making its moves.
        :param square: int
        :return: bitboard
        """
        mask = get_bishop_mask(square)
        return self.occupied_squares & mask

    def get_ray_attacks(self, square, mask):
        """
        Returns a bitboard representing the sliding attacks along a ray in a given direction from the given square,
        given the occupancy of the board.
        :param square: int
        :param mask: bitboard
        :return: bitboard
        """
        rank_attacks = self.get_rank_attacks(square)
        file_attacks = self.get_file_attacks(square)
        return get_bishop_attacks(square) & mask | rank_attacks & bit_utils.FILE_A | file_attacks & bit_utils.RANK_8

    def get_rank_attacks(self, square, occupied_squares):
        """Return a bitboard representing the squares that a rook on the given square attacks"""
        rank_mask = RANK_MASKS[square // 8]
        occupied = rank_mask & occupied_squares
        left_occ = occupied & FILE_A_CLEAR_MASKS[square % 8]
        right_occ = occupied & FILE_H_CLEAR_MASKS[square % 8]
        left = left_occ << 1
        right = right_occ >> 1
        attacks = left_occ | right_occ | left | right
        return attacks & RANK_MASKS[square // 8]

    def get_file_attacks(self, square, occupied_squares):
        """Return a bitboard representing the squares that a rook on the given square attacks"""
        file_mask = FILE_MASKS[square % 8]
        occupied = file_mask & occupied_squares
        up_occ = occupied << 8
        down_occ = occupied >> 8
        up = get_single_bitboard(up_occ)
        down = get_single_bitboard(down_occ)
        attacks = up_occ | down_occ | up | down
        return attacks & FILE_MASKS[square % 8]


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
