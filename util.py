# Contains some utility functions for the project

def square_to_coordinates(square):
    """Convert a square on the chessboard to coordinates.
    a1 is (0, 7), h1 is (7, 7), a8 is (0, 0) and h8 is (7, 0)"""
    x = ord(square[0]) - ord('a')
    y = 8 - int(square[1])

    return x, y


def coordinates_to_square(x, y):
    """Convert coordinates to a square on the chessboard.
    a1 is (0, 7), h1 is (7, 7), a8 is (0, 0) and h8 is (7, 0)"""
    square = f"{chr(ord('a') + x)}{8 - y}"

    return square


def get_opponent_color(color):
    """Return the opponent's color"""
    if color == 'white':
        return 'black'
    else:
        return 'white'


def export_pgn(game):
    """Export a game to a PGN file"""
    # Create a PGN file
    pgn = open(f"./game.pgn", "w")
    # Write the game to the PGN file
    pgn.write(game.pgn)
    pgn.close()
