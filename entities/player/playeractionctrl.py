import logging

from config import Config
from sprite.direction import Direction
from entities.actionctrl import ActionCtrl
from texture.character.characteranimationtype import CharacterAnimationType

logger = logging.getLogger(__name__)


class PlayerActionCtrl(ActionCtrl):
    """ The Player-Character controller. Manage states, like standing->walking """

    def changeTo(self, newCharacterAnimationType, direction):
        self.parentEntity.setActive(True)

        if newCharacterAnimationType is CharacterAnimationType.walking:
            # we start, or continue, walking, endlessly
            self.durationTimer.setTimer(1.0)
            self.durationTimer.reset()

            # if we were already walking, dont destroy the animation state
            if self.action is not CharacterAnimationType.walking:
                logger.debug("Player Change action to: " + str(newCharacterAnimationType))
                self.parentEntity.texture.changeAnimation(newCharacterAnimationType, direction)
        else: 
            logger.debug("Player Change action to: " + str(newCharacterAnimationType))
            
            self.parentEntity.texture.changeAnimation(newCharacterAnimationType, direction)
            animationTime = self.parentEntity.texture.getAnimationTime()

            self.durationTimer.setTimer(animationTime)
            self.durationTimer.reset()

        self.action = newCharacterAnimationType


    def specificAdvance(self):
        # stand still after some non walking
        if self.action is CharacterAnimationType.walking: 
            if self.durationTimer.timeIsUp():
                self.action = CharacterAnimationType.standing
                self.parentEntity.texture.changeAnimation(CharacterAnimationType.standing, Direction.right)

        # after hitting is finished, stand still
        if self.action is CharacterAnimationType.hitting: 
            if self.durationTimer.timeIsUp():
                self.action = CharacterAnimationType.standing
                self.parentEntity.texture.changeAnimation(CharacterAnimationType.standing, Direction.right)

        # when dying, desintegrate
        if self.action is CharacterAnimationType.dying: 
            if self.durationTimer.timeIsUp():
                logging.info("Player Deactivate!")
                self.isActive = False
