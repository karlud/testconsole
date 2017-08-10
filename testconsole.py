#!/usr/bin/env python3
#
# Trivial example of an enhanced REPL that provides feedback.
# Currently this is pretty silly.

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


class StateEngine(object):
    '''A StateEngine has many methods that consume data and return tuples
    of the form (output, newstate), where the newstate is another method.
    
    The StateEngine starts in the state called 'initial'.  Each state
    function can consume four inputs (inp, out, err, loc) defined as
    follows:
        inp - the student's input (a list of strings)
        out - the interpreter's standard output (a string)
        err - the interpreter's standard error (a string)
        loc - the intepreter's local variable dictionary

    The return value from the state function should be a tuple containing
    the message to the student, and the next state function.
    '''

    def initial(self, *args, **kwargs):
        return ('This state engine does nothing!', self.initial)

    def success(self, *args, **kwargs):
        return ('You have passed this quiz! Go to the next page.',
                self.success)

    def __init__(self):
        self.state = self.initial

    def send(self, *args, **kwargs):
        (output, newstate) = self.state(*args, **kwargs)
        self.state = newstate
        return output


class BalloonStateEngine(StateEngine):
    '''A StateEngine that wants you to define a balloon variable.'''
    def initial(self, inp, out, err, loc):
        if err:
            return ('Something went wrong there. Balloon plz?', self.initial)
        elif 'balloon' in loc:
            return ('Yay, I have a balloon!', self.success)
        elif 'balloon' in inp[0]:
            return ('I want a variable _named_ balloon.', self.initial)
        else:
            return ('I want a balloon.', self.initial)


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
        fancyprint(self.engine.send(inbuf,
                                    outbuf.getvalue(),
                                    errbuf.getvalue(),
                                    self.locals))


if __name__ == '__main__':
    t = TestConsole(BalloonStateEngine)
    t.interact()
