class BitUtils:
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

    @staticmethod
    def shift_north(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the north.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return bitboard << (BitUtils.NORTH * n)

    @staticmethod
    def shift_south(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the south.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return bitboard >> (BitUtils.SOUTH * n)

    @staticmethod
    def shift_east(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the east.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard << (BitUtils.EAST * n)) & BitUtils.NOT_A_FILE

    @staticmethod
    def shift_west(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the west.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard >> (BitUtils.WEST * n)) & BitUtils.NOT_H_FILE

    @staticmethod
    def shift_ne(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the north-east.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard << (BitUtils.NORTH_EAST * n)) & BitUtils.NOT_A_FILE

    @staticmethod
    def shift_nw(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the north-west.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard << (BitUtils.NORTH_WEST * n)) & BitUtils.NOT_H_FILE

    @staticmethod
    def shift_se(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the south-east.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard >> (BitUtils.SOUTH_EAST * n)) & BitUtils.NOT_A_FILE

    @staticmethod
    def shift_sw(bitboard, n=1):
        """
        Shifts the given bitboard n squares to the south-west.
        :param bitboard: bitboard
        :param n: int
        :return: bitboard
        """
        return (bitboard >> (BitUtils.SOUTH_WEST * n)) & BitUtils.NOT_H_FILE

    @staticmethod
    def get_lsb_index(bitboard):
        """
        Returns the index of the least significant bit.
        :param bitboard: bitboard
        :return: int
        """
        return (bitboard & -bitboard).bit_length() - 1

    @staticmethod
    def get_bitboard_for_square(square):
        """
        Returns a bitboard with only the bit corresponding to the given square set.
        :param square: int
        :return: bitboard
        """
        return 1 << square
