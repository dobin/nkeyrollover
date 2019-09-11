import logging

from stackfsm.brain import Brain
from ai.stickfigure.state_attack import StateAttack
from ai.cow.state_attack import StateAttack as CowStateAttack
from ai.stickfigure.state_attackwindup import StateAttackWindup
from ai.stickfigure.state_chase import StateChase
from ai.stickfigure.state_dying import StateDying
from ai.stickfigure.state_spawn import StateSpawn
from ai.stickfigure.state_wander import StateWander
from ai.stickfigure.state_dead import StateDead
from texture.character.charactertype import CharacterType

logger = logging.getLogger(__name__)


class Ai():
    def __init__(self, esperData, name, characterType):
        self.esperData = esperData
        self.offensiveAttackEntity = None
        self.characterType = characterType

        self.name :str = 'Bot' + name
        self.initAi()


    def initAi(self):
        self.brain :Brain = Brain(self.esperData)

        self.brain.register(StateSpawn)
        if self.characterType is CharacterType.cow:
            self.brain.register(CowStateAttack)
        else: 
            self.brain.register(StateAttack)
        self.brain.register(StateChase)
        self.brain.register(StateWander)
        self.brain.register(StateDying)
        self.brain.register(StateDead)
        self.brain.register(StateAttackWindup)
        self.brain.push("spawn")


    def advance(self, deltaTime :float):
        self.brain.update(deltaTime)


    def __repr__(self):
        return self.name
