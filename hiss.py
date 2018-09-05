import curses

def initialize():
  return curses.initscr()

def customize_curse(stdscr):
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)

def revert_customization(stdscr):
  stdscr.keypad(0)
  curses.nocbreak()
  curses.echo()

def terminate():
  curses.endwin()

if __name__ == '__main__':
  stdscr = initialize()
  customize_curse(stdscr)
  revert_customization(stdscr)
  terminate()

