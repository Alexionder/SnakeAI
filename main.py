import Snake
import game

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board_size = 100
    game.play(Snake.SnakeBFS(coords=(10, 10),
                             tail_size=3,
                             orientation=0,
                             bounds=(board_size, board_size),
                             apple=Snake.Apple(bounds=(board_size, board_size))
                             ))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
