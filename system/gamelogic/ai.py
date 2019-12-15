import logging

from stackfsm.brain import Brain
from ai.stickfigure.state_attack import StateAttack
from ai.cow.state_attack import StateAttack as CowStateAttack
from ai.stickfigure.state_attackwindup import StateAttackWindup
from ai.stickfigure.state_chase import StateChase
from ai.dragon.state_chase import DragonStateChase
from ai.stickfigure.state_dying import StateDying
from ai.stickfigure.state_spawn import StateSpawn
from ai.stickfigure.state_wander import StateWander
from ai.stickfigure.state_dead import StateDead
from game.enemytype import EnemyType
from ai.rambo.state_attacking import RamboStateAttacking
from ai.rambo.state_standing import RamboStateStanding
from ai.rambo.state_spawn import RamboStateSpawn

logger = logging.getLogger(__name__)


class Ai():
    def __init__(self, name :str, enemyType :EnemyType =None):
        self.offensiveAttackEntity = None
        self.enemyType = enemyType

        self.name :str = 'Bot' + name


    def initAi(self, esperData):
        self.brain :Brain = Brain(esperData)
        
        if self.enemyType is EnemyType.rambo:
            self.brain.register(RamboStateAttacking)
            self.brain.register(RamboStateStanding)
            self.brain.register(RamboStateSpawn)

            self.brain.register(StateDying)
            self.brain.register(StateDead)
        else:
            self.brain.register(StateSpawn)
            if self.enemyType is EnemyType.cow:
                self.brain.register(CowStateAttack)
            else:
                self.brain.register(StateAttack)
            if self.enemyType is EnemyType.dragon:
                self.brain.register(DragonStateChase)
            else:
                self.brain.register(StateChase)
            self.brain.register(StateWander)
            self.brain.register(StateDying)
            self.brain.register(StateDead)
            self.brain.register(StateAttackWindup)
        self.brain.push("spawn")


    def advance(self, deltaTime :float):
        self.brain.update(deltaTime)


    def setEnemyType(self, enemyType):
        self.enemyType = enemyType


    def __repr__(self):
        return self.name
