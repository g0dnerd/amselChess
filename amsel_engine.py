import util


def get_backward_pawns(game, color):
    """
        Returns a set of backward pawns for the given color.
        A pawn is considered backward if it has no pawns in front of it
        on its current file or on either adjacent file, and cannot advance safely.
        """
    backward_pawns = set()
    pawns = game.board.get_pieces_by_type_and_color('pawn', color)
    for pawn in pawns:
        file = pawn.square[0]
        coords = pawn.position
        pawn_color = pawn.color
        is_isolated = file == 'a' or file == 'h' or not \
            game.board.get_piece_by_coordinates(coords[0], coords[1] - 1) or not \
            game.board.get_piece_by_coordinates(coords[0] - 1, coords[1] - 1) or not \
            game.board.get_piece_by_coordinates(coords[0] + 1, coords[1] - 1)
        if is_isolated:
            continue
        if pawn_color == 'white':
            for i in range(coords[1], 8):
                piece = game.board.get_piece_by_coordinates(coords[0], i)
                if piece and piece.type == 'pawn' and piece.color == 'white':
                    backward_pawns.add(pawn)
                    break
        else:
            for i in range(coords[1] - 1, 0, -1):
                # print("Trying to get piece by coordinates", coords[0], i)
                piece = game.board.get_piece_by_coordinates(coords[0], i)
                if piece and piece.type == 'pawn' and piece.color == 'black':
                    backward_pawns.add(pawn)
                    break
    return backward_pawns


def get_doubled_pawns(game, color):
    """
    Returns a list of all the doubled pawns for the given color.
    A pawn is considered doubled if there is another pawn of the same color on the same file.
    """
    pawns = game.board.get_pieces_by_type_and_color('pawn', color)
    pawn_positions = [pawn.position for pawn in pawns]
    doubled_pawns = []
    for file in range(8):
        pawns_on_file = [pos for pos in pawn_positions if pos[0] == file]
        if len(pawns_on_file) > 1:
            doubled_pawns += pawns_on_file
    return doubled_pawns


def get_passed_pawns(game, color):
    """
    Returns a list of all passed pawns for the given color.
    """
    passed_pawns = []
    enemy_color = "white" if color == "black" else "black"
    for file in range(8):
        for rank in range(8):
            piece = game.board.get_piece_by_coordinates(file, rank)
            if piece is not None and piece.color == color and piece.type == "pawn":
                if not is_passed_pawn(game, piece.square, enemy_color):
                    continue
                passed_pawns.append((file, rank))
    return passed_pawns


def is_passed_pawn(game, square, enemy_color):
    """
    Returns True if the given pawn is passed, False otherwise.
    """
    file, rank = util.square_to_coordinates(square)
    if enemy_color == 'white':
        for i in range(rank + 1, 8):
            if game.board.get_piece_by_coordinates(file, i) is not None:
                return False
        for i in range(rank + 1, 8):
            for j in range(-1, 2):
                if j == 0:
                    continue
                if (file + j) in range(8) and game.board.get_piece_by_coordinates(file + j, i) is not None:
                    return False
    else:
        for i in range(rank - 1, -1, -1):
            if game.board.get_piece_by_coordinates(file, i) is not None:
                return False
        for i in range(rank - 1, -1, -1):
            for j in range(-1, 2):
                if j == 0:
                    continue
                if (file + j) in range(8) and game.board.get_piece_by_coordinates(file + j, i) is not None:
                    return False
    return True


def get_isolated_pawns(game, color):
    """
    Returns the number of isolated pawns for the given color.
    """
    isolated_pawns = []

    pawns = game.board.get_pieces_by_type_and_color('pawn', color)

    for pawn in pawns:
        pawn_file = pawn.position[0]
        is_isolated = True
        # check if there are any pawns of the same color on the adjacent files
        for file_offset in [-1, 1]:
            adjacent_file = pawn_file + file_offset
            if adjacent_file < 0 or adjacent_file > 7:
                continue
            adjacent_pawns = game.board.get_pieces_by_type_and_file('pawn', color, adjacent_file)
            if len(adjacent_pawns) > 0:
                is_isolated = False
                break
        if is_isolated:
            isolated_pawns.append(pawn)

    return isolated_pawns


def get_pawn_chains(game, color):
    """Returns a list of pawn chains for the given color"""
    pawn_chains = []
    for file in range(8):
        chain = []
        for rank in range(8):
            piece = game.board.get_piece_by_coordinates(file, rank)
            if piece and piece.type == 'pawn' and piece.color == color:
                if not chain:
                    chain.append((file, rank))
                elif abs(rank - chain[-1][1]) == 1 and file == chain[-1][0]:
                    chain.append((file, rank))
                else:
                    pawn_chains.append(chain)
                    chain = [(file, rank)]
            elif chain:
                pawn_chains.append(chain)
                chain = []
        if chain:
            pawn_chains.append(chain)
    return pawn_chains


def get_pawn_score(game, color):
    """
    Evaluates the pawn structure for the given color on the board.
    Returns a score that reflects the strength of the pawn structure.
    """

    pawn_score = 0

    # Evaluate pawn chains
    pawn_chains = get_pawn_chains(game, color)
    for chain in pawn_chains:
        if len(chain) >= 3:
            # Bonus for long pawn chains
            pawn_score += 0.5 * len(chain)

    # Evaluate isolated pawns
    isolated_pawns = get_isolated_pawns(game, color)
    pawn_score -= 0.5 * len(isolated_pawns)

    # Evaluate doubled pawns
    doubled_pawns = get_doubled_pawns(game, color)
    pawn_score -= 0.5 * len(doubled_pawns)

    # Evaluate backward pawns
    backward_pawns = get_backward_pawns(game, color)
    pawn_score -= 0.5 * len(backward_pawns)

    # Evaluate passed pawns
    passed_pawns = get_passed_pawns(game, color)
    pawn_score += 0.5 * len(passed_pawns)

    pawn_positions = game.board.get_pieces_by_type_and_color('pawn', color)
    for pawn in pawn_positions:
        if pawn.position in doubled_pawns:
            pawn_score -= 0.25
        if pawn.position in isolated_pawns:
            pawn_score -= 0.25
        if pawn.position in backward_pawns:
            pawn_score -= 0.25
        if pawn.position in passed_pawns:
            pawn_score += 0.25

    # print('Pawn score for', color, ':', pawn_score)
    return pawn_score


def get_material_score(game):
    """Returns the material balance of the board"""
    material_balance = 0
    for square in game.board.board:
        piece = game.board.get_piece_by_square(square)
        if piece is not None:
            if piece.color == 'white':
                material_balance += piece.value
            else:
                material_balance -= piece.value
    return material_balance * 8


class Engine:
    def __init__(self):
        # Define constants
        self.MOBILITY_WEIGHT = 0.1
        # Values for each piece type depending on the position on the board
        self.POSITIONAL_VALUES = {
            'pawn': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'knight': [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            'bishop': [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            'rook': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ],
            'queen': [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            'king': [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]
            ]
        }
        self.POSITIONAL_WEIGHT = 0.005
        self.DOUBLED_PAWN_PENALTY = 20
        self.ISOLATED_PAWN_PENALTY = 10
        self.BACKWARD_PAWN_PENALTY = 15
        self.PASSED_PAWN_BONUS = 20
        self.WEAK_PAWN_PENALTY = 10
        self.PAWN_CHAIN_BONUS = 10

    def evaluate_position(self, game):
        # print('Evaluating position...')
        if game.game_result == '1-0':
            return 1000000
        elif game.game_result == '0-1':
            return -1000000
        elif game.game_result == 'draw' or game.game_result == 'stalemate':
            return 0
        material_score = get_material_score(game)
        mobility_score = self.get_mobility_score(game)
        white_pawn_score = get_pawn_score(game, 'white')
        black_pawn_score = get_pawn_score(game, 'black')
        pawn_score = black_pawn_score - white_pawn_score
        king_safety_score = 0
        if game.board.is_middle_game() or game.board.is_endgame():
            white_king_safety_score = self.get_king_safety_score(game, 'white')
            black_king_safety_score = self.get_king_safety_score(game, 'black')
            king_safety_score = white_king_safety_score - black_king_safety_score
        white_positional_score = self.get_positional_score(game, 'white')
        black_positional_score = self.get_positional_score(game, 'black')

        positional_score = black_positional_score - white_positional_score

        total_score = material_score + mobility_score + pawn_score + king_safety_score + positional_score

        return total_score

    def evaluate_for_maximizing_player(self, game):
        if game.current_player == 'white':
            return self.evaluate_position(game)
        else:
            return -self.evaluate_position(game)

    def get_mobility_score(self, game):
        """Returns the mobility score of the board"""
        white_mobility_score = self.get_mobility_score_for_color(game, 'white')
        black_mobility_score = self.get_mobility_score_for_color(game, 'black')
        mobility_score = white_mobility_score - black_mobility_score
        return mobility_score

    def get_mobility_score_for_color(self, game, color):
        """Returns the mobility score of the board for one player"""
        switched = False
        if color != game.current_player:
            game.current_player = color
            switched = True
        mobility_score = 0
        for square in game.board.board:
            piece = game.board.get_piece_by_square(square)
            if piece is not None and piece.color == color:
                mobility_score += len(game.get_valid_moves_for_piece(piece.square))
        mobility_score *= self.MOBILITY_WEIGHT
        if switched:
            game.current_player = util.get_opponent_color(color)
        return mobility_score

    def get_king_safety_score(self, game, color):
        """
        Evaluate king safety for a given color on the board.
        :param game: The chess game to evaluate.
        :param color: The color to evaluate king safety for.
        :return: A float representing the king safety score for the given color.
        """
        king_position = game.board.get_pieces_by_type_and_color('king', color)[0].position
        if king_position is None:
            return 0.0

        king_file, king_rank = king_position

        # Check if the king is in the center, which is generally less safe
        center_file, center_rank = 3, 3
        if color == 'black':
            center_rank = 4
        center_distance = abs(king_file - center_file) + abs(king_rank - center_rank)
        center_weight = 0.1
        center_score = center_weight * center_distance if center_distance <= 2 else 0.0

        # Check if the king is in the endgame, where it's generally safer to be more active
        endgame_weight = 0.5
        if game.board.is_endgame():
            mobility_score = self.get_mobility_score_for_color(game, color)
            return mobility_score * endgame_weight + center_score

        # Check for nearby enemy pieces that can attack the king
        attack_weight = 0.2
        attack_distance = 2
        nearby_attacks = 0
        for file in range(max(0, king_file - attack_distance), min(8, king_file + attack_distance + 1)):
            for rank in range(max(0, king_rank - attack_distance), min(8, king_rank + attack_distance + 1)):
                piece = game.board.get_piece_by_coordinates(file, rank)
                if piece is not None:
                    legal_moves = piece.get_legal_moves(game.board)
                if piece is not None and piece.color != color and piece.type != 'king':
                    if king_position in legal_moves:
                        nearby_attacks += 1
        attack_score = attack_weight * nearby_attacks

        # Check for pawn shield in front of the king
        shield_weight = 0.15
        if color == 'white':
            shield_file, shield_rank = king_file, king_rank - 1
            pawn_file1, pawn_file2 = king_file - 1, king_file + 1
            pawn_rank = king_rank - 2
        else:
            shield_file, shield_rank = king_file, king_rank + 1
            pawn_file1, pawn_file2 = king_file - 1, king_file + 1
            pawn_rank = king_rank + 2
        shield_score = 0.0
        piece = game.board.get_piece_by_coordinates(shield_file, shield_rank)
        if piece is not None and piece.type == 'pawn' and piece.color == color:
            # Check for doubled pawns that would weaken the shield
            doubled_pawns = get_doubled_pawns(game, color)
            if (pawn_file1, pawn_rank) not in doubled_pawns and (pawn_file2, pawn_rank) not in doubled_pawns:
                shield_score = shield_weight

        # Calculate the overall king safety score as a weighted sum of the individual scores
        overall_score = center_score + attack_score + shield_score

        return overall_score

    def get_positional_score(self, game, color):
        """
        Evaluates the positional strength of the given color on the board.

        args:
            board: the board to evaluate
            color: the color to evaluate

        returns:
            float: a score that reflects the positional strength of the given color
        """

        # Initialize positional score to 0
        positional_score = 0

        # Loop through all pieces of the given color
        for piece_pos in game.board.get_pieces_by_color(color):
            piece = game.board.get_piece_by_square(piece_pos)
            piece_position = piece.position
            piece_x = piece_position[0]
            piece_y = piece_position[1]

            # Add the value of the piece's position to the positional score.
            # Different piece types have different values for different positions on the board.
            # These values are stored in the POSITION_VALUES dictionary.
            if piece.type == 'pawn':
                if piece.color == 'white':
                    positional_score += self.POSITIONAL_VALUES[piece.type][piece_y][piece_x]
                    # print('Added to positional score:', self.POSITIONAL_VALUES[piece.type][piece_y][piece_x],
#                          'for', piece.color, piece.type, 'at position:', piece_pos)
                else:
                    positional_score += self.POSITIONAL_VALUES[piece.type][7 - piece_y][piece_x]
                    # print('Added to positional score:', self.POSITIONAL_VALUES[piece.type][7 - piece_y][piece_x],
#                          'for', piece.color, piece.type, 'at position:', piece_pos)
            else:
                if piece.color == 'white':
                    positional_score += self.POSITIONAL_VALUES[piece.type][piece_y][piece_x]
                    # print('Added to positional score:', self.POSITIONAL_VALUES[piece.type][piece_y][piece_x],
                     # 'for', piece.color, piece.type, 'at position:', piece_pos)
                else:
                    positional_score += self.POSITIONAL_VALUES[piece.type][7 - piece_y][piece_x]
                    # print('Added to positional score:', self.POSITIONAL_VALUES[piece.type][7 - piece_y][piece_x],
                     # 'for', piece.color, piece.type, 'at position:', piece_pos)

        positional_score *= self.POSITIONAL_WEIGHT
        # print("Evaluated positional score for", color, "as", positional_score)

        return positional_score
