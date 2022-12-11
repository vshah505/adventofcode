import math
import utils
import re


class Monkey:
    def __init__(self, starting_items, operation, test, true_result, false_result):
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.true_result = true_result
        self.false_result = false_result
        self.num_inspects = 0

    def get_next_monkey(self, worry):
        if worry % self.test == 0:
            return self.true_result
        else:
            return self.false_result

    def perform_inspection(self, item):
        local_ = {"old": item}
        exec(self.operation, globals(), local_)
        self.num_inspects += 1
        return local_["new"]


def get_input():
    with utils.get_input_fd(__file__) as f:
        monkeys = [line.split("\n") for line in f.read().split("\n\n")]

        return [
            Monkey(
                starting_items=list(map(int, re.findall(r"\d+", lines[1]))),
                operation=lines[2].split(":")[1].strip(),
                test=int(re.search(r"\d+", lines[3]).group()),
                true_result=int(re.search(r"\d+", lines[4]).group()),
                false_result=int(re.search(r"\d+", lines[5]).group()),
            )
            for lines in monkeys
        ]


def process_rounds(monkeys, num_rounds, relief):
    max_worry = math.prod([monkey.test for monkey in monkeys])

    for _ in range(num_rounds):
        for num, monkey in enumerate(monkeys):
            for item in monkey.items:
                worry = monkey.perform_inspection(item)
                if relief:
                    worry //= 3
                else:
                    worry %= max_worry
                monkeys[monkey.get_next_monkey(worry)].items.append(worry)
            monkey.items = []

    return math.prod(
        sorted([monkey.num_inspects for monkey in monkeys], reverse=True)[:2]
    )


def part1():
    monkeys = get_input()
    return process_rounds(monkeys, 20, True)


def part2():
    monkeys = get_input()
    return process_rounds(monkeys, 10000, False)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
