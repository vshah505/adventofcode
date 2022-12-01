import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        total_calories = list()
        current_calories = 0
        for line in f:
            if line == "\n":
                total_calories.append(current_calories)
                current_calories = 0
            else:
                current_calories += int(line)
        return total_calories


def part1():
    total_calories = get_input()
    return max(total_calories)


def part2():
    total_calories = get_input()
    return sum(sorted(total_calories, reverse=True)[:3])


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
