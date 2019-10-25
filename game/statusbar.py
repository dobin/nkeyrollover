import logging

from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from system.gamelogic.offensiveattack import OffensiveAttack
from system.gamelogic.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from utilities.entityfinder import EntityFinder
from system.singletons.apm import apm
from system.singletons.damagestat import damageStat
from asciimatics.screen import Screen
from config import Config

logger = logging.getLogger(__name__)


class StatusBar(object):
    def __init__(self, world, viewport):
        self.world = world
        self.viewport = viewport


    def drawStatusbar(self):
        # fps = 0
        # if n > 100:
        #    fps = 1000 * (float)(n) / (float)(current_milli_time() - self.startTime)
        #    #fps = self.workTime * 1000.0
        playerEntity = EntityFinder.findPlayer(self.world.world)
        if playerEntity is None:
            # No player here yet
            return

        #self.viewport.erase()
        #self.viewport.border()
        playerAttackable = self.world.world.component_for_entity(
            playerEntity, Attackable)
        player = self.world.world.component_for_entity(
            playerEntity, Player)

        color, attr = ColorPalette.getColorByColor(Color.black)
        bgcolor, _ = ColorPalette.getColorByColor(Color.white)

        s = " Health: " + str(playerAttackable.getHealth())
        s += "  Points: " + str(player.points)
        s += " " * (Config.columns - 2 - len(s))
        #s += "  FPS: %.0f" % (fps)
        self.viewport.addstrStatic(1, 1, s, color, attr, bg=bgcolor)

        self.printSkillbar(color, attr, bgcolor, playerEntity)
        self.printAttackbar(color, attr, bgcolor, playerEntity)


    def printSkillbar(self, color, attr, bgcolor, playerEntity):
        playerOffensiveSkill = self.world.world.component_for_entity(
            playerEntity, OffensiveSkill)

        basex = 34
        n = 0
        for skill in playerOffensiveSkill.skillStatus:
            if playerOffensiveSkill.isRdy(skill):
                self.viewport.addstrStatic(
                    1, basex + n, skill, color, attr, bg=Screen.COLOUR_GREEN)
            else:
                self.viewport.addstrStatic(
                    1, basex + n, skill, color, attr, bg=Screen.COLOUR_RED)

            n += 1

    def printAttackbar(self, color, attr, bgcolor, playerEntity):
        playerGroupId = self.world.world.component_for_entity(
            playerEntity, GroupId)
        playerOffensiveAttack = EntityFinder.findOffensiveAttackByGroupId(
            self.world.world,
            playerGroupId.getId())

        weaponIdx = 42
        self.viewport.addstrStatic(
            1,
            weaponIdx,
            'W:' + playerOffensiveAttack.getWeaponStr(),
            color,
            attr,
            bg=bgcolor)

        weaponIdx = 52
        self.viewport.addstrStatic(
            1,
            weaponIdx,
            'APM:' + str(int(apm.getApm() * 60)),
            color,
            attr,
            bg=bgcolor)

        weaponIdx = 62
        self.viewport.addstrStatic(
            1,
            weaponIdx,
            'DMG/s:' + str(int(damageStat.getDamageStat())),
            color,
            attr,
            bg=bgcolor)
