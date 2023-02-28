from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict
from amsel_engine import Engine
from dataclasses import dataclass
import util


@dataclass
class MinMaxValues:
    alpha: float = float('-inf')
    beta: float = float('inf')


def order_moves(state):
    legal_moves = state.get_valid_moves()
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
        # Finally, order by threat
        for move in legal_moves:
            new_state = state.apply_move(move[0], move[1])
            if new_state.is_checkmate():
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


class Minimax:
    MAX_DEPTH = 10
    THREADS = 6

    def __init__(self):
        self.engine = Engine()
        self.history = defaultdict(list)

    def minimax(self, state, depth, mm_values: MinMaxValues, maximizing_player, path=None):
        if path is None:
            path = []
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_for_maximizing_player(state), None
        if maximizing_player:
            best_value = float('-inf')
            best_move = None
            for move in order_moves(state):
                print(f'Processing state {state.move_history} at depth {self.MAX_DEPTH - depth}')
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                value, _ = self.minimax(new_state, depth - 1, mm_values, False, new_path)
                if value > best_value:
                    best_value = value
                    best_move = move
                mm_values.alpha = max(mm_values.alpha, value)
                if mm_values.alpha >= mm_values.beta:
                    print(f'Pruning {new_path} at depth {self.MAX_DEPTH - depth} with value {value}')
                    break
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in order_moves(state):
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                value, _ = self.minimax(new_state, depth - 1, mm_values, True, new_path)
                if value < best_value:
                    best_value = value
                    best_move = move
                mm_values.beta = min(mm_values.beta, value)
                if mm_values.alpha >= mm_values.beta:
                    print(f'Pruning {new_path} at depth {depth} with value {value}')
                    break
            return best_value, best_move

    def find_best_move(self, state):
        with ProcessPoolExecutor() as executor:
            mm_values = MinMaxValues()
            results = []
            initial_moves = order_moves(state)
            for move, result in zip(initial_moves, executor.map(
                    lambda m: self.minimax(state.apply_move(m[0], m[1]), self.MAX_DEPTH - 1, mm_values, True, [m]),
                    initial_moves
            )):
                if result[0] > 1000:
                    return move
                results.append((move, result))
                mm_values.alpha = max(mm_values.alpha, result[0])
            best_value = float('-inf')
            best_move = None
            for move, result in results:
                value, _ = result
                if value > best_value:
                    best_value = value
                    best_move = move
                mm_values.alpha = max(mm_values.alpha, value)
            return best_move
