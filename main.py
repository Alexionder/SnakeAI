import Snake
import game
import pandas as pd
import tqdm

if __name__ == '__main__':
    board_size = 25

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
        snake = Snake.SnakeAStar(coords=(10, 10),
                                 tail_size=3,
                                 orientation=0,
                                 bounds=(board_size, board_size),
                                 apple=Snake.Apple(bounds=(board_size, board_size))
                                 )
        game.play(snake, False)
        step = pd.DataFrame({
            'index': [i],
            'name': [f'Snake#{i:03d}'],
            'algorithm': ['A*'],
            'board size': [board_size],
            'score': [snake.score],
            'runtime': [snake.runtime],
            'calculation time': [snake.calc_time]
        })
        history = pd.concat([history, step])
    history.to_csv('Astart1.csv', index=False)

