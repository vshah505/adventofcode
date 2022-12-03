import itertools
import string
import utils

PRIORITIES = {
    item: priority + 1
    for priority, item in enumerate(
        list(string.ascii_lowercase) + list(string.ascii_uppercase)
    )
}


def get_input():
    with utils.get_input_fd(__file__) as f:
        rucksacks = [list(line.strip()) for line in f]
    return rucksacks


def part1():
    rucksacks = get_input()
    return sum(
        PRIORITIES[
            next(
                iter(
                    set(rucksack[:len(rucksack) // 2]).intersection(
                        rucksack[len(rucksack) // 2:]
                    )
                )
            )
        ]
        for rucksack in rucksacks
    )


def part2():
    rucksacks = get_input()
    return sum(
        PRIORITIES[
            next(
                iter(
                    set(group[0])
                    .intersection(set(group[1]))
                    .intersection(set(group[2]))
                )
            )
        ]
        for group in itertools.zip_longest(*[iter(rucksacks)] * 3)
    )


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
