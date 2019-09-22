import logging

from texture.character.characteranimationmanager import CharacterAnimationManager
from texture.phenomena.phenomenaanimationmanager import PhenomenaAnimationManager
from texture.action.actionanimationmanager import ActionAnimationManager
from texture.weapon.weaponanimationmanager import WeaponAnimationManager

logger = logging.getLogger(__name__)


class FileTextureLoader(object):
    def __init__(self):
        self.characterAnimationManager = CharacterAnimationManager()
        self.phenomenaAnimationManager = PhenomenaAnimationManager()
        self.actionAnimationManager = ActionAnimationManager()
        self.weaponAnimationManager = WeaponAnimationManager()


    def loadFromFiles(self):
        self.characterAnimationManager.loadFiles()
        self.phenomenaAnimationManager.loadFiles()
        self.actionAnimationManager.loadFiles()
        self.weaponAnimationManager.loadFiles()


fileTextureLoader = FileTextureLoader()
