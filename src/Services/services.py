class Service:
    def __init__(self, player_board, computer_board):
        self._player_board = player_board
        self._computer_board = computer_board
        self.player_moves = []
        self.computer_moves = []

    @property
    def player_board(self):
        return self._player_board

    @property
    def computer_board(self):
        return self._computer_board

    def place_all_possible_airplanes(self, row, column):
        airplanes_placed = 0
        for direction in ["up", "down", "left", "right"]:
            try:
                self._player_board.phantom_place(row, column, direction)
                airplanes_placed += 1
            except Exception:
                pass
        if airplanes_placed != 0:
            self._player_board.set_row_col_to_val(row, column, 7)
        return airplanes_placed
