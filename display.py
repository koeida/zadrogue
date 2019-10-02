import curses

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


def init_colors():
    curses.init_color(2, 600, 400, 255)
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

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK)  # walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK)  # walls, brown on black
    curses.init_pair(4, 4, curses.COLOR_BLACK)

    curses.init_pair(5, 6, 5)  # SAFE LIGHT
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_RED)  # DANGER LIGHT
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