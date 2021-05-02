from helpers import Node

moveset = [[0, -1], [1, 0], [0, 1], [-1, 0]]  # up, right, down, left


def get_neighbors(place, tail, bounds):
    neighbors = []
    for neighbor in moveset:
        neighbor = (place[0] + neighbor[0], place[1] + neighbor[1])
        if neighbor not in tail \
                and neighbor[0] >= 0 and neighbor[1] >= 0 \
                and neighbor[0] < bounds[0] and neighbor[1] < bounds[1]:
            neighbors.append(neighbor)
    return neighbors


def is_reachable(pos, tail, bounds):
    if pos in tail:
        return False
    if pos[0] < 0 or pos[1] < 0:
        return False
    if pos[0] >= bounds[0] or pos[1] >= bounds[1]:
        return False
    return True


def add_to_open(open, neighbor):
    for node in open:
        if neighbor == node and neighbor.f >= node.f:
            return False
    return True


def bfs(goal, pos, tail, bounds):
    visited, queue = set(), [Node(None, pos)]
    visited.add(pos)

    while queue:

        vertex = queue.pop(0)
        if vertex.pos == goal:
            return vertex

        for neighbour in get_neighbors(vertex.pos, tail, bounds):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(Node(vertex, neighbour))
    return None


def dfs(goal, pos, tail, bounds):

    visited, queue = set(), [Node(None, pos)]
    visited.add(pos)

    while queue:

        vertex = queue.pop()
        if vertex.pos == goal:
            return vertex

        for neighbour in get_neighbors(vertex.pos, tail, bounds):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(Node(vertex, neighbour))
    return None


def astar_search(goal, pos, tail, bounds):

    open = []
    closed = []

    start_node = Node(None, pos)
    goal_node = Node(None, goal)

    open.append(start_node)

    while len(open) > 0:

        open.sort()

        current_node = open.pop(0)

        closed.append(current_node)

        if current_node == goal_node:
            return current_node

        (x, y) = current_node.pos

        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for next_neighbor in neighbors:

            if not is_reachable(next_neighbor, tail, bounds):
                continue

            neighbor = Node(current_node, next_neighbor)

            if neighbor in closed:
                continue
            # Generate heuristics (Manhattan distance)
            neighbor.g = abs(neighbor.pos[0] - start_node.pos[0]) + abs(
                neighbor.pos[1] - start_node.pos[1])
            neighbor.h = abs(neighbor.pos[0] - goal_node.pos[0]) + abs(
                neighbor.pos[1] - goal_node.pos[1])
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if add_to_open(open, neighbor):
                # Everything is green, add neighbor to open list
                open.append(neighbor)

    return []
