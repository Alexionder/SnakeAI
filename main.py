import Snake
import game


if __name__ == '__main__':
    board_size = 50
    game.play(Snake.SnakeAStar(coords=(10, 10),
                               tail_size=3,
                               orientation=0,
                               bounds=(board_size, board_size),
                               apple=Snake.Apple(bounds=(board_size, board_size))
                               ))


