"""
this module provides module for tic tac game
"""


class TicTacGame:
    """
    this is class for tic tac game
    """
    def __init__(self, player1='Игрок1', player2='Игрок2'):
        # initialization
        self.field = [['.'] * 3 for i in range(3)]
        self.counter = 0
        self.winner = ''
        self.player1 = 'Победил: ' + player1
        self.player2 = 'Победил: ' + player2
        self.message_draw = 'Ничья!'

    def show_board(self) -> None:
        """
        method to show tic tac position
        """
        for i in range(3):
            for j in range(3):
                print(self.field[i][j], end=' ')
            print()

    def validate_input(self, value: str) -> bool:
        """
        validates input string
        """
        try:
            value_int = int(value)
        except ValueError:
            return False
        else:
            x, y = self.__separate_vals(value_int)
            if (1 <= x <= 3 and
                1 <= y <= 3 and
                    self.__check_free_point(x, y)):
                return True
            return False

    def hello_message(self) -> str:
        """
        returns welcome method
        """
        return "Формат ввода: xy, x - координата по оси x, " \
            "y - координата по оси y. x, y Могут принимать " \
            "значения {1, 2, 3}.\nПример хода в правильном формате: 22\n" \
            "Первым ходит Игрок1.\n"

    def move(self, value: str) -> None:
        """
        moves new symbol
        """
        sym = 'X' if self.counter % 2 == 0 else '0'
        self.counter += 1

        if self.validate_input(value):
            x, y = self.__separate_vals(int(value))
            self.field[y - 1][x - 1] = sym
        else:
            raise Exception('Wrong input value')

    def is_end(self) -> bool:
        """
        return true if game ended and false otherwise
        """
        for i in range(3):
            syms_horiz = set()
            sym_vert = set()
            for j in range(3):
                syms_horiz.add(self.field[i][j])
                sym_vert.add(self.field[j][i])
            if self.__validate_set_of_syms(syms_horiz):
                self.winner = self.__set_winner_name(syms_horiz)
                return True

            if self.__validate_set_of_syms(sym_vert):
                self.winner = self.__set_winner_name(sym_vert)
                return True

        syms_main_diag = set()
        syms_side_diag = set()

        for i in range(3):
            syms_main_diag.add(self.field[i][i])
            syms_side_diag.add(self.field[i][2 - i])
        if self.__validate_set_of_syms(syms_main_diag):
            self.winner = self.__set_winner_name(syms_main_diag)
            return True

        if self.__validate_set_of_syms(syms_side_diag):
            self.winner = self.__set_winner_name(syms_side_diag)
            return True

        # validate for draw
        for i in range(3):
            for j in range(3):
                if self.field[i][j] == '.':
                    return False

        self.winner = self.message_draw
        return True

    def get_result(self) -> str:
        """
        returns name of winner
        """
        return self.winner

    def __separate_vals(self, value: int):
        return value // 10, value % 10

    def __check_free_point(self, x, y) -> bool:
        return self.field[y - 1][x - 1] == '.'

    def __set_winner_name(self, set_of_syms: set) -> str:
        return self.player1 if next(iter(set_of_syms)) == 'X' else self.player2

    def __validate_set_of_syms(self, set_of_syms: set) -> bool:
        if len(set_of_syms) == 1 and next(iter(set_of_syms)) != '.':
            return True
        return False

