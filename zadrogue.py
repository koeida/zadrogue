from creatures import tick_creatures
from display import init_colors, draw_map, display_inv
from roguelib import *
import level
from misc import any


def main(stdscr):
    inp = 0
    current_level = 7

    curses.curs_set(False) # Disable blinking cursor
    init_colors()

    creatures, objects, floorplan, timer = change_level(current_level,coins=0)

    width = len(floorplan[1])
    height = len(floorplan)

    while(inp != 113): # Quit game if player presses "q"
        stdscr.clear()
        player = list(filter(lambda c: c.type == "player", creatures))[0]

        timer = update_timers(creatures, player, timer)

        invisibility_check(player, floorplan)

        # if player is alive, do all the things
        if player.health <= 0 and timer <= 0:
            death_screen(height, stdscr, width)
            break


        # creature movement    ]]]]
        player.status = "safe"
        if player.speedtimer <= 0 or player.speedtimer % 2 == 0:
            tick_creatures(creatures, floorplan, objects, player)

        # Draw player info/visibility alert
        status_color, status_symbol = generate_alert(creatures, player)
        stdscr.addstr(height, 0, status_symbol, curses.color_pair(status_color))
        stdscr.addstr(height, 5, "coins-" + str(player.coins), curses.color_pair(15))
        stdscr.addstr(height, 20, "TIME LEFT-" + str(timer), curses.color_pair(10))
        draw_map(stdscr, floorplan, tiles)

        # Draw all creatures
        for c in creatures:
            stdscr.addstr(c.y, c.x, c.tile, curses.color_pair(c.curcolor))

        for o in objects:
            stdscr.addstr(o.y, o.x, o.tile, curses.color_pair(o.color))



        status_y = 25
        csy = 0

        display_news(stdscr, news, width, height)

        display_inv(stdscr, player.inv, width, True)

        stdscr.addstr(height, 40, "health " + ("+" * player.health), curses.color_pair(1))

        stdscr.refresh()

        inp = stdscr.getch()  # "Get character" -- pauses and waits for player to type a key
        keyboard_input(inp, player, floorplan, objects, creatures, stdscr)

        if current_level == 0 and player.y == 0:
            current_level += 1
            creatures, objects, floorplan, timer = change_level(current_level, player.inv,player.coins)
            width = len(floorplan[1])
            height = len(floorplan)
        for o in objects:
            if player.x == o.x and player.y == o.y and o.pickupable == True:
                if o.buyable == False:
                    objects.remove(o)
                    if o.type == "coin":
                        player.coins +=1
                    else:
                        player.inv.append(o)
                else:
                    if player.coins >= o.cost:
                        prompt_str = "Do you want to buy this " + o.type + "? It costs " + str(o.cost) + " coins."
                        resp = prompt(stdscr, height, prompt_str)
                        if resp == ord("y"):
                            player.inv.append(o)
                            objects.remove(o)
                            player.coins -= o.cost

                    else:
                        prompt_str = "You dont have enough money to buy this " + o.type + "."
                        prompt(stdscr, height, prompt_str)


            # Are we at the end of the level?
            tilenum = floorplan[player.y][player.x]
            if tilenum == 7:# and any(lambda o: o.type == "treasure chest", player.inv):
                current_level += 1
                creatures, objects, floorplan, timer = change_level(current_level, player.inv, player.coins)
                width = len(floorplan[1])
                height = len(floorplan)


def generate_alert(creatures, player):
    gobbos = list(filter(lambda c: c.tile == "&" or c.tile == "!", creatures))
    gobbo_seeing = list(filter(lambda c: c.tile == "!", gobbos))
    gobbos_near = any(lambda gobbo: distance(gobbo, player) < 3, gobbos)
    yellowlert = list(filter(lambda g: g.target != None, gobbos))
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
    return status_color, status_symbol





def death_screen(height, stdscr, width):
    stdscr.clear()
    stdscr.addstr(height / 2, width / 2 - 9, "GAME OVER", curses.color_pair(1))
    stdscr.addstr(height / 2 + 1, width / 2 - 10, "===========", curses.color_pair(1))
    stdscr.refresh()
    inp = stdscr.getch()


def update_timers(creatures, player, timer):
    if player.speedtimer > 0:
        player.speedtimer -= 1
    if player.speedtimer <= 0 or player.speedtimer % 2 == 0:
        timer -= 1
    for c in creatures:
        if c.invisotimer > 0:
            c.invisotimer -= 1
    return timer


def invisibility_check(c, floorplan):
    if c.invisotimer == 0:
        c.curcolor = c.color  # Bug: now curcolor doesn't work
    else:
        # Get the tile number at the creature's x and y coordinate
        tilenum = floorplan[c.y][c.x]
        invisocolor = tiles[tilenum][1]
        # Set curcolor equal to that color
        c.curcolor = invisocolor


curses.wrapper(main)
