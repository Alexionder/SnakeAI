class Node:
    def __init__(self, root, name, point=None):
        self.root = root
        self.name = name
        self.point = point

    def __str__(self):
        return f'{self.root.name if self.root is not None else 0} -> ' \
               f'"{self.name}" -> {self.point.name if self.point is not None else 0}'
