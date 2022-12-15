import utils
import re


def get_input():
    sensors = dict()

    with utils.get_input_fd(__file__) as f:
        for line in f.read().split("\n"):
            values = tuple(map(int, re.findall(r"-?\d+", line)))
            sensors[(values[0], values[1])] = (values[2], values[3])

    return sensors


def get_relevant_range(sensor, beacon, row):
    distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    delta = abs(row - sensor[1])
    if delta <= distance:
        return sensor[0] - (distance - delta), sensor[0] + (distance - delta)

    return None


def get_excluded_ranges(sensors, row):
    ranges = [
        get_relevant_range(sensor, beacon, row) for sensor, beacon in sensors.items()
    ]
    ranges = sorted([r for r in ranges if r is not None])

    merged_ranges = ranges[:1]
    for r in ranges[1:]:
        if r[0] > merged_ranges[-1][1] + 1:
            merged_ranges.append(r)
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], r[1]))

    return merged_ranges


def part1():
    sensors = get_input()
    row = 2000000

    occupied = len(set(beacon for beacon in sensors.values() if beacon[1] == row))
    empty = sum(
        interval[1] - interval[0] + 1 for interval in get_excluded_ranges(sensors, row)
    )
    return empty - occupied


def part2():
    sensors = get_input()
    max_distance = 4000000

    # Assumption based on known location
    start_row = 3000000

    def process_row(row):
        excluded_ranges = get_excluded_ranges(sensors, row)

        for start, end in excluded_ranges:
            if start <= 0:
                if end >= max_distance:
                    return None
                elif end >= 0:
                    return (end + 1) * max_distance + row

    for row in range(start_row, max_distance + 1):
        result = process_row(row)
        if result is not None:
            return result


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
