from concurrent.futures import ProcessPoolExecutor as Pool
from itertools import repeat
from multiprocessing import current_process
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
            for move in order_moves(state):
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                print('Simulating move', move, 'at depth', self.MAX_DEPTH - depth + 1, 'with path', new_path)
                value, _ = self.minimax(new_state, depth - 1, alpha, beta, False, new_path)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    print('Pruning')
                    break
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in order_moves(state):
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                print('Simulating move', move, 'at depth', self.MAX_DEPTH - depth + 1, 'with path', new_path)
                value, _ = self.minimax(new_state, depth - 1, alpha, beta, True, new_path)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    print('Pruning')
                    break
            return best_value, best_move

    def find_best_move(self, state):
        _, best_move = self.minimax(state, self.MAX_DEPTH, float('-inf'), float('inf'), True)
        return best_move


class Multimax:
    MAX_DEPTH = 3
    NUM_WORKERS = 4

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
            with Pool(max_workers=self.NUM_WORKERS) as pool:
                print('Pool created')
                for move in order_moves(state):
                    print(
                        f'Current process: {current_process().name}, depth: {self.MAX_DEPTH - depth + 1}, move: {move}')
                    new_state = state.apply_move(move[0], move[1])
                    new_path = path + [move]
                    print('New state created')
                    value, _ = pool.map(self.minimax_worker,
                                        zip(repeat(new_state), repeat(depth - 1), repeat(alpha), repeat(beta),
                                            repeat(False), repeat(new_path)))
                    print('Comparing values')
                    if value > best_value:
                        best_value = value
                        best_move = move
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
                    if move == order_moves(state)[0]:
                        print(f'Depth: {self.MAX_DEPTH - depth + 1}, best move: {best_move}')
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            with Pool(max_workers=self.NUM_WORKERS) as pool:
                for move in order_moves(state):
                    new_state = state.apply_move(move[0], move[1])
                    new_path = path + [move]
                    value, _ = pool.map(self.minimax_worker,
                                        zip(repeat(new_state), repeat(depth - 1), repeat(alpha), repeat(beta),
                                            repeat(True), repeat(new_path)))
                    if value < best_value:
                        best_value = value
                        best_move = move
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
                    if move == order_moves(state)[0]:
                        print(f'Depth: {self.MAX_DEPTH - depth + 1}, best move: {best_move}')
            return best_value, best_move

    def minimax_worker(self, state, depth, alpha, beta, maximizing_player, path=None):
        print('Worker started at depth', depth)
        if path is None:
            path = []
        return self.minimax(state, depth, alpha, beta, maximizing_player, path)

    def find_best_move(self, state):
        _, best_move = self.minimax(state, self.MAX_DEPTH, float('-inf'), float('-inf'), True)[1]
        print('Best move:', best_move)
        return best_move
