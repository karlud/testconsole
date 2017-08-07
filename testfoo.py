#!/usr/bin/env python3
#
# Trivial example of an enhanced REPL that provides feedback.

import code, io, contextlib, readline, sys

try:
    # If termcolor is available, we can display feedback highlighted.
    import termcolor
    def fancyprint(s):
        termcolor.cprint(s, attrs=['reverse'])
except ImportError:
    # If not, we'll just print the feedback normally.
    fancyprint = print


class TestConsole(code.InteractiveConsole):
  def test_input(self, lines):
      # When the student defines a new function, give them feedback.
      if lines[0].startswith('def '):
          fancyprint('You just defined a function!')

  def test_output(self, output, error):
      # When the student gets Python to print the magic number, give feedback.
      if output.startswith("17"):
          fancyprint("*** YOU WIN A THE INTERNET ***")

  def runcode(self, code):
      '''Catch the interaction between the student and Python.
      
      This overrides the parent class's runcode method, which is called to run a
      completed (possibly multi-line) block of code.  This method captures the
      code input (from self.buffer) and the stdout/stderr output from running
      the code, and dispatches to the test_ methods to give feedback.

      Note, if the student's code has a syntax error, the parent class does not
      get as far as calling runcode.
      '''
      self.test_input(self.buffer)
      outbuf = io.StringIO()
      errbuf = io.StringIO()
      with contextlib.redirect_stdout(outbuf):
          with contextlib.redirect_stderr(errbuf):
              super(TestConsole, self).runcode(code)
      print(errbuf.getvalue(), end='', file=sys.stderr)
      print(outbuf.getvalue(), end='', file=sys.stdout)
      self.test_output(outbuf.getvalue(), errbuf.getvalue())


if __name__ == '__main__':
    t = TestConsole()
    t.interact()
