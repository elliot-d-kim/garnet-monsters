from src.stages.stage import Stage
from src.logic.ui import TriTextButton
import src.util.graphics as gr
import src.util.colors as col
from pygame import Rect
import json
from src.logic.animal import classFromType

class Splash(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        #declare assets
        self.titleArtUp = None
        self.titleArtLow = None

        #prepare ui elements
        self.playButton = TriTextButton(self, Rect(16, 120, gr.SCR_WID-32, 48),
                                        [col.TITLE_BUTTON_1, col.TITLE_BUTTON_2, col.TITLE_BUTTON_3], "PLAY",
                                        gr.FONT_28, col.BLACK, col.VERY_LIGHT_GRAY)
        self.loadButton = TriTextButton(self, Rect(16, 188, gr.SCR_WID/2 - 24, 32),
                                        [col.TITLE_BUTTON_1, col.TITLE_BUTTON_2, col.TITLE_BUTTON_3], "LOAD",
                                        gr.FONT_16, col.BLACK, col.VERY_LIGHT_GRAY, yOffset=-2)
        self.creditsButton = TriTextButton(self, Rect(gr.SCR_WID/2 + 12, 188, gr.SCR_WID/2 - 24, 32),
                                        [col.TITLE_BUTTON_1, col.TITLE_BUTTON_2, col.TITLE_BUTTON_3], "CREDITS",
                                        gr.FONT_16, col.BLACK, col.VERY_LIGHT_GRAY, yOffset=-2)

    """ Loading Methods """
    def load(self):
        super().load()

        #load assets
        self.titleArtUp = self.loadImage("src/assets/art/title-art-up.png")
        self.titleArtLow = self.loadImage("src/assets/art/title-art-low.png")
    def unload(self):
        #unload assets
        self.titleArtUp = None
        self.titleArtLow = None

    """ Input Methods """
    def mouseUp(self, position):
        if self.playButton.inBounds.collidepoint(position):
            self.switchStage("world")
        elif self.creditsButton.inBounds.collidepoint(position):
            self.switchStage("credits")
        elif self.loadButton.inBounds.collidepoint(position):
            try:
                # the file already exists
                with open('saveFile.txt') as load_file:
                    self.state.load = True

                    saveData = json.load(load_file)
                    self.state.area = saveData.get("area")
                    self.state.player_pos[0] = saveData.get("pos_x")
                    self.state.player_pos[1] = saveData.get("pos_y")
                    self.state.player_facing = saveData.get("facing")
                    self.state.analyzedAnimals = [classFromType(x) for x in saveData.get("analyzedAnimalsTypeIDs")]
                    self.state.berryCounts = saveData.get("berryCounts")
                    self.state.playerID = saveData.get("playerID")
                    self.state.licenseDateStr = saveData.get("licenseDateStr")

                    self.switchStage("world")
            except:
                pass

    """ Update Methods """
    def update(self):
        self.playButton.mouseUpdate(self.mousePos)
        self.loadButton.mouseUpdate(self.mousePos)
        self.creditsButton.mouseUpdate(self.mousePos)

    """ Draw Methods """
    def draw(self):
        #draw backgrounds
        self.drawUpImage(self.titleArtUp, Rect(0, 0, 0, 0))
        self.drawLowRect(col.TITLE_BGROUND, Rect(0, 0, gr.SCR_WID, gr.SCR_HT))

        #draw ui elements
        self.playButton.draw()
        self.loadButton.draw()
        self.creditsButton.draw()

        #draw text
        surface = gr.FONT_10.render("Arrow keys to move", False, col.VERY_DARK_GRAY)
        textRect = surface.get_rect()
        self.drawLowImage(surface, Rect(gr.SCR_WID/2-textRect.w/2, 232, 0, 0))
        surface = gr.FONT_10.render("Space to collect berries", False, col.VERY_DARK_GRAY)
        textRect = surface.get_rect()
        self.drawLowImage(surface, Rect(gr.SCR_WID/2-textRect.w/2, 244, 0, 0))
        surface = gr.FONT_10.render("Find animals in the tall grass!", False, col.VERY_DARK_GRAY)
        textRect = surface.get_rect()
        self.drawLowImage(surface, Rect(gr.SCR_WID/2 - textRect.w/2, 269, 0, 0))
