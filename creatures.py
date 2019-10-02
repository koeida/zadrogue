from random import randint, choice
from gamemap import its_opaque, tiles, no_wall_between, offmap
from misc import distance, rotate_list, between, anyslice
from roguelib import *


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


def get_gobbo_target(gobbo):
    if gobbo.target != None:
        tx = gobbo.target[0]
        ty = gobbo.target[1]
    else:
        tx, ty = wander(gobbo)
    return (tx, ty)


def tick_shoppo(c, player, floorplan):
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
    villy_speek = ["Gooday stranger, welcome to our modest little town of Brorldown.",
                   "I see you are loaded with stolen loot! Might I sugest you check out our magic item shops?",
                   "Oh its you, the notorious Namafero, raider of goblins! It is an honor to have you in our town...",
                   "'Sup!"]

    if distance(c, player) < 2:
        news.append("Villager sez: " + choice(villy_speek))


def wander(c):
    tx = c.x + randint(-1, 1)
    ty = c.y + randint(-1, 1)
    return tx, ty


def bump_steps(c, oldx, oldy, m):
    tilenum = m[c.y][c.x]
    if (m[oldy][oldx] not in [5, 6]) and tilenum == 6:
        return True
    if (m[oldy][oldx] == 6) and tilenum not in [5, 6]:
        return True
    return False


def gobbo_invalid_move(gobbo, m, oldx, oldy):
    if offmap(gobbo.x, gobbo.y, m):
        return True

    tilenum = m[gobbo.y][gobbo.x]
    if not wakabal(tilenum, gobbo.x, gobbo.y, m, gobbo):
        return True

    if bump_steps(gobbo, oldx, oldy, m):
        return True

    return False


def gobbo_attack(gobbo, player, m):
    # Make gobbo stand in place for a few turns after it hits you
    if gobbo.did_attack == True:
        if randint(1, 4) == 1:
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

    if is_visible(gobbo, player, m):
        gobbo.tile = "!"
        gobbo.target = (player.x, player.y)
    else:
        gobbo.tile = "&"


def tick_gobbo(gobbo, player, m):
    move_gobbo(gobbo, player, m)
    gobbo_attack(gobbo, player, m)
    gobbo_vision(gobbo, player, m)


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

    xmod, ymod = move_to_target(tx, ty, gobbo.x, gobbo.y)
    gobbo.x += xmod
    gobbo.y += ymod
    gobbo.target_steps += 1

    if gobbo_invalid_move(gobbo, m, oldx, oldy):
        gobbo.y = oldy
        gobbo.x = oldx


def do_doors(x, y, m, a, b):
    """Look at tiles around x and y on map m: if any are of type a, change them to type b"""
    if m[y - 1][x] == a:
        m[y - 1][x] = b

    if m[y + 1][x] == a:
        m[y + 1][x] = b

    if m[y][x + 1] == a:
        m[y][x + 1] = b

    if m[y][x - 1] == a:
        m[y][x - 1] = b


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
        if randint(1, 2) == 1:
            xmod = 0
        else:
            ymod = 0

    return (xmod, ymod)


def is_visible(c, t, m):

    column_visible = False
    if c.x == t.x:
        sy = c.y if c.y < t.y else t.y
        ey = c.y if c.y > t.y else t.y
        vtiles = []
        for y in range(sy, ey + 1):
            vtiles.append(m[y][c.x])

        column_visible = 1 not in vtiles and 2 not in vtiles
    row_visibile = c.y == t.y and no_wall_between(t.y, t.x, c.x, m)
    return column_visible or row_visibile
