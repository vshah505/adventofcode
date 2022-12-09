import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return [
            (line.strip().split(" ")[0], int(line.strip().split(" ")[1])) for line in f
        ]


def move_in_direction(position, direction):
    if direction == "U":
        return position[0] - 1, position[1]

    if direction == "D":
        return position[0] + 1, position[1]

    if direction == "R":
        return position[0], position[1] + 1

    if direction == "L":
        return position[0], position[1] - 1


def shift_tail(head, tail):
    distance_x, distance_y = (head[0] - tail[0], head[1] - tail[1])
    distance = abs(distance_x) + abs(distance_y)

    if distance >= 3 or ((distance_x == 0 or distance_y == 0) and distance == 2):
        x = 1 if distance_x > 0 else -1 if distance_x < 0 else 0
        y = 1 if distance_y > 0 else -1 if distance_y < 0 else 0
        return tail[0] + x, tail[1] + y

    return tail


def get_num_visited_tails(moves, num_knots):
    knots = [(0, 0)] * num_knots
    visited = {(0, 0)}

    for direction, steps in moves:
        for step in range(steps):
            knots[0] = move_in_direction(knots[0], direction)
            for i in range(1, len(knots)):
                knots[i] = shift_tail(knots[i - 1], knots[i])

            visited.add(knots[-1])

    return len(visited)


def part1():
    moves = get_input()
    return get_num_visited_tails(moves, 2)


def part2():
    moves = get_input()
    return get_num_visited_tails(moves, 10)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
