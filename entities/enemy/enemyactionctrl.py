
from entities.action import Action
from config import Config
from entities.direction import Direction

from entities.actionctrl import ActionCtrl

import logging
import random

logger = logging.getLogger(__name__)

class EnemyActionCtrl(ActionCtrl):
    """ The Enemy-Character controller. Manage states and the transfer between them
    
        States like standing->walking. 
        
        This mostly works on Enemy() class (via parentEntity), and its sprite
    """

    def changeTo(self, newAction, direction):
        self.parentEntity.setActive(True)
        
        if newAction is Action.walking:
            # we start, or continue, walking
            self.resetDuration(
                duration=Config.secToFrames(1),
                durationLeft=Config.secToFrames(1),
            )

            # if we were already walking, dont destroy the animation state
            if self.action is not Action.walking:
                logger.info("EE Change action to1: " + str(newAction))
                self.parentEntity.sprite.initSprite(newAction, direction, None)
        elif newAction is Action.dying: 
            logger.info("EE Change action to2: " + str(newAction))
            self.resetDuration(
                duration=Config.secToFrames(1),
                durationLeft=Config.secToFrames(1),
            )
            #animationIndex = random.randint(0, 1)
            animationIndex = 2

            if animationIndex == 2:
                logger.info("Death animation deluxe")
                self.world.makeExplode(self.parentEntity.sprite, None)
                self.parentEntity.sprite.initSprite(newAction, direction, animationIndex)
                self.parentEntity.isActive = False
            else: 
                self.parentEntity.sprite.initSprite(newAction, direction, animationIndex)
        else: 
            logger.info("EE Change action to3: " + str(newAction))
            self.resetDuration(
                duration=Config.secToFrames(1),
                durationLeft=Config.secToFrames(1),
            )
            self.parentEntity.sprite.initSprite(newAction, direction, None)

        self.action = newAction


    def specificAdvance(self):
        # when dying, desintegrate
        if self.action is Action.dying: 
            if self.durationTimeIsUp():
                logging.info("EE Deactivate!")
                self.parentEntity.setActive(False)
