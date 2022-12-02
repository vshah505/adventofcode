import utils

outcome_mapping = {
    # Loss
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("C", "Y"): 0,

    # Tie
    ("A", "X"): 3,
    ("B", "Y"): 3,
    ("C", "Z"): 3,

    # Win
    ("A", "Y"): 6,
    ("B", "Z"): 6,
    ("C", "X"): 6,
}

point_mapping = {"X": 1, "Y": 2, "Z": 3}


def get_input():
    with utils.get_input_fd(__file__) as f:
        rounds = [tuple(line.strip().split(" ")) for line in f]
    return rounds


def part1():
    rounds = get_input()
    return sum(outcome_mapping[r] + point_mapping[r[1]] for r in rounds)


def part2():
    rounds = get_input()

    condition_mapping = {
        "X": {"A": "Z", "B": "X", "C": "Y"},
        "Y": {"A": "X", "B": "Y", "C": "Z"},
        "Z": {"A": "Y", "B": "Z", "C": "X"},
    }

    return sum(
        outcome_mapping[(r[0], condition_mapping[r[1]][r[0]])]
        + point_mapping[condition_mapping[r[1]][r[0]]]
        for r in rounds
    )


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
