import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return list(map(int, f.read().split("\n")))


def get_grove_coordinates(encrypted_file, num_iterations):
    max_index = len(encrypted_file) - 1
    indices = [idx for idx in range(len(encrypted_file))]

    for _ in range(num_iterations):
        for i, value in enumerate(encrypted_file):
            idx = indices.index(i)
            idx_in_pos = indices.pop(idx)
            rotated_idx = (idx + value) % max_index
            indices.insert(rotated_idx, idx_in_pos)

    decrypted_file = [encrypted_file[idx] for idx in indices]

    return [
        decrypted_file[idx]
        for idx in [
            (decrypted_file.index(0) + offset) % len(decrypted_file)
            for offset in [1000, 2000, 3000]
        ]
    ]


def part1():
    encrypted_file = get_input()
    return sum(get_grove_coordinates(encrypted_file, 1))


def part2():
    encrypted_file = get_input()
    decryption_key = 811589153
    encrypted_file = [value * decryption_key for value in encrypted_file]
    return sum(get_grove_coordinates(encrypted_file, 10))


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
