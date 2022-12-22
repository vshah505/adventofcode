import re
import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        board, instructions = f.read().split("\n\n")
        board = board.split("\n")

    max_length = max(len(row) for row in board)
    board = [list(row.ljust(max_length)) for row in board]

    instructions = [
        tuple(re.split(r"(\d+)", instruction))
        for instruction in re.findall(r"\d+[R|L]?", instructions)
    ]
    instructions = [
        (int(instruction[1]), instruction[2]) for instruction in instructions
    ]

    return board, instructions


def get_next_direction(direction, rotation):
    if rotation == "":
        return direction

    elif direction == utils.Direction.EAST:
        if rotation == "R":
            return utils.Direction.SOUTH
        else:
            return utils.Direction.NORTH

    elif direction == utils.Direction.SOUTH:
        if rotation == "R":
            return utils.Direction.WEST
        else:
            return utils.Direction.EAST

    elif direction == utils.Direction.WEST:
        if rotation == "R":
            return utils.Direction.NORTH
        else:
            return utils.Direction.SOUTH

    elif direction == utils.Direction.NORTH:
        if rotation == "R":
            return utils.Direction.EAST
        else:
            return utils.Direction.WEST

    return direction


def get_next_position(position, direction, max_row, max_col):
    next_row, next_col = utils.move_in_direction(position, direction)

    return next_row % max_row, next_col % max_col


def get_next_position_in_cube(position, direction):
    """
    Face 1 -> 0-49, 50-99
    Face 2 -> 0-49, 100-149
    Face 3 -> 50-99, 50-99
    Face 4 -> 100-149, 0-49
    Face 5 -> 100-149, 0-49
    Face 6 -> 150-199, 0-49
    """
    row, col = position

    # Face 1
    if 0 <= row < 50 and 50 <= col < 100:
        # NORTH -> Face 6
        if direction == utils.Direction.NORTH and row == 0:
            return (150 + (col - 50), 0), utils.Direction.EAST

        # WEST -> Face 5
        elif direction == utils.Direction.WEST and col == 50:
            return (149 - (row - 0), 0), utils.Direction.EAST

    # Face 2
    elif 0 <= row < 50 and 100 <= col < 150:

        # NORTH -> Face 6
        if direction == utils.Direction.NORTH and row == 0:
            return (199, 0 + (col - 100)), utils.Direction.NORTH

        # EAST -> Face 4
        elif direction == utils.Direction.EAST and col == 149:
            return (149 - (row - 0), 99), utils.Direction.WEST

        # SOUTH -> Face 3
        elif direction == utils.Direction.SOUTH and row == 49:
            return (50 + (col - 100), 99), utils.Direction.WEST

    # Face 3
    elif 50 <= row < 100 and 50 <= col < 100:

        # WEST -> Face 5
        if direction == utils.Direction.WEST and col == 50:
            return (100, 0 + (row - 50)), utils.Direction.SOUTH

        # EAST -> Face 2
        elif direction == utils.Direction.EAST and col == 99:
            return (49, 100 + (row - 50)), utils.Direction.NORTH

    # Face 4
    elif 100 <= row < 150 and 50 <= col < 100:

        # EAST -> Face 2
        if direction == utils.Direction.EAST and col == 99:
            return (49 - (row - 100), 149), utils.Direction.WEST

        # SOUTH -> Face 6
        elif direction == utils.Direction.SOUTH and row == 149:
            return (150 + (col - 50), 49), utils.Direction.WEST

    # Face 5
    elif 100 <= row < 150 and 0 <= col < 50:

        # WEST -> Face 1
        if direction == utils.Direction.WEST and col == 0:
            return (49 - (row - 100), 50), utils.Direction.EAST

        # NORTH -> Face 3
        elif direction == utils.Direction.NORTH and row == 100:
            return (50 + (col - 0), 50), utils.Direction.EAST

    # Face 6
    elif 150 <= row < 200 and 0 <= col < 50:

        # WEST -> Face 1
        if direction == utils.Direction.WEST and col == 0:
            return (0, 50 + (row - 150)), utils.Direction.SOUTH

        # SOUTH -> Face 2
        elif direction == utils.Direction.SOUTH and row == 199:
            return (0, 100 + (col - 0)), utils.Direction.SOUTH

        # EAST -> Face 4
        elif direction == utils.Direction.EAST and col == 49:
            return (149, 50 + (row - 150)), utils.Direction.NORTH

    return utils.move_in_direction(position, direction), direction


def get_password(board, instructions, folded_cube=False):
    position = (0, board[0].index("."))
    current_direction = utils.Direction.EAST

    max_row = len(board)
    max_col = len(board[0])

    for distance, rotation in instructions:
        for _ in range(distance):

            # Walk through empty spaces
            next_position, next_direction = position, current_direction
            while 1:
                if folded_cube:
                    next_position, next_direction = get_next_position_in_cube(
                        next_position, next_direction
                    )
                else:
                    next_position = get_next_position(
                        next_position, next_direction, max_row, max_col
                    )
                    next_direction = current_direction

                if board[next_position[0]][next_position[1]] != " ":
                    break

            # Hit a wall
            if board[next_position[0]][next_position[1]] == "#":
                break

            position = next_position
            current_direction = next_direction

        current_direction = get_next_direction(current_direction, rotation)

    facing = {
        utils.Direction.EAST: 0,
        utils.Direction.SOUTH: 1,
        utils.Direction.WEST: 2,
        utils.Direction.NORTH: 3,
    }

    return 1000 * (position[0] + 1) + 4 * (position[1] + 1) + facing[current_direction]


def part1():
    board, instructions = get_input()
    return get_password(board, instructions)


def part2():
    board, instructions = get_input()
    return get_password(board, instructions, folded_cube=True)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
