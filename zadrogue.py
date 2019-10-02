from creatures import *
from display import init_colors, draw_map
from roguelib import *
from collections import namedtuple
from misc import any

Level = namedtuple("Level", "m num_gobbos num_villagers num_gold time inhabitants")

shopkeeper1 = Creature(47,3, "v", 17, "shoppo")

levels = [
    Level(m="floorplan.txt",
          num_gobbos=5, num_villagers=0, num_gold=5,
          time=150, inhabitants=[]),
    Level(m="floorplan2.txt",
          num_gobbos=10, num_villagers=0, num_gold=5,
          time=150, inhabitants=[]),
    Level(m="floorplan3.txt",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=200, inhabitants=[]),
    Level(m="floorplan_4.txt",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=200, inhabitants=[]),
    Level(m="floorplan_5.txt",
          num_gobbos=0, num_villagers=5, num_gold=2,
          time=20000, inhabitants=[shopkeeper1])
]


def main(stdscr):
    inp = 0
    current_level = 0
    
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    
    creatures, objects, floorplan, timer = change_level(levels[current_level])
    width = len(floorplan[1])
    height = len(floorplan)

    while(inp != 113): # Quit game if player presses "q"
        stdscr.clear()
        player = list(filter(lambda c: c.type == "player", creatures))[0]
        timer -= 1
        
        # if player is alive, do all the things
        if player.health > 0 and timer > 0:
            # creature movement    ]]]]
            player.status = "safe"
            for c in creatures:
                if c.type == "gobbo":
                    tick_gobbo(c,player,floorplan)
                if c.type == "villager":
                    tick_villy(c,player,floorplan)
                if c.type == "shoppo":
                    tick_shoppo(c,player,floorplan)

            stdscr.addstr(height, 5, "NAMOFERO", curses.color_pair(10))
            stdscr.addstr(height, 20, "TIME LEFT-"+str(timer), curses.color_pair(10))
            draw_map(stdscr, floorplan, tiles)
            
            
            # Draw all creatures
            for c in creatures:
                stdscr.addstr(c.y, c.x, c.tile, curses.color_pair(c.color))
            
            for o in objects:
                stdscr.addstr(o.y, o.x, o.tile, curses.color_pair(o.color))
                
            # Draw player info line
            gobbos = filter(lambda c: c.tile == "&" or c.tile =="!", creatures)
            gobbo_seeing = filter(lambda c: c.tile == "!", gobbos)
            gobbos_near = any(lambda gobbo: distance(gobbo, player) < 3, gobbos)
            
            yellowlert = filter(lambda g: g.target != None, gobbos)
            if len(gobbo_seeing) > 0:
                player_status = "unsafe"
                status_color = 6
                status_symbol = " ! "
            elif len(yellowlert) > 0 or gobbos_near:
                player_status = "danger"
                status_color = 7
                status_symbol = " ? "
            else:
                player_status = "safe"
                status_color = 5
                status_symbol = " ~ "
            

                
            stdscr.addstr(height, 0, status_symbol, curses.color_pair(status_color))
            
            
            status_y = 25
            csy = 0        
            
            
            display_news(stdscr, news, width, height)
            
            stdscr.addstr(0, width + 2, "Inventory", curses.color_pair(9))
            stdscr.addstr(1, width + 1, "===========", curses.color_pair(9))
            
            cur_i = 3
            for o in player.inv:
                stdscr.addstr(cur_i, width + 1, "%s: %s" % (o.tile, o.type), curses.color_pair(o.color))
                cur_i += 1

            stdscr.addstr(height, 40, "health " + ("+" * player.health), curses.color_pair(1))
                
            
        else:
            stdscr.addstr(height / 2, width / 2 - 9, "GAME OVER", curses.color_pair(1))
            stdscr.addstr(height / 2 + 1, width / 2 - 10, "===========", curses.color_pair(1))

        #up to here: always do these things
        inp = stdscr.getch() # "Get character" -- pauses and waits for player to type a key
        keyboard_input(inp, player, floorplan, objects, creatures, stdscr)
        for o in objects:
            if player.x == o.x and player.y == o.y:
                objects.remove(o)
                player.inv.append(o)
                
        # Are we at the end of the level?
        tilenum = floorplan[player.y][player.x]
        if tilenum == 7:# and any(lambda o: o.type == "treasure chest", player.inv):
            current_level += 1
            player.health = 3
            news.append("Next level...")
            creatures, objects, floorplan, timer = change_level(levels[current_level], inv=player.inv)
            width = len(floorplan[1])
            height = len(floorplan)
        
        
            
        stdscr.refresh()
    


curses.wrapper(main)
