

class EnemyCell(object):
    """Information about when to spawn which enemy in the map. 
    These enemy definitions belong to the map. 
    It will spawn an enemy when sent with MessageType.SpawnEnemy
    """
    def __init__(self, id, enemyType, spawnTime, spawnX, spawnLocation, spawnDirection):
        self.id = id
        self.enemyType = enemyType
        self.spawnTime = spawnTime
        self.spawnX = spawnX

        self.spawnDirection = spawnDirection  # spawn left/right of current viewport
        self.spawnLocation = spawnLocation  # spawn at this position


    def __repr__(self):
        return "{} {} @{} @{} @{}".format(
            self.id,
            self.enemyType,
            self.spawnTime,
            self.spawnX,
            self.spawnLocation)
