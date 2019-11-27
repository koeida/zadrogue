from random import randint


def noeffect(player, cs, m, os):
    pass

def health_potion(player, cs, m, os):
    player.health += 2

def teleport_ring(player, cs, m, os):
    width = len(m[1])
    height = len(m)
    player.x = randint(0, width)
    player.y = randint(0, height)

def inviso_potion(player, cs, m, os):
    player.invisotimer = 10

def caltropz(player, cs, m, os):
    caltrop = Object(player.x, player.y, "*", 12, "caltrops", False, 3, pickupable=False)
    os.append(caltrop)

def ghost_toga(player, cs, m, os):
    #player.phaseotimer = 10
    player.tile = "M"
    player.color = 9




class Object:
    def __init__(self, x, y, tile, color, type, buyable=False, cost=0, effect=noeffect, pickupable=True):
        self.x = x
        self.y = y
        self.color = color
        self.tile = tile
        self.type = type
        self.buyable = buyable
        self.cost = cost
        self.effect = effect
        self.pickupable = pickupable