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
    turnOnSpot = True

    # enemy
    allowEnemyMovement = True  # freeze enemies for tests?
    allowEnemyAttacking = True
    showEnemyWanderDest = False
    showEnemyWeaponHitCollisionDetectionTargets = False
    showEnemyWeaponAttackLocations = False
    showEnemyDamageNumbers = True

    # gfx
    showBurstOnImpact = True
    showBurstOnImpactDamage = 19  # how much damage to activate Burst
    overwriteColorTime = 0.2

    # gameplay
    maxEnemiesInStateAttacking = 2
    maxEnemiesInStateChase = 3


Config = _Config()
