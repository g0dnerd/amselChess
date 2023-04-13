class BitBoard:
    def __init__(self):
        # Initialize empty boards for each piece type and color
        self.white_rooks = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_queens = 0
        self.white_king = 0
        self.white_pawns = 0

        self.black_rooks = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_queens = 0
        self.black_king = 0
        self.black_pawns = 0

        # Place the white pieces on their starting squares
        self.white_rooks |= (1 << 0) | (1 << 7)
        self.white_knights |= (1 << 1) | (1 << 6)
        self.white_bishops |= (1 << 2) | (1 << 5)
        self.white_queens |= (1 << 3)
        self.white_king |= (1 << 4)
        self.white_pawns = (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11) | (1 << 12) | (1 << 13) | (1 << 14) | (1 << 15)

        # Place the black pieces on their starting squares
        self.black_rooks |= (1 << 56) | (1 << 63)
        self.black_knights |= (1 << 57) | (1 << 62)
        self.black_bishops |= (1 << 58) | (1 << 61)
        self.black_queens |= (1 << 59)
        self.black_king |= (1 << 60)
        self.black_pawns = (1 << 48) | (1 << 49) | (1 << 50) | (1 << 51) | (1 << 52) | (1 << 53) | (1 << 54) | (1 << 55)

        # Store both colors in dictionaries
        self.bitboards = {
            'white': {
                'rooks': self.white_rooks,
                'knights': self.white_knights,
                'bishops': self.white_bishops,
                'queens': self.white_queens,
                'king': self.white_king,
                'pawns': self.white_pawns
            },
            'black': {
                'rooks': self.black_rooks,
                'knights': self.black_knights,
                'bishops': self.black_bishops,
                'queens': self.black_queens,
                'king': self.black_king,
                'pawns': self.black_pawns,
            }
        }

        # Initialize an empty en passant target
        self.en_passant_target = 0

        self.empty_squares = ~(self.white_rooks | self.white_knights | self.white_bishops | self.white_queens |
                               self.white_king | self.black_pawns | self.black_rooks | self.black_knights |
                               self.black_bishops | self.black_queens | self.black_king | self.black_pawns)
        self.occupied_squares = ~self.empty_squares

    def print_board(self):
        """
        Prints out a visual representation of the current board state.
        """
        piece_symbols = {
            'rooks': {'white': 'R', 'black': 'r'},
            'knights': {'white': 'N', 'black': 'n'},
            'bishops': {'white': 'B', 'black': 'b'},
            'queens': {'white': 'Q', 'black': 'q'},
            'king': {'white': 'K', 'black': 'k'},
            'pawns': {'white': 'P', 'black': 'p'}
        }

        print("  +-----------------+")
        for rank in range(8, 0, -1):
            rank_str = str(rank) + " | "
            for file in range(1, 9):
                bit = (1 << (8 * (rank - 1) + (file - 1)))
                piece = None
                for color in ['white', 'black']:
                    for piece_type in ['rooks', 'knights', 'bishops', 'queens', 'king', 'pawns']:
                        if self.bitboards[color][piece_type] & bit:
                            piece = piece_symbols[piece_type][color]
                            break
                    if piece is not None:
                        break
                if piece is not None:
                    rank_str += piece
                else:
                    rank_str += "-"
                rank_str += " "
            rank_str += "|"
            print(rank_str)
        print("  +-----------------+")
        print("    a b c d e f g h")
