from random import randint
from src.Domain.board import PlayerBoard

import pygame
import random

# Constants
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 550
CELL_SIZE = 30
MARGIN = 5
BOARD_OFFSET = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (173, 216, 230)
DARK_GRAY = (90, 90, 90)
GRAY = (200, 200, 200)

class GUI:

    @staticmethod
    def convert_pos_to_row_col(x, y):
        row = (y - BOARD_OFFSET) // (CELL_SIZE + MARGIN)
        col = (x - BOARD_OFFSET) // (CELL_SIZE + MARGIN)
        return row, col

    def convert_pos_to_row_col_second_board(self, x, y):
        row = (y - BOARD_OFFSET) // (CELL_SIZE + MARGIN)
        col = (x - (BOARD_OFFSET + (CELL_SIZE + MARGIN) * self._player_board.size + BOARD_OFFSET)) // (CELL_SIZE + MARGIN)
        return row, col

    def __init__(self, player_board, computer_board, service, heat_map = None, strategy = 1):
        self._player_board = player_board
        self._computer_board = computer_board
        self._service = service
        self._heat_map = heat_map
        self._strategy = strategy
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Airplanes Game")
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.placing_airplanes = True
        background_path = f"Pictures/background{randint(1,5)}.jpg"
        self.background_image = pygame.image.load(background_path)
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.button_rect = pygame.Rect(10, 10, 150, 50)  # Button position and size

    def show_game_over_screen(self, winner):
        self.screen.fill((0, 0, 0))  # Fill the screen with black

        # Load the appropriate game over image based on the winner
        if winner == "user":
            game_over_image_path = f"Pictures/PlayerWin3.jpg"
        else:
            game_over_image_path = f"Pictures/ComputerWin3.jpeg"

        game_over_image = pygame.image.load(game_over_image_path)
        game_over_image = pygame.transform.scale(game_over_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Blit the image onto the screen
        self.screen.blit(game_over_image, (0, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting = False

    def draw_fading_button_background(self, rect):
        for i in range(rect.height):
            color_intensity = int(255 * (i / rect.height))
            color = (color_intensity, color_intensity, color_intensity)
            pygame.draw.line(self.screen, color, (rect.left, rect.top + i), (rect.right, rect.top + i))

    def show_start_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        play_button_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        play_button_radius = 50
        # Draw the circle
        pygame.draw.circle(self.screen, WHITE, play_button_center, play_button_radius)
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Play", True, BLACK)
        text_rect = text_surface.get_rect(center=play_button_center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (mouse_x - play_button_center[0]) ** 2 + (
                            mouse_y - play_button_center[1]) ** 2 <= play_button_radius ** 2:
                        waiting = False


    def draw_moves(self, moves, x, y):
        max_moves = (WINDOW_HEIGHT - y) // 30 - 3  # Calculate the maximum number of moves that can be displayed
        start_index = max(0, len(moves) - max_moves)  # Determine the starting index to display moves

        for i, (move, outcome) in enumerate(moves[start_index:]):
            move_text = f"{chr(move[0] + 64)}{move[1]}"
            self.draw_text(move_text, x, y + (i + 1) * 30)
            color = WHITE
            if outcome == "missed":
                color = WHITE
            elif outcome == "hit":
                color = RED
            elif outcome == "destroyed":
                color = GREEN
            self.draw_text(outcome, x + 50, y + (i + 1) * 30, color)

    def draw_text(self, text, x, y, color=WHITE):
        font = pygame.font.Font(None, 36)
        text1 = font.render(text, True, color)
        self.screen.blit(text1, (x, y))

    def draw_moves_title(self):
        self.draw_text("Player moves", BOARD_OFFSET + 800, 50)
        self.draw_moves(self._service.player_moves, BOARD_OFFSET + 800, 50)
        self.draw_text("Computer moves", BOARD_OFFSET + 1000, 50)
        self.draw_moves(self._service.computer_moves, BOARD_OFFSET + 1000, 50)

    def draw_toggle_heat_map_button(self):
        pygame.draw.rect(self.screen, (255, 165, 0), self.button_rect)  # Orange button
        font = pygame.font.Font(None, 24)  # Smaller font size
        text = font.render("Toggle HeatMap", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)


    def update_screen(self, heat_map_toggled = False):
        self.screen.fill(BLACK)
        if heat_map_toggled:
            self.draw_board(self._player_board, BOARD_OFFSET, BOARD_OFFSET, heat_map_toggled=True)
        else:
            self.draw_board(self._player_board, BOARD_OFFSET, BOARD_OFFSET)
        self.draw_board(self._computer_board, BOARD_OFFSET + 400, BOARD_OFFSET, hidden=True)
        self.draw_moves_title()

        # Draw the button
        if self._strategy == 2:
            self.draw_toggle_heat_map_button()

        pygame.display.flip()


    def draw_board(self, board, offset_x, offset_y, hidden=False, heat_map_toggled = False):
        for row in range(1, board.size + 1):
            for col in range(1, board.size + 1):
                cell_value = board.board[row][col]
                color = WHITE
                if cell_value == 1 and not hidden:
                    color = BLUE
                elif cell_value == 2 and not hidden:
                    color = GREEN
                elif cell_value == 3:
                    color = RED
                elif cell_value == 4:
                    color = BLACK
                elif cell_value == 5:
                    color = GRAY
                elif cell_value == 6:
                    color = LIGHT_BLUE
                elif cell_value == 7:
                    color = LIGHT_GREEN
                if heat_map_toggled == True and isinstance(board, PlayerBoard):
                    if color == RED:
                        color = BLUE
                    if color == BLACK:
                        continue
                    if color == GRAY:
                        color = DARK_GRAY
                    else:
                        color = self._heat_map.get_color(row-1, col-1)
                pygame.draw.rect(self.screen, color,
                                 [(MARGIN + CELL_SIZE) * col + offset_x,
                                  (MARGIN + CELL_SIZE) * row + offset_y,
                                  CELL_SIZE, CELL_SIZE])

    def place_computer_airplanes(self):
        while self._service.computer_board.airplanes > 0:
            row = random.randint(1, 10)
            column = random.randint(1, 10)
            direction = random.choice(["up", "down", "left", "right"])
            try:
                self._service.computer_board.place_airplane(row, column, direction)
            except Exception as e:
                continue


    def place_hovered_airplane(self, row, col):
        if self._service.player_board.airplanes > 0:
            planes_placed = self._service.place_all_possible_airplanes(row, col)
            if planes_placed == 0:
                return False

            self.update_screen()

            #wait until the player clicks on one of the drawn airplanes
            airplane_selected = False
            while not airplane_selected:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        airplane_selected = True
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        airplane_row, airplane_col = self.convert_pos_to_row_col(mouse_x, mouse_y)
                        if 1 <= airplane_row <= 10 and 1 <= airplane_col <= 10:
                            if self._service.player_board.board[airplane_row][airplane_col] == 6:
                                #find the direction of the airplane from row,col - head of the airplane, airplane_row, airplane_col get the direction
                                direction = ""
                                if airplane_row > row and (airplane_col == col or airplane_col == col + 1 or airplane_col == col - 1):
                                    direction = "down"
                                elif airplane_row < row and (airplane_col == col or airplane_col == col + 1 or airplane_col == col - 1):
                                    direction = "up"
                                elif airplane_col > col and (airplane_row == row or airplane_row == row + 1 or airplane_row == row - 1):
                                    direction = "right"
                                elif airplane_col < col and (airplane_row == row or airplane_row == row + 1 or airplane_row == row - 1):
                                    direction = "left"
                                #delete all the 6s and 7s from the _board and place an airplane at (row,col,direction)
                                for i in range(1, 11):
                                    for j in range(1, 11):
                                        if self._service.player_board.board[i][j] == 6 or self._service.player_board.board[i][j] == 7:
                                            self._service.player_board.board[i][j] = 0
                                self._service.player_board.place_airplane(row, col, direction)
                                return True
            return False

        else:
            raise Exception("You can't place more airplanes")

    def computer_move(self):
        valid_hit = False
        while not valid_hit:
            row, column = 0, 0
            if self._strategy == 1:
                if len(self._service.player_board.adjacent_list) == 0:
                    row = random.randint(1, 10)
                    column = random.randint(1, 10)
                else:
                    row, column = random.choice(self._service.player_board.adjacent_list)
            if self._strategy == 2:
                row, column = self._heat_map.get_best_move()
                row += 1
                column += 1
            try:
                result = self._service.player_board.hit(row, column)
                print("\n\nComputers move is: hit " + chr(row + 64) + str(column))
                outcome = ""
                if result == 5:
                    print("\nComputer missed!\n")
                    outcome = "missed"
                elif result == 3:
                    print("\nComputer hit an airplane!\n")
                    outcome = "hit"
                elif result == 4:
                    print("\nComputer destroyed an airplane!\n")
                    outcome = "destroyed"
                    if self._service.player_board.airplanes == 3:
                        print("Computer won!")
                        self.show_game_over_screen("computer")
                        return True
                valid_hit = True
                self._service.computer_moves.append(((row, column), outcome))

            except Exception:
                try:
                    self._service.player_board.remove_cell_from_adjacent_list((row, column))
                except Exception:
                    continue
                continue
            try:
                self._service.player_board.remove_cell_from_adjacent_list((row, column))
            except Exception:
                continue

    def handle_click(self, mouse_x, mouse_y):
        if self.placing_airplanes:
            # Determine the clicked cell for placing airplanes
            row, col = self.convert_pos_to_row_col(mouse_x, mouse_y)
            board_size = self._service.player_board.size
            if 1 <= row <= board_size and 1 <= col <= board_size:
                try:
                    placed = self.place_hovered_airplane(row, col)
                    if not placed:
                        return

                    if self._service.player_board.airplanes == 0:
                        self.placing_airplanes = False
                except Exception as e:
                    print(e)
        else:
            # Determine the clicked cell for making moves
            # this will be on the second board
            row, col = self.convert_pos_to_row_col_second_board(mouse_x, mouse_y)
            if 1 <= row <= 10 and 1 <= col <= 10:
                try:
                    result = self._service.computer_board.hit(row, col)
                    outcome = ""
                    if result == 5:
                        print("\nYou missed!\n")
                        outcome = "missed"
                    elif result == 3:
                        print("\nYou hit an airplane!\n")
                        outcome = "hit"
                    elif result == 4:
                        print("\n🎉You destroyed an airplane!🎉\n")
                        outcome = "destroyed"
                        if self._service.computer_board.airplanes == 3:
                            print("\n\n🎉🎉🎉You won!🎉🎉🎉\n\n")
                            self.show_game_over_screen("user")
                            self.running = False
                    # add move to players moves
                    self._service.player_moves.append(((row, col), outcome))

                    # Computer's turn
                    if self.running:
                        self.computer_move()
                        if self._service.player_board.airplanes == 3:
                            # print("Computer won!")
                            self.running = False

                except Exception as e:
                    print(e)

    def toggle_heatmap(self):
        if self._heat_map is None:
            return

        self.update_screen(heat_map_toggled=True)

        toggled = True
        while toggled:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    toggled = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.button_rect.collidepoint(mouse_x, mouse_y):
                        toggled = False
                        break

    def run(self):
        self.show_start_menu()
        if not self.running:
            return

        self.place_computer_airplanes()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.button_rect.collidepoint(mouse_x, mouse_y):
                        self.toggle_heatmap()
                    else:
                        self.handle_click(mouse_x, mouse_y)

            self.update_screen()

        pygame.quit()

# if __name__ == '__main__':
#     player_board = PlayerBoard()
#     computer_board = ComputerBoard()
#     gui = GUI(player_board, computer_board)
#     gui.run()