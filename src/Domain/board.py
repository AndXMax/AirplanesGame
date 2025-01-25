import math
import random

from matplotlib.animation import adjusted_figsize
from texttable import Texttable

class BoardExceptions(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

class  OutOfBoundsException(BoardExceptions):
    def __init__(self):
        super().__init__("Airplane is out of bounds")

class AlreadyHitException(BoardExceptions):
    def __init__(self):
        super().__init__("Place is already hit")

class AirplanesBoard:


    def __init__(self, size = 10):
        self._size = size
        self.board = [[0 for _ in range(self._size+1)] for _ in range(self._size+1)]
        # first line is 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        # first column is A, B, C, D, E, F, G, H, I, J
        # 0 is empty, 1 is airplane, 2 is head of airplane, 3 is hit airplane, 4 is hit head of airplane (destroyed), 5 is hit nothing, 6 is hover plane, 7 is hover head plane
        self.init_board()

        self._hits = []
        self._adjacent_to_hits = []
        self.airplanes = 3

    def init_board(self):
        for i in range(1, self._size+1):
            self.board[0][i] = i
            self.board[i][0] = chr(64+i)
        self.board[0][0] = ' '

    @property
    def size(self):
        return self._size


    @property
    def hits_list(self):
        return self._hits

    @property
    def adjacent_list(self):
        return self._adjacent_to_hits

    def add_adjacent_to_hit(self, row, column):
        adjacent = [(row-1, column), (row+1, column), (row, column-1), (row, column+1)]
        for adj in adjacent:
            if adj not in self._hits and self.is_inside_the_grid(adj) and adj not in self.adjacent_list:
                self._adjacent_to_hits.append(adj)

    def remove_cell_from_adjacent_list(self, directions):
        if directions in self._adjacent_to_hits:
            self._adjacent_to_hits.remove(directions)


    def hit(self, row, column):
        if row < 1 or row > self._size or column < 1 or column > self._size:
            raise OutOfBoundsException
        if self.board[row][column] == 3 or self.board[row][column] == 4 or self.board[row][column] == 5:
            raise AlreadyHitException
        if self.board[row][column] == 0:
            self.board[row][column] = 5
            return 5
        elif self.board[row][column] == 1:
            self.board[row][column] = 3
            self._hits.append((row, column))
            self.add_adjacent_to_hit(row, column)
            return 3
        elif self.board[row][column] == 2:
            self.board[row][column] = 4
            self._hits.append((row, column))
            self.airplanes += 1
            return 4


    def is_inside_the_grid(self, coordinates):
        row, column = coordinates[0], coordinates[1]
        return 1 <= row <= self._size and 1 <= column <= self._size

    def are_coordinates_valid(self, airplane_coordinates):
        for coordinates in airplane_coordinates:
            if coordinates[0] < 1 or coordinates[0] > self._size or coordinates[1] < 1 or coordinates[1] > self._size:
                return False
            if not (self.board[coordinates[0]][coordinates[1]] in [0, 6, 7]):
                return False
        return True

    def place_airplane(self, row, column, direction, hover = 0):
        if row < 1 or row > self._size or column < 1 or column > self._size:
            raise OutOfBoundsException
        if direction == "up":
            airplane_coordinates = [(row, column), (row-1, column), (row-1, column-1), (row-1, column+1),
                                    (row-2, column), (row-3, column), (row-3, column-1), (row-3, column+1)]
            if not self.are_coordinates_valid(airplane_coordinates):
                raise Exception("Airplane might collide with another airplane or is out of bounds")


            for coordinates in airplane_coordinates:
                self.board[coordinates[0]][coordinates[1]] = 1 + hover

            self.board[row][column] = 2 + hover

            self.airplanes -= 1

        elif direction == "down":
            airplane_coordinates = [(row, column), (row+1, column), (row+1, column-1), (row+1, column+1),
                                    (row+2, column), (row+3, column), (row+3, column-1), (row+3, column+1)]

            if not self.are_coordinates_valid(airplane_coordinates):
                raise Exception("Airplane might collide with another airplane or is out of bounds")

            for coordinates in airplane_coordinates:
                self.board[coordinates[0]][coordinates[1]] = 1 + hover

            self.board[row][column] = 2 + hover

            self.airplanes -= 1

        elif direction == "left":
            airplane_coordinates = [(row, column), (row, column-1), (row-1, column-1), (row+1, column-1),
                                    (row, column-2), (row, column-3), (row-1, column-3), (row+1, column-3)]

            if not self.are_coordinates_valid(airplane_coordinates):
                raise Exception("Airplane might collide with another airplane or is out of bounds")

            for coordinates in airplane_coordinates:
                self.board[coordinates[0]][coordinates[1]] = 1 + hover

            self.board[row][column] = 2 + hover

            self.airplanes -= 1


        elif direction == "right":
            airplane_coordinates = [(row, column), (row, column+1), (row-1, column+1), (row+1, column+1),
                                    (row, column+2), (row, column+3), (row-1, column+3), (row+1, column+3)]

            if not self.are_coordinates_valid(airplane_coordinates):
                raise Exception("Airplane might collide with another airplane or is out of bounds")

            for coordinates in airplane_coordinates:
                self.board[coordinates[0]][coordinates[1]] = 1 + hover

            self.board[row][column] = 2 + hover

            self.airplanes -= 1
        else:
            raise Exception("Invalid direction")



    # def __str__(self):
    #     t = Texttable()
    #     t.add_row(self.board[0])
    #     for i in range(1, self._size + 1):
    #         row = [self.board[i][0]]
    #         for j in range(1, self._size + 1):
    #             if self.board[i][j] == 0:
    #                 row.append(' ')
    #             elif self.board[i][j] == 1:
    #                 row.append('■')
    #             elif self.board[i][j] == 2:
    #                 row.append('▩')
    #             elif self.board[i][j] == 3:
    #                 row.append('X')
    #             elif self.board[i][j] == 4:
    #                 row.append('☠')
    #         t.add_row(row)
    #     return t.draw()

class PlayerBoard(AirplanesBoard):
    def __init__(self):
        super().__init__()

    def phantom_place(self, row, col, direction):
        if self.board[row][col] != 0:
            return 0
        self.place_airplane(row, col, direction, 5)
        self.airplanes += 1
        self.board[row][col] = 0
        return 1

    def set_row_col_to_val(self, row, col, val):
        self.board[row][col] = val

    def __str__(self):
        t = Texttable()
        t.add_row(self.board[0])
        for i in range(1, self._size + 1):
            row = [self.board[i][0]]
            for j in range(1, self._size + 1):
                if self.board[i][j] == 0:
                    row.append(' ')
                elif self.board[i][j] == 1:
                    row.append('■')
                elif self.board[i][j] == 2:
                    row.append('▩')
                elif self.board[i][j] == 3:
                    row.append('X')
                elif self.board[i][j] == 4:
                    row.append('☠')
                elif self.board[i][j] == 5:
                    row.append('•')
            t.add_row(row)
        return t.draw()

class ComputerBoard(AirplanesBoard):
    def __init__(self):
        super().__init__()
        self.difficulty = 1

    def __str__(self):
        t = Texttable()
        t.add_row(self.board[0])
        for i in range(1, self._size + 1):
            row = [self.board[i][0]]
            for j in range(1, self._size + 1):
                if self.board[i][j] == 0:
                    row.append(' ')
                elif self.board[i][j] == 1:
                    row.append('■')
                elif self.board[i][j] == 2:
                    row.append('▩')
                elif self.board[i][j] == 3:
                    row.append('X')
                elif self.board[i][j] == 4:
                    row.append('☠')
                elif self.board[i][j] == 5:
                    row.append('•')
            t.add_row(row)
        return t.draw()

    def hidden_board(self):
        t = Texttable()
        t.add_row(self.board[0])
        for i in range(1, self._size + 1):
            row = [self.board[i][0]]
            for j in range(1, self._size + 1):
                if self.board[i][j] == 0:
                    row.append(' ')
                elif self.board[i][j] == 1:
                    row.append(' ')
                elif self.board[i][j] == 2:
                    row.append(' ')
                elif self.board[i][j] == 3:
                    row.append('X')
                elif self.board[i][j] == 4:
                    row.append('☠')
                elif self.board[i][j] == 5:
                    row.append('•')
            t.add_row(row)
        return t.draw()

class HeatMap(AirplanesBoard):
    def __init__(self, player_board, computer_board, increase_factor = 0.5, decrease_factor = 0.02):
        super().__init__()
        self._player_board = player_board
        self._computer_board = computer_board
        self._heat_map = [[0.01 for _ in range(self._size)] for _ in range(self._size)]
        self._NULL_ELEMENT = -99999
        self.increase_factor = increase_factor
        self.decrease_factor = decrease_factor

    @staticmethod
    def normalize_list(lst):
        # Step 1: Ensure all elements are positive
        min_value = min(lst, key=lambda x: x[0])[0]
        if min_value < 0:
            lst = [(x[0] - min_value, x[1]) for x in lst]

        # Step 2: Normalize the list so that the sum equals 1
        total = sum(x[0] for x in lst)
        normalized_lst = [(x[0] / total, x[1]) for x in lst]

        return normalized_lst

    def _get_valid_elements_of_heat_map_as_list(self):
        elements = []
        for row in range(self._size):
            for col in range(self._size):
                if self._heat_map[row][col] != self._NULL_ELEMENT:
                    elements.append((self._heat_map[row][col],(row,col)) )
        return elements

    def _get_adjacent_cells(self, row, col):
        adjacent = []
        dx = [-1, 1, 0, 0, -1, -1, 1, 1]
        dy = [0, 0, -1, 1, -1, 1, -1, 1]
        for i in range(len(dx)):
            new_row = row + dx[i]
            new_col = col + dy[i]
            if (0 <= new_row < self._size and 0 <= new_col < self._size and
                    self._heat_map[new_row][new_col] != self._NULL_ELEMENT and self.board[new_row+1][new_col+1] in [0,1,2]):
                adjacent.append((new_row, new_col))
        return adjacent

    def _update_heat_map(self):
        for row in range(self._size):
            for col in range(self._size):
                if self._heat_map[row][col] == self._NULL_ELEMENT:
                    adjacent = self._get_adjacent_cells(row, col)
                    for adj in adjacent:
                        self._heat_map[adj[0]][adj[1]] -= self.decrease_factor

                if self._player_board.board[row+1][col+1] == 3:
                    self._heat_map[row][col] = self._NULL_ELEMENT
                    adjacent = self._get_adjacent_cells(row, col)
                    for adj in adjacent:

                        self._heat_map[adj[0]][adj[1]] += self.increase_factor
                if self._player_board.board[row+1][col+1] in [4, 5]:
                    self._heat_map[row][col] = self._NULL_ELEMENT
                    adjacent = self._get_adjacent_cells(row, col)
                    for adj in adjacent:
                        self._heat_map[adj[0]][adj[1]] -= self.decrease_factor

    @staticmethod
    def pick_random_coordinates(normalized_lst):
        # Use random.choices to pick a value based on the probabilities
        picked_value = random.choices(population=normalized_lst, weights=[x[0] for x in normalized_lst], k=1)[0]
        return picked_value[1]

    def get_mean_of_heat_map(self):
        sum = 0
        nums = 0
        for row in range(self._size):
            for col in range(self._size):
                if self._heat_map[row][col] != self._NULL_ELEMENT:
                    sum += self._heat_map[row][col]
                    nums += 1

        return sum/nums

    def get_best_move(self):
        self._update_heat_map()
        elements = self._get_valid_elements_of_heat_map_as_list()
        normalized_lst = self.normalize_list(elements)
        best_move = self.pick_random_coordinates(normalized_lst)

        return best_move

    @staticmethod
    def get_gradient_color(value, min_val, max_val):
        # Ensure value is within the range
        value = max(min_val, min(value, max_val))

        # Calculate the ratio of the value within the range
        ratio = (value - min_val) / (max_val - min_val)

        # Apply logarithmic scaling to the ratio
        if ratio > 0:
            log_ratio = math.log(ratio + 1) / math.log(2)
        else:
            log_ratio = 0

        # Calculate the RGB values for pink (255, 192, 203) to red (255, 0, 0)
        red = 255
        green = int(192 * (1 - log_ratio))
        blue = int(203 * (1 - log_ratio))

        return (red, green, blue)

    def get_color(self, row, col):
        self._update_heat_map()
        elements = self._get_valid_elements_of_heat_map_as_list()
        normalized_lst = self.normalize_list(elements)

        #get color gradient from white to red of color depending on the heat map value (white is the min of normalized_lst, red is the max)
        min_value = min(normalized_lst, key=lambda x: x[0])[0]
        max_value = max(normalized_lst, key=lambda x: x[0])[0]
        #check if (row,col) is in normalized_lst[i][1]
        index = -1
        for i in range(len(normalized_lst)):
            if normalized_lst[i][1] == (row, col):
                index = i
                break
        if index == -1:
            return (0,0,0)

        value = normalized_lst[index][0]

        color = self.get_gradient_color(value, min_value, max_value)

        return color






