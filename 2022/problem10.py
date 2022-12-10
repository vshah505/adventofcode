import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return [tuple(instruction.split(" ")) for instruction in f.read().split("\n")]


def get_register_changes(instructions):
    register_changes = list()
    for instruction in instructions:
        if instruction[0] == "addx":
            register_changes.extend([0, int(instruction[1])])
        if instruction[0] == "noop":
            register_changes.extend([0])

    return register_changes


def part1():
    instructions = get_input()
    register_changes = get_register_changes(instructions)

    signal_strengths = list()
    x_register = 1

    for cycle, register_change in enumerate(register_changes):
        current_cycle = cycle + 1
        if current_cycle == 20 or (current_cycle - 20) % 40 == 0:
            signal_strengths.append(current_cycle * x_register)
        x_register += register_change

    return sum(signal_strengths)


def part2():
    instructions = get_input()
    register_changes = get_register_changes(instructions)

    crt = list()
    x_register = 1
    pixels = ["."] * 40
    for cycle, register_change in enumerate(register_changes):
        pixels[cycle % 40] = "#" if abs((cycle % 40) - x_register) <= 1 else "."

        if (cycle + 1) % 40 == 0:
            crt.append(pixels)
            pixels = ["."] * 40

        x_register += register_change

    return "\n" + "\n".join(["".join(line) for line in crt])


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
