import collections
import enum
import math

import utils


class Direction(enum.Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)
    NORTHWEST = (-1, -1)
    NORTHEAST = (-1, 1)
    SOUTHWEST = (1, -1)
    SOUTHEAST = (1, 1)


def get_input():
    with utils.get_input_fd(__file__) as f:
        return {
            (i, j)
            for i, row in enumerate(f.read().split("\n"))
            for j, value in enumerate(row)
            if value == "#"
        }


def propose_moves(rules, elves):
    proposed_moves = {}

    for elf in elves:
        neighboring_tiles = {
            direction: utils.move_in_direction(elf, direction)
            for direction in Direction
        }

        if elves.intersection(neighboring_tiles.values()):
            for direction_to_move, directions in rules:
                if all(
                    neighboring_tiles[direction] not in elves
                    for direction in directions
                ):
                    proposed_moves[elf] = utils.move_in_direction(
                        elf, direction_to_move
                    )
                    break

    return proposed_moves


def execute_moves(elves, proposed_moves):
    moved_elves = set()
    destinations = collections.defaultdict(list)
    num_elves_moved = 0

    for elf, destination in proposed_moves.items():
        destinations[destination].append(elf)

    for elf in elves:
        destination = proposed_moves.get(elf)
        if destination and len(destinations[destination]) == 1:
            moved_elves.add(destination)
            num_elves_moved += 1
        else:
            moved_elves.add(elf)

    return moved_elves, num_elves_moved


def get_empty_tiles(elves):
    max_x = max(elf[0] for elf in elves)
    min_x = min(elf[0] for elf in elves)
    max_y = max(elf[1] for elf in elves)
    min_y = min(elf[1] for elf in elves)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def spread_out(elves, num_rounds):
    rules = collections.deque(
        [
            (
                Direction.NORTH,
                [Direction.NORTH, Direction.NORTHEAST, Direction.NORTHWEST],
            ),
            (
                Direction.SOUTH,
                [Direction.SOUTH, Direction.SOUTHEAST, Direction.SOUTHWEST],
            ),
            (
                Direction.WEST,
                [Direction.WEST, Direction.SOUTHWEST, Direction.NORTHWEST],
            ),
            (
                Direction.EAST,
                [Direction.EAST, Direction.SOUTHEAST, Direction.NORTHEAST],
            ),
        ]
    )

    rounds = 0
    elves_moved = -1
    while rounds != num_rounds and elves_moved != 0:
        proposed_moves = propose_moves(rules, elves)
        elves, elves_moved = execute_moves(elves, proposed_moves)
        rules.rotate(-1)
        rounds += 1

    return get_empty_tiles(elves), rounds


def part1():
    elves = get_input()
    empty_ground_tiles, _ = spread_out(elves, 10)
    return empty_ground_tiles


def part2():
    elves = get_input()
    _, num_rounds = spread_out(elves, math.inf)
    return num_rounds


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
