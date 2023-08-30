import math, pygame
import numpy as np
from pygame import Rect
from src.logic.state import BERRY_TYPES
from src.logic.ui import BerryButton, TextButton
from src.stages.stage import Stage
from src.util import graphics as gr, colors as col

class Bag(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        self.backButton = TextButton(self, Rect(4, gr.SCR_HT - 28 - 4, 52, 28), col.JOURNAL_SHADED, "Back", gr.FONT_12,
                                     col.BLACK, col.GRAY, yOffset=-2)

        self.berryButtons = []
        for i in range(0, len(BERRY_TYPES)):
            self.berryButtons.append(BerryButton(self, Rect(20+60*i, 72, 40, 40),
                                                 "src/assets/ui/berries/" + BERRY_TYPES[i] + ".png",
                                                 "src/assets/ui/berries/" + BERRY_TYPES[i] + "-gray.png", i))

    """ Loading """
    def load(self):
        for i in range(0, len(self.berryButtons)):
            self.berryButtons[i].setImageOn(self.state.berryCounts[i] > 0)

    """ Updating Methods """
    def update(self):
        self.backButton.mouseUpdate(self.mousePos)

    """ Input Methods """
    def mouseUp(self, position):
        if self.backButton.bounds.collidepoint(position):
            self.switchStage("world")

    """ Drawing Methods """
    def draw(self):
        #background
        self.drawUpRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)
        self.drawLowRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)

        #berry decor
        surface = gr.FONT_20.render("Berries", False, col.VERY_DARK_GRAY)
        self.drawLowImage(surface, Rect(90, 34, 0, 0))
        self.drawLowRect(col.JOURNAL_SHADED, Rect(14, 66, gr.SCR_WID-28, 52))

        #berries
        for button in self.berryButtons:
            button.draw()
        self.backButton.draw()