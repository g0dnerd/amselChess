from game import Game
from minimax import Minimax
from mmax import Negamax
import argparse
# Command line interface to test the engine in.


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test the chess engine.')
    parser.add_argument('--depth', type=int, default=10, help='The depth of the minimax algorithm.')
    parser.add_argument('--threads', type=int, default=4, help='The number of threads to use.')
    args = parser.parse_args()
    depth = args.depth
    threads = args.threads
    # Initialize the game
    game = Game()
    # minimax = Negamax(depth)
    minimax = Minimax(depth, threads)

    # Play the game
    while not game.is_game_over():
        # Print the board
        print(game.board)
        choice = input('Enter your move, "x" to let the engine make a move or "q" to quit: ')

        if choice == 'q':
            break
        elif choice == 'x':
            print('Calculating best move...')
            move = minimax.search(game)
            game.make_move(move[0], move[1])
        else:
            try:
                move = choice.split(' ')
                game.make_move(move[0], move[1])
            except:
                print('Invalid move. Try again.')
