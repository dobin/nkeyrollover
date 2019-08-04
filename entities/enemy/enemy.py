import random
import logging

from sprite.charactersprite import CharacterSprite
from entities.player.player import Player
from entities.direction import Direction
from entities.action import Action
from entities.character import Character
from .enemyweapon import EnemyWeapon
from config import Config
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.entitytype import EntityType
from ai.brain import Brain
import entities.enemy.aifsm as aifsm

logger = logging.getLogger(__name__)


class Enemy(Character):
    def __init__(self, win, parent, spawnBoundaries, world):
        Character.__init__(self, win, parent, spawnBoundaries, world, EntityType.enemy)
        self.player = world.getPlayer()
        self.sprite = CharacterSprite(parentEntity=self)
        self.lastInputTimer = Timer(1.0)
        self.characterWeapon = EnemyWeapon(win=win, parentCharacter=self)

        self.initAi()
        self.init()


    def init(self):
        self.x = random.randint(self.spawnBoundaries['min_x'], self.spawnBoundaries['max_x'])
        self.y = random.randint(self.spawnBoundaries['min_y'], self.spawnBoundaries['max_y'])
        self.direction = Direction.left
        self.lastInputTimer.reset()


    def initAi(self): 
        self.stateData = {
            'spawn': {
                'state_time': 1.0,
            },
            'wander': {
                'state_time': 5,
            },
            'chase': {
                'state_time': 5,
            }, 
            'attack': {
                'state_time': 2.0,
            },
            'dying': {
                'state_time': 2.0,
            },
        }

        self.brain = Brain(self)

        self.brain.register(aifsm.Idle)
        self.brain.register(aifsm.Spawn)
        self.brain.register(aifsm.Attack)
        self.brain.register(aifsm.Chase)
        self.brain.register(aifsm.Wander)
        self.brain.register(aifsm.Dying)
        self.brain.push("spawn")
        
        self.attackTimer = Timer(0.5, instant=False) # windup and cooldown
        self.wanderTimer = Timer(0.5, instant=True)
        self.chaseTimer = Timer(0.5, instant=True)


    ### AI

    def sSpawnInit(self): 
        self.sprite.initSprite(Action.standing, self.direction, None)
        self.setActive(True)
    
    
    def sAttackInit(self):
        self.attackTimer.init()
        self.sprite.initSprite(Action.hitting, self.direction, None)


    def sAttack(self):
    	if self.attackTimer.timeIsUp(): 
            logger.warn("I'm attacking!")
            self.attackTimer.reset()
            self.characterWeapon.doHit()


    def sWanderInit(self):
        self.wanderTimer.init()
        self.sprite.initSprite(Action.walking, self.direction, None)

    def sWander(self): 
        if self.wanderTimer.timeIsUp(): 
            logger.debug("I'm moving / wander!")
            self.wanderTimer.reset()
        
        self.getInputWander()


    def sChaseInit(self):
        self.chaseTimer.init()
        self.sprite.initSprite(Action.walking, self.direction, None)

    def sChase(self): 
        if self.chaseTimer.timeIsUp(): 
            logger.debug("I'm moving / chasing!")
            self.chaseTimer.reset()
        
        self.getInputChase()


    def sDyingInit(self): 
        if random.choice([True, False]): 
            animationIndex = 2
            logger.info("Death animation deluxe")
            self.world.makeExplode(self.sprite, self.direction, None)
            self.sprite.initSprite(Action.dying, self.direction, animationIndex)
            self.setActive(False)
        else: 
            animationIndex = random.randint(0, 1)
            self.sprite.initSprite(Action.dying, self.direction, animationIndex)


    def sDying(self): 
        pass


    # Game Mechanics
    def gmKill(self): 
        self.brain.pop()
        self.brain.push("dying")

    def gmRessurectMe(self): 
        if self.characterStatus.isAlive():
            logging.warn("Trying to ressurect enemy which is still alive")
            return

        logger.info("E New enemy at: " + str(self.x) + " / " + str(self.y))
        self.init()
        self.characterStatus.init()

        # if death animation was deluxe, there is no frame in the sprite
        # upon spawning, and an exception is thrown
        # change following two when fixed TODO
        self.sprite.initSprite(Action.standing, self.direction, None)
        self.setActive(True)

        self.brain.pop()
        self.brain.push('spawn')
        

    def gmHandleHit(self, damage):
        self.characterStatus.getHit(damage)
        self.setColorFor( 1.0 - 1.0/damage , EntityType.takedamage)
        if not self.characterStatus.isAlive():
            self.brain.pop()
            self.brain.push('dying')


    def canReachPlayer(self): 
        return Utility.pointInSprite(self.getLocation(), self.player.sprite)


    def isPlayerClose(self):
        distance = Utility.distance(self.player.getLocation(), self.getLocation())
        if distance['sum'] < 5:
            return True
        else: 
            return False


    ### /AI

    def getInputChase(self):
        # manage speed
        if not self.lastInputTimer.timeIsUp():
            return
        self.lastInputTimer.reset()

        # make run-animation 
        self.sprite.advanceStep()

        playerLocation = self.player.getLocation()

        if playerLocation['x'] > self.x:
            if self.x < Config.columns - self.sprite.width - 1:
                self.x += 1
                self.direction = Direction.right
        else: 
            if self.x > 1:
                self.x -= 1
                self.direction = Direction.left

        if playerLocation['y'] > self.y:
            if self.y < Config.rows - self.sprite.height - 1:
                self.y += 1
        else: 
            if self.y > 2:
                self.y -= 1


    def getInputWander(self):
        # manage speed
        if not self.lastInputTimer.timeIsUp():
            return
        self.lastInputTimer.reset()

        # make run-animation 
        self.sprite.advanceStep()

        playerLocation = self.player.getLocation()

        if playerLocation['y'] > self.y:
            # newdest is higher
            playerLocation['y'] -= 6
            
            if playerLocation['x'] > self.x:
                playerLocation['x'] += 9
            else:
                playerLocation['x'] -= 9

        else: 
            # newdest is lower
            playerLocation['y'] += 6
            
            if playerLocation['x'] > self.x:
                playerLocation['x'] += 9
            else:
                playerLocation['x'] -= 9


        if playerLocation['x'] > self.x:
            if self.x < Config.columns - self.sprite.width - 1:
                self.x += 1
                self.direction = Direction.right
        else: 
            if self.x > 1:
                self.x -= 1
                self.direction = Direction.left

        if playerLocation['y'] > self.y:
            if self.y < Config.rows - self.sprite.height - 1:
                self.y += 1
        else: 
            if self.y > 2:
                self.y -= 1


    def advance(self, deltaTime): 
        super(Enemy, self).advance(deltaTime)
        self.lastInputTimer.advance(deltaTime)

        ### AI
        self.attackTimer.advance(deltaTime)
        self.wanderTimer.advance(deltaTime)
        self.chaseTimer.advance(deltaTime)
        self.brain.update(deltaTime)
        
    def __repr__(self):
        return 'E0x01'