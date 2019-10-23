class _Config:
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

    moveBorderRight = 60
    moveBorderLeft = 8

    # system config
    devMode = False
    playground = False
    maxParticles = 512
    version = str(0.1)

    # some z orders
    zMax = 25
    zActionTexture = 26
    zSkill = 27

    # player config
    xDoubleStep = True
    announceDamage = 350  # min amount of damage done
    movementKeysPerSec = 20.0
    playerAttacksCd = 0.2  # player attack cooldown

    # enemy config
    enemyMovement = False  # freeze enemies for tests?
    enemyAttacking = True
    showEnemyWanderDest = False
    showEnemyHitbox = False
    showAttackDestinations = False
    enemiesInStateAttacking = 2
    enemiesInStateChase = 3

    showEnemyDamageNumbers = True
    showBurstOnImpact = True
    showBurstOnImpactDamage = 19  # how much damage to activate Burst


Config = _Config()
