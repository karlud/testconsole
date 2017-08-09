#!/usr/bin/env python3
#
# Trivial example of an enhanced REPL that provides feedback.

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
    # If not, we'll just print the feedback normally.
    fancyprint = print


# A Tester is a coroutine that accepts (in, out, err, locals) tuples and yields
# messages to the student.  An (in, out, err, locals) tuple consists of the
# student's typed input, the interpreter's stdout, the interpreter's stderr,
# and the interpreter's locals dict.
def TrivialTester():
    (i, o, e, l) = yield 'Tester online!'
    while True:
        if e:
            (i, o, e, l) = yield 'Something went a bit off there. Balloon plz?'
        elif 'balloon' in i[0]:
            if 'balloon' in l:
                while True:
                    (i, o, e, l) = yield 'Yay, I have a balloon!'
            else:
                (i, o, e, l) = yield 'No no, I want a balloon variable!'
        else:
            (i, o, e, l) = yield 'No balloon, please get me a balloon'


class TestConsole(code.InteractiveConsole):
    def __init__(self, tester, *args, **kwargs):
        super(TestConsole, self).__init__(*args, **kwargs)
        self.tester = tester
        self.tester.send(None)

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
            super(TestConsole, self).runcode(code)
        print(outbuf.getvalue(), end='', file=sys.stdout)
        fancyprint(self.tester.send((inbuf,
                                     outbuf.getvalue(),
                                     '',
                                     self.locals)))


if __name__ == '__main__':
    t = TestConsole(TrivialTester())
    t.interact()
