gametime = 0.0

# Set by:
# - GametimeProcessor
# Read by:
# - Component Attackable

def advance(time):
    global gametime
    gametime += time


def getGameTime():
    global gametime
    return gametime
