import unittest
from tic_tac import TicTacGame


class TestTicTacGame(unittest.TestCase):
    def setUp(self) -> None:
        # print("start setUp")
        self.game = TicTacGame("Player1", "Player2")

    def test_validate_input(self):
        self.assertFalse(self.game.validate_input("34"))
        self.assertFalse(self.game.validate_input("01"))
        self.assertFalse(self.game.validate_input("-12"))
        self.assertTrue(self.game.validate_input("12"))
        self.game.move("12")
        self.assertFalse(self.game.validate_input("12"))

    def test_move(self):
        self.game.move("12")
        self.assertFalse(self.game.validate_input("12"))

    def test_has_winner(self):
        self.assertFalse(self.game.is_end())
        self.game.move("11")
        self.game.move("21")
        self.game.move("12")
        self.game.move("22")
        self.game.move("13")
        self.assertTrue(self.game.is_end())
        self.assertEqual(self.game.get_result(), "Победил: Player1")

    def test_game_to_draw(self):
        self.game.move("11")
        self.game.move("21")
        self.game.move("12")
        self.game.move("22")
        self.game.move("23")
        self.game.move("13")
        self.game.move("31")
        self.game.move("32")
        self.game.move("33")
        self.assertTrue(self.game.is_end())
        self.assertEqual(self.game.get_result(), "Ничья!")

    def test_win_on_side_diag(self):
        self.game.move("31")
        self.game.move("21")
        self.game.move("22")
        self.game.move("11")
        self.game.move("13")
        self.assertTrue(self.game.is_end())
        self.assertEqual(self.game.get_result(), "Победил: Player1")

    def test_wrong_input(self):
        with self.assertRaises(ValueError):
            self.game.move("a3")
        with self.assertRaises(ValueError):
            self.game.move("111")
        with self.assertRaises(ValueError):
            self.game.move("-12")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
