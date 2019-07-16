import curses
from random import randint
from math import sqrt

status = []


    

class Creature:
    def __init__(self, x, y, tile, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.tile = tile
        self.target = None
        self.type = type
        self.target_steps = 0
        
def distance(c1,c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)

def any(f,l):
    for x in l:
        if f(x):
            return True
    return False
        
def output_status(screen):
    for s in status[-5:].__reversed__():
        screen.addstr(status_y + csy, 0, s, 1) # Display status string
        csy += 1
        
def its_opaque(tile_num, tiles):
    cur_tile_info = tiles[tile_num]    
    return not cur_tile_info[2]

def is_visible_old(c, t, floorplan):    
    """Is t visible to c?"""
    global status   
    
    if c.y == t.y:
        row = floorplan[c.y]
        
        #Look to the left
        for cur_x in range(c.x, t.x - 1, -1):        
            if cur_x == t.x:
                return True
            cur_tile_num = row[cur_x]            
            if its_opaque(cur_tile_num, tiles):
                break
            
        #Look to the right
        for cur_x in range(c.x, t.x + 1):        
            if cur_x == t.x:
                return True
            cur_tile_num = row[cur_x]            
            if its_opaque(cur_tile_num, tiles):
                break
    elif c.x == t.x:    
        columns = rotate_list(floorplan)
        column = list(columns[c.x])
        column.reverse()
        
        #Look up        
        
        
        for cur_y in range(c.y, t.y - 1, -1):            
            cur_tile_num = column[cur_y]            
            if its_opaque(cur_tile_num, tiles):
                break
            if cur_y == t.y:                
                return True
            
           
                
        #look down
        for cur_y in range(c.y, t.y + 1):        
            if cur_y == t.y:
                return True
            cur_tile_num = column[cur_y]           
            if its_opaque(cur_tile_num, tiles):
                break
    else:
        return False
    
tiles = { 0: (".", 9, True),
          1: ("#", 2,False),
          2: ("_", 2,False),
          3: ("\"", 3,True),
          4: ("/", 2,True)}

def offmap(x, y, floorplan):
    width = len(floorplan[1])
    height = len(floorplan)
    
    if x >= width or x < 0:
        return True
    #4) Is y off the map? If so, return False
    if y >= height or y < 0:
        return True
    
    return False

def wakabal(tilenum, x, y, floorplan):
    #Are we off the map?
    #1) Get map width
   
    #3) Is x off the map? If so, return False  
    
    if tilenum != 1 and tilenum != 2:
        return True
    else:
        return False
    
def move_gobbo(gobbo, player, m):
    oldx = gobbo.x
    oldy = gobbo.y    
    
    if gobbo.target != None:
        gobbo.target_steps +=1       
        tx = gobbo.target[0]
        ty = gobbo.target[1]
        if (tx == gobbo.x and ty == gobbo.y) or gobbo.target_steps >= 10:
            gobbo.target_steps = 0
            gobbo.target = None
    else:
        tx = gobbo.x + randint(-1,1)
        ty = gobbo.y + randint(-1,1)
        
        
    if tx > gobbo.x:
        gobbo.x += 1
    if tx < gobbo.x:
        gobbo.x -= 1
    
    if offmap(gobbo.x, gobbo.y, m) == False:
        tilenum = m[gobbo.y][gobbo.x]
        if not wakabal(tilenum,gobbo.x,gobbo.y,m):
           gobbo.y = oldy
           gobbo.x = oldx
    else:
        gobbo.y = oldy
        gobbo.x = oldx
       
    oldx = gobbo.x
    oldy = gobbo.y
       
    if ty > gobbo.y:
        gobbo.y += 1
    if ty < gobbo.y:
        gobbo.y -= 1
    if offmap(gobbo.x, gobbo.y, m) == False:
        tilenum = m[gobbo.y][gobbo.x]
        if not wakabal(tilenum,gobbo.x,gobbo.y,m):
           gobbo.y = oldy
           gobbo.x = oldx
    else:
        gobbo.y = oldy
        gobbo.x = oldx
       
    if is_visible_old(gobbo, player, m):
        gobbo.tile = "!"
        gobbo.target = (player.x,player.y)        
    else:
        gobbo.tile = "&"
        
def do_doors(x,y,m,a,b):
    """Look at tiles around x and y on map m: if any are of type a, change them to type b"""
    if m[y - 1][x] == a:
        m[y - 1][x] = b
        
    if m[y + 1][x] == a:
        m[y + 1][x] = b
        
    if m[y][x + 1] == a:
        m[y][x + 1] = b
        
    if m[y][x - 1] == a:
        m[y][x - 1] = b  
   

def keyboard_input(inp, player, m):
    oldx = player.x
    oldy = player.y
    if inp == curses.KEY_DOWN:
        player.y += 1        
    elif inp == curses.KEY_UP:
        player.y -= 1
    elif inp == curses.KEY_LEFT:
        player.x -= 1
    elif inp == curses.KEY_RIGHT:        
        player.x += 1
    elif inp == ord('o'):
        do_doors(player.x,player.y, m,2,4)
    elif inp == ord('c'):
        do_doors(player.x,player.y, m,4,2)
        
    if offmap(player.x, player.y, m) == False:
        tilenum = m[player.y][player.x]
        if not wakabal(tilenum,player.x,player.y,m):
            player.x = oldx
            player.y = oldy
    else:
        player.x = oldx
        player.y = oldy

def read_floorplan():
    f = file("floorplan.txt","r")
    lines = f.readlines()
    lines = map(lambda l: map(int, list(l.strip())), lines)
    f.close()
    return lines
        
def rotate_list(l, n = 1):
    newlist = l
    for x in range(n):
        newlist = list(zip(*newlist[::-1]))
    return newlist

def anyslice(i1,i2,l):
    s,e = (i1,i2) if i1 < i2 else (i2,i1)
    return l[s:e]



def wall_between(i1,i2,row):
    tiles_between = anyslice(i1,i2,row)        
    return False if 1 in tiles_between else True

def is_visible(c, t, floorplan):
    if c.y == t.y:
        row = floorplan[c.y]
        return wall_between(c.x,t.x,row)
    elif c.x == t.x:        
        row = rotate_list(floorplan,3)[c.x]
        return wall_between(c.y,t.y,row)        
    else:
        return False
    
floorplan_t = [[0,4,2],
               [3,1,5],
               [6,7,8]]
foo = Creature(2,0,None,None,None)
bar = Creature(0,0,None,None,None)
assert(is_visible(foo,bar,floorplan_t))
foo = Creature(0,2,None,None,None)
bar = Creature(0,2,None,None,None)
assert(is_visible(foo,bar,floorplan_t))
foo = Creature(0,1,None,None,None)
bar = Creature(2,1,None,None,None)
assert(not is_visible(foo,bar,floorplan_t))
foo = Creature(2,1,None,None,None)
bar = Creature(0,1,None,None,None)
assert(not is_visible(foo,bar,floorplan_t))

def draw_map(screen, m, tiles, x = 0, y = 0):
    for cy in range(len(m)):
        for cx in range(len(m[cy])):
            tile_id = m[cy][cx]
            img, color, opacity = tiles[tile_id]
            
            screen.addstr(y + cy, x + cx, img, curses.color_pair(color))

def init_colors():
    curses.init_color(2, 600, 400, 255)
    curses.init_color(3, 0, 1000, 0)
    curses.init_color(4, 100, 400, 0)
    
    curses.init_color(5, 0, 1000, 0)
    curses.init_color(6, 0, 500, 0)
    curses.init_color(7, 1000, 600, 0)
    curses.init_color(8, 1000, 1000, 1000)
    curses.init_color(9, 1000, 1000, 0)
    
    
    
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    
    curses.init_pair(5, 6, 5) # SAFE LIGHT
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_RED) # DANGER LIGHT
    curses.init_pair(7, 7, 9) # DANGER LIGHT
    curses.init_pair(9, 8, curses.COLOR_BLACK)
