import Snake
import game
import pandas as pd
import tqdm


# Algorithms: BFS, DFS, A*


def make_calc_time_csv(input_table):
    maximum_value = 0
    for calc_time in input_table['calculation time']:
        maximum_value = max(maximum_value, len(list(calc_time)))
    output_data = pd.DataFrame({
        'index': range(maximum_value)
    })
    for calc_time, i in zip(input_table['calculation time'], range(len(input_table['calculation time']))):
        output_data = pd.concat([output_data, pd.DataFrame({f'Run #{i:03d}': calc_time})], axis=1)
    return output_data


if __name__ == '__main__':
    board_size = 50

    history = pd.DataFrame({
        'index': [],
        'name': [],
        'algorithm': [],
        'board size': [],
        'score': [],
        'runtime': [],
        'calculation time': []
    })

    for i in tqdm.tqdm(range(100)):
        snake = Snake.AutoSnake(algorithm='A*',
                                pos=(10, 10),
                                tail_size=3,
                                orientation=0,
                                bounds=(board_size, board_size),
                                apple=Snake.Apple(bounds=(board_size, board_size))
                                )
        game.play(snake)
        step = pd.DataFrame({
            'index': [i],
            'name': [f'Snake#{i:03d}'],
            'algorithm': ['A* reverse'],
            'board size': [board_size],
            'score': [snake.score],
            'runtime': [snake.runtime],
            'calculation time': [snake.calc_time]
        })
        history = pd.concat([history, step])
    history.to_csv('AstarReverse2.csv', index=False)
    make_calc_time_csv(history).to_csv('AstarReverse2times.csv', index=False)
