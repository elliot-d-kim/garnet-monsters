from abc import ABC, abstractmethod
import pygame

"""
This class is the superclass for all other stages. It provides the methods that the App needs to communicate with the
stages. Additionally, it provides all methods that the children classes need for communicating with the App class.
Therefore, the child classes should never need to directly access the App.
"""
class Stage(ABC):

    # Constructor
    def __init__(self, app, state):
        self.app = app
        self.state = state

        self.mousePos = [0, 0]

    # Basic stage methods
    """
    Called when this stage becomes the active stage.
    """
    def load(self):
        self.mousePos = (-1, -1)
    """
    Called when this stage ceases to be the active stage.
    """
    def unload(self):
        pass
    """
    Called once per loop while this stage is active. Should be used to update the game state.
    """
    @abstractmethod
    def update(self):
        pass
    """
    Called once per loop while this stage is active. Should be used to draw onto the game canvas.
    """
    @abstractmethod
    def draw(self):
        pass

    # Input methods
    def mouseDown(self, position):
        pass
    def mouseUp(self, position):
        pass
    def setMousePos(self, position):
        self.mousePos = position
    def uiInput(self, fired, descript, location):
        pass

    # Wrapper for app methods
    def switchStage(self, stageName):
        self.app.switchStage(stageName)

    # Drawing methods, origin at the top left on the given screen
    def drawLowRect(self, color, rect):
        pygame.draw.rect(self.app.lowSurface, color, rect)

    def drawLowRectRoundedBorders(self, color, rect):
        pygame.draw.rect(self.app.lowSurface, color, rect, 4, 3)

    def drawLowImage(self, image, rect):
        self.app.lowSurface.blit(image, rect)

    def drawUpRect(self, color, rect):
        pygame.draw.rect(self.app.upSurface, color, rect)
    def drawUpImage(self, image, rect):
        self.app.upSurface.blit(image, rect)


    def runMenu(self, menu):
        menu.mainloop(self.app.lowSurface)



    # Asset methods
    @staticmethod
    def loadImage(path):
        return pygame.image.load(path)
