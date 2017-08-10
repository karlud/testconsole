#!/usr/bin/env python3

import testconsole


class SpiritAge(testconsole.QuizEngine):
    '''This is a state engine that implements the Spirit Age quiz from cs101.'''

    def initial(self):
        firstline = self.inputs[0]

        if '"age"' in firstline or "'age'" in firstline:
            self.message("Variable names don't need quotes.")
        elif 'age' not in self.locals:
            self.message('Define a variable called "age".')
        elif type(self.locals['age']) not in [int, float]:
            self.message('The "age" variable needs a number for its value.')
        else:
            # Student defined an age variable. Go to the next step!
            self.message("It's great to be {} years old. "
                         "How many days is that?".format(self.locals['age']))
            self.state = self.days

    def days(self):
        firstline = self.inputs[0]

        if '*' not in firstline:
            self.message('Multiply age by the number of days in a year.')
        elif 'age' not in firstline:
            self.message('Make use of the "age" variable to multiply with.')
        elif '=' in firstline:
            # Student is assigning a new variable.
            self.message("Okay, you're doing a computation.  Now print it!")
            self.state = self.printonly
        elif 'print' not in firstline:
            self.message('Make sure to print the result.')
        else:
            # Student is printing an expression.  Pass to the print checker.
            self.printonly()

    def printonly(self):
        try:
            days = float(self.output)
            self.message('It sounds like you are about {} days old. Awesome!'
                         .format(days))
            self.state = self.success
        except ValueError:
            self.message('Make sure to print out only a single number.')


if __name__ == '__main__':
    t = testconsole.TestConsole(SpiritAge)
    t.interact()

