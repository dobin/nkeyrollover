from system.graphics.particleeffecttype import ParticleEffectType


class SkillData(object):
    def __init__(self):
        self.skillType = None
        self.particleEffectType :ParticleEffectType = None
        self.damage :int = None
        self.cooldown :float = None
