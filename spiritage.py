#!/usr/bin/env python3

import testconsole


class SpiritAge(testconsole.StateEngine):
    '''This is a state engine that implements the Spirit Age quiz from cs101.'''

    def initial(self, inp, out, err, loc):
        if '"age"' in inp[0] or "'age'" in inp[0]:
            return ("Variable names don't need quotes.", self.initial)
        elif 'age' not in loc:
            return ('Define a variable called "age".', self.initial)
        
        try:
            years = float(loc['age'])
        except ValueError:
            return ('The "age" variable needs a number for its value.',
                    self.initial)
        
        # Student defined an age variable. Go to the next step!
        return ("It's great to be {} years old. How many days is that?"
                .format(loc['age']), self.days)

    def days(self, inp, out, err, loc):
        if '*' not in inp[0]:
            return ('Multiply age by the number of days in a year.', self.days)

        if 'age' not in inp[0]:
            return ('Make use of the "age" variable to multiply with.',
                    self.days)

        if 'print' not in inp[0]:
            return ('Make sure to print the result.', self.days)

        try:
            days = float(out)
        except ValueError:
            return ('Make sure to print out only a single number.', self.days)

        return ('It sounds like you are {} days old. Awesome!'.format(days),
                self.success)


if __name__ == '__main__':
    t = testconsole.TestConsole(SpiritAge)
    t.interact()

