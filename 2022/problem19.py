import collections
import enum
import math
import utils
import re


class Resource(enum.Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


def get_input():
    blueprints = dict()
    with utils.get_input_fd(__file__) as f:
        for line in f.read().split("\n"):
            values = list(map(int, re.findall(r"-?\d+", line)))
            blueprints[values[0]] = {
                Resource.ORE: (values[1], 0, 0, 0),
                Resource.CLAY: (values[2], 0, 0, 0),
                Resource.OBSIDIAN: (values[3], values[4], 0, 0),
                Resource.GEODE: (values[5], 0, values[6], 0),
            }

    return blueprints


def check_resources(resources, build_cost):
    return all(resource >= cost for resource, cost in zip(resources, build_cost))


def spend_resources(resources, build_cost):
    return tuple(value - build_cost[key] for key, value in enumerate(resources))


def collect_resources(resources, robots, max_costs):
    """
    Add resources and reduce the problem space if we have an abundance of a resources
    """
    return tuple(
        min(resource + robot, max_cost * 2)
        for resource, robot, max_cost in zip(resources, robots, max_costs)
    )


def add_robot(robots, robot_type):
    return tuple(
        robot_count + 1 if idx == robot_type.value else robot_count
        for idx, robot_count in enumerate(robots)
    )


def get_max_geodes(blueprint, time_limit):

    max_costs = [max(values) for values in zip(*blueprint.values())]
    max_costs[-1] = math.inf

    visited = set()
    resources = (0, 0, 0, 0)
    robots = (1, 0, 0, 0)
    queue = collections.deque([(resources, robots)])

    time_elapsed = 0

    while queue and time_elapsed < time_limit:
        for _ in range(len(queue)):
            state = queue.popleft()
            if state in visited:
                continue
            visited.add(state)
            resources, robots = state

            # Always build a geode robot if possible
            if check_resources(resources, blueprint[Resource.GEODE]):
                new_resources = collect_resources(
                    spend_resources(resources, blueprint[Resource.GEODE]),
                    robots,
                    max_costs,
                )
                new_robots = add_robot(robots, Resource.GEODE)
                queue.append((new_resources, new_robots))
            else:
                for robot, costs in blueprint.items():

                    # Don't build robots if we have an abundance of a resource
                    # based on the maximum cost of any resource
                    if robots[robot.value] >= max_costs[robot.value]:
                        continue

                    if check_resources(resources, costs):
                        new_resources = collect_resources(
                            spend_resources(resources, costs), robots, max_costs
                        )
                        new_robots = add_robot(robots, robot)
                        queue.append((new_resources, new_robots))

                new_resources = collect_resources(resources, robots, max_costs)
                queue.append((new_resources, robots))

        time_elapsed += 1

    return max(resources[Resource.GEODE.value] for resources, robots in queue)


def part1():
    blueprints = get_input()
    return sum(
        blueprint_num * get_max_geodes(blueprint, 24)
        for blueprint_num, blueprint in blueprints.items()
    )


def part2():
    blueprints = get_input()
    return math.prod(
        get_max_geodes(blueprint, 32)
        for blueprint_num, blueprint in blueprints.items()
        if blueprint_num <= 3
    )


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
