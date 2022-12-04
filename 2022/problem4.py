import utils


def get_section(assignment):
    start, end = assignment.split("-")
    return set(range(int(start), int(end) + 1))


def get_input():
    with utils.get_input_fd(__file__) as f:
        pairs = list()
        for line in f:
            assignment_1, assignment_2 = line.strip().split(",")
            pairs.append((get_section(assignment_1), get_section(assignment_2)))
        return pairs


def part1():
    pairs = get_input()
    return sum(
        assignment_1.issubset(assignment_2) or assignment_1.issubset(assignment_2)
        for assignment_1, assignment_2 in pairs
    )


def part2():
    pairs = get_input()
    return sum(
        bool(assignment_1.intersection(assignment_2))
        for assignment_1, assignment_2 in pairs
    )


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
