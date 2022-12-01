import contextlib
import os
import pathlib


@contextlib.contextmanager
def get_input_fd(
    problem_file: str,
):
    problem_path = pathlib.Path(problem_file).resolve()
    input_path = os.path.join(problem_path.parent, "inputs", f"{problem_path.stem}.txt")
    fd = open(input_path, "r")
    yield fd
    fd.close()
