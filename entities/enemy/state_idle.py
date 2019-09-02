import logging

from ai.states import BaseState as State

logger = logging.getLogger(__name__)


class StateIdle(State):
    name = "idle"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        pass

    def on_exit(self):
        pass