import util

def get_backward_pawns(board, color):
    """
        Returns a set of backward pawns for the given color.
        A pawn is considered backward if it has no pawns in front of it
        on its current file or on either adjacent file, and cannot advance safely.
        """
    backward_pawns = set()
    pawns = board.get_pieces_by_type('pawn', color)
    for pawn in pawns:
        file = pawn.square[0]
        rank = pawn.square[1]
        coords = pawn.position
        pawn_color = pawn.color
        is_isolated = file == 'a' or file == 'h' or not \
            board.get_piece_by_coordinates(coords[0], coords[1] - 1) or not \
            board.get_piece_by_coordinates(coords[0] - 1, coords[1] - 1) or not \
            board.get_piece_by_coordinates(coords[0] + 1, coords[1] - 1)
        if is_isolated:
            continue
        if pawn_color == 'white':
            for i in range(rank + 1, 8):
                piece = board.get_piece_by_coordinates(file, i)
                if piece and piece.type == 'pawn' and piece.color == 'white':
                    backward_pawns.add(pawn)
                    break
        else:
            for i in range(rank - 1, 0, -1):
                piece = board.get_piece_by_coords(file, i)
                if piece and piece.type == 'pawn' and piece.color == 'black':
                    backward_pawns.add(pawn)
                    break
    return backward_pawns


def get_doubled_pawns(board, color):
    """
    Returns a list of all the doubled pawns for the given color.
    A pawn is considered doubled if there is another pawn of the same color on the same file.
    """
    pawns = board.get_pieces_by_type('pawn', color)
    pawn_positions = [pawn.position for pawn in pawns]
    doubled_pawns = []
    for file in range(8):
        pawns_on_file = [pos for pos in pawn_positions if pos[0] == file]
        if len(pawns_on_file) > 1:
            doubled_pawns += pawns_on_file
    return doubled_pawns


def get_passed_pawns(board, color):
    """
    Returns a list of all passed pawns for the given color.
    """
    passed_pawns = []
    enemy_color = "white" if color == "black" else "black"
    for file in range(8):
        for rank in range(8):
            piece = board.get_piece_by_coordinates(file, rank)
            if piece is not None and piece.color == color and piece.type == "pawn":
                if not is_passed_pawn(board, piece.square, enemy_color):
                    continue
                passed_pawns.append((file, rank))
    return passed_pawns


def is_passed_pawn(board, square, enemy_color):
    """
    Returns True if the given pawn is passed, False otherwise.
    """
    file, rank = util.square_to_coordinates(square)
    if enemy_color == 'white':
        for i in range(rank + 1, 8):
            if board.get_piece_by_coordinates(file, i) is not None:
                return False
        for i in range(rank + 1, 8):
            for j in range(-1, 2):
                if j == 0:
                    continue
                if (file + j) in range(8) and board.get_piece_by_coordinates(file + j, i) is not None:
                    return False
    else:
        for i in range(rank - 1, -1, -1):
            if board.get_piece_by_coordinates(file, i) is not None:
                return False
        for i in range(rank - 1, -1, -1):
            for j in range(-1, 2):
                if j == 0:
                    continue
                if (file + j) in range(8) and board.get_piece_by_coordinates(file + j, i) is not None:
                    return False
    return True


def get_isolated_pawns(board, color):
    """
    Returns the number of isolated pawns for the given color.
    """
    isolated_pawns = []

    pawns = board.get_pieces_by_type('pawn', color)

    for pawn in pawns:
        pawn_file = pawn.position[0]
        is_isolated = True
        # check if there are any pawns of the same color on the adjacent files
        for file_offset in [-1, 1]:
            adjacent_file = pawn_file + file_offset
            if adjacent_file < 0 or adjacent_file > 7:
                continue
            adjacent_pawns = board.get_pieces_by_type_and_file('pawn', color, adjacent_file)
            if len(adjacent_pawns) > 0:
                is_isolated = False
                break
        if is_isolated:
            isolated_pawns.append(pawn)

    return isolated_pawns


def get_pawn_chains(board, color):
    """Returns a list of pawn chains for the given color"""
    pawn_chains = []
    for file in range(8):
        chain = []
        for rank in range(8):
            piece = board.get_piece_by_coordinates(file, rank)
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


def get_pawn_score(board, color):
    """
    Evaluates the pawn structure for the given color on the board.
    Returns a score that reflects the strength of the pawn structure.
    """

    pawn_score = 0

    # Evaluate pawn chains
    pawn_chains = get_pawn_chains(board, color)
    for chain in pawn_chains:
        if len(chain) >= 3:
            # Bonus for long pawn chains
            pawn_score += 0.5 * len(chain)

    # Evaluate isolated pawns
    isolated_pawns = get_isolated_pawns(board, color)
    pawn_score -= 0.5 * len(isolated_pawns)

    # Evaluate doubled pawns
    doubled_pawns = get_doubled_pawns(board, color)
    pawn_score -= 0.5 * len(doubled_pawns)

    # Evaluate backward pawns
    backward_pawns = get_backward_pawns(board, color)
    pawn_score -= 0.5 * len(backward_pawns)

    # Evaluate passed pawns
    passed_pawns = get_passed_pawns(board, color)
    pawn_score += 0.5 * len(passed_pawns)

    pawn_positions = board.get_pieces_by_type('pawn', color)
    for pawn in pawn_positions:
        if pawn.position in doubled_pawns:
            pawn_score -= 0.25
        if pawn.position in isolated_pawns:
            pawn_score -= 0.25
        if pawn.position in backward_pawns:
            pawn_score -= 0.25
        if pawn.position in passed_pawns:
            pawn_score += 0.25

    print('Pawn score: {}'.format(pawn_score))
    return pawn_score


class Engine:
    def __init__(self, game):
        self.game = game
        self.MOBILITY_WEIGHT = 0.1

    def get_legal_moves(self):
        return self.game.get_valid_moves()

    def evaluate_position(self):
        material_score = self.get_material_score()
        mobility_score = self.get_mobility_score()
        pawn_score = get_pawn_score(self.game.board, self.game.current_player)
        king_safety_score = 0
        positional_score = 0
        # king_safety_score = self.get_king_safety_score()
        # positional_score = self.get_positional_score()

        total_score = material_score + mobility_score + pawn_score + king_safety_score + positional_score

        return total_score

    def get_material_score(self):
        """Returns the material balance of the board"""
        material_balance = 0
        for square in self.game.board.board:
            piece = self.game.board.get_piece_by_square(square)
            if piece is not None:
                if piece.color == 'white':
                    material_balance += piece.value
                else:
                    material_balance -= piece.value
        return material_balance

    def get_mobility_score(self):
        """Returns the mobility score of the board"""
        mobility_score = 0
        for square in self.game.board.board:
            piece = self.game.board.get_piece_by_square(square)
            if piece is not None:
                if piece.color == 'white':
                    mobility_score += len(self.game.get_valid_moves_for_piece(piece.square))
                else:
                    mobility_score -= len(self.game.get_valid_moves_for_piece(piece.square))
        mobility_score *= self.MOBILITY_WEIGHT
        return mobility_score
