from game import Game
from minimax import Minimax

# Command line interface to test the engine in.


if __name__ == "__main__":
    # Initialize the game
    game = Game()
    minimax = Minimax()

    # Play the game
    while not game.is_game_over():
        # Print the board
        print(game.board)

        # If it's white's turn, get input from the user
        if game.current_player == 'white':
            move = input('Enter your move: ')
            move = move.split(' ')
            game.make_move((move[0]), (move[1]))
            continue
        else:
            print('Computer is thinking...')
            # Get the best move
            move = minimax.find_best_move(game)
            # Make the move
            game.make_move(move[0], move[1])
