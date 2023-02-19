# This file contains the Player class, which represents a human player of the game.
# It includes methods for getting input from the user and making moves on the board.

class Player:
    def __init__(self, color):
        self.color = color

    def get_opponent_color(self):
        if self.color == 'white':
            return 'black'
        else:
            return 'white'
