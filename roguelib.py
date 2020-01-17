import curses
from random import randint, choice

import creatures
from copy import deepcopy
from display import display_news, prompt
from gamemap import *
from misc import distance, drop_first, any
from objects import Object, caltropz
from rnews import *

status = []

def conv_if_int(s):
    try:
        return int(s)
    except:
        return s


def read_floorplan(fname):
    f = file(fname,"r")
    lines = f.readlines()
    lines = map(lambda l: map(conv_if_int, list(l.strip())), lines)
    f.close()
    return lines

def change_level(level, inv = [], coins=0):
    floorplan_file = level.m
    gobbonum = level.num_gobbos
    coinum = level.num_gold
    time = level.time
    cs = []
    objects = level.objects
    floorplan = read_floorplan(floorplan_file)
    
    width = len(floorplan[1])
    height = len(floorplan)
       
     # x, y, image, color
    
    player = creatures.Creature(18, 17, "@", 1, "player")
    player.coins = coins
    cs.append(player)
    
    player.inv = inv
    rawck = Object(0,0,".", 12, "rock")
    player.inv.append(rawck)

    
    gobbo = creatures.Creature(0, 0, "&", 4, "gobbo")
    spawn_random(1, width - 1, 1, height - 2, gobbo, floorplan, cs, gobbonum)

    villager = creatures.Creature(0, 0, "v", 17, "villager")
    spawn_random(1, width - 1, 1, height - 2, villager, floorplan, cs, level.num_villagers)
    for v in cs:
        if v.type == "villager" and level.name == "The dwarven village of Brorldown":
            brorlspeeches = ["Gooday stranger, welcome to our modest little town of Brorldown.",
                        "I see you are loaded with stolen loot! Might I sugest you check out our magic item shops?",
                        "Oh its you, the notorious Namafero, raider of goblins! It is an honor to have you in our town...",
                        "'Sup!",
                        "I hope you enjoy your stay here, adventurer!"]
            v.speek = choice(brorlspeeches)
        if v.type == "villager" and level.name == "The Begining":
            tankspeeches = ["Gooday stranger, welcome to our modest little town of Tankton.",
                        "I hear the town mage wants to converse with you.",
                        "You're going into the goblin base? That's madness! You'll die!",
                        "Hello there!",
                        "I hope you enjoy your stay here, adventurer!"]
            v.speek = choice(tankspeeches)
    
    chest = Object(0,0,"=", 15, "treasure chest")
    spawn_random(1, width - 1, 1, 5, chest, floorplan, objects, 1)
    
    coin = Object(0,0,"$",15,"coin")
    spawn_random(1, width - 1, 1, height - 2, coin, floorplan, objects, coinum)

    for i in level.inhabitants:
        cs.append(i)

    return (cs, objects, floorplan, time)


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

   
def throw_rock(player, objects, cs, stdscr, m):
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
    enemies = filter(lambda c: c.type != "player" and distance(c,rock) <= 10, cs)
    for e in enemies:
        e.target = (rock.x, rock.y)
        e.distracted = 3

def keyboard_input(inp, player, m, objects, cs, stdscr):
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
        creatures.do_doors(player.x, player.y, m, 2, 4)
    elif inp == ord('c'):
        creatures.do_doors(player.x, player.y, m, 4, 2)
    elif inp == ord('t') and any(lambda o: o.type == "rock", player.inv):
        throw_rock(player, objects, cs, stdscr, m)
    elif inp == ord('u'):
        wvich1 = prompt(stdscr, 30, "What item do you want to use?")
        wvich1 = wvich1 - 48 - 1
        if wvich1 in range(10):
            # Convert it to an int
            if wvich1 < len(player.inv):
                # Set a variable to the object we wanna use
                useditem = player.inv[wvich1]
                useditem.effect(player, cs, m, objects)
                player.inv.remove(useditem)
                # Remove it from inventory



        
    if offmap(player.x, player.y, m) == False:
        tilenum = m[player.y][player.x]
        if not creatures.wakabal(tilenum, player.x, player.y, m, player, objects):
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
