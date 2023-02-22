# This file contains the Piece class, which is the base class for all chess pieces.
# It contains methods for getting and setting the piece's position and color.
# The file also contains the King, Queen, Rook, Bishop, Knight and Pawn classes,
# which inherit from Piece and implement the get_legal_moves method.

import util


class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.position = (x, y)
        self.square = util.coordinates_to_square(x, y)
        self.moved = False
        self.defending_pieces = []

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
        self.square = util.coordinates_to_square(position[0], position[1])
        self.moved = True

    def move(self, square):
        self.position = util.square_to_coordinates(square)
        self.square = square
        self.moved = True

    def get_legal_moves(self, board):
        # this method should be overridden by subclasses
        raise NotImplementedError

    # def is_legal_move(self, board, target_x, target_y):
    #     target_coordinates = (target_x, target_y)
    #     if target_coordinates in self.get_legal_moves(board):
    #         return True
    #     else:
    #         return False


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # add the piece type attribute
        self.type = 'pawn'
        # add the piece value attribute
        self.value = 1
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'P'
        else:
            self.letter = 'p'
        # add the en passant flag
        self.en_passant = False

    def get_legal_moves(self, board):
        # Checks for legal moves for a pawn. Considers the following cases: 1. Pawn has not moved yet (can move 1 or
        # 2 squares) 2. Pawn has moved (can only move 1 square) 3. Pawn can capture a piece diagonally 4. Pawn can
        # capture a piece en passant 5. Move is not legal if it puts the king in check To check squares on the board,
        # we use the get_piece_by_coordinates method of the Board class. For usage of this method, a1 is (0, 7),
        # h1 is (7, 7), a8 is (0, 0) and h8 is (7, 0). This means that moving up the board is decreasing the y
        # coordinate and moving right is increasing the x coordinate.

        # get the position of the pawn
        x, y = self.position
        # get the color of the pawn
        color = self.color
        # initialize the list of legal moves
        moves = []
        # if the pawn is white
        if color == 'white':
            # if the pawn has not moved yet
            if not self.moved:
                # if the square in front of the pawn is empty
                if board.get_piece_by_coordinates(x, y - 1) is None:
                    # add the square in front of the pawn to the list of legal moves
                    moves.append((x, y - 1))
                    # if the square two squares in front of the pawn is empty
                    if board.get_piece_by_coordinates(x, y - 2) is None:
                        # add the square two squares in front of the pawn to the list of legal moves
                        moves.append((x, y - 2))
            # if the pawn has moved
            else:
                # if the square in front of the pawn is empty
                if board.get_piece_by_coordinates(x, y - 1) is None:
                    # add the square in front of the pawn to the list of legal moves
                    moves.append((x, y - 1))
            # if the pawn can capture a piece diagonally to the right
            if x + 1 < 8 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 1, y - 1) is not None and \
                        board.get_piece_by_coordinates(x + 1, y - 1).color == 'black':
                    moves.append((x + 1, y - 1))
                elif board.get_piece_by_coordinates(x + 1, y - 1) is not None and \
                        board.get_piece_by_coordinates(x + 1, y - 1).color == 'white':
                    self.defending_pieces.append((x + 1, y - 1))
            # if the pawn can capture a piece diagonally to the left
            if x - 1 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y - 1) is not None and \
                        board.get_piece_by_coordinates(x - 1, y - 1).color == 'black':
                    moves.append((x - 1, y - 1))
                elif board.get_piece_by_coordinates(x - 1, y - 1) is not None and \
                        board.get_piece_by_coordinates(x - 1, y - 1).color == 'white':
                    self.defending_pieces.append((x - 1, y - 1))
            # if the pawn can capture a piece en passant to the right
            if x + 1 < 8 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 1, y) is not None and \
                        board.get_piece_by_coordinates(x + 1, y).color == 'black' and \
                        board.get_piece_by_coordinates(x + 1, y).type == 'pawn' and \
                        board.get_piece_by_coordinates(x + 1, y).moved and \
                        board.get_piece_by_coordinates(x + 1, y).position[1] == 3:
                    moves.append((x + 1, y - 1))
            # if the pawn can capture a piece en passant to the left
            if x - 1 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y) is not None and \
                        board.get_piece_by_coordinates(x - 1, y).color == 'black' and \
                        board.get_piece_by_coordinates(x - 1, y).type == 'pawn' and \
                        board.get_piece_by_coordinates(x - 1, y).moved and \
                        board.get_piece_by_coordinates(x - 1, y).position[1] == 3:
                    moves.append((x - 1, y - 1))
        # if the pawn is black
        else:
            # if the pawn has not moved yet
            if not self.moved:
                # if the square in front of the pawn is empty
                if board.get_piece_by_coordinates(x, y + 1) is None:
                    # add the square in front of the pawn to the list of legal moves
                    moves.append((x, y + 1))
                    # if the square two squares in front of the pawn is empty
                    if board.get_piece_by_coordinates(x, y + 2) is None:
                        # add the square two squares in front of the pawn to the list of legal moves
                        moves.append((x, y + 2))
            # if the pawn has moved
            else:
                # if the square in front of the pawn is empty
                if board.get_piece_by_coordinates(x, y + 1) is None:
                    # add the square in front of the pawn to the list of legal moves
                    moves.append((x, y + 1))
            # if the pawn can capture a piece diagonally to the right
            if x + 1 < 8 and y + 1 < 8:
                if board.get_piece_by_coordinates(x + 1, y + 1) is not None and \
                        board.get_piece_by_coordinates(x + 1, y + 1).color == 'white':
                    moves.append((x + 1, y + 1))
                elif board.get_piece_by_coordinates(x + 1, y + 1) is not None and \
                        board.get_piece_by_coordinates(x + 1, y + 1).color == 'black':
                    self.defending_pieces.append((x + 1, y + 1))
            # if the pawn can capture a piece diagonally to the left
            if x - 1 >= 0 and y + 1 < 8:
                if board.get_piece_by_coordinates(x - 1, y + 1) is not None and \
                        board.get_piece_by_coordinates(x - 1, y + 1).color == 'white':
                    moves.append((x - 1, y + 1))
                elif board.get_piece_by_coordinates(x - 1, y + 1) is not None and \
                        board.get_piece_by_coordinates(x - 1, y + 1).color == 'black':
                    self.defending_pieces.append((x - 1, y + 1))
            # if the pawn can capture a piece en passant to the right
            if x + 1 < 8 and y + 1 < 8:
                if board.get_piece_by_coordinates(x + 1, y) is not None and \
                        board.get_piece_by_coordinates(x + 1, y).color == 'white' and \
                        board.get_piece_by_coordinates(x + 1, y).type == 'pawn' and \
                        board.get_piece_by_coordinates(x + 1, y).moved and \
                        board.get_piece_by_coordinates(x + 1, y).position[1] == 4:
                    moves.append((x + 1, y + 1))
            # if the pawn can capture a piece en passant to the left
            if x - 1 >= 0 and y + 1 < 8:
                if board.get_piece_by_coordinates(x - 1, y) is not None and \
                        board.get_piece_by_coordinates(x - 1, y).color == 'white' and \
                        board.get_piece_by_coordinates(x - 1, y).type == 'pawn' and \
                        board.get_piece_by_coordinates(x - 1, y).moved and \
                        board.get_piece_by_coordinates(x - 1, y).position[1] == 4:
                    moves.append((x - 1, y + 1))
        # return the list of legal moves
        return moves


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # add the piece type attribute
        self.type = 'knight'
        # add the piece value attribute
        self.value = 3
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'N'
        else:
            self.letter = 'n'

    def get_legal_moves(self, board):
        # get the position of the knight
        x, y = self.position
        # get the color of the knight
        color = self.color
        # initialize the list of legal moves
        moves = []
        # if the knight is white
        if color == 'white':
            # if the knight can move up and to the right
            if x + 1 < 8 and y - 2 >= 0:
                if board.get_piece_by_coordinates(x + 1, y - 2) is None or \
                        board.get_piece_by_coordinates(x + 1, y - 2).color == 'black':
                    moves.append((x + 1, y - 2))
                elif board.get_piece_by_coordinates(x + 1, y - 2).color == 'white':
                    self.defending_pieces.append((x + 1, y - 2))
            # if the knight can move up and to the left
            if x - 1 >= 0 and y - 2 >= 0:
                if board.get_piece_by_coordinates(x - 1, y - 2) is None or \
                        board.get_piece_by_coordinates(x - 1, y - 2).color == 'black':
                    moves.append((x - 1, y - 2))
                elif board.get_piece_by_coordinates(x - 1, y - 2).color == 'white':
                    self.defending_pieces.append((x - 1, y - 2))
            # if the knight can move down and to the right
            if x + 1 < 8 and y + 2 < 8:
                if board.get_piece_by_coordinates(x + 1, y + 2) is None or \
                        board.get_piece_by_coordinates(x + 1, y + 2).color == 'black':
                    moves.append((x + 1, y + 2))
                elif board.get_piece_by_coordinates(x + 1, y + 2).color == 'white':
                    self.defending_pieces.append((x + 1, y + 2))
            # if the knight can move down and to the left
            if x - 1 >= 0 and y + 2 < 8:
                if board.get_piece_by_coordinates(x - 1, y + 2) is None or \
                        board.get_piece_by_coordinates(x - 1, y + 2).color == 'black':
                    moves.append((x - 1, y + 2))
                elif board.get_piece_by_coordinates(x - 1, y + 2).color == 'white':
                    self.defending_pieces.append((x - 1, y + 2))
            # if the knight can move to the right and up
            if x + 2 < 8 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 2, y - 1) is None or \
                        board.get_piece_by_coordinates(x + 2, y - 1).color == 'black':
                    moves.append((x + 2, y - 1))
                elif board.get_piece_by_coordinates(x + 2, y - 1).color == 'white':
                    self.defending_pieces.append((x + 2, y - 1))
            # if the knight can move to the right and down
            if x + 2 < 8 and y + 1 < 8:
                if board.get_piece_by_coordinates(x + 2, y + 1) is None or \
                        board.get_piece_by_coordinates(x + 2, y + 1).color == 'black':
                    moves.append((x + 2, y + 1))
                elif board.get_piece_by_coordinates(x + 2, y + 1).color == 'white':
                    self.defending_pieces.append((x + 2, y + 1))
            # if the knight can move to the left and up
            if x - 2 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 2, y - 1) is None or \
                        board.get_piece_by_coordinates(x - 2, y - 1).color == 'black':
                    moves.append((x - 2, y - 1))
                elif board.get_piece_by_coordinates(x - 2, y - 1).color == 'white':
                    self.defending_pieces.append((x - 2, y - 1))
            # if the knight can move to the left and down
            if x - 2 >= 0 and y + 1 < 8:
                if board.get_piece_by_coordinates(x - 2, y + 1) is None or \
                        board.get_piece_by_coordinates(x - 2, y + 1).color == 'black':
                    moves.append((x - 2, y + 1))
                elif board.get_piece_by_coordinates(x - 2, y + 1).color == 'white':
                    self.defending_pieces.append((x - 2, y + 1))
        # if the knight is black
        else:
            # if the knight can move up and to the right
            if x + 1 < 8 and y - 2 >= 0:
                if board.get_piece_by_coordinates(x + 1, y - 2) is None or \
                        board.get_piece_by_coordinates(x + 1, y - 2).color == 'white':
                    moves.append((x + 1, y - 2))
                elif board.get_piece_by_coordinates(x + 1, y - 2).color == 'black':
                    self.defending_pieces.append((x + 1, y - 2))
            # if the knight can move up and to the left
            if x - 1 >= 0 and y - 2 >= 0:
                if board.get_piece_by_coordinates(x - 1, y - 2) is None or \
                        board.get_piece_by_coordinates(x - 1, y - 2).color == 'white':
                    moves.append((x - 1, y - 2))
                elif board.get_piece_by_coordinates(x - 1, y - 2).color == 'black':
                    self.defending_pieces.append((x - 1, y - 2))
            # if the knight can move down and to the right
            if x + 1 < 8 and y + 2 < 8:
                if board.get_piece_by_coordinates(x + 1, y + 2) is None or \
                        board.get_piece_by_coordinates(x + 1, y + 2).color == 'white':
                    moves.append((x + 1, y + 2))
                elif board.get_piece_by_coordinates(x + 1, y + 2).color == 'black':
                    self.defending_pieces.append((x + 1, y + 2))
            # if the knight can move down and to the left
            if x - 1 >= 0 and y + 2 < 8:
                if board.get_piece_by_coordinates(x - 1, y + 2) is None or \
                        board.get_piece_by_coordinates(x - 1, y + 2).color == 'white':
                    moves.append((x - 1, y + 2))
                elif board.get_piece_by_coordinates(x - 1, y + 2).color == 'black':
                    self.defending_pieces.append((x - 1, y + 2))
            # if the knight can move to the right and up
            if x + 2 < 8 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 2, y - 1) is None or \
                        board.get_piece_by_coordinates(x + 2, y - 1).color == 'white':
                    moves.append((x + 2, y - 1))
                elif board.get_piece_by_coordinates(x + 2, y - 1).color == 'black':
                    self.defending_pieces.append((x + 2, y - 1))
            # if the knight can move to the right and down
            if x + 2 < 8 and y + 1 < 8:
                if board.get_piece_by_coordinates(x + 2, y + 1) is None or \
                        board.get_piece_by_coordinates(x + 2, y + 1).color == 'white':
                    moves.append((x + 2, y + 1))
                elif board.get_piece_by_coordinates(x + 2, y + 1).color == 'black':
                    self.defending_pieces.append((x + 2, y + 1))
            # if the knight can move to the left and up
            if x - 2 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 2, y - 1) is None or \
                        board.get_piece_by_coordinates(x - 2, y - 1).color == 'white':
                    moves.append((x - 2, y - 1))
                elif board.get_piece_by_coordinates(x - 2, y - 1).color == 'black':
                    self.defending_pieces.append((x - 2, y - 1))
            # if the knight can move to the left and down
            if x - 2 >= 0 and y + 1 < 8:
                if board.get_piece_by_coordinates(x - 2, y + 1) is None or \
                        board.get_piece_by_coordinates(x - 2, y + 1).color == 'white':
                    moves.append((x - 2, y + 1))
                elif board.get_piece_by_coordinates(x - 2, y + 1).color == 'black':
                    self.defending_pieces.append((x - 2, y + 1))

        return moves


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        # add the piece type attribute
        self.type = 'bishop'
        # add the piece value attribute
        self.value = 3
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'B'
        else:
            self.letter = 'b'

    def get_legal_moves(self, board):
        # get the position of the bishop
        x, y = self.position
        # get the color of the bishop
        color = self.color
        # initialize the list of legal moves
        moves = []
        # if the bishop is white
        if color == 'white':
            # if the bishop can move down and to the left
            for i in range(1, 8):
                if x + i < 8 and y + i < 8:
                    if board.get_piece_by_coordinates(x + i, y + i) is None:
                        moves.append((x + i, y + i))
                    elif board.get_piece_by_coordinates(x + i, y + i).color == 'black':
                        moves.append((x + i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y + i))
                        break
                else:
                    break
            # if the bishop can move down and to the right
            for i in range(1, 8):
                if x - i >= 0 and y + i < 8:
                    if board.get_piece_by_coordinates(x - i, y + i) is None:
                        moves.append((x - i, y + i))
                    elif board.get_piece_by_coordinates(x - i, y + i).color == 'black':
                        moves.append((x - i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y + i))
                        break
                else:
                    break
            # if the bishop can move up and to the right
            for i in range(1, 8):
                if x + i < 8 and y - i >= 0:
                    if board.get_piece_by_coordinates(x + i, y - i) is None:
                        moves.append((x + i, y - i))
                    elif board.get_piece_by_coordinates(x + i, y - i).color == 'black':
                        moves.append((x + i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y - i))
                        break
                else:
                    break
            # if the bishop can move up and to the left
            for i in range(1, 8):
                if x - i >= 0 and y - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y - i) is None:
                        moves.append((x - i, y - i))
                    elif board.get_piece_by_coordinates(x - i, y - i).color == 'black':
                        moves.append((x - i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y - i))
                        break
                else:
                    break
        # if the bishop is black
        else:
            # if the bishop can move down and to the left
            for i in range(1, 8):
                if x + i < 8 and y + i < 8:
                    if board.get_piece_by_coordinates(x + i, y + i) is None:
                        moves.append((x + i, y + i))
                    elif board.get_piece_by_coordinates(x + i, y + i).color == 'white':
                        moves.append((x + i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y + i))
                        break
                else:
                    break
            # if the bishop can move down and to the right
            for i in range(1, 8):
                if x - i >= 0 and y + i < 8:
                    if board.get_piece_by_coordinates(x - i, y + i) is None:
                        moves.append((x - i, y + i))
                    elif board.get_piece_by_coordinates(x - i, y + i).color == 'white':
                        moves.append((x - i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y + i))
                        break
                else:
                    break
            # if the bishop can move up and to the right
            for i in range(1, 8):
                if x + i < 8 and y - i >= 0:
                    if board.get_piece_by_coordinates(x + i, y - i) is None:
                        moves.append((x + i, y - i))
                    elif board.get_piece_by_coordinates(x + i, y - i).color == 'white':
                        moves.append((x + i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y - i))
                        break
                else:
                    break
            # if the bishop can move up and to the left
            for i in range(1, 8):
                if x - i >= 0 and y - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y - i) is None:
                        moves.append((x - i, y - i))
                    elif board.get_piece_by_coordinates(x - i, y - i).color == 'white':
                        moves.append((x - i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y - i))
                        break
                else:
                    break

        return moves


class Rook(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'rook'
        # add the piece value attribute
        self.value = 5
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'R'
        else:
            self.letter = 'r'

    def get_legal_moves(self, board):

        x, y = self.position
        color = self.color
        moves = []
        # if the rook is white
        if color == 'white':
            # if the rook can move up
            for i in range(1, 8):
                if y - i >= 0:
                    if board.get_piece_by_coordinates(x, y - i) is None:
                        moves.append((x, y - i))
                    elif board.get_piece_by_coordinates(x, y - i).color == 'black':
                        moves.append((x, y - i))
                        break
                    else:
                        self.defending_pieces.append((x, y - i))
                        break
                else:
                    self.defending_pieces.append((x, y - i))
            # if the rook can move down
            for i in range(1, 8):
                if y + i <= 7:
                    if board.get_piece_by_coordinates(x, y + i) is None:
                        moves.append((x, y + i))
                    elif board.get_piece_by_coordinates(x, y + i).color == 'black':
                        moves.append((x, y + i))
                        break
                    else:
                        self.defending_pieces.append((x, y + i))
                        break
                else:
                    break
            # if the rook can move to the left
            for i in range(1, 8):
                if x - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y) is None:
                        moves.append((x - i, y))
                    elif board.get_piece_by_coordinates(x - i, y).color == 'black':
                        moves.append((x - i, y))
                        break
                    else:
                        self.defending_pieces.append((x - i, y))
                        break
                else:
                    break
            # if the rook can move to the right
            for i in range(1, 8):
                if x + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y) is None:
                        moves.append((x + i, y))
                    elif board.get_piece_by_coordinates(x + i, y).color == 'black':
                        moves.append((x + i, y))
                        break
                    else:
                        self.defending_pieces.append((x + i, y))
                        break
                else:
                    break
        # if the rook is black
        else:
            # if the rook can move up
            for i in range(1, 8):
                if y - i >= 0:
                    if board.get_piece_by_coordinates(x, y - i) is None:
                        moves.append((x, y - i))
                    elif board.get_piece_by_coordinates(x, y - i).color == 'white':
                        moves.append((x, y - i))
                        break
                    else:
                        self.defending_pieces.append((x, y - i))
                        break
                else:
                    break
            # if the rook can move down
            for i in range(1, 8):
                if y + i <= 7:
                    if board.get_piece_by_coordinates(x, y + i) is None:
                        moves.append((x, y + i))
                    elif board.get_piece_by_coordinates(x, y + i).color == 'white':
                        moves.append((x, y + i))
                        break
                    else:
                        self.defending_pieces.append((x, y + i))
                        break
                else:
                    break
            # if the rook can move to the left
            for i in range(1, 8):
                if x - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y) is None:
                        moves.append((x - i, y))
                    elif board.get_piece_by_coordinates(x - i, y).color == 'white':
                        moves.append((x - i, y))
                        break
                    else:
                        self.defending_pieces.append((x - i, y))
                        break
                else:
                    break
            # if the rook can move to the right
            for i in range(1, 8):
                if x + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y) is None:
                        moves.append((x + i, y))
                    elif board.get_piece_by_coordinates(x + i, y).color == 'white':
                        moves.append((x + i, y))
                        break
                    else:
                        self.defending_pieces.append((x + i, y))
                        break
                else:
                    break

        return moves


class Queen(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'queen'
        # add the piece value attribute
        self.value = 9
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'Q'
        else:
            self.letter = 'q'

    def get_legal_moves(self, board):

        x, y = self.position
        color = self.color
        moves = []
        # if the queen is white
        if color == 'white':
            # if the queen can move up
            for i in range(1, 8):
                # if the path up is clear
                if y - i >= 0:
                    if board.get_piece_by_coordinates(x, y - i) is None:
                        moves.append((x, y - i))
                    elif board.get_piece_by_coordinates(x, y - i).color == 'black':
                        moves.append((x, y - i))
                        break
                    else:
                        self.defending_pieces.append((x, y - i))
                        break
                else:
                    break
            # if the queen can move down
            for i in range(1, 8):
                if y + i <= 7:
                    if board.get_piece_by_coordinates(x, y + i) is None:
                        moves.append((x, y + i))
                    elif board.get_piece_by_coordinates(x, y + i).color == 'black':
                        moves.append((x, y + i))
                        break
                    else:
                        self.defending_pieces.append((x, y + i))
                        break
                else:
                    break
            # if the queen can move to the left
            for i in range(1, 8):
                if x - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y) is None:
                        moves.append((x - i, y))
                    elif board.get_piece_by_coordinates(x - i, y).color == 'black':
                        moves.append((x - i, y))
                        break
                    else:
                        self.defending_pieces.append((x - i, y))
                        break
                else:
                    break
            # if the queen can move to the right
            for i in range(1, 8):
                if x + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y) is None:
                        moves.append((x + i, y))
                    elif board.get_piece_by_coordinates(x + i, y).color == 'black':
                        moves.append((x + i, y))
                        break
                    else:
                        self.defending_pieces.append((x + i, y))
                        break
                else:
                    break
            # if the queen can move up and to the left
            for i in range(1, 8):
                if x - i >= 0 and y - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y - i) is None:
                        moves.append((x - i, y - i))
                    elif board.get_piece_by_coordinates(x - i, y - i).color == 'black':
                        moves.append((x - i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y - i))
                        break
                else:
                    break
            # if the queen can move up and to the right
            for i in range(1, 8):
                if x + i <= 7 and y - i >= 0:
                    if board.get_piece_by_coordinates(x + i, y - i) is None:
                        moves.append((x + i, y - i))
                    elif board.get_piece_by_coordinates(x + i, y - i).color == 'black':
                        moves.append((x + i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y - i))
                        break
                else:
                    break
            # if the queen can move down and to the left
            for i in range(1, 8):
                if x - i >= 0 and y + i <= 7:
                    if board.get_piece_by_coordinates(x - i, y + i) is None:
                        moves.append((x - i, y + i))
                    elif board.get_piece_by_coordinates(x - i, y + i).color == 'black':
                        moves.append((x - i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y + i))
                        break
                else:
                    break
            # if the queen can move down and to the right
            for i in range(1, 8):
                if x + i <= 7 and y + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y + i) is None:
                        moves.append((x + i, y + i))
                    elif board.get_piece_by_coordinates(x + i, y + i).color == 'black':
                        moves.append((x + i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y + i))
                        break
                else:
                    break
        # if the queen is black
        else:
            # if the queen can move up
            for i in range(1, 8):
                if y - i >= 0:
                    if board.get_piece_by_coordinates(x, y - i) is None:
                        moves.append((x, y - i))
                    elif board.get_piece_by_coordinates(x, y - i).color == 'white':
                        moves.append((x, y - i))
                        break
                    else:
                        self.defending_pieces.append((x, y - i))
                        break
                else:
                    break
            # if the queen can move down
            for i in range(1, 8):
                if y + i <= 7:
                    if board.get_piece_by_coordinates(x, y + i) is None:
                        moves.append((x, y + i))
                    elif board.get_piece_by_coordinates(x, y + i).color == 'white':
                        moves.append((x, y + i))
                        break
                    else:
                        self.defending_pieces.append((x, y + i))
                        break
                else:
                    break
            # if the queen can move to the left
            for i in range(1, 8):
                if x - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y) is None:
                        moves.append((x - i, y))
                    elif board.get_piece_by_coordinates(x - i, y).color == 'white':
                        moves.append((x - i, y))
                        break
                    else:
                        self.defending_pieces.append((x - i, y))
                        break
                else:
                    break
            # if the queen can move to the right
            for i in range(1, 8):
                if x + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y) is None:
                        moves.append((x + i, y))
                    elif board.get_piece_by_coordinates(x + i, y).color == 'white':
                        moves.append((x + i, y))
                        break
                    else:
                        self.defending_pieces.append((x + i, y))
                        break
                else:
                    break
            # if the queen can move up and to the left
            for i in range(1, 8):
                if x - i >= 0 and y - i >= 0:
                    if board.get_piece_by_coordinates(x - i, y - i) is None:
                        moves.append((x - i, y - i))
                    elif board.get_piece_by_coordinates(x - i, y - i).color == 'white':
                        moves.append((x - i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y - i))
                        break
                else:
                    break
            # if the queen can move up and to the right
            for i in range(1, 8):
                if x + i <= 7 and y - i >= 0:
                    if board.get_piece_by_coordinates(x + i, y - i) is None:
                        moves.append((x + i, y - i))
                    elif board.get_piece_by_coordinates(x + i, y - i).color == 'white':
                        moves.append((x + i, y - i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y - i))
                        break
                else:
                    break
            # if the queen can move down and to the left
            for i in range(1, 8):
                if x - i >= 0 and y + i <= 7:
                    if board.get_piece_by_coordinates(x - i, y + i) is None:
                        moves.append((x - i, y + i))
                    elif board.get_piece_by_coordinates(x - i, y + i).color == 'white':
                        moves.append((x - i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x - i, y + i))
                        break
                else:
                    break
            # if the queen can move down and to the right
            for i in range(1, 8):
                if x + i <= 7 and y + i <= 7:
                    if board.get_piece_by_coordinates(x + i, y + i) is None:
                        moves.append((x + i, y + i))
                    elif board.get_piece_by_coordinates(x + i, y + i).color == 'white':
                        moves.append((x + i, y + i))
                        break
                    else:
                        self.defending_pieces.append((x + i, y + i))
                        break
                else:
                    break

        return moves


class King(Piece):

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'king'
        # add the piece value attribute
        self.value = 0
        # add the piece letter attribute (color-sensitive)
        if color == 'white':
            self.letter = 'K'
        else:
            self.letter = 'k'

    def get_legal_moves(self, board):
        # returns a list of legal moves for the king. Also considers that the king cannot move into check and uses the
        # would_be_in_check method from the Board class to check if the king would be in check if it moved to a certain
        # square. Also considers if the king can castle or not.
        moves = []
        x, y = self.position
        color = self.color

        # if the king is white
        if color == 'white':
            # if the king can move up
            if y - 1 >= 0:
                if board.get_piece_by_coordinates(x, y - 1) is None:
                    moves.append((x, y - 1))
                elif board.get_piece_by_coordinates(x, y - 1).color == 'black':
                    moves.append((x, y - 1))
            # if the king can move down
            if y + 1 <= 7:
                if board.get_piece_by_coordinates(x, y + 1) is None:
                    moves.append((x, y + 1))
                elif board.get_piece_by_coordinates(x, y + 1).color == 'black':
                    moves.append((x, y + 1))
            # if the king can move to the left
            if x - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y) is None:
                    moves.append((x - 1, y))
                elif board.get_piece_by_coordinates(x - 1, y).color == 'black':
                    moves.append((x - 1, y))
            # if the king can move to the right
            if x + 1 <= 7:
                if board.get_piece_by_coordinates(x + 1, y) is None:
                    moves.append((x + 1, y))
                elif board.get_piece_by_coordinates(x + 1, y).color == 'black':
                    moves.append((x + 1, y))
            # if the king can move up and to the left
            if x - 1 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y - 1) is None:
                    moves.append((x - 1, y - 1))
                elif board.get_piece_by_coordinates(x - 1, y - 1).color == 'black':
                    moves.append((x - 1, y - 1))
            # if the king can move up and to the right
            if x + 1 <= 7 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 1, y - 1) is None:
                    moves.append((x + 1, y - 1))
                elif board.get_piece_by_coordinates(x + 1, y - 1).color == 'black':
                    moves.append((x + 1, y - 1))
            # if the king can move down and to the left
            if x - 1 >= 0 and y + 1 <= 7:
                if board.get_piece_by_coordinates(x - 1, y + 1) is None:
                    moves.append((x - 1, y + 1))
                elif board.get_piece_by_coordinates(x - 1, y + 1).color == 'black':
                    moves.append((x - 1, y + 1))
            # if the king can move down and to the right
            if x + 1 <= 7 and y + 1 <= 7:
                if board.get_piece_by_coordinates(x + 1, y + 1) is None:
                    moves.append((x + 1, y + 1))
                elif board.get_piece_by_coordinates(x + 1, y + 1).color == 'black':
                    moves.append((x + 1, y + 1))
        # if the king is black
        else:
            # if the king can move up
            if y - 1 >= 0:
                if board.get_piece_by_coordinates(x, y - 1) is None:
                    moves.append((x, y - 1))
                elif board.get_piece_by_coordinates(x, y - 1).color == 'white':
                    moves.append((x, y - 1))
            # if the king can move down
            if y + 1 <= 7:
                if board.get_piece_by_coordinates(x, y + 1) is None:
                    moves.append((x, y + 1))
                elif board.get_piece_by_coordinates(x, y + 1).color == 'white':
                    moves.append((x, y + 1))
            # if the king can move to the left
            if x - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y) is None:
                    moves.append((x - 1, y))
                elif board.get_piece_by_coordinates(x - 1, y).color == 'white':
                    moves.append((x - 1, y))
            # if the king can move to the right
            if x + 1 <= 7:
                if board.get_piece_by_coordinates(x + 1, y) is None:
                    moves.append((x + 1, y))
                elif board.get_piece_by_coordinates(x + 1, y).color == 'white':
                    moves.append((x + 1, y))
            # if the king can move up and to the left
            if x - 1 >= 0 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x - 1, y - 1) is None:
                    moves.append((x - 1, y - 1))
                elif board.get_piece_by_coordinates(x - 1, y - 1).color == 'white':
                    moves.append((x - 1, y - 1))
            # if the king can move up and to the right
            if x + 1 <= 7 and y - 1 >= 0:
                if board.get_piece_by_coordinates(x + 1, y - 1) is None:
                    moves.append((x + 1, y - 1))
                elif board.get_piece_by_coordinates(x + 1, y - 1).color == 'white':
                    moves.append((x + 1, y - 1))
            # if the king can move down and to the left
            if x - 1 >= 0 and y + 1 <= 7:
                if board.get_piece_by_coordinates(x - 1, y + 1) is None:
                    moves.append((x - 1, y + 1))
                elif board.get_piece_by_coordinates(x - 1, y + 1).color == 'white':
                    moves.append((x - 1, y + 1))
            # if the king can move down and to the right
            if x + 1 <= 7 and y + 1 <= 7:
                if board.get_piece_by_coordinates(x + 1, y + 1) is None:
                    moves.append((x + 1, y + 1))
                elif board.get_piece_by_coordinates(x + 1, y + 1).color == 'white':
                    moves.append((x + 1, y + 1))
        return moves


