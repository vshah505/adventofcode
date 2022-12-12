import math

import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return [[int(height) for height in list(line.strip())] for line in f]


def is_visible(tree_grid, i, j):
    max_north = max([tree_grid[k][j] for k in range(i)], default=-math.inf)
    max_south = max(
        [tree_grid[k][j] for k in range(i + 1, len(tree_grid))], default=-math.inf
    )
    max_east = max(tree_grid[i][j + 1 :], default=-math.inf)
    max_west = max(tree_grid[i][:j], default=-math.inf)

    return min([max_north, max_south, max_east, max_west]) < tree_grid[i][j]


def scenic_score(tree_grid, i, j):
    rows = len(tree_grid)
    columns = len(tree_grid[0])
    score = 1

    for direction in utils.Direction:
        visible_trees = 0
        current_position = utils.move_in_direction((i, j), direction)
        while 0 <= current_position[0] < rows and 0 <= current_position[1] < columns:
            visible_trees += 1

            if tree_grid[current_position[0]][current_position[1]] >= tree_grid[i][j]:
                break

            current_position = utils.move_in_direction(current_position, direction)

        score *= visible_trees

    return score


def part1():
    tree_grid = get_input()
    return sum(
        is_visible(tree_grid, i, j)
        for i in range(len(tree_grid))
        for j in range(len(tree_grid[i]))
    )


def part2():
    tree_grid = get_input()
    return max(
        scenic_score(tree_grid, i, j)
        for i in range(len(tree_grid))
        for j in range(len(tree_grid[i]))
    )


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
