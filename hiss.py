import curses
import sys
import locale

class Field:

  def __init__(self,size):
    self.__size_map = {'small':  {'width': 40, 'height': 20},
                       'medium': {'width': 60, 'height': 30},
                       'large':  {'width': 80, 'height': 40}}
    self.__width = self.__size_map[size]['width']
    self.__height = self.__size_map[size]['height']

  def get_height(self):
    return self.__height
  
  def get_width(self):
    return self.__width

class Snake:

  def __init__(self,head_x,head_y):
    self.__head = (head_x,head_y)
    self.__len = 3
    self.__body = [(head_x-1,head_y),(head_x-2,head_y)]
    self.__direction = curses.KEY_RIGHT

  def get_length(self):
    return self.__len
  
  def increment_length(self):
    self.__len += 1

  def get_head(self):
    return self.__head

  def set_head(self,new_head):
    self.__head = new_head

  def is_dead(self):
    return self.__head in self.__body 

  def add_body(self,point):
    self.__body = [point] + self.__body

  def pop_body(self):
    self.__body.pop()

  def render_snake(self,win):
    x,y = self.get_head()
    win.addch(y,x,curses.ACS_BLOCK)
    for point in self.__body:
      win.addch(point[1],point[0],curses.ACS_BLOCK)

  def get_direction(self):
    return self.__direction

  def set_direction(self,way):
    self.__direction = way

def initialize():
  locale.setlocale(locale.LC_ALL, '')
  return curses.initscr()

def spawn_window(height,width):
  win_h = height
  win_w = width
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

def play_game(win,field):

  fw = field.get_width()
  fh = field.get_height()
  snake = Snake(fw//2,fh//2)
  key = 0
  score = 0
  try:
    while key != 27:
      win.addstr(fh-1,fw-14,' Score:'+format(score,'04d')+' ')
      snake.render_snake(win)
        
      key = win.getch() 
  except Exception,e:
    revert_customization(win)
    terminate()
    print("play exception:",str(e))
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

  field = Field(scrsize)
  stdscr = initialize()
  win = spawn_window(field.get_height(),field.get_width())
  customize_curse(win)
  play_game(win,field)
  revert_customization(win)
  terminate()

