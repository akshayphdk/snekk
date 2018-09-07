import curses
import sys
import locale
import random

from curses import KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN

class Field:

  def __init__(self,size):
    # dictionary to determine size of playing field.
    self.__size_map = {'small':  {'width': 40, 'height': 20},
                       'medium': {'width': 60, 'height': 30},
                       'large':  {'width': 80, 'height': 40}}
    self.__width = self.__size_map[size]['width']
    self.__height = self.__size_map[size]['height']

  # accessor for field height.
  def get_height(self):
    return self.__height

  #accessor for field width.
  def get_width(self):
    return self.__width

  # method to generate food randomly within the field.
  def spawn_food(self):
    return (random.randint(2,self.get_width()-2),random.randint(2,self.get_height()-2)) 

class Snake:

  # create a snake of size 3 in the center of the field moving right.
  def __init__(self,head_x,head_y):
    self.__head = (head_x,head_y)
    self.__len = 3
    self.__body = [(head_x-1,head_y),(head_x-2,head_y)]
    self.__direction = KEY_RIGHT

  # accesor for length of snake.
  def get_length(self):
    return self.__len
  
  # mutator for length of snake wherein length always increases by 1.
  def increment_length(self):
    self.__len += 1

  # accessor for current position of snake's head.
  def get_head(self):
    return self.__head
 
  # mutator for setting current position of snake's head.
  def set_head(self,new_head):
    self.__head = new_head

  # check if snake has hit itself.
  def is_dead(self):
    return self.__head in self.__body 

  def in_body(self,point):
    return point in self.__body

  # add a point to the snake's body starting from the head.
  def add_body(self,point):
    self.__body = [point] + self.__body

  # remove a point from snake's body starting from tail.
  def pop_body(self):
    return self.__body.pop()

  # method to render the snake. 
  def render_snake(self,win):
    code = locale.getpreferredencoding()
    x,y = self.get_head()
    win.addch(y,x,curses.ACS_DIAMOND)
    for point in self.__body:
      win.addch(point[1],point[0],curses.ACS_DIAMOND)

  # accessor for snake's current direction.
  def get_direction(self):
    return self.__direction

  # mutator for setting snake's direction.
  def set_direction(self,way):
    self.__direction = way

def initialize():

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

  win.timeout(90)
  win.addstr(0,(fw//2)-6,' SNEKK v0.1 ')

  food = (3*fw//4,3*fh//4)
  win.addch(food[1],food[0],'*')

  try:
    while key != 27 and not snake.is_dead():

      win.addstr(fh-1,fw-14,' Score:'+format(snake.get_length()-3,'04d')+' ')

      if key in [KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN]:
        if (key == KEY_LEFT and snake.get_direction() != KEY_RIGHT) or \
           (key == KEY_RIGHT and snake.get_direction() != KEY_LEFT) or \
           (key == KEY_UP and snake.get_direction() != KEY_DOWN) or \
           (key == KEY_DOWN and snake.get_direction() != KEY_UP):
          snake.set_direction(key)

      old_head = snake.get_head()

      if old_head == food:
        snake.increment_length()
        snake.add_body(food)
        
        food = field.spawn_food()
        while snake.in_body(food):
          food = field.spawn_food()
        win.addch(food[1],food[0],'*')

      if snake.get_direction() == KEY_RIGHT:
        if old_head[0] == fw-2:
          snake.set_head((1,old_head[1]))
        else:
          snake.set_head((old_head[0]+1,old_head[1]))
      elif snake.get_direction() == KEY_LEFT:
        if old_head[0] == 1:
          snake.set_head((fw-2,old_head[1]))
        else:
          snake.set_head((old_head[0]-1,old_head[1]))
      elif snake.get_direction() == KEY_UP:
        if old_head[1] == 1:
          snake.set_head((old_head[0],fh-2))
        else:
          snake.set_head((old_head[0],old_head[1]-1))
      else:
        if old_head[1] == fh-2:
          snake.set_head((old_head[0],1))
        else:
          snake.set_head((old_head[0],old_head[1]+1))
    
      snake.add_body(old_head)
      tail = snake.pop_body()
      win.addch(tail[1],tail[0],' ')
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

