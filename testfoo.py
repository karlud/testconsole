#!/usr/bin/env python3

import code, io, contextlib, readline

class TestConsole(code.InteractiveConsole):
  def test(self, output):
    if output.startswith("17"):
      print("*** YOU WIN A THE INTERNET ***")
    else:
      print("--- Hint: try printing smallish primes ---")

  def runcode(self, code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
      super(TestConsole, self).runcode(code)
    print(buf.getvalue())
    self.test(buf.getvalue())


if __name__ == '__main__':
  t = TestConsole()
  t.interact()
