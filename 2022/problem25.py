import utils


def get_input():
    with utils.get_input_fd(__file__) as f:
        return f.read().split('\n')


def snafu_to_base_10(snafu):
    digits = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }

    return sum(
        (5 ** power) * digits[digit]
        for power, digit in enumerate(reversed(snafu))
    )


def base10_to_snafu(number):
    digits = {
        -1: '-',
        -2: '='
    }

    snafu = []

    while number > 0:
        remainder = number % 5
        if remainder > 2:
            number += remainder
            snafu.append(digits[remainder - 5])
        else:
            snafu.append(str(remainder))

        number //= 5

    return ''.join(reversed(snafu))


def part1():
    snafus = get_input()
    return base10_to_snafu(sum(snafu_to_base_10(snafu) for snafu in snafus))


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
