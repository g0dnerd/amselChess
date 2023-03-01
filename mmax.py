import util
import random
from amsel_engine import Engine


def order_moves(state):
    legal_moves = state.get_valid_moves()
    random.shuffle(legal_moves)
    if len(legal_moves) <= 1:
        return legal_moves
    else:
        ordered_moves = []
        # First, order by captures
        for move in legal_moves:
            if state.is_capture(move):
                ordered_moves.append(move)
        # Then, order by check
        for move in legal_moves:
            new_state = state.apply_move(move[0], move[1])
            if new_state.is_in_check(new_state.current_player):
                if move not in ordered_moves:
                    ordered_moves.append(move)
            if new_state.is_checkmate():
                if move not in ordered_moves:
                    ordered_moves.append(move)
            elif new_state.is_in_check(new_state.current_player):
                continue
            else:
                piece = state.board.get_piece_by_square(move[0])
                threatened_squares = piece.get_legal_moves(state.board)
                for threatened_pos in threatened_squares:
                    threatened_square = util.coordinates_to_square(threatened_pos[0], threatened_pos[1])
                    threatened_piece = new_state.board.get_piece_by_square(threatened_square)
                    if threatened_piece is not None and threatened_piece.color != piece.color:
                        if move not in ordered_moves:
                            ordered_moves.append(move)
                            break
        # Finally, add any remaining legal moves that haven't been added yet
        for move in legal_moves:
            if move not in ordered_moves:
                ordered_moves.append(move)
        return ordered_moves


class Negamax:
    def __init__(self, depth: object) -> object:
        self.engine = Engine()
        self.max_depth = depth

    def alphabeta(self, state, depth, alpha, beta):
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_for_maximizing_player(state)

        for move in order_moves(state):
            new_state = state.apply_move(move[0], move[1])
            print('Evaluating line', new_state.move_history)
            value = self.alphabeta(new_state, depth - 1, alpha, beta)
            alpha = max(alpha, value)
            if alpha >= beta:
                print('Pruning line', new_state.move_history)
                return alpha

        return alpha

    def find_best_move(self, state):
        best_move = None
        legal_moves = order_moves(state)
        alpha = float('-inf')
        beta = float('inf')

        if len(legal_moves) == 1:
            return legal_moves[0]

        for move in legal_moves:
            new_state = state.apply_move(move[0], move[1])
            score = self.alphabeta(new_state, self.max_depth, alpha, beta)
            if score >= 1000:
                return move
            if score > alpha:
                alpha = score
                best_move = move

        return best_move
