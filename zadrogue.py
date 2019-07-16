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
    
    creatures = [player]
    
    for x in range(5):
        creatures.append(Creature(randint(1,30),randint(1,20), "&", 4, "gobbo"))

    while(inp != 113): # Quit game if player presses "q"
        stdscr.clear()

        draw_map(stdscr, floorplan, tiles)       
        
        # creature movement
        player.status = "safe"
        for c in creatures:
            if c.type == "gobbo":
                move_gobbo(c,player,floorplan)

        # Draw all creatures
        for c in creatures:
            stdscr.addstr(c.y, c.x, c.tile, curses.color_pair(c.color))
            
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
        stdscr.refresh()

        inp = stdscr.getch() # "Get character" -- pauses and waits for player to type a key
        keyboard_input(inp, player, floorplan)
    

curses.wrapper(main)
