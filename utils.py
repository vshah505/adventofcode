import contextlib
import enum
import os
import pathlib


class Direction(enum.Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


def move_in_direction(position, direction):
    return position[0] + direction.value[0], position[1] + direction.value[1]


@contextlib.contextmanager
def get_input_fd(
    problem_file: str,
):
    problem_path = pathlib.Path(problem_file).resolve()
    input_path = os.path.join(problem_path.parent, "inputs", f"{problem_path.stem}.txt")
    fd = open(input_path, "r")
    yield fd
    fd.close()




