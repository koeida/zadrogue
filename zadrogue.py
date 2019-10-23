from creatures import *
from display import init_colors, draw_map, prompt, display_inv
from roguelib import *
from collections import namedtuple
from misc import any
from objects import health_potion, teleport_ring

Level = namedtuple("Level", "m num_gobbos num_villagers num_gold time inhabitants objects")

shopkeeper1 = Creature(47,3, "v", 17, "shoppo")

shield = Object(47,2, "0", 11, "shield", True, 3)
town_objects = [shield]
boots = Object(46,2, "L", 15, "boots of Jesus", True, 3)
town_objects.append(boots)
ring = Object(45,2, "o", 15, "ring of teleportation", True, 4, teleport_ring)
town_objects.append(ring)
potion_inv = Object(44,2, "b", 18, "potion of invisibility", True, 4)
town_objects.append(potion_inv)
potion_spe = Object(47,4, "b", 16, "potion of speed", True, 3)
town_objects.append(potion_spe)
caltrops = Object(46,4, "*", 12, "caltrops", True, 3)
town_objects.append(caltrops)
potion_hel = Object(45,4, "b", 1, "health potion", True, 3, health_potion)
town_objects.append(potion_hel)


levels = [
    Level(m="floorplan.txt",
          num_gobbos=5, num_villagers=0, num_gold=5,
          time=150, inhabitants=[], objects=[]),
    Level(m="floorplan2.txt",
          num_gobbos=10, num_villagers=0, num_gold=5,
          time=150, inhabitants=[], objects=[]),
    Level(m="floorplan3.txt",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=200, inhabitants=[], objects=[]),
    Level(m="floorplan_4.txt",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=200, inhabitants=[], objects=[]),
    Level(m="floorplan_5.txt",
          num_gobbos=0, num_villagers=5, num_gold=200, #num_gold=2,
          time=20000, inhabitants=[shopkeeper1], objects=town_objects)
]

def spend_coins(inv, cost):
    removes = []
    for o in inv:
        if o.type == "coin":
            removes.append(o)
            cost -= 1
            if cost == 0:
                break
    for r in removes:
        inv.remove(r)


def main(stdscr):
    inp = 0
    current_level = 4
    
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
            
            display_inv(stdscr, player.inv, width, True)

            stdscr.addstr(height, 40, "health " + ("+" * player.health), curses.color_pair(1))
                
            
        else:
            stdscr.addstr(height / 2, width / 2 - 9, "GAME OVER", curses.color_pair(1))
            stdscr.addstr(height / 2 + 1, width / 2 - 10, "===========", curses.color_pair(1))

        #up to here: always do these things
        inp = stdscr.getch() # "Get character" -- pauses and waits for player to type a key
        keyboard_input(inp, player, floorplan, objects, creatures, stdscr)
        for o in objects:
            if player.x == o.x and player.y == o.y:
                if o.buyable == False:
                    objects.remove(o)
                    player.inv.append(o)
                else:
                    playercoinz = filter(lambda i: i.type == "coin", player.inv)
                    if len(playercoinz) >= o.cost:
                        prompt_str = "Do you want to buy this " + o.type + "? It costs " + str(o.cost) + " coins."
                        resp = prompt(stdscr, height, prompt_str)
                        if resp == ord("y"):
                            player.inv.append(o)
                            objects.remove(o)
                            spend_coins(player.inv, o.cost)

                    else:
                        prompt_str = "You dont have enough money to buy this " + o.type + "."
                        prompt(stdscr, height, prompt_str)

                
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
