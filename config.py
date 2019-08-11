

class Config:
    fps = 100

    rows = 25
    columns = 80

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

    moveBorderRight = 76
    moveBorderLeft = 4

    playerSpawnPoint = {
        'x': 24,
        'y': 13,
    }

    devMode = False

    moveDiagonal = False

    announceDamage = 350
    maxParticles = 128
    movementKeysPerSec = 20.0
    