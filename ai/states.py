import logging

log = logging.getLogger(__name__)


class BaseState(object):
	name = "base"

	def __init__(self, brain):
		self.brain = brain
		self.timer = 0.0

	@property
	def owner(self):
		return self.brain.owner

	def pop(self):
		self.brain.pop()


	def setTimer(self, time):
		self.timer = time

	def updateTimer(self, dt):
		if self.timer > 0.0:
			self.timer -= dt

	def timeIsUp(self):
		if self.timer <= 0.0:
			return True
		else:
			return False


	# What follows is empty methods to be overloaded.
	def on_enter(self):
		pass

	def on_exit(self):
		pass

	def process(self, dt):
		pass

	def __repr__(self):
		return "<{}>".format(self.__class__.__name__)


