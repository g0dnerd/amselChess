from concurrent.futures import ThreadPoolExecutor, as_completed
from amsel_engine import Engine


def order_moves(state):
    legal_moves = state.get_valid_moves()
    if len(legal_moves) <= 1:
        return legal_moves
    else:
        ordered_moves = []
        for i, move in enumerate(legal_moves):
            if state.is_capture(move):
                ordered_moves.insert(i, move)
            else:
                ordered_moves.append(move)
        return ordered_moves


class Minimax:
    MAX_DEPTH = 3
    THREADS = 4

    def __init__(self):
        self.engine = Engine()

    def minimax(self, state, depth, alpha, beta, maximizing_player, path=None):
        if path is None:
            path = []
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_position(state), None
        if maximizing_player:
            best_value = float('-inf')
            best_move = None
            with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
                futures = []
                for move in order_moves(state):
                    new_state = state.apply_move(move[0], move[1])
                    new_path = path + [move]
                    futures.append(executor.submit(self.minimax, new_state, depth - 1, alpha, beta, False, new_path))
                for future in futures:
                    value, _ = future.result()
                    print('Result obtained')
                    if value > best_value:
                        best_value = value
                        best_move = future.arg
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        print('Pruning')
                        break
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
                futures = []
                for move in order_moves(state):
                    new_state = state.apply_move(move[0], move[1])
                    new_path = path + [move]
                    futures.append(executor.submit(self.minimax, new_state, depth - 1, alpha, beta, True, new_path))
                for future in futures:
                    value, _ = future.result()
                    print('Result obtained')
                    if value < best_value:
                        best_value = value
                        best_move = future.arg
                    beta = min(beta, value)
                    if alpha >= beta:
                        print('Pruning')
                        break
            return best_value, best_move

    def find_best_move(self, state):
        _, best_move = self.minimax(state, self.MAX_DEPTH, float('-inf'), float('inf'), True)
        return best_move
