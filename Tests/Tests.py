import unittest
from src.Domain.board import PlayerBoard
from src.Services.services import Service
from src.Domain.board import ComputerBoard, OutOfBoundsException, AlreadyHitException

from src.Domain.board import AirplanesBoard

class TestAirplanesBoard(unittest.TestCase):
    def test_hit(self):
        board = AirplanesBoard()
        board.place_airplane(2, 2, 'down')
        result = board.hit(2, 2)
        self.assertTrue(result)

class TestPlayerBoard(unittest.TestCase):

    def setUp(self):
        self.board = PlayerBoard()

    def test_str(self):
        board = PlayerBoard()
        self.assertIsInstance(str(board), str)

    def test_initial_board(self):
        self.assertEqual(self.board.size, 10)
        self.assertEqual(len(self.board.board), 11)
        self.assertEqual(len(self.board.board[0]), 11)

    def test_place_airplane(self):
        self.board.place_airplane(5, 5, "up")
        self.assertEqual(self.board.board[5][5], 2)
        self.assertEqual(self.board.board[4][5], 1)

    def test_place_airplane_out_of_bounds(self):
        with self.assertRaises(OutOfBoundsException):
            self.board.place_airplane(11, 11, "up")

    def test_hit_airplane(self):
        self.board.place_airplane(5, 5, "up")
        result = self.board.hit(5, 5)
        self.assertEqual(result, 4)

    def test_hit_empty(self):
        result = self.board.hit(1, 1)
        self.assertEqual(result, 5)

    def test_hit_already_hit(self):
        self.board.place_airplane(5, 5, "up")
        self.board.hit(5, 5)
        with self.assertRaises(AlreadyHitException):
            self.board.hit(5, 5)

class TestComputerBoard(unittest.TestCase):

    def setUp(self):
        self.board = ComputerBoard()


    def test_str(self):
        board = ComputerBoard()
        self.assertIsInstance(str(board), str)

    def test_initial_board(self):
        self.assertEqual(self.board.size, 10)
        self.assertEqual(len(self.board.board), 11)
        self.assertEqual(len(self.board.board[0]), 11)

    def test_place_airplane(self):
        self.board.place_airplane(5, 5, "up")
        self.assertEqual(self.board.board[5][5], 2)
        self.assertEqual(self.board.board[4][5], 1)

    def test_place_airplane_out_of_bounds(self):
        with self.assertRaises(OutOfBoundsException):
            self.board.place_airplane(11, 11, "up")

    def test_hit_airplane(self):
        self.board.place_airplane(5, 5, "up")
        result = self.board.hit(5, 5)
        self.assertEqual(result, 4)

    def test_hit_empty(self):
        result = self.board.hit(1, 1)
        self.assertEqual(result, 5)

    def test_hit_already_hit(self):
        self.board.place_airplane(5, 5, "up")
        self.board.hit(5, 5)
        with self.assertRaises(AlreadyHitException):
            self.board.hit(5, 5)

class ServiceTest(unittest.TestCase):

    def setUp(self):
        self.player_board = PlayerBoard()
        self.computer_board = ComputerBoard()
        self.service = Service(self.player_board, self.computer_board)

    def test_place_all_possible_airplanes(self):
        airplanes_placed = self.service.place_all_possible_airplanes(5, 5)
        self.assertGreater(airplanes_placed, 0)


    def test_player_moves(self):
        self.service.player_moves.append(((5, 5), "hit"))
        self.assertEqual(len(self.service.player_moves), 1)

    def test_computer_moves(self):
        self.service.computer_moves.append(((5, 5), "hit"))
        self.assertEqual(len(self.service.computer_moves), 1)



if __name__ == '__main__':
    unittest.main()