from random import randint, choice
from gamemap import its_opaque, tiles, no_wall_between, offmap
from misc import ordered
from roguelib import *
from objects import town_objects


class Creature:
    def __init__(self, x, y, tile, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.curcolor = color
        self.tile = tile
        self.target = None
        self.type = type
        self.target_steps = 0
        self.inv = []
        self.health = 3
        self.did_attack = False
        self.is_stuck = False
        self.distracted = 0
        self.has_talked = False
        self.invisotimer = 0
        self.coins = 0
        self.caltroppotimer = 0
        self.phaseotimer = 0
        self.jesustimer = 0
        self.speedtimer = 0



def get_gobbo_target(gobbo):
    if gobbo.target != None:
        tx = gobbo.target[0]
        ty = gobbo.target[1]
    else:
        tx, ty = wander(gobbo)
    return (tx, ty)

def make_kart():
    kart = Creature(23,3,"8",9,"kart")
    kart.xv = 0
    kart.yv = 1
    return kart

def check_around(x, y, m, a):
    count = 0
    if m[y - 1][x] == a:
        count += 1

    if m[y + 1][x] == a:
        count += 1

    if m[y][x + 1] == a:
        count += 1

    if m[y][x - 1] == a:
        count += 1

    return count

#def get_new_v(kart,gamemap):

def tick_kart(kart, gamemap):
    # Hold onto old x and y
    kartoldx = kart.x
    kartoldy = kart.y

    kart.x += kart.xv
    kart.y += kart.yv

    if gamemap[kart.y][kart.x] != "a":
        kart.x = kartoldx
        kart.y = kartoldy
        while kart.x == kartoldx and kart.y == kartoldy:
            kart.xv = randint(-1,1)
            kart.yv = randint(-1,1)
            kart.x += kart.xv
            kart.y += kart.yv
            if gamemap[kart.y][kart.x] != "a":
                kart.x = kartoldx
                kart.y = kartoldy


def tick_shoppo(c, player, floorplan, objects):
    oldx = c.x
    oldy = c.y
    tx, ty = wander(c)
    xmod, ymod = move_to_target(tx, ty, c.x, c.y)
    c.x += xmod
    c.y += ymod
    villager_sez(c, player)

    if gobbo_invalid_move(c, floorplan, oldx, oldy, objects):
        c.y = oldy
        c.x = oldx


def tick_villy(c, player, floorplan, objects):
    oldx = c.x
    oldy = c.y
    tx, ty = wander(c)
    xmod, ymod = move_to_target(tx, ty, c.x, c.y)
    c.x += xmod
    c.y += ymod
    villager_sez(c, player)

    if gobbo_invalid_move(c, floorplan, oldx, oldy, objects):
        c.y = oldy
        c.x = oldx


def villager_sez(c, player):

    if distance(c, player) < 2 and c.has_talked == False:
        news.append("Villager sez: " + c.speek)
        if c.type == "wizardio":
            player.inv.append(choice(town_objects))
        c.has_talked = True

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


def gobbo_invalid_move(gobbo, m, oldx, oldy, objects):
    if offmap(gobbo.x, gobbo.y, m):
        return True

    tilenum = m[gobbo.y][gobbo.x]
    if not wakabal(tilenum, gobbo.x, gobbo.y, m, gobbo, objects):
        return True

    if bump_steps(gobbo, oldx, oldy, m):
        return True

    return False


def player_has_shield(player):
    shieldrnot = filter(lambda o: o.type == "shield", player.inv)
    if shieldrnot != []:
        return True
    else:
        return False


def gobbo_attack(gobbo, player, m):
    # Make gobbo stand in place for a few turns after it hits you
    if gobbo.did_attack == True:
        if randint(1, 4) == 1:
            gobbo.did_attack = False
        return

    if distance(gobbo, player) <= 1:
        if not player_has_shield(player):
            player.health -= 1
            news.append("Oof! You got attacked!")
            gobbo.did_attack = True
        else:
            drop_first(lambda o: o.type == "shield", player.inv)


def gobbo_vision(gobbo, player, m):
    if gobbo.distracted > 0:
        gobbo.distracted -= 1
        return

    if is_visible(gobbo, player, m) and player.invisotimer <= 0:
        gobbo.tile = "!"
        gobbo.target = (player.x, player.y)
    else:
        gobbo.tile = "&"


def tick_gobbo(gobbo, player, m, objects):
    move_gobbo(gobbo, player, m, objects)
    gobbo_attack(gobbo, player, m)
    gobbo_vision(gobbo, player, m)


def move_gobbo(gobbo, player, m, objects):
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

    if gobbo_invalid_move(gobbo, m, oldx, oldy, objects):
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


def wakabal(tilenum, x, y, floorplan, critter, objects):
    # Is critter stuck? If so, make them unstuck and return false ("not wakabal")
    if critter.is_stuck:
        critter.is_stuck = False
        return False
    if tilenum == 8 and critter.jesustimer <= 0:
        critter.is_stuck = True
    else:
        critter.jesustimer -= 1

    if critter.caltroppotimer >= 0:
        critter.caltroppotimer -= 1
        return False

    if critter.phaseotimer > 0:
        critter.phaseotimer -=1
        if critter.phaseotimer == 0:
            critter.tile = "@"
            critter.curcolor = critter.color
        return True



    caltrops = filter(lambda o: o.type == "caltrops", objects)
    for cal in caltrops:
        if critter.x == cal.x and critter.y == cal.y:
            if critter.type != "player":
                critter.caltroppotimer = 8

    t = tiles[tilenum]
    t_icon, t_color, t_walkable = t
    if critter.type == "shoppo" and tilenum == 4:
        return False
    return t_walkable





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
    def is_visible_(m, n1, n2, f):
        open_tiles = filter(lambda tt: tiles[tt][2], tiles)
        visible = lambda l: len(set(l) - set(open_tiles)) == 0

        start, end = ordered(n1, n2)
        tiles_between = [f(n,m) for n in range(start, end + 1)]
        return visible(tiles_between)

    if c.x == t.x:
        return is_visible_(m, c.y, t.y, lambda n,m: m[n][c.x])
    elif c.y == t.y:
        return is_visible_(m, c.x, t.x, lambda n,m: m[c.y][n])
    else:
        return False
