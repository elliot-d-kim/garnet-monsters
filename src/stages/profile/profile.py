from src.stages.stage import Stage
from src.util import graphics as gr
from src.util import colors as col
from src.logic.animal import TYPE_TO_CLASS, classFromType
from src.logic.ui import Label, MultiLabel, TextButton
from pygame import Rect
import pygame

class Profile(Stage):

    def __init__(self, app, state):
        super().__init__(app, state)

        # animal icons
        self.animalIcons = {}
        for idx in TYPE_TO_CLASS:
            # shrink animal icons to fit small boxes
            animalIcon = pygame.transform.scale(
                self.loadImage("src/assets/sprites/animals/" + classFromType(idx).getFilename() + ".png"),
                (52, 52))
            # iconFrameDimn = 10
            # if idx < len(TYPE_TO_CLASS)/2:
            #     iconX = round((gr.SCR_WID - iconFrameDimn) * 0.1) + idx*30
            #     iconY = round((gr.SCR_HT - iconFrameDimn) * 0.2) + idx*30
            # else:
            #     iconX = round((gr.SCR_WID - iconFrameDimn) * 0.1) + idx * 30
            #     iconY = round((gr.SCR_HT - iconFrameDimn) * 0.2) + idx * 30
            iconX, iconY = 0, 0         # values replaced under draw()
            self.animalIcons[idx] = [animalIcon, iconX, iconY]

        #back button
        self.backButton = TextButton(self, Rect(4, gr.SCR_HT-28-4, 52, 28), col.JOURNAL_SHADED, "Back", gr.FONT_12, col.BLACK, col.GRAY, yOffset=-2)

        #top display state
        self.profileImageFrame, self.profileImage = None, None
        self.playerName = MultiLabel(self, Rect(140, 120, 0, 0), "", gr.FONT_16, col.BLACK, 14, 18)
        self.licenseDateLabel = MultiLabel(self, Rect(140, 195, 0, 0), "", gr.FONT_12, col.BLACK, 20, 14)

    """ Loading Methods """
    def load(self):
        super().load()

        #top state
        self.loadTopDisplayState()

    def loadTopDisplayState(self):
        self.profileImageFrame = self.loadImage("src/assets/art/journal-image-frame.png")
        self.profileImage = None

        self.playerName.changeText("TRAINER")
        self.licenseDateLabel.changeText("")

    def unload(self):
        pass

    """ Update Methods """
    def update(self):
        self.backButton.mouseUpdate(self.mousePos)

    """ Input Methods """
    def mouseUp(self, position):
        if self.backButton.bounds.collidepoint(position):
            self.switchStage("world")

    """ Drawing Methods """
    def draw(self):
        #draw backgrounds
        self.drawUpRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)
        self.drawLowRect(col.JOURNAL_BGROUND, gr.BOUND_SCR)

        #draw lower title
        speciesTitleSurface = gr.FONT_20.render("Species", False, col.VERY_DARK_GRAY)
        speciesTitleRect = speciesTitleSurface.get_rect()
        self.drawLowImage(speciesTitleSurface, Rect(gr.SCR_WID/2-speciesTitleRect.w/2, 25, 0, 0))
        self.backButton.draw()

        # draw analyzed animal icons
        padding = (gr.SCR_WID - (14 * 2) - (52 * 5)) / 4        # set padding between boxes
        for idx in TYPE_TO_CLASS:
            iconBoxX = 14 + (52 + padding) * (idx % 5)                  # set x coord for e/ box
            iconBoxY = (gr.SCR_HT - 28 - 4) / 2 - 52 - padding / 2      # set y coord "

            # second row of boxes
            if idx >= 6:
                iconBoxY += 52 + padding
            self.drawLowRect(col.JOURNAL_SHADED, Rect(iconBoxX, iconBoxY, 52, 52))

            self.animalIcons[idx][1] = iconBoxX
            self.animalIcons[idx][2] = iconBoxY

        for a in self.state.analyzedAnimals:
            idx = a.getTypeId()
            self.drawLowImage(self.animalIcons[idx][0], Rect(self.animalIcons[idx][1], self.animalIcons[idx][2], 52, 52))

        #draw top stuff
        self.drawTopDetails()

    def drawTopDetails(self):
        # id card outline
        idCardWidth = gr.SCR_WID - 20 - 6
        idCardHeight = gr.SCR_HT - 108 - 6
        idCardX = (gr.SCR_WID - idCardWidth)/2
        idCardY = (gr.SCR_HT - idCardHeight) / 2
        self.drawUpRect(col.JOURNAL_SHADED, Rect(idCardX, idCardY, idCardWidth, idCardHeight))
        idCardMargin = 15

        # profile frame
        profileFrameDimn = self.profileImageFrame.get_width()
        # profileFrameX = idCardX + round((idCardWidth - profileFrameDimn)*0.1)
        profileFrameX = idCardX + idCardMargin
        # profileFrameY = idCardY + round((idCardHeight - profileFrameDimn)*0.2)
        profileFrameY = idCardY + idCardHeight - profileFrameDimn - idCardMargin
        self.drawUpImage(self.profileImageFrame, Rect(profileFrameX, profileFrameY, profileFrameDimn, profileFrameDimn))

        # profile image
        self.profileImage = self.loadImage("src/assets/sprites/chars/player-stand-down.png")
        profileImageDimn = self.profileImage.get_width()
        profileImageX = profileFrameX + round((profileFrameDimn - profileImageDimn) * 0.5)
        profileImageY = profileFrameY + round((profileFrameDimn - profileImageDimn) * 0.5)
        self.drawUpImage(self.profileImage, Rect(profileImageX, profileImageY, profileImageDimn, profileImageDimn))

        #banner
        self.drawUpRect(col.JOURNAL_SHADED_DARK, Rect(idCardX, idCardY+10, idCardWidth, 35))
        surface = gr.FONT_20.render("GARNET MONSTERS", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(35, 70, 0, 0))

        #name
        self.playerName.draw()

        # id no.
        surface = gr.FONT_12.render("ID NO.: " + self.state.playerID, False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(140, 143, 0, 0))

        #divider
        self.drawUpRect(col.BLACK, Rect(140, 168, idCardWidth - 2*idCardMargin - profileFrameDimn - 12, 2))

        #license date
        surface = gr.FONT_12.render("Licensed: ", False, col.VERY_DARK_GRAY)
        self.drawUpImage(surface, Rect(140, 180, 0, 0))
        self.licenseDateLabel.changeText(self.state.licenseDateStr)
        self.licenseDateLabel.draw()
