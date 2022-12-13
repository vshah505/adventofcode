import utils
import functools


def get_input():
    with utils.get_input_fd(__file__) as f:
        lines = f.read().split("\n\n")

    pairs = list()
    for pair in lines:
        pairs.append(tuple([eval(packet) for packet in pair.split("\n")]))

    return pairs


def compare_values(l, r):
    # Both ints
    if isinstance(l, int) and isinstance(r, int):
        if l > r:
            return 1

        if l < r:
            return -1

        return 0

    # Mixed
    elif isinstance(l, int):
        return compare_values([l], r)
    elif isinstance(r, int):
        return compare_values(l, [r])

    # Both lists
    else:
        for l_, r_ in zip(l, r):
            result = compare_values(l_, r_)
            if result != 0:
                return result

        # Check length of lists if valid packet not found
        return compare_values(len(l), len(r))


def part1():
    pairs = get_input()
    return sum(
        i + 1
        for i, (left, right) in enumerate(pairs)
        if compare_values(left, right) < 0
    )


def part2():
    pairs = get_input()

    divider_1, divider_2 = [[2]], [[6]]
    packets = [packet for pair in pairs for packet in pair] + [divider_1, divider_2]

    packets.sort(key=functools.cmp_to_key(compare_values))
    return (packets.index(divider_1) + 1) * (packets.index(divider_2) + 1)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
