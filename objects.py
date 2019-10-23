from random import randint


def noeffect(player, cs, m):
    pass

def health_potion(player, cs, m):
    player.health += 2

def teleport_ring(player, cs, m):
    width = len(m[1])
    height = len(m)
    player.x = randint(0, width)
    player.y = randint(0, height)

def inviso_potion(player, cs, m):
    player.invisotimer = 15



class Object:
    def __init__(self, x, y, tile, color, type, buyable=False, cost=0, effect=noeffect):
        self.x = x
        self.y = y
        self.color = color
        self.tile = tile
        self.type = type
        self.buyable = buyable
        self.cost = cost
        self.effect = effect