import logging
import curses

from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from system.offensiveattack import OffensiveAttack
from system.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from utilities.entityfinder import EntityFinder


class StatusBar(object):
    def __init__(self, world, menuwin):
        self.world = world
        self.menuwin = menuwin


    def drawStatusbar(self):
        # fps = 0
        # if n > 100:
        #    fps = 1000 * (float)(n) / (float)(current_milli_time() - self.startTime)
        #    #fps = self.workTime * 1000.0

        playerEntity = EntityFinder.findPlayer(self.world.esperWorld)
        if playerEntity is None: 
            # No player here yet
            return


        #self.menuwin.erase()
        #self.menuwin.border()
        playerAttackable = self.world.esperWorld.component_for_entity(
            playerEntity, Attackable)
        player = self.world.esperWorld.component_for_entity(
            playerEntity, Player)

        s = "Health: " + str(playerAttackable.getHealth())
        s += "  Points: " + str(player.points)

        #s += "  FPS: %.0f" % (fps)
        color = ColorPalette.getColorByColorType(ColorType.menu, None)
        self.menuwin.addstr(1, 2, s, color )

        self.printSkillbar(color, playerEntity)
        self.printAttackbar(color, playerEntity)
        self.menuwin.refresh()


    def printSkillbar(self, color, playerEntity):
        playerOffensiveSkill = self.world.esperWorld.component_for_entity(
            playerEntity, OffensiveSkill)

        basex = 54
        n = 0
        for skill in playerOffensiveSkill.skillStatus:
            if playerOffensiveSkill.isRdy(skill):
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(9))
            else:
                self.menuwin.addstr(1, basex + n, skill, curses.color_pair(10))

            n += 1

    def printAttackbar(self, color, playerEntity):
        playerGroupId = self.world.esperWorld.component_for_entity(
            playerEntity, GroupId)
        playerOffensiveAttack = EntityFinder.findOffensiveAttackByGroupId(
            self.world.esperWorld,
            playerGroupId.getId())
        
        weaponIdx = 62
        self.menuwin.addstr(1,
            weaponIdx,
            'W:' + playerOffensiveAttack.getWeaponStr(),
            color)

        weaponIdx = 62
        self.menuwin.addstr(1,
            weaponIdx,
            'APM:' + str(int(self.world.inputProcessor.apm.getApm() * 60)),
            color)