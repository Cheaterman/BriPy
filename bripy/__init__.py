#!/usr/bin/env python3

import argparse
import math
import os
from time import sleep


BACKLIGHT_PATH = '/sys/class/backlight/intel_backlight'


class Backlight:
    def __init__(self):
        self.min = 1
        with open(os.path.join(BACKLIGHT_PATH, 'max_brightness')) as max_file:
            self.max = int(max_file.read())

    @property
    def current(self):
        with open(os.path.join(BACKLIGHT_PATH, 'brightness')) as current_file:
            return int(current_file.read())

    @current.setter
    def current(self, value):
        if not (self.min <= value <= self.max):
            raise ValueError('Invalid value for backlight: %r' % value)

        with open(
            os.path.join(BACKLIGHT_PATH, 'brightness'),
            'w'
        ) as current_file:
            current_file.write('%d' % value)

    @property
    def percentage(self):
        return math.log(self.current) / math.log(self.max)

    @percentage.setter
    def percentage(self, value):
        if not (0 <= value <= 1):
            raise ValueError('Invalid percentage for backlight: %r' % value)

        self.current = math.exp(value * math.log(self.max))

    def change_percentage(self, amount, default_amount=None, time=0, steps=1):
        if amount is None:
            amount = default_amount

        percentage = self.percentage

        for step in range(steps):
            self.percentage = max(
                self.min / math.log(self.max),
                min(percentage + amount / 100 * (step + 1) / steps, 1),
            )
            sleep(time / steps / 1000)

    def increase(self, amount, **kwargs):
        self.change_percentage(amount, default_amount=5, **kwargs)

    def decrease(self, amount, **kwargs):
        self.change_percentage(
            -amount if amount else amount,
            default_amount=-5,
            **kwargs
        )

    inc = increase
    dec = decrease

    def get(self):
        print(self.percentage * 100)


def main():
    parser = argparse.ArgumentParser(
        description='Control the backlight through sysfs',
    )
    parser.add_argument(
        'action',
        choices=sum(
            ((prefix, prefix + 'rease') for prefix in ('inc', 'dec')),
            tuple(),
        ) + ('+', '-', 'get'),
        help='Increase, decrease or get backlight brightness',
    )
    parser.add_argument(
        'amount',
        nargs='?',
        type=float,
        help='Percentage to increase or decrease brightness',
    )
    parser.add_argument(
        '-t',
        '--time',
        type=int,
        default=200,
        help='Length of time to spend fading the brightness',
    )
    parser.add_argument(
        '-s',
        '--steps',
        type=int,
        default=20,
        help='Number of steps to take while fading the brightness',
    )
    args = parser.parse_args()

    if args.action in ('+', '-'):
        args.action = 'inc' if args.action == '+' else 'dec'

    action_args = []
    action_kwargs = {}

    if args.action != 'get':
        action_args.append(args.amount)
        action_kwargs = {'time': args.time, 'steps': args.steps}

    backlight = Backlight()

    getattr(backlight, args.action)(*action_args, **action_kwargs)


if __name__ == '__main__':
    main()
