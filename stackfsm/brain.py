import logging
from collections import deque
from stackfsm.states import BaseState

STATES = []

#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Brain:
	"""
	All AI agents will contain this, this is the object
	that keeps and processes states, remove it and the
	agent becomes braindead...
	"""
	def __init__(self, owner, init_state=None):
		log.debug("{}: Initiated brain with owner \"{}\"".format(owner, owner))
		self.owner = owner
		self.stack = deque()
		self.avail_states = dict([(s.name, s) for s in STATES])
		if init_state:
			self.register(init_state)
			self.push(init_state.name)

	@property
	def state(self):
		if len(self.stack):
			return self.stack[-1]
		return None

	@property
	def states(self):
		return [k for k in self.avail_states]

	def emptyStack(self): 
		self.stack.clear()

	def __repr__(self):
		if self.state:
			return "{0}: brain in \"{1}\" state>".format(
				self.owner, self.state.name
			)

	def push(self, state):
		if state in self.avail_states:
			if isinstance(self.state, self.avail_states[state]):
				log.warning(
					"{}: Attempting to push the same state as the current one "
					"({}).".format(self.owner, state)
				)
				return
			log.debug("{}: Pushing state \"{}\" to stack.".format(self.owner, state))
			# Initiate a state object, pass it this brain instance as a
			# parameter, then push it to the top of the stack.
			self.stack.append(self.avail_states[state](self))
			log.info("{}: Current state is \"{}\"".format(self.owner, self.state.name))
			self.state.on_enter()
		else:
			log.error(
				"{}: {} is not a valid state (not registered).".format(self.owner, state)
			)

	def pop(self):
		try:
			s = self.stack.pop()
		except IndexError:
			log.error("{}: Attempted to pop on an empty stack.".format(self.owner))
		else:
			s.on_exit()
			log.debug("{}: Removed state \"{}\" from stack.".format(self.owner, s.name))
			if self.state:
				log.info("{}: Current state is \"{}\"".format(self.owner, self.state.name))

	def register(self, *args):
		if len(args) == 1 and isinstance(args[0], list):
			args = args[0]
		for state in args:
			if not issubclass(state, BaseState):
				raise ValueError("Not a valid state object, needs to inherit from BaseState")
			elif state.name in self.avail_states:
				log.error(
					"There's already a state with that name: " + state.name
				)
			else:
				# log.info("Registered a new state \"{}\".".format(state.name))
				self.avail_states[state.name] = state

	def unregister(self, name):
		if not name in self.avail_states:
			log.error("No such state registered: {}.".format(name))
			return
		log.info("Unregistering \"{}\" from available states.".format(name))
		s = self.avail_states.pop(name)

	def update(self, dt):
		if self.state:
			self.state.updateTimer(dt)
			self.state.process(dt)

