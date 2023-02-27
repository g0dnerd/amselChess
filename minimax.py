from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from amsel_engine import Engine
from dataclasses import dataclass

PIECE_VALUES = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000
}


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
        # Then, order by piece mobility
        piece_mobility_scores = {}
        for move in legal_moves:
            piece = state.board.get_piece_by_square(move[0]).type
            if piece in piece_mobility_scores:
                piece_mobility_scores[piece] += PIECE_VALUES[piece]
            else:
                piece_mobility_scores[piece] = PIECE_VALUES[piece]
        ordered_moves += sorted(legal_moves,
                                key=lambda move: piece_mobility_scores.get(
                                    state.board.get_piece_by_square(move[0]).type, 0), reverse=True)
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
        with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
            mm_values = MinMaxValues()
            results = []
            initial_moves = order_moves(state)
            for move in initial_moves:
                # print(f'Processing move {move}')
                new_state = state.apply_move(move[0], move[1])
                result = executor.submit(
                    self.minimax, new_state, self.MAX_DEPTH - 1, mm_values, True, [move])
                results.append((move, result))
            best_value = float('-inf')
            best_move = None
            for move, result in results:
                value, _ = result.result()
                if value > best_value:
                    best_value = value
                    best_move = move
                mm_values.alpha = max(mm_values.alpha, value)
            return best_move

