import curses
import sys

def initialize():
  return curses.initscr()

def spawn_window(winsize):
  size_map = {'small':  {'width': 40, 'height': 20},
              'medium': {'width': 60, 'height': 30},
              'large':  {'width': 80, 'height': 40}}
  win_h = size_map[winsize]['height']
  win_w = size_map[winsize]['width']
  offset_y = 1
  offset_x = 2
  playfield = curses.newwin(win_h,win_w,offset_y,offset_x)    
    
  return playfield

def customize_curse(win):
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  win.keypad(1)
  win.border(0)
  win.nodelay(1)

def play_game(win):
  key = 0
  try:
    while key != 27:
      win.addstr(1,1,'hello') 
      key = win.getch() 
  except:
    revert_customization(win)
    terminate()
    exit(1)

def revert_customization(win):
  win.nodelay(0)
  win.border(1)
  win.keypad(0)
  curses.curs_set(1)
  curses.nocbreak()
  curses.echo()

def terminate():
  curses.endwin()

if __name__ == '__main__':

  if len(sys.argv) > 1:
    scrsize = sys.argv[1]
    if not scrsize in ['small','medium','large']:
      print('Invalid screen size provided. Exiting...')
      exit(1)
  else:
    scrsize = 'small'

  stdscr = initialize()
  win = spawn_window(scrsize)
  customize_curse(win)
  play_game(win)
  revert_customization(win)
  terminate()

