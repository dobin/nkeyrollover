#!/usr/bin/env python

import unittest
import esper

import system.gamelogic.player
from messaging import messaging, MessageType
from sprite.coordinates import Coordinates
from config import Config
from texture.character.charactertype import CharacterType
from texture.character.charactertexture import CharacterTexture
from entities.esperdata import EsperData
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.renderable import Renderable
from system.gamelogic.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.offensiveattack import OffensiveAttack
from utilities.entityfinder import EntityFinder
from system.gamelogic.player import Player


class RenderableTest(unittest.TestCase):
    def test_renderable(self):

        self.world = esper.World()
        self.viewport = None
        self.particleEmiter = None

        # Player
        myid = 0
        self.playerEntity = self.world.create_entity()
        esperData = EsperData(self.world, self.playerEntity, 'player')
        texture = CharacterTexture(
            characterType=CharacterType.player,
            characterAnimationType=CharacterAnimationType.standing)
        texture.name = "Player"
        coordinates = Coordinates(
            Config.playerSpawnPoint['x'],
            Config.playerSpawnPoint['y']
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates)
        characterSkill = OffensiveSkill(
            esperData=esperData,
            particleEmiter=self.particleEmiter,
            viewport=self.viewport)
        
        renderable.name = "Player"
        groupId = GroupId(id=myid)
        player = system.gamelogic.player.Player()

        offensiveAttack = OffensiveAttack(
            parentChar=player,
            parentRenderable=renderable)


        self.world.add_component(self.playerEntity, offensiveAttack)

        self.world.add_component(self.playerEntity, groupId)
        self.world.add_component(self.playerEntity, characterSkill)
        self.world.add_component(self.playerEntity, renderable)
        self.world.add_component(self.playerEntity, player)
        self.world.add_component(self.playerEntity, Attackable(initialHealth=100))
        
        self.characterSkillEntity = characterSkill
        self.playerRendable = renderable



if __name__ == '__main__':
    unittest.main()