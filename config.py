

class Config:
    fps = 60

    rows = 25
    columns = 80

    topborder = 8

    areaDrawable = {
        'minx': 1,
        'miny': 0,
        'maxy': 24,
        'maxx': 79
    }

    areaMoveable = {
        'minx': 1,
        'miny': 8,
        'maxy': 24,
        'maxx': 79
    }

    moveBorderRight = 70
    moveBorderLeft = 8

    playerSpawnPoint = {
        'x': 24,
        'y': 13,
    }

    devMode = False
    enemyMovement = True # freeze enemies for tests?
    showEnemyWanderDest = True

    moveDiagonal = False # instead of up/down

    announceDamage = 350 # min amount of damage done
    maxParticles = 128
    movementKeysPerSec = 20.0
    
    playerAttacksCd = 0.2

    version = str(0.02)