from misc import anyslice, between, any
from rnews import *

tiles = { 0: (".", 9, True),
          1: ("#", 2,False),
          2: ("_", 2,False),
          3: ("\"", 3,True),
          4: ("/", 2,True),
          5: ("]", 10,True),
          6: ("]", 11,True),
          7: ("]", 12, True),
          8: ("~",16,True)}

def offmap(x, y, floorplan):
    width = len(floorplan[1])
    height = len(floorplan)

    if x >= width or x < 0:
        return True
    # 4) Is y off the map? If so, return False
    if y >= height or y < 0:
        return True

    return False


def its_opaque(tile_num, tiles):
    cur_tile_info = tiles[tile_num]
    return not cur_tile_info[2]

def wall_between(i1,i2,row):
    tiles_between = anyslice(i1,i2,row)
    return False if 1 in tiles_between else True

def no_wall_between(row, start, end, m, debug=False):
    inb = m[row][start:end + 1]

    return not any(lambda t: its_opaque(t, tiles), inb)
