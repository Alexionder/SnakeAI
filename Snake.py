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
        self.calc_time = []

    def ping_to_move(self):
        self.move(moveset[self.orientation])

    def move(self, direction):
        self.tail.append(self.coords[:])
        if len(self.tail) > self.tail_size:
            for i in range(len(self.tail) - self.tail_size):
                self.tail.pop(0)

        self.coords = list(self.coords)
        self.coords[0] = (self.coords[0] + direction[0])  # % self.bounds[0]
        self.coords[1] = (self.coords[1] + direction[1])  # % self.bounds[1]
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


class SnakeWithPath(Snake):
    path = []

    def ping_to_move(self):
        if len(self.path) == 0:
            self.calculate_new_path()
        if len(self.path) != 0:
            direction = (self.path[0][0] - self.coords[0], self.path[0][1] - self.coords[1])
            self.move(direction)
            self.path.pop(0)
        else:
            direction = (self.coords[0] - self.tail[-1][0], self.coords[1] - self.tail[-1][1])
            for possible_dir in moveset:
                possible_place = (self.coords[0] + possible_dir[0], self.coords[1] + possible_dir[1])
                if possible_place not in self.tail \
                        and possible_place[0] >= 0 and possible_place[1] >= 0 \
                        and possible_place[0] < self.bounds[0] and possible_place[1] < self.bounds[1]:
                    direction = possible_dir
            self.move(direction)

    def get_neighbors(self, place):
        neighbors = []
        for neighbor in moveset:
            neighbor = (place[0] + neighbor[0], place[1] + neighbor[1])
            if neighbor not in self.tail \
                    and neighbor[0] >= 0 and neighbor[1] >= 0 \
                    and neighbor[0] < self.bounds[0] and neighbor[1] < self.bounds[1]:
                neighbors.append(neighbor)
        return neighbors


class SnakeBFS(SnakeWithPath):

    def calculate_new_path(self):
        self.path = []
        start_time = time.time()
        node = self.bfs((self.apple.x, self.apple.y))
        print(f'BFS took {time.time() - start_time} seconds to calculate')
        while node is not None and node.pos is not self.coords:
            self.path = [node.pos] + self.path
            node = node.root

    def bfs(self, goal):

        visited, queue = set(), [Node(None, self.coords)]
        visited.add(self.coords)

        while queue:

            vertex = queue.pop(0)
            if vertex.pos == goal:
                return vertex

            for neighbour in self.get_neighbors(vertex.pos):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(Node(vertex, neighbour))
        return None


class SnakeDFS(SnakeWithPath):

    def calculate_new_path(self):
        self.path = []
        start_time = time.time()
        node = self.dfs((self.apple.x, self.apple.y))
        print(f'DFS took {time.time() - start_time} seconds to calculate')
        while node is not None and node.pos is not self.coords:
            self.path = [node.pos] + self.path
            node = node.root

    def dfs(self, goal):

        visited, queue = set(), [Node(None, self.coords)]
        visited.add(self.coords)

        while queue:

            vertex = queue.pop()
            if vertex.pos == goal:
                return vertex

            for neighbour in self.get_neighbors(vertex.pos):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(Node(vertex, neighbour))
        return None


class SnakeAStar(SnakeWithPath):

    def calculate_new_path(self):
        start_time = time.time()
        self.path = self.astar_search((self.apple.x, self.apple.y))
        print(f'A* took {time.time() - start_time} seconds to calculate')

    def astar_search(self, goal):

        open = []
        closed = []

        start_node = Node(None, self.coords)
        goal_node = Node(None, goal)

        open.append(start_node)

        while len(open) > 0:

            open.sort()

            current_node = open.pop(0)

            closed.append(current_node)


            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.pos)
                    current_node = current_node.root
                # Return reversed path
                return path[::-1]

            (x, y) = current_node.pos

            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            for next in neighbors:

                if not self.is_reachable(next):
                    continue

                neighbor = Node(current_node, next)

                if neighbor in closed:
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.pos[0] - start_node.pos[0]) + abs(
                    neighbor.pos[1] - start_node.pos[1])
                neighbor.h = abs(neighbor.pos[0] - goal_node.pos[0]) + abs(
                    neighbor.pos[1] - goal_node.pos[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if self.add_to_open(open, neighbor):
                    # Everything is green, add neighbor to open list
                    open.append(neighbor)

        return []

    def is_reachable(self, pos):
        if pos in self.tail:
            return False
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.bounds[0] or pos[1] >= self.bounds[1]:
            return False
        return True

    @staticmethod
    def add_to_open(open, neighbor):
        for node in open:
            if neighbor == node and neighbor.f >= node.f:
                return False
        return True


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
        print(f'Apple moved to x {self.x} y {self.y}')
