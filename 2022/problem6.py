import collections
import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return list(f.read())


def get_distinct_signal_marker(signal, marker_length):
    window = collections.deque(signal[:marker_length])
    for idx, character in enumerate(signal[marker_length:]):
        if len(set(window)) == marker_length:
            return idx + marker_length
        window.popleft()
        window.append(character)


def part1():
    signal = get_input()
    return get_distinct_signal_marker(signal, 4)


def part2():
    signal = get_input()
    return get_distinct_signal_marker(signal, 14)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
