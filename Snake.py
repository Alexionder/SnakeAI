import random
moveset = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # up, right, down, left


class Snake:
    def __init__(self, coords=(0, 0), tail_size=3, direction=0, bounds=(10, 10), apple=None):
        self.coords = coords
        self.tail = []
        self.tail_size = tail_size
        self.direction = direction
        self.bounds = bounds
        self.apple = apple
        self.alive = True

    def move(self):
        self.tail.append(self.coords[:])
        if len(self.tail) > self.tail_size:
            for i in range(len(self.tail)-self.tail_size):
                self.tail.pop(0)

        self.coords = list(self.coords)
        self.coords[0] = (self.coords[0] + moveset[self.direction][0]) # % self.bounds[0]
        self.coords[1] = (self.coords[1] + moveset[self.direction][1]) # % self.bounds[1]
        self.coords = tuple(self.coords)

        if self.coords == (self.apple.x, self.apple.y):
            self.tail_size += 2
            self.apple.change_position()

        self.check_collision()

    def change_direction(self, direction):
        if moveset[direction][0] + moveset[self.direction][0] != 0 or \
                moveset[direction][1] + moveset[self.direction][1] != 0:
            self.direction = direction

    def check_collision(self):
        if len(set(self.tail[:] + [self.coords])) < len(self.tail[:] + [self.coords]):
            print("collided")
            self.alive = False
        if self.coords[0] < 0 or self.coords[1] < 0 or \
                self.coords[0] >= self.bounds[0] or self.coords[1] >= self.bounds[1]:
            print("out of bounds")
            self.alive = False


class BetterSnake(Snake):
    @staticmethod
    def do_better_stuff():
        print("doing better stuff")


class Apple:
    def __init__(self, bounds):
        self.bounds = bounds
        self.x = 0
        self.y = 0
        self.change_position()

    def change_position(self):
        self.x = random.randint(0, self.bounds[0]-1)
        self.y = random.randint(0, self.bounds[1]-1)
        print(f'Apple moved to x {self.x} y {self.y}')
