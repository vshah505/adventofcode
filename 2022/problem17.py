import itertools
from collections import defaultdict
import utils


ROCKS_BIT_MATRIX = [
    [[1, 1, 1, 1]],  # Horizontal Line
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  # Plus
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],  # Reverse L
    [[1], [1], [1], [1]],  # Vertical Line
    [[1, 1], [1, 1]],  # Cube
]


def get_input():
    with utils.get_input_fd(__file__) as f:
        return [1 if direction == ">" else -1 for direction in f.read().strip("\n")]


class Rock:
    def __init__(self, bit_matrix, tower_width):
        self.masks = []
        for bits in bit_matrix:
            mask = 0
            for idx, bit in enumerate(bits):
                mask += bit << (tower_width - 2 - idx - 1)
            self.masks.append(mask)

    def set_masks(self, masks):
        self.masks = masks

    def shift(self, jet, tower_width):
        right_edge_mask = 1
        left_edge_mask = 1 << (tower_width - 1)

        if any(mask & right_edge_mask for mask in self.masks) and jet == 1:
            return self.masks
        elif any(mask & left_edge_mask for mask in self.masks) and jet == -1:
            return self.masks

        return [mask >> 1 if jet > 0 else mask << 1 for mask in self.masks]


class Tower:
    def __init__(self, width, start_height):
        self.jets = itertools.cycle(get_input())
        self.tower_width = width
        self.rock_start_height = start_height

        self.tower_height = 0
        self.heights = defaultdict(int)
        self.heights[0] = (2**self.tower_width) - 1

    def is_blocked(self, masks, curr_height):
        return any(
            [(m & self.heights[curr_height + i]) > 0 for i, m in enumerate(masks)]
        )

    def simulate_rock_fall(self, rock_idx):
        rock = Rock(ROCKS_BIT_MATRIX[rock_idx], self.tower_width)
        current_height = self.tower_height + self.rock_start_height + 1
        current_jet = None

        while not self.is_blocked(rock.masks, current_height):
            current_jet = next(self.jets)
            shifted_masks = rock.shift(current_jet, self.tower_width)
            if not self.is_blocked(shifted_masks, current_height):
                rock.set_masks(shifted_masks)
            current_height -= 1

        for idx, mask in enumerate(rock.masks):
            self.heights[current_height + idx + 1] |= mask

        self.tower_height = max(self.tower_height, current_height + len(rock.masks))
        tower_state = tuple(self.heights[self.tower_height - i] for i in range(31))

        return rock_idx, current_jet, tower_state

    def simulate(self, num_rocks):
        cache = {}
        total_stopped_rocks = 0

        while total_stopped_rocks < num_rocks:
            key = self.simulate_rock_fall(total_stopped_rocks % len(ROCKS_BIT_MATRIX))
            if key in cache:
                # Found a cycle that we can repeat
                (cached_stopped_rocks, cached_height) = cache[key]
                height_difference = self.tower_height - cached_height
                rock_fall_difference = total_stopped_rocks - cached_stopped_rocks

                repeats = (num_rocks - total_stopped_rocks) // rock_fall_difference
                self.tower_height += height_difference * repeats
                break

            cache[key] = (total_stopped_rocks, self.tower_height)

            total_stopped_rocks += 1

        return self.tower_height


def part1():
    return Tower(7, 3).simulate(2022)


def part2():
    return Tower(7, 3).simulate(1000000000000)


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
