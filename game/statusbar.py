import logging

from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from system.gamelogic.offensiveattack import OffensiveAttack
from system.gamelogic.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from utilities.entityfinder import EntityFinder
from system.singletons.apm import apm
from system.singletons.damagestat import damageStat
from asciimatics.screen import Screen

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

        s = "Health: " + str(playerAttackable.getHealth())
        s += "  Points: " + str(player.points)

        #s += "  FPS: %.0f" % (fps)
        color = ColorPalette.getColorByColorType(ColorType.menu, None)
        self.viewport.addstr(1, 2, s, color)

        self.printSkillbar(color, playerEntity)
        self.printAttackbar(color, playerEntity)


    def printSkillbar(self, color, playerEntity):
        playerOffensiveSkill = self.world.world.component_for_entity(
            playerEntity, OffensiveSkill)

        basex = 34
        n = 0
        for skill in playerOffensiveSkill.skillStatus:
            if playerOffensiveSkill.isRdy(skill):
                self.viewport.addstr(1, basex + n, skill, Screen.COLOUR_BLACK, bg=Screen.COLOUR_GREEN)
            else:
                self.viewport.addstr(1, basex + n, skill, Screen.COLOUR_BLACK, bg=Screen.COLOUR_RED)

            n += 1

    def printAttackbar(self, color, playerEntity):
        playerGroupId = self.world.world.component_for_entity(
            playerEntity, GroupId)
        playerOffensiveAttack = EntityFinder.findOffensiveAttackByGroupId(
            self.world.world,
            playerGroupId.getId())

        weaponIdx = 42
        self.viewport.addstr(
            1,
            weaponIdx,
            'W:' + playerOffensiveAttack.getWeaponStr(),
            color)

        weaponIdx = 52
        self.viewport.addstr(
            1,
            weaponIdx,
            'APM:' + str(int(apm.getApm() * 60)),
            color)

        weaponIdx = 62
        self.viewport.addstr(
            1,
            weaponIdx,
            'DMG/s:' + str(int(damageStat.getDamageStat())),
            color)
