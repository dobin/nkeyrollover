import logging

from texture.character.characteranimationmanager import CharacterAnimationManager
from texture.phenomena.phenomenaanimationmanager import PhenomenaAnimationManager
from texture.action.actionanimationmanager import ActionAnimationManager

logger = logging.getLogger(__name__)


class FileTextureLoader(object):
    def __init__(self):
        self.characterAnimationManager = CharacterAnimationManager()
        self.phenomenaAnimationManager = PhenomenaAnimationManager()
        self.actionAnimationManager = ActionAnimationManager()


    def loadFromFiles(self):
        logger.info("(Re)loading textures from files")
        self.actionAnimationManager.loadFiles()
        self.characterAnimationManager.loadFiles()
        self.phenomenaAnimationManager.loadFiles()


fileTextureLoader = FileTextureLoader()
