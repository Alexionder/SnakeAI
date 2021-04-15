import game, Snake


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game.play(Snake.SnakeBFS(coords=(10, 10), tail_size=3, orientation=0, bounds=(15, 15), apple=Snake.Apple(bounds=(15, 15))))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
