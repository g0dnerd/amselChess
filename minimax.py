import concurrent.futures
from multiprocessing import Manager
from amsel_engine import Engine
from dataclasses import dataclass
import time
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
    BATCH_SIZE = 2

    def __init__(self):
        self.engine = Engine()
        self.results = []
        self.lock = Manager().Lock()

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
                    best_move = move
                    print(f'Pruning {new_path} at depth {self.MAX_DEPTH - depth} with value {value}')
                    break
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in order_moves(state):
                print(f'Processing state {state.move_history} at depth {self.MAX_DEPTH - depth}')
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                value, _ = self.minimax(new_state, depth - 1, mm_values, True, new_path)
                if value < best_value:
                    best_value = value
                    best_move = move
                mm_values.beta = min(mm_values.beta, value)
                if mm_values.alpha >= mm_values.beta:
                    best_move = move
                    print(f'Pruning {new_path} at depth {depth} with value {value}')
                    break
            return best_value, best_move

    def process_result(self, move, result, mm_values):
        value, _ = result
        if value > mm_values.alpha:
            mm_values.alpha = value
        if value > 1000:
            mm_values.beta = 10000
        result_tuple = (move, value)
        with self.lock:
            self.results.append(result_tuple)

    def find_best_move(self, state):
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.THREADS) as thread_executor, \
                concurrent.futures.ProcessPoolExecutor() as process_executor:
            mm_values = MinMaxValues()
            initial_moves = order_moves(state)
            batches = [initial_moves[i:i + self.BATCH_SIZE] for i in range(0, len(initial_moves), self.BATCH_SIZE)]
            futures = []
            for batch in batches:
                print('Spawning processes for batch', batch)
                processes = []
                for move in batch:
                    new_state = state.apply_move(move[0], move[1])
                    process = process_executor.submit(
                        self.minimax, new_state, self.MAX_DEPTH - 1, mm_values, True, [move])
                    processes.append((move, process))
                for move, process in processes:
                    futures.append(thread_executor.submit(self.process_result, move, process, mm_values))
            concurrent.futures.wait(futures)
            best_value = float('-inf')
            best_move = None
            for move, result in self.results:
                value, _ = result.result()
                if value > best_value:
                    best_value = value
                    best_move = move
                mm_values.alpha = max(mm_values.alpha, value)
            total_time = time.time() - start_time
            print(f'Found move {best_move} in {total_time:.4f} seconds')
            return best_move
