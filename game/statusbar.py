import logging
import curses

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

logger = logging.getLogger(__name__)


class StatusBar(object):
    def __init__(self, world, menuwin):
        self.world = world
        self.menuwin = menuwin


    def drawStatusbar(self):
        # fps = 0
        # if n > 100:
        #    fps = 1000 * (float)(n) / (float)(current_milli_time() - self.startTime)
        #    #fps = self.workTime * 1000.0
        playerEntity = EntityFinder.findPlayer(self.world.world)
        if playerEntity is None:
            # No player here yet
            return

        #self.menuwin.erase()
        #self.menuwin.border()
        playerAttackable = self.world.world.component_for_entity(
            playerEntity, Attackable)
        player = self.world.world.component_for_entity(
            playerEntity, Player)

        s = "Health: " + str(playerAttackable.getHealth())
        s += "  Points: " + str(player.points)

        #s += "  FPS: %.0f" % (fps)
        color = ColorPalette.getColorByColorType(ColorType.menu, None)
        self.menuwin.addstr(1, 2, s, color)

        self.printSkillbar(color, playerEntity)
        self.printAttackbar(color, playerEntity)
        self.menuwin.refresh()


    def printSkillbar(self, color, playerEntity):
        playerOffensiveSkill = self.world.world.component_for_entity(
            playerEntity, OffensiveSkill)

        basex = 34
        n = 0
        for skill in playerOffensiveSkill.skillStatus:
            if playerOffensiveSkill.isRdy(skill):
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(9))
            else:
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(10))

            n += 1

    def printAttackbar(self, color, playerEntity):
        playerGroupId = self.world.world.component_for_entity(
            playerEntity, GroupId)
        playerOffensiveAttack = EntityFinder.findOffensiveAttackByGroupId(
            self.world.world,
            playerGroupId.getId())

        weaponIdx = 42
        self.menuwin.addstr(
            1,
            weaponIdx,
            'W:' + playerOffensiveAttack.getWeaponStr(),
            color)

        weaponIdx = 52
        self.menuwin.addstr(
            1,
            weaponIdx,
            'APM:' + str(int(apm.getApm() * 60)),
            color)

        weaponIdx = 62
        self.menuwin.addstr(
            1,
            weaponIdx,
            'DMG/s:' + str(int(damageStat.getDamageStat())),
            color)
