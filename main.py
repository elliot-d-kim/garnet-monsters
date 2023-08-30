import sys
import pygame
from pygame.locals import *
from pygame import Rect
from src.util import colors as col
from src.util import graphics as gr
from src.stages.splash.splash import Splash
from src.stages.world.world import World
from src.stages.bag.bag import Bag
from src.stages.catch.catch import Catch
from src.stages.credits.credits import Credits
from src.stages.journal.journal import Journal
from src.stages.profile.profile import Profile
from src.logic.state import State
from src.util.graphics import FPS
import logging

"""
Top level class of the project.
"""
class App:
    # Stages
    stageNames = {
        "splash": Splash,
        "world": World,
        "catch": Catch,
        "credits": Credits,
        "journal": Journal,
        "bag": Bag,
        "profile": Profile
    }

    # Constructor
    def __init__(self):
        # init PyGame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((gr.BOUND_TOT[2], gr.BOUND_TOT[3]))
        self.upSurface = self.surface.subsurface(gr.BOUND_UP)
        self.lowSurface = self.surface.subsurface(gr.BOUND_LOW)
        pygame.display.set_caption("Garnet Monsters")

        # init fonts
        App.loadFonts()


        # create all the stages
        self.stages = {}
        state = State()
        for n in App.stageNames:
            self.stages[n] = App.stageNames[n](self, state)

        #set the active stage
        self.active = self.stageNames["splash"](self, state)
        self.active.load()
    @staticmethod
    def loadFonts():
        pygame.font.init()
        gr.FONT_4 = pygame.font.Font("src/assets/fonts/joystix.ttf", 4)
        gr.FONT_6 = pygame.font.Font("src/assets/fonts/joystix.ttf", 6)
        gr.FONT_8 = pygame.font.Font("src/assets/fonts/joystix.ttf", 8)
        gr.FONT_10 = pygame.font.Font("src/assets/fonts/joystix.ttf", 10)
        gr.FONT_12 = pygame.font.Font("src/assets/fonts/joystix.ttf", 12)
        gr.FONT_14 = pygame.font.Font("src/assets/fonts/joystix.ttf", 14)
        gr.FONT_16 = pygame.font.Font("src/assets/fonts/joystix.ttf", 16)
        gr.FONT_20 = pygame.font.Font("src/assets/fonts/joystix.ttf", 20)
        gr.FONT_24 = pygame.font.Font("src/assets/fonts/joystix.ttf", 24)
        gr.FONT_28 = pygame.font.Font("src/assets/fonts/joystix.ttf", 28)
        gr.FONT_32 = pygame.font.Font("src/assets/fonts/joystix.ttf", 32)

    # Game loop
    def loop(self):
        # stage logic
        self.getInput()
        self.active.update()

        # prepare canvas
        self.surface.fill(col.LIGHT_GRAY)

        # stage drawing
        self.active.draw()

        # overlay on canvas
        self.drawCanvasRibbons()

        # update the display
        pygame.display.update()
    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    # Loop utility
    def drawCanvasRibbons(self):
        pygame.draw.rect(self.surface, col.BLACK, Rect(0, 0, gr.BOUND_TOT.w, gr.RIBBON))
        pygame.draw.rect(self.surface, col.BLACK, Rect(0, gr.RIBBON + gr.SCR_HT, gr.BOUND_TOT.w, gr.RIBBON))
        pygame.draw.rect(self.surface, col.BLACK, Rect(0, gr.BOUND_TOT.h - gr.RIBBON, gr.BOUND_TOT.w, gr.RIBBON))
        pygame.draw.rect(self.surface, col.BLACK, Rect(0, 0, gr.RIBBON, gr.BOUND_TOT.h))
        pygame.draw.rect(self.surface, col.BLACK, Rect(gr.BOUND_TOT.w - gr.RIBBON, 0, gr.RIBBON, gr.BOUND_TOT.h))
    def drawLowerBackground(self):
        pygame.draw.rect(self.surface, col.LIGHT_GRAY, gr.BOUND_LOW)
    def getInput(self):
        #update mouse position
        if gr.BOUND_LOW.collidepoint(pygame.mouse.get_pos()):
            self.active.setMousePos(App.transformPosToLower(pygame.mouse.get_pos()))
        else:
            self.active.setMousePos((-1, -1))

        #general events
        for event in pygame.event.get():
            if event.type == QUIT:
                App.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gr.BOUND_LOW.collidepoint(pygame.mouse.get_pos()):
                    self.active.mouseDown(App.transformPosToLower(pygame.mouse.get_pos()))
            elif event.type == pygame.MOUSEBUTTONUP:
                if gr.BOUND_LOW.collidepoint(pygame.mouse.get_pos()):
                    self.active.mouseUp(App.transformPosToLower(pygame.mouse.get_pos()))

    @staticmethod
    def transformPosToLower(position):
        return position[0]-gr.BOUND_LOW.x, position[1]-gr.BOUND_LOW.y

    # Outward facing
    def switchStage(self, stageName):
        if stageName in self.stageNames:
            self.active.unload()
            self.active = self.stages[stageName]
            self.active.load()
        else:
            logging.exception("Unknown stage name provided")


"""
App initialization and game loop.
"""
if __name__ == "__main__":
    app = App()
    while True:
        app.loop()
        app.clock.tick(FPS)
