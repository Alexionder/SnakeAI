class Node:
    def __init__(self, root, pos, point=None):
        self.root = root
        self.pos = pos
        self.point = point
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.pos == other.pos

    # Sort nodes
    def __lt__(self, other):
        return self.f > other.f

    def __str__(self):
        return f'{self.root.pos if self.root is not None else 0} -> ' \
               f'"{self.pos}" -> {self.point.pos if self.point is not None else 0}'
