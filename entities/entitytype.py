from enum import Enum

class EntityType(Enum): 
    player = 0
    enemy = 1

    takedamage = 2
    weapon = 3
    
    world = 4