from collections import namedtuple
from creatures import make_kart, Creature
from objects import town_objects

Level = namedtuple("Level", "m num_gobbos num_villagers num_gold time inhabitants objects name")

shopkeeper1 = Creature(47,3, "v", 17, "shoppo")
shopkeeper1.speek = "Welcome to the Flaming Cauldron, home to some of the greatest potions in the underdark."
shopkeeper2 = Creature(47,9, "v", 17, "shoppo")
shopkeeper2.speek = "Gooday, traveler. What kind of magical clothing do you wish to buy from Devon Malikar's Mystical Garb?"
shopkeeper3 = Creature(2,3, "v", 17, "shoppo")
shopkeeper3.speek = "So, how can we help you here at the Useful Junk Shoppe?"
old_wizardio = Creature(45,19, "R", 1, "wizardio")
old_wizardio.speek = "I hear you are going into the gobblin stronghold. 'Tis a perilous place. You shall need this."


levels = [
    Level(m="floorplan_0.txt", name="The Begining",
          num_gobbos=0, num_villagers=5, num_gold=0,
          time=99999, inhabitants=[old_wizardio], objects=[]),
    Level(m="floorplan.txt", name="Surface Stronghold",
          num_gobbos=5, num_villagers=0, num_gold=5,
          time=150, inhabitants=[], objects=[]),
    Level(m="floorplan2.txt", name="Undercollums",
          num_gobbos=10, num_villagers=0, num_gold=5,
          time=150, inhabitants=[], objects=[]),
    Level(m="floorplan3.txt", name="The Labrynth",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=150, inhabitants=[], objects=[]),
    Level(m="floorplan_4.txt", name="The Aquaducts",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=200, inhabitants=[], objects=[]),
    Level(m="floorplan_5.txt",name="The dwarven village of Brorldown",
          num_gobbos=0, num_villagers=5, num_gold=1,
          time=99999, inhabitants=[shopkeeper1, shopkeeper2, shopkeeper3], objects=town_objects),
    Level(m="floorplan_6.txt", name="Goblo Manor",
          num_gobbos=10, num_villagers=0, num_gold=15,
          time=100, inhabitants=[], objects=[]),
    Level(m="floorplan_7.txt", name="Ghouler Station",
          num_gobbos=10, num_villagers=0, num_gold=10,
          time=100, inhabitants=[make_kart()], objects=[])
]