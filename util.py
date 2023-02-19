# Contains some utility functions for the project

def square_to_coordinates(square):
    """Convert a square on the chessboard to coordinates. (0,0) corresponds to a1 and (7,7) corresponds to h8"""
    x = ord(square[0]) - ord('a')
    y = int(square[1]) - 1
    return x, y


def coordinates_to_square(x, y):
    """Convert coordinates to a square on the chessboard. (0,0) corresponds to a1 and (7,7) corresponds to h8"""
    square = f"{chr(ord('a') + x)}{y + 1}"
    return square
