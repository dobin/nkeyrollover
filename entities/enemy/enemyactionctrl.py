
from entities.action import Action
from config import Config
from entities.direction import Direction

from entities.baseactionctrl import BaseActionCtrl

import logging
import random

logger = logging.getLogger(__name__)

class EnemyActionCtrl(BaseActionCtrl):
    def changeTo(self, newAction, direction):
        self.parentEntity.setActive(True)
        
        if newAction is Action.walking:
            # we start, or continue, walking
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            # if we were already walking, dont destroy the animation state
            if self.type is not Action.walking:
                logger.info("EE Change action to1: " + str(newAction))
                self.parentEntity.sprite.initSprite(newAction, direction, None)
        elif newAction is Action.dying: 
            logger.info("EE Change action to2: " + str(newAction))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)
            #animationIndex = random.randint(0, 1)
            animationIndex = 1

            if animationIndex == 2:
                logger.info("Death animation deluxe")
                #world.makeExplode(self.sprite, None)
                self.parentEntity.sprite.initSprite(newAction, direction, animationIndex)
                self.parentEntity.isActive = False
            else: 
                self.parentEntity.sprite.initSprite(newAction, direction, animationIndex)
        else: 
            logger.info("EE Change action to3: " + str(newAction))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)
            self.parentEntity.sprite.initSprite(newAction, direction, None)

        self.type = newAction


    def specificAdvance(self):
        # when dying, desintegrate
        if self.type is Action.dying: 
            if self.durationLeft == 0:
                logging.warning("EE Deactivate!")
                self.parentEntity.setActive(False)
