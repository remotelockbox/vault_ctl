#!/usr/bin/env python3
import argparse
import random
import vault_ctl


def main():
    parser = argparse.ArgumentParser(
        description='Set a lock time on the pivault up to the maximum number of minutes given')
    parser.add_argument('max_minutes', default=None, type=int, metavar='N',
                        help='maximum minutes to add to the lock time. If not already locked, creates a new sessions')
    parser.add_argument('--style', default='uniform', help='choose a random number generator',
                        choices=['uniform', 'middle', 'high'])

    args = parser.parse_args()

    vault_ctl.read_credentials()

    if args.max_minutes is not None:
        if args.max_minutes == 0:
            print(f"no time added")
            return
        res = lock_max(args.max_minutes, args.style)
        vault_ctl.print_response(res)
    else:
        parser.print_help()


def lock_max(max_minutes, style):
    minutes = calculate_minutes(max_minutes, style)
    dt = vault_ctl.add_minutes_to_now(minutes)
    print(f"adding {minutes} minutes")
    return vault_ctl.set_unlock_time(dt)


def calculate_minutes(max_minutes, style) -> int:
    if style == 'uniform':
        return random.randint(1, max_minutes)
    elif style == 'middle':
        return int(gauss(max_minutes))
    elif style == 'high':
        return int(random.triangular(1, max_minutes, max_minutes))


def gauss(maximum: int):
    # clamps the range to 2 std deviations of a normal distribution
    return scale(random.gauss(0.0, 1.0), -2.0, 2.0, 1, maximum)


def scale(value, low, high, new_low, new_high):
    zeroed = value - low
    scale_factor = (new_high - new_low) / float(high - low)
    factored = zeroed * scale_factor
    translated = factored + new_low

    if factored < new_low:
        return new_low
    elif factored > new_high:
        return new_high
    else:
        return translated


if __name__ == '__main__':
    main()
