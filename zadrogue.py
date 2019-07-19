import curses
from roguelib import *
from random import randint
    
def main(stdscr):
    inp = 0
    floorplan = read_floorplan()

    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    
    width = len(floorplan[1])
    height = len(floorplan)
    
    player = Creature(18, 17, "@", 1, "player") # x, y, image, color
    chest = Object(randint(0, width), randint(1,5),"=", 14, "treasure chest")
    creatures = [player]
    objects = [chest]
    
    for x in range(5):
        creatures.append(Creature(randint(1,width),randint(1,height), "&", 4, "gobbo"))
    for x in range(5):
        objects.append(Object(randint(0, width-1), randint(1,height),"$", 14, "coin"))


    while(inp != 113): # Quit game if player presses "q"
        stdscr.clear()

        draw_map(stdscr, floorplan, tiles)       
        
        # creature movement    ]]]]
        player.status = "safe"
        for c in creatures:
            if c.type == "gobbo":
                move_gobbo(c,player,floorplan)

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
        stdscr.addstr(height, 5, "NAME_OF_HERO", curses.color_pair(8))
        
        status_y = 25
        csy = 0        
        
        output_status(stdscr)
        display_news(stdscr, news)
        stdscr.refresh()

        inp = stdscr.getch() # "Get character" -- pauses and waits for player to type a key
        keyboard_input(inp, player, floorplan)
    


curses.wrapper(main)
