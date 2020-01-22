import curses

def display_inv(screen, inv, width, show_numbers=False):
    screen.addstr(0, width + 2, "Inventory", curses.color_pair(9))
    screen.addstr(1, width + 1, "===========", curses.color_pair(9))

    cur_i = 3
    for o in inv:
        if show_numbers:
            screen.addstr(cur_i, width + 1, "%d) %s: %s" % (cur_i - 2,o.tile, o.type), curses.color_pair(o.color))
        else:
            screen.addstr(cur_i, width + 1, "%s: %s" % (o.tile, o.type), curses.color_pair(o.color))
        cur_i += 1

def draw_map(screen, m, tiles, x=0, y=0):
    for cy in range(len(m)):
        for cx in range(len(m[cy])):
            tile_id = m[cy][cx]
            img, color, opacity = tiles[tile_id]

            screen.addstr(y + cy, x + cx, img, curses.color_pair(color))


def display_news(screen, news, width, height):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    MAP_HEIGHT = height
    MAP_WIDTH = width
    for n in top_news:
        screen.addstr(MAP_HEIGHT + cn + 1, 0, " " * MAP_WIDTH, curses.color_pair(10 + cn)),
        screen.addstr(MAP_HEIGHT + cn + 1, 0, n, curses.color_pair(10 + cn))
        cn += 1

def prompt(screen, height, message):
    middle_height = int(height / 2) - 1
    mlength = len(message) + 5
    screen.addstr(middle_height,     5,               "*" * mlength)
    screen.addstr(middle_height + 1, 5,               "*" + message)
    screen.addstr(middle_height + 1, mlength + 4,"*")
    screen.addstr(middle_height + 2, 5,               "*" * mlength)
    return screen.getch()


def init_rgb(n, r, g, b):
    rpercent = r / 255.0
    gpercent = g / 255.0
    bpercent = b / 255.0
    r = int(1000 * rpercent)
    g = int(1000 * gpercent)
    b = int(1000 * bpercent)
    curses.init_color(n, r, g, b)

def init_colors():
    curses.init_color(1, 800, 0,0)
    curses.init_color(2, 500, 300, 200)
    curses.init_color(3, 0, 1000, 0)
    curses.init_color(4, 100, 400, 0)

    # Shades of grey for news
    curses.init_color(10, 800, 800, 800)
    curses.init_color(11, 600, 600, 600)
    curses.init_color(12, 400, 400, 400)
    curses.init_color(13, 300, 300, 300)

    curses.init_color(5, 0, 1000, 0)
    curses.init_color(6, 0, 500, 0)
    curses.init_color(7, 1000, 600, 0)
    curses.init_color(8, 1000, 1000, 1000)
    curses.init_color(9, 1000, 1000, 0)

    curses.init_color(14, 301, 376, 929)
    curses.init_color(15, 603, 454, 243)

    #init_rgb(16, 135, 42, 193)

    curses.init_pair(1, 1, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK)  # walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK)  # walls, brown on black
    curses.init_pair(4, 4, curses.COLOR_BLACK)

    curses.init_pair(5, 6, 5)  # SAFE LIGHT
    curses.init_pair(6, 9,1)  # DANGER LIGHT
    curses.init_pair(7, 7, 9)  # DANGER LIGHT
    curses.init_pair(9, 8, curses.COLOR_BLACK)

    # News fadeout
    curses.init_pair(10, 10, curses.COLOR_BLACK)
    curses.init_pair(11, 11, curses.COLOR_BLACK)
    curses.init_pair(12, 12, curses.COLOR_BLACK)
    curses.init_pair(13, 13, curses.COLOR_BLACK)
    curses.init_pair(14, 13, curses.COLOR_BLACK)
    curses.init_pair(15, 9, curses.COLOR_BLACK)

    curses.init_pair(16, 14, curses.COLOR_BLACK)

    curses.init_pair(17, 15, curses.COLOR_BLACK)

    #curses.init_pair(18, 16, curses.COLOR_BLACK)