# This file contains the GUI class, which provides a graphical user interface for the chess engine.
# It displays the board and allows the user to click and drag pieces to make moves.

import pygame
import pygame.freetype
import util


class PygameGUI:
    def __init__(self, game):
        pygame.freetype.init()
        self.dark_square_color = (209, 139, 71)
        self.light_square_color = (255, 206, 158)
        self.SCREEN_HEIGHT = 640
        self.BUTTON_COLOR = (100, 100, 100)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.SCREEN_WIDTH = 1280
        self.button_hover_color = self.dark_square_color
        self.cell_size = 80
        self.game = game
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.label_font = pygame.freetype.Font('./assets/fonts/Roboto-Bold.ttf', 16)
        self.annotation_font = pygame.freetype.Font('./assets/fonts/Roboto-Regular.ttf', 16)

        self.buttons = {
            'square_color': {
                'rect': pygame.Rect(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2 + 100, 200, 50),
                'text': 'Change Square Color',
                'color': self.BUTTON_COLOR,
                'function': self.toggle_square_color
            },
            'export_pgn': {
                'rect': pygame.Rect(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2 + 200, 200, 50),
                'text': 'Export PGN',
                'color': self.BUTTON_COLOR,
                'function': self.export_pgn
            }
        }

    def draw_board(self):
        """Draws the chess board using .png files in the /assets folder.
        Draws the pieces starting from the bottom left corner of the board."""
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    square_color = self.light_square_color
                else:
                    square_color = self.dark_square_color
                pygame.draw.rect(self.screen, square_color,
                                 (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size))

                # Draw file and rank labels
                if i == 7:
                    # draw file labels to the bottom most row of the board in the bottom right corner of the squares
                    font_color = self.light_square_color if square_color == \
                                                            self.dark_square_color else self.dark_square_color
                    label, _ = self.label_font.render(chr(ord('a') + j), font_color)
                    label_rect = label.get_rect(center=((j + 0.85) * self.cell_size,
                                                        (self.cell_size * 7) + self.cell_size * 0.9))
                    self.screen.blit(label, label_rect)
                if j == 0:
                    # draw rank labels on the left side of the board in the top left corner of the squares
                    font_color = self.light_square_color if square_color == \
                                                            self.dark_square_color else self.dark_square_color
                    label, _ = self.label_font.render(str(8 - i), font_color)
                    label_rect = label.get_rect(center=(self.cell_size * 0.1, (i + 0.15) * self.cell_size))
                    self.screen.blit(label, label_rect)

                piece = self.game.board.get_piece_by_coordinates(i, j)
                if piece is not None:
                    piece_image = pygame.image.load(f'assets/pieces/{piece.color}_{piece.type}.png')
                    piece_image = pygame.transform.scale(piece_image, (self.cell_size, self.cell_size))
                    self.screen.blit(piece_image, (i * self.cell_size, j * self.cell_size))

    def export_pgn(self):
        """Exports the game's PGN to a file."""
        util.export_pgn(self.game)

    def toggle_square_color(self):
        if self.light_square_color == (255, 206, 158):
            self.light_square_color = (238, 238, 210)
            self.dark_square_color = (118, 150, 86)
        else:
            self.light_square_color = (255, 206, 158)
            self.dark_square_color = (209, 139, 71)
        self.button_hover_color = self.dark_square_color

    def update_board(self, board):
        self.game.board = board
        self.draw_board()

    def draw_buttons(self):
        for button in self.buttons.values():
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            text, _ = self.label_font.render(button['text'], self.BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

            if button['rect'].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, self.button_hover_color, button['rect'])
                text, _ = self.label_font.render(button['text'], self.BUTTON_TEXT_COLOR)
                text_rect = text.get_rect(center=button['rect'].center)
                self.screen.blit(text, text_rect)

    def update_annotations(self, game):
        """Updates the annotations in the right half of the screen.
        Annotations include the current player, the move history and the game result."""
        # print('Updating annotations')

        # set up current player text
        current_player_text, _ = self.annotation_font.render(
            f'Current player: {self.game.current_player}', (255, 255, 255))
        current_player_rect = current_player_text.get_rect(
            midleft=(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2 - 50))

        # set up PGN text
        pgn_text, _ = self.annotation_font.render(f'PGN: {self.game.pgn}', (255, 255, 255))
        pgn_rect = pgn_text.get_rect(midleft=(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2))

        # set up game result text
        game_result = self.game.get_game_result()
        if game_result == 'checkmate':
            if self.game.current_player == 'white':
                game_result = 'black wins!'
            else:
                game_result = 'white wins!'
        game_result_text, _ = self.annotation_font.render(f'Game Result: {game_result}', (255, 255, 255))
        game_result_rect = game_result_text.get_rect(midleft=(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT // 2 + 50))

        # draw background color over the right half of the screen
        pygame.draw.rect(self.screen, (67, 69, 74), (
            self.SCREEN_WIDTH // 2, 0, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT))

        self.screen.blit(current_player_text, current_player_rect)
        self.screen.blit(pgn_text, pgn_rect)
        self.screen.blit(game_result_text, game_result_rect)

    def display_promotion_interface(self, position):
        # TODO
        pass

    def is_mouse_on_board(self, x, y):
        """Checks if the mouse is within the bounds of the board."""
        return 0 <= x <= self.SCREEN_WIDTH // 2 and 0 <= y <= self.SCREEN_HEIGHT

    def run(self):
        """Runs the GUI."""
        pygame.init()
        pygame.display.set_caption('amselChess 0.0.1')
        clock = pygame.time.Clock()

        running = True
        dragging = False
        selected_piece = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click is within the bounds of the board
                    if not self.is_mouse_on_board(event.pos[0], event.pos[1]):
                        # Check if a button was clicked
                        for button in self.buttons.values():
                            if button['rect'].collidepoint(event.pos):
                                button['function']()
                    else:
                        pos = pygame.mouse.get_pos()
                        x, y = self.mouse_to_board_coordinates(pos[0], pos[1])
                        piece = self.game.board.get_piece_by_coordinates(x, y)
                        if piece is not None and piece.color == self.game.current_player:
                            selected_piece = piece
                            dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        pos = pygame.mouse.get_pos()
                        x, y = self.mouse_to_board_coordinates(pos[0], pos[1])
                        # Check if it's the turn of the player who owns the selected piece
                        if selected_piece.color != self.game.current_player:
                            print('Not your turn')
                            selected_piece = None
                            dragging = False
                            continue
                        # Check if the move is valid
                        if self.game.is_valid_move(selected_piece.square, util.coordinates_to_square(x, y)):
                            self.game.make_move(selected_piece.square, util.coordinates_to_square(x, y))
                            # if the move was a pawn promotion
                            if self.game.promotion:
                                self.display_promotion_interface((x, y))
                                continue
                        else:
                            print('Illegal move')
                        selected_piece = None
                        dragging = False

                self.update_board(self.game.board)
                self.update_annotations(self.game)
                self.draw_buttons()
                pygame.display.flip()
                clock.tick(60)

        pygame.quit()

    def mouse_to_board_coordinates(self, mouse_x, mouse_y):
        """Converts mouse coordinates to board coordinates."""
        return mouse_x // self.cell_size, mouse_y // self.cell_size
