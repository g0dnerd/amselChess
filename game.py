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
        self.fen_history = []
        self.half_move_clock = 0
        self.full_move_number = 1
        self.white_king_pos = (4, 7)
        self.black_king_pos = (4, 0)
        self.pgn = ''
        self.promotion = False
        self.white_attackers = []  # Initialize the list of possible attackers for the white king
        self.black_attackers = []  # Initialize the list of possible attackers for the black king
        self.white_defenders = []  # Initialize the list of defenders for attacker on the black king
        self.black_defenders = []  # Initialize the list of defenders for attacker on the white king
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
        if piece is None:
            print('No piece at start position, was given move: ' + start + end)
            print('In board state', self.board)
            print('With move history', self.move_history)

        # Update the move history
        self.move_history.append((start, end))

        # Update the FEN history
        self.fen_history.append(self.board.get_fen())

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

        # Make the move
        self.board.move_piece(start, end)

        castling = False

        # If the move was a pawn promotion
        if piece.type == 'pawn':
            if self.current_player == 'white':
                if end[1] == '8':
                    self.promotion = True
            else:
                if end[1] == '1':
                    self.promotion = True

        # If the move is a castling move
        if piece.type == 'king' and abs(ord(start[0]) - ord(end[0])) == 2:
            castling = True
            if start == 'e1':
                if end == 'g1':
                    self.board.move_piece('h1', 'f1')
                else:
                    self.board.move_piece('a1', 'd1')
            else:
                if end == 'g8':
                    self.board.move_piece('h8', 'f8')
                else:
                    self.board.move_piece('a8', 'd8')

        self.white_king_pos = self.board.get_king_position('white')
        self.black_king_pos = self.board.get_king_position('black')
        self.update_attackers('white')
        self.update_attackers('black')

        if captured_piece is not None or piece.type == 'pawn':
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1

        # Switch players
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'

        self.update_game_result()

        # Update the PGN
        # print("Updating PGN")
        # print("Piece was a", piece.type, "of color", piece.color)
        # print("Move was", start, "to", end)
        # print("Captured piece was", captured_piece)
        # print("Current player is", self.current_player)
        if self.current_player == 'black':
            self.pgn += str(self.full_move_number) + '. '
        if castling:
            if end[0] == 'g':
                self.pgn += 'O-O'
            else:
                self.pgn += 'O-O-O'
        else:
            if piece.type == 'pawn' and captured_piece is not None:
                self.pgn += start[0]
            elif piece.type == 'pawn' and captured_piece is None and end[0] != start[0]:
                self.pgn += start[0]
            elif piece.type != 'pawn':
                self.pgn += piece.letter.upper()
            if captured_piece is not None:
                self.pgn += 'x'
            self.pgn += end
            if self.promotion:
                self.pgn += '=Q'
            if self.is_checkmate():
                self.pgn += '#'
            else:
                if self.is_in_check(self.current_player):
                    self.pgn += '+'

        self.pgn += ' '

        # Update the full move number
        if self.current_player == 'white':
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

        return True

    def apply_move(self, start, end):
        """Make a move on the board and update the game state"""
        state = copy.deepcopy(self)
        # Get the piece at the start position
        captured_piece = None
        piece = state.board.get_piece_by_square(start)
        if piece is None:
            print('No piece at start position, was given move: ' + start + end)
            print('In board state', state.board)
            print('With move history', state.move_history)

        # Update the move history
        state.move_history.append((start, end))

        # Update the FEN history
        state.fen_history.append(state.board.get_fen())

        # Update the captured piece
        # If the moved piece is not a pawn:
        if piece.type != 'pawn':
            captured_piece = state.board.get_piece_by_square(end)
        elif piece.type == 'pawn' and state.board.get_piece_by_square(end) is not None:
            captured_piece = state.board.get_piece_by_square(end)
        elif piece.type == 'pawn' and state.board.get_piece_by_square(end) is None and (end[0] != start[0]):
            captured_piece_coordinates = util.square_to_coordinates(end)[0], util.square_to_coordinates(start)[1]
            captured_piece_square = util.coordinates_to_square(
                captured_piece_coordinates[0], captured_piece_coordinates[1])
            captured_piece = state.board.get_piece_by_square(captured_piece_square)
            state.board.remove_piece(captured_piece_square)

        # Make the move
        state.board.move_piece(start, end)

        castling = False

        # If the move was a pawn promotion
        if piece.type == 'pawn':
            if state.current_player == 'white':
                if end[1] == '8':
                    state.promotion = True
            else:
                if end[1] == '1':
                    state.promotion = True

        # If the move is a castling move
        if piece.type == 'king' and abs(ord(start[0]) - ord(end[0])) == 2:
            castling = True
            if start == 'e1':
                if end == 'g1':
                    state.board.move_piece('h1', 'f1')
                else:
                    state.board.move_piece('a1', 'd1')
            else:
                if end == 'g8':
                    state.board.move_piece('h8', 'f8')
                else:
                    state.board.move_piece('a8', 'd8')

        state.white_king_pos = state.board.get_king_position('white')
        state.black_king_pos = state.board.get_king_position('black')
        state.update_attackers('white')
        state.update_attackers('black')

        if captured_piece is not None or piece.type == 'pawn':
            state.half_move_clock = 0
        else:
            state.half_move_clock += 1

        # Switch players
        if state.current_player == 'white':
            state.current_player = 'black'
        else:
            state.current_player = 'white'

        state.update_game_result()

        # Update the PGN
        # print("Updating PGN")
        # print("Piece was a", piece.type, "of color", piece.color)
        # print("Move was", start, "to", end)
        # print("Captured piece was", captured_piece)
        # print("Current player is", state.current_player)
        if state.current_player == 'black':
            state.pgn += str(state.full_move_number) + '. '
        if castling:
            if end[0] == 'g':
                state.pgn += 'O-O'
            else:
                state.pgn += 'O-O-O'
        else:
            if piece.type == 'pawn' and captured_piece is not None:
                state.pgn += start[0]
            elif piece.type == 'pawn' and captured_piece is None and end[0] != start[0]:
                state.pgn += start[0]
            elif piece.type != 'pawn':
                state.pgn += piece.letter.upper()
            if captured_piece is not None:
                state.pgn += 'x'
            state.pgn += end
            if state.promotion:
                state.pgn += '=Q'
            if state.is_checkmate():
                state.pgn += '#'
            else:
                if state.is_in_check(state.current_player):
                    state.pgn += '+'

        state.pgn += ' '

        # Update the full move number
        if state.current_player == 'white':
            state.full_move_number += 1

        # Update castling rights
        if piece.type == 'king':
            state.castling_rights[piece.color]['K'] = False
            state.castling_rights[piece.color]['Q'] = False
        elif piece.type == 'rook':
            if piece.color == 'white':
                if piece.position[0] == 0:
                    state.castling_rights['white']['Q'] = False
                elif piece.position[0] == 7:
                    state.castling_rights['white']['K'] = False
            else:
                if piece.position[0] == 0:
                    state.castling_rights['black']['Q'] = False
                elif piece.position[0] == 7:
                    state.castling_rights['black']['K'] = False

        return state

    def update_attackers(self, color):
        # Update the list of possible attacker squares on the king of the given color
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        attackers = []
        defenders = []
        all_piece_positions = self.board.get_pieces_by_color(util.get_opponent_color(color))
        for piece_pos in all_piece_positions:
            if self.is_valid_move(piece_pos, util.coordinates_to_square(king_pos[0], king_pos[1])):
                attackers.append(piece_pos)
        for piece_pos in all_piece_positions:
            for attacker in attackers:
                piece = self.board.get_piece_by_square(piece_pos)
                if util.square_to_coordinates(attacker) in piece.defending_pieces:
                    defenders.append(piece_pos)
        if color == 'white':
            self.white_attackers = attackers
            self.black_defenders = defenders
        else:
            self.black_attackers = attackers
            self.white_defenders = defenders

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

    def get_valid_moves(self):
        """Return a list of all valid moves for the current player"""
        valid_moves = []
        for piece_pos in self.board.get_pieces_by_color(self.current_player):
            piece = self.board.get_piece_by_square(piece_pos)
            for move in piece.get_legal_moves(self.board):
                move = util.coordinates_to_square(move[0], move[1])
                if self.is_valid_move(piece.square, move):
                    valid_moves.append((piece.square, move))
        return valid_moves

    def get_valid_moves_for_piece(self, square):
        piece = self.board.get_piece_by_square(square)
        valid_moves = []
        for move in piece.get_legal_moves(self.board):
            move = util.coordinates_to_square(move[0], move[1])
            if self.is_valid_move(piece.square, move):
                valid_moves.append(move)
        return valid_moves

    def is_in_check(self, color):
        """Return True if the given color is in check, False otherwise"""
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        attackers = self.white_attackers if color == 'white' else self.black_attackers
        for attacker in attackers:
            piece = self.board.get_piece_by_square(attacker)
            for move in piece.get_legal_moves(self.board):
                if move == king_pos:
                    return True
        pieces = self.board.get_pieces_by_color(util.get_opponent_color(color))
        for piece in pieces:
            piece = self.board.get_piece_by_square(piece)
            legal_moves = piece.get_legal_moves(self.board)
            if king_pos in legal_moves:
                return True
        return False

    def is_valid_move(self, start, end):
        """Return True if the given move is valid, False otherwise"""
        piece = self.board.get_piece_by_square(start)

        # Check if the piece exists and is the correct color
        if piece is None or piece.color != self.current_player:
            return False

        # Check if the piece can move to the given square
        legal_moves = piece.get_legal_moves(self.board)
        if util.square_to_coordinates(end) not in legal_moves:
            return False

        # If the move is en passant, check if the captured pawn moved two squares on the last move
        if piece.type == 'pawn' and end[0] != start[0] and self.board.get_piece_by_square(end) is None:
            # print("En passant move: ", start, end)
            last_move = self.move_history[len(self.move_history) - 1]
            # print("Last move: ", last_move)
            last_move = (util.square_to_coordinates(last_move[0]), util.square_to_coordinates(last_move[1]))
            end_move_coords = util.square_to_coordinates(end)
            if self.current_player == 'white':
                if last_move[1][1] != end_move_coords[1] + 1 or last_move[1][0] != end_move_coords[0]:
                    return False
            else:
                if last_move[1][1] != end_move_coords[1] - 1 or last_move[1][0] != end_move_coords[0]:
                    return False

        # Check if the checking piece is defended
        defenders = self.white_defenders if self.current_player == 'black' else self.black_defenders
        for defender in defenders:
            piece = self.board.get_piece_by_square(defender)
            if util.square_to_coordinates(end) in piece.defending_pieces:
                if self.board.get_piece_by_square(start).type == 'king':
                    return False

        # Make the move on a copy of the board to avoid altering the actual board
        game_copy = copy.deepcopy(self)

        # If the move is a castling move
        if piece.type == 'king' and abs(ord(start[0]) - ord(end[0])) == 2:
            if self.current_player == 'white':
                if self.board.get_piece_by_square('e1') is None:
                    return False
            else:
                if self.board.get_piece_by_square('e8') is None:
                    return False

            # print("Checking legality of castling move:", start, "to", end)
            # Can not castle while in check
            if self.is_in_check(self.current_player):
                return False

            # Can not castle if the king or rook has moved
            if self.current_player == 'white':
                if end == 'g1':
                    if self.board.get_piece_by_square('h1').type != 'rook' and \
                            self.board.get_piece_by_square('h1').color != 'white':
                        return False
                    else:
                        if not self.castling_rights['white']['K']:
                            return False
                else:
                    if self.board.get_piece_by_square('a1').type != 'rook' and \
                            self.board.get_piece_by_square('a1').color != 'white':
                        return False
                    else:
                        if not self.castling_rights['white']['Q']:
                            return False
            else:
                if end == 'g8':
                    if self.board.get_piece_by_square('h8').type != 'rook' and \
                            self.board.get_piece_by_square('h8').color != 'black':
                        return False
                    else:
                        if not self.castling_rights['black']['K']:
                            return False
                else:
                    if self.board.get_piece_by_square('a8').type != 'rook' and \
                            self.board.get_piece_by_square('a8').color != 'black':
                        return False
                    else:
                        if not self.castling_rights['black']['Q']:
                            return False

            king_piece = game_copy.board.get_piece_by_square(start)
            if king_piece.color == 'white':
                if end == 'g1':
                    rook_piece = game_copy.board.get_piece_by_square('h1')
                else:
                    rook_piece = game_copy.board.get_piece_by_square('a1')
            else:
                if end == 'g8':
                    rook_piece = game_copy.board.get_piece_by_square('h8')
                else:
                    rook_piece = game_copy.board.get_piece_by_square('a8')

            # print("Rook to move:", rook_piece.square)

            if rook_piece.square[0] == 'h':
                if rook_piece.square[1] == '1':
                    game_copy.board.move_piece('e1', 'f1')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                    game_copy.board.move_piece('f1', 'g1')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                else:
                    game_copy.board.move_piece('e8', 'f8')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                    game_copy.board.move_piece('f8', 'g8')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
            else:
                if rook_piece.square[1] == 1:
                    game_copy.board.move_piece('e1', 'd1')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                    game_copy.board.move_piece('d1', 'c1')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                else:
                    game_copy.board.move_piece('e8', 'd8')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False
                    game_copy.board.move_piece('d8', 'c8')
                    if game_copy.is_in_check(game_copy.current_player):
                        return False

            if game_copy.is_in_check(game_copy.current_player):
                return False
            return True
        else:
            piece = game_copy.board.get_piece_by_square(start)
            game_copy.board.move_piece(start, end)

            # Check if the move would put a king next to another king
            if piece.type == 'king':
                target_square = util.square_to_coordinates(end)
                for i in range(2):
                    for j in range(2):
                        try:
                            adj_piece = game_copy.board.get_piece_by_coordinates(
                                target_square[0] + i, target_square[1] + j)
                        except KeyError:
                            continue
                        if adj_piece is not None:
                            if adj_piece.type == 'king' and adj_piece.color != piece.color:
                                return False
                        try:
                            adj_piece = game_copy.board.get_piece_by_coordinates(
                                target_square[0] + i, target_square[1] - j)
                        except KeyError:
                            continue
                        if adj_piece is not None:
                            if adj_piece.type == 'king' and adj_piece.color != piece.color:
                                return False
                        try:
                            adj_piece = game_copy.board.get_piece_by_coordinates(
                                target_square[0] - i, target_square[1] + j)
                        except KeyError:
                            continue
                        if adj_piece is not None:
                            if adj_piece.type == 'king' and adj_piece.color != piece.color:
                                return False
                        try:
                            adj_piece = game_copy.board.get_piece_by_coordinates(
                                target_square[0] - i, target_square[1] - j)
                        except KeyError:
                            continue
                        if adj_piece is not None:
                            if adj_piece.type == 'king' and adj_piece.color != piece.color:
                                return False
                if piece.color == 'white':
                    game_copy.white_king_pos = util.square_to_coordinates(end)
                else:
                    game_copy.black_king_pos = util.square_to_coordinates(end)

            # Check if the move would put the player in check
            return not game_copy.is_in_check(piece.color)

    def is_checkmate(self):
        if self.is_in_check(self.current_player):
            for square in self.board.get_pieces_by_color(self.current_player):
                for move in self.get_legal_moves(square):
                    if self.is_valid_move(square, util.coordinates_to_square(move[0], move[1])):
                        return False
            if self.current_player == 'white':
                self.game_result = '1-0'
            else:
                self.game_result = '0-1'
            return True
        return False

    def is_stalemate(self):
        if not self.is_in_check(self.current_player):
            for square in self.board.get_pieces_by_color(self.current_player):
                piece = self.board.get_piece_by_square(square)
                for move in piece.get_legal_moves(self.board):
                    if self.is_valid_move(square, util.coordinates_to_square(move[0], move[1])):
                        return False
            self.game_result = 'stalemate'
            return True
        return False

    def is_insufficient_material(self):
        """Returns True if the game is a draw due to insufficient material, False otherwise"""
        # Check if there are any pawns, rooks, or queens
        if self.board.get_pieces_by_type('pawn') == [] and \
                self.board.get_pieces_by_type('rook') == [] and \
                self.board.get_pieces_by_type('queen') == []:
            # Check if there are any knights or bishops
            if self.board.get_pieces_by_type_and_color('knight', 'white') == [] and \
                    self.board.get_pieces_by_type_and_color('knight', 'black') == [] and \
                    self.board.get_pieces_by_type_and_color('bishop', 'white') == [] and \
                    self.board.get_pieces_by_type_and_color('bishop', 'black') == []:
                self.game_result = 'draw'
                print('Draw due to insufficient material')
                return True
            # Check if there is only one knight or bishop
            elif len(self.board.get_pieces_by_type('knight')) == 1 and self.board.get_pieces_by_type('bishop') == []:
                self.game_result = 'draw'
                print('Draw due to insufficient material')
                return True
            # Check if there are two bishops of different colors
            elif len(self.board.get_pieces_by_type('bishop')) == 1 and self.board.get_pieces_by_type('knight') == []:
                self.game_result = 'draw'
                print('Draw due to insufficient material')
                return True
            elif len(self.board.get_pieces_by_type('bishop')) == 2:
                bishop1 = self.board.get_piece_by_square(self.board.get_pieces_by_type('bishop')[0])
                bishop2 = self.board.get_piece_by_square(self.board.get_pieces_by_type('bishop')[1])
                if (bishop1.color == 'white' and bishop2.color == 'black') or \
                        (bishop1.color == 'black' and bishop2.color == 'white'):
                    self.game_result = 'draw'
                    print('Draw due to insufficient material')
                    return True
        return False

    def is_threefold_repetition(self):
        """Returns True if the game is a draw due to threefold repetition, False otherwise"""
        threefold = self.fen_history.count(self.board.get_fen()) >= 3
        if threefold:
            print('Threefold repetition')
            self.game_result = 'draw'
        return threefold

    def is_fifty_move_rule(self):
        """Returns True if the game is a draw due to the fifty move rule, False otherwise"""
        fifty_moves = self.half_move_clock >= 50
        if fifty_moves:
            print('Fifty move rule')
            self.game_result = 'draw'
        return fifty_moves

    def is_game_over(self):
        """Returns True if the game is over, False otherwise"""
        if self.game_result is not None:
            return True

    def update_game_result(self):
        """Updates the game result if the game is over"""
        self.is_stalemate()
        self.is_fifty_move_rule()
        self.is_checkmate()
        self.is_threefold_repetition()
        self.is_insufficient_material()

    def get_last_move(self):
        """Returns the last move in the game"""
        return self.move_history[-1]

    def get_first_move(self):
        """Returns the first move in the game"""
        return self.move_history[0]

    def get_move_by_number(self, move_number):
        """Returns the move at the given move number"""
        return self.move_history[move_number]

    def is_capture(self, move):
        """Returns True if the given move is a capture, False otherwise"""
        end = move[1]
        if self.board.get_piece_by_square(end) is not None:
            return True
        return False
