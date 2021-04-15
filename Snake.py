import random, time
from helpers import Node
moveset = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # up, right, down, left


class Snake:
    def __init__(self, coords=(0, 0), tail_size=3, orientation=0, bounds=(10, 10), apple=None):
        self.coords = coords
        self.tail = []
        self.tail_size = tail_size
        self.orientation = orientation
        self.bounds = bounds
        self.apple = apple
        self.alive = True
        self.score = 0

    def ping_to_move(self):
        self.move(moveset[self.orientation])

    def move(self, direction):
        self.tail.append(self.coords[:])
        if len(self.tail) > self.tail_size:
            for i in range(len(self.tail)-self.tail_size):
                self.tail.pop(0)

        self.coords = list(self.coords)
        self.coords[0] = (self.coords[0] + direction[0]) # % self.bounds[0]
        self.coords[1] = (self.coords[1] + direction[1]) # % self.bounds[1]
        self.coords = tuple(self.coords)

        if self.coords == (self.apple.x, self.apple.y):
            self.take_apple()

        self.check_collision()

    def take_apple(self):
        self.tail_size += 2
        self.apple.change_position(self.tail + [self.coords])
        self.score += 1

    def change_orientation(self, orientation):
        if moveset[orientation][0] + moveset[self.orientation][0] != 0 or \
                moveset[orientation][1] + moveset[self.orientation][1] != 0:
            self.orientation = orientation

    def check_collision(self):
        if len(set(self.tail[:] + [self.coords])) < len(self.tail[:] + [self.coords]):
            print("collided")
            self.die()
        if self.coords[0] < 0 or self.coords[1] < 0 or \
                self.coords[0] >= self.bounds[0] or self.coords[1] >= self.bounds[1]:
            print("out of bounds")
            self.die()

    def die(self):
        self.alive = False
        print(f'Died with score: {self.score}')


class SnakeBFS(Snake):
    path = []

    def ping_to_move(self):
        if len(self.path) == 0:
            self.calculate_new_path()
        if len(self.path) != 0:
            direction = (self.path[0][0] - self.coords[0], self.path[0][1] - self.coords[1])
            self.move(direction)
            self.path.pop(0)
        else:
            direction = (self.coords[0]-self.tail[-1][0], self.coords[1]-self.tail[-1][1])
            for possible_dir in moveset:
                if (self.coords[0] + possible_dir[0], self.coords[1] + possible_dir[1]) not in self.tail:
                    direction = possible_dir
            self.move(direction)

    def calculate_new_path(self):
        self.path = []
        start_time = time.time()
        node = self.bfs((self.apple.x, self.apple.y))
        print(f'BFS took {time.time() - start_time} time to calculate')
        while node is not None and node.name is not self.coords:
            self.path = [node.name] + self.path
            node = node.root

    def get_neighbors(self, place):
        neighbors = []
        for neighbor in moveset:
            neighbor = (place[0] + neighbor[0], place[1] + neighbor[1])
            if neighbor not in self.tail \
                    and neighbor[0] >= 0 and neighbor[1] >= 0 \
                    and neighbor[0] < self.bounds[0] and neighbor[1] < self.bounds[1]:
                neighbors.append(neighbor)
        return neighbors

    def bfs(self, goal):

        visited, queue = set(), [Node(None, self.coords)]
        visited.add(self.coords)

        while queue:

            vertex = queue.pop(0)
            # print(str(vertex) + " ", end='\n')
            if vertex.name == goal:
                return vertex

            for neighbour in self.get_neighbors(vertex.name):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(Node(vertex, neighbour))
        return None


class Apple:
    def __init__(self, bounds):
        self.bounds = bounds
        self.x = 0
        self.y = 0
        self.change_position([])

    def change_position(self, occupied):
        self.x = random.randint(0, self.bounds[0]-1)
        self.y = random.randint(0, self.bounds[1]-1)
        if (self.x, self.y) in occupied:
            self.change_position(occupied)
        print(f'Apple moved to x {self.x} y {self.y}')
