import esper
import curses, random, time, signal, sys
import logging
import locale 

from utilities.colorpalette import ColorPalette
from utilities.utilities import Utility
from world.scene import Scene
from config import Config
from world.world import World

current_milli_time = lambda: int(round(time.time() * 1000))


class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class KeyMove:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Renderable:
    def __init__(self, image, posx, posy, depth=0):
        self.image = image
        self.depth = depth
        self.x = posx
        self.y = posy
        self.w = 1
        self.h = 1


class MovementProcessor(esper.Processor):
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def process(self):
        for ent, (vel, rend) in self.world.get_components(KeyMove, Renderable):
            rend.x += vel.x
            rend.y += vel.y

            vel.x = 0
            vel.y = 0
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)

        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            # Update the Renderable Component's position by it's Velocity:
            rend.x += vel.x
            rend.y += vel.y
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)


class RenderProcessor(esper.Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.erase()
        self.window.border()

        # This will iterate over every Entity that has this Component, and blit it:
        for ent, rend in self.world.get_component(Renderable):
            #self.window.blit(rend.image, (rend.x, rend.y))
            self.window.addstr(rend.y, rend.x, rend.image)

##################################################################################################

class Nkro(object): 
    def __init__(self):
        self.init()
        self.initEsper()

    def init(self):
        locale.setlocale(locale.LC_ALL, '')
        Utility.setupLogger()

        if Config.devMode:
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')
        else: 
            logging.basicConfig(
                filename='app.log', 
                filemode='a', 
                level=logging.INFO,
                format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

        logger = logging.getLogger(__name__)
        logger.record("-----------------Start------------------------")

        self.menuwin = curses.newwin(3, Config.columns, 0, 0)
        self.menuwin.border()

        self.win = curses.newwin(Config.rows, Config.columns, 2, 0)
        curses.noecho()
        curses.cbreak()
        self.win.keypad(1) 
        curses.curs_set(0)    
        self.win.nodelay(1) # make getch() nonblocking
        ColorPalette.cursesInitColor()

        self.scene = Scene(self.win)

        if not Config.devMode:
            self.scene.titleScene()
            self.scene.introScene()

        self.win.clear()
        self.win.border()

        self.oldWorld = World(win=self.win)

        self.startTime = current_milli_time()
        self.currentTime = self.startTime
        self.workTime = 0


    def initEsper(self):
        # Initialize Esper world, and create a "player" Entity with a few Components.
        self.world = esper.World()

        self.player = self.world.create_entity()
        #self.world.add_component(player, Velocity(x=1, y=1))
        self.world.add_component(self.player, KeyMove(x=0, y=0))
        self.world.add_component(self.player, Renderable(image='p', posx=10, posy=10))
        
        # Another, motionless, Entity:
        enemy = self.world.create_entity()
        self.world.add_component(enemy, Renderable(image='r', posx=12, posy=12))

        # Create some Processor instances, and asign them to be processed.
        render_processor = RenderProcessor(window=self.win)
        movement_processor = MovementProcessor(minx=0, maxx=Config.columns, miny=0, maxy=Config.rows)
        self.world.add_processor(render_processor)
        self.world.add_processor(movement_processor)


    def loop(self): 
        n = 0
        targetFrameTime = 1.0 / Config.fps
        deltaTime = targetFrameTime # we try to keep it...
        timeStart = 0
        timeEnd = 0
        workTime = 0
        while self.oldWorld.gameRunning:
            timeStart = time.time()

            # has to be after draw, as getch() does a refresh
            # https://stackoverflow.com/questions/19748685/curses-library-why-does-getch-clear-my-screen
            # keep inputrate below half FPS (50/s by default)
            key = self.oldWorld.viewport.win.getch()

            if key == curses.KEY_LEFT:
                self.world.component_for_entity(self.player, KeyMove).x -= 1

            elif key == curses.KEY_RIGHT:
                self.world.component_for_entity(self.player, KeyMove).x += 1

            elif key == curses.KEY_UP:
                self.world.component_for_entity(self.player, KeyMove).y -= 1

            elif key == curses.KEY_DOWN: 
                self.world.component_for_entity(self.player, KeyMove).y += 1

            self.world.process()

            # fps logistics
            timeEnd = time.time()
            workTime = timeEnd - timeStart
            self.workTime = workTime
            if workTime > targetFrameTime:
                logging.warn("Could not keep FPS! Worktime was: {}ms".format( self.workTime * 100.0))

            targetSleepTime = targetFrameTime - workTime
            if targetSleepTime < 0:
                logging.error("Sleep for negative amount: " + str(targetSleepTime))
            else:
                time.sleep(targetSleepTime)
            n = n + 1 

        # Clean up before exiting
        curses.nocbreak()
        self.win.keypad(0)
        curses.echo()
        curses.endwin()


def signal_handler(sig, frame):
    # Clean up before exiting
    curses.nocbreak()
    curses.echo()
    curses.endwin()

    sys.exit(0)


def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)
    keyrollover = Nkro()
    keyrollover.loop()


if __name__ == '__main__':
    curses.wrapper(main)