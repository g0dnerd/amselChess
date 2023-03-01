import copy
from concurrent.futures import ThreadPoolExecutor
import threading
from amsel_engine import Engine
from dataclasses import dataclass
import time
import util
import random


@dataclass
class MinMaxValues:
    def __init__(self):
        self.lock = threading.Lock()
        self.alpha: float = float('-inf')
        self.beta: float = float('inf')


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
    def __init__(self, depth):
        self.engine = Engine()
        self.max_depth = depth + 1

    def alpha_beta(self, state, depth, alpha, beta, maximizing_player, path):
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_for_maximizing_player(state), None

        best_value = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in order_moves(state):
            new_state = state.apply_move(move[0], move[1])
            new_path = path + [move]
            print('Evaluating line', new_path)
            value, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, not maximizing_player, new_path)
            if maximizing_player:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    print(f'Pruning {new_path} at depth {self.max_depth - depth} with value {value}')
                    break
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    print(f'Pruning {new_path} at depth {self.max_depth - depth} with value {value}')
                    break

        return best_value, best_move

    def minimax(self, state, depth, maximizing_player, path=None):
        if path is None:
            path = []
        alpha = float('-inf')
        beta = float('inf')
        best_value, best_move = self.alpha_beta(state, depth, alpha, beta, maximizing_player, path)
        return best_value, best_move

    def find_best_move(self, state):
        start_time = time.time()
        best_value, best_move = self.minimax(state, self.max_depth - 1, True)
        total_time = time.time() - start_time
        print(f'Found move {best_move} with value {best_value} in {total_time:.4f} seconds')
        return best_move
