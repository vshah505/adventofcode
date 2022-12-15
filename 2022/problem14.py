import utils
import re


def get_input():
    rocks = set()
    with utils.get_input_fd(__file__) as f:
        coord_lines = [
            [tuple(map(int, re.findall(r"\d+", coord))) for coord in line.split(" -> ")]
            for line in f.read().split("\n")
        ]

    for coords in coord_lines:
        for idx in range(1, len(coords)):
            (x1, y1) = coords[idx - 1]
            (x2, y2) = coords[idx]

            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    rocks.add((x1, y))
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    rocks.add((x, y1))

    return rocks


def simulate_sand(blocked_coords, threshold, floor=False):
    directions = [(0, 1), (-1, 1), (1, 1)]

    def add_grain():
        grain_coord = (500, 0)

        if grain_coord in blocked_coords:
            return False

        falling = True
        while falling:
            falling = False

            for direction in directions:
                next_coord = (
                    grain_coord[0] + direction[0],
                    grain_coord[1] + direction[1],
                )

                if next_coord not in blocked_coords:
                    grain_coord = next_coord
                    if grain_coord[1] >= threshold and not floor:
                        return False

                    falling = True
                    break

            if not falling:
                blocked_coords.add(grain_coord)
                return True

            if floor and grain_coord[1] == threshold - 1:
                blocked_coords.add(grain_coord)
                return True

    grains = 0
    while add_grain():
        grains += 1

    return grains


def part1():
    rocks = get_input()
    abyss = max(coord[1] for coord in rocks)
    return simulate_sand(blocked_coords=rocks, threshold=abyss)


def part2():
    rocks = get_input()
    floor = max(coord[1] for coord in rocks) + 2
    return simulate_sand(blocked_coords=rocks, threshold=floor, floor=True)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
