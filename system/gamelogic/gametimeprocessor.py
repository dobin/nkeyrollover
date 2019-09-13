import esper
import logging

import system.singletons.gametime

logger = logging.getLogger(__name__)


class GametimeProcessor(esper.Processor):
    def process(self, dt):
        system.singletons.gametime.advance(dt)
