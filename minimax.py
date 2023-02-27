from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from amsel_engine import Engine

PIECE_VALUES = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000
}


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
    MAX_DEPTH = 5
    THREADS = 6

    def __init__(self):
        self.engine = Engine()
        self.history = defaultdict(list)

    def minimax(self, state, depth, alpha, beta, maximizing_player, path=None):
        if path is None:
            path = []
        if depth == 0 or state.is_game_over():
            return self.engine.evaluate_position(state), None
        if maximizing_player:
            best_value = float('-inf')
            best_move = None
            for move in order_moves(state):
                print(f'Processing state {state.move_history} at depth {depth}')
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                value, _ = self.minimax(new_state, depth - 1, alpha, beta, False, new_path)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    print(f'Pruning {new_path} at depth {depth} with value {value}')
                    break
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in order_moves(state):
                new_state = state.apply_move(move[0], move[1])
                new_path = path + [move]
                value, _ = self.minimax(new_state, depth - 1, alpha, beta, True, new_path)
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    print(f'Pruning {new_path} at depth {depth} with value {value}')
                    break
            return best_value, best_move

    def find_best_move(self, state):
        with ThreadPoolExecutor(max_workers=self.THREADS) as executor:
            results = []
            for move in state.get_valid_moves():
                print(f'Processing move {move}')
                result = executor.submit(self.minimax, state.apply_move(move[0], move[1]), self.MAX_DEPTH - 1,
                                         float('-inf'), float('inf'), False, [move])
                results.append(result)
            best_value = float('-inf')
            best_move = None
            for result in results:
                value, move = result.result()
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move
