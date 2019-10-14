import logging

from stackfsm.states import BaseState as State

logger = logging.getLogger(__name__)


class StateDead(State):
    name = "dead"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        pass

    def on_exit(self):
        pass
