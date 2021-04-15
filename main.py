import game, Snake


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game.play(Snake.Snake(coords=(10, 10), tail_size=3, direction=0, bounds=(25, 25), apple=Snake.Apple(bounds=(25, 25))))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
