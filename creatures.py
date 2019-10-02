from random import randint, choice
from gamemap import wall_between, its_opaque, tiles
from misc import distance, rotate_list
from roguelib import offmap, news


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

    if is_visible_old(gobbo, player, m):
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


def is_visible_old(c, t, floorplan):
    """Is t visible to c?"""
    global status

    if c.y == t.y:
        row = floorplan[c.y]

        # Look to the left
        for cur_x in range(c.x, t.x - 1, -1):
            if cur_x == t.x:
                return True
            cur_tile_num = row[cur_x]
            if its_opaque(cur_tile_num, tiles):
                break

        # Look to the right
        for cur_x in range(c.x, t.x + 1):
            if cur_x == t.x:
                return True
            cur_tile_num = row[cur_x]
            if its_opaque(cur_tile_num, tiles):
                break
    elif c.x == t.x:
        columns = rotate_list(floorplan)

        # FIX THIS
        try:
            column = list(columns[c.x])
        except:
            return
        column.reverse()

        # Look up
        for cur_y in range(c.y, t.y - 1, -1):
            cur_tile_num = column[cur_y]
            if its_opaque(cur_tile_num, tiles):
                break
            if cur_y == t.y:
                return True

        # look down
        for cur_y in range(c.y, t.y + 1):
            if cur_y == t.y:
                return True
            cur_tile_num = column[cur_y]
            if its_opaque(cur_tile_num, tiles):
                break
    else:
        return False


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
foo = Creature(2, 0, None, None, None)
bar = Creature(0, 0, None, None, None)
assert(is_visible(foo,bar,floorplan_t))
foo = Creature(0, 2, None, None, None)
bar = Creature(0, 2, None, None, None)
assert(is_visible(foo,bar,floorplan_t))
foo = Creature(0, 1, None, None, None)
bar = Creature(2, 1, None, None, None)
assert(not is_visible(foo,bar,floorplan_t))
foo = Creature(2, 1, None, None, None)
bar = Creature(0, 1, None, None, None)
assert(not is_visible(foo,bar,floorplan_t))