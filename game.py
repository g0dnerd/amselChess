# This file contains the 'Game' class, which represents the overall state of a chess game,
# including the current board, the current player, the move history and methods for making moves and
# checking game status.

import copy

import util
from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'white'
        self.move_history = []
        self.half_move_clock = 0
        self.full_move_number = 1
        self.white_king_pos = (4, 7)
        self.black_king_pos = (4, 0)
        self.pgn = ''
        self.white_attackers = []  # Initialize the list of possible attackers for the white king
        self.black_attackers = []  # Initialize the list of possible attackers for the black king
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
        captured_piece = None
        piece = self.board.get_piece_by_square(start)
        legal_moves = piece.get_legal_moves(self.board)
        if piece is None or piece.color != self.current_player:
            # If there is no piece at the start position or the piece is not the current player's color,
            # the move is invalid.
            return False
        if util.square_to_coordinates(end) not in legal_moves:
            # If the end position is not in the list of legal moves for the piece, the move is invalid.
            return False

        # Update the move history
        self.move_history.append((start, end))

        # Update the captured piece
        # If the moved piece is not a pawn:
        if piece.type != 'pawn':
            captured_piece = self.board.get_piece_by_square(end)
        elif piece.type == 'pawn' and self.board.get_piece_by_square(end) is not None:
            captured_piece = self.board.get_piece_by_square(end)
        elif piece.type == 'pawn' and self.board.get_piece_by_square(end) is None and (end[0] != start[0]):
            captured_piece_coordinates = util.square_to_coordinates(end)[0], util.square_to_coordinates(start)[1]
            captured_piece_square = util.coordinates_to_square(
                captured_piece_coordinates[0], captured_piece_coordinates[1])
            captured_piece = self.board.get_piece_by_square(captured_piece_square)
            self.board.remove_piece(captured_piece_square)

        self.board.move_piece(start, end)

        self.white_king_pos = self.board.get_king_position('white')
        self.black_king_pos = self.board.get_king_position('black')
        self.update_attackers('white')
        self.update_attackers('black')

        # Update the PGN
        if self.current_player == 'white':
            self.pgn += str(self.full_move_number) + '. '
        if piece.type == 'pawn' and captured_piece is not None:
            self.pgn += start[0]
        elif piece.type == 'pawn' and captured_piece is None and end[0] != start[0]:
            self.pgn += start[0]
        elif piece.type != 'pawn':
            self.pgn += piece.letter.upper()
        if captured_piece is not None:
            self.pgn += 'x'
        self.pgn += end
        if self.is_in_check(util.get_opponent_color(self.current_player)):
            self.pgn += '+'
        if captured_piece is not None and captured_piece.type == 'king':
            self.pgn += '#'
        self.pgn += ' '

        if captured_piece is not None or piece.type == 'pawn':
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1

        # Update the full move number
        if self.current_player == 'black':
            self.full_move_number += 1

        # Update castling rights
        if piece.type == 'king':
            self.castling_rights[piece.color]['K'] = False
            self.castling_rights[piece.color]['Q'] = False
        elif piece.type == 'rook':
            if piece.color == 'white':
                if piece.position[0] == 0:
                    self.castling_rights['white']['Q'] = False
                elif piece.position[0] == 7:
                    self.castling_rights['white']['K'] = False
            else:
                if piece.position[0] == 0:
                    self.castling_rights['black']['Q'] = False
                elif piece.position[0] == 7:
                    self.castling_rights['black']['K'] = False

        # Switch players
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'
        # Check for game results

        # Check for game results
        if self.is_checkmate():
            self.game_result = 'checkmate'
        return True

    def update_attackers(self, color):
        # Update the list of possible attacker squares on the king of the given color
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        attackers = []
        all_piece_positions = self.board.get_all_piece_positions(util.get_opponent_color(color))
        print("All piece positions: ", all_piece_positions)
        for piece_pos in all_piece_positions:
            if self.is_valid_move(piece_pos, util.coordinates_to_square(king_pos[0], king_pos[1])):
                attackers.append(piece_pos)
        if color == 'white':
            self.white_attackers = attackers
        else:
            self.black_attackers = attackers

    def get_current_player(self):
        return self.current_player

    def get_game_result(self):
        return self.game_result

    def get_move_history(self):
        return self.move_history

    def get_legal_moves(self, square):
        """Return a list of legal moves for the piece at the given square"""
        piece = self.board.get_piece_by_square(square)
        if piece is None or piece.color != self.current_player:
            return []
        return piece.get_legal_moves(self.board)

    def is_in_check(self, color):
        """Return True if the given color is in check, False otherwise"""
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        attackers = self.white_attackers if color == 'white' else self.black_attackers
        for attacker in attackers:
            piece = self.board.get_piece_by_square(attacker)
            for move in piece.get_legal_moves(self.board):
                if move == king_pos:
                    print("The ", color, " king is in check by ", piece.type, " at ", attacker)
                    return True
        return False

    def is_valid_move(self, start, end):
        """Return True if the given move is valid, False otherwise"""
        piece = self.board.get_piece_by_square(start)
        # Check if the piece exists and is the correct color
        if piece is None or piece.color != self.current_player:
            return False
        legal_moves = piece.get_legal_moves(self.board)
        # Check if the move is legal
        if util.square_to_coordinates(end) not in legal_moves:
            return False
        # If the move is en passant, check if the captured pawn moved two squares on the last move
        if piece.type == 'pawn' and end[0] != start[0] and self.board.get_piece_by_square(end) is None:
            print('En passant attempt')
            print('Last move: ', self.move_history[self.full_move_number])
            last_move = self.move_history[self.full_move_number]
            last_move = (util.square_to_coordinates(last_move[0]), util.square_to_coordinates(last_move[1]))
            end_move_coords = util.square_to_coordinates(end)
            if self.current_player == 'white':
                if last_move[1][1] != end_move_coords[1] + 1 or last_move[1][0] != end_move_coords[0]:
                    return False
            else:
                if last_move[1][1] != end_move_coords[1] - 1 or last_move[1][0] != end_move_coords[0]:
                    return False
        game_copy = copy.deepcopy(self)
        piece = game_copy.board.get_piece_by_square(start)
        game_copy.board.move_piece(start, end)
        if piece.type == 'king':
            if piece.color == 'white':
                game_copy.white_king_pos = util.square_to_coordinates(end)
            else:
                game_copy.black_king_pos = util.square_to_coordinates(end)
        # Check if the move would put the player in check
        return not game_copy.is_in_check(piece.color)

    def is_checkmate(self):
        if self.is_in_check(self.current_player):
            print(self.current_player, " is in check")
            for square in self.board.get_all_piece_positions(self.current_player):
                for move in self.get_legal_moves(square):
                    if self.is_valid_move(square, util.coordinates_to_square(move[0], move[1])):
                        return False
            print(self.current_player, " is in checkmate")
            return True
        return False
