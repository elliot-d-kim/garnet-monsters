from src.stages.stage import Stage
from src.logic.ui import TriTextButton
import src.util.colors as col
import src.util.graphics as gr
from pygame import Rect
import pygame

class Credits(Stage):

    SCROLL_SPEED = 4

    def __init__(self, app, state):
        super().__init__(app, state)

        #prepare scroll
        self.scroll = 0

        #prepare ui
        self.backButton = TriTextButton(self, Rect(4, gr.SCR_HT-4-24, 48, 24),
                                        [col.TITLE_BUTTON_1, col.TITLE_BUTTON_2, col.TITLE_BUTTON_3], "BACK",
                                        gr.FONT_12, col.BLACK, col.VERY_LIGHT_GRAY, yOffset=-4)
        self.artUp = self.loadImage("src/assets/art/credits-art-up.png")

        self.strings = self.readStrings()
        for i in range(0, len(self.strings)):
            self.strings[i] = self.strings[i].replace('\n', '')

    """ Loading Methods """
    def load(self):
        super().load()

        self.scroll = 0
    @staticmethod
    def readStrings():
        # get the metadata
        inp = open("src/assets/credits.txt", "r")
        return inp.readlines()

    """ Input Methods """
    def mouseUp(self, position):
        if self.backButton.inBounds.collidepoint(position):
            self.switchStage("splash")

    """ Update Methods """
    def update(self):
        keys = pygame.key.get_pressed()

        # move the scroll
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.scroll += self.SCROLL_SPEED
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.scroll -= self.SCROLL_SPEED

        #clamp scroll
        if self.scroll > 0:
            self.scroll = 0
        elif self.scroll < -len(self.strings)*18 + min(len(self.strings), 14)*18:
            self.scroll = -len(self.strings)*18 + min(len(self.strings), 14)*18

        #update ui
        self.backButton.mouseUpdate(self.mousePos)

    """ Drawing Methods """
    def draw(self):
        #draw the backgrounds
        self.drawUpImage(self.artUp, gr.BOUND_SCR)
        self.drawLowRect(col.TITLE_BGROUND, gr.BOUND_SCR)

        #write the text
        y = self.scroll
        for string in self.strings:
            #main text
            surface = gr.FONT_12.render(string, False, col.GRAY)
            self.drawLowImage(surface, Rect(8, y, 0, 0))

            #highlights
            spl = string.split(" - ")
            if len(spl) > 1:
                surface = gr.FONT_12.render(spl[0] + " -", False, col.BLACK)
                self.drawLowImage(surface, Rect(8, y, 0, 0))

            y += 18

        #draw bottom bar
        self.drawLowRect(col.TITLE_BGROUND, Rect(0, gr.SCR_HT-32, gr.SCR_WID, 32))

        #draw instruction text
        if len(self.strings) > 14:
            textSurface = gr.FONT_8.render("Use Up and Down to scroll", False, col.DARK_GRAY)
            self.drawLowImage(textSurface, Rect(56, gr.SCR_HT-20, 0, 0))

        #draw ui elements
        self.backButton.draw()
