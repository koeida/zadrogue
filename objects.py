from random import randint

def noeffect(player, cs, m, os):
    pass

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
    player.phaseotimer = 10
    player.tile = "M"
    player.curcolor = 9

def jesus_bootz(player, cs, m, os):
    player.jesustimer = 20

def speed_potion(player, cs, m, os):
    player.speedtimer = 15

def shield_effect(player, cs, m, os):
    pass
town_objects = []
shield = Object(2,2, "0", 11, "shield", True, 3, shield_effect)
boots = Object(47,8, "L", 15, "boots of Jesus", True, 3, jesus_bootz)
town_objects.append(boots)
ring = Object(47,9, "o", 15, "ring of teleportation", True, 4, teleport_ring)
town_objects.append(ring)
potion_inv = Object(47,2, "b", 18, "potion of invisibility", True, 4, inviso_potion)
town_objects.append(potion_inv)
potion_spe = Object(47,3, "b", 16, "potion of speed", True, 3, speed_potion)
town_objects.append(potion_spe)
caltrops = Object(2,3, "*", 12, "caltrops", True, 3, caltropz)
town_objects.append(caltrops)
potion_hel = Object(47,4, "b", 1, "health potion", True, 3, health_potion)
town_objects.append(potion_hel)
phasecloak = Object(47,10, "M", 9, "toga of ghostlyness", True, 5, ghost_toga)
town_objects.append(phasecloak)
town_objects.append(shield)



