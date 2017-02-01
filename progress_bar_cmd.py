#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def show_progress(value, scale, iteration, detail):
    rdy = '#' * value
    non = ' ' * (scale - value)
    progress = '[' + rdy + non + '] ' + str(iteration) + '/' + str(detail)
    print(progress, end='\r')


def bar(iteration, detail, scale=60):
    if detail >= scale:
        step = detail / scale
        j = int(iteration / step)
        show_progress(j, scale, iteration, detail)
    else:
        scale = detail
        show_progress(iteration, detail, iteration, detail)
    if iteration == detail:
        print()


if __name__ == "__main__":
    import time

    print('demo show.')
    print('process bar:')
    rng = 455
    for i in range(rng + 1):
        bar(i, rng)
        time.sleep(.01)
    print('complete!')

    rng = 20
    print('auto scale. maximum 60 cells')
    for i in range(rng + 1):
        bar(i, rng)
        time.sleep(.1)

    rng = 59
    for i in range(rng - 10, rng + 1):
        bar(i, rng)
        time.sleep(.1)

    rng = 60
    for i in range(rng - 10, rng + 1):
        bar(i, rng)
        time.sleep(.1)

    rng = 61
    for i in range(rng - 10, rng + 1):
        bar(i, rng)
        time.sleep(.1)
    print('complete!')
