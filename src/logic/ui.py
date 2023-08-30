from abc import ABC, abstractmethod
import src.util.graphics as gr
from src.util import colors as col
from pygame import Rect

"""
An abstract class for ui elements.
"""
class UiElement(ABC):

    def __init__(self, stage, rect):
        self.stage = stage
        self.bounds = rect

    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def click(self, pos):
        pass

class TextBox(UiElement):

    CHAR_LIM = 28

    def __init__(self, stage, rect):
        super().__init__(stage, rect)

        self.outBounds = self.bounds
        self.inBounds = Rect(self.bounds.x+3, self.bounds.y+3, self.bounds.w-6, self.bounds.h-6)

        self.strings = []
        self.topString = 0
        self.texts = ["", ""]
        self.frame = 0

        self.triangleOverride = False

        self.downArrow1 = stage.loadImage("src/assets/ui/down-arrow-1.png")
        self.downArrow2 = stage.loadImage("src/assets/ui/down-arrow-2.png")

    """ UiElement Methods """
    def update(self):
        if len(self.texts[0]) < len(self.strings[0]):
            self.texts[0] += self.strings[0][len(self.texts[0])]
        elif len(self.texts[1]) < len(self.strings[1]):
            self.texts[1] += self.strings[1][len(self.texts[1])]

        self.frame += 1
    def draw(self):
        # border
        self.stage.drawLowRect(col.BLACK, self.outBounds)
        self.stage.drawLowRect(col.LIGHT_GRAY, self.inBounds)

        # corners
        self.stage.drawLowRect(col.BLACK, Rect(self.inBounds.x+3, self.inBounds.y+3, 3, 3))
        self.stage.drawLowRect(col.BLACK, Rect(self.inBounds.x+3, self.inBounds.y+self.inBounds.h-6, 3, 3))
        self.stage.drawLowRect(col.BLACK, Rect(self.inBounds.x+self.inBounds.w-6, self.inBounds.y+3, 3, 3))
        self.stage.drawLowRect(col.BLACK, Rect(self.inBounds.x+self.inBounds.w-6, self.inBounds.y+self.inBounds.h-6, 3, 3))

        # text
        text_surface = gr.FONT_12.render(self.texts[0], False, (0, 0, 0))
        self.stage.drawLowImage(text_surface, Rect(self.inBounds.x+10, self.inBounds.y+6, 0, 0))
        text_surface = gr.FONT_12.render(self.texts[1], False, (0, 0, 0))
        self.stage.drawLowImage(text_surface, Rect(self.inBounds.x+10, self.inBounds.y+6+16, 0, 0))

        # continue triangle
        if self.texts[1] == self.strings[1] and (len(self.strings) > 2 or self.triangleOverride):
            self.stage.drawLowImage(self.downArrow1, Rect(self.inBounds.x+self.inBounds.w-12, self.inBounds.y+self.inBounds.h-14, 7, 4))
    def click(self, pos):
        if self.inBounds.collidepoint(pos[0], pos[1]):
            if len(self.strings) > 2 and self.texts[1] == self.strings[1]:
                self.texts[0] = self.texts[1]
                self.texts[1] = ""
                self.strings.pop(0)

    """ Outward facing methods """
    def changeText(self, text):
        self.texts[0] = ""
        self.texts[1] = ""
        self.strings = []
        self.triangleOverride = False

        i = 0
        start = 0
        lastSpace = i
        #loop through all the text
        while i < len(text):
            #update last space
            if text[i] == ' ':
                lastSpace = i
            #create the string
            if i - start == self.CHAR_LIM:
                self.strings.append(text[start:lastSpace])
                start = lastSpace + 1

            i += 1

        #add the trailing text
        if i - start != 0:
            self.strings.append(text[start:i])

        #add a second string if necessary
        if len(self.strings) == 1:
            self.strings.append("")
    def showingAllText(self):
        return self.texts[1]==self.strings[1] and len(self.strings)<=2
    def showTriangleForThisText(self, show):
        # if true, will show triangle until the text is changed
        self.triangleOverride = show

class MenuButton(UiElement):

    CHAR_LIM = 10

    def __init__(self, stage, rect, text, justify = "center"):
        super().__init__(stage, rect)

        self.outBounds = self.bounds
        self.inBounds = Rect(self.bounds.x + 3, self.bounds.y + 3, self.bounds.w - 6, self.bounds.h - 6)

        self.text = text
        self.justify = justify
    def update(self):
        pass
    def draw(self, textColor=col.BLACK):
        # border
        self.stage.drawLowRect(col.BLACK, self.outBounds)
        self.stage.drawLowRect(col.JOURNAL_SHADED, self.inBounds)

        # text
        text_surface = gr.FONT_12.render(self.text, False, textColor)
        if self.justify == "center":
            self.stage.drawLowImage(text_surface,
                                    Rect(self.inBounds.x + self.inBounds.w/2 - text_surface.get_width()/2,
                                         self.inBounds.y + 6, 0, 0))
        elif self.justify == "right":
            self.stage.drawLowImage(text_surface,
                                    Rect(self.inBounds.x + self.inBounds.w - text_surface.get_width() - 10,
                                         self.inBounds.y + 6, 0, 0))
        else:   # left justify
            self.stage.drawLowImage(text_surface, Rect(self.inBounds.x + 10, self.inBounds.y + 6, 0, 0))

    def click(self, pos):
        pass

class ImgButton(UiElement):
    """
    Rect should be 6 wider and 6 taller than the image.
    """
    def __init__(self, stage, rect, imgPath):
        super().__init__(stage, rect)

        self.outBounds = self.bounds
        self.inBounds = Rect(self.bounds.x + 3, self.bounds.y + 3, self.bounds.w - 6, self.bounds.h - 6)

        self.image = stage.loadImage(imgPath)

    def update(self):
        pass
    def draw(self):
        self.stage.drawLowRect(col.BLACK, self.outBounds)
        self.stage.drawLowImage(self.image, self.inBounds)
    def click(self, pos):
        pass

    """
    Outward facing methods
    """
    def changeImage(self, path):
        self.image = self.stage.loadImage(path)

class BerryButton(ImgButton):
    def __init__(self, stage, rect, onPath, offPath, berryIdx):
        super().__init__(stage, rect, onPath)

        self.onImage = stage.loadImage(onPath)
        self.offImage = stage.loadImage(offPath)
        self.berryIdx = berryIdx

    def draw(self):
        super().draw()

        textSurf = gr.FONT_12.render(str(self.stage.state.berryCounts[self.berryIdx]), False, (255,255,255))
        self.stage.drawLowImage(textSurf, Rect(self.inBounds.x+1, self.inBounds.y-1, 0, 0))

    """
    Outward facing methods
    """
    def changeImage(self, path):
        print("Warning: BerryButton.changeImage(path) should not be used.")
    def setImageOn(self, boolean):
        if boolean:
            self.image = self.onImage
        else:
            self.image = self.offImage

class TextButton(UiElement):
    def __init__(self, stage, rect, backColor, text, font, textBaseCol, textHoverCol, yOffset=0):
        super().__init__(stage, rect)

        self.outBounds = self.bounds
        self.inBounds = Rect(self.bounds.x + 3, self.bounds.y + 3, self.bounds.w - 6, self.bounds.h - 6)

        self.backColor = backColor
        self.text = text
        self.yOffset = yOffset
        self.font = font
        self.textBaseCol = textBaseCol
        self.textHoverCol = textHoverCol

        self.displayTextColor = textBaseCol

    def update(self):
        pass
    def mouseUpdate(self, mousePos):
        if self.inBounds.collidepoint(mousePos):
            self.displayTextColor = self.textHoverCol
        else:
            self.displayTextColor = self.textBaseCol

    def draw(self):
        self.stage.drawLowRect(col.BLACK, self.outBounds)
        self.stage.drawLowRect(self.backColor, self.inBounds)

        textSurface = self.font.render(self.text, False, self.displayTextColor)
        textRect = textSurface.get_rect()
        self.stage.drawLowImage(textSurface, Rect(self.inBounds.x + self.inBounds.w / 2 - textRect.w / 2,
                                                  self.inBounds.y + 6 + self.yOffset, 0, 0))

    def click(self, pos):
        pass

class TriTextButton(UiElement):
    def __init__(self, stage, rect, backCols, text, font, textBaseCol, textHoverCol, yOffset=0):
        super().__init__(stage, rect)

        self.outBounds = self.bounds
        self.inBounds = Rect(self.bounds.x + 3, self.bounds.y + 3, self.bounds.w - 6, self.bounds.h - 6)

        self.backCols = backCols
        self.backRects = []
        for i in range(0, len(backCols)):
            self.backRects.append(Rect(self.inBounds.x, self.inBounds.y + self.inBounds.h*i/len(backCols),
                                       self.inBounds.w, self.inBounds.h*1/len(backCols)+1))

        self.text = text
        self.yOffset = yOffset
        self.textBaseCol = textBaseCol
        self.textHoverCol = textHoverCol
        self.font = font

        self.displayTextColor = textBaseCol

    def update(self):
        pass
    def mouseUpdate(self, mousePos):
        if self.inBounds.collidepoint(mousePos):
            self.displayTextColor = self.textHoverCol
        else:
            self.displayTextColor = self.textBaseCol

    def draw(self):
        self.stage.drawLowRect(col.BLACK, self.outBounds)

        for i in range(0, len(self.backRects)):
            self.stage.drawLowRect(self.backCols[i], self.backRects[i])

        textSurface = self.font.render(self.text, False, self.displayTextColor)
        textRect = textSurface.get_rect()
        self.stage.drawLowImage(textSurface, Rect(self.inBounds.x + self.inBounds.w/2 - textRect.w/2,
                                                  self.inBounds.y + 6 + self.yOffset, 0, 0))

    def click(self, pos):
        pass

class Label(UiElement):
    def __init__(self, stage, rect, text, font, textBaseCol, textHoverCol, drawLow=True):
        super().__init__(stage, rect)

        self.stage = stage
        self.rect = rect
        self.text = text
        self.font = font
        self.textBaseCol = textBaseCol
        self.textHoverCol = textHoverCol

        self.displayTextColor = textBaseCol
        self.drawLow = drawLow

    def update(self):
        pass
    def mouseUpdate(self, mousePos):
        if self.bounds.collidepoint(mousePos):
            self.displayTextColor = self.textHoverCol
        else:
            self.displayTextColor = self.textBaseCol

    def changeText(self, text):
        self.text = text

    def draw(self):
        text_surface = self.font.render(self.text, False, self.displayTextColor)
        if self.drawLow:
            self.stage.drawLowImage(text_surface, Rect(self.rect.x, self.rect.y + 6, 0, 0))
        else:
            self.stage.drawUpImage(text_surface, Rect(self.rect.x, self.rect.y + 6, 0, 0))

    def click(self, pos):
        pass

class MultiLabel(UiElement):
    def __init__(self, stage, rect, text, font, color, charLim, rowHt):
        super().__init__(stage, rect)

        self.text = text
        self.font = font
        self.color = color
        self.charLim = charLim
        self.rowHt = rowHt

        self.strings = []
        self.changeText(text)

    """ Base Methods """
    def update(self):
        pass
    def draw(self):
        for i in range (0, len(self.strings)):
            surface = self.font.render(self.strings[i], False, self.color)
            self.stage.drawUpImage(surface, Rect(self.bounds.x, self.bounds.y + i*self.rowHt, 0, 0))
    def click(self, pos):
        pass

    """ Changing """
    def changeText(self, text):
        self.text = text
        self.strings = []

        i = 0
        start = 0
        lastSpace = i
        # loop through all the text
        while i < len(text):
            # update last space
            if text[i] == ' ':
                lastSpace = i
            # create the string
            if i - start == self.charLim:
                self.strings.append(text[start:lastSpace])
                start = lastSpace + 1

            i += 1

        # add the trailing text
        if i - start != 0:
            self.strings.append(text[start:i])
    def changeTextColor(self, color):
        self.color = color