# Constants representing shift directions
NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1
NORTH_EAST = 9
NORTH_WEST = 7
SOUTH_EAST = -7
SOUTH_WEST = -9
NOT_A_FILE = 0xFEFEFEFEFEFEFEFE
NOT_H_FILE = 0x7F7F7F7F7F7F7F7F
FILE_A = 0x0101010101010101
FILE_H = 0x8080808080808080
RANK_1 = 0x00000000000000FF
RANK_8 = 0xFF00000000000000


def shift_north(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the north.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return bitboard << (NORTH * n)


def shift_south(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the south.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return bitboard >> (SOUTH * n)


def shift_east(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the east.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard << (EAST * n)) & NOT_A_FILE


def shift_west(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the west.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard >> (WEST * n)) & NOT_H_FILE


def shift_ne(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the north-east.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard << (NORTH_EAST * n)) & NOT_A_FILE


def shift_nw(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the north-west.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard << (NORTH_WEST * n)) & NOT_H_FILE


def shift_se(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the south-east.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard >> (SOUTH_EAST * n)) & NOT_A_FILE


def shift_sw(bitboard, n=1):
    """
    Shifts the given bitboard n squares to the south-west.
    :param bitboard: bitboard
    :param n: int
    :return: bitboard
    """
    return (bitboard >> (SOUTH_WEST * n)) & NOT_H_FILE


def diagonal_nw(square):
    """
    Returns a bitboard representing the northwest diagonal that the given square is on.
    :param square: int
    :return: bitboard
    """
    return (FILE_A << (square % 8)) & (RANK_8 >> (7 - (square // 8)))


def diagonal_ne(square):
    """
    Returns a bitboard representing the northeast diagonal that the given square is on.
    :param square: int
    :return: bitboard
    """
    return (FILE_H >> (7 - (square % 8))) & (RANK_8 >> (7 - (square // 8)))


def diagonal_sw(square):
    """
    Returns a bitboard representing the southwest diagonal that the given square is on.
    :param square: int
    :return: bitboard
    """
    return (FILE_A << (square % 8)) & (RANK_1 << (square // 8))


def diagonal_se(square):
    """
    Returns a bitboard representing the southeast diagonal that the given square is on.
    :param square: int
    :return: bitboard
    """
    return (FILE_H >> (7 - (square % 8))) & (RANK_1 << (square // 8))


def get_lsb_index(bitboard):
    """
    Returns the index of the least significant bit.
    :param bitboard: bitboard
    :return: int
    """
    return (bitboard & -bitboard).bit_length() - 1


def get_bitboard_for_square(square):
    """
    Returns a bitboard with only the bit corresponding to the given square set.
    :param square: int
    :return: bitboard
    """
    return 1 << square


def mask_to_moves(mask):
    """
    Returns a bitboard representing all squares that can be reached from a given mask.
    :param mask: bitboard
    :return: list
    """
    moves = 0
    while mask:
        moves |= mask
        mask = (mask - 1) & mask
    return moves
