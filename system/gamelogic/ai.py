import esper
import logging

from ai.brain import Brain
from entities.enemy.state_attack import StateAttack
from entities.enemy.state_attackwindup import StateAttackWindup
from entities.enemy.state_chase import StateChase
from entities.enemy.state_dying import StateDying
from entities.enemy.state_idle import StateIdle
from entities.enemy.state_spawn import StateSpawn
from entities.enemy.state_wander import StateWander
from entities.enemy.state_stun import StateStun

logger = logging.getLogger(__name__)


class Ai():
    def __init__(self, player, name, esperData, director, world, viewport):
        self.enemyMovement :bool = True
        self.player = player #
        self.esperData = esperData
        self.director = director #
        self.world = world #
        self.viewport = viewport #
        self.offensiveAttackEntity = None

        self.name :str = 'Bot' + name
        self.initAi()


    def initAi(self):
        self.brain :Brain = Brain(self.esperData)

        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateChase)
        self.brain.register(StateWander)
        self.brain.register(StateStun)
        self.brain.register(StateDying)
        self.brain.register(StateAttackWindup)
        self.brain.push("idle")


    def advance(self, deltaTime :float):
        self.brain.update(deltaTime)


    def __repr__(self):
        return self.name
