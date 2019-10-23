#!/usr/bin/env python

import unittest
import esper

from system.gamelogic.attackable import Attackable
import game.isunittest
from system.gamelogic.attackableprocessor import AttackableProcessor
from system.gamelogic.gametimeprocessor import GametimeProcessor


class AttackableTest(unittest.TestCase):
    def test_stun(self):
        game.isunittest.setIsUnitTest()
        self.world = esper.World()

        attackable = Attackable(
            initialHealth=100,
            stunTime=0.75,
            stunCount=2,
            stunTimeFrame=3)

        entity = self.world.create_entity()
        self.world.add_component(entity, attackable)

        gametimeProcessor = GametimeProcessor()
        attackableProcessor = AttackableProcessor()
        self.world.add_processor(attackableProcessor)
        self.world.add_processor(gametimeProcessor)

        # 0
        self.assertTrue(attackable.isStunnable())

        attackable.addStun(0.75)  # 1
        self.assertTrue(attackable.isStunnable())

        self.world.process(0.5)
        attackable.addStun(0.75)  # 2
        self.assertTrue(attackable.isStunnable())

        self.world.process(0.5)
        self.assertTrue(attackable.isStunnable())
        attackable.addStun(0.75)  # 3

        self.world.process(0.5)
        self.assertFalse(attackable.isStunnable())
        # 3seconds to reset, so 1.5+1.6 > 3.0
        self.world.process(1.6)

        self.assertTrue(attackable.isStunnable())
