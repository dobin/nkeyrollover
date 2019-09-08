import logging
import esper

from messaging import messaging, MessageType
from config import Config
from directmessaging import directMessaging, DirectMessageType
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.graphics.renderable
import system.groupid

logger = logging.getLogger(__name__)


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        # list of HEIGHT lists
        # used to add renderable objects in the right Z order for render()
        self.renderOrder = [[] for i in range(Config.rows + 3)]


    def process(self, dt):
        # TODO which one first?
        self.collisionDetection()
        self.advance(dt)
        self.render()


    def advance(self, deltaTime):
        for ent, rend in self.world.get_component(system.graphics.renderable.Renderable):
            rend.advance(deltaTime)


    def collisionDetection(self):
        for message in messaging.get():
            # handle Player Attacks
            if message.type is MessageType.PlayerAttack:
                self.handleMessagePlayerAttack(message)

            # handle Enemy Attacks
            if message.type is MessageType.EnemyAttack:
                self.handleMessageEnemyAttack(message)


    def handleMessageEnemyAttack(self, message):
        hitLocations = message.data['hitLocations']
        damage = message.data['damage']

        for ent, (groupId, renderable, attackable, player) in self.world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.attackable.Attackable,
            system.gamelogic.player.Player
        ):
            if renderable.isHitBy(hitLocations):
                directMessaging.add(
                    groupId=groupId.id,
                    type=DirectMessageType.receiveDamage,
                    data=damage
                )


    def handleMessagePlayerAttack(self, message):
        damageSum = 0
        hitLocations = message.data['hitLocations']
        damage = message.data['damage']

        for ent, (groupId, renderable, attackable, enemy) in self.world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.attackable.Attackable,
            system.gamelogic.enemy.Enemy
        ):
            if renderable.isHitBy(hitLocations):
                directMessaging.add(
                    groupId=groupId.id,
                    type=DirectMessageType.receiveDamage,
                    data=damage
                )
                damageSum += damage

        # check if we should announce our awesomeness
        if damageSum > Config.announceDamage:
            # find player
            for ent, (groupId, player) in self.world.get_components(
                system.groupid.GroupId, system.gamelogic.player.Player
            ):
                directMessaging.add(
                    groupId = groupId.getId(),
                    type = DirectMessageType.activateSpeechBubble,
                    data = {
                        'text': 'Cowabunga!',
                        'time': 1.0,
                    }
                )


    def render(self):
        for l in self.renderOrder:
            l.clear()

        # add all elements to draw in the correct Z order
        # which is by y coordinates
        for ent, rend in self.world.get_component(system.graphics.renderable.Renderable):
            if rend.isActive():
                # logger.info("REND: {} {} {}".format(rend, rend.z, rend.coordinates))
                loc = rend.getLocation()
                self.renderOrder[loc.y + rend.z].append(rend)

        for l in self.renderOrder:
            for rend in l:
                rend.draw()