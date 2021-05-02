import random, time, Algorithms
from helpers import Node

moveset = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # up, right, down, left
algorithms = {
    'BFS': Algorithms.bfs,
    'DFS': Algorithms.dfs,
    'A*': Algorithms.astar_search
}


class Snake:
    def __init__(self, algorithm, pos=(0, 0), tail_size=3, orientation=0, bounds=(10, 10), apple=None):
        self.algorithm = algorithm
        self.pos = pos
        self.tail = []
        self.tail_size = tail_size
        self.orientation = orientation
        self.bounds = bounds
        self.apple = apple
        self.alive = True
        self.score = 0
        self.calc_time = []
        self.start_time = time.time()
        self.runtime = 0
        self.death_reason = ""

    def ping_to_move(self):
        self.move(moveset[self.orientation])

    def move(self, direction):
        self.tail.append(self.pos[:])
        if len(self.tail) > self.tail_size:
            for i in range(len(self.tail) - self.tail_size):
                self.tail.pop(0)

        self.pos = list(self.pos)
        self.pos[0] = (self.pos[0] + direction[0])  # % self.bounds[0]
        self.pos[1] = (self.pos[1] + direction[1])  # % self.bounds[1]
        self.pos = tuple(self.pos)

        if self.pos == (self.apple.x, self.apple.y):
            self.take_apple()

        self.check_collision()

    def take_apple(self):
        self.tail_size += 2
        self.apple.change_position(self.tail + [self.pos])
        self.score += 1

    def change_orientation(self, orientation):
        if moveset[orientation][0] + moveset[self.orientation][0] != 0 or \
                moveset[orientation][1] + moveset[self.orientation][1] != 0:
            self.orientation = orientation

    def check_collision(self):
        if len(set(self.tail[:] + [self.pos])) < len(self.tail[:] + [self.pos]):
            self.die("collided")
        if self.pos[0] < 0 or self.pos[1] < 0 or \
                self.pos[0] >= self.bounds[0] or self.pos[1] >= self.bounds[1]:
            self.die("out of bounds")

    def die(self, reason):
        # print(reason)
        self.death_reason = reason
        self.runtime = time.time() - self.start_time
        self.alive = False
        # print(f'Died with score: {self.score}')


class AutoSnake(Snake):
    path = []

    def ping_to_move(self):
        if len(self.path) == 0:
            self.calculate_new_path()
        if len(self.path) != 0:
            direction = (self.path[0][0] - self.pos[0], self.path[0][1] - self.pos[1])
            self.move(direction)
            self.path.pop(0)
        else:
            direction = (self.pos[0] - self.tail[-1][0], self.pos[1] - self.tail[-1][1])
            for possible_dir in moveset:
                possible_place = (self.pos[0] + possible_dir[0], self.pos[1] + possible_dir[1])
                if possible_place not in self.tail \
                        and possible_place[0] >= 0 and possible_place[1] >= 0 \
                        and possible_place[0] < self.bounds[0] and possible_place[1] < self.bounds[1]:
                    direction = possible_dir
            self.move(direction)

    def calculate_new_path(self):
        self.path = []
        start_time = time.time()
        direction = algorithms[self.algorithm]((self.apple.x, self.apple.y), self.pos, self.tail, self.bounds)
        self.calc_time.append(time.time() - start_time)
        while direction.pos != self.pos:
            self.path.append(direction.pos)
            direction = direction.root
        self.path = self.path[::-1]


class Apple:
    def __init__(self, bounds):
        self.bounds = bounds
        self.x = 0
        self.y = 0
        self.change_position([])

    def change_position(self, occupied):
        self.x = random.randint(0, self.bounds[0] - 1)
        self.y = random.randint(0, self.bounds[1] - 1)
        if (self.x, self.y) in occupied:
            self.change_position(occupied)
        # print(f'Apple moved to x {self.x} y {self.y}')
