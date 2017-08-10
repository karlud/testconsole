#!/usr/bin/env python3
#
# An enhanced Python REPL that can lead the student through an interactive
# programming quiz.
#
# To define a quiz, you define a subclass of the QuizEngine class, including
# a method called 'initial' and (potentially) some other methods.  Each of
# these methods represents a _state_ that the quiz can be in; roughly, a step
# that the student can be working on.  When the student completes a step,
# the QuizEngine gets advanced to the next step (by altering self.state).
#
# See the BalloonQuizEngine for a worked example.
#


import code
import io
import contextlib
import readline
import sys

try:
    # If termcolor is available, we can display feedback highlighted.
    import termcolor

    def fancyprint(s):
        termcolor.cprint(s, attrs=['reverse'])
except ImportError:
    print('Warning, no termcolor module - feedback will not be reverse video')
    # If not, we'll just print the feedback normally.
    fancyprint = print


# Workaround for Python 3.4 and earlier that lack redirect_stderr.
if 'redirect_stderr' not in dir(contextlib):
    print('Warning, no stderr redirection - upgrade to 2016 Python!\n')
    @contextlib.contextmanager
    def dummy(_):
        yield sys.stderr
    contextlib.redirect_stderr = dummy


class QuizEngine(object):
    '''A QuizEngine has many methods that consume data and return tuples
    of the form (output, newstate), where the newstate is another method.
    
    The QuizEngine starts in the state called 'initial'.  Each state is a
    function that gets called to handle the student's latest input.  Each
    state function has access to these member variables:

        self.inputs - a list of strings, the student's current input
        self.output - a string, the interpreter's last write to standard output
        self.error - a string, the interpreter's last write to standard error
        self.locals - a dictionary, the interpreter's local variables

    The state function is responsible for calling self.message() to display a
    message to the student (if desired) and updating self.state to point to a
    different state function (if the student has made progress).

    To indicate the successful end of a quiz, change the state to self.success.
    '''

    def message(self, msg):
        '''Display a message to the student.'''
        fancyprint(msg)

    def initial(self):
        self.message('This state engine does nothing!')
        self.state = self.success

    def success(self):
        self.message('You have passed this quiz! Go to the next page.')

    def __init__(self):
        self.state = self.initial

    def send(self, inputs, output, error, locals):
        self.inputs = inputs
        self.output = output
        self.error = error
        self.locals = locals
        self.state()


class BalloonQuizEngine(QuizEngine):
    '''A QuizEngine that wants the student to define a 'balloon' variable.'''
    def initial(self):
        if self.error:
            self.message('Something went wrong there. Balloon plz?')
        elif 'balloon' in self.locals:
            self.message('Yay, I have a balloon!')
            self.state = self.success
        elif 'balloon' in self.inputs[0]:
            self.message('I want a variable _named_ balloon.')
        else:
            self.message('I want a balloon')


class TestConsole(code.InteractiveConsole):
    def __init__(self, engine, *args, **kwargs):
        super(TestConsole, self).__init__(*args, **kwargs)
        self.engine = engine()

    def runcode(self, code):
        '''Catch the interaction between the student and Python.

        This overrides the parent class's runcode method, which is called to
        run a completed (possibly multi-line) block of code.  This method
        captures the code input (from self.buffer) and the stdout/stderr output
        from running the code, and dispatches to a tester coroutine to do the
        actual testing.

        Note, if the student's code has a syntax error, the parent class does
        not get as far as calling runcode.
        '''
        inbuf = self.buffer
        outbuf = io.StringIO()
        errbuf = io.StringIO()
        with contextlib.redirect_stdout(outbuf):
            with contextlib.redirect_stderr(errbuf):
                super(TestConsole, self).runcode(code)
        print(errbuf.getvalue(), end='', file=sys.stderr)
        print(outbuf.getvalue(), end='', file=sys.stdout)
        self.engine.send(inbuf,
                         outbuf.getvalue(),
                         errbuf.getvalue(),
                         self.locals)


if __name__ == '__main__':
    t = TestConsole(BalloonQuizEngine)
    t.interact()
