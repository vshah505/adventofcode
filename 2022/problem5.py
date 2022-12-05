import re
import utils


def parse_stack(stacks_input):
    num_stacks = int(stacks_input.pop()[-1])
    stacks = [list() for _ in range(num_stacks)]

    for line in stacks_input:
        crates = [line[i:i + 3].strip(" []") for i in range(0, len(line), 4)]
        [stacks[i].append(crate) for i, crate in enumerate(crates) if crate]

    return [list(reversed(stack)) for stack in stacks]


def parse_procedures(procedure_input):
    return [
        tuple([int(value) for value in re.findall(r"\d+", line)])
        for line in procedure_input
    ]


def get_input():
    stacks_input = list()
    procedure_input = list()
    current_input = stacks_input
    with utils.get_input_fd(__file__) as f:
        for line in f:
            if line == "\n":
                current_input = procedure_input
                continue
            current_input.append(line.strip("\n"))

    stacks = parse_stack(stacks_input)
    procedures = parse_procedures(procedure_input)

    return stacks, procedures


def execute_procedures(cratemover9000=False):
    stacks, procedures = get_input()

    for procedure in procedures:
        move, start, end = procedure
        crates = stacks[start - 1][-move:]
        if not cratemover9000:
            crates = reversed(crates)
        stacks[end - 1].extend(crates)
        stacks[start - 1] = stacks[start - 1][:-move]

    return "".join([stack[-1] for stack in stacks])


def part1():
    return execute_procedures(cratemover9000=False)


def part2():
    return execute_procedures(cratemover9000=True)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
