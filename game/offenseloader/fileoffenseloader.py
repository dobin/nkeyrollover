import logging

from game.offenseloader.weaponmanager import WeaponManager
from game.offenseloader.skillmanager import SkillManager

logger = logging.getLogger(__name__)


class FileOffenseLoader(object):
    def __init__(self):
        self.weaponManager = WeaponManager()
        self.skillManager = SkillManager()

    def loadFromFiles(self):
        logger.info("(Re)loading offense from files")
        self.weaponManager.loadFiles()
        self.skillManager.loadFiles()


fileOffenseLoader = FileOffenseLoader()
