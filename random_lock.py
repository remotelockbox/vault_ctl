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
                        choices=['uniform', 'moody', 'low', 'middle', 'high'])

    args = parser.parse_args()

    vault_ctl.read_credentials()

    if args.max_minutes is not None:
        if args.max_minutes == 0:
            print(f"no time added")
            return
        res = lock_up_to(args.max_minutes, args.style)
        vault_ctl.print_response(res)
    else:
        parser.print_help()


def lock_up_to(max_minutes, style):
    if style == 'moody':
        style = style_based_on_mood()

    minutes = calculate_minutes(max_minutes, style)
    dt = vault_ctl.add_minutes_to_now(minutes)
    print(f"adding {minutes} minutes")
    return vault_ctl.set_unlock_time(dt)


def style_based_on_mood():
    # determine mood on a scale of zero to four
    mood = random.randint(0, 4)
    # convert mood from a number to an emotion
    if mood < 1:
        emotion = 'hesitant'
        style = 'low'
    elif mood < 2:
        emotion = 'fair-minded'
        style = 'uniform'
    elif mood < 3:
        emotion = 'ambivalent'
        style = 'middle'
    else:
        emotion = 'enthusiastic'
        style = 'high'

    # print emotion in english
    print(f"The AI is feeling {emotion} about locking you up.")

    return style


def calculate_minutes(max_minutes, style) -> int:
    if style == 'uniform':
        return random.randint(1, max_minutes)
    elif style == 'middle':
        return int(gauss(max_minutes))
    elif style == 'high':
        return int(random.triangular(1, max_minutes, max_minutes))
    elif style == 'low':
        return int(random.triangular(1, max_minutes, 1))


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
