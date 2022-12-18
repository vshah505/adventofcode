import utils
import numpy
from scipy import ndimage

DIRECTIONS_3D = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]


def get_input():
    with utils.get_input_fd(__file__) as f:
        lava_cubes = [tuple(int(val) for val in line.split(',')) for line in f.read().split('\n')]

    return lava_cubes


def get_exposed_faces(lava_cubes):
    return sum((x + dx, y + dy, z + dz) not in lava_cubes for dx, dy, dz in DIRECTIONS_3D for x, y, z in lava_cubes)


def part1():
    lava_cubes = get_input()
    return get_exposed_faces(set(lava_cubes))


def part2():
    lava_cubes = numpy.array(get_input())

    # Create an empty surface with one layer of space on each side of the lava cubes
    surface = numpy.zeros(lava_cubes.max(axis=0, initial=0) + 1)

    # Transpose the 3 dimensional space and set the lava cubes on the surface
    x, y, z = lava_cubes.T
    surface[x, y, z] = 1

    # Fill the holes in the surface (air) so they don't get counted as exposed sides
    surface = ndimage.binary_fill_holes(surface).astype(int)

    # Get the set of lava cubes and air from the surface
    lava_cubes_with_air = set(zip(*numpy.where(surface)))

    return get_exposed_faces(lava_cubes_with_air)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
