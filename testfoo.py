#!/usr/bin/env python3

import code, io, contextlib, readline

try:
    import termcolor
    def fancyprint(s):
        termcolor.cprint(s, attrs=['reverse'])
except ImportError:
    fancyprint = print


class TestConsole(code.InteractiveConsole):
  def test_input(self, lines):
      if lines[0].startswith('def '):
          fancyprint('You just defined a function!')

  def test_output(self, output):
      if output.startswith("17"):
          fancyprint("*** YOU WIN A THE INTERNET ***")

  def runcode(self, code):
      self.test_input(self.buffer)
      buf = io.StringIO()
      with contextlib.redirect_stdout(buf):
          super(TestConsole, self).runcode(code)
      print(buf.getvalue())
      self.test_output(buf.getvalue())


if __name__ == '__main__':
    t = TestConsole()
    t.interact()
