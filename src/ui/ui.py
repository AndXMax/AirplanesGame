import os
import random
from time import sleep

from src.Domain.board import BoardExceptions

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class UI:

    def __init__(self, player_board, computer_board, service = None):
        self.player_board = player_board
        self.computer_board = computer_board
        self._service = service

    @staticmethod
    def print_start_screen():
        airplane_art = r"""
                               \ /                                          \   /
                              --o--           `\\             //'      .____-/.\-____.
                                                \\           //             ~`-'~
                                                 \\. __-__ .//
                                       ___/-_.-.__`/~     ~\'__.-._-\___
                .|.       ___________.'__/__ ~-[ \\.'-----'./ ]-~ __\__`.___________       .|.
                ~o~~~~~~~--------______-~~~~~-_/_/ |   .   | \_\_-~~~~~-______--------~~~~~~~o~
                ' `               + + +  (X)(X)  ~--\__ __/--~  (X)(X)  + + +               ' `
                                             (X) `/.' ~ `/.' (X)
                                                 "\_/"   "\_/"
                """
        print(airplane_art)
        print(
            color.BOLD + "----------------------------------------!Welcome to Airplanes!----------------------------------------" + color.END)
        print("--------In this game you have to destroy all the computers airplanes before they destroy yours!-------")
        print("-----If you want to find out more about how you play, type '", end="")
        print(color.BOLD + "help" + color.END, end="")
        print("' in the console and press enter!-----")
        print("--------------Otherwise, to start the game, type '", end="")
        print(color.BOLD + "start" + color.END, end="")
        print("' in the console and press enter!--------------")

    @staticmethod
    def print_help_menu():
        print("First of all, you have to place your airplanes on the board.")
        print(
            "You can do this by typing 'place' and then the coordinates of the head of the airplane and the direction you want to place it in.")
        print(
            "For example, 'place C3 right' will place an airplane starting from C3 and it's body to the right. You can also type 'place G5 down")
        print("So the usage is " + color.BOLD + "'place <head_row><head_column> <direction>'" + color.END + " direction is one of " + color.BOLD + "'up', 'down', 'left', 'right'" + color.END)
        print("You have " + color.BOLD + "3" + color.END + " airplanes to place.")
        print("The games goal is to knock down all the enemies airplanes.")
        print("You can do this by typing 'hit' and then the coordinates of the cell you want to hit.")
        print("For example, 'hit A1' will hit the cell in the first row and first column.")
        print("So the usage is " + color.BOLD + "'hit <row><column>'" + color.END)
        print("To knock down an airplane you need to hit its head")
        print("The game will end when you destroy all the enemies airplanes or when they destroy yours.")
        print("Good luck!")
        print("To start the game, type 'start' and press enter")

    @staticmethod
    def clear_console():
        _ = os.system('cls' if os.name == 'nt' else 'clear')

    def select_players_airplanes(self):
        print("Place your airplanes!!!")
        while self._service.player_board.airplanes > 0:
            #print(self._service.player_board)
            self.print_boards(str(self._service.player_board), str(self._service.computer_board.hidden_board()))
            print("You have " + str(self._service.player_board.airplanes) + " airplanes left to place")
            command = input(">").strip()
            if command == "exit":
                exit()
            try:
                command = command.split(' ')
                if command[0] == "place":
                    if len(command) != 3:
                        print("Invalid command")
                        continue
                    row = ord(command[1][0].upper()) - 64

                    column = int(command[1][1:])
                    direction = command[2]
                    try:
                        self._service.player_board.place_airplane(row, column, direction)
                    except Exception as e:
                        print(e)
                        continue
                else:
                    print("Invalid command")
                    continue
            except Exception as e:
                print(e)
                continue

    def select_computer_airplanes(self):
        while self._service.computer_board.airplanes > 0:
            row = random.randint(1, 10)
            column = random.randint(1, 10)
            direction = random.choice(["up", "down", "left", "right"])
            try:
                self._service.computer_board.place_airplane(row, column, direction)
            except Exception as e:
                continue

    def computer_move(self):
        valid_hit = False
        tries = 0
        while not valid_hit:
            tries += 1
            if len(self._service.player_board.adjacent_list) == 0 or tries > 10:
                row = random.randint(1, 10)
                column = random.randint(1, 10)
            else:
                row, column = random.choice(self._service.player_board.adjacent_list)
            try:
                result = self._service.player_board.hit(row, column)
                sleep(1)
                print("\n\nComputers move is: hit " + chr(row + 64) + str(column))
                if result == 5:
                    print("\nComputer missed!\n")
                elif result == 3:
                    print("\nComputer hit an airplane!\n")
                elif result == 4:
                    print("\nComputer destroyed an airplane!\n")
                    if self._service.player_board.airplanes == 3:
                        print("Computer won!")
                        return True
                valid_hit = True
                #print(str(self._service.player_board.hidden_board()))
                self.print_boards(str(self._service.player_board), str(self._service.computer_board.hidden_board()))
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

    def print_boards(self, first_board, second_board):
        first_board = first_board.split("\n")
        second_board = second_board.split("\n")
        for i in range(0, len(first_board)):
            print(first_board[i] + "           " + second_board[i])


    def run(self):
        self.print_start_screen()
        while True:
            command = input(">").strip()
            if command == "start":
                self.clear_console()
                print("\n" * 5)

                self.select_players_airplanes()
                self.print_boards(str(self._service.player_board), str(self._service.computer_board.hidden_board()))

                self.select_computer_airplanes()
                sleep(1)
                print("\n\nComputer is placing it's airplanes...")
                sleep(1.5)
                print("\n\n...")
                sleep(1)
                print("\n\nSTART GAME!!!\n\n")
                print("Type hit <row><column> to hit a cell\n\n")

                game_over = False

                while not game_over:

                    #get player's move
                    valid_command = False
                    while not valid_command:
                        command = input(">").strip()
                        if command == "exit":
                            return
                        if command == "show computer":
                            print(self._service.computer_board)
                            continue
                        if command == "show player":
                            print(self._service.player_board)
                            continue
                        try:
                            command = command.split(' ')
                            if command[0] == "hit":
                                if len(command) != 2:
                                    print("Invalid command")
                                    continue
                                row = ord(command[1][0].upper()) - 64
                                column = int(command[1][1:])
                                try:
                                    result = self._service.computer_board.hit(row, column)
                                    if result == 5:
                                        print("\nYou missed!\n")
                                    elif result == 3:
                                        print("\nYou hit an airplane!\n")
                                    elif result == 4:
                                        print("\n🎉You destroyed an airplane!🎉\n")
                                        if self._service.computer_board.airplanes == 3:
                                            print("\n\n🎉🎉🎉You won!🎉🎉🎉\n\n")
                                            game_over = True
                                            return
                                    valid_command = True
                                    #print(str(self._service.computer_board.hidden_board()))
                                    self.print_boards(str(self._service.player_board), str(self._service.computer_board.hidden_board()))
                                except BoardExceptions as e:
                                    print(e)
                                    continue
                            else:
                                print("Invalid command")
                                continue
                        except Exception as e:
                            print(e)
                            continue

                    if self.computer_move():
                        print("\n\nYou lost!!!\n\n")
                        exit()


            elif command == "help":
                self.clear_console()
                print("\n" * 5)

                self.print_help_menu()

            elif command == "exit":
                return

            else:
                print("Invalid command")
                continue
