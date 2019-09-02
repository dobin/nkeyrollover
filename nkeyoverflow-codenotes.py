# Stun

On hit:
* Move to state "Stunned"
  * Different animation in stunned
  ? should not be attackable for some time duration?
    * no chain stun, should recover after a bit?
  * dont pop, only push (interrupt current state)?


# Character Move Sequence

* Pushback
* Charge forward

def CharacterMoveSequence(object):
    def __init__(self):
        self.movArr = []
        self.movTimeArr = []
        self.characterAnimation = None
        self.init()

    def exampleInitJump(self):
        self.moveArr = [
            { x: 0, y: -1},
            { x: 1, y: 0},
            { x: 0, y: 1},
        ]
        self.movTimeArr = [ 0.0, 0.2, 0.2 ]

    def init(self):
        self.currentIdx = 0

    def increase(self):
        self.currentIdx += 1

    def getMoveArr(self):
        return self.moveArr[ self.currentIdx ]

    def getTime(self):
        return self.movTimeArr[ self.currentIdx ]

    def isEnd(self):
        if self.currentIdx = len(self.movArr):
            return True
        else:
            return False


def doCharacterMoveSequence(characterMoveSquence):
    character.pushState(MoveSquence, characterMoveSequence)


def MoveSquenceState(object):
    def __init__(self):
        self.characterMoveSequence = None

    def on_enter(self, characterMoveSequence):
        self.characterMoveSequence = characterMoveSequence
        self.characterMoveSequence.init()
        self.setTimer(self.characterMoveSequence.getTime())
        self.previousAnimationState = me.saveCurrentCharacterAnimationState()
        me.setCharacterAnimation(characterMoveSquence.characterAnimation)

    def process(self):
        if self.timeIsUp():
            me.move( self.characterMoveSequence.getMoveArr() )
            if self.characterMoveSequence.isEnd():
                me.restoreCharacterAnimationState(self.previousAnimationState)
                self.pop()
            else:
                self.characterMoveSequence.increase()
                self.setTimer( self.characterMoveSequence.getTime() )


# Map Sections

MapSection:
- start_x   // Upon reaching this point, spawn enemies below
- max_x     // Dont let player move behind this point
            // until all enemies are killed
- enemies[] :SectionEnemyData
  - startpos
  - type
  - wait_time

- How to spawn enemies?
  - all at the same time, but out of view, and deactivated
    till close enough?
  - let them spawn when player moves at locations?

## Director

def loadMapSections(self):
    file = ...
    mapSection = MapSection(fileData)
    self.mapSections.append(mapSection)
    self.currentMaxSectionIdx = 0
    self.currentMapSection = None

def spawnEnemy(sectionEnemy):
    enemy = self.enemiesDead.pop()
    enemy.setStatus(spawn, sectionEnemyData)
    self.enemiesAlive.append(enemy)

def setNewMapSection(self, mapSection):
    """Spawn all enemies of a new map section"""
    self.currentMapSection = mapSection
    for sectionEnemy in self.currentMapSection.enemies:
        self.spawnEnemy(sectionEnemy)

def checkMapSection(self):
    """Handle transition to next map section"""
    enemiesAlive = len(self.enemiesAlive)
    if enemiesAlive == 0:
        self.currentMapSectionIdx += 1
        self.setNewMapSection(self.mapSections[self.currentMapSectionIdx])
        self.viewport.setNewMapSection(self.currentMapSection)
        self.viewport.drawMessage("Section cleared in {} seconds")

## Viewport

def ViewportState(Enum):
    fight: 0
    scroll: 1

class Viewport(object):
    def setNewMapSection(self, mapSection):
        self.mapSection = mapSection

        if self.player.x < mapSection.start_x:
            self.moveScreenTillPlayer()

    def moveScreenTillPlayer(self):
        if not self.screenMoveTimer.timeIsUp():
            return

        if self.x != self.player.x - 2:
            self.screenMoveTimer.setTimer(1)
            self.screenMoveTimer.reset()
            self.x += 1

    def moveScreen(self, x):
        newX = self.x += x

        # make sure screen stays in bounds of current map section
        # stop moving it when player is close to the edge
        if newX < self.mapsection.start_x + 2:
            return
        if newX > self.mapSection.max_x - 2:
            return

        self.x = newX


## Player

def move(self):
    # Dont let player move left before current map section
    if MOVE_LEFT:
        if player.x <= self.director.mapSection.start_x:
            return False
    # Dont let player move right beyond current map section
    if MOVE_RIGHT:
        if player.x >= self.director.mapSection.max_x:
            return False


## Enemy

StateSpawn(State):
    on_enter(self, waitTime):
        # need timer, or can just use position as "timer"?
        self.setTimer(waitTime)

    process(self):
        if self.timeIsUp():
            changeToStatus(wander)

        # if the player advances to the right, dont present
        # him enemies who just sit around
        me = self.brain.owner
        if me.distanceToPlayer(5):
            changeToStatus(chase)
