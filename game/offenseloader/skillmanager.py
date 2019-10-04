import logging
import os
import yaml

from system.graphics.particleeffecttype import ParticleEffectType
from game.offenseloader.skilltype import SkillType
from game.offenseloader.skilldata import SkillData

logger = logging.getLogger(__name__)


class SkillManager(object):
    def __init__(self):
        self.skillData = {}


    def loadFiles(self):
        self.skillData = {}

        for skillType in SkillType:
            self.loadSkillData(skillType)


    def loadSkillData(self, skillType):
        skillName = skillType.name
        filename = "data/skills/skill_{}.yaml".format(skillName)

        if not os.path.isfile(filename):
            logger.debug("No skill definition in {}, skipping".format(
                filename
            ))
            return None

        skillData = self.readSkillYamlFile(filename)
        self.skillData[skillType] = skillData


    def readSkillYamlFile(self, filename :str) -> SkillData:
        skill = SkillData()

        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        try:
            if 'particleeffect' in data:
                skill.particleEffectType = ParticleEffectType[data['particleeffect']]
            skill.damage = int(data['damage'])

        except TypeError as error:
            raise Exception("Error, missing field in yaml file {}, error {}".format(
                filename, error
            ))

        return skill


    def getSkillData(
        self,
        skillType: SkillType
    ) -> SkillData:

        return self.skillData[skillType]