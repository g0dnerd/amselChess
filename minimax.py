import concurrent.futures
import threading
from amsel_engine import Engine
from dataclasses import dataclass
import util
import random


@dataclass
class MinMaxValues:
    def __init__(self):
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
    def __init__(self, max_depth, threads):
        self.engine = Engine()
        self.max_depth = max_depth
        self.threads = threads
        self.lock = threading.Lock()

    def alphabeta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_for_maximizing_player(state), None

        if maximizing_player:
            value = float('-inf')
            best_move = None
            futures = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                for move in order_moves(state):
                    child_state = state.apply_move(move[0], move[1])
                    print('Starting thread for move', child_state.move_history)
                    futures.append(executor.submit(self.alphabeta, child_state, depth-1, alpha, beta, False))
                for future in concurrent.futures.as_completed(futures):
                    result, _ = future.result()
                    with self.lock:
                        value = max(value, result)
                        if value > alpha:
                            alpha = value
                            best_move = futures[futures.index(future)].result()[1]
                        if alpha >= beta:
                            print('Pruning')
                            break
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            futures = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                for move in order_moves(state):
                    child_state = state.apply_move(move[0], move[1])
                    print('Starting thread for move', child_state.move_history)
                    futures.append(executor.submit(self.alphabeta, child_state, depth-1, alpha, beta, True))
                for future in concurrent.futures.as_completed(futures):
                    result, _ = future.result()
                    with self.lock:
                        value = min(value, result)
                        if value < beta:
                            beta = value
                            best_move = futures[futures.index(future)].result()[1]
                        if alpha >= beta:
                            print('Pruning')
                            break
            return value, best_move

    def search(self, state):
        _, best_move = self.alphabeta(state, self.max_depth, float('-inf'), float('inf'), True)
        return best_move
