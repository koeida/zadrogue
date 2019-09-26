import curses
from random import randint, choice
from math import sqrt
from copy import deepcopy

status = []
news = ["Welcome to GOBBO THIEF!"]

tiles = { 0: (".", 9, True),
          1: ("#", 2,False),
          2: ("_", 2,False),
          3: ("\"", 3,True),
          4: ("/", 2,True),
          5: ("]", 10,True),
          6: ("]", 11,True),
          7: ("]", 12, True),
          8: ("~",16,True)}

class Creature:
    def __init__(self, x, y, tile, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.tile = tile
        self.target = None
        self.type = type
        self.target_steps = 0
        self.inv = []
        self.health = 3
        self.did_attack = False
        self.is_stuck = False
        self.distracted = 0
        
class Object:
    def __init__(self, x, y, tile, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.tile = tile
        self.type = type

        
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


def change_level(level, inv = []):
    floorplan_file = level.m
    gobbonum = level.num_gobbos
    coinum = level.num_gold
    time = level.time
    creatures = []
    objects = []
    floorplan = read_floorplan(floorplan_file)
    
    width = len(floorplan[1])
    height = len(floorplan)
       
     # x, y, image, color
    
    player = Creature(18, 17, "@", 1, "player")
    creatures.append(player)
    
    player.inv = inv
    rawck = Object(0,0,".", 12, "rock")
    player.inv.append(rawck)
    
    gobbo = Creature(0,0, "&", 4, "gobbo")
    spawn_random(1, width - 1, 1, height - 2, gobbo, floorplan, creatures, gobbonum)

    villager = Creature(0, 0, "v", 17, "villager")
    spawn_random(1, width - 1, 1, height - 2, villager, floorplan, creatures, level.num_villagers)
    
    chest = Object(0,0,"=", 15, "treasure chest")
    spawn_random(1, width - 1, 1, 5, chest, floorplan, objects, 1)
    
    coin = Object(0,0,"$",15,"coin")
    spawn_random(1, width - 1, 1, height - 2, coin, floorplan, objects, coinum)

    for i in level.inhabitants:
        creatures.append(i)

    return (creatures, objects, floorplan, time)

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
        
        #FIX THIS
        try:
            column = list(columns[c.x])
        except:            
            return
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
    
def offmap(x, y, floorplan):
    width = len(floorplan[1])
    height = len(floorplan)
    
    if x >= width or x < 0:
        return True
    #4) Is y off the map? If so, return False
    if y >= height or y < 0:
        return True
    
    return False

def spawn_random(minx, maxx, miny, maxy, obj, m, dest_list, count):
    for x in range(count):
        o = deepcopy(obj)
        success = False
        while (success != True):
            o.x = randint(minx, maxx-1)
            o.y = randint(miny, maxy-1)
            obspot = m[o.y][o.x]
            if obspot not in [1,2,6]:
                success = True
                dest_list.append(o)
            
    
    
    

def wakabal(tilenum, x, y, floorplan, critter):

    # Is critter stuck? If so, make them unstuck and return false ("not wakabal")
    if critter.is_stuck:
        critter.is_stuck = False
        return False
    if tilenum == 8:
        critter.is_stuck = True
    
    if tilenum != 1 and tilenum != 2:
        return True
    elif critter.type == "shoppo" and tilenum == 4:
        return False
    else:
        return False
    
def move_to_target(tx, ty, cx, cy):
    xmod = 0
    ymod = 0
    if tx > cx:
        xmod = 1
    if tx < cx:
        xmod = -1
    if ty > cy:
        ymod = 1
    if ty < cy:
        ymod = -1
    
    if xmod != 0 and ymod != 0:
        if randint(1,2) == 1:
            xmod = 0
        else:
            ymod = 0
            
    return (xmod, ymod)

def get_gobbo_target(gobbo):
    if gobbo.target != None:              
        tx = gobbo.target[0]
        ty = gobbo.target[1]        
    else:
        tx, ty = wander(gobbo)
    return (tx,ty)

def tick_shoppo(c,player,floorplan):
    oldx = c.x
    oldy = c.y
    tx, ty = wander(c)
    xmod, ymod = move_to_target(tx, ty, c.x, c.y)
    c.x += xmod
    c.y += ymod
    villager_sez(c, player)
    if gobbo_invalid_move(c, floorplan, oldx, oldy):
        c.y = oldy
        c.x = oldx

def tick_villy(c, player, floorplan):
    oldx = c.x
    oldy = c.y
    tx, ty = wander(c)
    xmod, ymod = move_to_target(tx, ty, c.x, c.y)
    c.x += xmod
    c.y += ymod
    villager_sez(c, player)

    if gobbo_invalid_move(c, floorplan, oldx, oldy):
        c.y = oldy
        c.x = oldx


def villager_sez(c, player):
    villy_speek = ["Gooday stranger, welcome to our modest little town of Brorldown.","I see you are loaded with stolen loot! Might I sugest you check out our magic item shops?","Oh its you, the notorious Namafero, raider of goblins! It is an honor to have you in our town...", "'Sup!"]

    if distance(c, player) < 2:
        news.append("Villager sez: " + choice(villy_speek))


def wander(c):
    tx = c.x + randint(-1, 1)
    ty = c.y + randint(-1, 1)
    return tx, ty

def bump_steps(c, oldx, oldy, m):
    tilenum = m[c.y][c.x]
    if (m[oldy][oldx] not in [5,6]) and tilenum == 6:
        return True
    if (m[oldy][oldx] == 6) and tilenum not in [5,6]:
        return True
    return False
    
def gobbo_invalid_move(gobbo, m, oldx, oldy):    
    if offmap(gobbo.x, gobbo.y, m):
        return True
    
    tilenum = m[gobbo.y][gobbo.x]
    if not wakabal(tilenum,gobbo.x,gobbo.y,m,gobbo):
        return True
    
    if bump_steps(gobbo, oldx, oldy, m):
        return True
    
    return False

def gobbo_attack(gobbo,player,m):
    # Make gobbo stand in place for a few turns after it hits you
    if gobbo.did_attack == True:
        if randint(1,4) == 1:
            gobbo.did_attack = False
        return
    
    if distance(gobbo, player) <= 1:
        player.health -= 1
        news.append("Oof! You got attacked!")
        gobbo.did_attack = True
        
def gobbo_vision(gobbo, player, m):
    if gobbo.distracted > 0:
        gobbo.distracted -= 1
        return

    if is_visible_old(gobbo, player, m):
        gobbo.tile = "!"
        gobbo.target = (player.x,player.y)        
    else:
        gobbo.tile = "&"

def tick_gobbo(gobbo, player, m):    
    move_gobbo(gobbo, player, m)
    gobbo_attack(gobbo,player, m)
    gobbo_vision(gobbo,player, m)
    
def move_gobbo(gobbo, player, m):
    oldx = gobbo.x
    oldy = gobbo.y
    
    if gobbo.did_attack:
        return
    
    tx, ty = get_gobbo_target(gobbo)
        
    # Make gobbo give up chasing target after a while
    if (tx == gobbo.x and ty == gobbo.y) or gobbo.target_steps >= 10:
        gobbo.target_steps = 0
        gobbo.target = None
    
    xmod, ymod = move_to_target(tx,ty,gobbo.x,gobbo.y)
    gobbo.x += xmod
    gobbo.y += ymod
    gobbo.target_steps += 1
    
    if gobbo_invalid_move(gobbo, m, oldx, oldy):
        gobbo.y = oldy
        gobbo.x = oldx
        
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
        
def drop_first(f,l):
    for x in l:
        if f(x):
            l.remove(x)
            return
   
def throw_rock(player, objects, creatures, stdscr, m):
    width = len(m[1])
    height = len(m)
    news.append("Where do you want to throw the rock?")
    display_news(stdscr, news, width, height)
    stdscr.addstr(player.y - 1,player.x, "^", curses.color_pair(1)),
    stdscr.addstr(player.y + 1,player.x, "v", curses.color_pair(1))
    stdscr.addstr(player.y,player.x - 1, "<", curses.color_pair(1))
    stdscr.addstr(player.y,player.x + 1, ">", curses.color_pair(1))
    stdscr.refresh()
                                                 
    inp = stdscr.getch()
    dx = 0
    dy = 0
    if inp == curses.KEY_DOWN:
        dy = 5 
    elif inp == curses.KEY_UP:
        dy = -5
    elif inp == curses.KEY_LEFT:
        dx = -5
    elif inp == curses.KEY_RIGHT:
        dx = 5

    news.append("Yeet!")
                           
    drop_first(lambda x: x.type == "rock", player.inv)
    rock = Object(player.x + dx, player.y + dy,".", 12, "rock")
    objects.append(rock)   
    enemies = filter(lambda c: c.type != "player" and distance(c,rock) <= 10, creatures)
    for e in enemies:
        e.target = (rock.x, rock.y)
        e.distracted = 3

def keyboard_input(inp, player, m, objects, creatures, stdscr):
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
    elif inp == ord('t') and any(lambda o: o.type == "rock", player.inv):
        throw_rock(player, objects, creatures, stdscr, m)
        
    if offmap(player.x, player.y, m) == False:
        tilenum = m[player.y][player.x]
        if not wakabal(tilenum,player.x,player.y,m, player):
            player.x = oldx
            player.y = oldy
        if (m[oldy][oldx] not in [5,6,7]) and tilenum in [6,7]:
            player.x = oldx
            player.y = oldy
        if (m[oldy][oldx] in [6,7]) and tilenum not in [5,6,7]:
            player.x = oldx
            player.y = oldy
    else:
        player.x = oldx
        player.y = oldy

def read_floorplan(fname):
    f = file(fname,"r")
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
            

def display_news(screen, news, width, height):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    MAP_HEIGHT = height
    MAP_WIDTH = width
    for n in top_news:
        screen.addstr(MAP_HEIGHT + cn + 1, 0, " " * MAP_WIDTH, curses.color_pair(10 + cn)), 
        screen.addstr(MAP_HEIGHT + cn + 1, 0, n, curses.color_pair(10 + cn))
        cn += 1

def init_colors():
    curses.init_color(2, 600, 400, 255)
    curses.init_color(3, 0, 1000, 0)
    curses.init_color(4, 100, 400, 0)
    
    # Shades of grey for news
    curses.init_color(10, 800, 800, 800)
    curses.init_color(11, 600, 600, 600)
    curses.init_color(12, 400, 400, 400)
    curses.init_color(13, 300, 300, 300)
    
    curses.init_color(5, 0, 1000, 0)
    curses.init_color(6, 0, 500, 0)
    curses.init_color(7, 1000, 600, 0)
    curses.init_color(8, 1000, 1000, 1000)
    curses.init_color(9, 1000, 1000, 0)
    
    curses.init_color(14, 301, 376, 929)
    curses.init_color(15, 603, 454, 243)
    
    
    
    
    
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    
    curses.init_pair(5, 6, 5) # SAFE LIGHT
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_RED) # DANGER LIGHT
    curses.init_pair(7, 7, 9) # DANGER LIGHT
    curses.init_pair(9, 8, curses.COLOR_BLACK)
    
    # News fadeout
    curses.init_pair(10, 10, curses.COLOR_BLACK)
    curses.init_pair(11, 11, curses.COLOR_BLACK)
    curses.init_pair(12, 12, curses.COLOR_BLACK)
    curses.init_pair(13, 13, curses.COLOR_BLACK)
    curses.init_pair(14, 13, curses.COLOR_BLACK)
    curses.init_pair(15, 9, curses.COLOR_BLACK)
    
    curses.init_pair(16, 14, curses.COLOR_BLACK)

    curses.init_pair(17, 15, curses.COLOR_BLACK)


    
    
