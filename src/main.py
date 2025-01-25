from random import randint

from src.Domain.board import PlayerBoard, ComputerBoard, HeatMap
from src.ui.ui import UI
from src.ui.gui import GUI
from src.Services.services import Service

def main():
    player_board = PlayerBoard()
    computer_board = ComputerBoard()
    service = Service(player_board, computer_board)
    heat_map = HeatMap(player_board, computer_board, increase_factor=1, decrease_factor=0.1)
    #ui = UI(player_board, computer_board, service)
    gui = GUI(player_board, computer_board, service, heat_map, strategy=2)
    gui.run()

if __name__ == '__main__':
    main()