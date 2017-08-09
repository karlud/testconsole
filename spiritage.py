#!/usr/bin/env python3

import testconsole


def SpiritAge():
    (i, o, e, l) = yield 'Tester online!'
    while 'age' not in l:
        if '"age"' in i[0] or "'age'" in i[0]:
            (i, o, e, l) = yield "Variable names don't need quotes."
        else:
            (i, o, e, l) = yield 'Define a variable called "age".'
    (i, o, e, l) = yield 'You said you are {} years old.'.format(l['age'])

    while '*' not in i[0]:
        print(i)
        (i, o, e, l) = yield 'Multiply age by the number of days in a year.'

    while 'print' not in i[0]:
        (i, o, e, l) = yield 'Make sure to print your result.'

    while True:
        try:
            days = float(o)
            break
        except ValueError:
            (i, o, e, l) = yield 'Make sure to print out only a single number.'

    while True:
        _ = yield ' *** You have passed this quiz! *** '


if __name__ == '__main__':
    t = testconsole.TestConsole(SpiritAge())
    t.interact()

