import curses

def initialize():
  return curses.initscr()

def terminate():
  curses.endwin()

if __name__ == '__main__':
  stdscr = initialize()
  terminate()
