import collections
import utils


def get_input():
    rates = dict()
    tunnels = dict()

    with utils.get_input_fd(__file__) as f:
        lines = [line.split(" ") for line in f.read().split("\n")]

    for line in lines:
        valve = line[1]
        rate = int(line[4].split("=")[-1].strip(";"))
        tunnels[valve] = [tunnel.strip(",") for tunnel in line[9:]]
        rates[valve] = rate

    return rates, tunnels


def get_valve_distances(tunnels, rates):
    non_zero_rates = {valve: rate for valve, rate in rates.items() if rate}
    valve_distances = dict()
    for start in ("AA", *non_zero_rates):
        distances = {start: 0}
        seen = {start}
        queue = collections.deque([start])
        while queue and any(valve not in distances for valve in non_zero_rates):
            valve = queue.popleft()
            for adj_valve in tunnels[valve]:
                if adj_valve not in seen:
                    seen.add(adj_valve)
                    distances[adj_valve] = distances[valve] + 1
                    queue.append(adj_valve)

        valve_distances[start] = {
            valve: distances[valve]
            for valve in non_zero_rates
            if valve != start and valve in distances
        }

    return valve_distances


def find_paths(valve_distances, rates, time):
    pressures = []
    paths = []
    stack = [(time, 0, ["AA"])]
    while stack:
        time, pressure, path = stack.pop()
        current_valve = path[-1]
        path_increased = False
        for next_valve, distance in valve_distances[current_valve].items():
            if distance > time - 2 or next_valve in path:
                continue
            time_remaining = time - distance - 1
            current_pressure = pressure + rates[next_valve] * time_remaining
            stack.append((time_remaining, current_pressure, path + [next_valve]))
            path_increased = True

        if not path_increased:
            pressures.append(pressure)
            paths.append(path[1:])

    return pressures, paths


def part1():
    rates, tunnels = get_input()
    valve_distances = get_valve_distances(tunnels, rates)

    return max(find_paths(valve_distances, rates, 30)[0])


def part2():
    rates, tunnels = get_input()
    valve_distances = get_valve_distances(tunnels, rates)

    pressure_paths = list(zip(*find_paths(valve_distances, rates, 26)))
    pressures, paths = zip(*sorted(pressure_paths, reverse=True))

    lower_bound = 1
    while any(path in paths[lower_bound] for path in paths[0]):
        lower_bound += 1
    max_pressure = pressures[0] + pressures[lower_bound]

    for i in range(1, lower_bound):
        for j in range(i + 1, lower_bound + 1):
            if any(path in paths[j] for path in paths[i]):
                continue
            max_pressure = max(max_pressure, pressures[i] + pressures[j])

    return max_pressure


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
