import collections
import functools

import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return [list(line) for line in f.read().split("\n")]


@functools.lru_cache(maxsize=None)
def move_blizzards(time, blizzards, depth, width):
    new_blizzards = set()

    for x, y, direction in blizzards:
        dx, dy = direction.value
        new_blizzards.add(
            (1 + (x - 1 + dx * time) % depth, 1 + (y - 1 + dy * time) % width)
        )

    return new_blizzards


def get_next_tiles(current_tile, walls, blizzards):
    next_tiles = []
    for direction in utils.Direction:
        next_tile = utils.move_in_direction(current_tile, direction)
        if next_tile not in walls and next_tile not in blizzards:
            next_tiles.append(next_tile)

    if current_tile not in walls and current_tile not in blizzards:
        next_tiles.append(current_tile)

    return next_tiles


def bfs(valley, start, end, start_time):
    depth = len(valley) - 2
    width = len(valley[0]) - 2

    blizzard_directions = {
        "<": utils.Direction.WEST,
        ">": utils.Direction.EAST,
        "^": utils.Direction.NORTH,
        "v": utils.Direction.SOUTH,
    }

    walls = frozenset(
        {
            (x, y)
            for x, row in enumerate(valley)
            for y, tile in enumerate(row)
            if tile == "#"
        }.union({(-1, 1), (depth + 2, width)})
    )

    blizzards = frozenset(
        {
            (x, y, blizzard_directions[tile])
            for x, row in enumerate(valley)
            for y, tile in enumerate(row)
            if tile in blizzard_directions.keys()
        }
    )

    explored = set()
    queue = collections.deque([(start_time, start)])
    while queue:
        time, current_tile = queue.popleft()
        time += 1
        new_blizzards = move_blizzards(time % (depth * width), blizzards, depth, width)
        for next_tile in get_next_tiles(current_tile, new_blizzards, walls):
            if (time, next_tile) not in explored:
                if next_tile == end:
                    return time
                explored.add((time, next_tile))
                queue.append((time, next_tile))


def part1():
    valley = get_input()
    start = (0, 1)
    end = (len(valley) - 1, len(valley[0]) - 2)

    return bfs(valley, start, end, 0)


def part2():
    valley = get_input()
    start = (0, 1)
    end = (len(valley) - 1, len(valley[0]) - 2)

    t1 = bfs(valley, start, end, 0)
    t2 = bfs(valley, end, start, t1)
    return bfs(valley, start, end, t2)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
