#!/usr/bin/env python

import unittest

from messaging import messaging, MessageType
import game.isunittest


class MessagingTest(unittest.TestCase):
    def test_messaging(self):
        game.isunittest.setIsUnitTest()

        messaging.add(
            type=MessageType.Unittest,
            data={
                'test': 'test1'
            }
        )
        messaging.add(
            type=MessageType.Unittest,
            groupId=1,
            data={
                'test': 'test2'
            }
        )
        messaging.add(
            type=MessageType.AttackAt,
            data={
                'test': 'test3'
            }
        )

        self.assertTrue(len(messaging.get()) == 3)

        for (idx, msg) in enumerate(messaging.getByType(MessageType.Unittest)):
            if idx == 0:
                self.assertTrue(msg.data['test'] == 'test1')
            if idx == 1:
                self.assertTrue(msg.data['test'] == 'test2')
            self.assertTrue(idx <= 1)

        for (idx, msg) in enumerate(messaging.getByType(MessageType.AttackAt)):
            if idx == 0:
                self.assertTrue(msg.data['test'] == 'test3')
            self.assertTrue(idx <= 0)

        for (idx, msg) in enumerate(messaging.getByGroupId(1)):
            if idx == 0:
                self.assertTrue(msg.data['test'] == 'test2')
            self.assertTrue(idx <= 0)

        messaging.reset()

        self.assertTrue(len(messaging.get()) == 0)


if __name__ == '__main__':
    unittest.main()
