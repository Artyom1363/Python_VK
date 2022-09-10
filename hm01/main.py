from tic_tac import TicTacGame

if __name__ == "__main__":
    game = TicTacGame()
    print(game.hello_message())
    while not game.is_end():
        move = input("Введите ход\n")
        while not game.validate_input(move):
            move = input("Неправильный формат ввода, введите еще раз!\n")
        game.move(move)
        game.show_board()
    print(f"{game.get_result()}")