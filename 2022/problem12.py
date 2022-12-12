import collections
import utils


def get_input():

    start = end = (0, 0)
    grid = list()

    with utils.get_input_fd(__file__) as f:
        for line in f.read().split("\n"):
            grid.append(list(line))

    for x, row in enumerate(grid):
        for y, height in enumerate(row):
            if height == "S":
                row[y] = ord("a")
                start = (x, y)
            elif height == "E":
                row[y] = ord("z")
                end = (x, y)
            else:
                row[y] = ord(height)

    return start, end, grid


def is_valid(position, new_position, grid, visited):
    new_x, new_y = new_position
    x, y = position

    if (
        new_x < 0
        or new_y < 0
        or new_x >= len(grid)
        or new_y >= len(grid[0])
        or new_position in visited
    ):
        return False
    elif grid[new_x][new_y] <= grid[x][y] + 1:
        return True

    return False


def get_shortest_path(starts, end, grid):
    visited = set(starts)
    queue = collections.deque([(start, 0) for start in starts])

    while queue:
        position, moves = queue.popleft()
        if position == end:
            return moves

        for direction in utils.Direction:
            new_pos = utils.move_in_direction(position, direction)
            if is_valid(position, new_pos, grid, visited):
                visited.add(new_pos)
                queue.append((new_pos, moves + 1))

    return 0


def part1():
    start, end, grid = get_input()
    return get_shortest_path([start], end, grid)


def part2():
    _, end, grid = get_input()
    starts = [
        (x, y)
        for x, row in enumerate(grid)
        for y, height in enumerate(row)
        if height == ord("a")
    ]
    return get_shortest_path(starts, end, grid)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
